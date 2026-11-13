# Measures the button row of a shade screenshot: the gaps at both edges and between the buttons (KCCP epic 01).
# Usage: .pio-venv/Scripts/python.exe -I -X utf8 tools/shade_gaps.py <shot.webp> [land|port] [--max-spread N]
# Prints the content edges, the buttons found and the gaps in the shot's pixels; exit 1 when the spread of the gaps is
# above --max-spread (default 2: the shots are half-scale WebP, each edge is good to ±1 px).
import sys

from PIL import Image

DARK = 110          # a pixel darker than this is ink
BUTTON_MIN, BUTTON_MAX = 24, 31   # a button square at half scale (56 px on the panel), with antialiasing


def runs(row):
    out = []
    for x, value in enumerate(row):
        if value < DARK:
            if out and x <= out[-1][1] + 1:
                out[-1][1] = x
            else:
                out.append([x, x])
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    max_spread = 2
    if "--max-spread" in sys.argv:
        max_spread = int(sys.argv[sys.argv.index("--max-spread") + 1])
        args = [a for a in args if a != str(max_spread)]
    path = args[0]
    im = Image.open(path).convert("L")
    width, height = im.size
    kind = args[1] if len(args) > 1 else ("land" if width > height else "port")
    slider = (0.15, 0.24) if kind == "land" else (0.15, 0.23)
    band = (0.52, 0.66) if kind == "land" else (0.32, 0.385)
    pixels = im.load()

    def row(y):
        return [pixels[x, y] for x in range(width)]

    # The content edges: the brightness row's «−» box and the lamp toggle span the sheet's content width.
    left, right = width, 0
    for y in range(int(slider[0] * height), int(slider[1] * height)):
        xs = [x for x in range(width) if pixels[x, y] < DARK]
        if xs and xs[-1] - xs[0] > width * 0.8:
            left, right = min(left, xs[0]), max(right, xs[-1])
    # The button squares: the band row that shows the most square-wide ink clusters (walls of outlined squares merge).
    best = (None, [])
    for y in range(int(band[0] * height), int(band[1] * height)):
        clusters = []
        for r in runs(row(y)):
            if clusters and r[0] - clusters[-1][0] < BUTTON_MAX:
                clusters[-1][1] = r[1]
            else:
                clusters.append(list(r))
        squares = [c for c in clusters if BUTTON_MIN <= c[1] - c[0] + 1 <= BUTTON_MAX]
        if len(squares) > len(best[1]):
            best = (y, squares)
    y, squares = best
    if not squares or right <= left:
        print(f"shade_gaps: no button row found in {path}")
        return 2
    gaps = [squares[0][0] - left] + [squares[i + 1][0] - squares[i][1] - 1 for i in range(len(squares) - 1)]
    gaps.append(right - squares[-1][1])
    spread = max(gaps) - min(gaps)
    print(f"shade_gaps: {path} ({kind}, {width}x{height}): content {left}..{right}, row y {y}, "
          f"{len(squares)} buttons, gaps {gaps}, spread {spread}")
    return 0 if spread <= max_spread else 1


if __name__ == "__main__":
    sys.exit(main())
