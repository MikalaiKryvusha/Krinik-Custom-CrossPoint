#!/bin/bash
C=$HOME/.platformio/packages/tool-cppcheck/cppcheck
T=<laptop-scratchpad>
run() { "$C" --enable=all --check-level=exhaustive --suppress=missingIncludeSystem --suppress=missingInclude --suppress=unusedFunction --suppress=unmatchedSuppression --suppress=checkersReport --inline-suppr --language=c++ --std=c++20 -q -Isrc -Ilib/GfxRenderer "$1" 2>&1 | grep -E ': (error|warning|style|performance|portability):' | sed -E 's/:[0-9]+:[0-9]+:/:/' | sort; }
for d in night-epub-images lyra-title-lines viewer-reader-controls sleep-skip-truncated-bmp; do
  cd /Users/kryvusha/Xteink/pr-fixes/$d || continue
  git diff --name-only HEAD~1 HEAD -- '*.cpp' | grep -v '^test/' | while read -r f; do
    run "$f" > $T/after.txt; git stash list >/dev/null
    git show HEAD~1:"$f" > $T/base_src.cpp; cp "$f" $T/keep.cpp; cp $T/base_src.cpp "$f"; run "$f" > $T/before.txt; cp $T/keep.cpp "$f"
    echo "== $d $f new findings:"; comm -13 $T/before.txt $T/after.txt
  done
  git status --short | head -3
done
