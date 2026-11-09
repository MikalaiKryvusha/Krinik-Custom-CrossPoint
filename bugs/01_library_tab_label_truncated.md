# Bug 01 — Library: the "Recent" tab label is cut to «Недав...» in Russian

**Status:** 🔧 fix committed `d2b45c0e` on `pr/library-tab-fit`, smoke case pass; control cases pending · **Severity:** S2
(flagged by the owner) · **Fixing:** this session
**Version/build:** upstream CrossPoint `develop` f8db833f (also our `pr/screen-redraw-delay`); native Windows simulator
`simulator_x4_pro_win`, Lyra theme, Russian UI · **When/context:** 2026-11-09 16:55 +03:00, found by the owner in the
simulator window while the agent ran the CodeRabbit checks.
**Owner's word:** `[OWNER] 2026-11-09 16:55 +03:00 · chat: «вот такое обрезание - баг. мне не нравится. ЧИнить.» · «и ПР
будет на исправление это в апстриме»` (with a crop of the screen showing «Недав... ▾»).

## Goal vector and acceptance

Avoid: a tab label that fits the screen is never shortened with "...".
- Situation: Russian UI, Library open, the "Recent" tab selected with its sort arrow.
- Action: the agent opens Library in the simulator.
- Result: the first tab reads «Недавние ▾» in full; «Название» and «Автор» stay where they were.
- Check: `sh tools/sim_run.sh tab_fit_after …` → `qa_runs/tab_fit_after/shots/library.webp` shows «Недавние ▾».

## Repro

`SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh tab_fit_before '0:WAIT:Entering activity: Home;300:DOWN;300:ENTER;0:WAIT:Entering activity: Library;3000:QUIT' '2600:library'`
→ the tab bar reads «Недав... ▾ | Название | Автор».

## Root cause

`LibraryListActivity` sets `tabPillMaxPad = 16` ("three short tab labels"): `UiTabListActivity::buildTabBar()` puts
16 px of `contentInset` on each side of every pill. The pill is the equal-width slot minus `tabInset`, and the text
area is the pill minus 2 × 16 px. «Недавние» plus the sort indicator (gap 4 + 6 px) is wider than that area, so
FreeInkUI's `tabBar` elides the label. English «Recent» fits, so the bug shows only with longer translations.

## Fix plan

In `buildTabBar()`, cap the pad at half of the room the widest tab content leaves in its pill (label width +
indicator gap + indicator), floor 0: the label is never cut while the pill can hold it, the slots do not move, and
short labels keep the 16 px pad. Upstream PR from `pr/library-tab-fit` (cut from `upstream/develop` f8db833f); the
five-open-PR limit means it waits in the queue for a slot.

## Fix log

- 2026-11-09 17:18 red: `upstream/develop` f8db833f built (`simulator_x4_pro_win`), run `qa_runs/tab_fit_before` →
  `shots/library.webp` reads «Недав... ▾ | Название | Автор».
- 2026-11-09 17:21 green: `d2b45c0e` built, run `qa_runs/tab_fit_after` → `shots/library.webp` reads «Недавние ▾ |
  Название | Автор», the other two tabs in place.
- Still to run (after the KUMM quiet window): English UI — «Recent» keeps the 16 px pad (pill looks as before);
  selection down in the list (unfocused tab style); Settings tabs (`tabPillMaxPad = 0`, path unchanged).
- TWINS: searched `tabPillMaxPad` in `src/` — set only in `LibraryListActivity` (16); every other `UiTabListActivity`
  keeps 0 and does not enter the changed block.

## Owner's decisions

- The sort arrow stays: `[OWNER] 2026-11-09 17:31 +03:00 · chat + question «Убираем её совсем?» → «Оставить как есть»`,
  after the agent said it shows the sort direction (▾ descending, ▴ ascending; `LibraryListActivity::tabIndicator`);
  earlier words «и стрелка эта вниз слева нахуй не нужна» · «справа вернее» · «ааааа, понял».
- English control 2026-11-09 17:29: `upstream/develop` vs `d2b45c0e`, English UI, Library — BMPs differ only in
  (57,14)–(65,26), the clock digit; everything from y = 40 down (the tab bar included) is pixel-identical.

- To run, owner's word `[OWNER] 2026-11-09 17:50 +03:00 · chat: «и во всех бы темах проверить, не только Lyra»`:
  the Library tab bar in every UI theme (`uiTheme` values of the build), Russian, before/after.
- Hole, named: the only other `UiTabListActivity` is `TextSettingsActivity` (Settings → Reading → text settings and
  the reader menu); it keeps `tabPillMaxPad = 0`, so the changed block (`if (tabPillMaxPad > 0 …)`) is not entered —
  proved by the code gate, not observed on screen (a scripted walk there timed out: `WAIT:…Settings` also matches
  `SettingsList`). The unfocused tab state (selection in the list) needs a card with books — not run.

## Decisions made without the owner

- `[AI]` Fix in the firmware (`UiTabListActivity`), not in the FreeInkUI SDK: the cap is a CrossPoint choice, and a
  CrossPoint PR is what the owner asked for.

## Links

- `testcases/` run reports of this session; `researches/2026-11-09_native_windows_simulator.md` (the stand).
