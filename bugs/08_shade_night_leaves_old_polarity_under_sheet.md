# Bug 08 — the shade's night button: pictures under the sheet show as a negative until the shade closes

**Status:** 🔴 OPEN · **Severity:** S2
**Version/build:** KCCP `wip/kccp-1.1.3-debug2` (`07df1501`); upstream `develop` has the same code path (not run there yet)
· **When/context:** 2026-11-17 10:19 +03:00, seen in the bug 07 runs · **Fixing:** later — the owner 2026-11-17 10:21:
«Пофиксить бы, в будущем. Пока как баг заведи и нам и в апстрим»

## Symptom

Night mode switched by the shade's night button while the shade is open over Home (or any screen with pictures): the part
of the screen still visible below the sheet keeps the old polarity, so a picture there (a Home cover, a book picture) shows
as a negative until the shade closes. Text and lines under the sheet look right; only pictures are affected. After the
shade closes, the screen repaints and the picture is positive (with bug 07 fixed).

## Repro (deterministic)

`SD_TEMPLATE=../.tmp/sd_grid_night SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh <name> '0:WAIT:Entering activity: Home;8000:SHOT:before;9000:SWIPE:0.5,0.0,0.5,0.5,300;9000:WAIT:Entering activity: FrontlightPanel;2000:TAP:0.1875,0.3525;4500:SHOT:shade;10000:QUIT' ''`
→ `shade.webp`: the second cover («КАЛИБРОВКА») below the sheet is a negative. Seen in `qa_runs/grid_night_green/shots/shade.webp`
and `qa_runs/grid_night_red/shots/shadeday.webp`. The card recipe: `HOUSE_RULES.md` → «Домашний экран с обложками».

## Root cause (read in the code)

Night mode keeps pictures pre-inverted in the framebuffer, so they stay positive when the panel output is inverted.
`FrontlightPanelActivity::runTile` → `Tile::Night` flips `SETTINGS.screenInverted` and redraws only the sheet; the pixels
of the screen underneath keep the old byte form until that screen repaints. KCCP converts the frame under the sheet only
over the photo viewer (`grayglass::viewerUnderneath` → `renderer.invertScreen()`). Upstream `develop`
`FrontlightPanelActivity.cpp:148–149` flips the setting with no conversion at all.

## Fix plan (later)

Options to weigh when the fix is taken: re-express the visible frame under the sheet for the new polarity (as over the
viewer), or let the screen underneath repaint before the sheet is drawn again. To be decided with the upstream issue's
answer in view.

## Decisions made without the owner

- `[AI]` Severity S2: a transient visual defect, visible while the shade stays open.

## Links

`bugs/07_cover_grid_negative_after_night_switch.md`, `testcases/reports/2026-11-17_bug07_grid_night.md`; upstream issue
#4515 (https://github.com/crosspoint-reader/crosspoint-reader/issues/4515, opened 2026-11-17 10:24 +03:00 on the owner's
«Да, оба одобрено» · «отправляй»; text `qa_runs/pr-discussion-2026-11-17/issue-shade-night-underlay.md`). The issue was
filed from the KCCP observation; it was not reproduced on a clean `develop` build.
