# Test run report — idea 14: «Чистить фон чертежей» (the line-art filter) on the simulator

**Created:** 2026-11-20 15:14 +03:00 · **Run by:** the agent (Claude Opus 5.5) ·
**Version/build:** firmware `wip/kccp-line-art-filter` (from `wip/kccp-1.1.4` `8a8b44bc`) after the two independent
reviews' fixes, env `simulator_x4_pro_win`

## 1. Work

The line-art filter of idea 14 (`ideas/14_viewer_smart_filter_bw_lowres.md`): a black-and-white picture up to 480×800 of
area loses its faint JPEG noise in the full-screen viewer, the file browser's viewer and on the book page; photos are
untouched; a «Чтение» checkbox, on by default. Case set `testcases/TC_idea14_smart_filter.md` (cases 1–9).

## 2. Contour

The X4 Pro simulator (native Windows), viewer cards `.tmp/b17_i_016_{on,off}` and `.tmp/b17_i_140_{on,off}` (template card
+ the GEB picture at the root, `state.json` opening it at boot, `cleanLineArt: 0` on the `off` cards, this repo's
`panel_curve.txt` in `/.crosspoint/`, «Калибровка картинок» on by default); the page cards `.tmp/b17_geb_{on,off}` = the
owner's settings and GEB copy (П4, `.tmp/b14_sd`: landscape, Literata, «Калибровка книг» off). Not the reader: the eFuse
reader gets an image only after the owner's word on the release.

## 3. Runs

| # | Moment | Command | Exit / outcome |
|---|---|---|---|
| 1 | 2026-11-20 15:10 +03:00 | `SD_TEMPLATE=../.tmp/b17_i_016_on SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh idea14_i_016_on '0:WAIT:Entering activity: BmpViewer;5000:SHOT:view;7000:QUIT' ''` | 0 · 0 errors · `Line art 36x91: lighter than 203 -> white` |
| 2 | 2026-11-20 15:10 +03:00 | the same with `b17_i_016_off` / `idea14_i_016_off` | 0 · 0 errors · no `Line art` line |
| 3 | 2026-11-20 15:10 +03:00 | the same with `b17_i_140_on` / `idea14_i_140_on` | 0 · 0 errors · histogram counted, no `Line art` line |
| 4 | 2026-11-20 15:11 +03:00 | the same with `b17_i_140_off` / `idea14_i_140_off` | 0 · 0 errors |
| 5 | 2026-11-20 15:11 +03:00 | `START=60 CARD=.tmp/b17_geb_on sh tools/sim_pages.sh idea14_geb_on 10 10` | 10 shots, 9 ERR (all `[TTF]`, the stand's known lines) · `[IMG] Line art: lighter than 203 -> white` |
| 6 | 2026-11-20 15:12 +03:00 | `START=60 CARD=.tmp/b17_geb_off sh tools/sim_pages.sh idea14_geb_off 10 10` | 10 shots, 9 ERR (`[TTF]`) · no `Line art` line |
| 7 | 2026-11-20 15:04 +03:00 | `CROSSPOINT_SIM_SCREEN_TEXT=1 SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh idea14_set2 '0:WAIT:Entering activity: Home;1500:TAP:0.3,0.68;1500:WAIT:Entering activity: SettingsList;1500:TAP:0.3,0.37;1500:WAIT:Entering activity: Settings;1500:SHOT:r1;…;8000:QUIT' ''` (first build; the settings code unchanged since) | 0 · 0 errors |
| 8 | 2026-11-20 15:10–15:12 +03:00 | `tools/shot_diff.py` on the `i_140` and `i_016` pairs; `.tmp/bug17/pxc_compare.py` on the page caches | see Checks |
| 9 | 2026-11-20 ≈ 15:07 and 15:13 +03:00 | `TARGETS="LineArtFilterTest" sh tools/host_tests.sh` · `sh tools/host_tests.sh` | 7/7 · the full suite: see Checks |

## 4. Checks

- Hygiene: `LineArtFilterTest` 7/7 on the real GEB histograms; mutation proofs red on target (detector inverted → 4 of 5
  red; 80 % for 90 % → the cut case red; floor 0 → `CutNeverBelowTheFloor` red); the full host suite after the first
  version 1002 tests, «no new failure (known list: 10)»; after the review fixes again 1002, «no new failure (known list:
  10)», ended 2026-11-20 15:14 +03:00.
- Functional run: the simulator walked by the user's paths — a picture opened in the viewer (the file path), a GEB page
  turned to by page keys on the owner's settings, Settings → «Чтение» by taps; READ: the shots, the logs' `Line art` /
  `Gray histogram` lines, the screen text, and the page picture's pixel caches byte by byte.

| Case | Status | Observation |
|---|---|---|
| TC 1 | pass | the viewer's formula: the gray squares around the digits gone (`idea14_i_016_on/shots/view.webp`), log cut 203 |
| TC 2 | pass | the setting off: no `Line art` line; the squares as today; `shot_diff` off↔on 2773 px — the filter changes the frame |
| TC 3 | pass | the photo with the setting on: counted, detected as a photo, no filter |
| TC 4 | pass | the photo off↔on: `shot_diff` TOTAL 0 |
| TC 5 | pass | GEB chapter II p. 65 (spine 10): `[IMG] Line art: lighter than 203 -> white`; the page cache `img_10_0_f1.pxc` vs the off run's `img_10_0.pxc`: 18 of 3276 pixels differ (light gray → white), the black and dark levels identical (292 / 138) — the edges' anti-aliasing kept |
| TC 6 | pass | the page off: no `Line art` line; the page frames on↔off identical (`shot_diff` TOTAL 0 — the 36×91 picture at 1:1 without the book curve carries little noise) |
| TC 7 | pass | «Чтение» lists «Чистить фон чертежей» under «Изображения», checked (screen text + `r1.webp`) |
| TC 8 | pass (stand only) | the extra counting decode on the PC simulator: 0–1 ms against 7–8 ms of the render decode; the reader's time not measured (no timing reaches its log) |
| TC 9 | pass | 7/7; full suite — see Hygiene |

## 5. Found

- none in the firmware's behaviour on the stand; the reviews' findings (two passes, 3 MAJOR + 11 MINOR) were fixed before
  this run or recorded as the owner's open questions in idea 14 (the floor 160, BMP files).

## 6. Traces

- Logs and shots: `qa_runs/idea14_set1`, `qa_runs/idea14_set2` (the settings screens); the runs carrying GEB pictures and
  pages — `idea14_i_016_*`, `idea14_i_140_*`, `idea14_geb_*` — parked in `.tmp/b17_runs/` (third-party book, П4).
- Build logs `.tmp/bug17/sim_build.log`, `.tmp/bug17/sim_build2.log`; the cache comparer `.tmp/bug17/pxc_compare.py`.
- The reviews: idea 14 → «The independent review» (both passes).

## 7. Verdict

pass — every case of the set passed on the simulator; the reader itself is not verified (an image goes to it only after
the owner's word), and two choices wait for the owner (the floor 160, BMP files in the file browser).
