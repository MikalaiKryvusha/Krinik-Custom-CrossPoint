# Research 02 — CodeRabbit review comments on our five open upstream PRs

> **Created:** 2026-11-09 · **Parent:** owner, chat 2026-11-09 14:39 +03:00: «делаем дальше, чиним замечания, которые
> нам сделаны в наших ПР» · «тестируем на симуляторе на этой машине» · **Status:** inventory done 2026-11-09 14:46;
> #4328-3 analysed 14:50; no code changed yet · **Outbound:** fixes → fork `pr/*` branches; reply texts → owner's
> proofreading before posting.

Dump: `gh api repos/crosspoint-reader/crosspoint-reader/pulls/<n>/comments --paginate` filtered `user.login ~ coderabbit`
(14 inline comments, all «Minor»). Upstream PR ↔ fork branch: #4328 `pr/epub-anchor-first-line` · #4332
`pr/sleep-image-order` · #4375 `pr/screen-clean-menu` · #4376 `pr/screen-redraw-delay` · #4377 `pr/screen-calibration`.

## Inventory (state 2026-11-09 14:46)

| PR | File:line | CodeRabbit effort | State |
|---|---|---|---|
| #4328 | `ChapterHtmlSlimParser.cpp:345` | Heavy lift | addressed in 27b28a3 (CodeRabbit's mark) |
| #4328 | `ChapterHtmlSlimParser.cpp:1411` | Quick win | addressed in 27b28a3 (CodeRabbit's mark) |
| #4328 | `ChapterHtmlSlimParser.cpp:3027` | Quick win | OPEN — analysed below |
| #4332 | `SleepActivity.cpp:545` | Poor tradeoff | OPEN |
| #4375 | `lib/I18n/translations/english.yaml:669` | Low value | OPEN |
| #4376 | `BmpViewerActivity.cpp:465` | Low value | OPEN |
| #4376 | `src/main.cpp:541` | Low value | OPEN |
| #4376 | `src/main.cpp:722` | Heavy lift | OPEN |
| #4376 | `src/SettingsList.cpp:74` | Low value | OPEN |
| #4377 | `ImageBlock.cpp:47` | Low value | OPEN |
| #4377 | `ReaderUtils.h:273` | Low value | OPEN |
| #4377 | `CalibrationCard.cpp:192` | Low value | OPEN |
| #4377 | `CalibrationCardStorage.cpp:99` | Low value | OPEN |
| #4377 | `PanelCurve.cpp:62` | Low value | OPEN |

## #4328-3 — queued anchors when `finishParse()` finds no text block (HEAD 27b28a36)

- Claim: an empty `<table id=…>` at chapter end queues its id; `</table>` "resets `currentTextBlock` to null";
  `finishParse()` places anchors only inside `if (currentTextBlock)`, so the id is lost.
- INTENT: code does — `</table>` (`ChapterHtmlSlimParser.cpp:2783-2800`) calls `currentTextBlock.reset()` and then
  creates a new `ParsedText`; `finishParse()` (`:3015-3036`) runs `placeUnplacedAnchors()` and the pending id inside the
  `if`. The check expects — anchors placed with no text block. Spec — the PR body (anchors land on their text's page).
- Verdict `[AI]`: the table scenario as written does NOT reach a null block. A null block at chapter end remains
  possible in two paths: a chapter that ends inside an open table row (`:979` resets and returns; `:1591` resets on
  `<tr>`), and a failed `makeUniqueNoThrow` (OOM). In both, `unplacedAnchorIds`, `pendingAnchorId` and
  `inlineAnchorIds` are dropped.
- Proposed fix (not applied): move the anchor placement out of `if (currentTextBlock)` — with no block, place the
  queued ids on `completedPageCount - 1` (the last emitted page; 0 if none). Needs a host test (truncated table at
  chapter end with an id) — host tests wait for the native Windows toolchain (research 01).

## Next

1. Toolchain after the KAGO lock (STATUS → "Where to continue").
2. Walk the remaining 11 open comments the same way: claim → INTENT line → verdict → fix or reply draft.
3. Reply drafts to CodeRabbit go to the owner for proofreading; nothing is posted or pushed without his word.
