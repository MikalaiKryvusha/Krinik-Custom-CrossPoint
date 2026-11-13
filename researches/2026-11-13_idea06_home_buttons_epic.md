# Research — idea 06: the Home screen buttons settings (epic recon)

> **Created:** 2026-11-13 · **Parent:** ideas/06_home_buttons_settings.md · **Status:** recon · **Outbound:** —

The owner's ask (`ideas/06`, `[OWNER] 2026-11-13 13:29 +03:00 · chat`): «и дует меню с настройками кнопок главного
экрана» — a settings screen for the Home buttons, the same kind as «Кнопки в шторке» (epic 01 Ф2). This is rung 1 of
`/plan-epic`: industry sweep + local recon. Nothing is decided here; section 6 lists the owner's forks.

Local recon re-read 2026-11-13 ≈20:01 +03:00 on `firmware/` `wip/kccp-1.1.3-debug2` HEAD `376bcf11`. The working tree
holds uncommitted epic 01 Ф3 edits (8 files: the shade, the flashlight, `ShadeTilesActivity.{h,cpp}`, icons,
`MappedInputManager.h`); every Home file, `ActivityManager.*`, `ShadeTiles.h` and `CrossPointSettings.*` are clean, so
their line numbers below are HEAD's. Lines of files Ф3 touches are given at HEAD (`git show HEAD:<file>`), with the
working-tree line where it differs. All paths are under `firmware/` unless they start with `qa_runs/` or `testcases/`.

## 1. Industry findings (web sweep 2026-11-13)

Epic 01's research already holds I1–I6 (`researches/2026-11-13_idea05_shade_tiles_epic.md` §1): Android stores the
quick-settings order as one comma list of string ids (I1), keeps a minimum tile count in the editor (I2), opens a tile's
settings by a long press (I3); WCAG 2.5.7 asks a single-pointer alternative to dragging, up/down buttons qualify (I4).
They apply here unchanged and are not repeated. New for Home:

| # | Practice | Source | Quote |
|---|---|---|---|
| H1 | **KOReader** orders and hides its menus by a user file; an entry the file does not list (a NEW entry after an update) is shown, marked «NEW:», in the first menu; no entry is protected from hiding | `frontend/ui/menusorter.lua` — https://github.com/koreader/koreader/blob/master/frontend/ui/menusorter.lua | `orphaned_prefix = _("NEW: ")` · `-- attach orphans based on sorting_hint, or with a NEW prefix in the first menu if none found` · file `"%s/%s_menu_order.lua"` in the settings dir · hidden items go to `order["KOMenu:disabled"]` (`-- remove reference from input so it won't show up as orphaned`); the fetch found no code that refuses to hide any item |
| H2 | **Kobo** stock: no user ordering of Home found in this sweep; the community tool NickelMenu adds entries from a config file on the device and protects against lock-out by an out-of-band route | NickelMenu — https://pgaskin.net/NickelMenu/ | «adds custom menu items to various menus in Kobo's eReader software» · config `KOBOeReader/.adds/nm/config` · a failsafe — it «will never result in an unbootable Kobo» · uninstall: create `KOBOeReader/.adds/nm/uninstall`, reboot |
| H3 | **Kindle**: one whole-screen switch, no per-entry choice (and removed in newer software) | https://blog.the-ebook-reader.com/2019/01/25/how-to-change-your-kindles-homescreen-to-list-view/ | «go to Settings > Device Options > Advanced Options > Home & Library > Home Screen View» · «the home button takes you to the library view instead» · comment: «Turning off the home screen view is no longer an option on the new software post 5.13.7» |
| H4 | **Boox** launcher: the side buttons can be reordered, not added; the Library's function bar is chosen and reordered in a SETTINGS screen, not on the bar itself | https://ewritable.net/brands/boox/firmware/4-0/ · https://blog.the-ebook-reader.com/2025/04/09/onyx-boox-software-update-4-0-now-available-for-these-models/ | «You can reorder these buttons» · «you can't add new buttons, or widgets» · «You can select and re-order those functions in [Library Settings > Library List Settings]» — hiding a side button and a protected Settings button: not found |
| H5 | **Android** refuses to disable the system Settings app and the launcher — the lock-out rule, by name | AOSP Settings `AppButtonsPreferenceController.handleDisableable` — https://github.com/aosp-mirror/platform_packages_apps_settings/blob/main/src/com/android/settings/applications/appinfo/AppButtonsPreferenceController.java | «Try to prevent the user from bricking their phone by not allowing disabling of apps signed with the system cert and any launcher app in the system.» (An ICON of Settings may leave the home screen: the app stays reachable from the app drawer — the protection is on the route, not on the icon.) |
| H6 | **iOS**: Settings is not among the built-in apps a user can delete | Apple Support 118582 — https://support.apple.com/en-us/118582 | «you can delete some built-in Apple apps from your iPhone, iPad, or Apple Watch» — the iPhone list (Activity … Weather) has no Settings |
| H7 | **iOS Control Center** editor: every control is removable, because the way INTO the editor does not depend on any control; new third-party controls are not added by themselves | MacRumors iOS 18 guide — https://www.macrumors.com/guide/ios-18-control-center/ | «Long press on any empty space and hold until the grid shows up» (or the «+» button) · «None of the Control Center buttons are permanent» · third-party controls «can be added to Control Center through the Control Center gallery» |
| H8 | **Google TV** (a device without drag — remote only) reorders by a modal Move with arrow keys | Google Help — https://support.google.com/chromecast/answer/12390692 | «Hold the Select button on your remote until a menu appears» · «Select Move» · «To move the app, use the Left or Right buttons.» · «To save your new app order, select Done.» · «You can also use the Reorder tile to reorder your apps.» |
| H9 | **CrossPoint upstream**: Home has no scrolling; Home can no longer be landscape | issue #3259 — https://github.com/crosspoint-reader/crosspoint-reader/issues/3259 | «The home screen has no scrolling, so there is no way to bring those entries back into view.» · closing comment: «the quick-settings orientation tile no longer turns the renderer, so the home screen can no longer end up in landscape» |
| H10 | **CrossPoint upstream** names the enum-index anti-pattern for a stored menu choice | issue #3640 — https://github.com/crosspoint-reader/crosspoint-reader/issues/3640 | «Anything appended at the end is unreachable on the X3/X4, and renumbering shifts everyone's saved setting.» |

What the sweep answers on the three questions asked:

- **(a) Lock-out protection.** Two shapes exist. *Guard the item*: Android refuses to disable the Settings app (H5), iOS
  refuses to delete it (H6). *Guard the route*: iOS Control Center lets every control go, because the editor's entry
  is a long press on EMPTY space (H7); Android lets the Settings ICON leave the home screen because the drawer still
  has it (H5 note); NickelMenu keeps a file-on-the-card route that works whatever the menu shows (H2). KOReader guards
  nothing (H1). Epic 01 took a third, weaker shape: «at least one on» (I2), so a button stays to long-tap into the
  editor.
- **(b) Edit UI without drag.** A settings screen with a checkbox per entry and move controls (Boox H4, the agreed
  ▲ ▼ of epic 01, WCAG I4); on a remote-only device a modal «Move» driven by arrow keys (H8). No source found drags on
  e-ink.
- **(c) Order across updates.** Store ids, never positions (I1, H10). An entry new to the firmware is either shown
  and marked «NEW:» (KOReader H1) or offered and NOT added (Android QS I1, iOS gallery H7). Epic 01 chose «appended
  OFF» (`ShadeTiles.h:103-105`).

## 2. Local recon — the Home code at HEAD `376bcf11`

### 2.1 The five places of the code map §4, re-checked

The map (`researches/2026-11-13_idea05_06_code_map.md` §4, read at debug9 `35dc070c`) holds, with shifted lines, and
misses three per-item sites:

| # | Site | HEAD lines | What it hard-codes |
|---|---|---|---|
| 0 | `HomeMenuItem` enum | `src/activities/ActivityManager.h:21-31` | `NONE, FILE_BROWSER, LIBRARY, OPDS_BROWSER, FILE_TRANSFER, SETTINGS_MENU, FLASHLIGHT, SLEEP, MAMA_HEART` — no PLUGINS value: the plugins entry rides `OPDS_BROWSER` |
| 1 | item → index, index → item | `src/activities/home/HomeActivity.h:45-65`, `:68-81` | the order Files, Library, [slot], Transfer, Settings, Flashlight, Sleep, [Mama]; the parameter is named `hasOpdsUrl` but callers pass `hasLibrarySlot()` (`HomeActivity.cpp:267`, `:329`) |
| 2 | item count | `src/activities/home/HomeActivity.cpp:40-52` | `int count = 6;` + mama + slot + recent books; the comment `:43` says Mama sits «under Settings» — it is last (`:573-577`) |
| 3 | labels + icons of the list | `src/activities/home/HomeActivity.cpp:564-582` | a vector built in order, the slot inserted at `begin() + 2` (`:579-582`); «Для любимой Мамы» is a literal, not an `STR_` (`:575`) |
| 4 | cover-grid tabs | `src/components/CoverGridHomeUi.cpp:288-325` | `ICONS[]` per build (`:289-295`), the slot skipped by position `if (i == 2 && !hasOpds)` (`:299`), the icon remapped by position (`:316`) |
| 5 | `goHome` cursor by activity name | `src/activities/ActivityManager.cpp:377-401` (map: 376-398) | `FileBrowser`, `Library`, `OpdsBookBrowser`/`PluginCatalog`, `CrossPointWebServer`, `Settings`/`SettingsList`, `Flashlight`, `Mama` → item |
| + | the action switch | `src/activities/home/HomeActivity.cpp:329-361` | keyed by enum (order-free) — but every item needs its case |
| + | the tab array size | `src/components/CoverGridHomeUi.h:63-67` | `std::array<TabItem, 7>` / `8` under `KRINIK_MAMA` — a fixed capacity, a twin of `ICONS[]` |
| + | the selection start | `src/activities/home/HomeActivity.cpp:266-267` | `base + menuItemToIndex(initialMenuItem, hasLibrarySlot())` |

`TWINS:` searched `HomeMenuItem::` and `KRINIK_MAMA` over `src/` — the enum is read in `HomeActivity.{h,cpp}`,
`ActivityManager.cpp`, `Activity.{h,cpp}` (`onGoHome`), `FlashlightActivity.cpp`, `MamaActivity.cpp`,
`OpdsServerListActivity.cpp`, `main.cpp`; `KRINIK_MAMA` in six files (`ActivityManager.{h,cpp}`,
`HomeActivity.{h,cpp}`, `CoverGridHomeUi.{h,cpp}`).

### 2.2 The two layouts and how many buttons each shows (X4 Pro)

The panel is 800×480 landscape-native; Home is drawn **portrait 480×800 only**. No Home code sets an orientation, the
reader resets portrait on exit (`src/activities/reader/ReaderActivity.cpp:125`), and upstream closed the last landscape
path (H9). So «landscape» is not applicable to Home on the X4 Pro. The touch board draws no button-hint band
(`LyraTheme.cpp:121-123`, `if (gpio.hasTouch()) return;`). The classic list never scrolls (H9) — rows past the bottom
are simply off the glass. Numbers below are computed from the code's constants, not measured on a run:

| Theme (`uiTheme`) | Menu top / row / step | Fits fully | First cut row | Source lines |
|---|---|---|---|---|
| **Lyra (1) — the owner's** (KCCP `settings.json` → `uiTheme` value `1`) | 56 + 242 + 16 = **314** / 60 / 68 | **7** (7th ends at 782) | 8th: y 790–850, 10 px visible — the mama build's «Мама» (STATUS) | `LyraTheme.h:37-38,43,45,48`; `LyraTheme.cpp:321-328` (draws `rect.y + i*68`, ignores `rect.height`); `HomeActivity.cpp:590-598` |
| Classic (0) | 10 + 40 + 400 + 10 = **460** / 41 / 49 | **7** (7th ends at 795) | 8th starts at 803 — fully off | `BaseTheme.h:165,185-186,191,193,196`; `BaseTheme.cpp:742-747` |
| Lyra Extended (2) | 56 + 300 + 16 = **372** / 60 / 68 | **6** (6th ends at 772) | 7th: y 780–840 — already the plain KCCP build with the OPDS/plugins slot (7 items) | `Lyra3CoversTheme.h:12` |
| RoundedRaff (3) | pages: `pageItems = rect.height / rowStep` | one page | none — it pages; adds a «Продолжить чтение» row (`homeContinueReadingInMenu = true`) | `RoundedRaffTheme.cpp:153-160`; `RoundedRaffTheme.h:52`; `HomeActivity.cpp:584-588` |
| Cover grid (4, needs PSRAM) | an icon-only tab bar at the bottom: 32 px icons, `SpaceBetween`, no labels | **all** (7 / 8) in one row; capped by `tabItems` 7 / 8 | none | `CoverGridHomeUi.cpp:303,308,311`; `CoverGridHomeUi.h:63-67`; `UITheme.cpp:33-35` |

Noticed, not verified: RoundedRaff pages its drawn rows but `HomeActivity.cpp:468-476` builds the touch grid over all
`renderedMenuCount` rows from `menuTop` — past the first page the touch rows and the drawn rows may disagree.

Evidence of the five shapes (with the five items of 2026-11-08, before «Фонарик» and «Сон»):
`qa_runs/mama_matrix_home.webp` — the classic list of Classic, Lyra, Lyra Extended, RoundedRaff, and the cover grid
with its icon tabs.

### 2.3 How Home picks its first cursor

- `HomeActivity(…, HomeMenuItem initialMenuItemValue = NONE, …)` (`HomeActivity.h:101-105`) → `selectorIndex = NONE ? 0
  : recentBooks.size() + menuItemToIndex(item, hasLibrarySlot())` (`HomeActivity.cpp:266-267`). With recent books,
  index 0 is the first COVER, not the first button.
- Explicit callers (HEAD): `FlashlightActivity.cpp:43` → `FLASHLIGHT` (`:46` in the Ф3 tree); `MamaActivity.cpp:47` →
  `MAMA_HEART`; `OpdsServerListActivity.cpp:112` → `OPDS_BROWSER`. `main.cpp:703` and `:1098` pass `NONE`.
- Implicit: `goHome()` with `NONE` maps the CURRENT activity's name to an item (`ActivityManager.cpp:379-399`); every
  `onGoHome()` (`Activity.cpp:13`; 20 call sites at HEAD, `git grep -n "onGoHome()" HEAD -- src`) lands there. `SLEEP` has no mapping: after a wake the cursor is 0.
- A hidden or absent item today: `menuItemToIndex` returns 0 for `OPDS_BROWSER` without the slot (`HomeActivity.h:51`)
  — the precedent for «the remembered item is gone → the first position».

### 2.4 Conditional items

| Item | Condition | Lines |
|---|---|---|
| The library slot (ONE row) | `hasPlugins \|\| hasOpdsServers`; shows «Плагины» when plugins are on, else «OPDS браузер»; Plugins shows OPDS inside | `HomeActivity.h:25`; `HomeActivity.cpp:246,250,336-337,580,628` |
| «Для любимой Мамы» | compile time, `-DKRINIK_MAMA=1` in `[env:x4pro-mama]` and `[env:simulator_x4_pro_mama]` | `platformio.ini:896-915` |
| «Продолжить чтение» | theme (RoundedRaff only) — a book, not a button | `HomeActivity.cpp:584-588` |
| Recent covers | precede the buttons in `selectorIndex` — not buttons | `HomeActivity.cpp:324-328` |

Plugins add no Home entries of their own (`PluginCatalogActivity.cpp:1516-1517`: a root launch returns Home). The
plugins switch lives in Settings, hidden from the web page (`SettingsList.cpp:236`, `.withWebHidden()`).

**The only on-device way into Settings is the Home row «Настройки»** — `HomeActivity.cpp:622`
(`activityManager.goToSettings()`). The other `goToSettings` callers are the calibration-card returns
(`ReaderUtils.h:274`, `BmpViewerActivity.cpp:636`) and a silent-reboot resume (`main.cpp:1088`). Out of band: the
web settings API `/api/settings` (`CrossPointWebServer.cpp:334-335`) and USB drive mode
(`CrossPointWebServerActivity.cpp:162`) both sit behind the Home row «Передача файлов». No settings reset exists
(grep `reset settings|factoryReset|resetSettings` over `src/` → 0 hits). Whether the X4 Pro's microSD can be pulled
and edited in a PC: not checked.

## 3. What epic 01 gives as-is, and what needs generalizing

| Part | Where | As-is for Home | Needs |
|---|---|---|---|
| Stored form: ordered string ids, `-` = off, unknown skipped, missing appended OFF, empty → defaults | `src/util/ShadeTiles.h:13-16,103-142` | the algorithm and the format | the code is typed to `shadetiles::Tile`, `kCount = 7`, `kIds` (`:22-30`): a second id table (copy) or a template over (enum, ids, defaults) |
| `moveUp` / `moveDown` / `countOn` | `ShadeTiles.h:70-101` | logic | typed to `shadetiles::List` |
| «At least one on» | `ShadeTiles.h:84-89` (`canTurnOff`), `:130` (parse turns `list[0]` on) | — | Home's lock-out rule is per ITEM («Настройки» stays on), not a count: a `locked(item)` predicate; the parse repair must turn the locked item on, not `list[0]` |
| Equal-gap row layout | `ShadeTiles.h:144-179` | — | not needed: the list draws rows, the cover grid uses FreeInkUI `TabBarLayout::SpaceBetween` (`CoverGridHomeUi.cpp:308`) |
| Persistence (hand-saved string, omitted while default, parsed on load) | `CrossPointSettings.h:475-479`; `CrossPointSettings.cpp:124-125,316-320` | the pattern, one more key | — |
| Host test | `test/shade_tiles/` (`ShadeTilesTest.cpp`) | the template | its own cases (locked item, the slot, mama) |
| Screen: rows (icon, name, ▲ ▼, checkbox), stale-tap guard (`moveSerial`/`paintedSerial`), portrait while open, Back = `finish()` | `ShadeTilesActivity.h:28-68`, `.cpp:88-344` (HEAD) | the drawing and input code | it reads `SETTINGS.shadeTiles`, `tileIcon`/`tileName` (`.cpp:45-85`), `shown()` (Bluetooth, `:127-130`), `STR_SHADE_TILES(_NOTE)` directly: an adapter (count, icon, name, shown, locked, the list, title, note) or a near-copy |
| Hit budget | `static_assert(kCount * 3 <= 24)` (`.cpp:35`); `FreeInkApp<24, 6>` (`UiAppHost.h:29`) | — | 7 rows = 21; **8 rows = 24 = the cap, zero headroom**; 9 rows (slot split in two + mama) = 27 → overflow (dropped silently) |
| Row fit | rows shrink when they overflow (`.cpp:264-265`); measured row step ≈ 0.081 × 800 ≈ 65 px from y ≈ 264 (`testcases/reports/2026-11-13_epic01_p2.md:24`) | 7 rows | 8 rows ≈ 264 + 8 × 65 = 784 > the 760 content bottom → rows shrink ≈ 3 px each (computed, not run) |
| Names | «Ориентация чтения» was cut to «Ориентация чтен…» (`qa_runs/epic01_p2_c1/shots/tiles0.webp`) → a short string `STR_SHADE_TILE_ORIENTATION` | — | «Для любимой Мамы» (16 letters) and «Передача файлов» (15) are as long as the cut name: likely cut too |
| Settings entry | `SettingsActivity.cpp:165-169` (`addAction(Display, STR_SHADE_TILES, …)`, touch boards only), `:374-382` | the pattern | Home has key navigation too; on the X4 Pro (touch) the same gate holds |
| Long-tap entry | Ф3 tree: `FrontlightPanelActivity.cpp:37,169,320-322` (`ACTION_TILE` + `event.longPress`, long press only for a contact that began on the row) | the pattern for the cover-grid tabs (`routeTouch` today without long press, `CoverGridHomeUi.cpp:86`) | the classic list uses `rowTouch` (selection at 90 ms touch-down, `MappedInputManager.cpp:200`; activation on release, `HomeActivity.cpp:477-490`): a long press must be checked BEFORE `rowTouch` there; Home takes no long press today |
| Keys reorder | not built: «Moving a row by keys is not built» (`ShadeTilesActivity.cpp:201-202`) | — | if wanted: a modal Move with arrows (H8) |

## 4. Risks (Murphy, tiered)

**(a) Highest — defend in the plan**

1. **Lock-out.** Hiding «Настройки» removes the only on-device way into Settings (`HomeActivity.cpp:622`); hiding
   «Передача файлов» too removes the web and USB routes to the card (§2.4). No reset exists. Industry: guard the item
   (H5, H6) or guard the route (H7, H2). Owner's fork Q2.
2. **Twins.** Order lives in five places plus three per-item sites (§2.1); one id table must drive all of them, or a
   reordered list draws one order, touches another and remembers a third. Every site gets a host-test or simulator
   check.
3. **Silent hit overflow on the settings screen.** 8 rows × 3 hits = 24 = the cap; any 9th row (slot split, a future
   item) drops hits with no error (`ShadeTilesActivity.cpp:28,35`). The `static_assert` must count the Home list's
   maximum, not the shade's 7.
4. **The remembered cursor of a hidden item.** `goHome(FLASHLIGHT)` and the name mapping (§2.3) can point at a hidden
   or moved item; the index must come from the visible list, with a defined fallback.

**(b) Plausible — the contingency**

5. **Hiding does not cure the default overflow.** The mama build's 8th row (Lyra) and Lyra Extended's 7th row stay cut
   until the user hides something; the default list itself decides what the mother first sees (Q3, Q8).
6. **Long names cut** on the settings screen (§3) → short strings, as `STR_SHADE_TILE_ORIENTATION`.
7. **Upstream drift.** `HomeActivity.*` and `CoverGridHomeUi.*` are upstream CrossPoint files (KCCP already adds
   «Фонарик», «Сон», «Мама»); a model-driven Home widens every future merge from `develop`; a new upstream Home item
   arrives as an unknown entry (Q7).
8. **Long tap vs the list's touch.** The classic rows select at 90 ms and act on release; «Сон» paints the selection and
   sleeps (`HomeActivity.cpp:348-356`) — a long tap must be claimed first and suppress the rest of the contact
   (EXP-0016: one physical motion, several consumers).
9. **RoundedRaff paging vs the touch grid** (§2.2, noticed, not verified) — any visible-count change goes through it.

**(c) Low — listed**

10. The name «Кнопки главного экрана» sits near «Жесты кнопки «Домой»» (`STR_HOME_BUTTON`, `russian.yaml:628`) and
    `HomeButtonSettingsActivity` (the physical key) in code.
11. `restore.mjs` writes only what the web settings page lists; `shadeTiles` is not there (no hit in `src/network/`),
    nor would a Home key be — the owner's one-command setup would not carry his Home order.
12. Stale comment `HomeActivity.cpp:43`; misleading parameter name `hasOpdsUrl` (`HomeActivity.h:45,68`).

## 5. Fit

- `GOAL.md` success 1 (both readers on a KCCP release the owner checked) and `MASTER_PLAN.md` phase 2 — whose steps
  name «исправление главного меню маминой сборки (8 строк, строка «Мама» уходит за экран)»; this epic is one way to
  close that step (Q3, Q8).
- Heaviness test (`AGENT_GUIDE.md` → Planning discipline): touches ≥ 3 subsystems (Home, cover grid, activity manager,
  settings, persistence) · rests on industry practice · needs owner decisions (section 6) → HEAVY → `/plan-epic`.

## 6. The owner's decisions — forks to carry into an interview

Listed, not decided. Each goes to `interviews/` as a scenario in Russian (the place of questions,
`AGENT_GUIDE.md`); the precedent column is the fourth door for each `FORK:` line.

| # | Question | Options | Industry precedent |
|---|---|---|---|
| Q1 | Which Home buttons may be hidden? | A — every button except «Настройки» · B — every button, with at least one left on (epic 01's rule) · C — only KCCP's own («Фонарик», «Сон», «Мама»); the upstream ones stay | A: Android / iOS guard the Settings app (H5, H6) · B: Android QS minimum (I2), epic 01 · C: Boox — reorder, no add (H4) |
| Q2 | Must «Настройки» stay on? | A — yes: its checkbox is locked, a line on the screen says why · B — it may be hidden; a long tap on Home still opens this screen to bring it back (the rest of Settings is unreachable meanwhile) · C — it may be hidden; recovery only by editing `settings.json` on the card | A: H5 «prevent the user from bricking their phone», H6 · B: iOS Control Center — the editor's entry never depends on a control (H7) · C: NickelMenu's uninstall file (H2) |
| Q3 | Does the mama build's «Для любимой Мамы» join the list? | A — yes, a normal row (on by default, may be moved or hidden; a short name on the screen) · B — no, it stays fixed last, outside the list · C — yes, and the mama build's default hides one row so 7 fit on Lyra | A/C: Android's default tile list is a per-build resource, tiles a build lacks are filtered (I1) · B: no precedent found for a fixed entry outside an editable list |
| Q4 | Where does the screen sit in Settings? | A — «Настройки → Экран», right under «Кнопки в шторке» · B — «Настройки → Общие» · C — nowhere in Settings, only the long tap on Home | A/B: Boox — chosen and reordered in a settings screen (H4) · C: iOS Control Center — edited only from itself (H7) |
| Q5 | Where is its entry on Home? | A — a long tap on any Home button opens the screen with the cursor on that button (the shade's way) · B — only from Settings · C — a long tap on an empty part of Home (the header band) | A: Android long press → the tile's settings (I3), epic 01 · B: Kindle / Boox — settings only (H3, H4) · C: iOS — long press on empty space (H7) |
| Q6 | The «Плагины / OPDS браузер» slot: one row or two? | A — one row, as today (shows «Плагины» when plugins are on, else OPDS) · B — two rows, each on its own | A keeps the screen at ≤ 8 rows = the 24-hit cap · B needs 9 rows with mama → past the cap (§3); Android drops tiles the build lacks (I1) |
| Q7 | A Home button that a future firmware adds (a KCCP or upstream merge) — how does it appear? | A — at the end, OFF (as the shade) · B — at the end, ON · C — at the end, ON and marked «новая» on the screen | A: Android QS, iOS gallery (I1, H7) · C: KOReader «NEW:» (H1) · B: no fetched source |
| Q8 | More buttons on than the theme fits (Lyra 7, Lyra Extended 6) — what then? | A — the screen refuses the extra checkbox and says why · B — Home shrinks its rows to fit · C — Home pages its list (as RoundedRaff does) | A: Android QS editor limits (I2) · C: RoundedRaff here (`RoundedRaffTheme.cpp:153-160`); upstream Lyra has no scrolling (H9) |

Agent defaults that need no owner (reversible, `[AI]` when the plan is written): the stored key holds ids, never
enum positions (I1, H10); the settings screen reuses the Ф2 row look and ▲ ▼; Home reads ONE model in all five places.
