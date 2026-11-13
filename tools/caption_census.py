# Counts, per EPUB in a folder (recursive), how pictures and their captions are marked up: <img>/<image>, <figure>,
# <figcaption>, and a paragraph starting with "Рис"/"Fig" right after a picture. Read-only; prints a table.
# Usage: .pio-venv/Scripts/python.exe -I -X utf8 tools/caption_census.py <folder with EPUBs>
import re
import sys
import zipfile
from pathlib import Path

IMG = re.compile(rb"<(?:img|image)\b", re.I)
FIGURE = re.compile(rb"<figure\b", re.I)
FIGCAPTION = re.compile(rb"<figcaption\b", re.I)
AVOID = re.compile(rb"(?:page-)?break-(?:inside|after)\s*:\s*avoid", re.I)
# A picture, its closing wrappers, then a paragraph whose text begins with a figure label.
LABEL_AFTER_IMG = re.compile(
    rb"<(?:img|image)\b[^>]*>(?:\s*</(?:div|p|span|a|svg)>)*\s*<p\b[^>]*>\s*(?:<[^>]+>\s*)*"
    rb"(?:\xd0\xa0\xd0\xb8\xd1\x81|\xd0\xa0\xd0\xb8\xd1\x81\xd1\x83\xd0\xbd\xd0\xbe\xd0\xba|Fig|Figure)",
    re.I,
)


def census(path: Path):
    imgs = figures = figcaptions = labels = avoid = 0
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            low = name.lower()
            data = z.read(name) if low.endswith((".xhtml", ".html", ".htm", ".css")) else b""
            if not data:
                continue
            if low.endswith(".css"):
                avoid += len(AVOID.findall(data))
                continue
            imgs += len(IMG.findall(data))
            figures += len(FIGURE.findall(data))
            figcaptions += len(FIGCAPTION.findall(data))
            labels += len(LABEL_AFTER_IMG.findall(data))
    return imgs, figures, figcaptions, labels, avoid


def main():
    root = Path(sys.argv[1])
    books = sorted(root.rglob("*.epub"))
    total = [0, 0, 0, 0]
    with_pics = 0
    sys.stdout.reconfigure(encoding="utf-8")
    print("img\tfigure\tfigcap\tRis_after_img\tcss_avoid\tbook")
    for book in books:
        try:
            imgs, figures, figcaptions, labels, avoid = census(book)
        except (zipfile.BadZipFile, OSError) as e:
            print(f"-\t-\t-\t-\t-\t{book.name} (unreadable: {e})")
            continue
        if imgs > 1:
            with_pics += 1
        for i, v in enumerate((imgs, figures, figcaptions, labels)):
            total[i] += v
        print(f"{imgs}\t{figures}\t{figcaptions}\t{labels}\t{avoid}\t{book.name}")
    print(f"books: {len(books)}, with >1 picture: {with_pics}, totals img/figure/figcaption/Ris-after-img: {total}")


main()
