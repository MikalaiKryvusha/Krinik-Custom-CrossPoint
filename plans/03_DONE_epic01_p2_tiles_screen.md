# Plan 03 — epic 01, phase 2: the settings screen «Кнопки в шторке»

> **Created:** 2026-11-13 · **Parent:** `plans/01_EPIC_shade_tiles.md` → «Ф2 — экран «Кнопки в шторке»» · **Status:** 📐
> planned 2026-11-13 15:58 +03:00; P2.1 recon done; P2.2–P2.5 written 2026-11-13 16:57 +03:00, reworked to the mockup by
> 17:19; moved to `wip/kccp-1.1.3-debug2` 19:06; P2.6 judge 19:21 — no blockers (findings below); next P2.7 build +
> simulator; ✅ phase closed 2026-11-13 19:33 +03:00 — firmware `41718c61`, simulator C1–C8 pass
> (`testcases/reports/2026-11-13_epic01_p2.md`), host suite 773/781 = the 8 known · **Outbound:** —

## Goal vector (Achieve)

The owner edits the shade's row on one screen: which of the seven tiles are on and in what order. Phase 1 gave the model
(`src/util/ShadeTiles.h`, `CrossPointSettings::shadeTiles`); phase 2 gives the screen and its two entries; phase 3 will
draw the shade from the model and open this screen by a long tap.

Anchor (meta-plan, Ф2): «Список из семи строк: иконка, имя, квадратик прошивки, ▲ ▼. Книжная ориентация. Курсор на
строке плитки, по которой был долгий тап. Пункт в «Настройки → Экран». «Назад» возвращает в книгу, если экран открыт из
шторки, и в «Настройки → Экран», если экран открыт из настроек. Новые строки интерфейса на русском и английском.»

## Acceptance criteria (phase)

1. WHEN the owner opens «Настройки → Экран → Кнопки в шторке», the screen shall list the tiles in the stored order, each
   row with its name, the firmware square checkbox (filled = on) and ▲ ▼. Check: simulator shot, rows read.
2. WHEN he taps a row's checkbox, the tile shall turn on / off; the last tile on shall not turn off and the row shall
   say why. Check: simulator taps + shots.
3. WHEN he taps ▲ (▼) on a row, the row shall move one place up (down); ▲ on the first and ▼ on the last do nothing.
   Check: simulator taps + shots.
4. WHEN he leaves the screen, `settings.json` shall hold the new `shadeTiles` string (only if it differs from the default).
   Check: the file read after the run.
5. WHEN the screen was opened from Settings, Back shall return to «Экран»; WHEN opened by the entry phase 3 will call
   (the shade pushes `ShadeTilesActivity(tile)`), the cursor shall stand on that tile's row and Back shall return to the
   book. Check: the Settings half on the simulator in phase 2; the shade half with phase 3's long tap — the book page shot
   after Back.
6. The screen shall register at most 24 hit targets (the FreeInkApp cap drops overflow silently). Check: a
   `static_assert` on the count + the shot (all ▲ ▼ react).

## Steps

- [x] P2.1 Recon (read, cite): `UiListActivity` (rows, `ListItem.icon`, `setCheckboxRow`, `syncListViewport`, extra
      hits after `screen.list()` — later hits win), the hit cap, `KeyboardLayoutsActivity` (working copy, locked row,
      save on exit), idea 08's sub-screen wiring (`SettingsSection` past `End`, `addAction`), how Settings returns to the
      reader (`pendingSettingsSubSection`, `goToReader`). Anchor: «Список из семи строк…».
- [x] P2.2 Icons ▲ ▼ (1-bit `freeink::Icon`, Pillow script `tools/` → `src/components/icons/customListIcons.h`, the
      header's recipe); the tile icons of the rows: the shade's current ones (phase 3 replaces night / Sleep / Flashlight).
      Done 2026-11-13 16:50: `icon_tri_up_32`, `icon_tri_down_32` and `icon_half_circle_32` (the night tile's planned icon,
      so the night row and the «Сон» row do not both show a moon) pasted, shapes read as ASCII art.
- [x] P2.3 `ShadeTilesActivity` (on `UiAppHost` — the P2.1 findings below; NOT `UiListActivity`), written 2026-11-13
      16:55, judge pending. Deviations from this line, `[AI]`: no working copy — edits go straight into
      `SETTINGS.shadeTiles` (a shade opened over the screen shows them), the file is written on exit when the row was
      EDITED during the visit (a flag, not a comparison: a shade opened in between may have saved an intermediate row —
      judge 2026-11-13 19:21); the key itself is written only while the row differs from the default; the last-tile rule counts the SHOWN rows (a hidden Bluetooth tile that is on does not keep
      the shade alive); ▲ ▼ step over a hidden row. Rows drawn with `Screen::resolveListProps` tokens (the Settings list
      look); `[NOT-TESTED]`.
- [x] P2.4 Entries, written 2026-11-13 16:55: `SettingAction::ShadeTiles`, the row second in «Экран» right under «Настройки
      сна» (`[AI]` placement; touch boards only — a buttons-only board has no tile row). Changed `[AI]`: NO
      `SettingsSection::ShadeTiles` (the screen is its own activity, as `KeyboardLayoutsActivity`) and NO
      `goToShadeTiles(tile, fromBook)` — the shade is PUSHED over the book (`ActivityManager::loop`), so phase 3 lets the
      shade push this screen with the long-tapped tile and close itself when the screen returns; the book is never
      reopened (risk 3 gone). The screen's Back is `finish()` in both cases.
- [x] P2.5 Strings (en, ru), written 2026-11-13 16:57: `STR_SHADE_TILES` «Кнопки в шторке», `STR_SHADE_TILE_CLEANUP`
      «Очистка экрана», `STR_SHADE_TILES_NOTE` — one note above the rows (the Settings sub-screen pattern) that says the
      checked tiles stand in the shade in this order and one tile always stays on, with the reason (the long tap).
- [x] P2.6 Judge (fresh agent, the diff + this plan + the meta-plan + the mockup + the cases) BEFORE the build,
      2026-11-13 19:21 +03:00: VERIFIED WITH CAVEATS, no blockers; every identifier resolves; the stale-frame guard
      cannot lock the screen; seven rows fit (434 px of ~500). Fixed: the cases C1/C4/C8/R4/R5 and P2.3 now follow the
      code and the mockup (arrows on every row; save by the edit flag); clang-format 21 over the Ф2 files (the icon
      arrays were 815-char lines). Left as nits: a dropped tap still repaints; ▲ on row 1 does not move the cursor;
      «Bluetooth Page Turner» may be cut with an ellipsis on the device (look on the reader). To Ф3 (plan 04 risks):
      keys over the image viewer, a second copy of this screen from a shade over it.
- [x] P2.7 Build; simulator: criteria 1–5; `settings.json` read; run report `testcases/reports/2026-11-13_epic01_p2.md`:
      C1–C8 pass; found and fixed in the phase: «Ориентация чтения» cut with an ellipsis → the mockup's «Ориентация»
      (`STR_SHADE_TILE_ORIENTATION`, judged, re-run); a `tools/sim_run.sh` gap (in-script SHOT names) fixed in KCCP.
- [x] P2.8 Commit (firmware `41718c61`, 19:33); Ф2 ticked in the meta-plan; the phase 3 plan is `plans/04_epic01_p3_shade_row.md`.

## Risks

1. The 24-target cap: 7 rows + 14 arrows = 21 (the header back is `HeaderBackTapTarget`, outside the app's table).
   Reaction: `static_assert`; every row registers both arrows (the mockup), a dead arrow does nothing and does not
   fall through to the row.
2. A portrait list of 7 rows plus a note may not fit 800 px with the theme's row height. Reaction: the list scrolls
   (`syncListViewport`); the shot shows it.
3. ~~The return-to-book route crosses `goToSettings`'s replace (the book is closed). Reaction: reopen the book by
   `APP_STATE.openEpubPath`.~~ Gone 2026-11-13 16:52: the shade is pushed over the book (`ActivityManager::loop`), so the
   screen opened from the shade is pushed too and the book stays alive under both (P2.4).

## P2.1 recon — findings (2026-11-13, `wip/krinik-debug10` `8538f3dd`)

- `screen.list()` (FreeInkUI `components/lists/list.h`) lays the rows out inside itself and exposes no row rects and no
  custom trailing slot (only `value` / `toggle` / a swipe-reveal action); `UiListActivity`'s own comment: «Screens that
  are not a single list (sliders, tab layouts, state machines) should NOT derive from this — they use UiAppHost
  directly». A row with its own ▲ ▼ targets is such a screen → `ShadeTilesActivity` on `UiAppHost` (the shade's
  pattern: `screen.takeTop()` per row, `screen.frame().hit(rect, action, value, InputTouch)` per element).
- The firmware checkbox (`list.h:855-864`, `toggleCheckbox`): `stroke(box, fg, 2, 2)`, and when on `fill(box.inset(size/4),
  fg, 2)`, `size = min(togW, togH) - 6` — drawn the same way by hand.
- No arrow icons exist (`src/components/icons/`: only download / upload) → ▲ ▼ as 1-bit icons (P2.2).
- Handlers: `FreeInkApp<24, 6>` — ≤ 6 `app.on` actions (row toggle, up, down, back… — one action with the value
  encoding row × kind keeps it at 1–2); ≤ 24 hits: 7 rows × 3 = 21 + the header back.
- Keys on this screen: `KeyboardLayoutsActivity` reads buttons in `loop()` (Up/Down move the selection, Confirm toggles);
  for this screen: Up/Down select a row, Confirm toggles; moving a row by keys — an open detail, said in the report.

## Decisions made without the owner

Every call below is `[AI]` and reversible; listed at the phase closing 2026-11-13 19:33 +03:00.
- The screen is built on `UiAppHost`, not `UiListActivity` (P2.1: FreeInkUI `list()` has no slot for a row's own ▲ ▼).
- No working copy: edits go straight into `SETTINGS.shadeTiles`; the file is saved on exit after ANY edit (a flag, so an
  intermediate row a shade saved in between is overwritten); the key is written only while the row is not the default.
- The last-on rule counts the SHOWN rows (a hidden Bluetooth that is on does not keep the shade alive).
- ▲ ▼ step over a hidden row; ▲ on row 1 and ▼ on the last row do nothing and do not fall through to the checkbox.
- The row is the second of «Экран», right under «Настройки сна»; touch boards only.
- One note above the rows (the Settings sub-screen pattern) says what the checkboxes and arrows do and why one button
  stays on — the mockup has no note; the epic's rule asks for «строка текста поясняет почему».
- Moving a row by keys is not built (Up/Down move the cursor, Confirm checks); said here as an open detail.
- English on-device strings say "buttons" ("Control Center Buttons"), following the owner's Russian rename of 17:06.
- The orientation row is named «Ориентация» / "Orientation" (the mockup's word) by its own string.
- A tap on a frame that does not show the last move yet is dropped (the second of two fast ▲ waits for the frame).
