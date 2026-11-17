# Bug 07 — «Сетка обложек»: covers paste back as a negative after a night ↔ day switch on Home

**Status:** 🔴 OPEN — the cause is read in the code, the fix exists upstream; not reproduced on our stand yet · **Severity:** S2
**Version/build:** KCCP `wip/kccp-1.1.3-debug1` (`bcbd6dab`) and `wip/kccp-1.1.3-debug2` (`5da8f37f`); upstream before
`b9c23473` · **When/context:** 2026-11-17 09:54 +03:00, the owner: «нам ответили по фиксу бага с инверсией обложки… у него
воспроизвелось» · **Fixing:** after the owner's word — port the upstream hunk (below) onto `wip/kccp-1.1.3-debug2`
before the debug2 image

## Symptom

Upstream PR #4329 (ours, merged 2026-11-07) fixed the recent-book cover turning negative after a theme switch. On
2026-11-16 19:10 UTC itsthisjustin wrote under it: «even after this merge I was able to get the inverted covers when
switching from dark to light mode at the home screen», and at 19:12 UTC: «Ah your fix was specific to the single covers
not the grid I happen to use :)».

## Root cause (read in the code, not run)

Home keeps two independent cover snapshot caches, and #4329 fixed only one of them:

1. `HomeActivity::coverBuffer` — the single-cover snapshot of Classic / Lyra / Lyra Extended / RoundedRaff
   (`storeCoverBuffer` / `restoreCoverBuffer`). #4329 records `coverBufferInverted` and drops the snapshot when the
   polarity differs.
2. `HomeCoverCache` (`src/components/HomeCoverCache.{h,cpp}`, since #3657 of 2026-09-22 — already in the base of our
   PR) — the PSRAM per-cover snapshots of the «Сетка обложек» theme (`COVER_GRID`, PSRAM boards only; the X4 Pro has
   8 MB PSRAM, so it is offered on our readers). `prepare()` invalidated the cache on an ORIENTATION change only.

`HomeActivity::render` takes the grid branch first and `return`s before the #4329 polarity check, so the check never
runs for the grid; `CoverGridHomeUi::draw` → `coverCache.prepare()` keeps the snapshots taken in the other polarity
and `paint()` pastes them back → negative covers (night mode stores images pre-inverted).

The upstream fix: Justin added the polarity to `HomeCoverCache::prepare()` inside #4494 (merged 2026-11-16 19:59 UTC,
squash `b9c23473`, titled «Add EEGO A4 specific auto-sleep timing»): `coverCacheInverted` beside `coverCacheOrientation`,
invalidate when either changes. `prepare()` runs at the top of every grid draw, so that covers every repaint.

## Twin sweep

`TWINS: searched copyRegionToBuffer|copyBufferToRegion|storeBwBuffer|restoreBwBuffer in src/ lib/ of upstream/develop
and wip/kccp-1.1.3-debug2 — found 2 cross-render snapshot caches of Home (coverBuffer: fixed by #4329; HomeCoverCache:
open in KCCP) + the EPUB reader overlay page (its own NIGHT_MODE action calls discardOverlayPage() — handled) +
short-lived store/restore pairs inside one frame (SleepActivity band, ReaderUtils, ScreenshotUtil — no polarity switch
between them). Not checked: the shade's night tile toggled while a reader overlay snapshot is held.`

## Repro (to do — the stand step that comes next)

Simulator `simulator_x4_pro_win`, theme 4 card (`qa_runs/sd_theme4`) with recent books, night mode on → Home → open the
shade → night tile off → shade closes → shot of Home: expected positive covers; on debug2 expected negative.

## Fix plan

Port the two hunks of `b9c23473` (`src/components/HomeCoverCache.{h,cpp}`) onto `wip/kccp-1.1.3-debug2`; judge → build →
the repro above red on the old binary, green on the new one; `sh tools/host_tests.sh`.

## Decisions made without the owner

- `[AI]` Severity S2: a visible defect on a theme the owner's reader does not use (`settings.json` → `uiTheme` 1, Lyra).

## Links

PR #4329 (`qa_runs/pr-review-2026-11-05/4329.diff`), `researches/2026-11-07_upstream_pr_discussion.md`, EXP-0023.
