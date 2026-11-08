#!/bin/zsh
# sim.sh <branch-dir> <card> <run-name> '<input script>' '<ms:shot;...>'
R=/Users/kryvusha/Xteink/qa_runs/prs-2026-11-07-batch2
O=$R/runs/$3; rm -rf $O; mkdir -p $O/shots; cp -R $R/sd/$2 $O/sd
SH=$(echo "$5" | tr ';' '\n' | sed -n "s|^\([0-9]*\):\(.*\)$|\1:$O/shots/\2.bmp|p" | paste -sd ';' -)
cd /Users/kryvusha/Xteink/pr-fixes/night-epub-images
CROSSPOINT_SIM_SD=$O/sd CROSSPOINT_SIM_INPUT_SCRIPT="$4" CROSSPOINT_SIM_SCREENSHOTS="$SH" \
  timeout 60 $R/bin/$1 > $O/log.txt 2>&1; echo "exit $?"
ls $O/shots; grep -c -E '\[ERR\]|panic|Abort|Segmentation' $O/log.txt | sed 's/^/errors: /'
