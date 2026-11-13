# Summarises the reader's debug battery log (/.crosspoint/battery_log.csv): awake drain by light state and brightness,
# sleep drain per day, charging. Usage: python -I -X utf8 tools/battery_summary.py <battery_log.csv>
import csv
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

MSK = timezone(timedelta(hours=3))


def main():
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    for r in rows:
        for k in ("epoch", "uptime_s", "vcell_mv", "soc_pct", "charging", "light_on", "brightness_pct", "warm_pct"):
            r[k] = int(r[k])
    t0, t1 = rows[0]["epoch"], rows[-1]["epoch"]
    print(f"rows {len(rows)}; {datetime.fromtimestamp(t0, MSK):%Y-%m-%d %H:%M} .. "
          f"{datetime.fromtimestamp(t1, MSK):%Y-%m-%d %H:%M} ({(t1 - t0) / 86400:.1f} days)")
    events = defaultdict(int)
    for r in rows:
        events[r["event"]] += 1
    print("events:", dict(events))

    # Awake: consecutive rows in one boot session (uptime grows), not charging. Bucket by light state / brightness band.
    awake = defaultdict(lambda: [0.0, 0.0])  # key -> [hours, soc drop]
    sleep_hours = sleep_drop = 0.0
    sleeps = []
    for a, b in zip(rows, rows[1:]):
        dt = (b["epoch"] - a["epoch"]) / 3600
        if dt <= 0 or a["charging"] or b["charging"] or b["soc_pct"] > a["soc_pct"]:
            continue
        drop = a["soc_pct"] - b["soc_pct"]
        if a["event"] == "sleep" and b["event"] == "boot":
            sleep_hours += dt
            sleep_drop += drop
            sleeps.append((dt, drop))
        elif b["uptime_s"] > a["uptime_s"]:
            if not a["light_on"]:
                key = "light off"
            else:
                band = "≤10%" if a["brightness_pct"] <= 10 else "11-50%" if a["brightness_pct"] <= 50 else ">50%"
                key = f"light on {band}"
            awake[key][0] += dt
            awake[key][1] += drop
    print("awake drain (not charging):")
    for key, (hours, drop) in sorted(awake.items()):
        rate = drop / hours if hours else 0
        print(f"  {key:16s} {hours:6.1f} h  -{drop:4.0f} %  = {rate:.2f} %/h  (~{100 / rate:.0f} h per full charge)"
              if rate else f"  {key:16s} {hours:6.1f} h  -{drop:4.0f} %")
    if sleep_hours:
        print(f"sleep: {len(sleeps)} periods, {sleep_hours:.1f} h, -{sleep_drop:.0f} % = "
              f"{sleep_drop / sleep_hours * 24:.2f} %/day")
    long = [(h, d) for h, d in sleeps if h >= 6]
    if long:
        hours = sum(h for h, _ in long)
        drop = sum(d for _, d in long)
        print(f"sleep periods >= 6 h: {len(long)}, {hours:.1f} h, -{drop:.0f} % = {drop / hours * 24:.2f} %/day")
    charges = sum(1 for a, b in zip(rows, rows[1:]) if not a["charging"] and b["charging"])
    print(f"charging starts: {charges}; soc first {rows[0]['soc_pct']} %, last {rows[-1]['soc_pct']} %")


main()
