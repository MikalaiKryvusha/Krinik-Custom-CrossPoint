# Refuses a commit whose staged lines carry a moment stamp later than the machine's clock (EXP-0027: stamps typed by
# feel through a script bypass the clock hook). Reads `git diff --cached -U0`; a stamp is «YYYY-MM-DD HH:MM ±HH:MM»
# or its ISO form. Usage: .pio-venv/Scripts/python.exe -I -X utf8 tools/stamp_guard.py   → exit 1 on a stamp ahead
#                         .pio-venv/Scripts/python.exe -I -X utf8 tools/stamp_guard.py --selftest
# @guard stamp-ahead-of-clock
# THREAT:         a moment written ahead of the clock (15:46 at a real 15:45, 2026-11-17) lands in a commit
# PROVED-AGAINST: --selftest: a staged line with now + 2 min → red; now − 2 min and a date-only line → green
# GAP:            a stamp in the past but still invented (≈ honesty) is not caught; stamps without a zone are skipped
# ON-REAL-PATH:   2026-11-17 15:46 +03:00 — a staged probe line 2 min ahead → exit 1 on the real `git diff --cached`; a command run
#                 before commits by hand (not wired into a hook)
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

STAMP = re.compile(r"(\d{4}-\d{2}-\d{2})[ T](\d{2}):(\d{2})(?::\d{2})? ?([+-]\d{2}):?(\d{2})")
SLACK = timedelta(seconds=59)   # a stamp of the current minute is not ahead


def ahead(lines, now):
    found = []
    for line in lines:
        for m in STAMP.finditer(line):
            d, hh, mm, zh, zm = m.groups()
            sign = 1 if zh.startswith("+") else -1
            tz = timezone(sign * timedelta(hours=abs(int(zh)), minutes=int(zm)))
            moment = datetime.fromisoformat(f"{d}T{hh}:{mm}:00").replace(tzinfo=tz)
            if moment > now + SLACK:
                found.append((m.group(0), line.strip()[:100]))
    return found


def selftest():
    now = datetime.now().astimezone()
    f = lambda t: t.strftime("%Y-%m-%d %H:%M ") + t.strftime("%z")[:3] + ":" + t.strftime("%z")[3:]
    fails = []
    if not ahead([f"done {f(now + timedelta(minutes=2))}"], now):
        fails.append("a stamp 2 min ahead passed")
    if ahead([f"done {f(now - timedelta(minutes=2))}", "date only 2026-11-17", f"now {f(now)}"], now):
        fails.append("a past / current / date-only stamp flagged")
    iso = (now + timedelta(hours=1)).isoformat(timespec="seconds")
    if not ahead([f'"at": "{iso}"'], now):
        fails.append("an ISO stamp an hour ahead passed")
    for x in fails:
        print("FAIL " + x)
    print(f"selftest: {'FAIL' if fails else 'OK'} ({len(fails)} failure(s))")
    return 1 if fails else 0


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    diff = subprocess.run(["git", "diff", "--cached", "-U0"], capture_output=True, text=True, encoding="utf-8").stdout
    added = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
    found = ahead(added, datetime.now().astimezone())
    for stamp, line in found:
        print(f"ahead of the clock: {stamp} · {line}")
    print(f"stamp_guard: {len(found)} stamp(s) ahead of the clock in the staged lines")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
