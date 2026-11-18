# Bug 15 — a heading aligned left gets the reader's first-line indent

**Status:** 🔧 fix in work — KCCP 1.1.4, firmware branch `wip/kccp-1.1.4`, started 2026-11-18 08:53 +03:00
**Severity:** S2 · **Version/build:** KCCP 1.1.3 · **When/context:** the owner reading GEB, screenshots 2026-11-17
21:34–21:35, filed 2026-11-17 21:39 · **Fixing:** this session, with bug 14

## The owner's words (verbatim, chat 2026-11-17 21:39 +03:00; committed as is in `f5740e0`)

> 2) у заголовков ЗАЧЕМ-то  мне не понятно зачем есть красная строка - НИКТО ТАК В ТИПОГРАФИИ НЕ ДЕЛАЕТ. Заголовки или от
> левого края рисуют, или от левого с отступом, но тогла и все последующие строки ниже при длинном заголовке на насколько
> строк - получают такой же отступ. или заголовки ЦЕНТРИРУЮТ, и все строки ниже ЦЕНТРИРУЮТ, но не пишут как тест, с
> красной стройкой!!!!
>
> это проблема нашей книги, она так свёрстана, или всё же код читалки?

Answered in chat 2026-11-18 08:47 +03:00: the firmware's — the book says `text-indent: 0px` for the title's paragraph.

## Symptom

`ch10_p1.webp` (`.tmp/bug14/shots/`): «ГЛАВА I: Головоломка» starts further right than its second line «MU».

## Root cause

`lib/Epub/Epub/ParsedText.cpp:759` `resolveFirstLineIndent`: the reader's paragraph indent (`paragraphIndentSpaces`, the
setting) goes to the first line of EVERY block whose alignment is natural (justify, or left in LTR); a CSS `text-indent`
counts only when negative. GEB's chapter title `<div class="title3"><p class="p">` is `text-align: left` (natural), so it
gets the indent; its `.p { text-indent: 0px }` is ignored. An `h1`–`h6` the book aligns left gets it the same way.

`INTENT: code indents the first line of any left/justified block by the reader's setting; the owner expects a heading
with no first-line indent (left, left with an inset for every line, or centred); the spec — the book's CSS gives the
title text-indent: 0.` The firmware's design (the reader's indent setting overrides the book's indents,
`BlockStyle.h:145`) stays for body text; headings leave it.

## Fix plan

`FORK: options <A no reader indent on a heading: h1–h6 and every block kept with the next (keepWithNext — the CSS break-after:
avoid of bug 14) | B every block with a CSS text-indent: 0 | C the book's text-indent wins everywhere> · price of error
<B, C change body text in books whose CSS zeroes indents — the owner's own indent setting would stop working there;
A misses a heading the book marks with neither a heading tag nor break-after: avoid> · consulted <the owner's words above
(the scope is headings, «НИКТО ТАК В ТИПОГРАФИИ НЕ ДЕЛАЕТ»); the firmware's design (the setting overrides body text);
GEB's CSS (every heading class carries page-break-after: avoid)>` → A.

1. `ParsedText` — a block with `keepWithNext` gets no first-line indent (`resolveFirstLineIndent` returns 0; a negative
   CSS hanging indent stays as it is).
2. Host test: a left-aligned `<div style="page-break-after: avoid; text-align: left"><p>` heading's first line starts at
   the left inset, the same as its second line; a plain left-aligned `<p>` keeps the reader's indent (control).
3. Simulator on the owner's settings and his GEB (`HOUSE_RULES.md` П4): «ГЛАВА I: Головоломка MU» — both lines start at the
   same x.

## Decisions made without the owner

(filled at closing)

## Links

- Bug 14 (the same headings left alone at a page bottom) — the keep-with-next flag both fixes read.
- Epic 07 Ф2 — a caption has no indent by the same rule of «not a paragraph» (`captionDepth`).
