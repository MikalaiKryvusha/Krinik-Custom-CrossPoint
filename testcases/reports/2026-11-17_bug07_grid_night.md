# Run report — bug 07: Cover Grid covers after a night ↔ day switch (port of upstream b9c23473)

## 1. Work

The port of the two `HomeCoverCache` hunks of upstream `b9c23473` (#4494) onto `wip/kccp-1.1.3-debug2`, checked against
`testcases/TC_bug07_cover_grid_night_switch.md` (cases C1–C3, control K1) and `bugs/07_cover_grid_negative_after_night_switch.md`.
The owner's order, 2026-11-17 10:04 +03:00: «Сначала на симуляторе получить негатив на старой сборке, потом убедиться, что на
новой его нет».

## 2. Contour

Simulator `simulator_x4_pro_win` (PSRAM declared, so «Сетка обложек» is live). Old binary: built 2026-11-14 17:27 from the
`2fa20f3f` code (`5da8f37f` is comment-only; `HomeCoverCache` is the same in both). New binary: built 2026-11-17 10:18 from
`5da8f37f` + the uncommitted port (blobs `f181685a` / `52a5d779`, equal to `b9c23473`'s). Cards in `.tmp/`: `sd_grid_night`
(theme 4, `screenInverted` 1, recents `/guide.epub` = `РУКОВОДСТВО.epub`, `/calibration.epub` = `КАЛИБРОВКА.epub`, both
with JPEG covers), `sd_grid_day` (the same, `screenInverted` 0), `sd_lyra_night` (theme 1, night, `coverBmpPath` set).

## 3. Runs

Script S: `0:WAIT:Entering activity: Home;8000:SHOT:before;9000:SWIPE:0.5,0.0,0.5,0.5,300;9000:WAIT:Entering activity: FrontlightPanel;2000:TAP:0.1875,0.3525;4500:SHOT:shade;5500:BACK;9000:SHOT:after;10000:QUIT`;
the Lyra script opens the book first: `0:WAIT:Entering activity: Home;2000:TAP:0.3,0.22;2000:WAIT:Entering activity: EpubReader;4000:BACK;4000:WAIT:Entering activity: Home;6000:SHOT:before;…` (then as S).
Every run: `SD_TEMPLATE=../.tmp/<card> SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh <name> '<script>' ''`.

| # | Moment | Name · card · binary | Exit / outcome |
|---|---|---|---|
| 1 | 2026-11-17 10:07 +03:00 | `grid_night_probe` · `sd_grid_night` · old (Home, then the shade; locates the night button) | 0 errors |
| 2 | 2026-11-17 10:08 +03:00 | `grid_night_red` · `sd_grid_night` · old · S | 0 errors; `screenInverted` 0 after |
| 3 | 2026-11-17 10:11 +03:00 | `grid_day_red` · `sd_grid_day` · old · S | 0 errors; `screenInverted` 1 after |
| 4 | 2026-11-17 10:12 +03:00 | `lyra_night_old` · `sd_lyra_night` · old · Lyra script | 1 `[ERR]`: `Cannot generate thumb BMP, cache not loaded` before the book is opened (expected) |
| 5 | 2026-11-17 10:19 +03:00 | `grid_night_green` · `sd_grid_night` · new · S | 0 errors; `screenInverted` 0 after |
| 6 | 2026-11-17 10:19 +03:00 | `grid_day_green` · `sd_grid_day` · new · S | 0 errors; `screenInverted` 1 after |
| 7 | 2026-11-17 10:20 +03:00 | `lyra_night_new` · `sd_lyra_night` · new · Lyra script | the same 1 expected `[ERR]` |

Host suite: `sh tools/host_tests.sh` on the new tree — the result line is in section 4.

## 4. Checks

- Hygiene: the port is byte-identical to upstream (`git hash-object` = `b9c23473:` blobs); the independent judge (fresh agent,
  diff + requirement) — «OK TO BUILD», no blocker; the simulator build SUCCESS (00:02:50); host suite — see below.
- Functional run: the simulator, Home in «Сетка обложек» and Lyra, night switched by the shade's night button over Home, the
  WebP shots READ after the shade closed.

| Case | Status | Observation |
|---|---|---|
| K1 control (old binary) | pass | `grid_night_red/after.webp`: both covers negative in day (black page, white print); `grid_day_red/after.webp`: both negative in night |
| C1 smoke · grid night → day | pass | `grid_night_green/after.webp`: both covers light page, dark print |
| C2 · grid day → night | pass | `grid_day_green/after.webp`: both covers light page, dark print, as at a boot in night mode (`grid_night_probe/home.webp`) |
| C3 · Lyra night → day (#4329 path) | pass | old and new: `lyra_night_*/after.webp` the cover positive |

## 5. Found

- The bug itself, on the old binary (K1) — closed by the port.
- Seen alongside, not this fix: while the shade stays open after its night button, the Home pixels under it keep the old
  polarity, so a cover below the shade shows as a negative until the shade closes (`grid_night_red/shots/shadeday.webp`,
  `grid_night_green/shots/shade.webp`); the shade converts the frame under itself only over the photo viewer
  (`FrontlightPanelActivity::runTile`, `grayglass::viewerUnderneath` → `renderer.invertScreen()`). Recorded in bug 07.

## 6. Traces

`qa_runs/grid_night_probe/`, `qa_runs/grid_night_red/`, `qa_runs/grid_day_red/`, `qa_runs/lyra_night_old/`,
`qa_runs/grid_night_green/`, `qa_runs/grid_day_green/`, `qa_runs/lyra_night_new/` (log.txt + shots/*.webp);
`.tmp/build_bug07_sim.log`; `.tmp/host_tests_bug07.log`.

## 7. Verdict

pass on the simulator for C1–C3 with the control red. Not verified on the owner's reader (comes with the debug2 image).
