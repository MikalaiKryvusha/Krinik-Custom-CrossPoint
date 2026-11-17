#!/bin/sh
# Removes the card copy (qa_runs/<run>/sd) of each NAMED simulator run before its evidence is committed; refuses a run
# whose sd/ holds files git tracks (EXP-0031: a prefix glob deleted a committed 2026-11-08 card). No globs: name the runs.
# Usage: sh tools/clean_run_cards.sh <run> [<run>…]     → exit 1 when any run was refused
# @guard clean-run-cards
# THREAT:         an `rm -rf qa_runs/<prefix>_*/sd` cleanup deletes tracked evidence of an older run with the same prefix
# PROVED-AGAINST: run on qa_runs/guide_after (tracked sd/) → refused, exit 1, files intact; on a fresh run → sd/ removed
# GAP:            a run named by mistake whose sd/ is untracked is still removed (that is the tool's job)
# ON-REAL-PATH:   2026-11-17 16:00 +03:00 — the real tree: guide_after (4 tracked files) refused, globs refused, a fresh run cleaned
cd "$(dirname "$0")/.." || exit 2
status=0
for run in "$@"; do
  case "$run" in */*|*'*'*|*'?'*|'') echo "refused: '$run' — a run name, not a path or a glob"; status=1; continue ;; esac
  dir="qa_runs/$run/sd"
  [ -d "$dir" ] || { echo "skip: $dir — none"; continue; }
  tracked=$(git ls-files -- "$dir" | wc -l)
  if [ "$tracked" -gt 0 ]; then
    echo "refused: $dir — $tracked file(s) tracked by git"; status=1; continue
  fi
  rm -rf "$dir" && echo "removed: $dir"
done
exit $status
