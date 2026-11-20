# Test run report — idea 14: the owner's pick «N» (sharp upscale of enlarged line art) on the simulator

**Created:** 2026-11-20 15:59 +03:00 · **Run by:** the agent (Claude Opus 5.5) · **Version/build:** firmware
`wip/kccp-line-art-filter` `353cb8b5` (N on top of the filter `5a9e1624`), env `simulator_x4_pro_win`

## 1. Work

The viewer draws an enlarged (≥ ×2) line-art picture of ≤ 8192 source pixels by `sharpup::Upscaler` = Pillow's
`resize(BICUBIC)` + `UnsharpMask(3, 160, 2)`, the owner's pick N (`ideas/14_viewer_smart_filter_bw_lowres.md`, 15:22–15:31);
photos and the rest keep the bilinear. Basis: the owner's picks on the PC mock-ups and his rejection of an approximation.

## 2. Contour

The X4 Pro simulator, viewer cards `.tmp/b17_i_016_on`, `.tmp/b17_i_001_on` (setting on by default), `.tmp/b17_i_140_on`
(a photo), `.tmp/b17_i_016_off` (`cleanLineArt: 0`); this repo's `panel_curve.txt`. Not the reader.

## 3. Runs

| # | Moment | Command | Exit / outcome |
|---|---|---|---|
| 1 | ≈ 2026-11-20 15:55 +03:00 | `TARGETS="SharpUpscaleTest LineArtFilterTest" sh tools/host_tests.sh` | 6/6 · 7/7 |
| 2 | ≈ 2026-11-20 15:55 +03:00 | the threshold mutated to `>=` in `SharpUpscale.h`, the same command, then restored | 3 of 6 red (the three Pillow goldens) |
| 3 | ≈ 2026-11-20 15:57 +03:00 | `SD_TEMPLATE=../.tmp/b17_<card> SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh idea14n_<card> '0:WAIT:Entering activity: BmpViewer;6000:SHOT:view;8000:QUIT' ''` for `i_016_on`, `i_001_on`, `i_140_on`, `i_016_off` | 0 · 0 errors each |
| 4 | ≈ 2026-11-20 15:58 +03:00 | `.tmp/bug17/compare_view_cache.py <view_*.bmp> .tmp/geb_in.epub OPS/images/<pic>.jpg panel_curve.txt` | see Checks |
| 5 | ≈ 2026-11-20 15:58 +03:00 | `sh tools/host_tests.sh` | 1008 tests, «no new failure (known list: 10)» |

## 4. Checks

- Hygiene: `SharpUpscaleTest` 6/6 byte-exact against Pillow goldens (x8, x2, a 3×5 source, output lines shorter than the blur
  window, flat pictures, the heap estimate), mutation-proven; `LineArtFilterTest` 7/7; the full host suite, no new failure.
- Functional run: the simulator opened each picture in the viewer at boot (the user's file path); READ: the log lines
  (`Sharp upscale …`, `Line art …`, `render time`), the viewer's cached 2-bit BMP of each run decoded level by level and compared
  with Pillow's N through the same curve and Bayer, the frames shown to the owner.

| Case | Status | Observation |
|---|---|---|
| formula `i_016`, on | pass | `Sharp upscale 36x91 -> 316x800: 38 ms` (PC simulator time); the cache vs Pillow N: 26 of 252 800 pixels differ — JPEGDEC's source grays vs libjpeg's |
| «3³³» `i_001`, on | pass | `Sharp upscale 52x54 -> 480x498: 35 ms`; vs Pillow N: 5 of 239 040 differ |
| photo `i_140`, on | pass | no `Sharp upscale` line — the decoder's bilinear (`render time: 8 ms`) |
| formula, setting off | pass | no `Line art`, no `Sharp upscale` — today's bilinear |
| the frames | shown | `.tmp/bug17/idea14_n_simulator.webp` (today vs N, the caches at full scale) opened in VS Code ≈ 15:58 |

## 5. Found

- none on the stand; the independent review's findings (1 MAJOR, 4 MINOR) were fixed before this run.

## 6. Traces

- Runs `idea14n_*` parked in `.tmp/b17_runs/` (book pictures, П4); build log `.tmp/bug17/sim_build3.log`; the PC replica
  `.tmp/bug17/pillow_exact.py` (0 differing bytes vs Pillow on GEB `i_016`, `i_001`, `i_078`).

## 7. Verdict

pass — on the simulator N draws what the owner picked (Pillow's N to within the JPEG decoders' source differences) and
leaves photos alone; the reader not verified: the reader's time for N is not measured (the PC simulator's 35–38 ms is not
the reader's).
