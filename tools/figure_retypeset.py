# Re-typesets a COPY of an EPUB: a picture block followed by a «Рис. N…» / «Fig. N…» paragraph becomes
# <figure class="kccp-figure">picture<figcaption>…</figcaption></figure> + CSS break-inside: avoid (epic 07 Ф3, plan 14).
# The input is never changed. Usage: .pio-venv/Scripts/python.exe -I -X utf8 tools/figure_retypeset.py <in.epub> [<out.epub>] [--list]
#                                    .pio-venv/Scripts/python.exe -I -X utf8 tools/figure_retypeset.py --selftest
#
# [TESTED: 2026-11-17 · the test book: selftest (proven red by 9 mutants), census 3·3·0, simulator pages, the judge ·
#  testcases/reports/2026-11-17_epic07_p3.md] [NOT-TESTED] the owner's two books (T9: the reader not on the wire).
import io
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote

FIGURE_CLASS = "kccp-figure"
CSS_RULE = (b"\n/* KCCP epic 07: keep a picture and its caption on one page */\n"
            b"figure." + FIGURE_CLASS.encode() + b" { break-inside: avoid; page-break-inside: avoid; }\n")
OWN_CSS_NAME = "kccp-figure.css"
DOC_EXT = (".xhtml", ".html", ".htm")

# One token = a comment, a CDATA block, a declaration / processing instruction, a tag (a '>' inside a quoted attribute
# value stays inside the tag), or a run of text.
TOKEN = re.compile(r"""<!--.*?-->|<!\[CDATA\[.*?\]\]>|<[!?][^>]*>|<(?:[^>"']|"[^"]*"|'[^']*')*>|[^<]+""", re.S)
TAG_NAME = re.compile(r"<\s*/?\s*([A-Za-z][\w:.-]*)")
# HTML void elements: an XHTML book closes them with "/>", a sloppy one may not — both count as self-closed.
VOID = {"img", "br", "hr", "meta", "link", "input", "col", "area", "base", "wbr", "source", "param", "embed"}
PICTURE = {"img", "image"}
# The caption label: «Рис.» / «Рисунок» / «Fig.» / «Figure» (or in capitals) and then a number — «Рис. 2. …»,
# «Рисунок 3 – …», «Figure 7.». The census (tools/caption_census.py) counts any «Рис…» start; a body paragraph after a
# picture that only begins with those letters («Риск был велик…», «Fighting broke out…») is NOT a caption (the plan 14
# judge, finding 1).
LABEL = re.compile(r"(?:Рис(?:\.|унок)|РИС(?:\.|УНОК)|Fig(?:\.|ure)|FIG(?:\.|URE))(?:\s|&nbsp;|&#160;|&#xa0;)*\d")
SPACE = re.compile(r"(?:\s|&nbsp;|&#160;|&#xa0;| )*$", re.I)


def kind_of(tok):
    """'text' · 'other' (comment, CDATA, <!…>, <?…?>) · 'close' · 'self' · 'open'; plus the local tag name."""
    if not tok.startswith("<"):
        return "text", ""
    if tok.startswith("<!") or tok.startswith("<?"):
        return "other", ""
    m = TAG_NAME.match(tok)
    if not m:
        return "text", ""                       # a stray '<' — never a tag, never matched
    name = m.group(1).split(":")[-1].lower()     # <svg:image> → image
    if tok.lstrip("< \t").startswith("/"):
        return "close", name
    if tok.rstrip("> \t\r\n").endswith("/") or name in VOID:
        return "self", name
    return "open", name


def is_blank(text):
    return SPACE.match(text) is not None


ATTRS = re.compile(r"""\s([\w:.-]+)(\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>"']+))?""")
# A caption paragraph's class and inline style belong to the BODY paragraph (Hofstadter: class p1 = text-align: justify,
# text-indent) — on a <figcaption> they would beat the firmware's centred caption. Standard Ebooks styles a caption by the
# figcaption element itself (Manual 1.9.1 §7.8.5.2). id, lang, dir and the rest stay (a link may point at the id).
DROPPED_ON_CAPTION = {"class", "style"}


def caption_open_tag(p_tag):
    """'<p id="f" class="p1">' → '<figcaption id="f">'."""
    body = p_tag[TAG_NAME.match(p_tag).end():].rstrip(">").rstrip()
    kept = [m.group(0) for m in ATTRS.finditer(body) if m.group(1).lower() not in DROPPED_ON_CAPTION]
    return "<figcaption" + "".join(kept) + ">"


def retypeset_doc(src, captions=None):
    """One XHTML document → (new text, number of pairs re-typeset). Text outside the pairs is copied byte for byte.
    `captions`, when given, receives the plain text of every caption wrapped (for --list)."""
    toks = TOKEN.findall(src)
    kinds = [kind_of(t) for t in toks]
    n = len(toks)

    # Matching tags both ways and "inside a <figure>" — one forward pass with a stack.
    match = [-1] * n
    in_figure = [False] * n
    stack = []
    for i, (k, name) in enumerate(kinds):
        in_figure[i] = any(kinds[j][1] == "figure" for j in stack)
        if k == "open":
            stack.append(i)
        elif k == "close":
            # pop to the nearest open element of the same name (tolerates a sloppy unclosed inline tag)
            for depth in range(len(stack) - 1, -1, -1):
                if kinds[stack[depth]][1] == name:
                    match[stack[depth]] = i
                    match[i] = stack[depth]
                    del stack[depth:]
                    break

    def first_text_is_label(p_open, p_close):
        for j in range(p_open + 1, p_close):
            k, _ = kinds[j]
            if k == "text":
                if is_blank(toks[j]):
                    continue
                return LABEL.match(toks[j].lstrip(" \t\r\n ")) is not None
            if k in ("other",):
                continue
        return False

    def previous_sibling(p_open):
        """(start, end) of the element right before the <p>, or None when text or the parent's start is there."""
        j = p_open - 1
        while j >= 0:
            k, _ = kinds[j]
            if k == "other" or (k == "text" and is_blank(toks[j])):
                j -= 1
                continue
            if k == "self":
                return j, j
            if k == "close" and match[j] >= 0:
                return match[j], j
            return None                                     # text, or <p> is the parent's first child
        return None

    def is_picture_block(start, end):
        has_picture = False
        for j in range(start, end + 1):
            k, name = kinds[j]
            if k == "text" and not is_blank(toks[j]):
                return False
            if k in ("open", "self") and name in PICTURE:
                has_picture = True
            if name in ("figure", "figcaption"):
                return False
        return has_picture

    before = {}      # token index → text inserted before it
    after = {}       # token index → text inserted after it
    replace = {}     # token index → replacement token
    pairs = 0
    for i, (k, name) in enumerate(kinds):
        if k != "open" or name != "p" or in_figure[i] or match[i] < 0:
            continue
        close = match[i]
        if not first_text_is_label(i, close):
            continue
        sib = previous_sibling(i)
        if sib is None or not is_picture_block(*sib):
            continue
        start = sib[0]
        before[start] = before.get(start, "") + '<figure class="' + FIGURE_CLASS + '">'
        if captions is not None:
            captions.append(" ".join("".join(toks[j] for j in range(i + 1, close) if kinds[j][0] == "text").split()))
        replace[i] = caption_open_tag(toks[i])
        mc = TAG_NAME.match(toks[close])
        replace[close] = toks[close][:mc.start(1)] + "figcaption" + toks[close][mc.end(1):]
        after[close] = "</figure>" + after.get(close, "")
        pairs += 1

    if not pairs:
        return src, 0
    out = []
    for i, tok in enumerate(toks):
        out.append(before.get(i, ""))
        out.append(replace.get(i, tok))
        out.append(after.get(i, ""))
    return "".join(out), pairs


LINK = re.compile(r"<link\b[^>]*>", re.I)
ATTR = r"""\b{}\s*=\s*(?:"([^"]*)"|'([^']*)')"""


def attr(tag, name):
    m = re.search(ATTR.format(name), tag, re.I)
    return (m.group(1) if m.group(1) is not None else m.group(2)) if m else None


def first_stylesheet(doc_text):
    for tag in LINK.findall(doc_text):
        rel = (attr(tag, "rel") or "").lower().split()
        if "stylesheet" in rel and attr(tag, "href"):
            return unquote(attr(tag, "href").split("#")[0].split("?")[0])   # my%20style.css → my style.css
    return None


def add_link(doc, rel):
    """A <link> to rel at the end of the document's head; '<head/>' opens. None when the document has no head."""
    link = '<link rel="stylesheet" type="text/css" href="' + rel + '"/>'
    if "</head>" in doc:
        return doc.replace("</head>", link + "</head>", 1)
    m = re.search(r"<head\s*/>", doc)
    return doc[:m.start()] + "<head>" + link + "</head>" + doc[m.end():] if m else None


def opf_path(z):
    container = z.read("META-INF/container.xml").decode("utf-8", "replace")
    m = re.search(r"""full-path\s*=\s*["']([^"']+)["']""", container)
    if not m:
        raise ValueError("META-INF/container.xml names no OPF")
    return m.group(1)


def epub_version(opf_text):
    m = re.search(r"<(?:[\w.-]+:)?package\b[^>]*>", opf_text)          # <package …> or <opf:package …>
    v = attr(m.group(0), "version") if m else None
    return v or "?"


def retypeset_epub(src_bytes):
    """EPUB bytes → (new EPUB bytes or None, report dict). None = nothing written (EPUB 2, or no pairs).
    report["captions"] = [(document, caption text)] of every pair wrapped, in book order of the zip."""
    report = {"version": "?", "docs": 0, "pairs": 0, "css": [], "skipped": [], "nohead": [], "captions": []}
    with zipfile.ZipFile(io.BytesIO(src_bytes)) as z:
        infos = z.infolist()
        names = {i.filename for i in infos}
        opf = opf_path(z)
        opf_text = z.read(opf).decode("utf-8", "replace")
        report["version"] = epub_version(opf_text)
        if not report["version"].startswith("3"):
            return None, report                                   # plan 14 risk 1: EPUB 2 waits for a decision
        new = {}
        css_to_extend = set()
        own_css_docs = []
        for info in infos:
            low = info.filename.lower()
            if not low.endswith(DOC_EXT):
                continue
            raw = z.read(info.filename)
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                report["skipped"].append(info.filename)
                continue
            caps = []
            out, pairs = retypeset_doc(text, caps)
            if not pairs:
                continue
            report["captions"] += [(info.filename, c) for c in caps]
            report["docs"] += 1
            report["pairs"] += pairs
            href = first_stylesheet(out)
            css = posixpath.normpath(posixpath.join(posixpath.dirname(info.filename), href)) if href else None
            if css in names:
                css_to_extend.add(css)
            else:
                own_css_docs.append(info.filename)
            new[info.filename] = out
        if not report["pairs"]:
            return None, report
        for css in sorted(css_to_extend):
            data = z.read(css)
            if FIGURE_CLASS.encode() not in data:
                new[css] = data + CSS_RULE
            report["css"].append(css)
        added = []
        if own_css_docs:
            # Fallback: a changed document with no stylesheet of its own gets kccp-figure.css next to the OPF.
            own = posixpath.join(posixpath.dirname(opf), OWN_CSS_NAME)
            if own not in names:
                added.append((own, CSS_RULE.lstrip(b"\n")))
                opf_text = opf_text.replace(
                    "</manifest>", '<item id="kccp-figure-css" href="' + OWN_CSS_NAME + '" media-type="text/css"/></manifest>', 1)
                new[opf] = opf_text
            for doc in own_css_docs:
                rel = posixpath.relpath(own, posixpath.dirname(doc) or ".")
                linked = add_link(new[doc], rel)
                if linked is None:
                    report["nohead"].append(doc)          # said in the summary line: the rule does not reach it
                else:
                    new[doc] = linked
            report["css"].append(own)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zout:
            for info in infos:                                    # same order: mimetype stays first and stored
                data = new.get(info.filename, None)
                if data is None:
                    data = z.read(info.filename)
                elif isinstance(data, str):
                    data = data.encode("utf-8")
                zout.writestr(info, data, compress_type=info.compress_type)
            for name, data in added:
                zout.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
        return buf.getvalue(), report


def selftest():
    fails = []

    def case(name, src, want_pairs, want=None):
        out, pairs = retypeset_doc(src)
        if pairs != want_pairs or (want is not None and out != want):
            fails.append(f"{name}: pairs {pairs} (want {want_pairs})" + ("" if want is None or out == want else f"\n  got  {out}\n  want {want}"))
        return out

    owner = '<div class="image"><img class="z1" src="a.jpg" alt=""/></div>\n<p class="p1"><em>Рис. 2. Адольф.</em></p>'
    out = case("owner's markup", owner, 1,
               '<figure class="kccp-figure"><div class="image"><img class="z1" src="a.jpg" alt=""/></div>\n'
               '<figcaption><em>Рис. 2. Адольф.</em></figcaption></figure>')
    case("second run changes nothing", out, 0, out)
    case("bare img", '<p>Текст.</p><img src="a.png"/><p>Рисунок 3 – Схема</p>', 1)
    case("void img without slash", '<div><img src="a.png"></div><p>Рис. 4.</p>', 1)
    case("svg image", '<div><svg xmlns="http://www.w3.org/2000/svg"><image href="a.png"/></svg></div><p>Рис. 5.</p>', 1)
    case("nested inline tags", '<div><img src="a"/></div><p class="c"><span><strong>Рис. 6.</strong> Кот</span></p>', 1,
         '<figure class="kccp-figure"><div><img src="a"/></div><figcaption><span><strong>Рис. 6.</strong> Кот'
         '</span></figcaption></figure>')
    case("id and lang kept, class and style dropped",
         '<img src="a"/><p id="fig2" class="p1" style="text-align: left" xml:lang="ru">Рис. 2.</p>', 1,
         '<figure class="kccp-figure"><img src="a"/><figcaption id="fig2" xml:lang="ru">Рис. 2.</figcaption></figure>')
    case("english label", '<div><img src="a"/></div><p>Figure 7. A cat</p>', 1)
    case("picture then body text", '<div><img src="a"/></div><p class="p1">Рядом стоял дом.</p>', 0)
    case("lone label after text", '<p>Текст.</p><p>Рис. 8. Без картинки.</p>', 0)
    case("label as first child", '<div><p>Рис. 9.</p></div>', 0)
    case("text between", '<div><img src="a"/></div> хвост <p>Рис. 10.</p>', 0)
    case("figure already", '<figure><img src="a"/><figcaption>Рис. 11.</figcaption></figure>', 0)
    case("p caption inside a figure", '<figure><img src="a"/><p>Рис. 12.</p></figure>', 0)
    case("picture block with text", '<div><img src="a"/>подпись</div><p>Рис. 13.</p>', 0)
    keep = '<!-- <div><img src="x"/></div><p>Рис. 0.</p> --><![CDATA[ <p>Рис</p> ]]>'
    case("comment and CDATA copied", keep + owner, 1)
    if not retypeset_doc(keep + owner)[0].startswith(keep):
        fails.append("comment and CDATA: not copied byte for byte")
    case("two pictures, two captions", owner + "\n" + owner, 2)
    # The label needs a number (the plan 14 judge, finding 1): body text that only starts with the letters stays.
    pic = '<div class="image"><img src="a"/></div>'
    for body in ("Риск был велик, но он решился.", "рисунки Эшера висели.", "Рисовал он плохо.", "Fighting broke out.",
                 "Figaro sang.", "Рис как крупа."):
        case("body text «" + body + "»", pic + '<p class="p1">' + body + "</p>", 0)
    for label in ("Рис.&nbsp;4. Схема.", "РИС. 5. Схема.", "Рисунок 6 — Схема", "Fig. 7. A cat", "Рис.8. Слитно."):
        case("label «" + label + "»", pic + "<p>" + label + "</p>", 1)
    case("a figure as the previous sibling", '<figure><img src="a"/></figure><p>Рис. 3.</p>', 0)
    case("a comment between picture and caption", pic + "<!-- x --><p>Рис. 1.</p>", 1)
    case("a quoted '>' in the caption's attribute", '<img src="a"/><p class="p1" title="x>y">Рис. 1.</p>', 1,
         '<figure class="kccp-figure"><img src="a"/><figcaption title="x>y">Рис. 1.</figcaption></figure>')
    caps = []
    retypeset_doc(owner + "\n" + pic + '<p><span>Рисунок 3</span> –  Схема</p>', caps)
    if caps != ["Рис. 2. Адольф.", "Рисунок 3 – Схема"]:
        fails.append(f"--list captions: {caps}")

    # The whole EPUB: EPUB 3 with a linked stylesheet, EPUB 2 refused, no-pairs book left alone.
    def epub(version, body, css_link=True, doc="OPS/ch.xhtml", css="p { text-indent: 1em; }\n", head=None,
             package="package"):
        b = io.BytesIO()
        with zipfile.ZipFile(b, "w") as z:
            z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
            z.writestr("META-INF/container.xml", '<container><rootfiles><rootfile full-path="OPS/c.opf"/></rootfiles></container>')
            z.writestr("OPS/c.opf", f'<{package} version="{version}"><manifest><item href="ch.xhtml"/></manifest></{package}>')
            href = posixpath.relpath("OPS/css/s.css", posixpath.dirname(doc))
            link = f'<link rel="stylesheet" type="text/css" href="{href}"/>' if css_link else ""
            z.writestr(doc, f"<html>{head if head is not None else '<head>' + link + '</head>'}<body>{body}</body></html>",
                       compress_type=zipfile.ZIP_DEFLATED)
            z.writestr("OPS/css/s.css", css)
        return b.getvalue()

    def entry(data, name):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            return z.read(name).decode()

    out, rep = retypeset_epub(epub("3.0", owner, css="p { }\n" + CSS_RULE.decode()))
    if entry(out, "OPS/css/s.css").count(FIGURE_CLASS) != 1:
        fails.append("a stylesheet that already has the rule got it twice")
    out, rep = retypeset_epub(epub("3.0", owner, css_link=False, doc="OPS/Text/ch.xhtml"))
    if 'href="../' + OWN_CSS_NAME + '"/></head>' not in entry(out, "OPS/Text/ch.xhtml"):
        fails.append("own CSS from a subfolder: the <link> is not '../kccp-figure.css' at the end of <head>")
    out, rep = retypeset_epub(epub("3.0", owner, css_link=False, head="<head/>"))
    if '<head><link rel="stylesheet" type="text/css" href="' + OWN_CSS_NAME + '"/></head>' not in entry(out, "OPS/ch.xhtml") \
            or rep["nohead"]:
        fails.append("<head/>: the <link> is not inserted")
    out, rep = retypeset_epub(epub("3.0", owner, package="opf:package"))
    if out is None or rep["version"] != "3.0":
        fails.append(f"<opf:package>: version {rep['version']}")

    out3, rep = retypeset_epub(epub("3.0", owner))
    if out3 is None or rep["pairs"] != 1:
        fails.append(f"epub 3: {rep}")
    else:
        with zipfile.ZipFile(io.BytesIO(out3)) as z:
            first = z.infolist()[0]
            if first.filename != "mimetype" or first.compress_type != zipfile.ZIP_STORED:
                fails.append("epub 3: mimetype is not first and stored")
            if z.read("OPS/css/s.css").count(FIGURE_CLASS.encode()) != 1:
                fails.append("epub 3: the CSS rule is not appended exactly once")
            if "<figcaption" not in z.read("OPS/ch.xhtml").decode():
                fails.append("epub 3: no figcaption in the chapter")
        again, rep2 = retypeset_epub(out3)
        if again is not None or rep2["pairs"] != 0:
            fails.append(f"epub 3: a second run wrote something: {rep2}")
    out2, rep = retypeset_epub(epub("2.0", owner))
    if out2 is not None or rep["version"] != "2.0":
        fails.append(f"epub 2: not refused: {rep}")
    none, rep = retypeset_epub(epub("3.0", "<p>Текст.</p>"))
    if none is not None:
        fails.append("no pairs: a book was written")
    own, rep = retypeset_epub(epub("3.0", owner, css_link=False))
    with zipfile.ZipFile(io.BytesIO(own)) as z:
        if "OPS/" + OWN_CSS_NAME not in z.namelist() or OWN_CSS_NAME not in z.read("OPS/c.opf").decode() \
                or 'href="' + OWN_CSS_NAME + '"' not in z.read("OPS/ch.xhtml").decode():
            fails.append("no stylesheet: kccp-figure.css not added, listed and linked")

    for f in fails:
        print("FAIL " + f)
    print(f"selftest: {'FAIL' if fails else 'OK'} ({len(fails)} failure(s))")
    return 1 if fails else 0


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    args = [a for a in sys.argv[1:] if a != "--list"]
    if len(args) not in (1, 2):
        print("usage: figure_retypeset.py <in.epub> [<out.epub>] [--list] | --selftest")
        return 2
    src = Path(args[0])
    dst = Path(args[1]) if len(args) == 2 else src.with_name(src.stem + ".figure.epub")
    try:
        data, report = retypeset_epub(src.read_bytes())
    except (zipfile.BadZipFile, KeyError, ValueError) as e:
        print(f"{src.name}: not a readable EPUB ({e})")
        return 2
    if "--list" in sys.argv[1:]:                           # every caption wrapped — the run on a book is READ, not only counted
        for doc, caption in report["captions"]:
            print(f"  {doc}: {caption}")
    line = (f"{src.name}: EPUB {report['version']} · documents changed {report['docs']} · pairs {report['pairs']}"
            + (f" · CSS {', '.join(report['css'])}" if report["css"] else "")
            + (f" · no <head>, CSS not linked in {len(report['nohead'])}" if report["nohead"] else "")
            + (f" · not UTF-8, skipped {len(report['skipped'])}" if report["skipped"] else ""))
    if data is None:
        why = "EPUB 2: not re-typeset (plan 14, risk 1)" if not report["version"].startswith("3") else "no pairs: nothing written"
        print(line + " · " + why)
        return 3 if not report["version"].startswith("3") else 0
    if dst.resolve() == src.resolve():
        print("refusing to overwrite the input")
        return 2
    dst.write_bytes(data)
    print(line + f" · out {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
