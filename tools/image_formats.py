# Counts picture file extensions inside every EPUB under a folder. Usage: python -I -X utf8 tools/image_formats.py <folder>
import sys
import zipfile
from collections import Counter
from pathlib import Path

total = Counter()
for book in sorted(Path(sys.argv[1]).rglob("*.epub")):
    with zipfile.ZipFile(book) as z:
        exts = Counter(Path(n).suffix.lower() for n in z.namelist()
                       if Path(n).suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".webp"))
    total.update(exts)
    print(dict(exts), book.name)
print("total:", dict(total))
