#!/bin/sh
# Remove macOS AppleDouble «._name» files from the reader's card (macOS writes them on FAT at every copy;
# the library shows ._*.epub as extra books, ._*.bmp in .sleep can be picked as a broken sleep image).
# Only files that really are AppleDouble (magic 00 05 16 07) are deleted. 
# sh card_clean.sh "/Volumes/X4-KRINIK"
V="${1:-/Volumes/X4-KRINIK}"; n=0
# No card at that path → fail loudly, so a chained «… && diskutil eject» stops instead of ejecting an uncleaned card.
[ -d "$V" ] || { echo "НЕТ КАРТЫ: $V" >&2; exit 1; }
find "$V" \( -name .Spotlight-V100 -o -name .fseventsd -o -name .Trashes \) -prune -o -name '._*' -type f -print | while IFS= read -r f; do
  if [ "$(head -c 4 "$f" | xxd -p)" = "00051607" ]; then rm -f "$f" && echo "удалён: ${f#$V}"; else echo "оставлен (не AppleDouble): ${f#$V}"; fi
done
# No library.dirty mark: the library finds new files itself, and the forced rescan froze the home screen (03.11.2026)
sync
# Verify: any AppleDouble left → non-zero exit, the eject after it does not run.
all=$(find "$V" \( -name .Spotlight-V100 -o -name .fseventsd -o -name .Trashes \) -prune -o -name '._*' -type f -print) || {
  echo "КАРТА НЕ ЧИТАЕТСЯ: $V" >&2; exit 1; }
left=$(printf '%s\n' "$all" | while IFS= read -r f; do
  [ -n "$f" ] && [ "$(head -c 4 "$f" | xxd -p)" = "00051607" ] && echo "$f"; done)
[ -z "$left" ] || { echo "ОСТАЛИСЬ ДВОЙНИКИ:" >&2; echo "$left" >&2; exit 1; }
echo "двойников ._ нет"
