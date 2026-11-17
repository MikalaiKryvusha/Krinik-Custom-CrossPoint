# Test cases — epic 07 Ф3: the re-typeset tool turns «Рис. N…» paragraphs after a picture into figure + figcaption

**Created:** 2026-11-17 · **Under test:** `tools/figure_retypeset.py` · **Version/build:** the tool at its first commit;
the books opened on the simulator `simulator_x4_pro_win`, firmware `wip/kccp-1.1.3-debug2` `90406599`
**Test basis:** `plans/14_epic07_p3_retypeset_tool.md` (criteria 1–7); the meta-plan `plans/07_EPIC_figure_caption.md` →
Ф3 and criterion 4; `[OWNER]` interview #005 → A (the caption text stays the author's, 2026-11-17 10:40).

## 1. Goal vector

Achieve: the owner's books carry the standard caption markup, so the firmware keeps each picture with its caption on
one page and draws the caption centred without indent. Maintain: the caption text and everything outside the pairs.

## 2. Requirements under test

| # | Requirement (EARS sentence) | Fit criterion (Scale · Meter · Target) |
|---|---|---|
| R1 | WHEN a picture block is followed by a paragraph whose text starts with «Рис.», «Рисунок», «Fig.» or «Figure» and a number, the tool shall wrap both in `<figure class="kccp-figure">` and rename the paragraph `<figcaption>`. | pairs · `caption_census.py` on the output · default test book 3 `<figure>`, 3 `<figcaption>`, 0 plain |
| R2 | The tool shall keep the caption's inner markup byte-identical. | captions whose inner HTML differs · diff of the extracted captions · 0 |
| R3 | The tool shall leave the input file unchanged and write the result beside it. | SHA-256 of the input before vs after · `sha256sum` · equal |
| R4 | IF a picture is followed by body text, or a «Рис…» paragraph follows no picture, THEN the tool shall leave it. | wrongly wrapped · `--selftest` cases · 0 |
| R5 | WHEN the tool runs on its own output, it shall find 0 pairs and write nothing. | pairs on the second run · tool summary line · 0 |
| R6 | IF the book is EPUB 2, THEN the tool shall write nothing and exit 3. | exit code · a run of the tool on an EPUB 2.0 copy of the test book · 3, no file |
| R7 | The re-typeset book shall open on the reader and show picture 2 with its caption on one page, the caption centred, no first-line indent. | shots · simulator · picture and caption on one page; `[ERR]` lines in the log 0 |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| picture markup | `<div><img/></div>` (the owner's Hofstadter form), a bare `<img/>`, `<img>` without slash, SVG `<image>` | `<object>` / `<picture>` pictures — none in the owner's census (low) |
| caption markup | `<p><em>Рис…</em></p>`, nested `<span><strong>`, «Рисунок N –», «Figure N.» | a caption split over two paragraphs (the second stays a paragraph; risk 3 of plan 14) |
| what must stay | picture + body text, lone «Рис…», «Рис…» as a first child, text between, a figure already in place, comments/CDATA | — |
| book level | EPUB 3 with a linked stylesheet, EPUB 3 without one (own CSS), EPUB 2 (refused), a book with no pairs | non-UTF-8 documents — skipped and counted, not converted (low: the owner's books are UTF-8 by the census run) |
| the owner's books | — | Hofstadter, Tegmark: blocked, the books live only on the reader's card (T9) |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| T1 smoke | the default test book (`qa_runs/sd_book_images/image_test.epub`, a copy in `.tmp/`) → the tool → census of the output: 3 · 3 · 0; the summary line names EPUB 3.0, 1 document, 3 pairs | use case | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic07_p3.md] |
| T2 smoke | the re-typeset book on the simulator, landscape («Альбомная 180°»), 5 pages: picture 2 and «Рис. 2. …» on one page, the caption centred without indent; 0 `[ERR]` | use case | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic07_p3.md] |
| T3 | the 3 captions' inner HTML in the input = in the output | equivalence | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic07_p3.md] |
| T4 | SHA-256 of the input copy before = after | invariant | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic07_p3.md] |
| T5 | the tool on its own output → «pairs 0 · no pairs: nothing written», no file | state transition | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic07_p3.md] |
| T6 | the `--figure` test book (already standard) → 0 pairs, nothing written | equivalence | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic07_p3.md] |
| T7 | `--selftest`: 33 document checks + 8 book-level scenarios → `selftest: OK` | decision table, boundary | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic07_p3.md] |
| T8 | an EPUB 2.0 copy of the test book → exit 3, «EPUB 2: not re-typeset», no file | error guessing | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic07_p3.md] |
| T9 | Hofstadter → 148 · 148 · 0; Tegmark → 98 · 98 · 0, and `--list` read caption by caption: every wrapped paragraph is a caption, every census «Рис» left unwrapped is named (copies in `.tmp/`, deleted after) | use case | blocked — the reader is not on the wire |
| T10 | a paragraph after a picture that only begins with «Рис»/«Fig» letters («Риск был велик…», «Fighting…») stays a paragraph; «Рис.&nbsp;4», «РИС. 5», «Рисунок 6 —», «Fig. 7», «Рис.8» are captions | boundary | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic07_p3.md] |
| T11 | `--list` prints every wrapped caption with its document | use case | [TESTED: 2026-11-17 · testcases/reports/2026-11-17_epic07_p3.md] |

## 5. Control cases

| # | Control → expected: the behaviour is absent | Status + evidence |
|---|---|---|
| K1 | `--selftest` on broken matchers → red: the label always true, the picture check skipped, the old loose label, and the judge's six mutants | pass — 9 mutants red, `testcases/reports/2026-11-17_epic07_p3.md` runs 4 and 10 |
| K2 | the default book NOT re-typeset on the same firmware: picture 2 alone on page 4, «Рис. 2.» opens page 5 with an indent (`qa_runs/fig_default_after/shots/p4.webp`, `p5.webp`) | pass — read 2026-11-17 14:51 +03:00 from the Ф1 after-shots (firmware `869a5bd3` + the same parser path for plain paragraphs) |
