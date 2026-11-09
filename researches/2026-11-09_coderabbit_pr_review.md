# Research 02 — CodeRabbit review comments on our five open upstream PRs

> **Created:** 2026-11-09 · **Parent:** owner, chat 2026-11-09 14:39 +03:00: «делаем дальше, чиним замечания, которые
> нам сделаны в наших ПР» · «тестируем на симуляторе на этой машине» · **Status:** inventory done 2026-11-09 14:46;
> #4328-3 analysed 14:47; no code changed yet · **Outbound:** fixes → fork `pr/*` branches; reply texts → owner's
> proofreading before posting.

Dump: `gh api repos/crosspoint-reader/crosspoint-reader/pulls/<n>/comments --paginate` filtered `user.login ~ coderabbit`
(14 inline comments, all «Minor»). Upstream PR ↔ fork branch: #4328 `pr/epub-anchor-first-line` · #4332
`pr/sleep-image-order` · #4375 `pr/screen-clean-menu` · #4376 `pr/screen-redraw-delay` · #4377 `pr/screen-calibration`.

## Inventory (state 2026-11-09 14:46)

| PR | File:line | CodeRabbit effort | State |
|---|---|---|---|
| #4328 | `ChapterHtmlSlimParser.cpp:345` | Heavy lift | addressed in 27b28a3 (CodeRabbit's mark) |
| #4328 | `ChapterHtmlSlimParser.cpp:1411` | Quick win | addressed in 27b28a3 (CodeRabbit's mark) |
| #4328 | `ChapterHtmlSlimParser.cpp:3027` | Quick win | REPLY, no code (2026-11-09 15:22) — the path is not reachable in a parsed chapter; reply draft below |
| #4332 | `SleepActivity.cpp:545` | Poor tradeoff | FIXED on the branch in ca5d9fa0 (below); only a reply to CodeRabbit is missing |
| #4375 | `lib/I18n/translations/english.yaml:669` | Low value | ANALYSED — string draft waits for the owner (below) |
| #4376 | `BmpViewerActivity.cpp:465` | Low value | FIX committed locally `d101e463` on `pr/screen-redraw-delay` — [NOT-TESTED], not built, not pushed |
| #4376 | `src/main.cpp:541` | Low value | FIX committed locally `9448f2a5` on `pr/screen-redraw-delay` (path cleared in `redrawCustomImage`) — not built on the reader, not pushed |
| #4376 | `src/main.cpp:722` | Heavy lift | ANALYSED — needs a design + device check (below) |
| #4376 | `src/SettingsList.cpp:74` | Low value | FIX committed locally `2d5bb845` (emit on every board, hide via `isHiddenOnDevice()`) — [NOT-TESTED], not pushed |
| #4377 | `ImageBlock.cpp:47` | Low value | ANALYSED — design tradeoff, reply or fix is the owner's call (below) |
| #4377 | `ReaderUtils.h:273` | Low value | FIX committed locally `75b92fc0` (clear pending sub-section on OOM in `SettingsListActivity::openSection`) — [NOT-TESTED], not pushed |
| #4377 | `CalibrationCard.cpp:192` | Low value | FIX committed locally `7addf5be` (valid UUID `…-8c51-6b65696e6b74`, card `books_card_v2.epub`, v1 removed) — [NOT-TESTED], not pushed |
| #4377 | `CalibrationCardStorage.cpp:99` | Low value | ANALYSED — the current design is deliberate (below) |
| #4377 | `PanelCurve.cpp:62` | Low value | FIX committed locally `b6477e41` (CodeRabbit's own diff) — [NOT-TESTED], not pushed |

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
- Re-check 2026-11-09 15:22 (`[AI]`): the "chapter ends inside an open table row" path does NOT reach `finishParse()` —
  an unclosed element is an expat error at the final buffer, `parseStep()` returns `Error` (`:2968-2976`; only
  trailing data after `</html>` is tolerated). Every `currentTextBlock.reset()` inside a table (`:979`, `:1547`,
  `:1591`, `:1611`) is followed by `</table>` → `:2799`, which opens a new block. The one remaining null path is OOM
  at `:2799` (or `:2397`), which logs and does not latch `layoutOom` — it then drops the whole final page, not only
  the anchors, and that code is upstream's, outside this PR's diff (`git diff 8503b7fb pr/epub-anchor-first-line`).
- FORK: defensive fix in `finishParse()` | reply with the reachability analysis · price of error low · consulted:
  CodeRabbit's own agent prompt ("Fix only still-valid issues, skip the rest with a brief reason"), the code above →
  reply. A defensive fix would be untestable without OOM injection.

## #4332 — repeated sleep image when `sleep_last.txt` cannot be written (comment on 4a5ac603)

- Owner's prior choice: interview #001 Q2 → `A` («продолжать цикл при обычном сне и пробуждении»;
  `interviews/decisions/interview_001_crosspoint_user_choices.decision.json`).
- Already on `origin/pr/sleep-image-order`: `ca5d9fa0 fix: retain unsaved sleep image cursor` (2026-11-05 15:48 +03:00) —
  `RTC_DATA_ATTR SleepImageCursor` (289 bytes) keeps the unsaved position through deep sleep and wins over the card
  until a write succeeds; cold boot falls back to the card; host tests `test/sleep_image_cursor/`; USER_GUIDE updated.
- To do: a reply in the CodeRabbit thread pointing at ca5d9fa0 — draft for the owner's proofreading. Host tests not
  re-run on this PC yet (no toolchain).

## #4375 — the Screen Cleaning note implies cleaning runs with Refresh Frequency = Never (HEAD ea0a3625)

- Screen «Screen Cleaning» / «Очистка экрана» holds two rows: `STR_REFRESH_FREQ` («Refresh Frequency» / «Частота
  обновления») and `fadingFix`; the note `STR_SCREEN_CLEAN_NOTE` is drawn under them (`SettingsActivity.cpp:523-526`).
- Now: EN `english.yaml:669` «Screen cleans run from time to time and remove traces and halos of previous screens.»;
  RU `russian.yaml:642` «Очистки экрана выполняются периодически, помогают убрать следы и ореолы прошлых экранов.»
- Verdict `[AI]`: the claim holds — "from time to time / периодически" is false when Refresh Frequency is Never.
- Draft for the owner (on-device text in his name — his wording decides) `[AI]`:
  EN «Screen cleans remove traces and halos of previous screens. Refresh Frequency sets how often they run.»
  RU «Очистка экрана убирает следы и ореолы прошлых экранов. Как часто она выполняется, задаёт «Частота обновления».»
  Both strings fit the note's two-line area? — check on the simulator before the commit.

## #4376 — stale sleep image path arms another redraw timer (HEAD d7cc4e83)

- `main.cpp:530-541` arms the timer from `SleepActivity::lastCustomImagePath()`, a RAM `std::string`
  (`SleepActivity.cpp:35`) cleared ONLY in `SleepActivity::onEnter()` (`:700`) and set at `:803`, `:815`.
- Claim holds by code: a deep-sleep entry that skips `SleepActivity` (CodeRabbit: a suppressed page-button release)
  reads the previous path. Candidate fix `[AI]`: clear the path at the start of every sleep transition, before
  `SleepActivity` runs — needs the exact call order of the sleep entry in `main.cpp` (not read yet) so the clear never
  wipes the path `SleepActivity` has just set. Verify on the simulator: power press during a timer redraw → no second
  timer for the old path in the log.

- Fixed 2026-11-09 15:20 in `9448f2a5 fix: forget the redrawn sleep image path`: setter inventory of
  `lastCustomSleepPath` — two writes, both inside `renderCustomSleepBmp()` (`:803`, `:815`); one clear, in
  `onEnter()`. Inside one boot the only path that outlives its sleep is the timer redraw in `setup()` followed by a
  wake; `ActivityManager::loop()` returns early on `consumeSuppressedRelease()` (`ActivityManager.cpp:106`) and skips
  `onEnter()`. `redrawCustomImage()` now clears the path after painting. FORK: clear in `redrawCustomImage` | new
  static clear called from `enterDeepSleep` · price low · consulted: CodeRabbit's prompt ("keep changes minimal"),
  the setter inventory → the one-line fix. The timer path is `!SIMULATOR`: the simulator compiles it, only the
  reader runs it.

## #4376 — a valid power hold during the timer redraw is lost (`main.cpp:700-721`, HEAD d7cc4e83)

- During `redrawCustomImage()` an interrupt only sets `settledRedrawPress` (edge seen). After it: wake if
  `settledRedrawPress && shortPwrBtn == SLEEP`, else `gpio.verifyPowerButtonWakeup()` — which samples the button NOW.
  A hold that starts and ends inside the redraw, long enough to wake normally, is therefore ignored when `shortPwrBtn`
  is not SLEEP. Claim holds by code.
- Candidate fix `[AI]`: the ISR records press and release times (`millis()` on both edges, `CHANGE`); after the redraw,
  a completed hold ≥ the normal wake hold time counts as a wake request. Needs the wake threshold from
  `verifyPowerButtonWakeup()` and a check on the reader (the simulator has no deep-sleep timer path) → the owner's
  device test; propose to keep it out of this PR and answer CodeRabbit with the limit, if the owner agrees.

## #4376 — `BmpViewerActivity.cpp:465` (fixed locally, d101e463)

`millis() - paintedAtMs.load()` → paint time loaded into a local first, then `millis()`; the writer
(`render()` → `paintedAtMs` relaxed, `imagePainted` release) and the reader's acquire stay paired.

## #4377 — two design tradeoffs (HEAD f90b29b4)

- **`ImageBlock.cpp:47` superseded curve caches.** `getCachePath()` names a pixel cache `<image>_k<hash>.pxc` per
  book tone curve; a new curve leaves the old caches on the card. CodeRabbit's number: 4 obsolete curves × 500 images
  at 482×728 ≈ 176 MB. Claim holds by code. Options `[AI]`: (a) on a curve change, remove `*_k*.pxc` whose hash is not
  the current one (a directory walk per book on the first image); (b) reply: curves change rarely (one calibration per
  panel), the card is the user's, a "Clear reading cache" action already exists (`STR_CLEAR_READING_CACHE`).
- **`CalibrationCardStorage.cpp:99` reuse both picture-card orientations.** `picturesCard()` keeps ONE card in the folder
  on purpose (comment: "the viewer pages through its siblings") and rewrites 1.15 MB when the orientation changes.
  CodeRabbit proposes caching both and excluding the unused one from sibling navigation. Verdict `[AI]`: the current
  design trades a rare rewrite for no special case in the viewer; propose a reply with that reason.

## Reply drafts for the CodeRabbit threads — NOT posted, the owner proofreads first `[AI]`

- **#4332 `SleepActivity.cpp:545`:** "Fixed in ca5d9fa0: the unsaved position is kept in RTC memory (`RTC_DATA_ATTR`,
  survives deep sleep) and takes priority over `sleep_last.txt` until a write succeeds; a cold boot falls back to the
  card. Host tests in `test/sleep_image_cursor/`."
- **#4377 `CalibrationCardStorage.cpp:99`:** "Intentional: the folder holds one picture card so the viewer's sibling
  navigation needs no special case. An orientation change rewrites the card once; the calibration screen is opened
  rarely, so the rewrite is cheaper than a second card plus a sibling filter."
- **#4328 `ChapterHtmlSlimParser.cpp:3027`:** "The table case does not reach `finishParse()` with a null block:
  `</table>` opens a new text block right away, and a chapter that ends inside an open table is an XML error, so the
  section build fails before `finishParse()`. The only remaining null path is an allocation failure of the
  post-table block, which loses the whole final page, not only its anchors; that path predates this PR, so I would
  keep it out of here."
- **#4377 `ImageBlock.cpp:47`:** pending the owner's choice (cleanup on curve change, or reply pointing at "Clear
  reading cache").
- Fix replies (after the build and the simulator run, with the commit hash): #4376 ×2, #4377 ×3.

## Next

1. Toolchain after the KAGO lock (STATUS → "Where to continue").
2. Walk the remaining 11 open comments the same way: claim → INTENT line → verdict → fix or reply draft.
3. Reply drafts to CodeRabbit go to the owner for proofreading; nothing is posted or pushed without his word.
