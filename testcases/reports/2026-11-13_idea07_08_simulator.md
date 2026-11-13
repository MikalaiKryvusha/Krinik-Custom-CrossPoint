# Test run report — idea 07 second set (every touch follows the picture) and idea 08 («Настройки сна»), simulator

**Created:** 2026-11-13 15:56 +03:00 · **Run by:** the agent (Claude, KCCP session) · **Version/build:** firmware `wip/krinik-debug10`
(= `551173b8` + the uncommitted ideas 07/08 diff after five judge passes), simulator `simulator_x4_pro_win`, MSYS2 from
`F:\ai_sandbox\msys64`

## 1. Work

- Idea 07, cases C6–C9 of `testcases/TC_idea07_viewer_rotation_by_half.md` (section 6): after a turn the viewer reads
  every touch in the picture's orientation — the long-tap halves of the picture, the Back swipe.
- Idea 08, step S3 of `ideas/08_sleep_settings_submenu.md`: «Экран» shows «Настройки сна» first and none of the nine
  sleep options; «Настройки сна» shows the nine in the code order; Back returns to «Экран».

## 2. Contour

The native Windows simulator, X4 Pro profile. Idea 07: card `qa_runs/sd_book_images` (landscape CCW = the owner's
`orientation: 3`, the test book with the orientation triangle). Idea 08: card `qa_runs/sd_template` (boots to Home,
portrait settings). Device not involved — no `REAL WORLD:` claim.

## 3. Runs

| # | Moment | Name · script | Exit / outcome |
|---|---|---|---|
| 1 | 2026-11-13 15:55 +03:00 | `idea07_c6_c9` · `3000:TAP:0.5,0.40;3000:WAIT:Entering activity: BmpViewer;1500:SHOT:v0;2000:TAP:0.75,0.5,800;2000:WAIT:View turns;1500:SHOT:c6;2500:TAP:0.75,0.5,800;2500:WAIT:View turns;1500:SHOT:c7;2500:TAP:0.25,0.5,800;2500:WAIT:View turns;1500:SHOT:c8;2500:SWIPE:0.05,0.5,0.6,0.5,300;2500:WAIT:Popped;1500:SHOT:c9;3000:QUIT` | 0 · 0 errors |
| 2 | 2026-11-13 15:56 +03:00 | `idea08_s3` · `0:WAIT:Entering activity: Home;1500:TAP:0.3,0.68;1500:WAIT:Entering activity: SettingsList;1500:TAP:0.3,0.275;1500:WAIT:Entering activity: Settings;1500:SHOT:display;2000:TAP:0.3,0.17;2000:WAIT:Entering activity: Settings;1500:SHOT:sleep;2500:SWIPE:0.05,0.5,0.6,0.5,300;2500:WAIT:Popped;1500:SHOT:back;3000:QUIT` | 0 · 0 errors |

All runs: `SIM_ENV=simulator_x4_pro_win [SD_TEMPLATE=…] sh tools/sim_run.sh <name> '<script>' ''`.

## 4. Checks

Hygiene: simulator build SUCCESS, no warnings in the touched files; five read-only judge passes (idea 08: no blockers;
the viewer and its keys / touch-hold fix: two shapes refused with blockers, the third shape no blockers — `ideas/07`).
Functional run: both scripts walked the user's path; every WebP shot and the log lines were READ.

| Case | Status | Observation |
|---|---|---|
| C6 | pass | right long tap → log `long tap at x=599 of 800 (right half)`, `View turns: 1`; shot `c6` is PORTRAIT with the picture upright, triangle top-left — the viewer stays in the picture's orientation |
| C7 | pass | long tap at (0.75, 0.5) of the new frame → log `x=359 of 480 (right half)`, `View turns: 2` — the halves are the picture's; shot `c7` landscape, picture upright |
| C8 | pass | long tap at (0.25, 0.5) → log `x=199 of 800 (left half) -> rotate counterclockwise`, `View turns: 1` |
| C9 | pass | Back swipe from the left edge of the turned frame → `Popped from activity stack`; shot `c9` = book page 1/8; log `page repainted 15 ms after the picture closed` |
| 08-S3 «Экран» | pass | shot `display`: «Настройки сна» first row; «Плавная подсветка», «Скрыть % батареи», «Тема интерфейса», «Ночной режим», «Настройки очисток экрана», «Калибровка экрана»; no sleep option |
| 08-S3 «Настройки сна» | pass | shot `sleep`: «Экран сна», «Сон через», «Режим обложки сна», «Порядок обложек сна», «Ориентация заставки сна», «Подсветка на засыпании», «Фильтр экрана сна», «Возобновление по таймауту», «Подсветка при пробуждении» |
| 08-S3 Back | pass | swipe Back → `Popped`, shot `back` = «Экран» |

NOT run, said aloud:
- The book's touch hold after a TURNED picture (the second fast swipe): the simulator repaints in 15 ms, no second swipe
  can land in the window — the reader's check (homework), the log line `page repainted N ms` gives the device time.
- The keys in the viewer: the book picture has no siblings to page to, and what the keys should do there (page or
  rotate) is the owner's open question (asked 15:22).
- 08: changing «Сон через» on the sub-screen and reading `settings.json` (the value code is unchanged; the routing is
  what changed).

## 5. Found

- None in the change on the simulator.

## 6. Traces

`qa_runs/idea07_c6_c9/`, `qa_runs/idea08_s3/` — `log.txt` + `shots/*.webp`.

## 7. Verdict

partial — every case run passes; the touch hold after a turned picture and the keys wait for the reader and the
owner's answer.
