# Plan 14 — epic 07, phase 3: a PC tool re-typesets a book's «Рис. N…» captions into the standard figure markup

> **Created:** 2026-11-17 · **Parent:** `plans/07_EPIC_figure_caption.md` → «Ф3 — инструмент перевёрстки» (criterion 4) ·
> **Status:** 🔧 planned 2026-11-17 14:45 +03:00, started in the day loop while Ф2 P2.4 (the caption font) waits for the owner's
> choice (homework 08); P3.1–P3.5 done 2026-11-17 15:08 +03:00 on the test book (report `testcases/reports/2026-11-17_epic07_p3.md`, the
> judge VERIFIED WITH CAVEATS, its majors fixed); open: P3.6 the owner's two books — the reader on the wire · **Outbound:** —

## Goal vector (Achieve)

The owner's books mark a caption as a plain paragraph right after the picture, so the firmware cannot tell it is a
caption: `<div class="image"><img class="z1" …/></div><p class="p1"><em>Рис. 2. …</em></p>` (Hofstadter,
`OPS/ch1-6.xhtml:12-13`, `ideas/03` recon). The firmware keeps a `<figure>` (and any block with `break-inside: avoid`)
on one page since Ф1 and gives a `<figcaption>` no indent, centred, since Ф2 (`90406599`). This tool rewrites a copy of
the book so each such pair becomes the standard markup the firmware already honours; the caption text stays the
author's (`[OWNER]` interview #005 → A, 2026-11-17 10:40).

Anchor (meta-plan, Ф3): «Скрипт в `tools/`: картинка и абзац «Рис. N…» сразу после неё → `<figure>` с `<figcaption>` и
CSS `break-inside: avoid` с `page-break-inside: avoid`, как у Standard Ebooks. Скрипт проверяет версию EPUB книги. Текст
подписи — по ответу Николая на интервью № 005.» Gate: «критерий 4 на книгах Хофштадтера и Тегмарка; оригинал книги не
меняется, результат пишется рядом».

## Acceptance criteria (phase)

1. **Pairs become figures.** WHEN the tool runs on the default test book (`make_image_test_epub.py`, 3 pictures, each
   followed by `<p class="p1"><em>Рис. N. …</em></p>`), the output shall hold 3 `<figure>`, 3 `<figcaption>` and 0
   «Рис…» paragraphs after a picture. Check: `tools/caption_census.py <dir with the output>` prints `3 · 3 · 0`.
2. **The caption text is unchanged.** The inner markup of every caption (`<em>Рис. 2. …</em>`) is byte-identical
   before and after. Check: the tool's own `--selftest` and a diff of the caption inner HTML in the run report.
3. **The original is untouched; the result lies beside it.** Check: SHA-256 of the input before = after; the output
   path is printed.
4. **Only real pairs.** A picture followed by body text — also text that only begins with the letters «Рис»/«Fig»
   («Риск был велик…») — and a «Рис. N…» paragraph that does not follow a picture stay as they are: the label is
   «Рис.» / «Рисунок» / «Fig.» / «Figure» and a number. Check: `--selftest` cases.
5. **A second run changes nothing** (idempotent). Check: running the tool on its own output reports 0 pairs.
6. **The book still opens and lays out as the figure book does.** On the simulator the re-typeset test book shows
   picture 2 and its caption on one page, the caption centred under the picture with no first-line indent
   (meta criteria 1 and 3). Check: shots + `Entering activity: EpubReader`, 0 errors in the log.
7. **The owner's two books** (meta criterion 4): Hofstadter → 148 `<figure>`, 148 `<figcaption>`, 0 plain captions;
   Tegmark → 98 / 98 / 0. Check: `caption_census.py` on the outputs in `.tmp/` (third-party books never enter the
   repo) AND the tool's `--list` read caption by caption — the census counts any «Рис…» start, so equal counts can hide
   a different set (the judge, 2026-11-17). Needs the reader on the wire (the books live only on its card,
   `G:\Книги`); until then — `blocked`.

## Design

- **Where the pair is found.** Tokenize each XHTML/HTML document of the zip into tags and text. A caption candidate is
  a `<p>` whose first text (after inline tags such as `<em>`, `<strong>`, `<span>`) starts with `Рис.` / `Рисунок` /
  `Fig.` / `Figure` (or capitals) and then a number (the census counts any `Рис` start; the judge's finding 1). Its previous sibling element (found by a backward scan with a depth counter) is
  the picture block when that sibling contains an `<img>` or an SVG `<image>` and no text; a bare `<img/>` sibling counts
  too. Nothing else is touched.
- **What is written (EPUB 3).** `<figure class="kccp-figure">` + the picture block as it was + the caption paragraph
  renamed `<p …>` → `<figcaption …>` (inner markup kept byte for byte; `id`, `lang` and the other attributes kept;
  `class` and `style` dropped) + `</figure>`. The picture block is kept whole, so the book's own picture styling
  (`.image`) stays. Why `class` goes: the caption paragraph carries the BODY paragraph's class (the test book and
  Hofstadter: `p1` = `text-align: justify; text-indent: 1.5em`), and on a `<figcaption>` the book's alignment wins over
  the firmware's centring (plan 13) — seen on the simulator 2026-11-17 14:55 +03:00: `qa_runs/p3_retype_keepclass/shots/p4.webp`, the caption
  justified, its last line at the left edge.
  `FORK: options <keep the paragraph's class | drop class + style, keep id/lang | keep class + an overriding CSS rule> ·
  price of error <the owner's captions justified or left instead of centred; reversible — the original book is untouched
  and the tool re-runs> · consulted <Standard Ebooks Manual 1.9.1 §7.8.5.2: figcaption styled by its element selector,
  no class (researches/2026-11-13_idea03_caption_standards.md §3); the simulator run above>` → drop class + style.
- **CSS.** One rule appended once to the stylesheet each changed document links (the first `<link rel="stylesheet">`):
  `figure.kccp-figure { break-inside: avoid; page-break-inside: avoid; }`. A changed document with no linked stylesheet
  gets its own `kccp-figure.css`, a manifest item and a `<link>` (fallback, not expected in the owner's books).
- **EPUB version.** Read `<package version>` from the OPF and print it. EPUB 3 → the form above. EPUB 2 (XHTML 1.1 has
  no `<figure>`) → the tool stops and prints `EPUB 2: not re-typeset` until the owner's two books show their version
  (risk 1); the EPUB 2 form is written only if one of them needs it.
- **The zip.** Entries are copied in the input's order with their compression (a valid EPUB has `mimetype` first and
  stored, and keeps it).
- **Output.** `<name>.figure.epub` beside the input (or a path given as the second argument); a summary line per book:
  version, documents changed, pairs found; `--list` prints every wrapped caption with its document.

## Steps

- [x] P3.1 Case set `testcases/TC_epic07_p3_retypeset.md` (criteria 1–7 + the control: the test book's own `--figure`
      twin is NOT changed — 0 pairs). Anchor: «Скрипт в `tools/`: картинка и абзац «Рис. N…» сразу после неё».
- [x] P3.2 `tools/figure_retypeset.py` with `--selftest` (synthetic documents: a pair, `<img>` bare, SVG `<image>`,
      a picture + body text, a lone «Рис…», a figure already in place, nested inline tags in the caption); the self-test
      proven red on a broken matcher. Anchor: «Скрипт проверяет версию EPUB книги».
- [x] P3.3 Runs on the test books: census, idempotence, SHA-256 of the input; simulator shots of the re-typeset book.
- [x] P3.4 The judge (fresh agent, the diff + the meta-plan criteria); fix findings.
- [x] P3.5 Commit; rows in `PROJECT_STRUCTURE_EXTERNAL_MAP.md` and `HOUSE_RULES.md` tools; run report.
- [ ] P3.6 The owner's books — when the reader is on the wire: copy the two books to `.tmp/`, read their EPUB version,
      run with `--list`, census (criterion 7), read every listed caption; delete the copies after. Then the Ф4 plan
      (image + books + homework).

## Risks

1. **EPUB 2 books.** If Hofstadter or Tegmark is EPUB 2, `<figure>` is not valid XHTML 1.1. The meta-plan's `[AI]`
   decision says: keep EPUB 2, write a `<div>` with the property. A `<p>` caption in that `<div>` would still get the
   reader's paragraph indent (Ф2 suppresses it for `<figcaption>` only, `plan 13` design) — the owner's word «НЕ НУЖНА
   КРАСНАЯ СТРОКА». So the EPUB 2 form is a fork decided when the version is known: `FORK:` line then.
   **Known 2026-11-17 ≈ 21:05 +03:00:** the owner's GEB is EPUB 2.0 (`<package version="2.0">`; the tool: «EPUB 2: not
   re-typeset»). Recon in the firmware: `ParsedText::resolveFirstLineIndent` gives NO first-line indent when the block's
   alignment is not natural — a caption `<p>` with CSS `text-align: center` is centred and unindented with no firmware
   change. `FORK: options <A EPUB 2 → <div class="kccp-figure"> (break-inside: avoid) + <p class="kccp-caption">
   (text-align: center) | B <figure> inside EPUB 2 (not valid XHTML 1.1) | C convert the book to EPUB 3> · price of error
   <an invalid book in other readers (B); a heavy conversion (C); a caption without Ф2's look (A, refuted by the recon)>
   · consulted <the meta-plan's [AI] (a div with the property), the firmware's indent rule above, the owner's
   «НЕ НУЖНА КРАСНАЯ СТРОКА»>` → A, to build after debug5 (bugs 12, 13 first).
2. **The reader's layout cache is keyed by the book's path** (`lib/Epub/Epub.cpp:29`, `epub_<hash of the path>`), and a
   cache found on the card is loaded without comparing the file (`Epub.cpp:478`). A re-typeset book copied over the old
   one under the same name would show the OLD layout. Ф4's homework says: copy under the new name, delete the old file
   (or clear the book's cache). The tool's default output name already differs (`.figure.epub`).
3. **Unknown markup in Tegmark's book** — the census counted 98 pairs by its regex, the tool's matcher is stricter
   (siblings). A count below 98 is a finding to read, never a pass.
4. **Regex-free but hand-made tokenizing.** XHTML comments, CDATA and `<script>` are copied as text tokens; the
   self-test carries a comment and a CDATA block.

## Decisions made without the owner

- `[AI]` Ф3 starts before Ф2 closes: the meta-plan puts Ф3 after Ф2 so that the tool writes markup the firmware already
  knows; the firmware knows `<figure>`/`<figcaption>` since `90406599`. The open Ф2 step P2.4 sets only the caption's
  default font, which the tool does not write (the owner's books carry their own `<em>`).
- `[AI]` The picture block is kept whole inside `<figure>` (the book's picture styling stays); the caption `<p>` becomes
  `<figcaption>` without its `class` and `style` (the `FORK:` line in Design).
- `[AI]` The class name `kccp-figure` marks what the tool wrote, so a second run and a reader of the book can tell it.
