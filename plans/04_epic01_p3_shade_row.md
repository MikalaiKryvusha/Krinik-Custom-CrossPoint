# Plan 04 — epic 01, phase 3: the shade draws its row from the model; «Сон», «Фонарик»; a long tap opens the settings

> **Created:** 2026-11-13 · **Parent:** `plans/01_EPIC_shade_tiles.md` → «Ф3 — шторка» · **Status:** 📐 draft with the
> P3.1 recon, written [NOW] while the Ф2 screen is under its judge; final when Ф2 closes (the ladder rule: phase N+1 is
> planned when phase N closes — the steps below are re-read then) · **Outbound:** —

## Goal vector (Achieve)

The shade shows the buttons the owner picked, in his order, with equal gaps at the edges and between the buttons; two
new buttons, «Сон» and «Фонарик», work from the shade over a book; a long tap on any button opens «Кнопки в шторке» with
the cursor on that button, and Back from there returns to the book page.

Anchor (meta-plan, Ф3): «Ряд кнопок по модели с равными отступами. Кнопки «Сон» и «Фонарик». Иконки: круг с залитой
половиной для ночного режима, полумесяц для «Сна», фонарь. Долгий тап по кнопке открывает экран Ф2.»

## Acceptance criteria (phase; the meta-plan's criteria 1, 2, 4, 5, 6, 7 + the Ф3 gate)

1. WHEN the shade opens, it shall draw the shown buttons that are on, in the stored order, each `kQuickControlSize`
   wide, placed by `shadetiles::tileLeft`, touch slots by `shadetiles::tileSlot`. Check: shots with 5 and 6 buttons in
   landscape and portrait (7 needs Bluetooth — not on the simulator, said aloud; the layout of 7 is the Ф1 host test).
2. WHEN the owner long-taps a button, the shade shall push `ShadeTilesActivity(tile)`; the screen opens portrait with
   the cursor on that button's row. Check: log `Entering activity: ShadeTiles`, the shot (meta-plan criterion 1).
3. WHEN he leaves that screen, the shade shall close behind it and the book page under it shall be on the glass, in the
   book's orientation. Check: the shot after Back = the page the shade was opened over (criterion 4).
4. WHEN «Сон» is checked and moved up four places on the screen, the shade shall show six buttons, «Сон» second.
   Check: the shade shot; `shadeTiles` in `settings.json` (criterion 2).
5. WHEN `settings.json` has no `shadeTiles` (a debug9 card), the shade shall show debug9's five buttons in debug9's
   order (four on the simulator). Check: the shot + log `Shade tiles:` (criterion 5).
6. WHEN he taps «Фонарик» in the shade over a book, the flashlight screen shall open; Back/tap there shall return to the
   book page. Check: log enter/leave, the page shot (criterion 6).
7. WHEN he taps «Сон» in the shade, the reader shall go to sleep with the sleep screen. Check: log, the sleep shot
   (criterion 7).
8. A button the slide switch owns shall still take no TAP, and shall take the LONG tap (meta-plan `[AI]` decision:
   «Долгий тап работает и на кнопке, которую сейчас нельзя переключить тапом»).

## Steps

- [x] P3.1 Recon (2026-11-13, `wip/kccp-1.1.3-debug2` `84c33f85`) — findings below.
- [ ] P3.2 The row from the model: `FrontlightPanelActivity::buildPanelScreen` walks `SETTINGS.shadeTiles` (shown and
      on), places each by `tileLeft`, hits by `tileSlot`; `runTile` dispatches by `shadetiles::Tile`, not by a slot
      index; the night / orientation / touch / Bluetooth drawing stays as it is (filled = on, the orientation glyph
      turned, the Bluetooth-off glyph). Anchor: «Ряд кнопок по модели с равными отступами».
- [ ] P3.3 Icons: night → `icon_half_circle_32` (pasted in Ф2), «Сон» → `icon_moon_32`, «Фонарик» → a lamp (a new 1-bit
      icon by `tools/make_icon.py`, or the Home menu's flashlight glyph if it is a bitmap — look first); the Ф2 screen's
      `tileIcon()` takes the same three. Anchor: «Иконки: круг с залитой половиной…».
- [ ] P3.4 «Сон»: `activityManager.requestSleep()` (the shade's `prepareForSleep` already skips its exit clean).
- [ ] P3.5 «Фонарик»: `FlashlightActivity` gets a «return to the caller» mode — `finish()` instead of
      `goHome(HomeMenuItem::FLASHLIGHT)` (Home keeps its cursor-on-Flashlight return); the shade pushes it with
      `startActivityForResult` and closes itself in the result handler. `[AI]` meta-plan: «Фонарик» opens over the book.
- [ ] P3.6 The long tap: each button's hit takes `InputTouch | InputLongPress`; `event.longPress` → push
      `ShadeTilesActivity(tile)` with a result handler that calls `finish()`. Anchor: «Долгий тап по кнопке открывает
      экран Ф2».
- [ ] P3.7 Judge (fresh agent: the diff + this plan + the meta-plan) BEFORE the build; simulator runs for criteria 1–8;
      run report `testcases/reports/<date>_epic01_p3.md`; cases `testcases/TC_epic01_p3_shade_row.md`.
- [ ] P3.8 Commit; tick Ф3; write the Ф4 plan (judge of the whole epic, the 1.1.3-debug2 image when the owner asks).

## Risks

1. A long press under the shade could also reach the book's own long press (clip selection). Reaction: the shade is the
   current activity and the only one whose `loop()` reads input; the simulator run of criterion 2 reads the log for a
   `ClipSelection` line (must be none).
2. The portrait screen over a landscape book: `ShadeTilesActivity` sets portrait in `onEnter` and restores the caller's
   orientation in `onExit`; the book repaints in its own orientation. Check: the shot of criterion 3.
3. Heap: book + shade + settings screen at once. Reaction: `makeUniqueNoThrow`, the log's free heap after the push.
4. The long-press threshold of the input layer vs «дольше полсекунды» (criterion 1). Reaction: read the threshold in
   `MappedInputManager` / HAL and quote it in the cases.

## P3.1 recon — findings (2026-11-13)

- The row today (`FrontlightPanelActivity.cpp:422-466`): five hard-coded buttons (four without Bluetooth) in equal
  SLOTS `row.width * id / tileCount` — the edge gap is half the inner gap (the epic's goal 3); `runTile(idx)` switches on
  the slot index 0–4; a slide-switch-owned button gets no hit at all (`switchOwned`).
- The model's layout (`src/util/ShadeTiles.h:143-180`): `gapWidth`, `tileLeft` (space-evenly, gaps differ ≤ 1 px),
  `tileSlot` (touch slots meet exactly, the first and the last reach the row's edges).
- Long press in FreeInkUI (`FreeInkUICore.h:302`, `:1013-1027`, `:1351-1355`): a hit registered with `InputLongPress`
  is dispatched on the long-press release with `ActionEvent::longPress = true`; a plain `InputTouch` hit never takes a
  long press (`findTouch`, `:1234-1236`).
- Home «Сон» (`HomeActivity.cpp:349-355`): `requestUpdateAndWait()` then `activityManager.requestSleep()`. Home
  «Фонарик» (`:345-346`): `activityManager.goToFlashlight()` — a REPLACE (`ActivityManager.cpp:303`), the book would
  close; `FlashlightActivity::loop()` leaves by `goHome(HomeMenuItem::FLASHLIGHT)` (`FlashlightActivity.cpp:41-43`).
- Pop (`ActivityManager.cpp:166-211`): the parent's result handler runs, and the parent is repainted only when the
  handler set no action — a handler that calls `finish()` closes the parent with no frame of it in between.
- `GUI.drawHeader` publishes the header back arrow as a tap target (`HeaderBackTapTarget`, cleared on a push,
  `ActivityManager.cpp:228-230`) — the Ф2 screen's header arrow is a Back.
