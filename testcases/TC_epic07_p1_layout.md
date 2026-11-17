# Test cases — epic 07 Ф1: a picture and its caption stay on one page

**Created:** 2026-11-17 · **Under test:** keep-together groups in `ChapterHtmlSlimParser` (`<figure>`, `break-inside:
avoid`), the picture shrink · **Version/build:** `wip/kccp-1.1.3-debug2`, host suite + simulator `simulator_x4_pro_win`
**Test basis:** `plans/12_DONE_epic07_p1_layout.md` criteria 1–4 = the meta-plan's 1, 2, 5, 6 (`plans/07_EPIC_figure_caption.md`);
the owner 2026-11-13 10:38 «всегда нужно держать подпись рядом с картинкой», 10:39 (the picture may shrink), 2026-11-17
10:40 «подпись ВСЕГДА должна быть рядом с картинкой, ни в коем случае не должна открываться на отдельную страницу».

## 1. Goal vector

Avoid: a caption opening a page alone after its picture. Achieve: the group moves together; the picture shrinks when the
group does not fit an empty page; books with no group lay out as before.

## 2. Requirements under test

| # | Requirement (EARS sentence) | Fit criterion (Scale · Meter · Target) |
|---|---|---|
| R1 | WHEN a figure's caption line does not fit under its picture, the firmware shall move the picture and the caption to the next page. | page index of the picture = of the caption's first line · host test + shots · equal |
| R2 | WHEN a figure is taller than an empty page, the firmware shall shrink its picture so the caption stands under it. | picture height + caption ≤ viewport, one page · host test + shots · true |
| R3 | WHILE a chapter has no group, the firmware shall lay it out as before. | the shots of every page of the default test book before/after · pixel diff · 0 |
| R4 | WHEN the owner taps a moved or shrunk picture, the firmware shall open it full screen. | log `Entering activity: BmpViewer` · present |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| markup | `<figure>` + `<figcaption>`; `div` with `break-inside: avoid` (host) | `<figure>` with no caption (nothing to carry — low) |
| fit | the caption's line overflows (move); the group taller than a page (shrink) | a caption taller than a page (the floor 1/4 — CSS allows the break; low) |
| caption length | 1–2 lines (shots), several lines (host) | > 5 lines when moving (the carry ring holds 6 elements: the move falls back — low) |
| orientation | landscape 180° (the card's), portrait (shots) | — |
| books | the generated test books | the owner's books — Ф3 re-typesets them; Ф1 alone changes nothing on them (said in every report) |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| C1 smoke | host `ChapterFigureKeepTest.FigureMovesWithItsCaption`: picture fits, caption line not → both on page 1 | boundary | [TESTED: 2026-11-17 · pass — run 2/6 · testcases/reports/2026-11-17_epic07_p1.md] |
| C2 | host `BreakInsideAvoidBlockMovesWithItsCaption`: the same by CSS on a `div` | equivalence | [TESTED: 2026-11-17 · pass — run 2/6 · testcases/reports/2026-11-17_epic07_p1.md] |
| C3 | host `TallFigurePictureShrinksForItsCaption`: a page-tall picture + several caption lines → one page, picture shrunk | boundary | [TESTED: 2026-11-17 · pass — run 2/6 (strengthened: picture bottom ≤ caption top, last line inside) · testcases/reports/2026-11-17_epic07_p1.md] |
| C4 | host `PictureOutsideAGroupKeepsTheOldLayout`: no group → the old break | regression | [TESTED: 2026-11-17 · pass — run 2 · testcases/reports/2026-11-17_epic07_p1.md] |
| C5 | simulator, `--figure` book, landscape: picture 2 (tall) with «Рис. 2…» under it on ONE page (before: picture page 4, caption opens page 5) | use case | [TESTED: 2026-11-17 · pass — `fig_figure_after/shots/p4.webp` · testcases/reports/2026-11-17_epic07_p1.md] |
| C6 | simulator, default book (no `<figure>`): all 8 pages pixel-equal to the pre-phase shots | regression (golden) | [TESTED: 2026-11-17 · pass — `tools/shot_diff.py` TOTAL 0 (8 pages) · testcases/reports/2026-11-17_epic07_p1.md] |
| C7 | simulator, `--figure` book, portrait | equivalence | [TESTED: 2026-11-17 · pass — `fig_figure_portrait/shots/p3.webp` · testcases/reports/2026-11-17_epic07_p1.md] |
| C8 | simulator: tap on the shrunk picture → `BmpViewer` | use case | [TESTED: 2026-11-17 · pass — `fig_figure_tap`: BmpViewer · testcases/reports/2026-11-17_epic07_p1.md] |

## 5. Control cases

| # | Control → expected: the behaviour is absent | Status + evidence |
|---|---|---|
| K1 | C1–C3 on the code before the change → red | pass — 3 red before the parser change (2026-11-17, `.tmp/parser_test_run.log` of that run; C4 green) |
| K2 | C5 on the old binary → the caption opens page 5 alone | pass — `qa_runs/fig_figure_before/shots/p4.webp` (picture) + `p5.webp` («Рис. 2…» first line) |
