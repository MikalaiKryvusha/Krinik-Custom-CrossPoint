# TC — KCCP 1.1.4: denser toolbar lists on touch, the bigger night-mode circle, the version order

> **Created:** 2026-11-20 · **Parent:** the owner's tasks 2026-11-20 09:39 / 09:40, his mock-up verdicts 10:36
> (`interviews/decisions/mockups_1_1_4_2026-11-20.decision.json`), 10:20 (version order) · **Status:** written before the run; executed 2026-11-20 10:43–10:46 +03:00, all pass
> · **Outbound:** —

## Test basis

- Lists: «В меню … по ним открываеются листаемые списки - в них почему-то огромные отступы, нужно сделать более тестно»
  (09:40) → «Вариант 2» (10:36): on the touch X4 Pro the Contents / Text / More panels use rows max(theme row, 44 px) with
  a 6 px gap (was a 72 px stride, 3 items in landscape). Button boards keep the theme's dense rows.
- Circle: «кружок кнопки переключения темы сделать больше радиусом, на прочентов 20» (09:39), no remark at 10:36 → the
  shade's night tile circle 26 px across (was 22).
- Version order: «нужно проверку версий найчить различать -debug1, 2, 3» · «и RC1, RC2» · «как Линус выпускает версии»
  (10:20) → HOUSE_RULES П5 item 6; host cases in `firmware/test/kccp_version`.

## Dimensions

Orientation {landscape (the owner's, orientation 3), portrait} × panel {Contents, Text, More}; the owner's settings and
GEB copy (П4); the circle on the shade over the book. Consciously not covered here: button-only boards (the X4 Pro
simulator has touch; the code path keeps `denseRows` for them unchanged, read in the diff), other themes (Lyra is the
owner's; the judge computed 44 + 6 for Base/Lyra/RoundedRaff from the code).

## Cases

| # | Kind | Steps (simulator, `.tmp/ui_sd` / `.tmp/ui_sd_port`) | Expected | Status |
|---|---|---|---|---|
| 1 | smoke | open the book, centre tap, tap ≡ | Contents: ≥ 4 rows visible in landscape, 44 px rows + 6 px gap, titles not clipped | pass — run report 2026-11-20 |
| 2 | smoke | then tap T | Text settings: ≥ 4 rows, values right-aligned and whole, the checkbox row fits | pass — run report 2026-11-20 |
| 3 | smoke | then tap ⋯ | More: ≥ 4 rows, the «Ночной режим» checkbox fits | pass — run report 2026-11-20 |
| 4 | boundary | cases 1–3 in portrait | more rows than in landscape; no row clipped; no scroll strip on a list that fits | pass — run report 2026-11-20 |
| 5 | smoke | swipe the shade open over the book | the night tile shows the 26 px circle, centred in its 56 px tile | pass — run report 2026-11-20 |
| 6 | control | the 2026-11-20 «before» shots (`.tmp/ui_mock_2026-11-20/ui_before`) | the same panels show 3 rows at a 72 px stride | pass — run report 2026-11-20 |
| 7 | hygiene | `TARGETS="KccpVersionTest" sh tools/host_tests.sh`; then the full `sh tools/host_tests.sh` | 9/9; no new failure | pass — run report 2026-11-20 |
