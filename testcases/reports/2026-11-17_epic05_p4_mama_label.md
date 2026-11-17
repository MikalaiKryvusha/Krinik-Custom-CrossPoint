# Run report — epic 05 Ф4, step P4.7: the mama row reads «Для Мамы» on «Кнопки домашнего экрана»

## 1. Work

Interview #006 → A (the owner, 2026-11-17 10:18 +03:00): on the Settings screen «Кнопки домашнего экрана» of the mama
build the mama row reads «Для Мамы»; Home keeps «Для любимой Мамы». Case H5 of `testcases/TC_epic05_p4_home_buttons_screen.md`,
plan 10 step P4.7. Code: `HomeScreenButtonsActivity::rowName` (`src/activities/settings/HomeScreenButtonsActivity.cpp`).

## 2. Contour

Simulator `simulator_x4_pro_mama_win` (`-DKRINIK_MAMA=1`), card `qa_runs/sd_template` (Lyra, no plugins, no OPDS: 7 rows).
Before: the binary of 2026-11-14 17:29 (`2fa20f3f` code). After: built 2026-11-17 10:33 from `07df1501` + the change.

## 3. Runs

Script H: `0:WAIT:Entering activity: Home;2000:TAP:0.3,0.683;2000:WAIT:Entering activity: SettingsList;1500:TAP:0.3,0.275;1500:WAIT:Entering activity: Settings;2000:TAP:0.5,0.325;2000:WAIT:Entering activity: HomeScreenButtons;2000:SHOT:rows;3000:QUIT`;
every run `SIM_ENV=simulator_x4_pro_mama_win sh tools/sim_run.sh <name> '<script>' ''`.

| # | Moment | Name · binary · script | Exit / outcome |
|---|---|---|---|
| 1 | 2026-11-17 10:27 +03:00 | `mama_label_probe` · before · Home → Settings list (locates «Экран») | 0 errors |
| 2 | 2026-11-17 10:28 +03:00 | `mama_label_before` · before · H | 0 errors |
| 3 | 2026-11-17 10:33 +03:00 | `mama_label_after` · after · H, then three `BACK` and a Home shot | 0 errors; the first `BACK` popped the screen, the next two did not reach Home (the WAIT timed out; the script's key timing, not this change — Home was shot by run 4) |
| 4 | 2026-11-17 10:34 +03:00 | `mama_label_home` · after · `0:WAIT:Entering activity: Home;2000:SWIPE:0.5,0.85,0.5,0.45,60;3500:SHOT:home;4500:QUIT` | 0 errors |

## 4. Checks

- Hygiene: the independent judge (fresh agent, the diff + the owner's answer) — «OK TO BUILD», no findings on the code;
  the mama simulator build SUCCESS (00:02:46); host suite `sh tools/host_tests.sh` — see `.tmp/host_tests_mama_label.log`
  and the commit message.
- Functional run: the mama simulator, Home → Настройки → Экран → «Кнопки домашнего экрана», the shot READ; Home shot READ.

| Case | Status | Observation |
|---|---|---|
| H5 (control: before) | fail as expected | `mama_label_before/shots/rows.webp`: «Для любимой Ма…» |
| H5 (after) | pass | `mama_label_after/shots/rows.webp`: 7 rows, the last «Для Мамы» whole before ▲ ▼ and the checkbox |
| Home keeps the full name | pass | `mama_label_home/shots/home.webp`: «Для любимой Мамы» whole as the 7th row |

## 5. Found

none in the change. Script note: `BACK` ×3 at 3 s steps did not walk Settings → Settings list → Home in run 3.

## 6. Traces

`qa_runs/mama_label_probe/`, `qa_runs/mama_label_before/`, `qa_runs/mama_label_after/`, `qa_runs/mama_label_home/`
(log.txt + shots); `.tmp/build_mama_label.log`.

## 7. Verdict

pass on the simulator. Not verified on the mama reader (no mama image; the image is built on the owner's word).
