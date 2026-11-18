#!/bin/sh
# Krinik EPUB Linter's tests (+ ruff) with every temp file inside the project (HOUSE_RULES П1): TEMP/TMP and pytest's
# --basetemp in .tmp/, no .pytest_cache. Usage (Git Bash, workspace root): sh tools/kel_tests.sh [pytest args…]
# Why: plain pytest put its tmp_path folders into the harness's F:\Temp\pytest-of-<user> (2026-11-18, the judge;
# EXP-0037's class).
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
TMPD=$ROOT/.tmp/pytest
mkdir -p "$TMPD"
case "$(uname -s)" in MINGW*|MSYS*) TEMP=$(cygpath -w "$ROOT/.tmp"); TMP=$TEMP; export TEMP TMP ;; esac
cd "$ROOT/epub-linter" || exit 2
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider --basetemp="$TMPD" "$@"
rc=$?
.venv/Scripts/ruff.exe check . || rc=1
rm -rf "$TMPD"
exit $rc
