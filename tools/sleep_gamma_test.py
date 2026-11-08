"""Gamma test card for the sleep screen: the same frame 2×2 in four tones, labelled, as a 480×800 BMP (turned 90° cw).
python3 -I sleep_gamma_test.py <src> <out.bmp> [x0] [--fix-color] [gammas, default 0.9,1.0,1.2,1.4] [labels, e.g. Сейчас,A,B,C,D]\nUp to 4 → 2×2 full frames; 5–6 → 3×2, centre part of the frame."""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import sleep_image as si
args = [a for a in sys.argv[1:] if not a.startswith('--')]; src, out = args[0], args[1]
x0 = float(args[2]) if len(args) > 2 else 0.5
gammas = [float(g) for g in (args[3].split(',') if len(args) > 3 else ['0.9', '1.0', '1.2', '1.4'])]
im = Image.open(src).convert('RGB')
if '--fix-color' in sys.argv: im = si.fix_color(im)
labels = [a.split('=')[0] for a in (args[4].split(',') if len(args) > 4 else [])] or list('ABCDEF')
g0 = ImageOps.grayscale(im.crop(si.crop_box(*im.size, 800, 480, x0))).resize((400, 240), Image.LANCZOS)
g0 = ImageOps.autocontrast(g0, cutoff=(0.3, 0.2))
cols = 2 if len(gammas) <= 4 else 3; cw = 800 // cols; ch = 240
g0 = g0.crop(((400 - cw) // 2, 0, (400 - cw) // 2 + cw, 240)) if cw < 400 else g0
card = Image.new('L', (800, 480), 255)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 30)
for i, gm in enumerate(gammas):
    t = g0.point([round(255 * (v / 255) ** gm) for v in range(256)])
    x, y = (i % cols) * cw, (i // cols) * ch; card.paste(t, (x, y))
    d = ImageDraw.Draw(card); lab = f"{labels[i]} {gm:g}"; w = d.textlength(lab, font=font)
    d.rectangle((x, y, x + w + 14, y + 40), fill=0); d.text((x + 7, y + 3), lab, fill=255, font=font)
card.convert('RGB').rotate(-90, expand=True).save(out); print(out, list(zip(labels, gammas)))
