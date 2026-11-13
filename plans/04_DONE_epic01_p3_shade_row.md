# Plan 04 — epic 01, phase 3: the shade draws its row from the model; «Сон», «Фонарик»; a long tap opens the settings

> **Created:** 2026-11-13 · **Parent:** `plans/01_EPIC_shade_tiles.md` → «Ф3 — шторка» · **Status:** 📐 draft with the
> P3.1 recon, written ≈ 2026-11-13 19:10 +03:00 (committed 19:12) while the Ф2 screen was under its judge; final when Ф2 closes (the ladder rule: phase N+1 is
> planned when phase N closes — the steps below are re-read then); ✅ phase closed 2026-11-13 20:05 +03:00 — firmware
> `261e5c63`, simulator D1–D8 pass (`testcases/reports/2026-11-13_epic01_p3.md`) · **Outbound:** —

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
- [x] P3.2 The row from the model: `FrontlightPanelActivity::buildPanelScreen` walks `SETTINGS.shadeTiles` (shown and
      on), places each by `tileLeft`, hits by `tileSlot`; `runTile` dispatches by `shadetiles::Tile`, not by a slot
      index; the night / orientation / touch / Bluetooth drawing stays as it is (filled = on, the orientation glyph
      turned, the Bluetooth-off glyph). Anchor: «Ряд кнопок по модели с равными отступами».
- [x] P3.3 Icons: night → `icon_half_circle_32` (pasted in Ф2), «Сон» → `icon_moon_32`, «Фонарик» → the Home menu's lamp,
      `FlashlightIcon` (`src/components/icons/flashlight.h`, 32×32, 128 bytes, the 1-bit format of `freeink::Icon`:
      read as ASCII 2026-11-13 — a lamp lying with its beam and rays to the LEFT, «stored rotated 90° CCW»): wrapped as
      `freeink::Icon{32, 32, 16, FlashlightIcon}` and drawn with `fui::Rotation::CW90` so the beam points up — the shot
      confirms; the Ф2 screen's `tileIcon()` takes the same three. Anchor: «Иконки: круг с залитой половиной…».
- [x] P3.4 «Сон»: `activityManager.requestSleep()` (the shade's `prepareForSleep` already skips its exit clean).
- [x] P3.5 «Фонарик»: `FlashlightActivity` gets a «return to the caller» mode — `finish()` instead of
      `goHome(HomeMenuItem::FLASHLIGHT)` (Home keeps its cursor-on-Flashlight return); the shade pushes it with
      `startActivityForResult` and closes itself in the result handler. `[AI]` meta-plan: «Фонарик» opens over the book.
- [x] P3.6 The long tap: each button's hit takes `InputTouch | InputLongPress`; `event.longPress` → push
      `ShadeTilesActivity(tile)` with a result handler that calls `finish()`. Anchor: «Долгий тап по кнопке открывает
      экран Ф2».
- [x] P3.7 Judge (fresh agent: the diff + this plan + the meta-plan) BEFORE the build — 19:52, no blockers; simulator runs for criteria 1–8;
      run report `testcases/reports/<date>_epic01_p3.md`; cases `testcases/TC_epic01_p3_shade_row.md`.
- [x] P3.8 Commit (`261e5c63`); Ф3 ticked. The Ф4 plan is written when the owner asks for the image (19:01 «со
      сборкой не торопись»): the whole-epic judge, the device build, the smoke on the image's commit, the homework.

## Risks

1. A long press under the shade could also reach the book's own long press (clip selection). Reaction: the shade is the
   current activity and the only one whose `loop()` reads input; the simulator run of criterion 2 reads the log for a
   `ClipSelection` line (must be none).
2. The portrait screen over a landscape book: `ShadeTilesActivity` sets portrait in `onEnter` and restores the caller's
   orientation in `onExit`; the book repaints in its own orientation. Check: the shot of criterion 3.
3. Heap: book + shade + settings screen at once. Reaction: `makeUniqueNoThrow`, the log's free heap after the push.
4. ~~The long-press threshold of the input layer vs «дольше полсекунды»~~ — closed by the recon: 500 ms (below).
5. The shade over the IMAGE VIEWER (the Ф2 judge, 19:21): the viewer keeps `setKeysFollowReadingOrientation(true)`
   while it lives, so on «Кнопки в шторке» pushed from that shade the keys would follow `SETTINGS.orientation`, not the
   portrait screen. Reaction: the screen clears the flag in `onEnter` and puts the previous value back in `onExit` (a
   getter in `MappedInputManager` if none exists); a simulator case opens the screen from a shade over a picture.
6. A shade opened OVER «Кнопки в шторке» (the top-edge swipe works there) and a long tap in it would push a second copy
   of the screen. Reaction: the shade does not take the long tap when the screen below it is «Кнопки в шторке» (or the
   long tap closes the shade only) — decided in P3.6, with a case.

## P3.1 recon — findings (2026-11-13)

- The row today (`FrontlightPanelActivity.cpp:422-466`): five hard-coded buttons (four without Bluetooth) in equal
  SLOTS `row.width * id / tileCount` — the edge gap is half the inner gap (the epic's goal 3); `runTile(idx)` switches on
  the slot index 0–4; a slide-switch-owned button gets no hit at all (`switchOwned`).
- The model's layout (`src/util/ShadeTiles.h:143-180`): `gapWidth`, `tileLeft` (space-evenly, gaps differ ≤ 1 px),
  `tileSlot` (touch slots meet exactly, the first and the last reach the row's edges).
- Long press in FreeInkUI (`FreeInkUICore.h:302`, `:1013-1027`, `:1351-1355`): a hit registered with `InputLongPress`
  is dispatched with `ActionEvent::longPress = true` the moment the long press fires, the finger still DOWN (the app's
  `touchSnapshotFrom`, `src/components/UiAppHelpers.h:174-192`, delivers it as a released+longPress snapshot and the
  rest of the contact is suppressed, so the lift cannot also tap); a plain `InputTouch` hit never takes a
  long press (`findTouch`, `:1234-1236`).
- Home «Сон» (`HomeActivity.cpp:349-355`): `requestUpdateAndWait()` then `activityManager.requestSleep()`. Home
  «Фонарик» (`:345-346`): `activityManager.goToFlashlight()` — a REPLACE (`ActivityManager.cpp:303`), the book would
  close; `FlashlightActivity::loop()` leaves by `goHome(HomeMenuItem::FLASHLIGHT)` (`FlashlightActivity.cpp:41-43`).
- Pop (`ActivityManager.cpp:166-211`): the parent's result handler runs, and the parent is repainted only when the
  handler set no action — a handler that calls `finish()` closes the parent with no frame of it in between.
- The long-press threshold (risk 4, closed): `InputManager::TOUCH_LONG_PRESS_MS = 500`
  (`freeink-sdk/libs/hardware/InputManager/include/InputManager.h:536`) — the meta-plan's «дольше полсекунды»; it fires
  once per contact while the finger is down, and the screen reacts at that moment (see the line above; corrected 19:24 —
  an earlier line here said «on the release»). `UiAppHost::routeTouch(input,
  withLongPress, routeHeld)` forwards it only with `withLongPress = true`; the shade calls `routeTouch(mappedInput,
  false, /*routeHeld=*/true)` today (`FrontlightPanelActivity.cpp:271`) — P3.6 sets the first flag.
- `GUI.drawHeader` publishes the header back arrow as a tap target (`HeaderBackTapTarget`, cleared on a push,
  `ActivityManager.cpp:228-230`) — the Ф2 screen's header arrow is a Back.

## Decisions made without the owner

Every call below is `[AI]` and reversible; listed at the phase closing 2026-11-13 20:05 +03:00.
- The long press is taken only for a contact that began on the button row (a resting finger on a slider keeps
  dragging) — the slider half is not run on the simulator; the owner's reader shows it.
- A long tap from a shade lying over «Кнопки в шторке» only closes the shade (no second copy of the screen).
- «Фонарик» from the shade: pushed over the screen below in a return-to-caller mode; Home's «Фонарик» unchanged. A
  flashlight opened over the Home flashlight (Home → «Фонарик» → shade → «Фонарик») returns the first one at the
  normal brightness instead of full (the judge, rare) — left as is.
- «Сон» from the shade: the Home sleep call as it is (no selection paint first: the button is not a list row).
- The lamp: the Home menu's bitmap, turned CW90 (no new drawing); the night button: the half-filled circle.
- The settings screen takes the keys off the reading orientation while open and puts the caller's value back.
- Not changed: the shared sleep log line says «from the home menu» also for the shade's «Сон» (a nit in `main.cpp`).
