"""Darkroom-style test strip for the sleep screen: one whole frame cut into vertical strips, each in its own gamma.
python3 -I sleep_test_strip.py <src> <out.bmp> <x0> <gammas 0.9,1.0,...> <labels Сейчас,A,...> [--fix-color] [--hl=0,0.4,0.7,1] (highlight roll-off per cell; one gamma for all)
Default: whole frames 2×2 (up to 4); --strips: one frame cut into strips.\nOutput: 480×800 BMP (frame 800×480 turned 90° cw), labels small at the bottom of each strip."""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import sleep_image as si
a = [x for x in sys.argv[1:] if not x.startswith('--')]
src, out, x0 = a[0], a[1], float(a[2]); gammas = [float(g) for g in a[3].split(',')]; labels = a[4].split(',')
hls = [float(x) for x in next((o.split('=')[1] for o in sys.argv if o.startswith('--hl=')), '').split(',') if x] or [0.0] * len(gammas)
if len(gammas) == 1: gammas = gammas * len(hls)
def frame(keep_white):
    im = Image.open(src).convert('RGB')
    if '--fix-color' in sys.argv: im = si.fix_color(im, keep_white)
    g = ImageOps.grayscale(im.crop(si.crop_box(*im.size, 800, 480, x0))).resize((800, 480), Image.LANCZOS)
    return ImageOps.autocontrast(g, cutoff=(0.3, 0.0 if keep_white else 0.2))
base = {False: frame(False), True: frame(True)}
def toned(i, size=None):
    g = base[hls[i] > 0]
    if size: g = g.resize(size, Image.LANCZOS)
    return g.point([round(255 * si.shoulder((v / 255) ** gammas[i], hls[i])) for v in range(256)])
g0 = base[False]
n = len(gammas)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 18)
card = Image.new('L', (800, 480), 255)
def label(d, cx, y, lab):
    w = d.textlength(lab, font=font)
    d.rounded_rectangle((cx - w / 2 - 8, y, cx + w / 2 + 8, y + 26), radius=6, fill=255); d.text((cx - w / 2, y + 3), lab, fill=0, font=font)
if '--strips' in sys.argv:  # one frame cut into vertical strips
    edges = [round(800 * i / n) for i in range(n + 1)]
    for i, gm in enumerate(gammas):
        card.paste(toned(i).crop((edges[i], 0, edges[i + 1], 480)), (edges[i], 0))
    d = ImageDraw.Draw(card)
    for i in range(n):
        if i: d.line([(edges[i], 0), (edges[i], 479)], fill=255, width=2)
        label(d, (edges[i] + edges[i + 1]) / 2, 446, f'{labels[i]} · {gammas[i]:g}')
else:  # default: whole frames in a 2×2 grid, 4 px white gutters
    G = 4; cw, ch = (800 - G) // 2, (480 - G) // 2
    sh = round(cw * 480 / 800); top = (sh - ch) // 2
    d = ImageDraw.Draw(card)
    for i, gm in enumerate(gammas[:4]):
        x, y = (i % 2) * (cw + G), (i // 2) * (ch + G)
        card.paste(toned(i, (cw, sh)).crop((0, top, cw, top + ch)), (x, y))
        label(d, x + cw / 2, y + ch - 32, labels[i])
card.convert('RGB').rotate(-90, expand=True).save(out); print(out, list(zip(labels, gammas)))
