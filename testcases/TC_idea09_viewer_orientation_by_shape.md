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
| R1 (А) | WHEN a wide picture opens and the reading orientation is landscape, the viewer shall show it in that landscape. | landscape shot; no `Shape turns` line |
| R2 (Б) | WHEN a wide picture opens and the reading orientation is portrait, the viewer shall show it in «Альбомная 180°». | log `Shape turns: 1` (from «Книжная») / `3` (from «Инверсия»); landscape shot |
| R3 (В) | WHEN a tall picture opens and the reading orientation is portrait, the viewer shall show it in that portrait. | portrait shot; no `Shape turns` line |
| R4 (Г) | WHEN a tall picture opens and the reading orientation is landscape, the viewer shall show it in «Книжная». | log `Shape turns: 3` (from «Альбомная 180°») / `1` (from «Альбомная»); portrait shot |
| R5 | A square picture shall open as the reader stands. | no `Shape turns` line; the shot in the reading orientation |
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
| E1 | o3 «Альбомная 180°»: Home → «Обзор файлов» → `pics` → `a_wide.jpg` → landscape, no `Shape turns` | smoke (R1) | not run |
| E2 | E1 → next picture → `b_tall.png` → `Shape turns: 3`, portrait shot | state transition (R4, R6) | not run |
| E3 | E2 → next → `c_square.bmp` → no `Shape turns`, landscape | boundary (R5) | not run |
| E4 | o0 «Книжная»: `a_wide.jpg` → `Shape turns: 1`, landscape shot | use case (R2) | not run |
| E5 | E4 → next → `b_tall.png` → no `Shape turns`, portrait | use case (R3, R6) | not run |
| E6 | o1 «Альбомная»: open `b_tall.png` → `Shape turns: 1`, portrait | use case (R4, the other landscape) | not run |
| E7 | o2 «Инверсия»: open `a_wide.jpg` → `Shape turns: 3`, landscape | use case (R2, the other portrait) | not run |
| E8 | the test book in «Книжная»: tap `pic1` (wide) → `Shape turns: 1`, landscape | use case (R7) | not run |
| E9 | E4 → a long tap on the right half → `View turns: 2` (idea 07 still turns from the shape's start) | regression | not run |

## 5. Not covered — said aloud

- An EXIF-rotated JPEG from a phone (the judge reads whether the painter honours EXIF) — the owner's own pictures.
- The control «without the feature»: the debug1 behaviour (always the reading orientation) is recorded in the idea 07
  runs (`testcases/reports/2026-11-13_idea07_simulator.md`).
