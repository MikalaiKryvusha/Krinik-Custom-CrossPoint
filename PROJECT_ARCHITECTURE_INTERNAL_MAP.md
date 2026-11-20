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
- `lib/Epub/Epub/parsers/ChapterHtmlSlimParser.cpp` — expat XHTML → text blocks → pages, streaming (a picture is placed
  before the parser sees its caption); queues anchor ids and places them on pages (#4328); a malformed chapter is a parse
  error, `finishParse()` closes the last page. Page breaks: `addLineToPage` breaks when a line overflows and
  `breakPageCarryingLines` moves the page's trailing elements (orphan/widow lines, a heading kept with what follows) to
  the next page through the carry ring (`recentLineOffsets` / anchors, 6 entries, `canCarry`). Epic 07 Ф1 (1.1.3-debug2,
  in work): a `<figure>` or a block with CSS `break-inside: avoid` is a keep-together group — its first picture enters the
  ring, a caption line that overflows carries the picture along, and a group that opens its page and still overflows
  shrinks the picture (`shrinkGroupImageFor`, floor = viewport / 4); `figcaption` is a block. Anchors (the state is in
  `ChapterHtmlSlimParser.h`): a block's id → `pendingAnchorId` → `unplacedAnchorIds`, placed with the block's first
  content (`aeee710b`); an inline id → `inlineAnchorIds` by visible offset; a `<span>` id is dropped (upstream #2303,
  KePub heap guard) unless no visible text comes before the next block — then `spanAnchorCandidates` join that block's
  anchors (bug 09, 1.1.3-debug4); all under `MAX_ANCHORS_PER_CHAPTER` = 1024 (`anchorCount()`). Host tests:
  `test/chapter_html_slim_parser/ChapterHtmlSlimParserTest.cpp` (since 2026-11-17 it builds on Windows; three of its tests
  fail only here — Windows cannot delete an open file).
- `lib/Epub/Epub/blocks/BlockStyle.h` — a block's resolved style (`fromCssStyle`; `getCombinedBlockStyle` accumulates
  the stack on the Horizontal axis, the Vertical one merges into a reused empty block). Headings (KCCP 1.1.4, bugs 14/15):
  `keepWithNext` — h1–h6 and any block with CSS `break-after: avoid` (`CssStyle::breakAfterAvoid`, wire byte 2) keep their
  lines with what follows; `keepContentWithNext` — `break-after` + `break-inside: avoid` together (GEB's
  `<div class="title3"><p>`) make every inner block kept; `ParsedText::resolveFirstLineIndent` gives a kept block no
  reader's indent (a hanging CSS indent stays).
- `src/activities/reader/EpubReaderActivity.{h,cpp}` — the EPUB reader (the header holds the shown page's state:
  `currentPageLinks`, `currentPageFootnotes`, the overlay state): `loop()` routes input in priority order (overlay →
  long press = clip selection → Home-button actions → link tap (`currentPageLinks`, beats the zones) → centre tap = menu →
  Back → side taps / swipes / buttons = page turn); the page render keeps the current page's links for hit-testing.
- `lib/Epub/Epub/Page.{h,cpp}` — one laid-out page from the section cache: `elements` (PageLine — `yPos` = the top of
  the line box, the line ends at yPos + lineHeight; PageImage; PageDropCap — yPos = the last spanned line's baseline;
  PageBorderBox — yPos + height), page-relative `links` and `footnotes`; `Section::loadPage` is the one door every
  reader path loads a page through (render, clip selection, the next-page prefetch). `Page.cpp` holds the element
  (de)serialization, the render paths and (KCCP 1.1.4, bug 16) `Page::squeezeBottom` — the gap above the status bar
  taken from the shown page's line gaps (`PageSqueeze.h`, setting `statusBarGap`); `PageLine::glyphBottom` is the
  parser's clamp formula, `PageLine::inkBottom` the real ink bottom.
- `lib/Epub/Epub/converters/` — the picture decoders behind `ImageToFramebufferDecoder` (JPEG — JPEGDEC 8-bit gray, coarse
  1/2..1/8 DCT scale then a fine bilinear/nearest scale; PNG — PNGdec scanlines; GIF); `RenderConfig.toneCurve` is the one
  256-entry tone table applied to every gray before the 4×4 Bayer dither to 4 levels (`DitherUtils.h`); `PixelCache.h`
  streams the 2-bit result to a `.pxc` (uint16 w, h, then rows of 4 px per byte, MSB first) in row bands — free heap on an
  image page is routinely ~55 KB (its header comment). KCCP idea 14: `LineArtFilter.h` — line art told from a photo by its histogram
  (`grayHistogram`, one counting decode at the render's scale, refused over 480×800 of area), the darkness-weight white cut
  (never below `kMinCut`) as `RenderConfig::sourceFilter`, applied to the SOURCE grays before scaling — the panel curve
  stays after it (host test `test/line_art_filter/`, real GEB histograms);
  `test/page_squeeze/` guards bug 16's squeeze.
- `lib/BmpToBmpConverter/BmpToBmpConverter.{h,cpp}` — a BMP of any depth to a screen-ready 2-bit BMP (1-bit sources stay
  1-bit): source rows by `Bitmap::readRowGray` (display order, seek per row), bilinear up / area-average down, the tone
  curve AFTER the scaling, `adjustPixel` (a no-op: `USE_BRIGHTNESS = false`, `BitmapHelpers.cpp`) and an Atkinson dither
  whose legacy thresholds turn every gray ≥ 150 white (`BitmapHelpers.h`; a flat 215 dithers all white, 170 does not); callers — the sleep cover (`SleepActivity`) and the viewer. KCCP idea 14 (1.1.4, in work): an optional
  `sourceFilter` on every source row before the scaling. Host test `test/bmp_to_bmp/` (builds on Windows since
  2026-11-20, `path.string()`).
- `src/activities/reader/ReaderToolbarUi.{h,cpp}` — the bottom sheet of a book opened by a centre tap (FreeInkUI on
  `UiAppHost`): the toolbar (chapter ◀ ▶, progress track with a knob, meta line) and the tool row of three icon slots
  Contents / Text / More (`kToolRowH` 80, the active one in an outline pill); a slot opens a PANEL in the same sheet —
  title, a scrolling list sized to whole rows (row height `tokens.rowHeight` + gap `max(listRowGap, listTouchRowGap)`,
  or the theme's `listRowHeight` + `listRowGap` when the reader sets `model.denseRows`), the tool row at the bottom.
- `src/activities/util/BmpViewerActivity.cpp` — the file browser's full-screen image viewer (BMP/JPEG/PNG through the
  panel curve, cache `/.crosspoint/view_*.bmp`, siblings of the folder, long tap rotates); opened by
  `ActivityManager::goToReader` for an image file (replace), and since debug9 pushed over the book reader for a tapped
  book picture (idea 02). The picture is painted in `drawOrientation()` (the reading orientation set in Settings +
  long-tap turns) and the renderer STAYS there, so every touch — swipes, side taps, Back, the long-tap halves (idea
  07: right half clockwise, left counterclockwise) and the shade opened over it — is read as the picture stands
  upright (the owner, 13.11.2026: «как смотришь на картинку, так и управляешь»; since debug10). The physical keys keep the
  reading orientation (`MappedInputManager::setKeysFollowReadingOrientation`, set in the viewer's onEnter, cleared in
  onExit): a short press pages the pictures, a long press turns the picture. Idea 09 (1.1.3-debug2, in work): every
  picture OPENS by its shape — `shapeTurns()` sets `viewTurns` in `onEnter` and `openSibling` (a wide picture in a
  portrait reader → «Альбомная 180°», a tall one in a landscape reader → «Книжная»).
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
- `src/activities/settings/ToggleRowsActivity.{h,cpp}` + `ToggleRowsLayout.h` (epic 05 Ф4, `2fa20f3f`) — the shared rows
  screen of a user-ordered on/off list (icon, name, ▲ ▼, checkbox; stale-tap guard; portrait while open; save on exit)
  with virtual rows; `ShadeTilesActivity` and `HomeScreenButtonsActivity` («Кнопки домашнего экрана», Settings → Display
  under «Кнопки в шторке»; «Настройки» without a checkbox) derive. `src/util/HomeLibrarySlot.h` — the one test «does Home
  draw the plugins/OPDS row», asked by Home and the screen.
- `src/util/ShadeTiles.h` (debug10, epic 01) — the shade tile model: ten tiles by string id (since 1.1.4 idea 11 also settings · transfer · library, off by default; at most `kMaxOn` = 8 on — what fits the portrait row at 56 px, «Кнопки в шторке» refuses the ninth with a modal), on/off and order,
  `parse`/`format` of the `settings.json` string `shadeTiles` ("night,cleanup,…,-sleep"), all may be off (idea 10: no row then), the
  equal-gap row layout and touch slots; host test `test/shade_tiles/` (`ShadeTilesTest.cpp`, 12 cases); held by
  `CrossPointSettings::shadeTiles`. Since epic 05 Ф1 its token loop and ▲ ▼ edits come from `src/util/IdOrderList.h`
  (namespace `idorder`: `forEachToken`, `appendToken`, `moveUp/moveDown/countOn`), the storage algorithm both models share.
- `src/util/HomeMenuButtons.h` (1.1.3-debug2, epic 05 Ф1) — the Home button model, namespace `homemenu`: ids files,
  library, plugins_opds (ONE row: «Плагины» or «OPDS браузер»), transfer, settings, flashlight, sleep and, under
  `KRINIK_MAMA` only, mama (so `kCount` is 7 or 8 per build); default = today's order, all on; settings locked on
  (`isLocked`, `canToggle`); `visible(list, hasPluginsOpdsSlot)` = the buttons Home shows, `indexIn` = a button's row;
  key `homeButtons` in `settings.json` (omitted while default, `Home buttons:` logged at load); host test
  `test/home_menu_buttons/` built twice (`HomeMenuButtonsTest`, `HomeMenuButtonsMamaTest` with `-DKRINIK_MAMA=1`).
- `src/activities/home/HomeActivity.{h,cpp}` — the Home screen: recent covers first, then the button rows. Since epic 05
  Ф2 (`f9ae704b`) `onEnter` reads `homemenu::visible(SETTINGS.homeButtons, slot)` into `shownButtons`; the count, the
  labels/icons, the action switch, the first cursor and `CoverGridHomeUi`'s icon tabs index that one list. One mapping
  `menuItemOf(Button) → HomeMenuItem`; `menuIndexOf` searches the list through it (hidden/absent → the first button).
  Both `.cpp` files turn `-Wswitch` into an error by `#pragma` — the build has no `-Wall`. `shownButtons` is not
  refreshed while Home stays alive under a pushed screen (only `onEnter`). Since Ф3 (`a47582b0`) the list themes draw
  the slice [`menuTopRow`, + `visibleMenuRows()`) of the menu rows (whole rows down to the content bottom minus the hint
  band; X4 Pro: top 314, bottom 797, Lyra 7 rows), a thumb scroll bar while rows overflow; a swipe that starts on the
  list scrolls by a page, keys pull the list to the selection; the cover grid does not scroll. `LOG_DBG` «Menu
  geometry» on entry prints the numbers. Since Ф5 (`de8feb20`) a long tap on a button PUSHES «Кнопки домашнего экрана»
  (`HomeScreenButtonsActivity(button)`): list themes claim the long press only for a contact that began on a button row
  (`contactOnButton`, `buttonAt`, checked before the cover/row touches); on the pop `onButtonSettingsClosed` re-reads
  `shownButtons` under the render lock — Home is popped back to, so no `onEnter` and no «Entering activity: Home» line.
- `src/components/CoverGridHomeUi.{h,cpp}` — the cover-grid Home (theme 4) on FreeInkUI: the current book, the grid, one
  icon tab per shown button (`buttons`, `setButtons`); `selectedAction` returns the tapped tab or cover. Since epic 05 Ф5
  the tabs accept `InputLongPress`, claimed only inside the tabs' SDK hit rect (`ensureMinTouchRect`: ≥ 44 px, snapped to
  the screen edge within 12 px — wider than the drawn bar); `actionWasLongPress()` tells Home.
- `firmware/platformio.local.ini` (ignored) — this PC's native Windows simulator envs (research 01).
- The book position: `<book cache>/progress.bin` (`EpubReaderActivity::onEnter`) — little-endian u16 spine index, u16
  page, then optionally u16 chapter page count and u32 visible-text offset (4, 6 or 10 bytes).
- `simulator/src/SimScreenText.cpp` — with `CROSSPOINT_SIM_SCREEN_TEXT=1` every refresh logs the screen's strings as one
  `[SIM] SCREEN:` line (reading order, no coordinates); `tools/guide_screens_check.py` reads it.
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
