# Test run report — idea 07: a long tap in the viewer turns the picture toward its half of the screen (simulator)

**Created:** 2026-11-13 14:33 +03:00 · **Run by:** the agent (Claude, KCCP session) ·
**Version/build:** firmware `wip/krinik-debug10` (= `35dc070c` + the idea 07 diff, uncommitted at run time; control:
`wip/krinik-debug9` `35dc070c`), simulator `simulator_x4_pro_win` built clean 14:21 with the MSYS2 toolchain in
`F:\ai_sandbox\msys64` (271 files compiled, 0 from cache)

## 1. Work

The long-tap rotation of idea 07 (`ideas/07_viewer_long_tap_rotation_by_half.md`) against the case set
`testcases/TC_idea07_viewer_rotation_by_half.md` (R1–R4, D0, C1–C5): right half → clockwise, left half →
counterclockwise, one each way → the first view, the swipe Back unchanged.

## 2. Contour

The native Windows simulator (X4 Pro profile, landscape CCW = the owner's `orientation: 3`, touch on), card
`qa_runs/sd_book_images` copied fresh per run — own generated test book `image_test.epub`, its pictures carry an
orientation triangle in the top-left corner since `22391ea`. Device not involved — no `REAL WORLD:` claim; the owner's
reader is the next stand (the debug10 image after idea 05).

## 3. Runs

All runs: `SD_TEMPLATE=sd_book_images SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh <name> '<script>' ''`.

| # | Moment | Name · script | Exit / outcome |
|---|---|---|---|
| 1 | ≈ 2026-11-13 14:12 +03:00 (log overwritten by run 3) | `idea07_d0_debug9` · `3000:TAP:0.5,0.40;WAIT:Entering activity: BmpViewer;…` (WAIT without its time) | 0 · the script ran at once: shot and a long tap in the book — discarded (EXP-0015) |
| 2 | ≈ 2026-11-13 14:13 +03:00 (log overwritten by run 3) | `idea07_d0_debug9` · times going down inside a WAIT segment | 0 · the second tap before the shot — discarded (EXP-0015) |
| 3 | 2026-11-13 14:14 +03:00 | `idea07_d0_debug9` (debug9 binary) · `3000:TAP:0.5,0.40;3000:WAIT:Entering activity: BmpViewer;1500:SHOT:v0;2000:TAP:0.75,0.5,800;2000:WAIT:long tap;1500:SHOT:r1;2500:TAP:0.25,0.5,800;2500:WAIT:long tap;1500:SHOT:l1;3000:QUIT` | 0 · D0, see Checks |
| 4 | 2026-11-13 14:31 +03:00 | `idea07_c1235` (debug10) · the script of run 3 + `2500:SWIPE:0.05,0.5,0.6,0.5,300;2500:WAIT:Popped;1500:SHOT:back;3000:QUIT` | 0 · C1, C2, C3, C5 |
| 5 | 2026-11-13 14:31 +03:00 | `idea07_c4` (debug10) · `3000:TAP:0.5,0.40;3000:WAIT:Entering activity: BmpViewer;1500:SHOT:v0;2000:TAP:0.25,0.5,800;2000:WAIT:long tap;1500:SHOT:l0;3000:QUIT` | 0 · C4 |

## 4. Checks

Hygiene: clean simulator build SUCCESS (no warnings in `BmpViewerActivity.cpp`); the judge's read-only review — no
blockers (`ideas/07` → «Judge»); the `sim_run.sh` script guard red on the two broken scripts of runs 1–2.
Functional run: the simulator walked by the user's path (boot into the book → tap the picture → long taps as the owner
makes them → swipe Back), every WebP shot and the log lines READ for each case below.

| Case | Status | Observation |
|---|---|---|
| D0 | pass (control) | debug9: right long tap → triangle top-left → top-right; left long tap → top-right → bottom-right: both halves turn clockwise, `+1` = clockwise on screen (`idea07_d0_debug9/shots/v0,r1,l1.webp`) |
| C1 | pass | the viewer shows picture 1 full screen, triangle top-left (`idea07_c1235/shots/v0.webp`) |
| C2 | pass | right long tap → triangle top-right, the picture tall; log `long tap at x=599 of 800 (right half) -> rotate clockwise` (`r1.webp`) |
| C3 | pass | then a left long tap → triangle top-left again, the view of C1; log `x=199 of 800 (left half) -> rotate counterclockwise` (`l1.webp`) |
| C4 | pass | a left long tap first → triangle bottom-left, counterclockwise; log `left half` (`idea07_c4/shots/l0.webp`) |
| C5 | pass | swipe Back after C3 → book page 1/8 as before the tap; log `Popped from activity stack` (`back.webp`) |

## 5. Found

- No defect of the change.
- Two slips of my own scripts (runs 1–2): a WAIT without its time, and times going down inside a WAIT segment — both
  silently misread by the simulator; closed by a guard in `tools/sim_run.sh` (exit 2, proven red on both), EXP-0015.

## 6. Traces

- `qa_runs/idea07_d0_debug9`, `qa_runs/idea07_c1235`, `qa_runs/idea07_c4` — `log.txt` + `shots/*.webp` each.
- The judge's report: summarised in `ideas/07_viewer_long_tap_rotation_by_half.md` → «Judge».

## 7. Verdict

partial — every simulator case passes and the control shows the change is what made the difference; open: the frame of
the halves after the reader is turned in the hands (the owner's choice A/B, asked 14:20) and the real path — the
owner's reader with the debug10 image.
