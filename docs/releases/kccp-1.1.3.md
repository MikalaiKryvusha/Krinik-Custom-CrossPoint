**English** · [Русский ↓](#русский)

**KCCP — Krinik Custom CrossPoint**: a custom build of [CrossPoint Reader](https://github.com/crosspoint-reader/crosspoint-reader) 2.0.0 for the **Xteink X4 Pro** (panel controller UC8279). Checked on the CrossPoint simulator; the 1.1.3 debug builds run on the author's reader. **Release build — no debug-only features.**

<i>❤️ Dedicated to my mother, Sofia Fadeevna Kryvusha — a great reader and lover of books, who gave me my love of reading.</i>

## What's new

Changes since [KCCP 1.1.2](https://github.com/MikalaiKryvusha/Krinik-Custom-CrossPoint/releases/tag/kccp-1.1.2).

**Control Center**
- Buttons are yours: pick, order and switch off each one in **Settings → Display → Control Center buttons**; Sleep and Flashlight are new; a long tap on a button in the Control Center opens that screen.
- With every button off the Control Center shows only the light controls.
- Buttons by default: Night mode, Orientation, Flashlight, Sleep.
- The buttons are spaced evenly from edge to edge.
- "Sleep" shows the tap before the reader falls asleep.

**Home screen**
- "Sleep" item; it shows its selection before the sleep starts.
- Buttons are yours: pick and order them in **Settings → Display → Home buttons**; "Settings" always stays; a long tap on a Home button opens that screen.
- The button list scrolls when the buttons do not fit; in Mom's build "For beloved Mom" is last by default.
- Cover Grid stays positive after the night switch in the Control Center.

**Pictures**
- A tap on a picture in a book opens it full screen.
- A long tap on the right half turns the picture clockwise, on the left half counterclockwise; taps, swipes and keys follow the picture as it stands.
- A picture opens turned by its shape: a wide one in a portrait reader, a tall one in a landscape reader.

**Reading**
- A picture and its caption stay on one page in books that mark them as a figure; the caption is centred, without a first-line indent.
- A footnote link whose target wraps the whole note opens the note's page (the notes of «Gödel, Escher, Bach» used to open on the first page of the notes).
- The back link at the start of a note returns to the text; Back does not walk the same jump again.

**Frontlight and sleep**
- "Precise temperature" (Settings → Display, on by default): the cold and warm channels mix in fractional steps only at brightness ≤ 9 %, in whole steps from 10 %.
- Sleep settings live in their own menu: **Settings → Display → Sleep settings**.
- The sleep-screen redraw is timed from the sleep; a press that does not wake no longer shifts or cancels it.
- Light lingering at sleep: with Short Power Button ≠ Sleep only a hold cancels the sleep, a click does not.

## Install

1. Put `cp-2.0.0-krinik-1.1.3.bin` on the card, for example in `/.firmware/`; keep the previous firmware beside it for a rollback.
2. **Settings → System → Firmware from SD card** → choose the file. The reader checks the header, the checksum and SHA256.
3. `RUKOVODSTVO-krinik.epub` — the guide to every setting, in Russian: put it on the card and open it as a book.

The first time each book is opened after the update, its chapters are laid out again. **Do not accept "Check for updates"** — it installs the official version and replaces KCCP. About shows `cp-2.0.0-krinik-1.1.3`.

## Known

- A heading can stay alone at the bottom of a page, and a heading gets a first-line indent — next version.
- The guide `RUKOVODSTVO-krinik.epub` is the 1.1.2 edition: the new 1.1.3 screens are in the next edition.
- The Control Center's night button: pictures under the open sheet stay negative until the sheet closes.
- A screenshot in dark mode is saved wrong.
- True gray book images in dark mode (now dithering).

## Contribution to CrossPoint

| PR | What | State |
|---|---|---|
| [#4329](https://github.com/crosspoint-reader/crosspoint-reader/pull/4329) | Recent-book cover stays positive after a theme switch | ✅&nbsp;merged |
| [#4330](https://github.com/crosspoint-reader/crosspoint-reader/pull/4330) | Empty-cover text stays inside the frame (Classic) | ✅&nbsp;merged |
| [#4331](https://github.com/crosspoint-reader/crosspoint-reader/pull/4331) | SD card size, used and free space in About | ✅&nbsp;merged |
| [#4328](https://github.com/crosspoint-reader/crosspoint-reader/pull/4328) | Footnote link opens the page of the note's first line | 💡&nbsp;open |
| [#4332](https://github.com/crosspoint-reader/crosspoint-reader/pull/4332) | Sleep Image Order: Random or In Order | 💡&nbsp;open |
| [#4375](https://github.com/crosspoint-reader/crosspoint-reader/pull/4375) | Screen cleaning settings grouped | 💡&nbsp;open |
| [#4376](https://github.com/crosspoint-reader/crosspoint-reader/pull/4376) | Optional delayed image redraws | 💡&nbsp;open |
| [#4377](https://github.com/crosspoint-reader/crosspoint-reader/pull/4377) | Calibrate picture and book image tones | 💡&nbsp;open |

Roadmap and documents — [README](https://github.com/MikalaiKryvusha/Krinik-Custom-CrossPoint#roadmap) · firmware source — `crosspoint-reader-kccp-1.1.3-src.tar.gz` and `freeink-sdk-kccp-1.1.3-src.tar.gz` (attached) · sister project — [KEINKT](https://github.com/MikalaiKryvusha/KEINKT).

`cp-2.0.0-krinik-1.1.3.bin` SHA256 `0f95815210a6d19d856a984094250f5e410695102f400e30891d1ce4a73edf5d`

---

## Русский

**KCCP — Krinik Custom CrossPoint**: своя сборка [CrossPoint Reader](https://github.com/crosspoint-reader/crosspoint-reader) 2.0.0 для **Xteink X4 Pro** (контроллер панели UC8279). Проверено на симуляторе CrossPoint; отладочные сборки 1.1.3 работают на читалке автора. **Релизная сборка — без отладочных функций.**

<i>❤️ Проект посвящён моей маме — Кривуше Софии Фадеевне, очень большому читателю-книголюбу, которая привила мне любовь к чтению книг.</i>

## Что нового

Изменения после [KCCP 1.1.2](https://github.com/MikalaiKryvusha/Krinik-Custom-CrossPoint/releases/tag/kccp-1.1.2).

**Шторка**
- Кнопки выбираете вы: выбор, порядок и выключение каждой — в **Настройки → Экран → Кнопки в шторке**; добавлены «Сон» и «Фонарик»; долгий тап по кнопке в шторке открывает этот экран.
- Если выключить все кнопки, в шторке остаются только регуляторы подсветки.
- Кнопки по умолчанию: «Ночной режим», «Ориентация», «Фонарик», «Сон».
- Кнопки стоят с равными промежутками от края до края.
- «Сон» показывает нажатие до того, как читалка уснёт.

**Главный экран**
- Пункт «Сон»; он выделяется до начала сна.
- Кнопки выбираете вы: выбор и порядок — в **Настройки → Экран → Кнопки домашнего экрана**; «Настройки» остаются всегда; долгий тап по кнопке главного экрана открывает этот экран.
- Список кнопок прокручивается, если кнопки не помещаются; в маминой сборке «Для любимой Мамы» по умолчанию последняя.
- «Сетка обложек» не уходит в негатив после «Ночи» в шторке.

**Картинки**
- Тап по картинке в книге открывает её на весь экран.
- Долгий тап по правой половине поворачивает картинку по часовой стрелке, по левой — против; тапы, свайпы и кнопки работают так, как стоит картинка.
- Картинка открывается повёрнутой по своей форме: широкая — на книжной читалке, высокая — на альбомной.

**Чтение**
- Картинка и подпись к ней держатся на одной странице в книгах, где они размечены как рисунок; подпись по центру, без красной строки.
- Ссылка на сноску, цель которой охватывает всю сноску, открывает страницу сноски (в «Гёдель, Эшер, Бах» сноски открывались на первой странице примечаний).
- Обратная ссылка в начале сноски возвращает в текст; «Назад» не проходит этот переход заново.

**Подсветка и сон**
- «Точная температура» (Настройки → Экран, по умолчанию включена): холодный и тёплый каналы смешиваются дробными шагами только при яркости до 9 %, с 10 % — целыми.
- Настройки сна в своём меню: **Настройки → Экран → Настройки сна**.
- Перерисовка заставки отсчитывается от ухода в сон; нажатие, которое не будит, её не сдвигает и не отменяет.
- Подсветка на засыпании: при «Короткое нажатие PWR» не «Сон» сон отменяет только удержание, щелчок — нет.

## Установка

1. Положите `cp-2.0.0-krinik-1.1.3.bin` на карту, например в `/.firmware/`; рядом — прежнюю прошивку для отката.
2. **Настройки → Система → Прошивка с SD карты** → выберите файл. Читалка проверяет заголовок, контрольную сумму и SHA256.
3. `RUKOVODSTVO-krinik.epub` — руководство по всем настройкам: положите на карту и откройте как книгу.

При первом открытии каждой книги после обновления читалка заново раскладывает её главы. **Не соглашайтесь на «Проверить обновление»** — читалка поставит официальную версию и затрёт KCCP. В «Об устройстве» — `cp-2.0.0-krinik-1.1.3`.

## Известное

- Заголовок может остаться один внизу страницы, и у заголовка есть красная строка — в следующей версии.
- Руководство `RUKOVODSTVO-krinik.epub` — издание 1.1.2: новые экраны 1.1.3 войдут в следующее издание.
- «Ночь» в шторке: картинки под открытой шторкой остаются в негативе, пока шторка не закроется.
- Снимок экрана в тёмной теме сохраняется неверно.
- Настоящие серые картинки в книге в тёмной теме (сейчас дизеринг).

## Вклад в CrossPoint

| PR | Что | Состояние |
|---|---|---|
| [#4329](https://github.com/crosspoint-reader/crosspoint-reader/pull/4329) | Обложка последней книги остаётся позитивной после смены темы | ✅&nbsp;принят |
| [#4330](https://github.com/crosspoint-reader/crosspoint-reader/pull/4330) | Текст пустой обложки не выходит за рамку (Classic) | ✅&nbsp;принят |
| [#4331](https://github.com/crosspoint-reader/crosspoint-reader/pull/4331) | Объём, занятое и свободное место SD-карты в «Об устройстве» | ✅&nbsp;принят |
| [#4328](https://github.com/crosspoint-reader/crosspoint-reader/pull/4328) | Ссылка на сноску открывает страницу её первой строки | 💡&nbsp;открыт |
| [#4332](https://github.com/crosspoint-reader/crosspoint-reader/pull/4332) | Порядок заставок сна: случайно или по порядку | 💡&nbsp;открыт |
| [#4375](https://github.com/crosspoint-reader/crosspoint-reader/pull/4375) | Настройки очисток экрана в одном меню | 💡&nbsp;открыт |
| [#4376](https://github.com/crosspoint-reader/crosspoint-reader/pull/4376) | Отложенная перерисовка картинок | 💡&nbsp;открыт |
| [#4377](https://github.com/crosspoint-reader/crosspoint-reader/pull/4377) | Калибровка тонов картинок и иллюстраций в книгах | 💡&nbsp;открыт |

Дорожная карта и документы — [README](https://github.com/MikalaiKryvusha/Krinik-Custom-CrossPoint#дорожная-карта) · исходники прошивки — `crosspoint-reader-kccp-1.1.3-src.tar.gz` и `freeink-sdk-kccp-1.1.3-src.tar.gz` (вложены) · проект-побратим — [KEINKT](https://github.com/MikalaiKryvusha/KEINKT).

`cp-2.0.0-krinik-1.1.3.bin` SHA256 `0f95815210a6d19d856a984094250f5e410695102f400e30891d1ce4a73edf5d`
