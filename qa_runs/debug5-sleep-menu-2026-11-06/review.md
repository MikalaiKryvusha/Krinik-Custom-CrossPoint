# debug5 — home «Сон» review

[AI]
Owner's order 06.11 22:03: «сейчас в главном меню под фонариком делаем» (simpler than the configurable shade; shade findings parked).
Delta vs debug4: sleep.h icon (lucide moon rotated 90° CCW, checked against folder icon), UIIcon::Sleep, Lyra mapping, cover-grid tabs (7/8),
HomeMenuItem::SLEEP + index maps + count, ActivityManager requestSleep()/takeSleepRequest(), main loop → enterDeepSleep(), version debug5.
One independent judge (read-only): no BUG. RISK confirmed in code and fixed: a pending request survived a sleep entered by another path and
cancelled in the light linger → second unasked sleep; now enterDeepSleep() consumes the request first. RISK noted, not fixed: list themes have
no scroll — Lyra krinik 6–7 rows fit (≤782 px of 800); mama build + OPDS/plugins slot pushes the Mama row off-screen (8 rows); Lyra Extended
and Classic with 7–8 rows cut the last row. Nikolai uses Lyra. NIT: «should never be hit» comments after enterDeepSleep() are stale.
Checks: x4pro-krinik-debug SUCCESS; host 936/936 PASS; simulator X4 Pro: home shows «Сон» under «Фонарик»; tap → «Sleep requested» →
sleep screen → deep sleep → wake to Home; buttons 5×DOWN+ENTER → same; «Фонарик» still opens Flashlight. Mama build not compiled.
Device: not tested.
[/AI]
