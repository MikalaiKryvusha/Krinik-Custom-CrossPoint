# Test cases — epic 05 Ф5: a long tap on a Home button opens «Кнопки домашнего экрана» on that button

**Created:** 2026-11-17 · **Under test:** `HomeActivity::loop` (list themes), `CoverGridHomeUi::selectedAction` (cover
grid), `HomeActivity::onButtonSettingsClosed` · **Version/build:** `wip/kccp-1.1.3-debug2` + the Ф5 diff, simulators
`simulator_x4_pro_win` and `simulator_x4_pro_mama_win`
**Test basis:** `plans/11_DONE_epic05_p5_home_long_tap.md` (criteria 1–6); `plans/05_EPIC_home_buttons.md` → Ф5 (criteria 7–9);
`[OWNER]` interview #004, Q4 → A (a long tap of 0.5 s on a Home button opens its setting).

## 1. Goal vector

Achieve: the owner reaches a Home button's setting from the button itself. Maintain: a short tap, a long hold on a
cover, and every other theme behaviour stay as they are.

## 2. Requirements under test

| # | Requirement (EARS sentence) | Fit criterion (Scale · Meter · Target) |
|---|---|---|
| R1 | WHEN the owner holds a Home button for 800 ms, the firmware shall open «Кнопки домашнего экрана» with the cursor on that button's row. | log line + shot · simulator · `Entering activity: HomeScreenButtons`, the row selected — in all five themes |
| R2 | WHEN the owner taps a Home button briefly, the firmware shall run the button as before. | log · simulator · `Entering activity: Flashlight` for «Фонарик» |
| R3 | WHEN the screen opened by a long tap is left with Back after a button was moved, Home shall show the new order. | shot · simulator · «Сон» one row higher |
| R4 | IF the owner long-taps «Сон», THEN the reader shall not go to sleep. | log · simulator · no sleep line, the screen opens |
| R5 | WHEN the owner holds a recent-book cover, the book shall open as before. | log · simulator · `Entering activity: EpubReader` |
| R6 | WHERE the mama build runs, a long tap on «Для любимой Мамы» shall open the screen on «Для Мамы». | shot · mama simulator |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| theme | Classic, Lyra, Lyra 3 covers, RoundedRaff, Cover grid (`qa_runs/sd_theme0…4`) | — |
| contact | long hold on a button, short tap, long hold on a cover, long hold on «Сон» | a long hold that starts on a button and slides (a swipe is not a long press — SDK) |
| return | Back after a move; the cursor on the same button | a button switched off on the screen (the selection falls to the first button — read in code, not run) |
| build | plain, mama | — |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| L1 smoke | Lyra: hold «Фонарик» 800 ms → `Entering activity: HomeScreenButtons`, the «Фонарик» row selected | use case | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic05_p5.md] |
| L2 smoke | Lyra: tap «Фонарик» → `Entering activity: Flashlight` | use case | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic05_p5.md] |
| L3 | Lyra: hold «Сон» → the screen opens on «Сон», no sleep | error guessing | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic05_p5.md] |
| L4 | Lyra: hold «Фонарик», ▲ on «Сон», Back → Home shows «Сон» above «Фонарик», the cursor on «Фонарик» | state transition | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic05_p5.md] |
| L5 | Classic, Lyra 3 covers, RoundedRaff: hold «Фонарик» → the screen on «Фонарик» | equivalence (themes) | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic05_p5.md] |
| L6 | Cover grid: hold the «Фонарик» tab → the screen on «Фонарик»; tap the tab → Flashlight; hold «Сон» at the bottom edge (y 0.995) → the screen, no sleep | equivalence (themes) | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic05_p5.md] |
| L7 | a recent book on the card: hold its cover → `Entering activity: EpubReader` (list theme and cover grid) | boundary (contact start) | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic05_p5.md] |
| L8 | mama build, Lyra: hold «Для любимой Мамы» → the screen on «Для Мамы» | equivalence (build) | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic05_p5.md] |

## 5. Control cases

| # | Control → expected: the behaviour is absent | Status + evidence |
|---|---|---|
| K1 | L1 on the binary before the change → the hold opens the flashlight on the release (the old tap) | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic05_p5.md] |
| K2 | the grid's long-tap band = the DRAWN tab bar (mutant): «Сон» held at the bottom edge → sleep | pass — red on the mutant, `testcases/reports/2026-11-17_epic05_p5.md` run 5 |
