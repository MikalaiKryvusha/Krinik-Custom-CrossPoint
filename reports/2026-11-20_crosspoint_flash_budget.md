# Чем занята флеш-память прошивки CrossPoint: upstream develop, X4 Pro

> **Created:** 2026-11-20 · **Parent:** слово владельца в чате 2026-11-20 09:50 ·
> **Status:** ✅ замер выполнен 2026-11-20 (upstream develop `3331d189`, env `x4pro`) · **Outbound:** —

## Что измерено

- **Исходники:** оригинальный CrossPoint Reader, `crosspoint-reader/crosspoint-reader`, ветка `develop`,
  коммит `3331d18967878ce208ad0cf321a856039db6748e` от 2026-11-19 16:27 −05:00
  («fix(sleep): clear sleep image when the device replaces it (#4542)»); подмодуль `freeink-sdk` на коммите
  `634a3f8c067a3714a6a7c622015138af096ab5d2`, который закреплён в этом коммите upstream.
- **Сборка:** env `x4pro` (Xteink X4 Pro, ESP32-S3, 16 МБ флеша, 8 МБ PSRAM): pioarduino 55.03.311,
  framework-arduinoespressif32 3.3.11, ESP-IDF 5.5.5, GCC xtensa 14.2.0. В `x4pro` включены
  `LOG_LEVEL=2` и `ENABLE_SERIAL_LOG`; релизный env `x4pro-gh_release` (`LOG_LEVEL=1`) не замерялся.
- **Раздел:** `partitions.csv`, `app0` = `0x640000` = 6 553 600 байт (6400 КБ); второй слот OTA `app1` того же
  размера.
- **Единица:** КБ = 1024 байта. Проценты считаются от раздела `app0`.

## Итог

| Что | Байт | КБ | % раздела |
|---|---:|---:|---:|
| Образ `firmware.bin` | 5 505 808 | 5376,8 | **84,01** |
| Свободно в разделе `app0` | 1 047 792 | 1023,2 | 15,99 |
| Раздел `app0` | 6 553 600 | 6400,0 | 100 |

Образ по секциям ELF (все секции с флагом ALLOC и типом PROGBITS):

| Секция | Что это | Байт | КБ |
|---|---|---:|---:|
| `.flash.text` | код, исполняемый из флеша | 2 772 228 | 2707,3 |
| `.flash.rodata` | константы: шрифты, строки, словари, таблицы | 2 590 140 | 2529,4 |
| `.iram0.text` + `.iram0.vectors` | код, копируемый в IRAM при старте | 106 643 | 104,1 |
| `.dram0.data` | начальные значения переменных в DRAM | 31 539 | 30,8 |
| `.eh_frame` | таблицы раскрутки стека | 4 756 | 4,6 |
| `.flash.appdesc` | описатель приложения | 256 | 0,3 |
| `.rtc.text`, `.rtc.force_fast`, `.rtc.force_slow` | код и данные RTC | 128 | 0,1 |
| **Сумма секций** | | **5 505 690** | **5376,6** |

Сверка суммы:

| Шаг | Байт |
|---|---:|
| Разнесено по блокам (входные секции из линкер-карты + `*fill*`) | 5 505 686 |
| Не разнесено: хвост `.eh_frame` без входной секции | 4 |
| = сумма секций ELF | 5 505 690 |
| + формат образа esptool: заголовок 24, семь заголовков сегментов 56, выравнивание сегментов 2, контрольная сумма 4, SHA-256 32 | 118 |
| = `firmware.bin` | 5 505 808 |

ОЗУ, коротко: статические DRAM-данные 111 828 байт (`.dram0.data` 31 539 + `.dram0.bss` 80 288 + `.noinit` 1),
по счёту PlatformIO 34,1 % из 327 680; по счёту `esp_idf_size` область DIRAM занята на 202 086 из 341 760 байт
(59,1 %, вместе с IRAM-кодом, размещённым в DIRAM), область IRAM 16 384 из 16 384. RTC SLOW: `.rtc_noinit`
5532 байта. Статических секций в PSRAM нет: PSRAM работает только как куча во время работы.

## Флеш по функциональным блокам

Сумма блоков — 5 505 686 байт (5376,6 КБ, 84,0 % раздела). Строки таблицы округлены до 0,1 КБ, и сумма строк
расходится с итогом на десятые доли.

| Блок | Что входит | Флеш, КБ | % раздела | Строк .c/.cpp | Крупнейшие части, КБ |
|---|---|---:|---:|---:|---|
| Встроенные растровые шрифты | 21 начертание: NotoSans 12/14/16/18 pt × обычный, жирный, курсив, жирный курсив (текст книги, 2 бита, сжатые); Ubuntu 8, 10, 12 pt (интерфейс, 1 бит, без сжатия) | **1207,2** | **18,9** | — (данные в `.h`) | NotoSans 895,4 (18 pt 259,1; 16 pt 234,3; 14 pt 213,1; 12 pt 188,9); Ubuntu 311,8 (ubuntu_12_bold 74,3); по видам данных: растры глифов 700,7, таблицы глифов 370,5, кернинг 121,6, интервалы, группы, лигатуры и описатели шрифтов 14,5 |
| Wi-Fi и TCP/IP | драйвер Wi-Fi, WPA, PHY, lwIP, esp_netif, mDNS, Arduino WiFi/Network, экран выбора сети | **549,7** | **8,6** | 10 256 | драйвер Wi-Fi 217,0 (net80211 141,2; pp 60,7); lwIP + esp_netif 141,6; wpa_supplicant 60,2; радио PHY (общее с Bluetooth) 39,4; mDNS и provisioning 33,8; Arduino WiFi/Network + экран выбора сети 57,6 |
| Экраны, меню, темы и функции чтения | `src/activities`, `src/components`, FreeInkUI, LibraryIndex, настройки, словарь, цитаты, закладки, `main.cpp` | **541,8** | **8,5** | 31 037 | экраны чтения 165,8 (EpubReaderActivity 44,1); каркас UI 144,1 (FreeInkUI 23,9; клавиатура 18,8; BaseTheme 18,1); главный экран, библиотека, файлы 109,2 (FileBrowserActivity 32,0; LibraryListActivity 26,2); настройки 86,1 (SettingsList 21,0); экран сна и загрузки 22,1; `main.cpp` (setup/loop) 14,6 |
| Строки интерфейса (i18n) | 35 языков × 651 ключ, UTF-8 без сжатия | **432,1** | **6,8** | 158 052 (сгенерированный `I18nStrings.cpp`) | строки 382,0 (русский 20,0; иврит 16,4; английский 10,9); таблицы смещений 44,5 (35 × 1302 байта); код и имена языков 5,6 |
| Система | ядро Arduino, ESP-IDF (чип, прерывания, сон, такты, куча, MMU/PSRAM, VFS, события), FreeRTOS, NVS, флеш, coredump, libc/libm/libgcc/libstdc++ | **402,1** | **6,3** | 892 (свои утилиты; ESP-IDF — готовые `.a`) | ESP-IDF 135,0 (esp_hw_support 36,6; hal 20,1; esp_system 17,9; heap 13,0); C/C++ рантайм 122,0 (libc 73,4; libstdc++ 29,8, из него `floating_from_chars` 20,2); NVS, флеш, разделы, coredump 55,7; ядро Arduino 52,9; FreeRTOS 25,6; Preferences, Serialization, Logging, Memory 10,9 |
| Переносы слов | словари-trie 11 языков и алгоритм Лианга | **351,1** | **5,5** | 1 225 (словари — в `.h`) | словари 343,2: немецкий 201,4; русский 32,6; английский 26,3; шведский 23,0; украинский 20,8; польский 15,2; испанский 13,3; французский 6,8; итальянский, финский, португальский 3,8; код 7,0 |
| Шрифтовой движок | TTF/OTF с карты (FreeType), шрифты с SD, шейпинг OpenType, bidi, отрисовка | **281,4** | **4,4** | 17 081 | FreeType 127,3 (autofit 44,8; sfnt 40,0; truetype 19,0; base 17,6); EpdFont 62,3 (SdCardFont 19,6); OtShaper 42,2; GfxRenderer 32,1; FreeInkFont 9,2; MiniBidi 8,2 |
| Книги: EPUB и другие форматы | разбор XHTML/OPF/TOC, CSS, вёрстка строк и страниц, кэш книги, expat, ZIP/inflate, TXT, XTC, UTF-8 | **266,1** | **4,2** | 27 594 | EPUB 175,6 (ChapterHtmlSlimParser 36,5; ParsedText 30,2; CssParser 21,5; Epub.cpp 21,5; BookMetadataCache 15,2); expat 53,3; TXT, XTC, UTF-8 25,0; ZIP и inflate 12,2 |
| TLS и криптография | wolfSSL (TLS 1.2/1.3, wolfCrypt), mbedTLS crypto из ESP-IDF, SecureNet, TrustedTime, DeviceSecret | **250,6** | **3,9** | 273 781 (исходники wolfSSL) | wolfSSL 176,8 (internal.c 30,1; asn.c 18,9; aes.c 18,6; ecc.c 12,6; tls.c 12,4; tls13.c 11,0); mbedTLS crypto 70,2; SecureNet, TrustedTime, DeviceSecret 3,6 |
| Bluetooth | контроллер BLE, хост NimBLE, BleKeyboardHost, BlePageTurner (пульт перелистывания), экран настроек BLE | **218,6** | **3,4** | 65 587 (NimBLE и обвязка; контроллер — готовый `.a`) | хост NimBLE 97,9 (ble_gap 8,3; ble_sm 8,0; ble_gattc 7,4); контроллер BLE 96,0 (btdm_app 87,9); BleKeyboardHost 10,6; BlePageTurner 7,5; экран настроек BLE 6,4 |
| Веб-сервер и передача файлов | страницы и скрипты веб-интерфейса (минифицированы и сжаты gzip), сервер CrossPoint, WebDAV, WebServer, WebSockets, DNSServer, QR-код, экраны передачи файлов | **208,0** | **3,2** | 10 474 (страницы — в `.h`) | страницы и скрипты 83,5 (jszip.min.js 27,7; FilesPage 24,9; epub-optimizer.js 11,1; SettingsPage 5,5); код сервера и WebDAV 77,9; библиотеки WebServer, WebSockets, DNSServer, QRCode 31,5; экраны 15,1 |
| Драйверы устройства | экран (три контроллера), кнопки и тач, батарея, подсветка, RTC, HAL, Wire/SPI, драйверы ESP-IDF RMT/I2C/UART/GPIO/LEDC/ADC | **124,4** | **1,9** | 15 806 | FreeInkDisplay 27,2 (SSD1677 8,8; UC8279 7,0; UC8179 6,2); RMT 16,5; I2C 13,2; HAL проекта 11,7; UART 10,0; GPIO 9,1; InputManager 7,9; LEDC 5,9; Wire 5,3; ADC 4,9; BatteryMonitor 4,7 |
| Онлайн-каталоги OPDS | OPDS 1/2, вход в каталог, списки серверов, экран каталога | **107,4** | **1,7** | 5 657 | OpdsBookBrowserActivity 26,6; OpdsImplicitAuth 11,9; Opds2Parser 9,0; CatalogScreens 6,6; OpdsParser 5,7; OpdsServerListActivity 5,3 |
| Картинки | JPEG, PNG, GIF, BMP: декодеры и вывод в кадр и в BMP | **83,2** | **1,3** | 7 298 | JPEGDEC 23,9; PNGdec 21,7 (crc32 8,7; inflate 8,1); вывод картинок книги в кадр 19,8; конвертеры в BMP 11,6; AnimatedGIF 5,7 |
| Плагины | каталог плагинов, события, HTTP для плагинов | **80,8** | **1,3** | 3 099 | PluginCatalogActivity 53,6; PluginEvents 12,2; PluginHttp 9,3; PluginLocations 2,9; PluginHubInstallActivity 2,8 |
| Синхронизация KOReader и цитат | клиент KOSync, сопоставление позиций, синхронизация цитат, экраны | **68,0** | **1,1** | 3 802 | KOReaderSyncClient 15,4; ClippingSync 12,0; KOReaderSyncActivity 11,0; ProgressMapper 9,5; ChapterXPathResolver 6,2; KOReaderSettingsActivity 6,0 |
| USB | TinyUSB, USB-диск (MSC), CDC, USB Serial/JTAG | **62,1** | **1,0** | 513 (TinyUSB — готовый `.a`) | TinyUSB 42,9 (из них объекты хост-режима и классов video/audio/MIDI/NCM/DFU 27,0); esp32-hal-tinyusb 4,7; HWCDC 3,3; libusb 3,2; USB Serial/JTAG 2,1; экран USB-диска 2,0 |
| SD-карта и файловая система | SdFat (FAT/exFAT), SDMMC, SDCardManager, FsHelpers | **51,7** | **0,8** | 8 493 | sdmmc 17,4; SdFat 15,5; esp_driver_sdmmc 9,8; SDCardManager 5,6; FsHelpers 3,4 |
| Обновление прошивки и загрузки из сети | OTA, прошивка с SD, загрузчик HTTP, загрузка шрифтов из сети | **40,9** | **0,6** | 2 588 | FontDownloadActivity 18,8; HttpDownloader 6,1; app_update 3,3; SdFirmwareUpdateActivity 3,2; FirmwareFlasher 2,9; OtaUpdateActivity 2,9; OtaUpdater 2,7 |
| Выравнивание между секциями | `*fill*` компоновщика | **25,7** | **0,4** | — | — |
| Защита контента (LCP) | ContentProtection, ключ книги, пароль LCP, устройство LCP | **23,7** | **0,4** | 1 900 | ProtectedBook 6,8; WolfsslCrypto 5,1; ContentProtection.cpp 2,7; LcpPassphraseStore 2,6; Zip 2,0; LcpDevice 1,8 |
| **Итого** | | **5376,6** | **84,0** | | |

Столбец «Строк .c/.cpp» — второстепенный: строки файлов `.c`/`.cpp`, объектные файлы которых дали в образ хотя
бы один байт; заголовки и готовые библиотеки ESP-IDF (`.a`) в счёт не входят. Для wolfSSL и `I18nStrings.cpp`
число строк велико, а в образ попадает часть кода: компоновщик выбрасывает неиспользуемые функции.

## Как измерено

Команды (PowerShell, рабочая папка `D:\work\ai_sandbox\KCCP`):

```powershell
git -C firmware fetch upstream develop
git -C firmware worktree add --detach ../.tmp/upstream_develop upstream/develop
git -C .tmp/upstream_develop submodule update --init --recursive
$env:PYTHONUTF8 = "1"; $env:TEMP = "D:\work\ai_sandbox\KCCP\.tmp"; $env:TMP = $env:TEMP
$env:PLATFORMIO_BUILD_FLAGS = "-Wl,-Map,D:/work/ai_sandbox/KCCP/.tmp/flash_budget/firmware.map"
.pio-venv\Scripts\pio.exe run -d .tmp\upstream_develop -e x4pro          # [SUCCESS], 1180 с
# линкер-карту записала сама платформа: .tmp\upstream_develop\.pio\build\x4pro\firmware.map
$tc = "C:\Users\krinik\.platformio\packages\toolchain-xtensa-esp-elf\bin"
& "$tc\xtensa-esp32s3-elf-readelf.exe" -S -W firmware.elf                # секции образа
& "$tc\xtensa-esp32s3-elf-size.exe" -A firmware.elf
C:\Users\krinik\.platformio\penv\Scripts\esptool.exe --chip esp32s3 image-info firmware.bin
.pio-venv\Scripts\python.exe -I -X utf8 .tmp\flash_budget\parse_map.py firmware.map firmware.nodebug.elf "$tc\xtensa-esp32s3-elf-readelf.exe" .tmp\flash_budget
.pio-venv\Scripts\python.exe -I -X utf8 .tmp\flash_budget\summarize.py .tmp\flash_budget "$tc\xtensa-esp32s3-elf-c++filt.exe"
.pio-venv\Scripts\python.exe -I -X utf8 .tmp\flash_budget\classify.py .tmp\flash_budget .tmp\upstream_develop C:\Users\krinik\.platformio\packages\framework-arduinoespressif32\libraries x
.pio-venv\Scripts\python.exe -I -X utf8 .tmp\flash_budget\subgroups.py .tmp\flash_budget
C:\Users\krinik\.platformio\penv\Scripts\python.exe -I -X utf8 -m esp_idf_size firmware.map            # сверка
C:\Users\krinik\.platformio\penv\Scripts\python.exe -I -X utf8 -m esp_idf_size --archives --format csv firmware.map
```

Метод:

- Из таблицы секций ELF взяты секции, которые попадают в образ (ALLOC + PROGBITS, размер > 0). Внутри каждой
  из них линкер-карта даёт входные секции с адресом, размером и объектным файлом или архивом; сумма входных
  секций и `*fill*` совпадает с размером секции ELF до байта во всех секциях, кроме `.eh_frame` (4 байта хвоста).
- Слитые строки: компоновщик сливает одинаковые строки (`*.str1.1`, `*.str1.4`, `*.str4.4`) в общий блок и в
  карте записывает весь блок на одну входную секцию. Таких блоков четыре: 232 896, 3276 и 20 байт в
  `.flash.rodata`, 6299 байт в `.dram0.data` — вместе 242 491 байт (4,4 % образа). Каждый блок разделён между
  объектами пропорционально их строкам до слияния: итог точный, доля строк каждого блока — оценка.
- Блок назначается по пути объектного файла или по имени архива; внутри `main.cpp` по имени символа данные
  `notosans_*`/`ubuntu_*` отнесены к шрифтам, остальное — к экранам. Нераспределённых входных секций — 0.
- Сверка с `esp_idf_size` 2.3.2: сумма по его таблице архивов — 5 479 348 байт, сумма входных секций этого
  отчёта без `*fill*` — 5 479 384 байт; разница 36 байт = `.rtc.force_slow` 32 + `.rtc.force_fast` 4, которых
  нет в его таблице архивов. По отдельным архивам числа расходятся на долю слитых строк: `esp_idf_size` относит
  весь блок 232 896 байт к первому объекту (`Wire.cpp.o`).

Сырые выходы лежат в `.tmp/flash_budget/`: `build.log`, `firmware.map`, `firmware.bin`, `firmware.nodebug.elf`,
`readelf_sections.txt`, `size_A.txt`, `image_info.txt`, `check.txt` (сверка по секциям), `pieces.tsv`,
`by_archive.tsv`, `by_object.tsv`, `top_symbols.tsv`, `blocks.tsv`, `blocks_detail.tsv`, `subgroups.tsv`,
`block_of_piece.tsv`, `loc_objects.tsv`, `esp_idf_size_summary.txt`, `esp_idf_size_archives.csv`.

## Наблюдения

1. Четыре набора данных занимают 2060,4 КБ — 32,2 % раздела и 38,3 % образа: растровые шрифты 1207,2 КБ,
   строки интерфейса с таблицами смещений 426,5 КБ, словари переносов 343,2 КБ, страницы веб-интерфейса
   83,5 КБ. Код (`.flash.text` и IRAM) — 2811,4 КБ.
2. Встроенные шрифты — самый крупный блок, 18,9 % раздела: 21 начертание и 23 709 глифов. Таблицы глифов
   (16 байт на глиф) занимают 370,5 КБ — больше половины от 700,7 КБ самих растров. Крупнейшее начертание —
   ubuntu_12_bold, 74,3 КБ: шрифты Ubuntu для интерфейса хранятся 1-битными без сжатия, NotoSans для текста
   книги — 2-битными со сжатием.
3. Немецкий словарь переносов занимает 201,4 КБ — больше, чем словари остальных десяти языков вместе
   (141,8 КБ).
4. Строки интерфейса: 35 языков по 651 ключу, UTF-8 без сжатия; русский набор — 20,0 КБ, английский — 10,9 КБ;
   один язык добавляет в образ строки плюс таблицу смещений 1302 байта.
5. Сетевые блоки — Wi-Fi и TCP/IP, TLS, веб-сервер, OPDS, плагины, KOReader, OTA — вместе 1305,3 КБ, 20,4 %
   раздела. В прошивке две криптобиблиотеки: wolfSSL 176,8 КБ для TLS и mbedTLS crypto 70,2 КБ; mbedTLS
   подтягивают `wpa_supplicant` (WPA), `ObfuscationUtils` (base64) и `WolfsslCrypto` из ContentProtection
   (по разделу «Archive member included…» линкер-карты).
