# Test cases — #4376 `pr/screen-redraw-delay`: fixes for the CodeRabbit round

**Created:** 2026-11-09 · **Under test:** fork branch `pr/screen-redraw-delay` at `4818dba0` (fixes `d101e463`, `2d5bb845`,
`9448f2a5`, `4818dba0`) · **Version/build:** `simulator_x4_pro_win` / `simulator_win` (native Windows simulator, `simulator`
`0431782`), device image for the owner
**Test basis:** the CodeRabbit comments quoted in `researches/2026-11-09_coderabbit_pr_review.md`; the owner's choice in
`interviews/interview_003_coderabbit_round2.md` Q3 = B; the commit messages of the four fixes.

## 1. Goal vector

Maintain: the delayed redraws of PR #4376 keep working, and the four review findings no longer hold — a settings file
keeps the sleep-redraw value on every board, the image redraw fires once and never early, a stale sleep path arms no
timer, a power hold made during the timer redraw wakes the reader.

## 2. Requirements under test

| # | Requirement (EARS sentence) | Fit criterion |
|---|---|---|
| R1 | WHERE the board is the X4 Pro, the Display settings shall show the sleep-image redraw row. | screenshot of Display settings shows the row |
| R2 | WHEN a board other than the X4 Pro saves settings, the file shall keep `sleepRedrawDelay`. | `settings.json` after the save · grep · value = the seeded `2` |
| R3 | WHILE an image is open with a 1-minute image redraw, the viewer shall redraw it once, ≥ 60 s after the paint. | log line `Settled image redraw` · its timestamp − paint timestamp ≥ 60 000 ms, count = 1 |
| R4 | WHEN the timer redraw has painted, the recorded sleep path shall be empty. | device only (`!SIMULATOR`) |
| R5 | IF a power hold starts and ends during the timer redraw and lasts as long as a normal wake hold, THEN the reader shall wake. | device only — the owner's check |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| board | X4 Pro (R1, R3), X4 (R2) | other boards — same `isHiddenOnDevice` path, risk low |
| redraw delay | 1 min (R3) | 2 and 5 min — same arithmetic, risk low |
| timer wake | — | R4, R5: the simulator has no deep-sleep timer path; device image for the owner |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| C1 smoke | X4 Pro sim: Home → Settings → Экран → «Настройки очисток экрана» → the row «Обновлять заставку» is listed | use-case walk | pass 2026-11-09 17:45 · `qa_runs/c1_display/shots/screen_clean.webp` + screen text «Обновлять заставку \| ВЫКЛ» |
| C2 | X4 sim, card seeded with `"sleepRedrawDelay":2`: boot (settings resave) → file still has `"sleepRedrawDelay":2`; Display settings without the row | decision table (board × saved value) | pass (persistence) 2026-11-09 17:42 · `qa_runs/c2_x4_keep` log «Hardware detect: X4», «Resaving settings», file `"sleepRedrawDelay":2`; the hidden row NOT observed (X4 Home keys open Library) — by code: `isHiddenOnDevice` → `!isX4Pro()` |
| C3 | X4 Pro sim, image redraw = 1 min, a BMP opened from the file browser, wait 75 s → one `Settled image redraw` ≥ 60 s after the paint | boundary (delay) | pass 2026-11-09 17:50 · `qa_runs/c3_bmp_redraw` log: paint 2013 ms, redraw 62 179 ms (+60.2 s), 1 line in 77 s |
| C4 | Device image `x4pro` of `4818dba0` built; owner: sleep with a custom image and 1-min sleep redraw, press and hold power during the redraw → the reader wakes | state transition | [NOT-TESTED] |

## 5. Control cases

| # | Control → expected: the behaviour is absent | Status + evidence |
|---|---|---|
| K1 | C2 on the commit before the fix (`d7cc4e83`): the resaved file loses `sleepRedrawDelay` | red as expected 2026-11-09 17:44 · `qa_runs/k1_x4_drop`: X4, resave, key ABSENT |
| K2 | C3 with image redraw = Off: no `Settled image redraw` in 75 s | pass 2026-11-09 17:52 · `qa_runs/k2_bmp_off`: viewer open 1 966 → ≥ 70 219 ms, 0 lines |

## 6. Verdict

Pending.
