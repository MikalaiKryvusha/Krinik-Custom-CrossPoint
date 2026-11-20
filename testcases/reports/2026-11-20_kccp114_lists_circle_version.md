# Run report — KCCP 1.1.4: denser toolbar lists on touch, the bigger night circle, the version order

## Work

The case set `testcases/TC_kccp114_toolbar_lists_circle.md` (written before the run): the owner's picks of 2026-11-20 10:36
(`interviews/decisions/mockups_1_1_4_2026-11-20.decision.json`: lists «Вариант 2», the circle without a remark) and his
words of 10:20 on the version order (HOUSE_RULES П5 item 6).

## Contour

Firmware `wip/kccp-1.1.4` at `78d89fcd` + the uncommitted diff of this run (`ReaderToolbarUi.cpp`, `customListIcons.h`,
`KccpVersion.h`, `OtaUpdater.cpp`, `test/kccp_version`, `platformio.ini`); simulator `simulator_x4_pro_win` on the
simulator branch `fix/x4pro-viewable-insets` (the X4 Pro viewable insets = the device's, EXP-0041); the П4 stand — the
owner's `settings.json` read from his card 2026-11-20 09:41 (Lyra, Literata 16, landscape orientation 3) and his GEB copy,
`.tmp/ui_sd`; the portrait copy `.tmp/ui_sd_port` (orientation 0, all else the same).

## Runs

| # | When | Command | Result |
|---|---|---|---|
| 1 | 2026-11-20 10:42 +03:00 (build-log mtime) | `pio run -d firmware -e simulator_x4_pro_win` | SUCCESS, 110 s |
| 2 | 2026-11-20 10:43 +03:00 (log mtime) | `KEEP_BMP=1 SD_TEMPLATE=../.tmp/ui_sd SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh d114_2_land "…centre tap; ≡; T; ⋯; the shade swipe…"` | 6 shots, 9 `[ERR]` (the simulator's TTF autohint lines) |
| 3 | 2026-11-20 10:44 +03:00 (log mtime) | the same on `.tmp/ui_sd_port` as `d114_2_port` (tool row taps at y 0.94) | 5 shots, 9 `[ERR]` |
| 4 | 2026-11-20 10:39 +03:00 (log mtime) | `TARGETS="KccpVersionTest" sh tools/host_tests.sh` (+ two mutants run red earlier: «true at equal numbers» → 3 cases red; «all label ranks 0» → `ReleaseCandidatesAsTheKernel` red) | 9/9 |
| 5 | 2026-11-20 10:46 +03:00 (log mtime) | `sh tools/host_tests.sh` | 990 tests, 10 failed = the known list, no new failure |

## Checks

Hygiene: host 9/9 for the version order with two mutants seen red; the full host suite — no new failure; two judges over
the diffs (version: no BLOCKER/MAJOR, minors fixed — `%n` guard, `strtol` clamp, asset tests; UI: no BLOCKER/MAJOR).
Functional run: the simulator on the owner's settings and book, by the user's path (centre tap → ≡ / T / ⋯; the shade by
its swipe), the shots READ:

| Case | Status | Observed |
|---|---|---|
| 1 Contents, landscape | pass | 4 rows at a 50 px stride (was 3 at 72), titles whole |
| 2 Text, landscape | pass | 4 rows; values right-aligned and whole |
| 3 More, landscape | pass | 4 rows; the «Ночной режим» and «Подсветка» checkboxes fit |
| 4 portrait | pass | Contents 7 rows, Text 5, More 7; no row clipped vertically; long titles and «Выравнивание абз…» end in «…» — a width matter this change does not touch |
| 5 the shade circle | pass | the night tile's circle 26 px, centred in its tile |
| 6 control | pass | the 2026-11-20 «before» shots (`.tmp/ui_mock_2026-11-20/ui_before`) show 3 rows at 72 px |
| 7 hygiene | pass | runs 4 and 5 |

## Found

None in this run. Earlier the same day, the stand defect EXP-0041 (the simulator's X4 Pro insets) — fixed before these runs.

## Traces

Shots `qa_runs/d114_2_land/shots/`, `qa_runs/d114_2_port/shots/` (parked to `.tmp/` after the run — the book's text);
the tiles `.tmp/mock/smoke_land.webp`, `.tmp/mock/smoke_port.webp`; logs `.tmp/mock/build_final.log`,
`.tmp/mock/host_full.log`, `.tmp/host_tests_KccpVersionTest.log`.

## Verdict

pass — the three panels and the circle as the owner picked them, on his settings and book; the version order by its host
cases. Not verified on the reader: the e-ink look of 44 px rows and the finger target on the real touch panel; the OTA
path itself (no release fetched) — both with the 1.1.4-debug2 image.
