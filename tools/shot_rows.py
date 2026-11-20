# Row profile of upright WebP/BMP screen shots: prints each band of rows holding dark pixels (text lines, the status bar)
# as (first_row, last_row) — compares a simulator page with the owner's reader screenshot by numbers (KCCP bug 16,
# EXP-0041). Usage: .pio-venv/Scripts/python.exe -I -X utf8 tools/shot_rows.py <shot> [<shot>…]
# [TESTED: 2026-11-20 · the owner's shots ch11_p25/ch11_p45 (bar 450–465) vs qa_runs/ui_before and ui_v1 (454 → 450)]
import sys

from PIL import Image

DARK = 128  # a pixel below this grey level counts as ink

for path in sys.argv[1:]:
    image = Image.open(path).convert("L")
    width, height = image.size
    pixels = image.load()
    dark_per_row = [sum(1 for x in range(width) if pixels[x, y] < DARK) for y in range(height)]
    bands, start = [], None
    for y, count in enumerate(dark_per_row + [0]):
        if count > 0 and start is None:
            start = y
        if count == 0 and start is not None:
            bands.append((start, y - 1))
            start = None
    print(path, f"{width}x{height}", bands)
