# Test cases — epic 07 Ф2: the caption has no first-line indent and stands centred

**Created:** 2026-11-17 · **Under test:** `figcaption` block style in `ChapterHtmlSlimParser::startElement` ·
**Version/build:** `wip/kccp-1.1.3-debug2`, host + simulator `simulator_x4_pro_win`
**Test basis:** `plans/13_epic07_p2_caption_look.md`; the owner 2026-11-13 11:13 «подписи картинок - это не параграф, они
не обязаны слушаться правила отступа для красной строки параграфа», 2026-11-17 10:40 «НЕ НУЖНА КРАСНАЯ СТРОКА, это НЕ
АБЗАЦ, чтобы ему делать отступ слева»; centring — `[AI]` from ГОСТ 7.32-2017 6.5.7 / БГУИР СТП 01–2024 2.5.5.

## 1. Goal vector

Avoid: a caption indented like a paragraph. Achieve: the caption centred under its picture.

## 2. Requirements under test

| # | Requirement (EARS sentence) | Fit criterion (Scale · Meter · Target) |
|---|---|---|
| R1 | WHILE the reader's paragraph indent is on, a figcaption's first line shall have no indent. | first word x of a one-line caption · host test · = (480 − 84) / 2 ± 1 |
| R2 | WHEN the book's CSS gives the figcaption a text-indent, the firmware shall ignore it. | the same · host test (`text-indent: 2em`) · same target |
| R3 | A figcaption with no text-align of its own shall be centred. | line alignment · host test · Center; shot · the caption line's middle = the picture's middle ± 2 px |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| indent source | the reader's setting (5 on the card, 3 in the host test); the book's CSS | a negative (hanging) CSS indent — zeroed by the same line (judge to confirm) |
| caption markup | plain text; text with `<br/>` (breakTextLine suppresses the indent itself, read 2026-11-17) | a nested `<p>` inside `<figcaption>`: its own block resets the suppression — the Ф3 tool writes no nested `<p>` (low) |
| alignment | no text-align (centred) | a book's own text-align on figcaption — wins by design |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| C1 smoke | host `CaptionHasNoFirstLineIndentAndIsCentred`: reader indent 3 + CSS 2em → caption x = 198, Center; the control paragraph indented | decision table | see the run report |
| C2 | simulator, `--figure` book (card indent 5), landscape: captions 1 and 2 centred, no indent (shots) | use case | see the run report |
| C3 | default book (no figcaption): pages equal to the Ф1 after-shots (`tools/shot_diff.py`) | regression | see the run report |

## 5. Control cases

| # | Control → expected: the behaviour is absent | Status + evidence |
|---|---|---|
| K1 | C1 on the code before the change → red | pass — red 2026-11-17 (alignment 0 ≠ 2, x ≠ 198); the control paragraph x > 0 |
