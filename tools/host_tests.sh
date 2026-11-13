#!/bin/sh
# The full host-test suite of firmware/ against the list of failures known on this PC; exit 1 on any NEW failure.
# sh tools/host_tests.sh            (Git Bash; build + ctest -j1; logs in .tmp/, temp files in .tmp/ — HOUSE_RULES П1)
# Env: FW_DIR (default <workspace>/firmware), KNOWN (default tools/host_tests_known_failures.txt), SKIP_BUILD=1.
# Why: debug10 8538f3dd broke RemoteButtonInputIntegration and no full suite ran until 1.1.3-debug1 (EXPERIENCE
# EXP-0018) — a count read by eye drifts, a diff against the known list does not.
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
FW=${FW_DIR:-$ROOT/firmware}
KNOWN=${KNOWN:-$ROOT/tools/host_tests_known_failures.txt}
TMPD=$ROOT/.tmp
mkdir -p "$TMPD"
case "$(uname -s)" in MINGW*|MSYS*)
  [ -d /f/ai_sandbox/msys64/ucrt64/bin ] && PATH=/f/ai_sandbox/msys64/ucrt64/bin:$PATH
  TEMP=$(cygpath -w "$TMPD"); TMP=$TEMP; export TEMP TMP ;;
*) TMPDIR=$TMPD; export TMPDIR ;; esac
export PATH PYTHONUTF8=1
BUILD_LOG=$TMPD/host_tests_build.log
CTEST_LOG=$TMPD/host_tests_ctest.log
if [ "${SKIP_BUILD:-0}" != 1 ]; then
  cmake --build "$FW/build/test" -- -k 0 >"$BUILD_LOG" 2>&1  # the known NOT_BUILT targets fail here by design
fi
(cd "$FW/build/test" && ctest -j1 >"$CTEST_LOG" 2>&1)
SUMMARY=$(grep -m1 "tests passed" "$CTEST_LOG")
[ -n "$SUMMARY" ] || { echo "host_tests: no ctest summary in $CTEST_LOG"; exit 2; }
echo "host_tests: $SUMMARY"
# The failing names, one per line, sorted: "  N - Name (Failed)" / "(Not Run)".
FAILED_LIST=$TMPD/host_tests_failed.txt
sed -n 's/^[[:space:]]*[0-9][0-9]* - \([^ ]*\) (.*)$/\1/p' "$CTEST_LOG" | sort >"$FAILED_LIST"
NEW=$(grep -vxF -f "$KNOWN" "$FAILED_LIST" || true)
GONE=$(grep -v '^$' "$KNOWN" | grep -vxF -f "$FAILED_LIST" || true)
[ -n "$GONE" ] && printf 'host_tests: known failures that PASS now (shrink the list): %s\n' "$(echo $GONE)"
if [ -n "$NEW" ]; then
  printf 'host_tests: NEW failures: %s\n' "$(echo $NEW)"
  echo "host_tests: details: (cd $FW/build/test && ctest -R '<name>' --output-on-failure)"
  exit 1
fi
echo "host_tests: no new failure (known list: $(grep -vc '^$' "$KNOWN"))"
