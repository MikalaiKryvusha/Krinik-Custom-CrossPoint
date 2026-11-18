# Bug 14 — a heading the book marks `page-break-after: avoid` stays alone at the page bottom

**Status:** ✅ DONE (see the end) — KCCP 1.1.4, firmware branch `wip/kccp-1.1.4` (from the 1.1.3 release `c1c38089`), started 2026-11-18 08:53 +03:00
**Severity:** S2 · **Version/build:** KCCP 1.1.3 (`cp-2.0.0-krinik-1.1.3.bin`) · **When/context:** the owner reading GEB
on his reader, screenshots 2026-11-17 21:34–21:35, filed 2026-11-17 21:39 · **Fixing:** this session

## The owner's words (verbatim, chat 2026-11-17 21:39 +03:00; committed as is in `f5740e0`)

> наделал скриншотов, они на читалке, читалка на проводе - скачай, будем разбирать по ним баги.
>
> 1) на двух скриншотах видно "одинокий" заголовок - так быть не должно. Он ОБЯЗАТЕЛЬНО должен быть на новой странице с
> текстом. Если текст не помещается, то не должна читалка оставлять его одиноким

`[OWNER] 2026-11-18 08:46 +03:00 · chat: «ты на моих настройках читалки бы тестировал у себя в эмуляторе... на моей копии
книги.... я же там блять баги нахожу...»` → `HOUSE_RULES.md` П4: the acceptance runs on his settings and his GEB copy.

## Symptom

A section heading is the last line of a page; its text starts on the next page. The owner's screenshots (copies in
`.tmp/bug14/shots/`, never committed — third-party text): `ch10_p20.webp` «Внутри и снаружи системы», `ch10_p28.webp`
«Прыжки за пределы системы» (GEB, «ГЛАВА I: Головоломка MU», landscape 180°).

## Repro

The owner's GEB copy (`.tmp/bug09/geb.epub`, EPUB 2.0, md5 `0e91a974…`), `OPS/ch1-8.xhtml`:
`<p class="subtitle">Внутри и снаружи системы</p><p class="p1">Большинство читателей…`. Its `OPS/style.css`:

```css
.subtitle { … page-break-after: avoid; page-break-inside: avoid; text-align: center; text-indent: 0px; }
.title3   { … margin: 1em 0px 0.5em 1.563em; page-break-after: avoid; page-break-inside: avoid; text-align: left; }
```

Chapter titles are `<div class="title3"><p class="p">ГЛАВА I: Головоломка MU</p></div>` (`.p { text-indent: 0px }`).
Every heading class of the book (`title1`, `title2`, `title3`, `subtitle`) carries `page-break-after: avoid`.

## Root cause

1. `lib/Epub/Epub/css/CssParser.cpp:1069` — `page-break-after` / `break-after` go through `interpretForcedBreak()`
   (`always`, `page`, `left`, `right`, `recto`, `verso`); the value `avoid` is dropped.
2. Keep-with-next exists only for `h1`–`h6`: `ChapterHtmlSlimParser.cpp:2183` `headerBlockStyle.keepWithNext = true`.
   GEB's headings are `<p>` and `<div><p>`, so the carry ring never takes them along (`linesToCarry`, `keepWithNextLines`).

`INTENT: code keeps only h1–h6 with the next block; the owner expects a heading always on a page with its text; the spec —
CSS 2.1 §13.3.1 and CSS Fragmentation 3 §3.1: "avoid: avoid a page break after the principal box" — says the book asked
for exactly that.` The three agree once `avoid` is read; the defect is the firmware's.

## Fix plan

1. `CssStyle::breakAfterAvoid` — `avoid` / `avoid-page` of `page-break-after` / `break-after`; it shares the declared bit
   of `pageBreakAfter` (the defined-bits word is full) and the wire byte carries 0 none · 1 forced · 2 avoid;
   `CSS_CACHE_VERSION` 20 → 21.
2. A block with `breakAfterAvoid` gets `keepWithNext`, as a heading does.
3. The blocks nested inside such a block inherit `keepWithNext` (GEB `div.title3 > p`: the text lives in the inner `<p>`,
   laid out before the `</div>` is seen).
   `FORK: options <A every nested block inherits keep-with-next | B only the container's last child, set when the container
   closes | C inherit only when the container is also break-inside: avoid> · price of error <A: a big wrapper marked
   break-after: avoid makes every paragraph keep-with-next — pages end up to 6 lines early where a paragraph opens a page
   (bounded by MAX_CARRIED_LINES = 6 and canCarry); B: the inner <p> is laid out at its own </p>, before the container
   closes, so B needs a retroactive carry — more code, and the inner <p> still is not a heading for bug 15; C: misses a
   wrapper with break-after alone> · consulted <CSS Fragmentation 3 §3.1 (break-after of a box applies at its end edge,
   which its last child shares); GEB's markup (every heading wrapper has both break-after and break-inside: avoid, one
   child each)>` → A, the risk tier (b) named below. **Revised 2026-11-18 ≈ 09:10 +03:00 → C** on the judge's MAJOR (A
   makes every paragraph of a big `break-after: avoid` wrapper kept — pages up to 6 lines short, the indent lost; a
   heading + a kept epigraph over 6 lines leaves the heading alone again): a wrapper reaches inside only with
   `break-inside: avoid` too (`BlockStyle::keepContentWithNext`), which every GEB heading class has (`title`, `title1`,
   `title2`, `title3`, `subtitle` — `style.css` read). A wrapper with `break-after` alone keeps only its own direct text.
4. `SECTION_FILE_VERSION` 77 → 78: cached chapters are laid out again.
5. Host tests in `test/chapter_html_slim_parser/` (`ChapterWidowOrphanTest`): a `<p style="page-break-after: avoid">`
   and a `<div style="page-break-after: avoid"><p>` move with the next paragraph; the same `<p>` without the property
   stays (control).
6. Simulator on the owner's settings and his GEB (П4): pages 20 and 28 of chapter «ГЛАВА I» no longer end with a heading.

## Risks

- (b) A wrapper with `break-after: avoid` alone around a heading's inner `<p>` (no `break-inside`) does not keep it —
  the lonely heading stays for that markup (not in the owner's books). A spacer paragraph (`<p>&nbsp;</p>`) between a
  heading and its text resets the keep (the judge's finding 3; true for h1–h6 before this change too); GEB's headings are
  followed by their text directly. A heading before a table row or an `<hr>` is never carried (unchanged).
- (c) The cache bump re-lays every book once (first open of each chapter is slower).

## Decisions made without the owner

- `[AI]` FORK → C (the line above): a wrapper's keep reaches its inner blocks only with `break-inside: avoid` too — the
  judge refuted A. Reversible.
- `[AI]` `avoid-page` counts as `avoid` (CSS Fragmentation 3); `avoid-column` / `avoid-region` do not (no columns).
- `[AI]` The CSS and section caches are bumped (21, 78): every book is laid out again once.
- `[AI]` A spacer paragraph between a heading and its text still resets the keep (judge's finding 3) — not in GEB, left.
- PENDING settled: «GEB's every heading class carries both properties» — confirmed by reading `style.css` (5 classes).

## Links

- Bug 15 (the same headings drawn with a first-line indent) — fixed together, same branch.
- Run report `testcases/reports/2026-11-18_kccp114_headings_captions.md`.

## ✅ STATUS: DONE (2026-11-18 09:45 +03:00)

Firmware `d727eeef` (fix), `21671e33` (1.1.4-debug1), branch `wip/kccp-1.1.4`, local; image
`firmware-builds/cp-2.0.0-kccp-1.1.4-debug1.bin`.
- Hygiene: host suite 978, 10 failed = the known list; five mutants red; the judge VERIFIED WITH CAVEATS, its major fixed.
- Functional run: the owner's GEB on his settings (`HOUSE_RULES.md` П4) — page 27 (his 28) ended with «Прыжки за пределы
  системы» before, ends with text after; the heading opens page 28 with its text. Shots read.
- Not verified on the reader: it is not on the wire; the image goes to the card when it is.
- `TWINS: searched <page-break-after / break-after readers in lib/Epub> — found 0 other sites; the forced break reads the
  same property at the element's close (ChapterHtmlSlimParser.cpp:2912), unchanged.`
- `PROJECT_ARCHITECTURE_INTERNAL_MAP.md` → `ChapterHtmlSlimParser.cpp` (the carry ring).
