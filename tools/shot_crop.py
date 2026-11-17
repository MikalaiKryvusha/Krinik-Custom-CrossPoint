# Crop a WebP/BMP shot around a box, scale it 6x, draw a 10 px grid with labels — to measure a TAP target. python -I -X utf8 shot_crop.py <in> <out.png> x0 y0 x1 y1
import sys
from PIL import Image, ImageDraw

src, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
im = Image.open(src).convert('RGB').crop((x0, y0, x1, y1))
k = 6
im = im.resize((im.width * k, im.height * k), Image.NEAREST)
d = ImageDraw.Draw(im)
for x in range(x0 - x0 % 10, x1, 10):
    if x < x0:
        continue
    d.line([((x - x0) * k, 0), ((x - x0) * k, im.height)], fill=(255, 0, 0), width=1)
    d.text(((x - x0) * k + 2, 2), str(x), fill=(255, 0, 0))
for y in range(y0 - y0 % 10, y1, 10):
    if y < y0:
        continue
    d.line([(0, (y - y0) * k), (im.width, (y - y0) * k)], fill=(0, 0, 255), width=1)
    d.text((2, (y - y0) * k + 2), str(y), fill=(0, 0, 255))
im.save(out)
