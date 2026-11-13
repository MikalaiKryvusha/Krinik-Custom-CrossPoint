# Test run report — idea 07 third set: the viewer keys (short press pages, long press turns), simulator

**Created:** 2026-11-13 16:14 +03:00 · **Run by:** the agent (Claude, KCCP session) · **Version/build:** firmware `wip/krinik-debug10`
(= `8538f3dd` + the uncommitted long-press diff, judged: no blockers), simulator `simulator_x4_pro_win`

## 1. Work

Cases C10–C12 of `testcases/TC_idea07_viewer_rotation_by_half.md` §7 — the owner 16:01–16:02: «А — листают картинки, как
и было» · «Лонг-нажатием можно сделать вразение»; `[AI]` forward key clockwise, back key counterclockwise.

## 2. Contour

The native Windows simulator, X4 Pro profile; a temporary card = `qa_runs/sd_template` + `pics/pic1.jpg`, `pics/pic2.jpg`
(600×400, an orientation triangle, one / two black bars); the viewer opened from «Обзор файлов» (file-browser mode).
Device not involved — no `REAL WORLD:` claim.

## 3. Runs

| # | Moment | Name · script | Exit / outcome |
|---|---|---|---|
| 1 | ≈ 2026-11-13 16:12 +03:00 (log overwritten by run 2) | `idea07_keys` · `0:WAIT:Entering activity: Home;1500:TAP:0.3,0.43;1500:WAIT:Entering activity: FileBrowser;1500:SHOT:files;2500:QUIT` | 0 · the folder `pics` at y 0.17 (overwritten by run 2) |
| 2 | 2026-11-13 16:13 +03:00 | `idea07_keys` · `…;1500:TAP:0.3,0.17;2500:TAP:0.3,0.17;2500:WAIT:Entering activity: BmpViewer;1500:SHOT:v0;2000:DOWN:150;2000:WAIT:Show 2;1500:SHOT:c10;2500:DOWN:1000;2500:WAIT:View turns;1500:SHOT:c11;2500:UP:1000;2500:WAIT:View turns;1500:SHOT:c12;3000:QUIT` | 0 · 0 errors |

All runs: `SD_TEMPLATE=sd_viewer_keys_tmp SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh <name> '<script>' ''`.

## 4. Checks

Hygiene: simulator build SUCCESS; the judge's read-only review — no blockers (two low findings for boards with front keys
and a hold-plus-swipe edge, none on the X4 Pro).
Functional run: the file browser → the folder → picture 1 → the keys as the owner presses them; the log lines and the
shots READ.

| Case | Status | Observation |
|---|---|---|
| C10 | pass | short DOWN (150 ms) → `Input: button prev`, `Show 2/2` — one page turn, on the release (two pictures wrap) |
| C11 | pass | hold DOWN 1000 ms → `long press back -> rotate counterclockwise`, `View turns: 3`, no `Input: button` line; shot `c11` = picture 2 (two bars), turned |
| C12 | pass | hold UP 1000 ms → `long press forward -> rotate clockwise`, `View turns: 0`, no page |

## 5. Found

- None. Noted from the judge (not the X4 Pro): on a board with front keys, a long front-key press pages instead of turning;
  holding a key while swiping Back can leave a suppressed-release bit for the next screen.

## 6. Traces

`qa_runs/idea07_keys/` — `log.txt` + `shots/*.webp`.

## 7. Verdict

pass on the simulator; the reader is the next stand (with the shade, one debug10 image).
