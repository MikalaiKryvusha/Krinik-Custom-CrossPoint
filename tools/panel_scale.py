"""Calibration card for the e-ink panel: smooth gradient + 21 patches 0…100 % (step 5 %), labelled; 480×800 BMP (90° cw).
python3 -I panel_scale.py <out.bmp>  → photograph the sleep screen, read which patches look the same."""
import sys
from PIL import Image, ImageDraw, ImageFont
W, H = 800, 480; card = Image.new('L', (W, H), 255); d = ImageDraw.Draw(card)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 15)
for x in range(W): d.line([(x, 0), (x, 110)], fill=round(255 * x / (W - 1)))          # smooth gradient
for i in range(0, 101, 10):
    x = round((W - 1) * i / 100); d.line([(x, 110), (x, 122)], fill=0); d.text((max(2, min(x - 12, W - 42)), 124), f'{i}%', fill=0, font=font)
pw, ph, gap = 68, 140, 4; rows = [list(range(0, 55, 5)), list(range(55, 101, 5))]
for r, vals in enumerate(rows):
    y = 160 + r * (ph + 16)
    for c, v in enumerate(vals):
        x = 6 + c * (pw + gap); g = round(255 * v / 100)
        d.rectangle((x, y, x + pw, y + ph), fill=g, outline=0)
        lab = f'{v}'; w = d.textlength(lab, font=font)
        d.text((x + (pw - w) / 2, y + ph / 2 - 9), lab, fill=255 if v < 55 else 0, font=font)
card.convert('RGB').rotate(-90, expand=True).save(sys.argv[1]); print(sys.argv[1])
