# Debug2: two-hour discharge comparison — observation plan

[AI]
Goal: preserve and compare the owner's two exact one-hour discharge stages on installed debug2: first awake with light off, then awake at brightness 100%, warmth 50%, disconnected from power. Source: owner confirmation «Ровно по часу», researches/2026-11-06_debug_test_plan.md and prior capture qa_runs/debug2-charge-2026-11-06-180555/.
Acceptance: exact raw log backup verified against a second read; identify new rows, boots/sleep/charge/light transitions, sampling intervals, actual observable windows and missing data. Compare percent points per hour and gauge voltage by stage; do not label percentage-derived current as directly measured. Do not assume minute samples identify a seconds-precise boundary; owner's one-hour timing remains a separate source. The gauge is not a coulomb counter. No extrapolation to lifespan or certified battery capacity.
AUTH: owner connected reader and explicitly requested read/copy/analyze logs. Preserve debug2, card contents and existing source worktrees. No flash or settings changes.
Known mechanism from own prior source work: BatteryLog.cpp writes once per minute while awake, pauses in USB Drive (main.cpp); columns include gauge voltage, percent, charger status, logical light enabled, configured brightness and warmth. Warmth/brightness while light is OFF do not imply consumption at those settings.
Relevant EXPERIENCE.md search for Xteink/debug2/battery_log/АКБ/подсветк returned no lessons. Prior recon and raw charge run are the own-work reference.
Status: acquisition pending.
[/AI]

[AI]
Completed acquisition and analysis: qa_runs/debug2-light-hours-2026-11-06-201434/report.md, analysis.json and chart. 60 samples light off,60 light on; two marker intervals3605s. Source copied twice with matching bytes and matches the prior snapshot prefix. Owner suspects SD logging caused roughly5percentage points/hour; this run has no logging-disabled control. Owner proposes periodic sampling every20minutes; proposal recorded, no firmware change. Card ejected. Current activity is discussion of results, not firmware implementation.
[/AI]
