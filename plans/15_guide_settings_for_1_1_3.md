# Plan 15 — the on-device guide («РУКОВОДСТВО.epub») describes the KCCP 1.1.3 settings screens as they are

> **Created:** 2026-11-17 · **Parent:** `ideas/08_sleep_settings_submenu.md` → S6; STATUS open work 9; the release-time
> debt for KCCP 1.1.3 · **Status:** 📐 recon done 2026-11-17 15:28 +03:00 (the screens' texts captured on the simulator, below); no text
> written yet · **Outbound:** the rewritten section → the owner's proofreading (owner text), then into the epub on his word

## Goal vector (Achieve)

The owner (and his mother) read the settings chapter of the guide on the reader and find each setting where the
reader shows it, under the name the reader shows. Today the chapter «Настройки: Экран» is one flat list written for the
2026-11-05 build (`РУКОВОДСТВО.epub` → `OEBPS/readme.xhtml`); the separate source `guide_settings_section.xhtml`
(2026-11-08) is newer than the epub and older than debug10 (idea 08's sub-screens), epic 01 («Кнопки в шторке») and
epic 05 («Кнопки домашнего экрана»).

## Acceptance criteria

1. **Every row the reader shows has its line.** For «Экран» and its sub-screens: each row in the captured screen text
   below has one line in the guide, under its screen, in the screen's order, with the reader's own name. Check: a script
   compares the `[SIM] SCREEN:` lines of a fresh capture with the guide's `<b>…</b>` names → 0 missing, 0 extra.
2. **No line describes a setting the reader no longer shows** (e.g. «Перерисовка меню» — absent from every screen
   captured below). Check: the same script, the reverse direction.
3. **Values from the code.** Every value named in a line («через 5 мин», «30 стр.») is one of the option list in
   `SettingsList.cpp` / the Russian translation. Check: the judge reads each line against the code.
4. **The owner's read.** The text is written BY the owner's portrait, checked (`kaif-voice-lint` + a clean §7B pass) and
   proofread by the owner before it enters the epub.

## Recon — the screens as the simulator shows them (2026-11-17, `wip/kccp-1.1.3-debug2` `de8feb20`)

Captured with `CROSSPOINT_SIM_SCREEN_TEXT=1` (runs `qa_runs/guide_display`, `guide_sleep`, `guide_clean`,
`guide_calib`; card `qa_runs/sd_template`, Lyra):

- **Экран:** Настройки сна › · Кнопки в шторке › · Кнопки домашнего экрана › · Плавная подсветка (200 мс) · Скрыть %
  батареи (Никогда) · Тема интерфейса (Lyra) · Ночной режим (флажок) · Настройки очисток экрана › · Калибровка экрана ›
- **Настройки сна:** Экран сна (Свой) · Сон через (10 мин) · Режим обложки сна (Вписать) · Порядок обложек сна (По
  порядку) · Ориентация заставки сна (По картинке) · Подсветка на засыпании (5 сек) · Фильтр экрана сна (Нет) ·
  Возобновление по таймауту · Подсветка при пробуждении
- **Настройки очисток экрана:** an intro («Очистки экрана выполняются периодически, помогают убрать следы и ореолы
  прошлых экранов.») · Очищать каждые (30 стр.) · Очищать домашний экран · Очищать после шторки · Обновлять заставку
  (через 5 мин) · Обновлять картинки (через 2 мин)
- **Калибровка экрана:** an intro (KEINKT Calibrator, the ticks) · Калибровочный экран картинок › · Калибровочный экран
  книг › · Калибровка картинок · Калибровка книг
- **Кнопки в шторке**, **Кнопки домашнего экрана:** rows with ▲ ▼ and a tick (epic 01 Ф2, epic 05 Ф4).

Differences from `guide_settings_section.xhtml` seen so far: renamed — «Частота обновления» → «Очищать каждые»,
«Очищать главный экран» → «Очищать домашний экран», «Перерисовка заставки сна» → «Обновлять заставку» (a time, not ВКЛ),
«Перерисовка картинок» → «Обновлять картинки» (a time); missing in the guide — «Плавная подсветка», the whole
«Калибровка экрана», both button screens; gone from the reader — «Перерисовка меню». The other chapters («Система»,
«Чтение», «Кнопки», «Библиотека», «Подключения») are not captured yet.

## Steps

- [ ] G1. Capture the other settings screens the same way; extend the differences list.
- [ ] G2. Read each changed setting's options in `src/SettingsList.cpp` and the Russian strings.
- [ ] G3. The comparison script (criteria 1–2) in `tools/`, proven red on today's section.
- [ ] G4. Rewrite the section by the portrait; voice-lint + a clean §7B pass; the judge on criterion 3.
- [ ] G5. The owner's proofreading (homework); then into `РУКОВОДСТВО.epub` (no build tool exists: `OEBPS/readme.xhtml`
      is edited and re-zipped — a tool for that is part of this step).

## Risks

1. **No build route.** The epub is edited by hand today; a zip written wrong (mimetype not first) does not open —
   `tools/epub_lint.mjs` checks it.
2. **The reader's cache** keeps the old guide's layout under the same path (`Epub.cpp:29`; plan 14, risk 2): the
   homework says how to clear it.

## Decisions made without the owner

- `[AI]` The guide follows the screens' own names and order (the reader is the source of truth; the guide describes it).
