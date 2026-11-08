"""Sleep-screen image for the e-ink reader: crop to the screen ratio, tone for e-ink, simulate the screen.
python3 -I sleep_image.py <src> <out-prefix> [x0 fraction of spare width, 0..1, default 0.5] [W H, default 800 480]
    [--fix-color] (murky source: dehaze + exposure) [--gamma=0.9] (default 0.9) [--hl-start=0.55] [--haze=0..1] [--lift=0..1] (shadow lift) [--recipe5] (picked recipe) [--steps] (tone-to-step curve for 4 greys) [--panel] (inverse of the measured sleep-screen response; last step — NOT for the krinik firmware: it applies the same curve itself, prepare flat) [--book] (same for images inside EPUBs) [--hl=0..1] (highlight roll-off: sky under the white step, sun stays white;
    Nikolai picked gamma 1.3 + hl 1.0 for frame 5 from test cards, 03.11.2026) [--strong] (old engraving-like tone; owner found it «страшный», 03.11.2026)
Default tone is gentle: levels + slight mid lift, no local contrast, no sharpening, no dithering (firmware converts).
Writes <out>_gray.png (tone-corrected, the thing to convert to BMP) and <out>_eink.png (4-gray dithered simulation),
<out>_crop.jpg (source with the crop frame)."""
import sys
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageEnhance

def crop_box(w, h, W, H, x0):
    r = W / H
    if w / h > r:  # too wide: cut sides
        cw = round(h * r); left = round((w - cw) * x0); return (left, 0, left + cw, h)
    ch = round(w / r); top = round((h - ch) * x0); return (0, top, w, top + ch)

def fix_color(im, keep_white=False):
    # murky source: remove the haze cast per channel, slight gamma, a touch of saturation (approved by Nikolai 03.11.2026 on frame 5)
    im = Image.merge('RGB', [ImageOps.autocontrast(c, cutoff=(0.8, 0.0 if keep_white else 0.4)) for c in im.split()])
    im = im.point([round(255 * (i / 255) ** 0.82) for i in range(256)] * 3)
    return ImageEnhance.Color(im).enhance(1.12)

def shoulder(v, k, start=0.55):
    # highlight roll-off for e-ink: below 0.55 untouched; above, light tones pulled down so sky drops under the
    # panel's white step while the brightest (sun) stays white. k=0 off … 1 strong. v, result in 0..1
    if v <= start or k <= 0: return v
    w = 1 - start; u = (v - start) / w
    return start + w * ((1 - k) * u + k * u ** 2.2)

def toe(v, k, end=0.35):
    # shadow lift: below `end` blend toward v**0.6 (posts of the pier stop drowning in black); k 0..1; black stays black
    if v >= end or k <= 0: return v
    u = v / end; return end * ((1 - k) * u + k * u ** 0.6)

# Measured response of this X4 Pro (CrossPoint 2.0.0) sleep screen, 03.11.2026: photo of tools/panel_scale.py card,
# file % → seen % (0 = black patch, 100 = whitest patch). Banding seen by Nikolai at 10–15, 32–34 and a little at 50–65 %;
# plateau 35–55 % (all one tone).
PANEL_RESPONSE = [(0, 0), (5, 3), (10, 11), (15, 39), (20, 45), (25, 54), (30, 67), (35, 80),
                  (55, 80.5), (60, 86), (65, 91), (70, 95), (75, 98), (80, 99.6), (85, 100), (100, 100)]

# Images inside an EPUB (Settings → Images: Показать) go another way: firmware dithers them itself.
# Measured 03.11.2026 on Калибровка.epub: shadows crushed (≤15 % → black), mids honest, ≥95 % → white.
BOOK_RESPONSE = [(0, 0), (15, 1.9), (20, 8.3), (25, 15.5), (30, 21.2), (35, 28.6), (40, 36.4), (45, 42.3), (50, 50),
                 (55, 51.4), (60, 62.8), (65, 74.7), (70, 83.2), (75, 86.5), (80, 91.2), (85, 95.6), (90, 98.4), (95, 100), (100, 100)]

def panel(g, table=None, strength=1.0):
    # inverse of the measured response: wanted on-screen tone → file value; flat parts (plateaus) are never used
    table = table or PANEL_RESPONSE
    if table is PANEL_RESPONSE: pts = [(s, f) for f, s in table if not 35 < f <= 55 and f <= 85]
    else:
        pts, last = [], -1
        for f, s in table:
            if s > last: pts.append((s, f)); last = s
    def inv(seen):
        for (s1, f1), (s2, f2) in zip(pts, pts[1:]):
            if seen <= s2: return f1 + (f2 - f1) * (seen - s1) / (s2 - s1) if s2 > s1 else f2
        return 100
    # strength < 1 blends with «no correction» (the book shadows were over-lifted at 1.0, 03.11.2026)
    return g.point([round(255 * ((1 - strength) * v / 255 + strength * inv(100 * v / 255) / 100)) for v in range(256)])

def steps(g):
    # tone-to-step curve for the 4-grey panel: column of ruins (~30 %) stays on the 33 % step,
    # forest behind it (~48 %) is pushed over the 50 % border (Nikolai: «ступени были лучше», 03.11.2026)
    pts = [(0, 0), (0.22, 0.2), (0.36, 0.33), (0.44, 0.58), (0.7, 0.72), (0.86, 0.86), (1, 1)]
    def f(v):
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if v <= x2: return y1 + (y2 - y1) * (v - x1) / (x2 - x1)
        return v
    return g.point([round(255 * f(v / 255)) for v in range(256)])

def dehaze(g, amount):
    # local contrast for hazy frames: large-radius unsharp mask, no edge sharpening. amount 0..1 → percent
    return g.filter(ImageFilter.UnsharpMask(radius=40, percent=round(80 * amount), threshold=0)) if amount > 0 else g

def tone_gentle(g, gamma=0.9, hl=0.0, keep_white=False, hl_start=0.55, haze=0.0, lift=0.0):
    # minimal: levels + gamma; dithering is left to the firmware. 0.9 came out «белёсо» on the X4 Pro,
    # 1.3 is on trial for frame 5 on the reader (03.11.2026) — >1 darkens the mids
    g = ImageOps.autocontrast(g, cutoff=(0.3, 0.0 if keep_white else 0.2))
    g = dehaze(g, haze)
    return g.point([round(255 * toe(shoulder((i / 255) ** gamma, hl, hl_start), lift)) for i in range(256)])

def tone(g):
    # e-ink: blacks are heavy and mid-greys go dark → stretch levels, lift shadows, add local contrast
    g = ImageOps.autocontrast(g, cutoff=(0.5, 0.3))
    lut = [round(255 * (i / 255) ** 0.78) for i in range(256)]          # lift mids/shadows
    g = g.point(lut)
    g = g.filter(ImageFilter.UnsharpMask(radius=24, percent=35, threshold=0))  # «clarity»
    g = g.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=2))  # crisp edges at 220 ppi
    return g

def eink(g):
    # 4 grey levels with Floyd–Steinberg, painted in the panel's own tones (black is not black, white is warm paper)
    pal = Image.new('P', (1, 1)); pal.putpalette([0, 0, 0, 85, 85, 85, 170, 170, 170, 255, 255, 255] + [0] * 756)
    q = g.convert('RGB').quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG).convert('L')
    paper = {0: (30, 30, 30), 85: (105, 105, 103), 170: (172, 171, 166), 255: (233, 231, 224)}
    near = lambda i: paper[min(paper, key=lambda k: abs(k - i))]
    return Image.merge('RGB', [q.point([near(i)[c] for i in range(256)]) for c in range(3)])

if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    opts = [a for a in sys.argv[3:] if a.startswith('--')]; pos = [a for a in sys.argv[3:] if not a.startswith('--')]
    x0 = float(pos[0]) if pos else 0.5
    W, H = (int(pos[1]), int(pos[2])) if len(pos) > 2 else (800, 480)
    im = Image.open(src).convert('RGB')
    hl = float(next((o.split('=')[1] for o in opts if o.startswith('--hl=')), '0'))  # highlight roll-off 0..1
    if '--recipe5' in opts: hl = 1.0
    if '--fix-color' in opts: im = fix_color(im, keep_white=hl > 0); im.save(out + '_color.jpg', quality=90)
    box = crop_box(*im.size, W, H, x0)
    view = im.copy(); d = ImageDraw.Draw(view); lw = max(3, im.size[0] // 300)
    shade = Image.new('RGB', im.size, (0, 0, 0)); mask = Image.new('L', im.size, 150); ImageDraw.Draw(mask).rectangle(box, fill=0)
    view = Image.composite(shade, view, mask); ImageDraw.Draw(view).rectangle(box, outline=(255, 210, 0), width=lw)
    view.thumbnail((W, W)); view.save(out + '_crop.jpg', quality=85)
    g = ImageOps.grayscale(im.crop(box)).resize((W, H), Image.LANCZOS)
    gamma = float(next((o.split('=')[1] for o in opts if o.startswith('--gamma=')), '0.9'))
    num = lambda name, d: float(next((o.split('=')[1] for o in opts if o.startswith(f'--{name}=')), d))
    if '--recipe5' in opts:  # Nikolai's pick 03.11.2026: «A + тени +» (gamma 1.3, sky roll-off from 0.78, dehaze 0.8, shadow lift 0.5)
        gamma, hl = 1.3, 1.0; hs, hz, lf = 0.78, 0.8, 0.5
        if '--no-lift' in opts: lf = 0.0  # for books: the book correction lifts shadows itself
    else:
        hs, hz, lf = num('hl-start', 0.55), num('haze', 0), num('lift', 0)
    g = tone(g) if '--strong' in opts else tone_gentle(g, gamma, hl, keep_white=hl > 0, hl_start=hs, haze=hz, lift=lf)
    if '--steps' in opts: g = steps(g)
    if '--panel' in opts: g = panel(g)  # last: compensate this screen's response (sleep screen)
    if '--book' in opts or any(o.startswith('--book=') for o in opts):  # images inside books; --book=0.5 half strength
        g = panel(g, BOOK_RESPONSE, num('book', 1.0) if any(o.startswith('--book=') for o in opts) else 1.0)
    g.save(out + '_gray.png')
    # what goes to the reader: uncompressed 24-bit BMP in its own orientation (a landscape frame stays 800×480). The krinik
    # firmware draws own sleep images and the viewer in the reading orientation (04.11.2026). --portrait-file: the old
    # stock layout, turned 90° clockwise into a 480×800 file (stock CrossPoint draws sleep images in portrait).
    rgb = g.convert('RGB')
    (rgb.rotate(-90, expand=True) if '--portrait-file' in opts else rgb).save(out + '.bmp')
    if '--sim' in opts: eink(g).save(out + '_eink.png')  # screen simulation only on request
    print(out, im.size, 'crop', box)
