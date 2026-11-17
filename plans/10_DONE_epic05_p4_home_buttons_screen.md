# Plan 10 — epic 05, phase 4: the screen «Кнопки домашнего экрана»

> **Created:** 2026-11-14 · **Parent:** `plans/05_EPIC_home_buttons.md` → «Ф4 — экран «Кнопки домашнего экрана»» ·
> **Status:** ✅ DONE 2026-11-17 10:36 +03:00 — built and run 2026-11-14 17:38 +03:00 (firmware `2fa20f3f`; the shade C1–C8 and H1–H4 pass); H5 closed by interview #006 → A, firmware `da382c2f` · **Outbound:** —

## Goal vector (Achieve)

The owner sets which Home buttons are on and their order on a Settings screen that looks and works like «Кнопки в
шторке»; «Настройки» has ▲ ▼ and no checkbox (interview #004, Q1); the screen's row sits in «Настройки → Экран» right
under «Кнопки в шторке», named «Кнопки домашнего экрана» (Q3).

Anchor (meta-plan, Ф4): «Экран по образцу «Кнопки в шторке»: строка — значок, имя, ▲ ▼, чекбокс; в строке «Настройки»
чекбокса нет. Строка, которая открывает этот экран, стоит в «Настройки → Экран» сразу под строкой «Кнопки в шторке».
«Назад» возвращает туда, откуда экран открыт. Новые строки интерфейса на русском и английском».

## Decision at the fork

- `FORK: the screen's code <a near-copy of ShadeTilesActivity | one shared base for both screens> · price of error: a
  copy is a pair of twins (a fix lands in one, the other keeps the defect — EXP-0005, EXP-0016); a shared base risks the
  tested shade screen · consulted: BUG_FIXING_FRAMEWORK.md «fix by form — one shared component instead of clones»,
  research 2026-11-13_idea06 §3 (both options named)` → one shared base `ToggleRowsActivity`; the shade screen's
  cases (epic 01 Ф2 C1–C8, Ф3 long-tap entry) are re-run on the refactored screen.
- `[OWNER]` interview #006, Q1 → **A** (2026-11-17 10:18 +03:00, recorded by the review contour): the mama row reads
  «Для Мамы» on this screen only; Home keeps «Для любимой Мамы». Applied in step P4.7.

## Acceptance criteria (phase)

1. **Rows** (meta-plan criteria 1–3). WHEN the screen opens from «Настройки → Экран», it shall show one row per Home
   button of this build in the stored order — icon (the Home glyph), name, ▲, ▼, a checkbox; «Настройки» with no
   checkbox. Check: shot (a card with no plugins and no OPDS server: plain 6 rows, mama 7 incl. «Для любимой Мамы»; with them 7 / 8).
2. **Toggle and move.** A tap on a row's checkbox switches it, ▲ / ▼ move it; Back saves `homeButtons` and Home shows
   the change. Check: `settings.json` read; a Home shot.
3. **«Настройки» stays on.** A tap on the «Настройки» row changes nothing. Check: shot; no `-settings` in the key.
4. **Back** returns to «Настройки → Экран» (criterion 10). Check: `Entering activity:` lines; shot.
5. **The shade screen is unchanged** (the shared base): its epic 01 Ф2 cases C1–C8 pass again. Check: the Ф2 scripts.
6. **Strings** in Russian and English; the Settings row only on a touch board (as «Кнопки в шторке»).

## Steps

- [x] P4.1 `ToggleRowsActivity` (`src/activities/settings/`): the drawing, the input, the stale-tap guard, portrait while
      open, save-on-exit — with virtual rows (count, shown, on, has-checkbox, can-turn-off, icon, name, move, title,
      note, save). `ShadeTilesActivity` derives from it unchanged in behaviour. Anchor: «Экран по образцу «Кнопки в шторке»».
- [x] P4.2 `HomeScreenButtonsActivity` (named `HomeButtonsActivity` in the draft): rows from `SETTINGS.homeButtons`, «Настройки» without a checkbox (`homemenu::canToggle`),
      the plugins/OPDS row labelled as Home labels it, the Home glyphs; strings `STR_HOME_BUTTONS`, `STR_HOME_BUTTONS_NOTE`.
- [x] P4.3 `SettingsActivity`: `SettingAction::HomeButtons` right under `ShadeTiles` (touch boards).
- [x] P4.4 Judge BEFORE the build; fix findings.
- [x] P4.5 Host suite; simulator: criteria 1–6 (`testcases/TC_epic05_p4_home_buttons_screen.md`) + the shade C1–C8; run
      report.
- [x] P4.6 Commit (`2fa20f3f`), tick Ф4 (🟡 on #006), write the Ф5 plan (with the Ф2 judge's note: Home refreshes `shownButtons` on return).
- [x] P4.7 Interview #006 → A (done 2026-11-17 10:36 +03:00, firmware `da382c2f`, report
      `testcases/reports/2026-11-17_epic05_p4_mama_label.md`): `HomeScreenButtonsActivity::rowName` returns «Для Мамы» for the mama row; judge → mama
      simulator build → H5 again (before: `qa_runs/mama_label_before/shots/rows.webp` «Для любимой Ма…») → host suite →
      commit. Anchor: «Строка, которая открывает этот экран…» / risk 3 («a shorter name is the owner's word»).

## Risks

1. **The refactor changes the shade screen** — guarded by re-running its C1–C8 (criterion 5).
2. **Hit capacity** 24: the mama build has 8 rows = 7 × 3 + 2 (no checkbox hit on «Настройки») = 23 — a static_assert per
   screen.
3. **«Для любимой Мамы» cut** by the arrows (16 letters, as «Ориентация чтения» was) — read on the shot; a shorter name is
   the owner's word (an identity string), asked only if it is cut.

## Decisions made without the owner

- `[AI]` One shared base `ToggleRowsActivity` for both screens (the FORK line above).
- `[AI]` The plugins/OPDS row is shown only while Home draws it (`homeLibrarySlotExists()`), the Ф4 judge's finding 1 —
  the meta-plan's criterion 2 (6 rows) holds.
- `[AI]` The screen's row is on touch boards only, as «Кнопки в шторке» (the judge's finding 8, signed here).
- `[AI]` Names `HomeScreenButtons*` and `rowName()` (the judge's findings 5, 6).
- The mama row's name — the owner's word, interview #006 → A (2026-11-17 10:18 +03:00): «Для Мамы» on this screen.
- `[AI]` #006 (a label) does not block Ф5 (the long tap): Ф5 builds on the screen as it is; the label lands when answered.
- `[AI]` «Для Мамы» stays a literal in `rowName`, as Home's «Для любимой Мамы» is a literal: the mama build is
  Russian-only, and an i18n key for one build's button would be a string with no English reader.

## ✅ STATUS: DONE (2026-11-17 10:36 +03:00)

Ф4 is closed: the screen «Кнопки домашнего экрана» works on the simulator in the plain and mama builds (H1–H5), the shade
screen on the shared base keeps its C1–C8. Not verified on the readers (Ф6, with the image). Next: plan 11, Ф5 — the long
tap on a Home button.
