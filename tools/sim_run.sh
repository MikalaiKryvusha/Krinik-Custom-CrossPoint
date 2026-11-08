#!/bin/sh
# One simulator run on a fresh copy of the template card.
# sh sim_run.sh <name> '<input script>' '<ms:shot;ms:shot>' ['<after-wake input>' '<after-wake shots>']
# Shots are names (home, sleep1…) → qa_runs/<name>/shots/<shot>.bmp, then WebP. Template: qa_runs/sd_template.
set -e
R=$HOME/Xteink/qa_runs/$1; rm -rf "$R"; mkdir -p "$R/shots"; cp -R "$HOME/Xteink/qa_runs/${SD_TEMPLATE:-sd_template}" "$R/sd"
expand() { echo "$1" | tr ';' '\n' | sed -n "s|^\([0-9]*\):\(.*\)$|\1:$R/shots/\2.bmp|p" | paste -sd ';' -; }
cd "${FW_DIR:-$HOME/Xteink/firmware}"
CROSSPOINT_SIM_SD="$R/sd" CROSSPOINT_SIM_INPUT_SCRIPT="$2" CROSSPOINT_SIM_SCREENSHOTS="$(expand "$3")" \
CROSSPOINT_SIM_INPUT_SCRIPT_AFTER_WAKE="${4:-}" CROSSPOINT_SIM_SCREENSHOTS_AFTER_WAKE="$(expand "${5:-}")" \
  timeout ${SIM_TIMEOUT:-90} .pio/build/${SIM_ENV:-simulator_x4_pro}/program > "$R/log.txt" 2>&1 || echo "exit $? (see $R/log.txt)"
[ -n "$KEEP_BMP" ] || python3 -I "$HOME/Xteink/tools/shot_webp.py" "$R/shots" >/dev/null
ls "$R/shots"; grep -c -E '\[(ERR|E)\]|panic|Abort|Segmentation' "$R/log.txt" | sed 's/^/errors in log: /'
