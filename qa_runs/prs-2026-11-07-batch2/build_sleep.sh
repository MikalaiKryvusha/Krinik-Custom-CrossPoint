#!/bin/zsh
R=/Users/kryvusha/Xteink/qa_runs/prs-2026-11-07-batch2; cd /Users/kryvusha/Xteink/pr-fixes/sleep-skip-truncated-bmp
for e in x4pro default; do ~/.platformio/penv/bin/pio run -e $e > $R/sleep-$e.log 2>&1; echo "sleep $e exit=$?" >> $R/summary.txt; done
{ cmake -S test -B build/test -G Ninja -DCMAKE_BUILD_TYPE=Release && cmake --build build/test && ctest --test-dir build/test -j 4; } > $R/sleep-host.log 2>&1
echo "sleep host exit=$? $(grep -o '[0-9]*% tests passed.*' $R/sleep-host.log | tail -1)" >> $R/summary.txt; echo SLEEP-DONE >> $R/summary.txt
