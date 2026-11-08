# Simulator BMP screenshots → WebP q80 (half size). python3 -I shot_webp.py <dir-or-files...>
import sys, pathlib
from PIL import Image
paths = []
for a in sys.argv[1:]:
    p = pathlib.Path(a)
    paths += sorted(p.glob('*.bmp')) if p.is_dir() else [p]
for p in paths:
    im = Image.open(p).convert('L')
    im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    out = p.with_suffix('.webp'); im.save(out, 'WEBP', quality=80); p.unlink()
    print(out, im.size)
