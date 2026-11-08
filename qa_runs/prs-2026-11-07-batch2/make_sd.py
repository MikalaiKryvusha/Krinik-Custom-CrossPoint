# Builds the simulator SD cards for batch-2 PR frames. python3 -I make_sd.py
import json, shutil, zipfile, pathlib
R = pathlib.Path(__file__).resolve().parent
T = pathlib.Path('/Users/kryvusha/Xteink/qa_runs/sd_template')
FW = pathlib.Path('/Users/kryvusha/Xteink/firmware/test/epubs')
TITLE = 'The Life and Strange Surprizing Adventures of Robinson Crusoe, of York, Mariner'

def crusoe(path):
    opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="id">crusoe-demo</dc:identifier>
<dc:title>{TITLE}</dc:title><dc:creator>Daniel Defoe</dc:creator><dc:language>en</dc:language>
<meta property="dcterms:modified">2026-11-07T00:00:00Z</meta></metadata>
<manifest><item id="c1" href="c1.xhtml" media-type="application/xhtml+xml"/>
<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/></manifest>
<spine><itemref idref="c1"/></spine></package>'''
    page = '<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>I</title></head><body><p>I was born in the year 1632, in the city of York, of a good family.</p></body></html>'
    nav = '<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Nav</title></head><body><nav epub:type="toc"><ol><li><a href="c1.xhtml">I</a></li></ol></nav></body></html>'
    cont = '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', cont); z.writestr('content.opf', opf)
        z.writestr('c1.xhtml', page); z.writestr('nav.xhtml', nav)

def card(name, inverted=0, open_book=''):
    sd = R / 'sd' / name
    shutil.rmtree(sd, ignore_errors=True); (sd / '.crosspoint').mkdir(parents=True); (sd / 'Books').mkdir()
    s = json.loads((T / '.crosspoint/settings.json').read_text())
    s.update(language='EN', uiTheme=1, screenInverted=inverted, imageRendering=0)
    (sd / '.crosspoint/settings.json').write_text(json.dumps(s, indent=1))
    crusoe(sd / 'Books/Robinson Crusoe.epub')
    shutil.copy(FW / 'test_jpeg_images.epub', sd / 'Books/JPEG Image Tests.epub')
    (sd / '.crosspoint/recent.json').write_text(json.dumps({'books': [
        {'path': '/Books/Robinson Crusoe.epub', 'title': TITLE, 'author': 'Daniel Defoe', 'coverBmpPath': ''}]}))
    if open_book:
        (sd / '.crosspoint/state.json').write_text(json.dumps({'openEpubPath': open_book, 'showBootScreen': False}))

card('home')
card('night', inverted=1, open_book='/Books/JPEG Image Tests.epub')
card('day', inverted=0, open_book='/Books/JPEG Image Tests.epub')
print('cards:', sorted(p.name for p in (R / 'sd').iterdir()))
