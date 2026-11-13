# Test run report — idea 02: a tap on a book picture opens it full screen (simulator)

**Created:** 2026-11-13 11:25 +03:00 · **Run by:** the agent (Claude, KCCP session) ·
**Version/build:** firmware `wip/krinik-debug9` `526c7452` (control: `wip/krinik-debug8` `c072214b`), simulator
`simulator_x4_pro_win`, simulator library `fix/gray-absolute-reset` `49ded1a`

## 1. Work

The picture tap of idea 02 (`ideas/02_image_fullscreen_on_tap.md`) against the case set
`testcases/TC_idea02_image_fullscreen_tap.md` (R1–R4, C1–C6, K1–K3): tap a picture → full screen; swipe Back → the
same book page; a tap inside a picture in the centre or a side zone opens it; taps on text keep the zones.

## 2. Contour

The native Windows simulator (X4 Pro profile, landscape CCW = the owner's `orientation: 3`, touch on, toolbar menu,
font size 16, page turn by tap and swipe), card `qa_runs/sd_book_images` copied fresh per run (own generated test
book `image_test.epub`: three JPEG pictures with «Рис. N» captions). Device not involved — no `REAL WORLD:` claim;
the owner's reader is the next stand (homework).

## 3. Runs

All runs: `SD_TEMPLATE=sd_book_images SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh <name> '<script>' '<shots>'`.

| # | Moment | Command (name · script) | Exit / outcome |
|---|---|---|---|
| 1 | 2026-11-13 11:12 +03:00 | `idea02_c1` · `12000:QUIT` | 0 · boot into the book, page 1 shot, 0 errors |
| 2 | 2026-11-13 11:13 +03:00 | `idea02_c2c3` · `3000:TAP:0.5,0.40;7000:SWIPE:0.05,0.5,0.6,0.5,300;13000:QUIT` | 0 · viewer opened; after Back the page was DARK |
| 3 | 2026-11-13 11:14 +03:00 | `idea02_dark` · tap, Back, swipe next, swipe prev | 0 · every page after the viewer dark |
| 4 | 2026-11-13 11:15 +03:00 | `idea02_ctrl_browser` (card `_tmp_viewer_ctrl`) · `4000:SWIPE:0.05,0.5,0.6,0.5,300;9000:QUIT` | 0 · viewer → file browser light (control) |
| 5 | 2026-11-13 11:17 +03:00 | `idea02_dark_fix` · as run 3, firmware clean-base change | 0 · still dark — hypothesis 1 refuted |
| 6 | 2026-11-13 11:21 +03:00 | `idea02_c2c3_fix` · as run 3, simulator fix `49ded1a` | 0 · page 1/8 and 2/8 light |
| 7 | 2026-11-13 11:22 +03:00 | `idea02_c4_k1_k2` · `3000:TAP:0.83,0.40;6000:SWIPE:…;9000:TAP:0.95,0.75;12000:TAP:0.5,0.5;15500:QUIT` | 0 · see C4, K2, K1 |
| 8 | 2026-11-13 11:22 +03:00 | `idea02_find_p` · three side taps on text | 0 · the tall picture is on page 4 |
| 9 | 2026-11-13 11:22 +03:00 | `idea02_c5` · to page 4, `TAP:0.5,0.45`, Back, next page | 0 · see C5 |
| 10 | 2026-11-13 11:24 +03:00 | `idea02_k3_debug8` (debug8 build) · `3000:TAP:0.5,0.40;6500:QUIT` | 0 · menu, no viewer |
| 11 | 2026-11-13 11:27 +03:00 | `idea02_smoke_final` (`35dc070c`, the image's code) · side tap on pic 1, Back, pages, tap on pic 2, Back | 0 · viewer → 1/8, viewer → 4/8 |
| 12 | 2026-11-13 11:34 +03:00 | `idea02_c7_png` · to page 6, `TAP:0.5,0.37`, Back | 0 · PNG full screen → 6/8 |

## 4. Checks

Hygiene: host test `PageImageTargetTest` 4/4 + `PageLinkTest` 1/1 (`cmake --build build/test --target …`, MSYS2
UCRT64 + Ninja); mutation `<` → `<=` red on 2 of 4; simulator build SUCCESS ×4, no warnings in the touched files.
Functional run: the simulator walked by the user's path (boot into the book → tap / swipe as the owner does), the
WebP shots and the log lines READ for every case below.

| Case | Status | Observation |
|---|---|---|
| C1 | pass | page 1/8: heading, picture 1, caption; 0 errors (`idea02_c1/shots/p1.webp`) |
| C2 | pass | tap at picture 1's centre → the picture fills the screen; log `[INF] [ERS] Image tap: …img_0_0.jpg (heap free …)`, `Entering activity: BmpViewer` |
| C3 | pass (after the simulator fix) | Back swipe → `Popped … Handling result`, page 1/8 as before the tap (`idea02_c2c3_fix/shots/back.webp`); next page 2/8 light |
| C4 | pass | tap inside picture 1 at x=0.83 (the right page-turn zone) → the viewer, not page 2 |
| C5 | pass | full-page tall picture on page 4 → viewer shows it full height; Back → 4/8 |
| C6 | skipped | the simulator repaints the page ~13 ms after the pop, so a second swipe cannot land inside the window; the device check (homework) covers it |
| C7 | pass | the small PNG picture 3 (240×160) on page 6 → the viewer scales it to the full screen; Back → 6/8 (`idea02_c7_png`) |
| K1 | pass | centre tap on text (page 2) → the toolbar menu |
| K2 | pass | side tap on text (caption line, x=0.95) → page 2/8 |
| K3 | pass | the same picture tap on debug8 → the toolbar menu, no viewer — the feature is what changed it |

## 5. Found

- The simulator kept its absolute grayscale preview mode after the image viewer, so every later overlay page showed
  dark (runs 2–5); not a firmware defect (the control run 4 and the cause in `simulator/src/HalDisplay.cpp`
  `composeGrayscalePreview` / `refreshDisplay`); fixed in the simulator `49ded1a` (local branch, not pushed) —
  `bugs/06_sim_absolute_gray_mode_stale.md`.
- Seen on the way, idea 03's class on our own book: the tall picture moved whole to page 4, page 3 half empty, its
  caption «Рис. 2…» opens page 5 (`idea02_c5/shots/p4.webp`, `p5.webp`).

## 6. Traces

- `qa_runs/idea02_c1`, `idea02_c2c3`, `idea02_dark`, `idea02_ctrl_browser`, `idea02_dark_fix`, `idea02_c2c3_fix`,
  `idea02_c4_k1_k2`, `idea02_find_p`, `idea02_c5`, `idea02_k3_debug8`, `idea02_smoke_final`, `idea02_find_png`,
  `idea02_c7_png` — `log.txt` + `shots/*.webp` each.
- The judge's reports: summarised in `ideas/02_image_fullscreen_on_tap.md` → «Judge findings».

## 7. Verdict

partial — every simulator case passes (C6 skipped for a reason the simulator cannot model), but the feature's real
path is the owner's reader (heap under the viewer, the panel's repaint time for C6) and that run is next.
