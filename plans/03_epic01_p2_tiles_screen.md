# Plan 03 — epic 01, phase 2: the settings screen «Плитки шторки»

> **Created:** 2026-11-13 · **Parent:** `plans/01_EPIC_shade_tiles.md` → «Ф2 — экран «Плитки шторки»» · **Status:** 📐
> planned 2026-11-13 15:58 +03:00; P2.1 recon done, P2.2 icon tool `tools/make_icon.py` done (icons not pasted yet); next P2.3 · **Outbound:** —

## Goal vector (Achieve)

The owner edits the shade's row on one screen: which of the seven tiles are on and in what order. Phase 1 gave the model
(`src/util/ShadeTiles.h`, `CrossPointSettings::shadeTiles`); phase 2 gives the screen and its two entries; phase 3 will
draw the shade from the model and open this screen by a long tap.

Anchor (meta-plan, Ф2): «Список из семи строк: иконка, имя, квадратик прошивки, ▲ ▼. Книжная ориентация. Курсор на
строке плитки, по которой был долгий тап. Пункт в «Настройки → Экран». «Назад» возвращает в книгу, если экран открыт из
шторки, и в «Настройки → Экран», если экран открыт из настроек. Новые строки интерфейса на русском и английском.»

## Acceptance criteria (phase)

1. WHEN the owner opens «Настройки → Экран → Плитки шторки», the screen shall list the tiles in the stored order, each
   row with its name, the firmware square checkbox (filled = on) and ▲ ▼. Check: simulator shot, rows read.
2. WHEN he taps a row's checkbox, the tile shall turn on / off; the last tile on shall not turn off and the row shall
   say why. Check: simulator taps + shots.
3. WHEN he taps ▲ (▼) on a row, the row shall move one place up (down); ▲ on the first and ▼ on the last do nothing.
   Check: simulator taps + shots.
4. WHEN he leaves the screen, `settings.json` shall hold the new `shadeTiles` string (only if it differs from the default).
   Check: the file read after the run.
5. WHEN the screen was opened from Settings, Back shall return to «Экран»; WHEN opened by the entry phase 3 will call
   (`goToShadeTiles(tile, fromBook)`), the cursor shall stand on that tile's row and Back shall return to the book.
   Check: a simulator run through a debug entry (or phase 3's long tap) — the book page shot after Back.
6. The screen shall register at most 24 hit targets (the FreeInkApp cap drops overflow silently). Check: a
   `static_assert` on the count + the shot (all ▲ ▼ react).

## Steps

- [x] P2.1 Recon (read, cite): `UiListActivity` (rows, `ListItem.icon`, `setCheckboxRow`, `syncListViewport`, extra
      hits after `screen.list()` — later hits win), the hit cap, `KeyboardLayoutsActivity` (working copy, locked row,
      save on exit), idea 08's sub-screen wiring (`SettingsSection` past `End`, `addAction`), how Settings returns to the
      reader (`pendingSettingsSubSection`, `goToReader`). Anchor: «Список из семи строк…».
- [ ] P2.2 Icons ▲ ▼ (1-bit `freeink::Icon`, Pillow script `tools/` → `src/components/icons/customListIcons.h`, the
      header's recipe); the tile icons of the rows: the shade's current ones (phase 3 replaces night / Sleep / Flashlight).
- [ ] P2.3 `ShadeTilesActivity` (on `UiAppHost` — the P2.1 findings below; NOT `UiListActivity`): a working copy of `SETTINGS.shadeTiles`; rows from
      `shadetiles::List` (Bluetooth row only when compiled in — the model keeps it); checkbox via `canTurnOff`; ▲ ▼ via
      `moveUp/moveDown`; save on exit when edited; `[NOT-TESTED]`.
- [ ] P2.4 Entries: `SettingsSection::ShadeTiles` + an action row in «Экран» (after «Настройки сна»? — order said in the
      report); `ActivityManager::goToShadeTiles(tile, fromBook)` with a pending return-to-book flag (cleared by goHome).
- [ ] P2.5 Strings (en, ru): «Плитки шторки», «Очистка экрана» (the tile name), the last-tile note; the rest exist.
- [ ] P2.6 Judge (fresh agent, the diff + this plan + the meta-plan) BEFORE the build; fix findings.
- [ ] P2.7 Build; simulator: criteria 1–5; `settings.json` read; run report `testcases/reports/<date>_epic01_p2.md`.
- [ ] P2.8 Commit; tick Ф2; write the phase 3 plan.

## Risks

1. The 24-target cap: 7 rows + 14 arrows + the header back = 22. Reaction: `static_assert`, and the arrows of a row
   whose move is impossible register no hit (fewer targets).
2. A portrait list of 7 rows plus a note may not fit 800 px with the theme's row height. Reaction: the list scrolls
   (`syncListViewport`); the shot shows it.
3. The return-to-book route crosses `goToSettings`'s replace (the book is closed). Reaction: reopen the book by
   `APP_STATE.openEpubPath` — the same path the reader uses at boot; the page restores from its progress file.

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
