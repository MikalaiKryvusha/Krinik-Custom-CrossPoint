# Draws a simple 1-bit firmware icon with Pillow and prints it as a C++ freeink::Icon (KCCP epic 01: the ▲ ▼ of
# «Плитки шторки», the half-filled circle of the night-mode tile). No rsvg on this PC, so the shapes are drawn here.
# Usage: python -I -X utf8 tools/make_icon.py <shape> <name> [size]   shapes: tri_up, tri_down, half_circle
# Format (freeink-sdk Icon.h): rows top to bottom, (w+7)/8 bytes each, MSB first, bit 1 = transparent, bit 0 = black;
# opticalCenterY = the row of the black pixels' centre of mass.
import sys

from PIL import Image, ImageDraw

SUPERSAMPLE = 8  # draw large, then reduce: smooth edges before the 1-bit threshold
THRESHOLD = 128  # mean coverage of a target pixel at or above this → black


def draw(shape, size):
    big = size * SUPERSAMPLE
    img = Image.new("L", (big, big), 0)  # 0 = empty, 255 = ink
    d = ImageDraw.Draw(img)
    m = big // 6  # margin
    if shape == "tri_up":
        d.polygon([(big // 2, m), (big - m, big - m - big // 8), (m, big - m - big // 8)], fill=255)
    elif shape == "tri_down":
        d.polygon([(m, m + big // 8), (big - m, m + big // 8), (big // 2, big - m)], fill=255)
    elif shape == "half_circle":
        # iOS-style appearance glyph: a ring with its left half filled (the owner: «круг черный и белый по половине»).
        ring = SUPERSAMPLE * 2
        box = [m, m, big - m, big - m]
        d.ellipse(box, fill=255)
        inner = [m + ring, m + ring, big - m - ring, big - m - ring]
        d.ellipse(inner, fill=0)
        d.pieslice(box, 90, 270, fill=255)  # the left half solid
    else:
        raise SystemExit(f"unknown shape: {shape}")
    return img.resize((size, size), Image.BOX)


def to_icon(img, name):
    w, h = img.size
    px = img.load()
    rows, ink_rows = [], []
    for y in range(h):
        row = []
        for xb in range(0, w, 8):
            byte = 0
            for bit in range(8):
                x = xb + bit
                black = x < w and px[x, y] >= THRESHOLD
                if black:
                    ink_rows.append(y)
                byte |= (0 if black else 1) << (7 - bit)
            row.append(byte)
        rows.extend(row)
    center = round(sum(ink_rows) / len(ink_rows)) if ink_rows else h // 2
    body = ", ".join(f"0x{b:02X}" for b in rows)
    return (f"static const uint8_t {name}_bits[] = {{{body}}};\n"
            f"static const freeink::Icon {name} = {{{w}, {h}, {center}, {name}_bits}};\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__ or "usage: make_icon.py <shape> <name> [size]")
    shape, name = sys.argv[1], sys.argv[2]
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 32
    img = draw(shape, size)
    print(to_icon(img, name), end="")
