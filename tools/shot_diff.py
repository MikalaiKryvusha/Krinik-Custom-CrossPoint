# Compares the same-named WebP shots of two simulator runs: pixels that differ by more than a threshold, the status bar
# (clock, battery, page number) cut off. WebP q90 is lossy and its encoder segments the whole frame, so a changed clock
# shifts other blocks by up to ~11 levels: a golden compares content, not bytes (measured 2026-11-17, epic 07 Ф1).
# Usage: .pio-venv/Scripts/python.exe -I -X utf8 tools/shot_diff.py <shots dir A> <shots dir B> [bottom rows to cut, 22] [threshold, 32]
# Exit 1 when any page differs. Prove it can fail first: compare two different runs.
import pathlib
import sys

from PIL import Image, ImageChops

a, b = (pathlib.Path(p) for p in sys.argv[1:3])
cut = int(sys.argv[3]) if len(sys.argv) > 3 else 22
threshold = int(sys.argv[4]) if len(sys.argv) > 4 else 32
total = 0
for shot in sorted(a.glob("*.webp")):
    other = b / shot.name
    if not other.exists():
        print(f"{shot.name}: missing in {b}")
        total += 1
        continue
    x, y = Image.open(shot).convert("L"), Image.open(other).convert("L")
    if x.size != y.size:
        print(f"{shot.name}: size {x.size} vs {y.size}")
        total += 1
        continue
    box = (0, 0, x.width, x.height - cut)
    diff = ImageChops.difference(x.crop(box), y.crop(box))
    count = sum(1 for value in diff.get_flattened_data() if value > threshold) if hasattr(diff, "get_flattened_data") \
        else sum(1 for value in diff.getdata() if value > threshold)
    print(f"{shot.name}: {count}")
    total += count
print(f"TOTAL {total}")
sys.exit(1 if total else 0)
