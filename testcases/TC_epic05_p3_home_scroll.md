# Test cases — epic 05, phase 3: the Home button list scrolls

**Created:** 2026-11-14 · **Under test:** `wip/kccp-1.1.3-debug2` (`firmware/`) — `HomeActivity` (the visible slice, the
swipe over the list, the keys, the scroll bar, the touch rows) · **Version/build:** simulator `simulator_x4_pro_win`
(plain) and `simulator_x4_pro_mama_win` (mama, `-DKRINIK_MAMA=1`), then `1.1.3-debug2` on the owner's X4 Pro
**Test basis:** `plans/09_DONE_epic05_p3_home_scroll.md` → criteria 1–6; the meta-plan `plans/05_EPIC_home_buttons.md` →
criteria 4 and 5; the owner, interview #004 Q5.

## 1. Goal vector

Achieve: when the buttons do not fit, the button list scrolls by a swipe that starts on it and follows the keys; the
cover stays; when they fit, nothing scrolls.

## 2. Requirements under test

| # | Requirement (EARS) | Fit criterion |
|---|---|---|
| R1 | WHILE 8 buttons and 7 fit (mama, Lyra, plugins on), WHEN a swipe up starts on the list, the list shall show buttons 2–8 and a scroll bar; the cover band shall not change. | shots before/after: «Для любимой Мамы» whole; the cover band crop: 0 px ≥ 40 levels apart |
| R2 | WHILE all buttons fit (plain, Lyra, 6), WHEN a swipe up starts on the list, the screen shall not change. | shots before/after: 0 px ≥ 40 levels apart below the status bar |
| R3 | WHEN the list is scrolled, a tap on a visible row shall open that row's button. | log `Entering activity: Mama` after a tap on the last row |
| R4 | WHEN the Down key moves the selection past the last visible row, the list shall scroll to show it. | shot: the 8th button selected and visible |
| R5 | WHEN Home opens with the cursor on a button below the fold, the list shall show it. | shot after Back from Mama: «Для любимой Мамы» visible and selected |
| R6 | WHILE a theme fits fewer buttons than are on, its list shall scroll the same way (Lyra Extended plain + plugins; Classic, RoundedRaff mama + plugins); the cover grid shall draw all icons in one bar. | shots per theme |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| build | plain, mama | — |
| overflow | 0 (6 on Lyra), 1 (8 on Lyra mama; 7 on Lyra Extended plain), 2 (Lyra Extended mama + plugins: 8 rows, 6 visible; RoundedRaff mama + plugins + a book: 9 rows, 7 visible) — the Ф3 judge's simulation | 3+ (no build has that many rows) |
| theme | Lyra, Lyra Extended, Classic, RoundedRaff, cover grid | — |
| input | swipe on the list, swipe on the cover (stays today's behaviour), keys Next, tap | long press (Ф5) |

Note (the Ф3 judge): a swipe whose finger rests ≥ 90 ms in the tap slop before moving first selects the touched row
(`RowTouch::Down`, old behaviour) — the S1 swipe is scripted as one continuous motion; a selection change seen there is
that rule, not a scroll.

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| S1 | plain, Lyra, 6 buttons: shot → swipe up from the list → shot; equal | boundary (fits) | pass · `epic05_p3_s1`: 0 px ≥ 40 apart (60 ms swipe) |
| S2 | mama, Lyra, plugins: shot (7 rows + bar) → swipe up from the list → shot: rows 2–8, bar moved, cover band equal; the log holds 0 `Outside range` lines (the baseline run `epic05_p3_before`: 452) | boundary (overflow 1) | pass · `epic05_p3_s2`: rows 2–8, bar moved, cover band equal, 0 `Outside range` |
| S3 | the S2 state → tap the last visible row → `Entering activity: Mama` | state transition | pass · `epic05_p3_s3` → `Entering activity: Mama` |
| S4 | mama, Lyra, plugins: NEXT × 8 from the first cover/button → shot: «Для любимой Мамы» selected, visible | state transition | pass · `epic05_p3_s4` (`DOWN` ×7; `NEXT` is the cover key) → «Для любимой Мамы» selected, visible |
| S5 | mama, Lyra, plugins: tap «Для любимой Мамы» after scroll → Mama → Back → shot: Home with it visible and selected | state transition | pass · `epic05_p3_s5`: back from Mama, rows 2–8, selected |
| S6 | Lyra Extended plain + plugins; Classic and RoundedRaff mama + plugins: swipe up from the list → shots | equivalence (theme) | pass · `epic05_p3_classic`, `_lyx_plain`, `_rr`: up → last rows, down → top |
| S6b | overflow 2: Lyra Extended mama + plugins (6 of 8 visible) — swipe up → rows 3–8, the thumb at the end; swipe down → rows 1–6 | boundary (a page step clamped to 2) | pass · `epic05_p3_lyx_mama`: up → rows 3–8, down → rows 1–6 |
| S6c | RoundedRaff plain + plugins + a recent book (8 rows: «Продолжить чтение» + 7 buttons, 7 visible): before Ф3 row 8 fell off the screen; swipe up → rows 2–8 | regression (an old off-screen row) | pass · `epic05_p3_rrbook`: 7 of 8, up → rows 2–8, the book card unchanged |
| S7 | cover grid, mama + plugins: shot — 8 icons in one bar | equivalence | pass · `epic05_p3_grid`: 8 icons in one bar |
