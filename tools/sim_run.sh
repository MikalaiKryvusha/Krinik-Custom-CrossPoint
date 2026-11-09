#!/bin/sh
# One simulator run on a fresh copy of the template card.
# sh sim_run.sh <name> '<input script>' '<ms:shot;ms:shot>' ['<after-wake input>' '<after-wake shots>']
# Shots are names (home, sleep1…) → qa_runs/<name>/shots/<shot>.bmp, then WebP. Template: qa_runs/sd_template.
# Env: SD_TEMPLATE (card folder under qa_runs/), SIM_ENV (default simulator_x4_pro, on Windows simulator_x4_pro_win),
# FW_DIR (default <workspace>/firmware), SIM_TIMEOUT (s), KEEP_BMP. Windows: run from Git Bash; the UCRT64 bin
# folder (SDL2.dll) is put first in PATH when D:/msys64 exists.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
R=$ROOT/qa_runs/$1; rm -rf "$R"; mkdir -p "$R/shots"; cp -R "$ROOT/qa_runs/${SD_TEMPLATE:-sd_template}" "$R/sd"
expand() { echo "$1" | tr ';' '\n' | sed -n "s|^\([0-9]*\):\(.*\)$|\1:$R/shots/\2.bmp|p" | paste -sd ';' -; }
PROG=program; PY=python3
case "$(uname -s)" in MINGW*|MSYS*) PROG=program.exe; PY="$ROOT/.pio-venv/Scripts/python.exe"  # has Pillow for shot_webp.py
  R=$(cygpath -m "$R")  # a native exe needs D:/… paths inside env values
  [ -d /d/msys64/ucrt64/bin ] && PATH=/d/msys64/ucrt64/bin:$PATH ;; esac
cd "${FW_DIR:-$ROOT/firmware}"
# The window opens 480x800 (100 %) in the top-left corner of the owner's screen (owner, 2026-11-09). Keep 100 %:
# the screenshot hook captures the window, a smaller window gives smaller shots.
export CROSSPOINT_SIM_WINDOW_POS="${CROSSPOINT_SIM_WINDOW_POS:-0,32}" CROSSPOINT_SIM_WINDOW_PERCENT="${CROSSPOINT_SIM_WINDOW_PERCENT:-100}"
CROSSPOINT_SIM_SD="$R/sd" CROSSPOINT_SIM_INPUT_SCRIPT="$2" CROSSPOINT_SIM_SCREENSHOTS="$(expand "$3")" \
CROSSPOINT_SIM_INPUT_SCRIPT_AFTER_WAKE="${4:-}" CROSSPOINT_SIM_SCREENSHOTS_AFTER_WAKE="$(expand "${5:-}")" \
  timeout ${SIM_TIMEOUT:-90} .pio/build/${SIM_ENV:-simulator_x4_pro}/$PROG > "$R/log.txt" 2>&1 || echo "exit $? (see $R/log.txt)"
[ -n "$KEEP_BMP" ] || $PY -I "$ROOT/tools/shot_webp.py" "$R/shots" >/dev/null
ls "$R/shots"; grep -c -E '\[(ERR|E)\]|panic|Abort|Segmentation' "$R/log.txt" | sed 's/^/errors in log: /' || true
