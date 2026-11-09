# Idea 01 — Home «Сон»: show the selection on tap before the sleep starts

**Status:** 🔧 built as debug8 `c072214b` (judged, simulator-checked), on the owner's check — homework 03 · the owner's own request · **Scope:** KCCP debug line only (the Home «Сон» item is KCCP) ·
**Created:** 2026-11-09 23:22 +03:00
**Owner's words (verbatim):** `[OWNER] 2026-11-09 23:22 +03:00 · chat: «по нашей кнопке Сон на домашней есть импрувмент
- успевать её покрасить выделением при тапе по ней, и только потом запускать алгоритмы сна. Сейчас она при тапе не
выделяется»`.

## Acceptance

Tap «Сон» on Home → the row is drawn selected (highlighted) first, then the sleep image and the rest of the sleep.

## Cause (code, `wip/krinik-debug7`; corrected 2026-11-09 23:35 after the independent judge)

My first reading ("the Down render is late") was wrong. `MappedInputManager::wasScreenTouchDown()` returns nothing
until the finger has been down `TOUCH_DOWN_SELECT_DELAY_MS = 90` ms (`src/MappedInputManager.cpp:181, 223`), so a quick
tap never takes the Down branch: on release `selectorIndex` is set and `activateSelection()` → `requestSleep()` runs with
NO render queued. The cover-grid home never renders on touch down at all. Taps ≥ 90 ms most likely painted already.

## Plan

In `case HomeMenuItem::SLEEP:` call `requestUpdateAndWait()` (exists in `Activity.h:44`: renders and waits for the
render task) before `activityManager.requestSleep()`. Then the owner's order: independent judge → build → simulator
smoke (tap «Сон»: a shot of the highlighted row before the sleep screen) → debug8 image → owner's check.
