# Idea 08 — gather the Sleep options of «Настройки → Экран» into a child menu «Настройки сна»

> **Created:** 2026-11-13 (the owner's request, chat — given while epic 01 phase 1 was under the judge) · **Parent:** — ·
> **Status:** 🔧 built 2026-11-13 on `wip/krinik-debug10` `52212d81`, simulator S3 pass (`testcases/reports/2026-11-13_idea07_08_simulator.md`); open: S6 the on-device guide, the owner's check on the reader · **Outbound:** —

`[OWNER] 2026-11-13 14:44 +03:00 · chat:`

> в настройках экрана много опций кастаельно Сна, собираем их в отдельное дочернее меню
> Настройки сна

## Goal vector (Achieve)

«Настройки → Экран» mixes nine Sleep options with the display ones. They shall live on their own sub-screen
«Настройки сна», reached by one row in «Экран», the way «Настройки очисток экрана» already gathers the cleanup options.

## Recon (2026-11-13, `wip/krinik-debug10`)

- Precedent: `SettingsActivity.cpp` → `sectionFor()` routes settings by their field to a Display sub-screen
  (`SettingsSection::ScreenClean`, `ScreenCalibration`, both past `End` in `SettingsSection.h`); the row that opens a
  sub-screen is `addAction(SettingsSection::Display, StrId::STR_SCREEN_CLEAN_SETTINGS, SettingAction::ScreenCleanSettings)`
  (`SettingsActivity.cpp:151`); the return into a sub-screen goes through `pendingSettingsSubSection`.
- The Display settings (`src/SettingsList.cpp`, category `STR_CAT_DISPLAY`) with their Russian labels
  (`lib/I18n/translations/russian.yaml`):

| Field | Label on the reader | Goes to «Настройки сна» |
|---|---|---|
| `sleepScreen` | «Экран сна» | yes |
| `sleepTimeoutMinutes` | «Сон через» | yes |
| `sleepScreenCoverMode` | «Режим обложки сна» | yes |
| `sleepImageOrder` | «Порядок обложек сна» | yes |
| `sleepOrientation` | «Ориентация заставки сна» | yes |
| `sleepLightLinger` | «Подсветка на засыпании» | yes |
| `sleepScreenCoverFilter` | «Фильтр экрана сна» | yes |
| `quickResumeSleepScreen` | «Возобновление по таймауту» | yes |
| `frontlightRestoreOnWake` | «Подсветка при пробуждении» | yes `[AI]` — the wake from sleep |
| `sleepSettledRedraw` | «Обновлять заставку» | no — stays in «Настройки очисток экрана», where every clean / refresh / redraw setting went by the owner's word 2026-11-05 (the comment over `sectionFor`) |
| `lightRamp`, `frontlightPreciseTemperature`, `hideBatteryPercentage`, `uiTheme`, `screenInverted` | «Плавная подсветка», «Точная температура», «Скрыть % батареи», «Тема интерфейса», «Ночной режим» | no — stay in «Экран» |

## Plan (ordinary — heaviness 0 of 5: one subsystem, the precedent exists, one session)

- [x] S1. `SettingsSection::SleepSettings` past `End`; `sectionFor()` routes the nine fields above; `SettingAction` +
      `addAction(SettingsSection::Display, STR_SLEEP_SETTINGS, …)`; the sub-screen title; `pendingSettingsSubSection`
      return like ScreenClean; string `STR_SLEEP_SETTINGS` = «Настройки сна» (ru) / "Sleep Settings" (en); `[NOT-TESTED]`.
- [x] S2. Judge on the diff before the build.
- [x] S3. (partly — the value change of «Сон через» and the `settings.json` read NOT run; the report says so) Simulator: Settings → «Экран» shows «Настройки сна» and none of the nine; the sub-screen shows the nine in the
      order of the table; changing «Сон через» there and going Back keeps the value (`settings.json` read). Shots read.
- [ ] S4. The web settings page (`src/network/html/SettingsPage.html`) groups by category, not by sub-screen — check it
      still lists the nine (no change expected).
- [x] S5. (`52212d81`) Commit on `wip/krinik-debug10`; the image is the one debug10.
- [ ] S6. The owner's on-device guide `guide_settings_section.xhtml` (→ `РУКОВОДСТВО.epub`) lists the nine under
      «Настройки: Экран»: move them under «Настройки сна» (owner-facing text — voice portrait, check, then his read).

## Decisions made without the owner (open)

- `[AI]` «Подсветка при пробуждении» goes with the Sleep options (it acts on waking from sleep).
- `[AI]` «Обновлять заставку» stays in «Настройки очисток экрана» (his 2026-11-05 grouping of every redraw).
- `[AI]` The row «Настройки сна» is the FIRST row of «Экран»: the sleep options opened that screen before they moved
  («Сон через» second there, the owner's word 2026-11-04 in `SettingsList.cpp`).

## Judge (S2, a fresh agent on the uncommitted diff, 2026-11-13 15:09 +03:00) — no blockers

Routing of the nine matches the table; no other sub-screen loses a field; the sleep-screen / quick-resume coupling
matches by field, both rows move together; `SleepSettings` past `End` breaks no array; English + Russian keys are
enough (other languages fall back). Fixed: the table order (code order: «Подсветка на засыпании» before «Фильтр
экрана сна»), the stale comment in `SettingsList.cpp`, the comment's authorship of «Подсветка при пробуждении»,
"eight" → nine; the row moved to the top of «Экран»; the guide → S6.
