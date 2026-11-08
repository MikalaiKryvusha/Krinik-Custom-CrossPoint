"""Adapt images inside an unpacked EPUB for the X4 Pro in-book renderer (rules of Nikolai, 03.11.2026):
  keep — print-ready portraits / engravings (untouched)   bw — charts, tables, diagrams: hard black & white
  half — not print-ready portrait: levels + book correction ½   full — not print-ready scene / landscape: levels + full correction
python3 -I book_images.py <unpacked-dir> '<json {"file name": "bw|half|full|keep"}>' [--bw-threshold=0.72] [--dry DIR]
The file keeps its name and format (JPEG q92 / PNG), so the book's XHTML and manifest stay valid."""
import sys, os, json, glob
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sleep_image as si
d, rules = sys.argv[1], json.loads(sys.argv[2])
th = float(next((a.split('=')[1] for a in sys.argv if a.startswith('--bw-threshold=')), '0.72'))
dry = sys.argv[sys.argv.index('--dry') + 1] if '--dry' in sys.argv else None
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P', 'PA'):
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); im = Image.alpha_composite(bg, im.convert('RGBA'))
    return ImageOps.grayscale(im.convert('RGB'))
for name, mode in rules.items():
    found = [f for f in glob.glob(os.path.join(d, '**', name), recursive=True)]
    if len(found) != 1: print('не найдено однозначно:', name, found); continue
    f = found[0]
    if mode == 'keep': continue
    g = flat(Image.open(f))
    if mode == 'bw': g = g.point(lambda v: 0 if v < 255 * th else 255)
    else:
        g = ImageOps.autocontrast(g, cutoff=(0.5, 0.5))   # paper of the scan → white
        g = si.panel(g, si.BOOK_RESPONSE, 0.5 if mode == 'half' else 1.0)
    out = os.path.join(dry, name) if dry else f
    if f.lower().endswith(('.jpg', '.jpeg')): g.save(out, quality=92)
    else: g.save(out)
    print(f'{name}: {mode}')
