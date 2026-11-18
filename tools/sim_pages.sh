#!/bin/sh
# Pages through one chapter of a book in the simulator, one WebP shot per page (HOUSE_RULES П4: the owner's settings and
# book copy on the card). Usage (Git Bash, from the workspace root):
#   CARD=.tmp/<card> [BOOK=<file.epub>] [START=<page0>] [SIM_TIMEOUT=<s>] [CROSSPOINT_SIM_SCREEN_TEXT=1] \
#     sh tools/sim_pages.sh <run> <spine> <pages> [key]
# The card holds /geb.epub (BOOK is copied there, the card's own copy restored after), .crosspoint/settings.json and the
# book's cache folder with progress.bin (u16 spine, u16 page — written here). Page turns: UP; shots every 2 s; the
# default 90 s SIM_TIMEOUT ends a run at ≈ 40 pages. CROSSPOINT_SIM_SCREEN_TEXT=1 logs each page's text as
# «[SIM] SCREEN:» (the first 2 lines are the boot screens).
set -u
RUN=$1; SPINE=$2; N=$3; KEY=${4:-UP}; START=${START:-0}
C=${CARD:?CARD=<card folder> is required}
CACHE=$(find "$C/.crosspoint" -maxdepth 1 -type d -name 'epub_*' | head -1)
[ -n "$CACHE" ] || { echo "sim_pages: no epub_* cache folder in $C/.crosspoint (open the book once to create it)"; exit 2; }
[ -n "${BOOK:-}" ] && { cp "$C/geb.epub" "$C/.geb.epub.keep" && cp "$BOOK" "$C/geb.epub"; }
printf "$(printf '\\%03o' "$SPINE")\000$(printf '\\%03o' "$START")\000" > "$CACHE/progress.bin"
S="0:WAIT:Entering activity: EpubReader;9000:SHOT:p$(printf %03d "$START")"
i=1; T=9000
while [ $i -lt "$N" ]; do
  T=$((T+300)); S="$S;$T:$KEY"; T=$((T+1700)); S="$S;$T:SHOT:p$(printf %03d $((START+i)))"; i=$((i+1))
done
T=$((T+1500))
SD_TEMPLATE=../$C SIM_ENV=${SIM_ENV:-simulator_x4_pro_win} sh tools/sim_run.sh "$RUN" "$S;$T:QUIT" '' > /dev/null 2>&1
[ -f "$C/.geb.epub.keep" ] && mv "$C/.geb.epub.keep" "$C/geb.epub"
echo "$RUN: $(ls qa_runs/$RUN/shots | wc -l) shots, $(grep -a -c '\[ERR\]' qa_runs/$RUN/log.txt) ERR; $(grep -a -o 'Progress saved[^\r]*' qa_runs/$RUN/log.txt | tail -1)"
