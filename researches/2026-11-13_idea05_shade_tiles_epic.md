# Research — epic 01: configurable shade tiles (idea 05) — industry practice, local recon, requirements

> **Created:** 2026-11-13 · **Parent:** `ideas/05_shade_quick_actions_settings.md` (design agreed, go-ahead 2026-11-13
> 13:28 +03:00) · **Status:** 🔬 rung 1 of `/plan-epic` done 2026-11-13 14:37 +03:00 · **Outbound:** the meta-plan
> `plans/01_EPIC_shade_tiles.md`

## 1. Industry sweep (web, 2026-11-13)

| # | Practice | Source | What it says |
|---|---|---|---|
| I1 | Tile order stored as ONE ordered list of stable string ids | AOSP `Settings.Secure.QS_TILES` = `"sysui_qs_tiles"`, read by `QSTileHost.TILES_SETTING` (commit in an AOSP fork: https://gitlab.e.foundation/e/os/android_frameworks_base/-/commit/9813cb61dd07e7d59f88a554d9a05c5b779fa8d8) | "a comma separated list of ordering of QS tiles"; the default list is a resource (`quick_settings_tiles_default`) of short specs (wifi, bt, dnd, flashlight); tiles a build lacks are filtered out of the default |
| I2 | A minimum number of tiles in the editor | AOSP SystemUI resource `quick_settings_min_num_tiles` (default 6), checked by the tile editor before a removal (commits in the same fork, e.g. https://gitlab.e.foundation/e/os/android_frameworks_base/-/commit/ea2d2267bee388c0977c0423bd2cf8c679293d0d) | the editor refuses to remove a tile below the minimum and says so ("at least N tiles") |
| I3 | A long press on a quick tile opens ITS settings screen | Android developer guide, QR-code payment tile: https://developer.android.com/develop/ui/views/quicksettings-tiles/qr-code ; `TileService.ACTION_QS_TILE_PREFERENCES` | by default a long press opens the app info; an activity with `ACTION_QS_TILE_PREFERENCES` makes it open the tile's preferences — the same shape as the owner's «лонг-тап из шторки сразу ведёт внутрь настроек» |
| I4 | Reordering needs a single-pointer alternative to drag: move-up / move-down buttons | W3C WCAG 2.2 SC 2.5.7 Dragging Movements: https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements ; failure F108: https://www.w3.org/WAI/WCAG20/Techniques/failures/F108 | a reorderable list with no single-pointer way to reorder fails; up/down buttons are a valid alternative — exactly the ▲▼ the owner chose (an e-ink panel cannot follow a drag anyway) |
| I5 | Equal gaps between items AND at the edges = `space-evenly` | MDN `justify-content`: https://developer.mozilla.org/docs/CSS/justify-content (CSS Box Alignment Level 3) | `space-evenly`: every gap, edges included, is the same; `space-around` gives edges HALF the inner gap — the defect the owner saw in today's shade |
| I6 | The "appearance / dark mode" glyph is a circle with one half filled | Apple Developer Forums (community answer, not Apple's word): https://developer.apple.com/forums/thread/706624 → SF Symbol `circle.lefthalf.filled`; Flutter `CupertinoIcons.circle_lefthalf_fill`: https://api.flutter.dev/flutter/cupertino/CupertinoIcons/circle_lefthalf_fill-constant.html | the owner's «круг чёрный и белый по половине»; Lucide `contrast` (MIT, already in the SDK's icon source tree) is the same shape |

Anti-patterns the sources name or imply:
- storing positions as enum indices (an enum reorder or a new tile silently scrambles saved orders) — I1 stores ids;
- a reorder that only works by dragging (I4);
- `space-around`-style slots for a centred row (I5) — today's `row.width * id / tileCount`.

## 2. Local recon (re-read 2026-11-13 ≈14:35 on `wip/krinik-debug10` `9f02db5f`; the subagent map `researches/2026-11-13_idea05_06_code_map.md` confirmed line by line where cited here)

- **Shade** `src/activities/util/FrontlightPanelActivity.{h,cpp}`: `kTileCount = 5` (`.h:40`); tiles drawn in equal
  SLOTS `row.x + row.width * id / tileCount` with the tile centred in its slot (`.cpp:437-442`) — the edge gap is half
  the inner gap (I5's `space-around`); the Bluetooth tile is dropped when not compiled in (`.cpp:423`); tiles 0 and 3
  take no tap while the slide switch owns them (`.cpp:462-463`); actions in `runTile(idx)` (`.cpp:165-224`), indices
  hard-wired to the drawing order.
- **Input caps:** `FreeInkApp<24, 6>` (`src/components/UiAppHost.h:29`): 24 hit targets, 6 handlers; the shade
  registers 6 handlers already (`.cpp:81-86`) → a long-tap handler must REUSE `ACTION_TILE` and branch on the event's
  long-press flag. An overflowing hit target is dropped SILENTLY (`InteractionBuffer::addInteraction`,
  `FreeInkUICore.h:1050-1060`, sets `overflowed_`). Touches today: `routeTouch(mappedInput, false, …)` (`.cpp:271`) —
  long press off.
- **Settings entry:** `ActivityManager::goToSettings(section)` REPLACES the activity (`ActivityManager.cpp:307-309`),
  so the book under the shade is closed; a Display sub-screen is reopened through `pendingSettingsSubSection`
  (`SettingsSection.h`, cleared by goHome `ActivityManager.cpp:377`); sub-screens sit past `End` in the enum
  (`ScreenClean`, `ScreenCalibration`). Back to the BOOK has no route today.
- **Persistence:** `/.crosspoint/settings.json`; hand-saved fields beside the generic `uint8_t` loop, e.g.
  `keyboardLayouts` written only when set (`CrossPointSettings.cpp:119-120`) and read if present (`:307-308`).
- **Nearest list screen:** `src/activities/settings/KeyboardLayoutsActivity.cpp` (80 lines, checkbox rows, a working
  copy saved on exit). No screen reorders items today.
- **Flashlight:** `goToFlashlight()` replaces the activity (`ActivityManager.cpp:302`) — from the shade it would close
  the book; the tile must open it over the book and return there.
- **Orientation:** the shade is drawn in the READING orientation (the owner: landscape, 800 wide); Settings screens are
  portrait (`qa_runs/idea05_settings_look`).
- **Lessons:** EXP-0015 / EXP-0009 (simulator scripts: WAIT with its time, times rising inside a segment — now a guard
  in `tools/sim_run.sh`); EXP-0014 (a launched window is not a shown window — look before saying it is open).

## 3. Requirements (the owner's words — verbatim in `ideas/05`)

- Entry: «3 Долгий тап по любой плитке» (12:23); «пусть лонг-тап из шторки сразу ведёт внутрь настроек на
  соответствующий экран» (12:25).
- Screen: «А Список с галочками и стрелками» (12:24); «в прошивке квадратики» (13:19) — the firmware checkbox.
- Row: «отступы нужно будет пересчитывать для разного числа плиток … с равными отступами между ними и по краям» (13:00).
- Icons: «для переключателя темы нужно нарисовать новую кнопку, как в iOS - круг черный и белый по половине» ·
  «Сон - будет полумесяц» (13:24).
- Set: seven tiles — night mode, screen cleanup, orientation, touch, Bluetooth, Sleep, Flashlight («да, гоу, делаем» ·
  «фонарик тоже - опция шторки», 13:28).
- `[AI]` defaults said to him (12:57, not contested): Back from «Плитки шторки» returns to the book; the screen is also in
  «Настройки → Экран»; the cursor stands on the long-tapped tile.
- Fit: `GOAL.md` success 1 (the reader runs a KCCP build he checked); `MASTER_PLAN.md` phase 2 (KCCP 1.1.3 features).

## 4. Findings → implications for epic 01

1. **Storage (I1):** one JSON value `shadeTiles` in `settings.json` — the ordered list of ALL known tile ids as stable
   strings, each with its on/off; absent → today's five on in today's order + Sleep, Flashlight off at the end; an
   unknown id is dropped; a known id missing from a saved list is appended OFF (a future tile never changes the
   owner's row by itself — I1's "available" area). The parser is a pure function with a host test.
   `FORK: options <ordered string ids | enum-index array | per-tile uint8 fields> · price of error <saved orders
   scrambled by a firmware update> · consulted <AOSP sysui_qs_tiles (I1)>` → ordered string ids.
2. **Layout (I5):** gap = (row width − n × tile) / (n + 1), tile i at row.x + gap × (i + 1) + tile × i; the touch
   target of a tile spans to the midpoints of its gaps (the outer ones to the row edge). A pure function with a host
   test over n = 1…7 in both widths (landscape 800, portrait 480): every gap within 1 px of the others.
3. **Minimum (I2):** `[AI]` at least ONE tile stays on — the last checkbox cannot be cleared (one line of text says why);
   with zero tiles the long-tap entry would vanish. Cheap to reverse; said to the owner.
4. **Long tap (I3):** reuse `ACTION_TILE`, branch on the long-press flag; `routeTouch(…, true, …)`; the slide-switch-owned
   tiles still accept the long tap (it edits the row, not the function). Risk: a finger resting 500 ms on a SLIDER must
   not count — sliders keep their own route.
5. **Reorder (I4):** ▲▼ per row; 7 rows × 3 targets = 21 of the 24-target cap — counted, with a guard that the screen
   never registers more than it can (the silent overflow).
6. **Return to the book:** a pending "return to reader" flag set before `goToSettings`, consumed by the Settings Back
   (`goToReader(openEpubPath)`), cleared by goHome — the same shape as `pendingSettingsSubSection`.
7. **Flashlight / Sleep tiles:** Flashlight pushed over the reader and finished back to it (not `goToFlashlight`'s
   replace); Sleep closes the shade and calls the existing `requestSleep()` path.
8. **Icons:** half-filled circle for night mode (I6, Lucide `contrast` mirrored + filled), crescent for Sleep
   (`icon_moon_filled_32` exists), flashlight from Lucide; drawn as 1-bit `freeink::Icon` with Pillow (no `rsvg-convert`
   on this PC).

## 5. Open forks for the owner

- None blocking. The `[AI]` choices above (minimum one tile; a new future tile appears OFF; the long tap also works on a
  slide-switch-owned tile) are reversible and go into the meta-plan's «Решения без владельца».
- Idea 06 (Home buttons) reuses the list screen of phase 2 — planned as its own epic after this one closes.
