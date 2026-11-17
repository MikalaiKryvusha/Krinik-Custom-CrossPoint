# Bug 09 — a footnote link opens the first page of the notes chapter: the note's target is a `<span id>`

**Status:** 🔧 fix pending verification · **Severity:** S2
**Version/build:** the owner's reader KCCP 1.1.1-debug9 (`wip/krinik-debug9` `35dc070c`); the same code on
`wip/kccp-1.1.3-debug2` and upstream `develop` (`8df647a7`, 2026-11-16) · **When/context:** filed by the owner
2026-11-17 (before 19:45 +03:00), the book «Гёдель, Эшер, Бах» on his reader · **Fixing:** this session (KCCP 1.1.3-debug4)

## The owner's report (verbatim, committed first in `6cc642b`)

> всё ещё воспроизводится баг с нафигацией по ссылкам. На прошивке, которая стоит на моей читалке, в книге "Gödel,
> Escher, Bach" по ссылке [4] открыло страницу со ссылками 1, 2, 3, а ссылка 4 была НА СЛЕДУЮЩЕЙ странице.
>
> Дополнение 1: там же, по ссылке 5 тоже не на ту страницу перешло. По сслыке 6 тоже не перешло на нужную страницу, а
> переходит на первую страницу Примечаний!!!
>
> Дополнение 2: в это йже книге много предложений не закрыты точкой! Это проблема наших инструментов по проверке книг на
> адекватность!

«Дополнение 2» is a different defect (the book's text, not the firmware): `bugs/10_geb_notes_lost_punctuation.md`.

## Goal vector (Avoid) and acceptance

A footnote link never opens the start of the notes chapter instead of its note. Done when:
- WHEN the reader follows `ch3.xhtml#id81` in the owner's GEB, the opened page shows note «[4]» — Check: the simulator
  run of the owner's book (`.tmp/bug09/geb.epub`, never committed), links [4] [5] [6], the shot of each landing page.
- The #2303 heap guard holds: ids on text spans (Kobo KePub) are still not recorded — Check: host tests
  `ChapterAnchorPageTest.SpanAroundTextStaysUnrecorded`, `…SpanWithTextBeforeItsBlockStaysUnrecorded`.

## Symptom

Every link into the notes chapter opens its page 0. Notes [1]–[3] stand on that page, so [4] looks «one page off» and
[5], [6] land «on the first page of the notes» — one cause, three faces.

## Forensics (the owner's reader, copied read-only 2026-11-17 19:47 +03:00 to `.tmp/bug09/`)

- The notes chapter `OPS/ch3.xhtml` (spine 65) wraps each note in a span: `<span id="id81"><p class="p1"><a
  href="ch1-7.xhtml#fnref35" …>[4]</a> Charles Babbage …</p></span>`; links: `<a href="ch3.xhtml#id81" …>[4]</a>`.
- The reader's own section cache `.crosspoint/epub_1421811873/sections/65.bin` (file time 2026-11-12 14:07, cache
  version 75 = debug9) holds **0** `idNN` strings: no anchor of the notes chapter was recorded.
- No serial port: the reader on the wire is a USB mass storage device (`VID_303A&PID_1001`), so no live log.

## Root cause

`ChapterHtmlSlimParser::startElement` drops every non-TOC id on a `<span>` — `isNonNavigableInlineElement()`, upstream
PR #2303 (a heap guard against converters that put an id on every inline text span, Kobo KePub). Footnote targets on a
span wrapping the note's block are dropped with them; `getPageForAnchor` finds nothing and the reader opens page 0.
Upstream knows it: issue #3667 (open, X3/X4, 1.6 and 2.0; a user reverted #2303 and the bug went away), #3798 (closed
as its duplicate), fix PR #3799 (open, 25 files, section cache v56, not tried on hardware).

The earlier anchor fix `aeee710b` («anchor page follows its block's first line», debug9 and later) covers ids on blocks,
not on spans — hence the owner's «всё ещё».

## Fix

`FORK: options <A port upstream #3799 (25 files, cache v56, unmerged, not tried on hardware) | B a <span> that directly
opens a block keeps its id (one candidate list, the 1024 cap and the KePub filter stay) | F our book tool moves the id
onto the block> · price of error <links land on wrong pages in other books; heap exhaustion from converter spans
(#2292) if the filter loosens too far> · consulted <upstream #2303 (why the filter: inline KePub spans), #3667 + #3798
(the reported structure: span wrapping div/p), #3799 (upstream's fix in review)>` → B.

`INTENT: code drops every non-TOC <span id> · the tests and the owner's book expect a <span> that opens a note block to
be a link target · upstream #3667/#3798 (a link opens the element with the id, as Calibre and Apple Books do) agree with
the tests — the code is the side that is wrong.`

Firmware (uncommitted at the time of writing, `wip/kccp-1.1.3-debug2`): a `<span id>` waits in
`spanAnchorCandidates`; visible (non-whitespace) text clears the list; a block start (`startNewTextBlock` →
`flushBlockStartAnchors`, after the previous block is laid out) moves the candidates to the anchors waiting for the
block's first content; leftovers at `finishParse` land on the last page. `anchorCount()` counts the candidates against
`MAX_ANCHORS_PER_CHAPTER`. `SECTION_FILE_VERSION` 76 → 77 (caches built without span anchors rebuild).

Host tests (red before the fix: 3 of 5, the two KePub guards green before and after):
`ChapterAnchorPageTest.SpanWrappedNotesEachLandOnTheirFirstLine` · `…SpanWrappingATitleDivAndNoteLandsOnTheTitle` ·
`…EmptySpanMarkerBeforeAHeadingFollowsTheHeading` · `…SpanAroundTextStaysUnrecorded` ·
`…SpanWithTextBeforeItsBlockStaysUnrecorded`. Full host suite 2026-11-17 19:57 +03:00: 970 tests, 10 failed = the known
list (`sh tools/host_tests.sh`: «no new failure»).

`TWINS:` the same filter is the only place span ids are dropped (`git grep -n isNonNavigableInlineElement` → one
definition, one use); TOC span ids bypass it already.

## Verification

- [x] Independent judge over the diff (before any build) — 2026-11-17 ≈ 20:09 +03:00 OK WITH NOTES; finding 2 (span
      markers could eat the 1024 cap → span ids stop at half of it, `MAX_ANCHORS_BEFORE_SPAN_IDS_STOP`, test
      `SpanMarkersLeaveRoomForRealTargets` red on the full-cap mutant) and 6 (two tests sharpened) fixed. Committed
      firmware `df4fab1a`.
- [x] Simulator, the owner's GEB (report `testcases/reports/2026-11-17_bug09_bug11_debug4.md`): [4] → the notes page
      with note 4, [5] and [6] → page 2/18 with notes 5–8.
- [x] Simulator smoke of the debug4 commit `3e223b4d`; image `cp-2.0.0-krinik-1.1.3-debug4.bin` built 2026-11-17
      20:32 +03:00.
- [ ] On the reader: not verified (the simulator only; the agent observes the reader by its card screenshots and logs — `HOUSE_RULES.md` П2).

Follow-ups from the judge (not regressions, not done): a `<span id>` around a picture in an empty block lands one page
late (as `<img id>` does); an empty marker span INSIDE a paragraph is still dropped (record it as an inline anchor on
`</span>`); hidden text clears a candidate (the clear sits before the skip check); a span before a table is dropped
(`flushPendingAnchor` instead of `flushBlockStartAnchors` at table start).

## Decisions made without the owner

- `[AI]` Option B over porting upstream #3799 (above): smallest change covering every structure reported upstream.
- `[AI]` An empty `<span id>` marker before a block also counts (no text = a marker, never a KePub text span).
- `[AI]` The punctuation part of the report moved to its own bug 10 (one document per defect).

## Links

Upstream #2303 · #3667 · #3798 · #3799 · `bugs/10_geb_notes_lost_punctuation.md` · epic 07 (the same book, captions).
