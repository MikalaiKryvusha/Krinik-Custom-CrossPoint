#!/bin/zsh
# Builds and host tests for the batch-2 PR branches. Logs beside this script.
R=/Users/kryvusha/Xteink/qa_runs/prs-2026-11-07-batch2
PIO=$HOME/.platformio/penv/bin/pio
for d in night-epub-images lyra-title-lines viewer-reader-controls; do
  cd /Users/kryvusha/Xteink/pr-fixes/$d || exit 1
  cp -n ../screen-clean-menu/platformio.local.ini . 2>/dev/null
  for env in simulator_x4_pro x4pro default; do
    $PIO run -e $env > $R/$d-$env.log 2>&1; echo "$d $env exit=$?" >> $R/summary.txt
  done
  { cmake -S test -B build/test -G Ninja -DCMAKE_BUILD_TYPE=Release && cmake --build build/test && ctest --test-dir build/test -j 8; } > $R/$d-host.log 2>&1
  echo "$d host exit=$? $(grep -o '[0-9]*% tests passed.*' $R/$d-host.log | tail -1)" >> $R/summary.txt
done
echo DONE >> $R/summary.txt
