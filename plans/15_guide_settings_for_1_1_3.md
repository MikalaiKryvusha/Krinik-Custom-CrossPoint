# Plan 15 — the on-device guide («РУКОВОДСТВО.epub») describes the KCCP 1.1.3 settings screens as they are

> **Created:** 2026-11-17 · **Parent:** `ideas/08_sleep_settings_submenu.md` → S6; STATUS open work 9; the release-time
> debt for KCCP 1.1.3 · **Status:** 📐 recon done 2026-11-17 15:28 +03:00 (the screens' texts captured on the simulator,
> below); **corrected 2026-11-17 15:45 +03:00** — the G4 draft (`44cbf99`) was built on the stale separate file while the epub holds the
> owner's newer text: the draft reverted, G4 restarts from the epub · **Outbound:** the rewritten chapter → the owner's
> proofreading (owner text), then into the epub on his word

## Goal vector (Achieve)

The owner (and his mother) read the settings chapter of the guide on the reader and find each setting where the
reader shows it, under the name the reader shows. The guide on the reader is `РУКОВОДСТВО.epub` → `OEBPS/readme.xhtml`
(entry mtime 2026-11-05 14:58): its settings chapters already carry the reader's new names and the owner's text for them
(«Плавная подсветка», «Настройки очисток экрана», «Калибровка экрана»…) — `tools/guide_screens_check.py` on it: 1 miss
(«Проверить обновление» stands under «Подключения», the screen has it under «Система»). It lacks what came after it:
the «Настройки сна» sub-screen (idea 08, debug10 — the nine rows are there, flat under «Экран»), «Кнопки в шторке»
(epic 01), «Кнопки домашнего экрана» (epic 05), «Точная температура». The separate file `guide_settings_section.xhtml`
(in the repo since 2026-11-08, its own date unknown) is OLDER in content than the epub (the old names: «Частота
обновления», «Перерисовка меню»…); nothing records what it is for — a drift pair with the epub (owner's question, G5).
Correction 2026-11-17 15:45 +03:00: this paragraph said the opposite (the epub older); the clean §7B pass of the G4 draft found the epub's
text.

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
«Калибровка экрана», both button screens; gone from the reader — «Перерисовка меню».

The other chapters (runs `qa_runs/guide_system`, `guide_reading`, `guide_keys`, `guide_library`, `guide_network`; every
list fits one screen — the swipe shots equal the first ones, the last row ends above the bottom):

- **Система:** Язык · Часы › · Раскладки клавиатуры › · Проверить обновление · Прошивка с SD карты · Показать скрытые
  файлы · Об устройстве. Guide: «Проверить обновления», «Обновление системы с SD-карты», another order.
- **Чтение:** Настройки текста › · Управление шрифтами › · Ориентация чтения (Альбомная 180°) · Изображения (Показать) ·
  Стиль меню чтения (Список) · Настройка строки состояния › · Очистить кэш чтения. Guide has «Словарь» — not on this
  screen (with no dictionary on the card? to read in the code).
- **Кнопки:** Жесты кнопки «Домой» (Настроить) · Боковые кнопки (Назад/Вперёд) · Тачскрин для листания (флажок) ·
  Следующая страница (Тап и свайп) · Предыдущая страница (Тап и свайп) · Открывать меню (Тап) · Боковая долго (Изменить
  ориентацию) · Двойной клик питания: подсветка · Питание коротко (Сон). Guide: «Сенсорное управление чтением», «Долгое
  нажатие», «Короткое нажатие PWR»; «Зоны тапа», «Быстрый возврат из ссылок» — not on this screen.
- **Библиотека:** Использовать метаданные книг · Скрывать прочитанные · Прочитанные в Read. Guide: «Убирать прочитанные
  из недавних», «Прочитанные — в папку Read».
- **Подключения:** Wi-Fi сети › · CrossPoint Sync › · Серверы OPDS › · Плагины (Выключено). «Bluetooth-пульт» is absent
  because the simulator is built without Bluetooth (`PROJECT_ARCHITECTURE_INTERNAL_MAP.md`, the shade) — not a difference.

One level deeper (runs `qa_runs/guide_clock`, `guide_text`, `guide_statusbar`, `guide_homekey`, `guide_sync`):

- **Часы**, **Настройка строки состояния**, **CrossPoint Sync** — the rows match the guide's `›` lines by name.
- **Жесты кнопки «Домой»:** Нажатие (Домой) · Двойное нажатие (Вкл./выкл. подсветку) · Долгое нажатие (Меню). Guide:
  one line «› Действия Home».
- **Настройки текста:** tabs Шрифт (Noto Sans) · Размер (12 / 14 / 16 / 18 pt) · Разметка (Межстрочный интервал +10% ·
  Межсловный интервал 100% · Межбуквенный интервал 0 px · Доп. интервал абзаца · Отступ абзаца 5 · Выравнивание «Стиль
  книги» · Поля 5) · Стиль (Фокусное чтение · Hyphenation · Embedded Style · Text Anti-Aliasing, the last three «(no
  preview)», untranslated) — the names match the guide's `›` lines.

## Steps

- [x] G1. Capture the other settings screens the same way; extend the differences list. (The six chapters and the
      Экран sub-screens done 2026-11-17 15:30 +03:00; the deeper sub-screens 2026-11-17 15:31 +03:00 and the text tabs
      15:32 +03:00 (log mtime).)
- [x] G2. Read each changed setting's options in `src/SettingsList.cpp` and the Russian strings. Read so far (2026-11-17 15:33 +03:00,
      `SettingsList.cpp` at `de8feb20`, `lib/I18n/translations/russian.yaml`):
      - Плавная подсветка: ВЫКЛ · 200 мс · 500 мс · 1000 мс (`lightRamp`, :56).
      - Очищать каждые: 1 стр. · 5 стр. · 10 стр. · 15 стр. · 30 стр. · Никогда (`refreshFrequency`, :85).
      - Очищать домашний экран, Очищать после шторки: ВЫКЛ · ВКЛ (:90, :92).
      - Обновлять заставку, Обновлять картинки: ВЫКЛ · через 1 мин · через 2 мин · через 5 мин (:100, :103; the old
        on/off keys migrate in `fromJson()`).
      - Калибровка картинок, Калибровка книг: флажки (:95, :97).
      - Боковая долго: Ничего · Пропуск главы · Изменить ориентацию (:215).
      - **Device-only rows the simulator does not show** (compile-time `#if`, the device envs define them):
        «Точная температура» (флажок, `FREEINK_FRONTLIGHT_DITHER && FREEINK_DEVICE_X4PRO`, `platformio.ini` — the two
        `x4pro-krinik*` envs) — on the reader it stands in «Экран» right after «Плавная подсветка» (emit order :56 → :60);
        «Вибрация» — `FREEINK_CAP_HAPTIC` = Metalio only, not on the X4 Pro; «Теплота» — `FREEINK_CAP_WARMLIGHT` is on
        for the X4 Pro, but the setting has no category (`SettingsList.cpp:265`), so no settings screen shows it (the
        shade's slider). So criterion 1's capture is the SIMULATOR's list; the device list = the capture + «Точная
        температура» + «Bluetooth-пульт» (the simulator is built without Bluetooth).
- [x] G3. The comparison script (criteria 1–2) in `tools/`, proven red on today's section. `tools/guide_screens_check.py`
      (criterion 2: every guide name on a captured screen of its chapter; criterion 1 stays the judge's read):
      today's section → 16 names not shown (the renamed and gone rows above, plus «Словарь», «Действия Home», «URL
      сервера синхронизации» — the sync screen draws that row's value only); `--selftest` OK, red on a no-gap mutant.
- [x] G4. Rewrite the section by the portrait; voice-lint + a clean §7B pass; the judge on criterion 3.
      First draft (`44cbf99`, on the separate file) REVERTED ≈ 2026-11-17 15:44 +03:00: its base was the stale file; the
      clean §7B pass found the owner's newer text in the epub. Restart: base = the epub's settings chapters
      (`OEBPS/readme.xhtml`), the owner's lines kept as they are; changes only where the reader differs — the «Настройки
      сна» sub-screen as `›` rows, the rows «Кнопки в шторке», «Кнопки домашнего экрана», «Точная температура»,
      «Проверить обновление» under «Система». Facts the pass confirmed, to use: two calibration files —
      `/.crosspoint/panel_curve.txt` for pictures and own sleep images, `/.crosspoint/panel_curve_book.txt` for pictures
      in books (`PanelCurve.h:17,24`), the built-in curve without a file; «Точная температура» 9 % / 10 %
      (`HalFrontlight.cpp:50–52`, the comment «fractional warm/cool mixing» :49); «Кнопки в шторке» keeps at least one
      button on (`ShadeTiles.h:76`); the clean screen's own note (`STR_SCREEN_CLEAN_NOTE`). Then voice-lint, a clean
      §7B pass, the judge on criterion 3.
      Restart done (the draft in `guide_settings_section.xhtml` = the epub's six settings chapters, the owner's lines
      verbatim; new: «Настройки сна» line + the nine rows in the screen's order, «Кнопки в шторке», «Кнопки домашнего
      экрана», «Точная температура» [AI]; «Настройки очисток экрана» «последний» → «предпоследний» [AI-ed]);
      `guide_screens_check.py` 0 misses (the old file 11); voice-lint 6 hits, all in the owner's epub lines kept
      verbatim, none in the [AI] lines. The clean §7B pass + judge on the [AI] lines (2026-11-17 15:58 +03:00): the
      orders, defaults, 9 %, the one-button rule, the long taps confirmed by file:line; fixed — «▲ ▼» (no such glyphs in
      the reader's fonts; the screens say «стрелки») → «стрелки», «со всеми настройками сна» (contradicted: «Обновлять
      заставку» stands in the clean screen), «без него» (ambiguous) → «целыми шагами», «Настройки» always on Home said,
      «сразу на этой кнопке» → «строка этой кнопки уже выделена». Check 0 misses; voice hits 6, all in owner lines.
- [ ] G5. The owner's proofreading (homework); then into `РУКОВОДСТВО.epub` (no build tool exists: `OEBPS/readme.xhtml`
      is edited and re-zipped — a tool for that is part of this step).

## Risks

1. **No build route.** The epub is edited by hand today; a zip written wrong (mimetype not first) does not open —
   `tools/epub_lint.mjs` checks it.
2. **The reader's cache** keeps the old guide's layout under the same path (`Epub.cpp:29`; plan 14, risk 2): the
   homework says how to clear it.

## Decisions made without the owner

- `[AI]` The guide follows the screens' own names and order (the reader is the source of truth; the guide describes it).
