# Test cases — idea 02: a tap on a book picture opens it full screen

**Created:** 2026-11-13 · **Under test:** `wip/krinik-debug9` (`firmware/`) — reader picture tap + the image viewer's
book mode · **Version/build:** simulator `simulator_x4_pro_win` first, then `1.1.1-debug9` on the owner's X4 Pro
**Test basis:** the owner's words, verbatim in `ideas/02_image_fullscreen_on_tap.md` (2026-11-13 10:34–10:41 +03:00):
«Тап по изображению в книге должен открывать изображение на Full Screen» (R1) · «жест свайп Назад - должен вести из Full
Screen просмотра картинки назад в книгу» (R2) · «тап в область миниатюры изодражения в книге - и это важнее, чем тамы
навигации по книжке» (R3); R4 is the unchanged behaviour outside pictures (control).

## 1. Goal vector

Achieve: a picture on a book page can be looked at full screen by one tap and left by the swipe Back, back on the
same page; taps outside pictures keep doing what they did.

## 2. Requirements under test

| # | Requirement (EARS sentence) | Fit criterion |
|---|---|---|
| R1 | WHEN the reader taps inside a picture on a book page, the reader shall show that picture full screen in the image viewer. | the shot after the tap shows the picture filling the screen; log `ERS: Image tap: <path>` |
| R2 | WHEN the viewer was opened from a book and the reader swipes Back, the viewer shall return to the same book page. | the shot after the swipe matches the page shot before the tap; log `Popped from activity stack` |
| R3 | WHEN the tap inside a picture lies in the centre (menu) or a side (page-turn) zone, the reader shall open the picture and shall neither open the menu nor turn the page. | shots: viewer, never the toolbar; the page number unchanged after the return |
| R4 | WHEN the reader taps outside every picture, the reader shall act on the zones as before (centre → menu, side → page turn). | shots: toolbar on a centre tap on text; next page on a side tap on text |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| tap position vs picture | inside (centre zone) · inside (side zone) · outside on text (centre, side) | on the picture's 1-px edge — host test covers the edges |
| picture kind | wide (600×260) · tall full-page (300×640) JPEG; small (240×160) PNG (C7) — own test book | the sample book holds 103 JPEG + 77 PNG (counted 2026-11-13 on the local copy); the other books not counted (the reader left the wire); GIF — drawn in books, the viewer cannot open it: the tap falls to the zones (known gap, judge finding 4) |
| orientation | landscape CCW (the owner's `orientation: 3`) | portrait, inverted, landscape CW — the hit-test is orientation-free (logical coordinates); device check optional |
| return path | swipe Back | the physical Back button of other boards — X4 Pro has none |
| state | fresh card, first open of the book | sleep while the viewer is open; a book with cached pages from an older build — device check by the owner |
| memory | simulator (no ESP32 heap) | heap on the reader — the owner's serial log during his check |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| C1 | boot into `image_test.epub` (card `qa_runs/sd_book_images`) → page 1 shows picture 1 under the heading, no `[ERR]` | smoke | pass — [TESTED: 2026-11-13 · simulator, page 1/8 read · testcases/reports/2026-11-13_idea02_simulator.md] |
| C2 | C1 → `TAP` at picture 1's centre → the viewer shows picture 1 full screen; log `Image tap` | use case (R1, R3 centre) | pass — [TESTED: 2026-11-13 · simulator, viewer shot + log `Image tap` · testcases/reports/2026-11-13_idea02_simulator.md] |
| C3 | C2 → `SWIPE` from x < 120 to the right → book page 1 again, the same as C1's shot | state transition (R2) | pass after the simulator fix (bugs/06) — [TESTED: 2026-11-13 · back shot = page 1/8 · testcases/reports/2026-11-13_idea02_simulator.md] |
| C4 | C1 → `TAP` inside picture 1 near its right end (a side zone) → the viewer, not page 2 | decision table (R3 side) | pass — [TESTED: 2026-11-13 · tap x=0.83 → viewer · testcases/reports/2026-11-13_idea02_simulator.md] |
| C5 | page with the tall picture 2 (fills the page) → `TAP` on it → viewer; swipe Back → same page | boundary (full-page picture) | pass — [TESTED: 2026-11-13 · page 4/8 → viewer → 4/8 · testcases/reports/2026-11-13_idea02_simulator.md] |
| C6 | C2 → two Back `SWIPE`s ~300 ms apart (the second while the picture is still on the glass) → book page 1, NOT the page before; log `Back swipe before the page repaint ignored` | error guessing (judge finding 7) | skipped in the simulator (repaint ~13 ms) — device check, homework 04 |
| C7 | the page with the small PNG picture 3 → `TAP` on it → the viewer shows it full screen; Back → the same page | partition (PNG: 77 of the sample book's 180 pictures) | [NOT-TESTED] |

## 5. Control cases

| # | Control → expected: the behaviour is absent | Status + evidence |
|---|---|---|
| K1 | C1 → `TAP` on text in the centre zone → the toolbar menu, no viewer (R4) | pass — [TESTED: 2026-11-13 · centre tap on text → toolbar · testcases/reports/2026-11-13_idea02_simulator.md] |
| K2 | C1 → `TAP` on text in a side zone → page 2, no viewer (R4) | pass — [TESTED: 2026-11-13 · side tap on text → 2/8 · testcases/reports/2026-11-13_idea02_simulator.md] |
| K3 | the same `TAP` as C2 on a `wip/krinik-debug8` build → the menu opens, no viewer (the feature off) | pass — [TESTED: 2026-11-13 · debug8: menu, no viewer · testcases/reports/2026-11-13_idea02_simulator.md] |

## 6. Verdict

partial — the simulator run passes (C6 skipped there); the feature waits for the owner's reader (homework 04): testcases/reports/2026-11-13_idea02_simulator.md.
