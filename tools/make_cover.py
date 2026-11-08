# Typographic EPUB cover for the reader: 480×800, white paper, Literata, author on top, title large.
# python3 -I make_cover.py <out.jpg> "<author>" "<title>" ["<subtitle>"] [--scale]
# --scale adds a 16-step gray scale at the bottom (for «Калибровка»).
# --image=<file> puts a picture (portrait) in the upper part; author and title go below it.
# --reader draws a stylized e-reader with «X4 PRO» in the upper part (for «РУКОВОДСТВО»).
# Short words (prepositions, conjunctions) stick to the next word: no «О» alone at a line end.
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 480, 800
FONTS = Path(__file__).resolve().parent.parent / 'fonts' / 'Literata'
args = [a for a in sys.argv[1:] if not a.startswith('--')]
image = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--image=')), None)
out, author, title = args[0], args[1], args[2]
subtitle = args[3] if len(args) > 3 else ''
scale = '--scale' in sys.argv
reader = '--reader' in sys.argv

img = Image.new('L', (W, H), 255)
d = ImageDraw.Draw(img)
font = lambda name, size: ImageFont.truetype(str(FONTS / f'Literata-{name}.ttf'), size)


def wrap(text, f, width):
    words, glued = text.split(), []
    for w in words:  # glue a short word to the next one
        prev = glued[-1].split('\u00a0')[-1] if glued else ''  # last word of the glued chunk
        if prev and ((len(prev) <= 2 and prev.isalpha()) or (len(prev) == 2 and prev[0].isalpha() and prev[1] == '.')):
            glued[-1] += '\u00a0' + w
        else:
            glued.append(w)
    lines, line = [], ''
    for word in glued:
        probe = (line + ' ' + word).strip()
        if d.textlength(probe, font=f) <= width or not line:
            line = probe
        else:
            lines.append(line)
            line = word
    return lines + ([line] if line else [])


def block(lines, f, y, gap):
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((W - w) / 2, y), ln, font=f, fill=0)
        y += f.size + gap
    return y


margin = 48
d.rectangle([24, 24, W - 25, H - 25], outline=0, width=2)
if reader:
    # stylized X4 Pro: rounded body, wide bottom chin, screen with text lines, the name under it
    bx0, by0, bx1, by1 = 150, 60, 330, 350
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=22, fill=40)
    d.rounded_rectangle([bx0 + 12, by0 + 14, bx1 - 12, by1 - 46], radius=6, fill=235)
    if scale:
        # the screen shows a gray scale (calibration): 8 bands, black to white, top to bottom
        sx0, sy0, sx1, sy1 = bx0 + 22, by0 + 26, bx1 - 22, by1 - 58
        band = (sy1 - sy0) / 8
        for i in range(8):
            d.rectangle([sx0, sy0 + i * band, sx1, sy0 + (i + 1) * band - 1], fill=round(255 * i / 7))
        d.rectangle([sx0, sy0, sx1, sy1 - 1], outline=0, width=1)
        scale = False  # no second scale at the page bottom
    else:
        for i, frac in enumerate([0.9, 0.95, 0.8, 0.92, 0.6, 0.0, 0.88, 0.94, 0.85, 0.7]):
            if frac:
                ly = by0 + 34 + i * 20
                d.rounded_rectangle([bx0 + 26, ly, bx0 + 26 + (bx1 - bx0 - 52) * frac, ly + 6], radius=3, fill=120)
    d.ellipse([(bx0 + bx1) / 2 - 7, by1 - 30, (bx0 + bx1) / 2 + 7, by1 - 16], outline=200, width=2)
    nf = font('Bold', 40)
    name = 'X4 PRO'
    d.text(((W - d.textlength(name, font=nf)) / 2, by1 + 22), name, font=nf, fill=0)
    y = by1 + 22 + 40 + 30
    y = block(wrap(author.upper(), font('Regular', 24), W - 2 * margin), font('Regular', 24), y, 6)
    area_top, area_h = y + 10, H - 40 - (y + 10)
elif image:
    # picture fills the frame width, top part; centre-crop to the box
    box_w, box_h = W - 52, 470
    pic = Image.open(image).convert('L')
    k = max(box_w / pic.width, box_h / pic.height)
    pic = pic.resize((round(pic.width * k), round(pic.height * k)), Image.LANCZOS)
    left, top = (pic.width - box_w) // 2, max(0, (pic.height - box_h) // 5)
    img.paste(pic.crop((left, top, left + box_w, top + box_h)), (26, 26))
    y = 26 + box_h + 26
    y = block(wrap(author.upper(), font('Regular', 26), W - 2 * margin), font('Regular', 26), y, 6)
    area_top, area_h = y + 12, H - 40 - (y + 12)
else:
    y = 96
    y = block(wrap(author.upper(), font('Regular', 28), W - 2 * margin), font('Regular', 28), y, 8)
    d.line([(W / 2 - 40, y + 24), (W / 2 + 40, y + 24)], fill=0, width=2)
    area_top, area_h = 230, 330

# title: the largest size whose wrapped block (plus the subtitle) fits its area
sf = font('Italic', 26)
sub_lines = wrap(subtitle, sf, W - 2 * margin) if subtitle else []
sub_h = (18 + len(sub_lines) * (sf.size + 6)) if sub_lines else 0
for size in range(60, 18, -2):
    tf = font('Bold', size)
    tl = wrap(title, tf, W - 2 * margin)
    if len(tl) * (size + 10) + sub_h <= area_h and all(d.textlength(t, font=tf) <= W - 2 * margin for t in tl):
        break
ty = area_top + (area_h - len(tl) * (size + 10) - sub_h) / 2
y = block(tl, tf, ty, 10)
if sub_lines:
    block(sub_lines, sf, y + 18, 6)

if scale:
    steps, x0, x1, top = 16, margin, W - margin, H - 170
    step = (x1 - x0) / steps
    for i in range(steps):
        d.rectangle([x0 + i * step, top, x0 + (i + 1) * step - 1, top + 70], fill=round(255 * i / (steps - 1)))
    d.rectangle([x0, top, x1 - 1, top + 70], outline=0, width=1)

img.convert('RGB').save(out, 'JPEG', quality=92)
print(out)
