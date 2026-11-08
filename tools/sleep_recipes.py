"""Sleep-screen recipe test card (web recipes for 4-grey e-ink): 2×2 whole frames, 480×800 BMP turned 90° cw.
python3 -I sleep_recipes.py <src> <out.bmp> <x0> [--fix-color]
A: gamma 1.3 + sky-only roll-off (from 0.78) + dehaze 0.8 (Nikolai's pick 03.11.2026)
B: A + Floyd–Steinberg to 4 greys (Adafruit)   C: ImageMagick CLAHE + same curve + FS   D: A + ordered (Bayer) dither (InkFrame)
--dither: current pick vs step mapping vs FS vs Atkinson. --shadows: A, A + shadow lift 0.5 / 1.0, FS of lift 0.5.\nDither is applied at the final pixel size. Needs ImageMagick (brew install imagemagick)."""
import sys, subprocess, tempfile, os
from PIL import Image, ImageOps, ImageDraw, ImageFont
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import sleep_image as si
src, out, x0 = sys.argv[1], sys.argv[2], float(sys.argv[3]); tmp = tempfile.mkdtemp()
LEVELS = [0, 85, 170, 255]
def magick(*a): subprocess.run(['magick', *a], check=True)
def palette():
    p = os.path.join(tmp, 'pal.png'); Image.frombytes('L', (4, 1), bytes(LEVELS)).save(p); return p
def base(keep_white=True):
    im = Image.open(src).convert('RGB')
    if '--fix-color' in sys.argv: im = si.fix_color(im, keep_white)
    g = ImageOps.grayscale(im.crop(si.crop_box(*im.size, 800, 480, x0))).resize((800, 480), Image.LANCZOS)
    return ImageOps.autocontrast(g, cutoff=(0.3, 0.0))
def curve(g, lift=0.0): return g.point([round(255 * si.toe(si.shoulder((v / 255) ** 1.3, 1.0, 0.78), lift)) for v in range(256)])
def clahe(g):
    a, b = os.path.join(tmp, 'c_in.png'), os.path.join(tmp, 'c_out.png'); g.save(a)
    magick(a, '-clahe', '12x12%+128+2', b); return Image.open(b).convert('L')
def fs(g):
    a, b = os.path.join(tmp, 'f_in.png'), os.path.join(tmp, 'f_out.png'); g.save(a)
    magick(a, '-dither', 'FloydSteinberg', '-remap', palette(), b); return Image.open(b).convert('L')
def bayer(g):
    a, b = os.path.join(tmp, 'o_in.png'), os.path.join(tmp, 'o_out.png'); g.save(a)
    magick(a, '-ordered-dither', 'o4x4,4', b); return Image.open(b).convert('L')
def atkinson(g):
    # Atkinson dither to the 4 panel greys: spreads 6/8 of the error (lighter, cleaner highlights than FS)
    import numpy as np
    a = np.asarray(g, dtype=np.float32).copy(); h, w = a.shape; lv = np.array(LEVELS, dtype=np.float32)
    for y in range(h):
        for x in range(w):
            o = a[y, x]; n = lv[np.abs(lv - o).argmin()]; a[y, x] = n; e = (o - n) / 8
            for dx, dy in ((1, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (0, 2)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and yy < h: a[yy, xx] += e
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'), 'L')
def steps(g):
    # tone-to-step mapping: keep the column (~30 %) on the 33 % step, push the forest (~48 %) over the 50 % border
    pts = [(0, 0), (0.22, 0.2), (0.36, 0.33), (0.44, 0.58), (0.7, 0.72), (0.86, 0.86), (1, 1)]
    def f(v):
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if v <= x2: return y1 + (y2 - y1) * (v - x1) / (x2 - x1)
        return v
    return g.point([round(255 * f(v / 255)) for v in range(256)])
def posterize(g, cuts=(0.18, 0.40, 0.70)):
    # our own posterization to the 4 panel greys with chosen borders: the file looks exactly like the screen
    c = [round(255 * x) for x in cuts]
    return g.point([LEVELS[sum(v >= k for k in c)] for v in range(256)])
G = 4; cw, ch = (800 - G) // 2, (480 - G) // 2; sh = round(cw * 480 / 800); top = (sh - ch) // 2
fit = lambda g: g.resize((cw, sh), Image.LANCZOS).crop((0, top, cw, top + ch))
g = base(); hz = si.dehaze(g, 0.8)
if '--dither' in sys.argv:  # recipe «A + тени +» vs step mapping vs our own dithering
    A1 = fit(curve(hz, 0.5))
    cells = [('Сейчас', A1), ('Постеризация', posterize(A1)), ('Floyd–Steinberg', fs(A1)), ('Atkinson', atkinson(A1))]
elif '--shadows' in sys.argv:  # shadow-lift test on top of A
    A, A1, A2 = fit(curve(hz)), fit(curve(hz, 0.5)), fit(curve(hz, 1.0))
    cells = [('A · как сейчас', A), ('A + тени +', A1), ('A + тени ++', A2), ('B · тени + и Floyd–Steinberg', fs(A1))]
else:
    A = fit(curve(hz)); Cg = fit(curve(clahe(g)))
    cells = [('A · кривая + дымка', A), ('B · A + Floyd–Steinberg', fs(A)), ('C · CLAHE + FS', fs(Cg)), ('D · A + Bayer', bayer(A))]
card = Image.new('L', (800, 480), 255); d = ImageDraw.Draw(card)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 17)
for i, (lab, im) in enumerate(cells):
    x, y = (i % 2) * (cw + G), (i // 2) * (ch + G); card.paste(im, (x, y))
    w = d.textlength(lab, font=font); cx = x + cw / 2
    d.rounded_rectangle((cx - w / 2 - 8, y + ch - 32, cx + w / 2 + 8, y + ch - 6), radius=6, fill=255); d.text((cx - w / 2, y + ch - 29), lab, fill=0, font=font)
card.convert('RGB').rotate(-90, expand=True).save(out); print(out, [c[0] for c in cells])
