# Plan 11 — epic 05, phase 5: the long tap on a Home button opens «Кнопки домашнего экрана»

> **Created:** 2026-11-17 · **Parent:** `plans/05_EPIC_home_buttons.md` → «Ф5 — вход долгим тапом» (criteria 7, 8, 9) ·
> **Status:** ⏸ planned 2026-11-17 10:40 +03:00, parked 10:42 for epic 07 (the owner's repeated caption decision comes
> first); no code yet — resume at P5.1 (`UiAppHost::routeTouch` read: with `withLongPress` it calls `wasScreenLongPress`,
> which consumes the contact) · **Outbound:** —

## Goal vector (Achieve)

The owner reaches the setting of a Home button from the button itself: holding a Home button longer than 0.5 s opens
«Кнопки домашнего экрана» with the cursor on that button's row (interview #004, Q4 → A); a short tap keeps doing what it
does today; Back returns to Home, which shows the edited order at once.

Anchor (meta-plan, Ф5): «Долгий тап по кнопке домашнего экрана открывает экран «Кнопки домашнего экрана» с курсором на
строке этой кнопки; короткий тап работает как сейчас.» Gate: «критерии 7, 8, 9 на симуляторе в каждой теме; судья без
блокеров».

## Acceptance criteria (phase)

1. **Long tap** (meta criterion 7). WHEN the owner holds «Фонарик» on Home for 800 ms, the firmware shall open
   «Кнопки домашнего экрана» with the cursor on «Фонарик» — in all five themes. Check: `Entering activity:
   HomeScreenButtons` in the log; a shot with the «Фонарик» row selected.
2. **Short tap** (criterion 8). WHEN the owner taps «Фонарик» briefly, the firmware shall open the flashlight, in all
   five themes. Check: `Entering activity: Flashlight`.
3. **Back to Home** (criterion 9). WHEN the screen was opened by a long tap and «Сон» was moved up one row, Back shall
   show Home with «Сон» one button higher. Check: a Home shot after Back (Lyra and the cover grid at least; all five if cheap).
4. **No side action on the release.** WHEN the owner long-taps «Сон», the reader shall NOT go to sleep (the release is
   swallowed). Check: no sleep line in the log; the screen opens.
5. **Covers unchanged.** WHEN the owner holds a recent-book cover (list themes), the book shall open as today. Check:
   `Entering activity: EpubReader`.
6. **Mama build.** The long tap on «Для любимой Мамы» opens the screen with the cursor on «Для Мамы». Check: shot.

## Design (from reading the code, 2026-11-17)

- **List themes** (`HomeActivity::loop`, `rowTouch` at ~604): a long press is claimed only for a contact that BEGAN on a
  drawn button row — the shade's pattern (`FrontlightPanelActivity::loop`, `contactOnTiles`): on the press frame
  (`wasScreenTouchPressed`) record whether the point is inside the drawn rows; while that flag holds, call
  `mappedInput.wasScreenLongPress(x, y)` BEFORE the cover and row touch checks (EXP-0016: one contact, several
  consumers). `wasScreenLongPress` consumes the contact (`suppressTouchContact`), so the release cannot also activate the
  button (criterion 4). A contact that began on a cover never calls it (criterion 5).
- **Cover grid** (`CoverGridHomeUi`): the tab bar's `inputMask` gains `fui::InputLongPress`; `selectedAction` routes with
  `withLongPress` for a contact that began on the tab bar; `onAction` keeps `event.longPress`; a new accessor returns the
  long-tapped tab. Read `UiAppHost::routeTouch` first: whether it consumes the SDK long press (the shade relies on it).
- **Opening:** `startActivityForResult(HomeScreenButtonsActivity(renderer, mappedInput, button), handler)` — a PUSH, so
  Home stays alive and Back (`finish()`) returns to it. `HomeScreenButtonsActivity` already takes `cursorButton` (Ф4).
- **Return:** the handler re-reads `shownButtons = homemenu::visible(SETTINGS.homeButtons, homeLibrarySlotExists())`
  (the Ф2 judge's note: only `onEnter` sets it today), hands the list to `CoverGridHomeUi` (a `setButtons`, or `begin`
  again — decide after reading), puts the selection on the same button (or the first if it was switched off), clamps
  `menuTopRow`, `keepSelectionVisible()`, `requestUpdate()`.

## Steps

- [ ] P5.1 Read `UiAppHost::routeTouch` and `MappedInputManager::wasScreenTouchPressed` once more; write the claim rule
      into the code comment. Anchor: «Долгий тап по кнопке домашнего экрана открывает экран…».
- [ ] P5.2 List themes: the contact flag + the long-press claim + `openButtonSettings(button)`.
- [ ] P5.3 Cover grid: the long-press mask on the tabs + the accessor; Home calls the same `openButtonSettings`.
- [ ] P5.4 The return handler (refresh, selection, grid tabs). Anchor: «Назад» на домашний экран (criterion 9).
- [ ] P5.5 The judge BEFORE the build; fix findings.
- [ ] P5.6 Builds: `simulator_x4_pro_win`, `simulator_x4_pro_mama_win`; host suite (`sh tools/host_tests.sh`).
- [ ] P5.7 Case set `testcases/TC_epic05_p5_home_long_tap.md` (criteria 1–6 × themes, control K1 on the old binary: a long
      tap on «Фонарик» opens the flashlight on the release); runs (the long tap in a script: `TAP:x,y,800`); run report.
- [ ] P5.8 Commit; map lines (`HomeActivity`, `CoverGridHomeUi`); tick Ф5 in the meta-plan; the Ф6 plan waits for the
      owner's word on the image.

## Risks

1. **The long press and the row's own 90 ms selection** — the row is highlighted before the long press fires; harmless
   (the screen covers Home), named so a shot showing it is not read as a defect.
2. **The cover grid's tab bar may not forward the long press** through `routeTouch` the way the shade's tiles do — P5.1
   reads it before coding; fallback: the list-theme pattern (contact flag + `wasScreenLongPress`) over the tab rect.
3. **Home repaint after the pop** — `ActivityManager` repaints the parent after its handler unless the handler
   `finish()`es; the handler only refreshes state. Checked by the Back shot (criterion 3).
4. **Orientation** — `ToggleRowsActivity` forces portrait while open and restores on exit; Home is portrait: no change
   expected; a landscape Home is outside this phase.

## Decisions made without the owner

- `[AI]` The long press is claimed only for a contact that began on a button (the shade's rule), so a long hold on a
  cover keeps opening the book.
- `[AI]` 800 ms in the scripts: above the SDK's `TOUCH_LONG_PRESS_MS = 500`
  (`freeink-sdk/libs/hardware/InputManager/include/InputManager.h:536`) with margin; the firmware threshold is the SDK's
  500 ms = the owner's 0.5 s (interview #004, Q4 → A).
