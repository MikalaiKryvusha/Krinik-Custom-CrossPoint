# Bug 02 — PR #4376 test image: a power press during the timer redraw looked like a crash — NOT A DEFECT

**Status:** ✅ CLOSED 2026-11-09 19:10 +03:00 — not a defect: the press WOKE the reader (a CrossPoint wake from deep
sleep is a full boot: CrossPoint boot screen → Home); the image kept running, no `/crash_report.txt`. Correction of
the title and of the agent's chat line «прошивка упала» written before the facts. · **Severity:** was S1 (suspected)
**Version/build:** `pr/screen-redraw-delay` `2dbfff7d` (contains `4818dba0`), image
`firmware-builds/crosspoint-2.0.0-pr4376-2dbfff7d-x4pro.bin` (SHA256 `ad34ece5…c975`) · **When/context:**
2026-11-09 19:05 +03:00, homework 01 step 4, on the owner's X4 Pro.
**Owner's report (verbatim):** `[OWNER] 2026-11-09 19:05 +03:00 · chat: «прошивка словно упала, и читалка запустилась со
стоковой.» · «Я нажал кнопку во время перерисовывания»`.

## Goal vector and acceptance

Avoid: a power press during the timer redraw never crashes the reader. Achieve: the hold wakes the reader (Q3 = B).
- Check: on the owner's reader, homework 01 steps 4 and 5 pass; `/crash_report.txt` is not rewritten.

## Repro

Homework 01: image installed, «Обновлять заставку» = «через 1 мин», «Экран сна» = «Свой», «Короткое нажатие PWR» ≠
«Сон»; sleep; during the redraw press and hold power, release before the redraw ends → the firmware "fell" and the
reader came up looking like stock CrossPoint (the test image has no KCCP, so a reboot into it looks stock).

## Forensics

- Needed: `/crash_report.txt` from the card (written by `HalSystem::checkPanic()` on the next boot of the same app),
  and what the screen showed after the fall (crash screen or Home).
- Not observable on the simulator: the timer-redraw path is `FREEINK_DEVICE_X4PRO && !SIMULATOR`.

## Hypotheses (ranked; no patch before the crash report)

1. The new ISR `onSettledRedrawEdge()` (IRAM) calls `millis()` and `gpio_get_level()`; if either is not in IRAM, an
   interrupt while the flash cache is off panics («Cache disabled but cached memory region accessed»). The old ISR
   only stored a bool.
2. The wake continuation after the redraw (`holdWakes` → the normal boot path with the display already started
   `seamless`) is a path the old code reached only with Short Power = Sleep; something after it may assume a fresh
   boot.
3. Unrelated to the press: a crash of the upstream `develop` base on this reader.

## Fix plan

Read the crash report (backtrace address → `xtensa-esp32s3-elf-addr2line` on `firmware.elf` of `2dbfff7d`), then fix
the class it names; device re-check by the owner after a simulator smoke of the same commit.

## Resolution (2026-11-09 19:06–19:10 +03:00)

- Card read over USB: no `/crash_report.txt` (a panic writes it on the next boot of the same app, `HalSystem.cpp:107`).
- Owner, in answers: first «Заводская Xteink», then corrected `[OWNER] «ой, не на заводской» · «а на стоковом
  кроспоинте»`; then on the decisive check `[OWNER] «Строка есть, была загрузка»` — «Обновлять заставку» is present
  (only the #4376 test image has it) and the screen showed the CrossPoint boot, then Home.
- Verdict: homework 01 step 4 PASS (the hold during the redraw woke the reader). Step 5 (no press → stays asleep)
  still to run.
- Lesson for the next device check: tell the owner in advance what a successful wake looks like on this build (boot
  screen → Home), so a correct result is not read as a crash.

## Decisions made without the owner

- none.
