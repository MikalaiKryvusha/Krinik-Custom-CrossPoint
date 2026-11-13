#!/bin/sh
# One simulator run on a fresh copy of the template card.
# sh sim_run.sh <name> '<input script>' '<ms:shot;ms:shot>' ['<after-wake input>' '<after-wake shots>']
# Shots are names (home, sleep1…) → qa_runs/<name>/shots/<shot>.bmp, then WebP. Template: qa_runs/sd_template.
# Env: SD_TEMPLATE (card folder under qa_runs/), SIM_ENV (default simulator_x4_pro, on Windows simulator_x4_pro_win),
# FW_DIR (default <workspace>/firmware), SIM_TIMEOUT (s), KEEP_BMP. Windows: run from Git Bash; the UCRT64 bin
# folder (SDL2.dll) is put first in PATH when F:/ai_sandbox/msys64 exists (moved from D:/msys64 2026-11-13).
set -e
# Script guard (EXP-0009, EXP-0015). Every input-script item is <ms>:<action>, and its time counts from the last WAIT,
# so inside one WAIT segment the times must not go down. The simulator silently misreads both slips (a bare `WAIT:…`
# ran the rest at once; a `1000:TAP` written after a `1500:SHOT` ran before it) — refuse them before the run.
for s in "$2" "${4:-}"; do
  echo "$s" | tr ';' '\n' | grep -v '^$' | awk -F: '
    $1 !~ /^[0-9]+$/ { print "sim_run: script item without <ms>: prefix: " $0; exit 2 }
    $1 + 0 < prev { print "sim_run: item earlier than the one before it (times count from the last WAIT): " $0; exit 2 }
    { prev = $1 + 0; if ($2 == "WAIT") prev = 0 }' >&2 || exit 2
done
ROOT=$(cd "$(dirname "$0")/.." && pwd)
R=$ROOT/qa_runs/$1; rm -rf "$R"; mkdir -p "$R/shots"; cp -R "$ROOT/qa_runs/${SD_TEMPLATE:-sd_template}" "$R/sd"
expand() { echo "$1" | tr ';' '\n' | sed -n "s|^\([0-9]*\):\(.*\)$|\1:$R/shots/\2.bmp|p" | paste -sd ';' -; }
PROG=program; PY=python3
case "$(uname -s)" in MINGW*|MSYS*) PROG=program.exe; PY="$ROOT/.pio-venv/Scripts/python.exe"  # has Pillow for shot_webp.py
  R=$(cygpath -m "$R")  # a native exe needs D:/… paths inside env values
  [ -d /f/ai_sandbox/msys64/ucrt64/bin ] && PATH=/f/ai_sandbox/msys64/ucrt64/bin:$PATH ;; esac
# An in-script `<ms>:SHOT:<name>` with a bare name goes to this run's shots folder: the simulator takes the text after
# SHOT: as a path, so a bare name landed in the cwd (firmware/) with no extension (2026-11-13, run epic01_p2_c1).
shots() { echo "$1" | sed "s#\(^\|;\)\([0-9]*\):SHOT:\([^;/]*\)#\1\2:SHOT:$R/shots/\3.bmp#g"; }
SCRIPT=$(shots "$2"); SCRIPT_AFTER_WAKE=$(shots "${4:-}")
cd "${FW_DIR:-$ROOT/firmware}"
# The window opens 480x800 physical pixels, borderless, at the very top-left of the owner's 4K screen (owner,
# 2026-11-09). Keep 100 %: the screenshot hook captures the window, a smaller window gives smaller shots.
export CROSSPOINT_SIM_WINDOW_POS="${CROSSPOINT_SIM_WINDOW_POS:-0,0}" CROSSPOINT_SIM_WINDOW_PERCENT="${CROSSPOINT_SIM_WINDOW_PERCENT:-100}" \
  CROSSPOINT_SIM_WINDOW_BORDERLESS="${CROSSPOINT_SIM_WINDOW_BORDERLESS:-1}"
CROSSPOINT_SIM_SD="$R/sd" CROSSPOINT_SIM_INPUT_SCRIPT="$SCRIPT" CROSSPOINT_SIM_SCREENSHOTS="$(expand "$3")" \
CROSSPOINT_SIM_INPUT_SCRIPT_AFTER_WAKE="$SCRIPT_AFTER_WAKE" CROSSPOINT_SIM_SCREENSHOTS_AFTER_WAKE="$(expand "${5:-}")" \
  timeout ${SIM_TIMEOUT:-90} .pio/build/${SIM_ENV:-simulator_x4_pro}/$PROG > "$R/log.txt" 2>&1 || echo "exit $? (see $R/log.txt)"
[ -n "$KEEP_BMP" ] || $PY -I "$ROOT/tools/shot_webp.py" "$R/shots" >/dev/null
ls "$R/shots"; grep -c -E '\[(ERR|E)\]|panic|Abort|Segmentation' "$R/log.txt" | sed 's/^/errors in log: /' || true
