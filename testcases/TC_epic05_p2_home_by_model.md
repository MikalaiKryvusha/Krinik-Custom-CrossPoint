# Test cases — epic 05, phase 2: Home draws its buttons from the model

**Created:** 2026-11-14 · **Under test:** `wip/kccp-1.1.3-debug2` (`firmware/`) — `HomeActivity` (rows, labels, icons,
action, first cursor), `CoverGridHomeUi` (icon tabs) reading `homemenu::visible(SETTINGS.homeButtons, slot)` ·
**Version/build:** simulator `simulator_x4_pro_win` (plain build), then `1.1.3-debug2` on the owner's X4 Pro
**Test basis:** `plans/08_DONE_epic05_p2_home_by_model.md` → criteria 1–5; the meta-plan `plans/05_EPIC_home_buttons.md` →
criteria 6 and 11, the Ф2 gate («критерии 6 и 11 на симуляторе; тап по каждой кнопке при сдвинутом порядке открывает
экран этой кнопки»).

## 1. Goal vector

Achieve: Home draws, touches and remembers its buttons in the order and on/off state of `homeButtons`, in all five
themes; a card without the key looks exactly as before.

## 2. Requirements under test

| # | Requirement (EARS) | Fit criterion |
|---|---|---|
| R1 | WHILE `homeButtons` = `files,sleep,-library,plugins_opds,transfer,settings,flashlight` and no plugins/OPDS server, Home shall draw Обзор файлов, Сон, Передача файлов, Настройки, Фонарик, in that order, in each theme 0–4. | five shots: the labels (list themes) / the icons (cover grid) in that order, no Библиотека |
| R2 | WHEN the owner taps the second button in that state, the reader shall go to sleep. | log: the sleep entry after the tap, per theme |
| R3 | WHEN a button stands at a moved row, a tap on that row shall open that button's screen. | log `Entering activity: <its screen>` per button |
| R4 | WHEN `settings.json` has no `homeButtons`, Home shall draw today's order. | log `Home buttons: files,library,plugins_opds,transfer,settings,flashlight,sleep`; the Lyra shot below the status bar equals the phase 1 shot pixel for pixel |
| R5 | WHEN the owner leaves by «Фонарик» standing at a moved row and comes back, the cursor shall stand on «Фонарик». | the shot after the return: the selection on the «Фонарик» row |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| theme | Classic 0, Lyra 1, Lyra Extended 2, RoundedRaff 3, cover grid 4 | — |
| slot | absent (fixture cards have no plugins, no OPDS server) | present — needs plugins on: one Lyra run with `pluginsEnabled: 1` if time allows |
| buttons | each of files, transfer, settings, flashlight, sleep tapped at a moved row (Lyra) | library — its screen needs a library index; mama — no Windows mama simulator env (Ф3 adds it) |
| cursor memory | the shown button at a moved row (flashlight) | a hidden remembered button (goHome to a hidden item): no user path reaches it except Settings → OPDS servers; the fallback is host-tested (`indexIn` −1 → row 0) |
| recent covers | none (empty cards) | with covers the button rows are offset by the covers; covered by code review only |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| C1 | card `sd_template` (no key), Lyra → boot → Home shot | regression, control | pass · run `epic05_p2_c1`: log default order; 0 px ≥ 40 levels vs the Ф1 shot (WebP, clock differs) |
| C2 | card `.tmp/sd_p2_theme0` (Classic) → Home shot → tap the 2nd button → sleep | equivalence (theme), decision | pass · `epic05_p2_t0` shot, `epic05_p2_tap0` → Sleep |
| C3 | the same, Lyra (`sd_p2_theme1`) | equivalence | pass · `epic05_p2_t1`, `epic05_p2_tap1` → Sleep |
| C4 | the same, Lyra Extended (`sd_p2_theme2`) | equivalence | pass · `epic05_p2_t2`, `epic05_p2_tap2` → Sleep |
| C5 | the same, RoundedRaff (`sd_p2_theme3`) | equivalence; research risk «paging vs touch grid» | pass · `epic05_p2_t3`, `epic05_p2_tap3` → Sleep |
| C6 | the same, cover grid (`sd_p2_theme4`): the 2nd icon tab | equivalence | pass · `epic05_p2_t4` icons in order, `epic05_p2_tap4` → Sleep |
| C7 | Lyra, order `flashlight,settings,transfer,files,sleep,-library`: tap row 1..5 in five runs → Flashlight, Settings, CrossPointWebServer, FileBrowser, sleep | state transition | pass · `epic05_p2_row0…4` → Flashlight, SettingsList, CrossPointWebServer, FileBrowser, Sleep |
| C8 | Lyra, the C7 order: tap «Фонарик» (row 1) → the flashlight → tap → Home shot | state transition | pass · `epic05_p2_c8`: the selection on «Фонарик», row 2 (order `settings,flashlight,…`, not row 1 — the case was moved off the fallback row) |

## 5. Not expressible on the simulator

- The owner's reader (touch timing, the real panel) — the image's homework (Ф6).
