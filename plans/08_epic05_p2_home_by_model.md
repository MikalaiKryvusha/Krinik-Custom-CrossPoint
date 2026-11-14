# Plan 08 — epic 05, phase 2: Home draws its buttons from the model

> **Created:** 2026-11-14 · **Parent:** `plans/05_EPIC_home_buttons.md` → «Ф2 — домашний экран по модели» · **Status:**
> 🔧 in work since 2026-11-14 15:57 +03:00 (Ф1 closed); drafted 2026-11-14 15:51 +03:00 · **Outbound:** —

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

- [ ] P2.1 One mapping `homemenu::Button ↔ HomeMenuItem` as an exhaustive `switch` over `Button` with no `default`, so
      `-Wswitch` catches a new button; `Mama` under `#if KRINIK_MAMA` (judge Ф1, finding 8). Anchor: «во всех восьми
      местах кода».
- [ ] P2.2 `HomeActivity`: `menuItemToIndex`/`indexToMenuItem`, `getMenuItemCount`, the labels/icons vector, the
      selection start and the action switch read the visible list; labels and icons by button.
- [ ] P2.3 `CoverGridHomeUi`: `begin()` takes the visible list; `drawTabs` icons by button; `tabItems` capacity =
      `homemenu::kCount`.
- [ ] P2.4 `goHome` keeps its name → `HomeMenuItem` map; Home resolves it through `indexIn` (−1 → the first button).
- [ ] P2.5 Judge BEFORE the build; fix findings.
- [ ] P2.6 Host suite (`sh tools/host_tests.sh`); simulator runs for criteria 1–5 by a case set
      `testcases/TC_epic05_p2_home_by_model.md`; run report.
- [ ] P2.7 Commit, tick Ф2 in the meta-plan, write the Ф3 plan (and add `simulator_x4_pro_mama_win`).

## Risks

1. **A twin site missed** (research §2.1 lists eight; `TWINS:` search `HomeMenuItem::` and `KRINIK_MAMA` over `src/`
   again before the judge). A missed site draws one order and acts on another — criterion 2 taps every button.
2. **RoundedRaff paging vs the touch grid** (research §2.2, noticed, not verified) — criterion 1 taps in theme 3.
3. **Upstream drift** in `HomeActivity.*` / `CoverGridHomeUi.*` (upstream files): keep the diff to the eight sites.
