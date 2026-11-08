"""Sleep-screen test card: up to 4 whole frames 2×2, each with its own tone recipe, labelled; 480×800 BMP (90° cw).
python3 -I sleep_test_cells.py <src> <out.bmp> <x0> '<json list of cells>' [--fix-color]
cell: {"l": label, "g": gamma, "hl": highlight roll-off 0..1, "s": roll-off start 0..1, "z": dehaze 0..1}"""
import sys, json
from PIL import Image, ImageOps, ImageDraw, ImageFont
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import sleep_image as si
src, out, x0, cells = sys.argv[1], sys.argv[2], float(sys.argv[3]), json.loads(sys.argv[4])
G = 4; cw, ch = (800 - G) // 2, (480 - G) // 2; sh = round(cw * 480 / 800); top = (sh - ch) // 2
card = Image.new('L', (800, 480), 255); d = ImageDraw.Draw(card)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 18)
for i, c in enumerate(cells[:4]):
    kw = c.get('hl', 0) > 0
    im = Image.open(src).convert('RGB')
    if '--fix-color' in sys.argv: im = si.fix_color(im, kw)
    g = ImageOps.grayscale(im.crop(si.crop_box(*im.size, 800, 480, x0))).resize((800, 480), Image.LANCZOS)
    g = si.tone_gentle(g, c.get('g', 0.9), c.get('hl', 0), kw, c.get('s', 0.55), c.get('z', 0))  # tone at full size, then shrink
    g = g.resize((cw, sh), Image.LANCZOS).crop((0, top, cw, top + ch))
    x, y = (i % 2) * (cw + G), (i // 2) * (ch + G); card.paste(g, (x, y))
    w = d.textlength(c['l'], font=font); cx = x + cw / 2
    d.rounded_rectangle((cx - w / 2 - 8, y + ch - 32, cx + w / 2 + 8, y + ch - 6), radius=6, fill=255); d.text((cx - w / 2, y + ch - 29), c['l'], fill=0, font=font)
card.convert('RGB').rotate(-90, expand=True).save(out); print(out, [c['l'] for c in cells])
