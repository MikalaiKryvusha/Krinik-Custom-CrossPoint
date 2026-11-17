# Plan 13 — epic 07, phase 2: the caption has no first-line indent and stands centred under its picture

> **Created:** 2026-11-17 · **Parent:** `plans/07_EPIC_figure_caption.md` → «Ф2 — вид подписи» (criterion 3) ·
> **Status:** 🔧 the indent + centring DONE on the simulator 2026-11-17 11:51 +03:00 (firmware `90406599`, report
> `testcases/reports/2026-11-17_epic07_p2.md`; the judge FIX FIRST fixed); open: P2.4 italic × size mock-ups — the owner's
> taste · **Outbound:** —

## Goal vector (Achieve)

The owner never sees a caption indented like a paragraph: `[OWNER] 2026-11-13 11:13 · «подписи картинок - это не
параграф, они не обязаны слушаться правила отступа для красной строки параграфа»`, repeated 2026-11-17 10:40: «НЕ НУЖНА
КРАСНАЯ СТРОКА, это НЕ АБЗАЦ, чтобы ему делать отступ слева». The caption stands centred under its picture (`[AI]` from
the standards he ordered read: ГОСТ 7.32-2017 6.5.7, БГУИР СТП 01–2024 2.5.5 — the meta-plan's decisions).

Anchor (meta-plan, Ф2): «`<figcaption>` по центру под картинкой …, без отступа красной строки (слово Николая 2026-11-13
11:13 +03:00). Курсив и размер шрифта подписи — макеты на симуляторе, выбор Николая по домашке.»

## Acceptance criteria

1. **No first-line indent, whatever the book's CSS and the reader's paragraph-indent setting say.** Check: host test —
   the caption's first line starts at the same x as its centred position would without an indent (the line's x offset
   = (width − line width) / 2 ± 1 px); a shot.
2. **Centred** (meta 3): the caption line's middle = the picture's middle ± 2 px (shot measure).
3. **Italic and size** — taste class: mock-ups on the test book (upright / italic × body size / one size smaller), the
   owner chooses by homework; until then the book's own style stands.

## Design (read 2026-11-17)

- `ChapterHtmlSlimParser::startElement`, the `BLOCK_TAGS` branch: for `figcaption` the block style comes from
  `BlockStyle::fromCssStyle(cssStyle, emSize, CssTextAlign::Center, viewportWidth)` (headings do the same with Center),
  then `textIndent = 0`, `textIndentDefined = true`; after `startNewTextBlock` — `currentTextBlock->suppressFirstLineIndent()`
  (the reader's `paragraphIndentSpaces` is applied by `ParsedText` itself, `ParsedText.cpp:763-765`).
- The owner's books get `<figcaption>` from the Ф3 tool; Ф2 alone changes nothing on them.

## Steps

- [x] P2.1 Host test first (red): a figcaption under a figure with the reader's paragraph indent on → no indent, centred.
- [x] P2.2 The parser change. Anchor: «без отступа красной строки».
- [x] P2.3 Judge → simulator (`--figure` book: shots), host suite, run report.
- [ ] P2.4 Mock-ups for italic × size → homework to the owner (`homeworks/`), his verdict recorded.

## Decisions made without the owner

- `[AI]` Every block born inside a caption gets no indent (`captionDepth`, `startNewTextBlock`): the judge's nested-`<p>` case.
- `[AI]` The caption's alignment is defined (as headings), so a figure's `text-align` does not pass to it.

- `[AI]` Centre by default (ГОСТ / БГУИР); a book's own `text-align` on its caption still wins — the owner's word binds
  the indent, not the alignment.
