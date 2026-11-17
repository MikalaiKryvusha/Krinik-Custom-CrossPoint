# Bug 11 — a note's backlink opens a new jump instead of closing the one it returns from

**Status:** 🔧 fix pending verification · **Severity:** S2
**Version/build:** the owner's reader KCCP 1.1.1-debug9; the same code on `wip/kccp-1.1.3-debug2` · **When/context:**
the owner in chat 2026-11-17 20:01 +03:00, while bug 09 was being fixed · **Fixing:** this session (KCCP 1.1.3-debug4)

## The owner's words (chat, verbatim)

> и странно, что я по ссылке перехожу - покпадаю на страницу с текстом ссылки. Если там тоже перейду по ссылке - то
> попадаю назад в книгу, и если начну делать свайпы назад - то я иду по полному стеку переходов.
>
> ТОЧНО ЛИ НУЖНО ДЕЛАТЬ ССЫЛКИ В ПРИМЕЧАНИЯХ ПОЛНОЦЕННЫМИ??? ЧТОБЫ ОНИ В СТЕК ПИСАЛИСЬ?

## Goal vector (Avoid) and acceptance

Returning from a note never adds a jump. Done when, on the owner's GEB:
- Situation. The reader shows the chapter page with the reference «[4]».
- Action. The user taps «[4]», then taps «[4]» at the start of the note.
- Result. The chapter page with «[4]» is on the screen again, and a Back swipe no longer opens the note or the chapter
  again (with no jump on the stack the X4 Pro's edge swipe is not a Back — `ReaderUtils::handleBackNavigation` returns
  false on `wasBackGesture()` — so the reader stays in the book).
- Check. The simulator log of that run shows `Saved position [1]` then `Link back to spine 8 closes jump [1]` and no
  `Restoring position` after the Back swipe.

Correction 2026-11-17 20:17 +03:00: the first draft of this Result (and the chat to the owner at ≈ 20:03) said «a Back
swipe leaves the book»; the judge read `ReaderUtils.h:277` — at depth 0 the edge swipe is not a Back on the X4 Pro.

## Root cause

`EpubReaderActivity::navigateToHref(href, true)` pushes the current place onto `savedPositions` (depth ≤ 3,
`links.bin` across sleep) for EVERY followed link; the note's backlink `<a href="ch1-7.xhtml#fnref35">[4]</a>` is
followed like a forward link, so it pushes the notes page, and Back (the left-edge swipe,
`MappedInputManager::wasBackGesture`) then walks note → chapter → note … Upstream PR #3799 (open) fixes the same class
(«Following an EPUB backlink such as “Return” leaves the original footnote return position active»).

## Fix

`[AI]` reading of the owner's question: a link that LEAVES the current chapter for the chapter the last jump came
from closes that jump (the stack shrinks); any other link pushes as before. In `navigateToHref`: when `savePosition`,
the target spine ≠ the current spine and the top saved position's spine is the target's → `footnoteDepth--` instead of
a push, and the reader lands on the saved page when the backlink's anchor is not in the chapter's map. Firmware,
uncommitted at writing.

The judge's round 1 (2026-11-17 20:16 +03:00, FIX FIRST): matching on the spine alone popped forward links inside one
chapter (a single-file book, same-file notes, «see note 3») and left the reader with no way back → the
`targetSpineIndex != currentSpineIndex` condition; a popped jump whose anchor is missing landed on page 0 → the saved
page. Follow-ups, not done: same-file backlinks (`#fnref1`) still push, as before the fix; a stale top entry (the stack
survives TOC navigation and sleep) can turn a cross-reference into a return.

## Verification

- [x] Independent judge over the diff — round 1 FIX FIRST, fixed (above); round 2 OK WITH NOTES: a link with no
      fragment would pop and land on the saved page → `!anchor.empty()` added. Committed firmware `87b8ead1`.
- [x] Simulator, the owner's GEB (report `testcases/reports/2026-11-17_bug09_bug11_debug4.md`): `Saved position [1]` →
      `Link back to spine 8 closes jump [1]` → page 15/68 with «[4]»; the Back swipe after it: no `Restoring
      position`, the page turned back to 14/68.
- [ ] The owner's check on the reader (image 1.1.3-debug4).

## Decisions made without the owner

- `[AI]` The rule matches by chapter (spine), not by the exact page: a backlink of another note into the same chapter
  also closes the jump and lands on that note's reference. Simpler than upstream #3799's page matching.
- `[AI]` Same-chapter notes (notes at the end of the chapter) follow the same rule.

## Links

`bugs/09_ssylka.md` · upstream #3799
