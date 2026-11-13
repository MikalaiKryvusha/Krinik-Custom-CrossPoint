# Test cases — epic 01, phase 3: the shade draws the owner's row; «Сон», «Фонарик»; the long tap

**Created:** 2026-11-13 · **Under test:** `wip/kccp-1.1.3-debug2` (`firmware/`) — `FrontlightPanelActivity` (the row,
the buttons, the long tap), `FlashlightActivity` (return to the caller), `ShadeTilesActivity` (the entry from the shade:
the cursor, the keys flag, `isOpen`) · **Version/build:** simulator `simulator_x4_pro_win` (built WITHOUT Bluetooth),
then `1.1.3-debug2` on the owner's X4 Pro
**Test basis:** `plans/04_DONE_epic01_p3_shade_row.md` → criteria 1–8; the meta-plan `plans/01_EPIC_shade_tiles.md` →
«Критерии приёмки» 1, 2, 4, 5, 6, 7 and the Ф3 gate («снимки шторки с 5, 6 и 7 кнопками в обеих ориентациях; критерии
1, 2, 4, 5, 6, 7 на симуляторе»).

## 1. Goal vector

Achieve: the shade shows the owner's buttons in his order with equal gaps; «Сон» and «Фонарик» work over a book; a long
tap on a button opens «Кнопки в шторке» on that button, and Back returns to the book page.

## 2. Requirements under test

| # | Requirement (EARS) | Fit criterion |
|---|---|---|
| R1 | WHEN the shade opens, it shall draw the shown buttons that are on, in the stored order, with equal gaps at the edges and between them. | shot: the buttons and their order; the gaps measured on the shot differ by ≤ 1 px (the layout itself is the Ф1 host test) |
| R2 | WHEN the owner holds a button 500 ms, the shade shall open «Кнопки в шторке» in portrait with the cursor on that button's row. | log `Long tap on <id>` + `Entering activity: ShadeTiles`; the shot: the pill on that row |
| R3 | WHEN he leaves that screen, the shade shall close behind it and the book page shall be on the screen in the book's orientation. | log: two `Popped`; the shot = the book page, landscape, no shade |
| R4 | WHEN he taps «Фонарик», the flashlight screen shall open over the book; its tap shall return to the book page. | log `Entering activity: Flashlight`, then two `Popped`; the page shot |
| R5 | WHEN he taps «Сон», the reader shall go to sleep. | log: the sleep entry; the sleep shot |
| R6 | IF the shade lies over «Кнопки в шторке», THEN a long tap shall only close the shade (no second copy). | log: one `Entering activity: ShadeTiles` in the run |
| R7 | A long press that began on a slider shall not be consumed (the slider still drags). | — not expressible in the simulator's script (see §5) |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| button count | 4 (default on the simulator: Bluetooth not compiled), 5 (+ «Сон»), 6 (+ «Фонарик») | 7 — needs Bluetooth: the owner's reader |
| orientation | the shade over the book in «Альбомная 180°» (card `sd_book_images`, orientation 3); over Home (portrait) | the two other orientations — same code path, the turned orientation glyph is today's |
| entry to the settings | long tap on a shade button over the book | over the image viewer (keys flag, risk 5) — a follow-up case if time allows |
| buttons | night, cleanup, orientation, touch (old behaviour, one tap each), «Сон», «Фонарик» | Bluetooth (not compiled); slide-switch-owned buttons (no switch on the simulator) |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| D1 | Book (`sd_book_images`) → top-edge swipe → shade: four buttons Ночной режим (half-filled circle), Очистка, Ориентация, Сенсор; equal gaps at the edges and between (shot) | smoke (R1) | pass — [TESTED: 2026-11-13 · shot d1, shade_gaps spread 1 (the old row 34) · testcases/reports/2026-11-13_epic01_p3.md] |
| D2 | D1 → long tap on «Ориентация» (third) → `Long tap on orientation`, `Entering activity: ShadeTiles`; portrait shot with the pill on «Ориентация» | use case (R2) | pass — [TESTED: 2026-11-13 · log Long tap on orientation, shot d2 · testcases/reports/2026-11-13_epic01_p3.md] |
| D3 | D2 → swipe Back → two `Popped`; the shot = the book page in landscape, no shade | use case (R3) | pass — [TESTED: 2026-11-13 · two Popped, shot d3 the book · testcases/reports/2026-11-13_epic01_p3.md] |
| D4 | D1 → long tap on «Ночной режим» → the screen; tap «Сон» ☑, ▲ ×3 on «Сон» (the meta-plan's ×4 counts the Bluetooth row the simulator hides: «Сон» is 5th here) → Back → book; open the shade again → five buttons, «Сон» (moon) second (shot); `settings.json` lists `sleep` second | use case (meta criterion 2) | pass — [TESTED: 2026-11-13 · settings.json night,sleep,…, shot d4c five buttons · testcases/reports/2026-11-13_epic01_p3.md] |
| D5 | Card with «Фонарик» on (a hand-written `shadeTiles` with `flashlight` on) → shade → tap «Фонарик» → `Entering activity: Flashlight` (shot: the lamp button upright in the shade before the tap); tap → two `Popped` → the book page | use case (R4) | pass — [TESTED: 2026-11-13 · Flashlight then two Popped, shot d5c · testcases/reports/2026-11-13_epic01_p3.md] |
| D6 | Card with «Сон» on → shade → tap «Сон» → the sleep entry in the log (shot of the sleep screen) | use case (R5) | pass — [TESTED: 2026-11-13 · Entering activity: Sleep, shot d6 · testcases/reports/2026-11-13_epic01_p3.md] |
| D7 | Home → Settings → «Экран» → «Кнопки в шторке» → top-edge swipe (the shade over the screen) → long tap on a button → the shade closes; ONE `Entering activity: ShadeTiles` in the log | control (R6) | pass — [TESTED: 2026-11-13 · one Popped, one ShadeTiles entry, shot d7b · testcases/reports/2026-11-13_epic01_p3.md] |
| D8 | Each old button by one tap in the shade over the book: night mode inverts, cleanup closes the shade, orientation cycles, touch toggles (shots/log) | regression | pass — [TESTED: 2026-11-13 · shots d8*, settings.json · testcases/reports/2026-11-13_epic01_p3.md] |

## 5. Not covered — said aloud

- Coordinates (landscape book, row y 0.5875): four buttons at x 0.191 · 0.397 · 0.628 · 0.859; six at 0.132 · 0.279 ·
  0.426 · 0.574 · 0.721 · 0.868 (`tileLeft` over the 768 px row from x 16, button 56 px).

- Seven buttons (Bluetooth), the slide-switch-owned buttons, the panel's look — the owner's reader.
- R7 (a resting finger on a slider, then a drag): the simulator script has TAP (a hold in place) and SWIPE (a moving
  contact from its first ms) but no «hold still, then move» — the guard is read in the code (`contactOnTiles`) and the
  judge; the owner's hand on the reader is the real check.
