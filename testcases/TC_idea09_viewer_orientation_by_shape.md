# Test cases — idea 09: the image viewer opens a picture by its shape

**Created:** 2026-11-13 · **Under test:** `wip/kccp-1.1.3-debug2` (`firmware/`) — `BmpViewerActivity::shapeTurns()` and
its two call sites (`onEnter`, `openSibling`) · **Version/build:** simulator `simulator_x4_pro_win`, then 1.1.3-debug2
on the owner's X4 Pro
**Test basis:** `ideas/09_viewer_orientation_by_picture_shape.md` — the owner's cases А–Г (2026-11-13 14:53, verbatim
there) and the acceptance table; the agent's open decisions (square / unreadable → as the reader stands; every picture
by its own shape).

## 1. Goal vector

Achieve: every picture opens the way its shape reads best — a wide one in a landscape orientation, a tall one in a
portrait one — from the file browser and from a book.

## 2. Requirements under test

| # | Requirement (EARS) | Fit criterion |
|---|---|---|
| R1 (А) | WHEN a wide picture opens and the reading orientation is landscape, the viewer shall show it in that landscape. | landscape shot; `Shape turns: 0` |
| R2 (Б) | WHEN a wide picture opens and the reading orientation is portrait, the viewer shall show it in «Альбомная 180°». | log `Shape turns: 1` (from «Книжная») / `3` (from «Инверсия»); landscape shot |
| R3 (В) | WHEN a tall picture opens and the reading orientation is portrait, the viewer shall show it in that portrait. | portrait shot; `Shape turns: 0` |
| R4 (Г) | WHEN a tall picture opens and the reading orientation is landscape, the viewer shall show it in «Книжная». | log `Shape turns: 3` (from «Альбомная 180°») / `1` (from «Альбомная»); portrait shot |
| R5 | A square picture shall open as the reader stands. | `Shape turns: 0 (…x… equal)`; the shot in the reading orientation |
| R6 | WHEN the owner pages to the next picture, it shall open by its own shape. | the log line per picture |
| R7 | The book picture (idea 02 entry) shall follow the same rule. | `Shape turns` for the book picture in a portrait book |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered |
|---|---|---|
| reading orientation | all four (cards `sd_idea09_o0…o3`, temporary) | — |
| shape | wide · tall · square | an EXIF-rotated JPEG (none on the stand) |
| format | JPEG (wide) · PNG (tall) · BMP (square) | GIF (the viewer does not open it) |
| entry | file browser + paging; a book picture | — |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| E1 | o3 «Альбомная 180°»: Home → «Обзор файлов» → `pics` → `a_wide.jpg` → landscape, `Shape turns: 0` | smoke (R1) | pass — [TESTED: 2026-11-13 · run 1, shot a · testcases/reports/2026-11-13_idea09.md] |
| E2 | E1 → next picture → `b_tall.png` → `Shape turns: 3`, portrait shot | state transition (R4, R6) | pass — [TESTED: 2026-11-13 · run 1, shot c · testcases/reports/2026-11-13_idea09.md] |
| E3 | E2 → next → `c_square.bmp` → `Shape turns: 0`, landscape | boundary (R5) | pass — [TESTED: 2026-11-13 · run 1 · testcases/reports/2026-11-13_idea09.md] |
| E4 | o0 «Книжная»: `a_wide.jpg` → `Shape turns: 1`, landscape shot | use case (R2) | pass — [TESTED: 2026-11-13 · run 2, shot a · testcases/reports/2026-11-13_idea09.md] |
| E5 | E4 → next → `b_tall.png` → `Shape turns: 0`, portrait | use case (R3, R6) | pass — [TESTED: 2026-11-13 · run 2 · testcases/reports/2026-11-13_idea09.md] |
| E6 | o1 «Альбомная»: open `b_tall.png` → `Shape turns: 1`, portrait | use case (R4, the other landscape) | pass — [TESTED: 2026-11-13 · run 3 · testcases/reports/2026-11-13_idea09.md] |
| E7 | o2 «Инверсия»: open `a_wide.jpg` → `Shape turns: 3`, landscape | use case (R2, the other portrait) | pass — [TESTED: 2026-11-13 · run 4, shot a · testcases/reports/2026-11-13_idea09.md] |
| E8 | the test book in «Книжная»: tap `pic1` (wide) → `Shape turns: 1`, landscape | use case (R7) | pass — [TESTED: 2026-11-13 · run 5, shot e8 · testcases/reports/2026-11-13_idea09.md] |
| E9 | E8 → a long tap on the right half → `View turns: 2` (idea 07 still turns from the shape's start) | regression | pass — [TESTED: 2026-11-13 · run 5, View turns: 2 · testcases/reports/2026-11-13_idea09.md] |
| E10 | o0: `a_wide.jpg` open (turns 1) → the shade's «Ориентация» (0 → 1) → close → `Shape turns: 0 (…, reading orientation 1)`, the wide picture landscape | the judge's finding (R1 after an orientation change) | pass — [TESTED: 2026-11-13 · run 6 · testcases/reports/2026-11-13_idea09.md] |

## 5. Not covered — said aloud

- An EXIF-rotated JPEG from a phone (the judge reads whether the painter honours EXIF) — the owner's own pictures.
- The control «without the feature»: the debug1 behaviour (always the reading orientation) is recorded in the idea 07
  runs (`testcases/reports/2026-11-13_idea07_simulator.md`).
