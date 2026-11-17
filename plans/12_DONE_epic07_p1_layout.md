# Plan 12 — epic 07, phase 1: a picture and its caption stay on one page

> **Created:** 2026-11-17 · **Parent:** `plans/07_EPIC_figure_caption.md` → «Ф1 — раскладка» (criteria 1, 2, 5, 6) ·
> **Status:** ✅ DONE 2026-11-17 11:16 +03:00 on the simulator (planned 10:50; judge FIX FIRST 11:06, fixed; report
> `testcases/reports/2026-11-17_epic07_p1.md`); the reader check comes with the debug2 image · **Outbound:** — (the HTML5-markup half is a CrossPoint PR candidate later)

## Goal vector (Achieve)

The owner never sees a picture on one page and its caption on the next (`[OWNER] 2026-11-13 10:38 · «всегда нужно держать
подпись рядом с картинкой»`, repeated 2026-11-17 10:40: «подпись ВСЕГДА должна быть рядом с картинкой, ни в коем случае
не должна открываться на отдельную страницу»). The firmware keeps a `<figure>` — and any block with `break-inside: avoid`
or `page-break-inside: avoid` — on one page: the group moves to the next page when it does not fit the rest of this one,
and the picture shrinks when the group does not fit an empty page (`[OWNER] 2026-11-13 10:39 · «возможно это потребует
уменьшения размера миниатюры картинки - но это и не важно»`).

Anchor (meta-plan, Ф1): «`<figure>` с картинкой и `<figcaption>` раскладывается на одну страницу. Блок с картинкой и
свойством `page-break-inside: avoid` или `break-inside: avoid` держится так же. Если пара не помещается в остаток страницы,
она переходит на следующую; если не помещается на пустую страницу, картинка уменьшается, пока подпись не встанет под ней.»

## Acceptance criteria (phase) — the meta-plan's 1, 2, 5, 6

1. **The pair moves together** (meta 1). WHEN a `<figure>`'s picture fits the rest of a page and its caption's first line
   does not, the firmware shall start the next page with the picture and the caption. Check: host test on the page list
   (the picture and the caption lines on one page index); simulator shots of the two pages (`make_image_test_epub.py --figure`).
2. **The picture shrinks** (meta 2). WHEN a `<figure>`'s picture with its caption is taller than an empty page, the
   firmware shall scale the picture down (aspect kept) so the caption stands under it on that page. Check: host test
   (the image element's height + the caption lines ≤ the viewport, one page); shots in portrait and landscape.
3. **Old books unchanged** (meta 5). WHEN a chapter has no `<figure>` and no `break-inside: avoid`, the pages shall be the
   same as before the phase. Check: a host golden — the page list of the existing parser fixtures before/after equal;
   simulator shots of the default `image_test.epub` chapter equal to the pre-phase shots pixel for pixel.
4. **Tap on the picture** (meta 6). The moved/shrunk picture opens full screen on a tap (idea 02). Check:
   `Entering activity: BmpViewer`.

## The code today (read 2026-11-17)

- `ChapterHtmlSlimParser.cpp:56` — `figure` is a plain block tag; `figcaption` is not in `BLOCK_TAGS` (laid out as inline
  text of the enclosing block).
- `:1875-1971` — `<img>` handling: flushes the pending text block, breaks the page only when the picture does not fit the
  rest (`:1902-1913`; a heading introducing the picture is carried along — `keepWithNextCarry`), places a `PageImage`,
  resets `keepWithNextLines`. The picture is never scaled down for what follows it.
- `:3092-3124` `linesToCarry` / `keepWithNextCarry` / `canCarry` and `:3128-` `breakPageCarryingLines` — the carry
  mechanism moves the page's trailing TEXT LINES (`TAG_PageLine` only) with their visible offsets
  (`recentLineOffsets`), anchors and links to the next page. Headings use it (`BlockStyle::keepWithNext`).
- CSS: `CssStyle` knows `pageBreakBefore` / `pageBreakAfter` only (`CssStyle.h:111`, serialized in `CssParser.cpp:453`);
  `break-inside` / `page-break-inside` are not parsed.
- `ImageBlock` decodes at render time to its `width` × `height` (`ImageBlock.cpp:318-`), so a smaller size set at layout
  is enough to shrink a picture.
- `Section.cpp` `SECTION_FILE_VERSION = 75` — the chapter layout cache; bumped with any layout change (meta risk 1).

## Design

`FORK: how the group is held <A: reserve caption room when the picture is placed (break before / shrink the picture for N
caption lines) | B: carry the whole group (picture + caption lines so far) to the next page when a line of the group
overflows, shrinking the picture when the group does not fit an empty page | A+B> · price of error: a layout regression
in every book (pages shift, offsets/anchors break, progress positions move) · consulted: this parser's own carry mechanism
for headings (prior art here, KISS — the built-in path), CSS Fragmentation L3 §4.4 and KOReader's handling of
break-inside (research 2026-11-13_idea03_caption_standards.md §2.5)` → **B**, with A's single-line reserve only as the
cheap first guard at placement if B's tests show a gap. B is exact for captions of any length; A alone breaks on a
caption longer than its reserve.

1. **The group.** A "keep-together group" opens at a `<figure>` start tag or at a block whose CSS has
   `break-inside: avoid` / `page-break-inside: avoid`, and closes at its end tag (nesting: the outermost wins).
   `figcaption` joins `BLOCK_TAGS` so the caption is its own block (centring and the indent are Ф2).
2. **Mark the picture.** When a `PageImage` is placed inside an open group, remember the group's first element on the
   current page (its index and its `yPos`) and push the picture into the carry bookkeeping (a recent-entry with its
   visible offset and an empty anchor range) so the carry can move it.
3. **Carry the group.** Where a line of the group would overflow the page (the line-placement break path), the carry
   count becomes "every element from the group's first one" when that is not the whole page; `canCarry` accepts a
   `PageImage` inside the group's tail.
4. **Shrink.** After the carry, if the group (picture + caption lines + the overflowing line) is taller than the viewport,
   the picture is scaled down by the overflow (aspect kept, a floor of 1/4 of the viewport — meta risk 2: a caption taller
   than a page then breaks as CSS allows), and the caption lines below it move up by the same amount.
5. **CSS.** `break-inside` and `page-break-inside: avoid` parsed into one `CssStyle` bit (both names, as KOReader and KDP);
   the CSS cache serialization gets the bit and its version bump.
6. **Cache.** `SECTION_FILE_VERSION` 75 → 76.

## Steps

- [x] P1.1 Host tests FIRST (red on today's code): (a) a figure whose caption line overflows → picture + caption on page
      n+1; (b) a figure taller than the viewport with a two-line caption → one page, image height + caption ≤ viewport;
      (c) `div` with `break-inside: avoid` behaves as (a); (d) a chapter with no group: the page list equals today's
      (golden captured before the change). Anchor: «Если пара не помещается в остаток страницы, она переходит на следующую».
- [x] P1.2 CSS bit + serialization + version.
- [x] P1.3 Parser: the group (open/close), `figcaption` as a block, the picture's mark.
- [x] P1.4 Parser: the carry of the group (canCarry/breakPageCarryingLines over a `PageImage`).
- [x] P1.5 Parser: the shrink. Anchor: «если не помещается на пустую страницу, картинка уменьшается».
- [x] P1.6 `SECTION_FILE_VERSION` bump.
- [x] P1.7 The judge BEFORE the build; fix findings.
- [x] P1.8 Host suite (no new failures); simulator: the `--figure` test book (portrait + landscape 180°), the default test
      book (pixel-equal to the pre-phase shots), a tap on a moved picture; case set `testcases/TC_epic07_p1_layout.md` +
      run report.
- [x] P1.9 Commit; the internal map (parser lines); tick Ф1; write the Ф2 plan.

## Risks

1. **Offsets and anchors** — the carry moves visible-text offsets and anchor page numbers; a picture has an offset but no
   anchors. Guarded by test (a) reading the page's visible offset and by the existing carry tests.
2. **The owner's books have no groups** — Ф1 changes nothing on them until Ф3 re-typesets them; said in every report, so a
   pass of Ф1 is never read as «the owner's books are fixed».
3. **A picture inside a group with no caption** — the group is the picture alone; nothing to carry; no change.
4. **Stop/abandon paths** (`stopRequested`, layout OOM) inside the carry — the existing early returns kept.

## Decisions made without the owner

- `[AI]` Mechanism B (the FORK line above).
- `[AI]` The judge's fixes: a heading right before a figure belongs to the group (`groupStartIndex`); the picture's
  anchors (a `<figure id>`) ride in its carry-ring entry; open boxes shift with the shrink; no shrink when more than
  `MAX_CARRIED_LINES - 1` lines follow the picture (a long wrapper never fits).
- `[AI]` Known and left: a framed `<figure>` carried to the next page leaves an empty frame slice on the old page (the
  judge's minor; the Ф3 tool writes no frames); a caption longer than 5 lines falls back to the old break (the ring).
- `[AI]` `figcaption` outside a `<figure>` (invalid HTML) now lays out as a block — accepted by design item 1.
- `[AI]` WebP shots compared with `tools/shot_diff.py` (threshold 32, status bar cut): WebP q90 noise is up to 11 levels.
- `[AI]` Shrink floor 1/4 of the viewport: below it a picture is unreadable on the page; the full-screen tap (idea 02)
  remains. To revisit if the owner's books show captions that hit it.

## ✅ STATUS: DONE (2026-11-17 11:16 +03:00)

Ф1 works on the simulator: a `<figure>` (or a `break-inside: avoid` block) keeps its picture and caption on one page,
the picture shrinks when needed, books with no group lay out as before (all 8 pages of the default test book equal).
Not verified on the readers. P1.9 (commit, map, the Ф2 plan) — done with this status. Next: plan 13, Ф2.
