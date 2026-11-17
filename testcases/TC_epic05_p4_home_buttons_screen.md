# Test cases — epic 05, phase 4: the screen «Кнопки домашнего экрана» (and «Кнопки в шторке» on the shared base)

**Created:** 2026-11-14 · **Under test:** `wip/kccp-1.1.3-debug2` (`firmware/`) — `ToggleRowsActivity` (the shared rows
screen), `ShadeTilesActivity` (refactored onto it), `HomeScreenButtonsActivity` (new), the «Настройки → Экран» row ·
**Version/build:** simulators `simulator_x4_pro_win`, `simulator_x4_pro_mama_win`, then `1.1.3-debug2` on the owner's
X4 Pro
**Test basis:** `plans/10_DONE_epic05_p4_home_buttons_screen.md` → criteria 1–6; the meta-plan `plans/05_EPIC_home_buttons.md`
→ criteria 1, 2, 3, 10; the owner, interview #004 Q1, Q3; the shade screen's own basis — `testcases/TC_epic01_p2_tiles_screen.md`.

## 1. Goal vector

Achieve: the owner switches Home buttons on and off and reorders them on a Settings screen that works like «Кнопки в
шторке»; «Настройки» cannot be switched off; «Кнопки в шторке» keeps working exactly as before on the shared code.

## 2. Requirements under test

| # | Requirement (EARS) | Fit criterion |
|---|---|---|
| R1 | WHEN «Настройки → Экран» opens, it shall list «Настройки сна», «Кнопки в шторке», «Кнопки домашнего экрана» first. | shot |
| R2 | WHEN «Кнопки домашнего экрана» opens, it shall show one row per Home button of the build in the stored order (Home glyph, name, ▲ ▼, checkbox), «Настройки» without a checkbox. | shot: no plugins/OPDS — plain 6 rows, mama 7; with them 7 / 8 |
| R3 | WHEN the owner taps a row with a checkbox, it shall flip; Back saves; Home then shows the change. | log `Home buttons saved:`; `settings.json`; Home shot |
| R4 | WHEN the owner taps the «Настройки» row, nothing shall change. | shot; no `-settings` |
| R5 | WHEN the owner taps ▲ on a row, it shall move up one row; Home follows. | shot; key; Home shot |
| R6 | WHEN Back is pressed, «Настройки → Экран» shall come back. | log `Popped`; shot |
| R7 | «Кнопки в шторке» on the shared base shall pass its epic 01 Ф2 cases C1–C8 again. | the Ф2 scripts, their shots and log lines |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| build | plain (6 rows), mama (7 rows) on a card with no plugins/OPDS | with them (7 / 8 rows) — not run |
| row kind | checkbox row, the locked «Настройки», the plugins/OPDS row (plugins off → «OPDS браузер») | the plugins/OPDS row with plugins on (label «Плагины») — one shot if time allows |
| input | tap on a row, tap on ▲, Back key; the shade's own C1–C8 (taps, header arrow, swipe Back, keys) | moving a row by keys (not built, epic 01 Ф2 open detail) |
| entry | from «Настройки → Экран» | from a Home long tap (Ф5) |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| H1 | Home → Настройки → Экран: shot — the three rows in order | smoke | pass · `epic05_p4_h1` |
| H2 | → «Кнопки домашнего экрана» (plain): shot — 6 rows (no plugins/OPDS), «Настройки» with no checkbox | smoke | pass · `epic05_p4_h2`: 6 rows |
| H3 | tap «Передача файлов» row → unchecked; ▲ on «Сон» → «Сон» above «Фонарик»; Back → log `Home buttons saved: …-transfer…sleep,flashlight`; Home shot without «Передачи файлов», «Сон» above «Фонарик» | state transition | pass · `epic05_p4_h3`: the saved key, Home shot |
| H4 | tap the «Настройки» row → no change (shot equal) | negative | pass · `epic05_p4_h3` (the tap on «Настройки») |
| H5 | mama build: the screen shows 7 rows (no plugins/OPDS) incl. the mama row, its name whole before ▲ — «Для Мамы» since interview #006 → A (2026-11-17) | equivalence (build) | 2026-11-14 fail (taste) · `epic05_p4_h5`: «Для любимой Ма…» → interview #006; 2026-11-17: before `mama_label_before` «Для любимой Ма…», after — `mama_label_after` |
| S-C1…C8 | the shade screen, epic 01 Ф2 scripts unchanged except the run names | regression | pass · `epic05_p4_c1`…`_c8`: the saved rows equal 2026-11-13 |
