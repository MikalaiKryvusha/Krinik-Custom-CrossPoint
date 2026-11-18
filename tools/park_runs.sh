#!/bin/sh
# Moves NAMED simulator runs out of qa_runs/ into .tmp/<dest>/ (runs whose shots carry a third-party book's text never
# enter the repo); refuses a run that git tracks any file of. Usage: sh tools/park_runs.sh <dest> <run> [<run>…]
# Why: «mv qa_runs/cap_* …» also took the tracked homework-08 runs cap_look_A…D (2026-11-18, EXP-0039; EXP-0031 is the
# same class for rm). A shell glob expands before the script sees it, so the guard is per run: tracked → refused.
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
[ $# -ge 2 ] || { echo "usage: park_runs.sh <dest> <run> [<run>…]"; exit 2; }
DEST=$ROOT/.tmp/$1; shift
mkdir -p "$DEST"
rc=0
for run in "$@"; do
  run=${run#qa_runs/}; run=${run%/}
  src=$ROOT/qa_runs/$run
  if [ ! -d "$src" ]; then echo "park_runs: no run $run"; rc=1; continue; fi
  if [ -n "$(git -C "$ROOT" ls-files -- "qa_runs/$run" | head -1)" ]; then
    echo "park_runs: REFUSED $run — git tracks its files"; rc=1; continue
  fi
  mv "$src" "$DEST/" && echo "park_runs: $run → .tmp/${DEST##*/.tmp/}/"
done
exit $rc
