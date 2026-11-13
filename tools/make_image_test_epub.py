# Builds a small EPUB 3 test book with pictures and captions (own generated content, safe for the public repo) for the
# simulator runs of ideas 02 (tap a picture → full screen) and 03 (keep a caption with its picture).
# Usage: python -I tools/make_image_test_epub.py <out.epub> [--figure]   (Pillow: the .pio-venv python)
#   default   — captions as in the owner's FB2-converted books: <div><img/></div><p><em>Рис. N. …</em></p>
#   --figure  — the standard markup: <figure><img/><figcaption>Рис. N. …</figcaption></figure>
import io
import sys
import zipfile

from PIL import Image, ImageDraw

# Picture sizes chosen against the landscape page (800×480 logical, minus margins and the status bar):
# a wide one that leaves room for text, a tall one that fills the page height, a small one beside text.
PICTURES = [
    ("pic1.jpg", (600, 260), "1"),
    ("pic2.jpg", (300, 640), "2"),
    ("pic3.png", (240, 160), "3"),
]
FILLER = (
    "Это проверочный абзац тестовой книги. Он нужен, чтобы картинки стояли на странице не одни, а среди текста, "
    "как в настоящей книге: строка за строкой, с переносами и отступом первой строки."
)


def media_type(name):
    return "image/png" if name.endswith(".png") else "image/jpeg"


def picture_bytes(name, size, label):
    """A gray test card: a frame, diagonal bands and a big label, so the full-screen view is easy to tell apart.
    JPEG or PNG by the file name — the owner's sample book mixes both (103 JPEG + 77 PNG)."""
    w, h = size
    img = Image.new("L", size, 235)
    draw = ImageDraw.Draw(img)
    for i in range(-h, w, 40):
        draw.line([(i, 0), (i + h, h)], fill=150, width=12)
    draw.rectangle([0, 0, w - 1, h - 1], outline=0, width=6)
    # Orientation mark: a black triangle in the top-left corner, so a quarter turn is told clockwise from
    # counterclockwise in a shot (the diagonal bands look alike after either turn) — the viewer rotation of idea 07.
    mark = min(w, h) // 3
    draw.polygon([(0, 0), (mark, 0), (0, mark)], fill=0)
    box = min(w, h) // 2
    draw.rectangle([w // 2 - box // 2, h // 2 - box // 2, w // 2 + box // 2, h // 2 + box // 2], fill=0)
    draw.text((w // 2 - 4, h // 2 - 6), label, fill=255)
    out = io.BytesIO()
    if name.endswith(".png"):
        img.save(out, "PNG")
    else:
        img.save(out, "JPEG", quality=90)
    return out.getvalue()


def picture_block(name, number, figure):
    caption = f"Рис. {number}. Тестовая картинка номер {number} с подписью под ней."
    if figure:
        return (f'<figure class="fig"><img src="images/{name}" alt=""/>'
                f"<figcaption>{caption}</figcaption></figure>")
    return f'<div class="image"><img src="images/{name}" alt=""/></div><p class="p1"><em>{caption}</em></p>'


def chapter_xhtml(figure):
    paragraphs = [f'<p class="p1">{FILLER}</p>']
    body = ['<h2>Глава 1. Картинки</h2>', picture_block(PICTURES[0][0], 1, figure)]
    body += paragraphs * 3
    body.append(picture_block(PICTURES[1][0], 2, figure))
    body += paragraphs * 2
    body.append(picture_block(PICTURES[2][0], 3, figure))
    body += paragraphs * 4
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru"><head><title>Глава 1</title>'
        '<link rel="stylesheet" type="text/css" href="style.css"/></head><body>' + "".join(body) + "</body></html>"
    )


STYLE = (
    ".p1 { margin: 0; text-align: justify; text-indent: 1.5em; }\n"
    ".image { text-align: center; }\n"
    ".fig { break-inside: avoid; page-break-inside: avoid; text-align: center; }\n"
)
CONTAINER = (
    '<?xml version="1.0"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
    '<rootfiles><rootfile full-path="OPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>'
    "</container>"
)
NAV = (
    '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" '
    'xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Оглавление</title></head><body>'
    '<nav epub:type="toc"><ol><li><a href="ch1.xhtml">Глава 1. Картинки</a></li></ol></nav></body></html>'
)


def opf(title):
    items = "".join(f'<item id="i{n}" href="images/{name}" media-type="{media_type(name)}"/>'
                    for n, (name, _, _) in enumerate(PICTURES, 1))
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
        'unique-identifier="id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
        f'<dc:identifier id="id">kccp-image-test</dc:identifier><dc:title>{title}</dc:title>'
        '<dc:language>ru</dc:language><dc:creator>KCCP</dc:creator>'
        '<meta property="dcterms:modified">2026-11-13T00:00:00Z</meta></metadata><manifest>'
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
        '<item id="css" href="style.css" media-type="text/css"/>'
        f'<item id="ch1" href="ch1.xhtml" media-type="application/xhtml+xml"/>{items}</manifest>'
        '<spine><itemref idref="ch1"/></spine></package>'
    )


def main():
    out = sys.argv[1]
    figure = "--figure" in sys.argv[2:]
    title = "Тест картинок (figure)" if figure else "Тест картинок"
    with zipfile.ZipFile(out, "w") as z:
        # mimetype first and stored, as the OCF container requires.
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", CONTAINER, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OPS/content.opf", opf(title), compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OPS/nav.xhtml", NAV, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OPS/style.css", STYLE, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OPS/ch1.xhtml", chapter_xhtml(figure), compress_type=zipfile.ZIP_DEFLATED)
        for name, size, label in PICTURES:
            z.writestr(f"OPS/images/{name}", picture_bytes(name, size, label), compress_type=zipfile.ZIP_STORED)
    print(out)


main()
