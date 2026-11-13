# Krinik Custom CrossPoint — Internal architecture map

> **The INTERNAL map: the project's logical architecture** — the abstraction objects the project's sphere
> works in, their essence, and how they interact. Where `PROJECT_STRUCTURE_EXTERNAL_MAP.md` says *where
> things live*, this says *how the system thinks*. A fresh session reads this to understand the model, not
> just the file layout.
>
> **Adapt the abstractions to the sphere:**
> - *Programming* — modules, interfaces, objects, data structures, data flows, state, protocols.
> - *Science* — hypotheses, variables, models, datasets, methods, inference chains.
> - *Sociology* — subjects, objects, institutions, roles, the relations between them.
> - *Business* — actors, processes, value flows, resources, constraints.
> - …and so on for any sphere. If unsure, describe the domain's nouns and the verbs that connect them.
>
> **Living reference — never DONE-tagged.**

---

## The core abstractions

| Abstraction | What it *is* (essence) | Responsibility |
|-------------|------------------------|----------------|
| **Upstream CrossPoint** | `crosspoint-reader/crosspoint-reader`, branch `develop` | the base KCCP builds on and gives back to |
| **The fork** | `MikalaiKryvusha/crosspoint-reader` (+ `freeink-sdk`) | carries `pr/*` branches for upstream PRs; KCCP lines (`nikolai`, `release/*`, `wip/*`) are moving out |
| **KCCP build** | a firmware image from a fork branch (`x4pro-krinik[-debug]`) | what the owner's and his mother's X4 Pro readers run |
| **Debug line** | `wip/krinik-debugN` (debug2–10), since 2026-11-13 the KCCP 1.1.3 line `wip/kccp-1.1.3-debugN` (debug10 + release 1.1.2 merged; the code map in `STATUS.md`) | features tested on the reader before a release; the owner 13.11: 1.1.3 is the next release |
| **Upstream PR** | one `pr/<topic>` branch + body + before/after frames | moves a feature proven on the reader into CrossPoint |
| **Reader setup** | `restore.mjs` + `settings.json` + fonts + guide EPUBs | reproduces the owner's reader state |
| **Panel curve** | `panel_curve.txt` from KEINKT Calibrator | maps gray levels to how the e-ink panel really shows them |
| **Evidence** | `qa_runs/<run>/` | proves what a build or a PR does (logs, shots, measurements) |
| **Own test books** | `tools/make_image_test_epub.py` → `qa_runs/sd_book_images/image_test.epub` (JPEG + PNG pictures with «Рис. N» captions, `--figure` for the standard markup) | the simulator stand for book pictures (ideas 02/03); third-party books never enter the repo |

## How they interact

```
upstream develop ──fork──▶ pr/* ──PR (owner proofreads text)──▶ upstream review ──merge──▶ upstream develop
        │
        └──▶ KCCP branches ──pio run──▶ image ──SD card──▶ X4 Pro (owner tests) ──proven──▶ pr/* candidate
                                         │
                                         └──▶ firmware-builds/ + GitHub release (this repo)
KEINKT Calibrator ──phone photos──▶ panel_curve.txt ──card──▶ KCCP draws pictures / sleep screens through it
simulator (tools/sim_run.sh) ──shots + log──▶ qa_runs/ ──▶ PR frames, regression checks
```

## Firmware code the PR work touches (in `firmware/`, not this repo)

- `src/main.cpp` — boot `setup()` (wake cause, X4 Pro timer-redraw wake) and `enterDeepSleep()` (sleep screen via
  `ActivityManager::goToSleep()`, then the redraw timer is armed from `SleepActivity::lastCustomImagePath()`).
- `src/activities/boot_sleep/SleepActivity.cpp` — draws the sleep screen; records the custom image path for the
  delayed redraw (#4376) and repaints it on the timer wake (`redrawCustomImage`).
- `lib/Epub/Epub/parsers/ChapterHtmlSlimParser.cpp` — expat XHTML → text blocks → pages; queues anchor ids and
  places them on pages (#4328); a malformed chapter is a parse error, `finishParse()` closes the last page.
- `src/activities/reader/EpubReaderActivity.{h,cpp}` — the EPUB reader (the header holds the shown page's state:
  `currentPageLinks`, `currentPageFootnotes`, the overlay state): `loop()` routes input in priority order (overlay →
  long press = clip selection → Home-button actions → link tap (`currentPageLinks`, beats the zones) → centre tap = menu →
  Back → side taps / swipes / buttons = page turn); the page render keeps the current page's links for hit-testing.
- `src/activities/util/BmpViewerActivity.cpp` — the file browser's full-screen image viewer (BMP/JPEG/PNG through the
  panel curve, cache `/.crosspoint/view_*.bmp`, siblings of the folder, long tap rotates); opened by
  `ActivityManager::goToReader` for an image file (replace), and since debug9 pushed over the book reader for a tapped
  book picture (idea 02). The picture is painted in `drawOrientation()` (the reading orientation set in Settings +
  long-tap turns) and the renderer STAYS there, so every touch — swipes, side taps, Back, the long-tap halves (idea
  07: right half clockwise, left counterclockwise) and the shade opened over it — is read as the picture stands
  upright (the owner, 13.11.2026: «как смотришь на картинку, так и управляешь»; since debug10). The physical keys keep the
  reading orientation (`MappedInputManager::setKeysFollowReadingOrientation`, set in the viewer's onEnter, cleared in
  onExit): a short press pages the pictures, a long press turns the picture.
- `src/activities/ActivityManager.{h,cpp}` — one current activity + a stack: `startActivityForResult` PUSHES (the parent
  stays alive, no `onExit`), `finish()` POPS (the parent's result handler runs, then the parent is repainted);
  `goTo*` REPLACES and clears the stack (`onExit` for all). The shade is PUSHED over whatever is in front (`loop()`, the
  top-edge swipe or a status-bar tap), so the book stays alive under it. A result handler that itself calls `finish()`
  pops the parent too, WITHOUT repainting it (`ActivityManager.cpp` ~205: `requestUpdate()` only when no action is
  pending) — the shade can close right behind a screen it pushed with no shade frame in between (epic 01 Ф3). Pop with
  an empty stack goes Home. `GUI.drawHeader` registers the header's back arrow as a tap target (`HeaderBackTapTarget`,
  cleared on a push). `goToFlashlight()` REPLACES (the book closes) and `FlashlightActivity` leaves by `goHome()`.
- `src/activities/util/FrontlightPanelActivity.{h,cpp}` — the shade (control center; the header holds its one-shot
  close flags `themeApplying` · `refreshTileUsed` · `goingToSleep`): grabber, brightness / warmth sliders,
  the button row (since 1.1.3-debug2 `261e5c63`, epic 01 Ф3): the buttons of `SETTINGS.shadeTiles` that are on and shown,
  in the owner's order, placed by `shadetiles::tileLeft` (equal gaps), hit value = the `Tile`; «Сон» requests sleep,
  «Фонарик» pushes `FlashlightActivity(returnToCaller)`; a long tap (only for a contact that began on the row) pushes
  `ShadeTilesActivity(tile)` and the shade closes when it returns. The simulator is built without Bluetooth
  (`FREEINK_CAP_BLE_HID_HOST` off → `bleturner::status().compiledIn` false), so there the default row has four buttons.
- `src/MappedInputManager.{h,cpp}` — logical buttons and screen gestures over `HalGPIO`: maps the physical keys by the
  live renderer orientation (or, while `keysFollowReadingOrientation` is set by the image viewer, by the reading
  orientation), taps / swipes / long presses in logical coordinates; `wasScreenLongPress` CONSUMES the long press and
  suppresses the rest of the contact.
- `src/activities/util/FlashlightActivity.{h,cpp}` — Home «Фонарик»: a white page, the light at full output, any tap /
  Back leaves (Home, cursor on «Фонарик»); with `returnToCaller` (epic 01 Ф3, the shade's button) it `finish()`es to
  the screen it was pushed over.
- `src/activities/UiListActivity.cpp` — the base of single-list screens (FreeInkUI `list()`, swipes scroll, keys move
  the selection); `KeyboardLayoutsActivity` is its checkbox-list example (a working mask, saved on exit).
- `src/activities/settings/SettingsActivity.cpp` — one Settings screen per `SettingsSection`: `sectionFor()` routes each
  setting (by its field) to a top-level group or to a Display sub-screen past `End` — «Настройки очисток экрана»,
  «Калибровка экрана», «Настройки сна» (debug10, idea 08); `addAction` rows open the sub-screens. The groups and the
  sub-screens past `End` are the enum `SettingsSection` (`SettingsSection.h`).
- `src/activities/settings/ShadeTilesActivity.{h,cpp}` (1.1.3-debug2 `41718c61`, epic 01 Ф2) — «Кнопки в шторке», the second row of
  «Экран»: one hand-drawn row per tile on `UiAppHost` (icon, name, checkbox, ▲ ▼; theme tokens from
  `Screen::resolveListProps`), edits go straight into `SETTINGS.shadeTiles`, the file is written on exit; portrait while
  open; Back = `finish()`. The Bluetooth row is hidden where Bluetooth is not compiled in (the simulator). Row names are
  the screen's own short strings where the Settings name is too long (`STR_SHADE_TILE_ORIENTATION` «Ориентация»).
  The constructor's `cursorTile` is the phase 3 entry (the long-tapped button).
- `src/util/ShadeTiles.h` (debug10, epic 01) — the shade tile model: seven tiles by string id, on/off and order,
  `parse`/`format` of the `settings.json` string `shadeTiles` ("night,cleanup,…,-sleep"), at least one on, the
  equal-gap row layout and touch slots; host test `test/shade_tiles/`; held by `CrossPointSettings::shadeTiles`.
- `firmware/platformio.local.ini` (ignored) — this PC's native Windows simulator envs (research 01).
- `simulator/src/HalStorage.cpp` — the simulator's SD card over a host folder (`CROSSPOINT_SIM_SD`); `replaceFile`
  mirrors the device's remove-then-rename (a bare `rename` cannot overwrite on Windows, found 2026-11-09).

## Invariants & rules of the model

- A feature reaches upstream only after it works on the real reader (the owner's word on the device).
- At most five open upstream PRs per author; PRs are never closed to free a slot.
- No outward text (PR, issue, review reply) without the owner's proofreading.
- The reader is eFuse-locked: SD card is the only flashing path.
- Debug-only aids never ship in a release image.

## Key decisions embedded in the architecture

- Firmware lives in forks, the workspace in this repo — the fork stays clean for upstream review
  (`[OWNER] 2026-11-08 · STATUS.md → code map`).
- Name: KCCP (Krinik Custom CrossPoint); `krinik-*` tags and image names stay as history
  (`[OWNER] 2026-11-08 · STATUS.md → "Next after Task 0"`).

---

> Keep this in sync with the real logic: when you LEARN how a part works, or see it differ from this map, and
> when you introduce, retire or rewire an abstraction — the line here changes in the same turn. File/directory placement belongs in
> `PROJECT_STRUCTURE_EXTERNAL_MAP.md`.
