# Plan 09 — epic 05, phase 3: the Home button list scrolls

> **Created:** 2026-11-14 · **Parent:** `plans/05_EPIC_home_buttons.md` → «Ф3 — скролл списка кнопок» · **Status:**
> ✅ phase closed 2026-11-14 17:05 +03:00 — firmware `a47582b0`; simulator S1–S7, S6b, S6c pass in the plain and the mama build, five
> themes, 0 `Outside range` (baseline 452) (`testcases/reports/2026-11-14_epic05_p3.md`); host suite 795/803 (the 8 known);
> judge: VERIFIED WITH CAVEATS, no blockers · in work since 2026-11-14 16:27 +03:00 · **Outbound:** —

## Goal vector (Achieve)

In the mama build with plugins (8 buttons) Lyra fits 7, and «Для любимой Мамы» is cut off and unreachable by touch.
After this phase the button list of every list theme scrolls when the buttons do not fit; the book cover stays put.

Anchor (meta-plan, Ф3): «Список кнопок скроллится во всех темах, когда кнопки не помещаются; обложка текущей книги вне
скролла. Скролл устроен как в списках настроек прошивки: свайп листает список кнопок постранично, физические кнопки
читалки двигают курсор, список идёт за курсором (`UiListActivity.cpp:177-189`).» The owner (interview #004, Q5):
«Пока помещаются кнопки - скролл не нужен. как только пункты не помещаются - появляется возможность скролить ИМЕННО
список кнопок, обложка текущей книги не скролится».

## Decisions at the forks

- `FORK: scroll unit <one row | a page of rows> · price of error: a step per row costs an e-ink redraw per row and
  differs from every other list on the reader · consulted: the firmware's own lists — UiListActivity.cpp:177-189 (a swipe
  scrolls by inputPageRows, the selection stays), the meta-plan's [AI] decision` → a page of rows.
- `FORK: overflow cue <scroll bar | partial trailing row | both | none> · price of error: the mother does not know more
  buttons exist · consulted: FreeInkUI list.h:153 (scrollIndicator = true by default in every Settings list),
  RoundedRaffTheme.cpp drawScrollBar (RoundedRaff already pages Home with this bar)` → a scroll bar in RoundedRaff's
  look (thumb only, theme metrics scrollBarWidth / scrollBarRightOffset), whole rows only.
- `FORK: where the swipe starts <anywhere on Home | over the button list> · price of error: a swipe on the cover would
  scroll the list · consulted: owner, Q5 «ИМЕННО список кнопок, обложка … вне scroll view»` → over the button list
  (start Y ≥ the menu top); a swipe that starts elsewhere keeps today's behaviour (moves the selection).

## Acceptance criteria (phase)

1. **Mama build overflow** (meta-plan criterion 4). WHILE the mama build, Lyra, plugins on (8 buttons, 7 fit), WHEN a
   swipe up starts on the button list, THEN the list shows buttons 2–8 with «Для любимой Мамы» whole, the cover region
   is pixel-identical before and after, a scroll bar is drawn. Check: two shots, a crop compare of the cover band.
2. **Fits → no scroll** (meta-plan criterion 5). WHILE 6 buttons on Lyra, WHEN a swipe up starts on the list, THEN the
   screen does not change. Check: two shots, 0 px ≥ 40 levels apart below the status bar.
3. **Tap after scroll.** WHEN the list is scrolled by one row, a tap on the last visible row opens «Для любимой Мамы»
   (`Entering activity: Mama`). Check: log.
4. **Keys follow.** WHEN the physical Down key walks the selection to the 8th button, the list scrolls to keep it
   visible. Check: shot.
5. **Return below the fold.** WHEN Home is entered with the cursor on «Для любимой Мамы» (back from Mama), the list is
   scrolled so the row is visible and selected. Check: shot.
6. **Other themes.** Lyra Extended (plain build with plugins: 7 buttons, 6 fit), Classic and RoundedRaff in the mama
   build with plugins scroll the same way; the cover grid needs no scroll (8 icons fit one bar). Check: shots.

## Steps

- [x] P3.1 `simulator_x4_pro_mama_win` in `firmware/platformio.local.ini` (extends `simulator_x4_pro_win`,
      `-DKRINIK_MAMA=1`); build it; boot smoke. Anchor: meta-plan Ф3 gate «в маминой и обычной сборке». Built on
      `f9ae704b` 2026-11-14 16:31 (`[SUCCESS] Took 176.89 seconds` — the first mama build of Ф1–Ф2). Baseline run
      `qa_runs/epic05_p3_before` (Lyra, plugins on): 7 rows drawn, «Для любимой Мамы» off the screen, the log holds 452
      `[ERR] [GFX] !! Outside range (x, 813…820)` lines — the 8th row drawn below 800 px. After Ф3 that count is 0.
- [x] P3.2 `HomeActivity`: `menuTopRow` (the first visible menu row) and `visibleMenuRows()` from the real bottom
      (the content area, minus the hint band only where hints are drawn — never on a touch board); render the slice
      [top, top + visible), touch rows offset by top, keep the selection visible on key moves and on enter; a swipe
      that starts on the list scrolls by a page (clamped), the selection stays; the scroll bar when rows > visible.
      Anchor: «свайп листает список кнопок постранично … список идёт за курсором».
- [x] P3.3 Judge BEFORE the build; fix findings.
- [x] P3.4 Host suite; simulator: criteria 1–6 by `testcases/TC_epic05_p3_home_scroll.md`; run report.
- [x] P3.5 Commit, tick Ф3 in the meta-plan and MASTER_PLAN phase 2 (the mama menu task), write the Ф4 plan.

## Risks

1. **RoundedRaff pages inside its own drawButtonMenu** by the selected index. Handing it a slice of ≤ one page keeps its
   own paging off; its «Продолжить чтение» row is part of the menu rows and scrolls with them.
2. **The rect the themes get is miscomputed** (its height counts from the screen top; Lyra ignores it). The visible
   count is computed from the content area, not from that rect.
3. **Upstream drift** — the change stays inside `HomeActivity`.

## Decisions made without the owner

- `[AI]` The three forks above (a page of rows; a thumb scroll bar, whole rows only; the swipe must start on the list),
  each with its `FORK:` line and source.
- `[AI]` The judge's finding 2 (take `verticalSpacing` off the row count for Classic's row-0 offset) was applied and then
  REVERTED by measurement: the X4 Pro content bottom is 797 (log «Menu geometry»), so the change cost Lyra its 7th row
  (6.98 → 6). On the X4 Pro Classic's 7th row still ends at 795 ≤ 797; another panel geometry is outside the project's
  scope (`GOAL.md`, boundaries). Recorded in the code comment of `visibleMenuRows()`.
- `[AI]` A swipe that starts on the cover keeps the old meaning (moves the selection) — the minimal change; the list
  swipe is the only new gesture.
- `[AI]` A permanent `LOG_DBG` «Menu geometry» line on entry — the measurement for future runs; absent from the device
  debug build (`LOG_LEVEL=1`).
- PENDING settled: none were opened.
