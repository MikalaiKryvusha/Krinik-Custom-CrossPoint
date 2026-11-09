# Idea 01 — Home «Сон»: show the selection on tap before the sleep starts

**Status:** ✅ approved — the owner's own request · **Scope:** KCCP debug line only (the Home «Сон» item is KCCP) ·
**Created:** 2026-11-09 23:22 +03:00
**Owner's words (verbatim):** `[OWNER] 2026-11-09 23:22 +03:00 · chat: «по нашей кнопке Сон на домашней есть импрувмент
- успевать её покрасить выделением при тапе по ней, и только потом запускать алгоритмы сна. Сейчас она при тапе не
выделяется»`.

## Acceptance

Tap «Сон» on Home → the row is drawn selected (highlighted) first, then the sleep image and the rest of the sleep.

## Cause (code, `wip/krinik-debug7` `src/activities/home/HomeActivity.cpp`)

On touch Down the row only asks for a render (`selectorIndex = touchedIndex; requestUpdate();`, line ≈ 475); the
render runs on the render task later. On touch Up `activateSelection()` → `case HomeMenuItem::SLEEP:
activityManager.requestSleep();` (line ≈ 348) starts the sleep at once, so a quick tap reaches the sleep before the
highlight is painted.

## Plan

In `case HomeMenuItem::SLEEP:` call `requestUpdateAndWait()` (exists in `Activity.h:44`: renders and waits for the
render task) before `activityManager.requestSleep()`. Then the owner's order: independent judge → build → simulator
smoke (tap «Сон»: a shot of the highlighted row before the sleep screen) → debug8 image → owner's check.
