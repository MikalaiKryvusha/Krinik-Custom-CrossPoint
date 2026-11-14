# Правила дома — Krinik Custom CrossPoint

> Местные правила этого проекта: постоянные правила Николая и системы, стенды и инструменты, с которыми агент работает в KCCP. Канон KAIF говорит, как
> агент работает (`AGENT_GUIDE.md`); этот файл говорит, где и с чем. Агент читает файл при входе в чат (`/resume`).

**Создан:** 2026-11-13 · **Владелец:** Николай Кривуша · **Перенесено сюда из канона:** пока ничего

## 1. Постоянные правила Николая

### П1. Временные файлы агента лежат в папке проекта

1. Клади всё временное в `.tmp/` в корне проекта: копии, патчи, выводы скриптов, рабочие копии веток (`git worktree`),
   скачанное. Папка `.tmp/` стоит в `.gitignore`.
2. Удаляй временный файл из `.tmp/` сразу, как только он больше не нужен: в том ходе работы, где он создан.
3. Ничего не пиши в `D:\Temp` и в другие папки вне проекта. Папку сессии, которую Claude Code называет в системных
   настройках (`D:\Temp\claude\…`), для своих файлов не бери.
- **Исключение:** служебные файлы самого Claude Code (выводы фоновых команд, журналы субагентов) пишет Claude Code, их
  папку задаёт его настройка. Перенос этих файлов в папку проекта ждёт выяснения, какая настройка за это отвечает.

[OWNER] 2026-11-13 18:55–18:56 +03:00 · чат: «а что это за свалка? D:\Temp\ я не разрешал агентам там работать» · «у
каждого проекта есть директория - там и работайте»

## 2. Стенды, окружения и устройства

Компилятор, Python (`tempfile`) и ctest кладут свои временные файлы в папку из переменных `TEMP` и `TMP`. Каждая команда
ниже ставит обе переменные на `.tmp/` проекта (правило П1).

| Стенд | Для чего | Как агент до него доходит (Git Bash) | Известные ловушки |
|---|---|---|---|
| Хост-тесты | модули прошивки на ПК, перед каждым коммитом кода прошивки | `sh tools/host_tests.sh`: сборка, `ctest -j1`, сверка упавших тестов со списком `tools/host_tests_known_failures.txt`; выход 1 при новом падении | 8 падений под Windows известны (ресёрч 01); `ParserStopTest` нестабилен под `-j`; EXP-0018 |
| Тест подсветки отдельно | шлюз «Точной температуры», плавные переходы | `TEMP` и `TMP` на `.tmp/`, `PATH` с UCRT64; `.pio-venv/Scripts/python.exe -I -X utf8 test/test_frontlight_dither.py` из `firmware/` | — |
| Симулятор | экраны прошивки, ввод скриптом, снимки WebP | сборка из PowerShell: `$env:PYTHONUTF8 = "1"; $env:TEMP = "D:\work\ai_sandbox\KCCP\.tmp"; $env:TMP = $env:TEMP; .pio-venv\Scripts\pio.exe run -d firmware -e simulator_x4_pro_win`; прогон: `SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh <имя> '<скрипт>' '<снимки>'` | EXP-0004, EXP-0009, EXP-0015; сборка под читалку стирает бинарник симулятора |
| Симулятор маминой сборки | домашний экран с кнопкой «Для любимой Мамы» (эпик 05) | окружение `simulator_x4_pro_mama_win` в `firmware/platformio.local.ini` (`-DKRINIK_MAMA=1`), сборка как у симулятора; прогон: `SIM_ENV=simulator_x4_pro_mama_win sh tools/sim_run.sh <имя> '<скрипт>' '<снимки>'` | строка, нарисованная за нижним краем экрана, даёт в логе сотни `[ERR] [GFX] !! Outside range` — это счётчик бага, не шум симулятора; кнопки читалки в скрипте — `UP`, `DOWN`, `LEFT`, `RIGHT`, `CONFIRM`, `BACK`, а `NEXT` и `PREV` — кнопки обложки-чехла, домашний экран их не видит; свайп по списку — быстрый (`SWIPE:…,60`): палец, задержанный дольше 90 мс, сначала выделяет строку |
| Замер шторки | равные отступы ряда кнопок на снимке симулятора | `.pio-venv/Scripts/python.exe -I -X utf8 tools/shade_gaps.py <снимок.webp>`: края, кнопки, промежутки; выход 1, если разброс больше 2 точек половинного масштаба | снимки WebP в половинном масштабе: край кнопки точен до ±1 точки |
| Сборка под читалку | образ для SD-карты | PowerShell, `PYTHONUTF8`, `TEMP` и `TMP` как у симулятора; `.pio-venv\Scripts\pio.exe run -d firmware -e x4pro-krinik-debug` | EXP-0004, EXP-0007 |

## 3. Досье окружения — факты машины

Правило — `AGENT_GUIDE.md` → «Environment dossier». Факт старше четырёх недель — гипотеза: перед опорой на него
повтори пробу из третьего столбца.

> **Досье окружения.** Снято: 2026-11-14 16:25 +03:00 · Обновление: `/refresh-context`, шаг досье.

| Факт | Значение | Проба |
|---|---|---|
| ОС | Windows 11 Pro 10.0.26200 | PowerShell: `(Get-CimInstance Win32_OperatingSystem).Version` |
| Процессор и память | AMD Ryzen 7 5700G, 16 логических ядер, 31,8 ГБ | PowerShell: `[Environment]::ProcessorCount`, `(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory` |
| Оболочки | Git Bash (MINGW64, MSYS 3.4.9), Windows PowerShell 5.1 | `uname -srmo`; `$PSVersionTable.PSVersion` |
| Кодировки | консоль PowerShell UTF-8; ANSI по умолчанию windows-1251 (ACP 1251), OEM 866 — `Set-Content` пишет в 1251 | PowerShell: `[Console]::OutputEncoding`, `[System.Text.Encoding]::Default` |
| Локаль | PowerShell ru-RU, интерфейс en-US; Git Bash `LANG` не задан | `Get-Culture`; `echo $LANG` |
| Python | в Git Bash `python3` — заглушка Microsoft Store (`WindowsApps`); настоящий — `.pio-venv/Scripts/python.exe` 3.11.0 | `command -v python3`; `.pio-venv/Scripts/python.exe -V` |
| Сборка | PlatformIO 6.2.0 (`.pio-venv`); cmake 4.4.5 и gcc 16.2.0 только с `F:\ai_sandbox\msys64\ucrt64\bin` в PATH; Node 24.15.0; gh 2.95.0 | `--version` у каждого |
| `tar` / `curl` / `find` | Git Bash: GNU tar 1.35, curl 8.4.0 (mingw64), GNU find; PowerShell: `tar` = `C:\Windows\system32\tar.exe` (bsdtar), `curl` = псевдоним `Invoke-WebRequest`, `find` = `find.exe` Windows | `type -t tar curl find`; `Get-Command tar,curl,find` |
| Окончания строк в git | этот репозиторий `core.autocrlf=true`; клон `firmware/` `core.autocrlf=false` (EXP-0007); помощник учётных данных `manager` | `git config --get core.autocrlf`; `git -C firmware config --get core.autocrlf` |
| Менеджер пакетов | winget (из обеих оболочек); MSYS2 pacman в `F:\ai_sandbox\msys64` | `command -v winget` |
| Ловушки, оплаченные инцидентами | EXP-0004 (cp1251 в Python из Git Bash), EXP-0007 и EXP-0019 (CRLF), EXP-0008 (`grep` падает на длинном потоке), EXP-0010 (`cd` в параллельных вызовах), EXP-0017 (временные файлы вне проекта) | `EXPERIENCE.md` |
