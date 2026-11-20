# Run report — bug 16: the gap above the status bar taken from the page's own line gaps

## Work

The case set `testcases/TC_bug16_status_bar_gap_squeeze.md` (written before the run), the owner's verdict of 2026-11-20
10:36 (`interviews/decisions/mockups_1_1_4_2026-11-20.decision.json` p13): no line carried, a squeeze of the shown page's
line spacing; his earlier ask for a minimum-bottom-gap setting.

## Contour

Firmware `wip/kccp-1.1.4` at `48d7d52c` + the uncommitted bug 16 diff (`PageSqueeze.h`, `Page::squeezeBottom`,
`PageLine::glyphBottom/inkBottom`, `Section::loadPage`, `GfxRenderer::getFontDescenderSize`, `UITheme::statusTextRise`,
setting `statusBarGap`); simulator `simulator_x4_pro_win` on `fix/x4pro-viewable-insets` (the device's insets); the П4
stand — the owner's settings (Lyra, Literata 16, «+10 %», landscape) and GEB copy, cards `.tmp/ui_sd_g0/g5/g10` (only
`statusBarGap` differs); the «before» page `.tmp/ui_mock_2026-11-20/d114_2_land/shots/page.webp` (build `48d7d52c`).

## Runs

| # | When | Command | Result |
|---|---|---|---|
| 1 | 2026-11-20 ≈ 11:05 +03:00 | first build + `sim_run.sh b16_g{0,5,10}` | g0 = before; g5/g10 moved 1 px only (the glyph-bottom air gate) |
| 2 | 2026-11-20 ≈ 11:18 +03:00 | build after the ink bottom + status text limit; the same runs | g5/g10 still 1 px (the ink-metric air gate) |
| 3 | 2026-11-20 11:21 +03:00 (shot clock) | build without an air gate (`build_b16c.log` 47 s); `KEEP_BMP=1 SD_TEMPLATE=../.tmp/ui_sd_g$g SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh b16_g$g "0:WAIT:Entering activity: EpubReader;20000:SHOT:page;21000:QUIT"` | see Checks |
| 4 | 2026-11-20 11:25 +03:00 (screen text clock) | `CROSSPOINT_SIM_SCREEN_TEXT=1 … sim_run.sh b16_set3` (book → Back → Home → «Настройки» → «Чтение») | the setting row shown |
| 5 | 2026-11-20 ≈ 11:26 +03:00 | `b16_end_g0` / `b16_end_g5` — the chapter's last page (progress 10/104); `tools/shot_diff.py` | TOTAL 0 |
| 6 | 2026-11-20 ≈ 11:27 +03:00 | `TARGETS="PageSqueezeTest" sh tools/host_tests.sh` with the mutant «no spread» → red ×2; then `sh tools/host_tests.sh` | 5/5 clean; the full suite 995, 10 failed = the known list |

## Checks

Hygiene: PageSqueezeTest 5/5, the mutant «the whole rise at the first gap» red (`TextLinesShareThePixelsEvenly`,
`NoPixelFromAGapNextToAPicture`); the full host suite no new failure; three judges over the diff (the BLOCKER and both
MAJORs of round 1 fixed; rounds 2–3 minors fixed or answered).
Functional run: the simulator on the owner's settings and book by the user's path, the shots READ, rows measured with
`tools/shot_rows.py`:

| Case | Status | Observed |
|---|---|---|
| 1 control G = 0 | pass | `tools/shot_diff.py <before> <g0> 32` (the status bar's clock cut) TOTAL 0 — pixel-identical; 2 px between the last ink (447) and the status text (450) |
| 2 smoke G = 5 | pass | the same 11 lines, the first at y 26; the last ink at 440 → 9 px to the status text; «~25/105» unchanged |
| 3 boundary G = 10 | pass | the same lines; the last ink at 437 → 12 px; each line gap smaller by 0 or 1 px (10 gaps, the cap reached) |
| 4 no-op | pass | the chapter's last page (text ends at 428): G 0 vs 5 pixel-identical, `shot_diff` TOTAL 0 |
| 5 promise | pass | the status bar shows «~25/105» at G 0 and 5 — no re-pagination |
| 6 setting | pass | «Настройки → Чтение»: «Отступ над строкой состояния | 5» (run 4's screen text); the 0…20 steps read in the code, not walked |
| 7 hygiene | pass | run 6 |

## Found

Two defects of my own code, both found by the runs and fixed before the final run:

- the air gate on the parser's glyph bottom (the font's advance) disqualified every gap inside a paragraph (run 1);
- the gap was measured from the text area's bottom while the status text is drawn 4 px above it, and the ink-metric gate
  (ascender + descender > the 37 px pitch of the owner's spacing) again disqualified every gap (run 2) — the gate removed
  (`Page.cpp` comment names the runs), the limit is the status text's top (`UITheme::statusTextRise`, shared with
  `BaseTheme::drawStatusBar`).

## Traces

`qa_runs/b16_g0`, `b16_g5`, `b16_g10`, `b16_end_g0`, `b16_end_g5`, `b16_set`, `b16_set2`, `b16_set3` (parked to `.tmp/` after
this report — the book's text); `.tmp/mock/out2/gap_squeeze.webp`; build logs `.tmp/mock/build_b16*.log`; host logs in
`.tmp/host_tests_*.log`.

## Verdict

pass — no line is carried, the gap grows with the setting up to the page's line-gap budget, G 0 is today's page. Not
verified on the reader: the e-ink look of the 1 px tighter line gaps — with the 1.1.4-debug2 image; the default is the owner's
pick 12 (2026-11-20 11:39, firmware 8a8b44bc).
