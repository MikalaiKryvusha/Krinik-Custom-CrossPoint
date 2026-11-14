# Plan 08 — epic 05, phase 2: Home draws its buttons from the model

> **Created:** 2026-11-14 · **Parent:** `plans/05_EPIC_home_buttons.md` → «Ф2 — домашний экран по модели» · **Status:**
> ✅ phase closed 2026-11-14 16:22 +03:00 — firmware `f9ae704b`; simulator C1–C8 pass in all five themes (`testcases/reports/2026-11-14_epic05_p2.md`),
> the `-Wswitch` error proven red, host suite 795/803 (the 8 known); judge: VERIFIED WITH CAVEATS, no blockers,
> findings fixed · in work since 2026-11-14 15:57 +03:00 · **Outbound:** —

## Goal vector (Achieve)

Home today hard-codes its button order in eight places (research `2026-11-13_idea06_home_buttons_epic.md` §2.1). After
this phase every one of them reads `homemenu::visible(SETTINGS.homeButtons, hasLibrarySlot())`, in all five themes, so
the order and the on/off state the owner sets (Ф4) are what Home draws, touches and remembers. No settings screen yet:
the phase is driven by a hand-written `homeButtons` key on the simulator card.

Anchor (meta-plan, Ф2): «Домашний экран берёт порядок и включённые кнопки из модели во всех восьми местах кода, где
порядок сейчас зашит (исследование, §2.1), во всех пяти темах. Курсор после возврата на домашний экран встаёт на
кнопку, с которой ушли; если эта кнопка выключена — на первую кнопку.»

## Acceptance criteria (phase)

1. **Order and off state, all themes** (meta-plan criterion 6). WHEN `homeButtons` = `"files,sleep,-library,
   plugins_opds,transfer,settings,flashlight"`, each of the five themes (`uiTheme` 0–4) shall draw «Обзор файлов»,
   «Сон», … without «Библиотека». Check: five simulator shots; a tap on the second button → the log shows the sleep.
2. **Each button opens its own screen** at a moved position. Check: per button, a simulator tap on its row → the
   `Entering activity:` line of its screen (Flashlight, Settings, FileBrowser, CrossPointWebServer, Library).
3. **Old card** (meta-plan criterion 11). WHEN `settings.json` has no `homeButtons`, Home shall draw today's order. Check:
   shot + `Home buttons:` log line; a shot of Lyra before the change and after it are pixel-identical.
4. **Cursor on return.** WHEN the owner leaves by «Фонарик» and comes back, the cursor shall stand on «Фонарик» at its
   moved row; WHEN the remembered button is off, on the first button. Check: simulator shots after the return.
5. **Cover grid** (theme 4): the icon tabs follow the model (icon per button, not per position). Check: shot.

## Steps

- [x] P2.1 One mapping `homemenu::Button → HomeMenuItem` as an exhaustive `switch` over `Button` with no `default`; the
      reverse searches the shown list through it (the Ф2 judge: two inverse switches are a pair). The build has no
      `-Wall`, so each file turns `-Wswitch` into an error by `#pragma GCC diagnostic error "-Wswitch"` — proven red on
      a removed case; `Mama` under `#if KRINIK_MAMA` (judge Ф1, finding 8). Anchor: «во всех восьми местах кода».
- [x] P2.2 `HomeActivity`: `menuItemToIndex`/`indexToMenuItem`, `getMenuItemCount`, the labels/icons vector, the
      selection start and the action switch read the visible list; labels and icons by button.
- [x] P2.3 `CoverGridHomeUi`: `begin()` takes the visible list; `drawTabs` icons by button; `tabItems` capacity =
      `homemenu::kCount`.
- [x] P2.4 `goHome` keeps its name → `HomeMenuItem` map; Home resolves it through `indexIn` (−1 → the first button).
- [x] P2.5 Judge BEFORE the build; fix findings.
- [x] P2.6 Host suite (`sh tools/host_tests.sh`); simulator runs for criteria 1–5 by a case set
      `testcases/TC_epic05_p2_home_by_model.md`; run report.
- [x] P2.7 Commit, tick Ф2 in the meta-plan, write the Ф3 plan (and add `simulator_x4_pro_mama_win`).

## Carried forward (the Ф2 judge, ≈ 2026-11-14 16:11)

- **Ф5:** `shownButtons` is set only in `HomeActivity::onEnter`. If the «Кнопки домашнего экрана» screen is PUSHED over
  Home, Home gets no `onEnter` when it closes and keeps the old order — meta-plan criterion 9 would fail. Ф5 recomputes
  `shownButtons` (and `coverGridUi->begin`) on return, or leaves the screen through `goHome`.
- **P2.7:** `PROJECT_ARCHITECTURE_INTERNAL_MAP.md` → the `HomeActivity` line says the order is hard-coded; rewrite it.

## Risks

1. **A twin site missed** (research §2.1 lists eight; `TWINS:` search `HomeMenuItem::` and `KRINIK_MAMA` over `src/`
   again before the judge). A missed site draws one order and acts on another — criterion 2 taps every button.
2. **RoundedRaff paging vs the touch grid** (research §2.2, noticed, not verified) — criterion 1 taps in theme 3.
3. **Upstream drift** in `HomeActivity.*` / `CoverGridHomeUi.*` (upstream files): keep the diff to the eight sites.

## Decisions made without the owner

- `[AI]` The reverse lookup (`HomeMenuItem` → row) searches the shown list through the one forward mapping — the Ф2
  judge's finding 2; two inverse switches would be a pair that can drift.
- `[AI]` `#pragma GCC diagnostic error "-Wswitch"` in `HomeActivity.cpp` and `CoverGridHomeUi.cpp`: the build has no
  `-Wall` (the judge's finding 1), so the exhaustive switches over `homemenu::Button` / `HomeMenuItem` are guarded by
  the file itself; proven red on a removed case.
- `[AI]` A hidden or absent remembered button lands on the first BUTTON (`base + 0`), `NONE` on the first cover — the
  meta-plan's «если эта кнопка выключена — на первую кнопку», as the absent plugins/OPDS slot behaved before.
- `[AI]` The cover-grid tabs copy the shown list in `begin()` (`tabItems` capacity = `homemenu::kCount`).
- PENDING settled: none were opened.
