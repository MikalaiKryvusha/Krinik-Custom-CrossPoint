# Bug 13 — the shade's «Сон»: the tapped button is not shown before the reader falls asleep

**Status:** 🔧 fix pending verification · **Severity:** S2
**Version/build:** KCCP 1.1.3-debug4 on the owner's reader (firmware `3e223b4d`); the button since epic 01 Ф3
`261e5c63` · **When/context:** the owner in chat 2026-11-17 20:53 +03:00, testing debug4 · **Fixing:** this session

## The owner's words (chat, verbatim, committed first in `2850162`)

> кнопка Сон в шторке не успевает выделиться по тапу - такой же баг чинили для этой же кнопки на главном экране

## Goal vector (Achieve) and acceptance

A tap on the shade's «Сон» shows the button pressed before the sleep starts — as Home's «Сон» does since debug8.
- Check: the simulator log of a tap on «Сон» shows a rendered shade frame between the tap and `Sleep requested`, and a
  shot taken in that window shows the button filled.

## Root cause

`FrontlightPanelActivity::runTile` → `Tile::Sleep` called `activityManager.requestSleep()` at once; the shade's buttons
have no pressed state (only the toggles are drawn filled), so nothing showed the tap. Home had the same defect, fixed in
debug8 `c072214b`: `requestUpdateAndWait()` before `requestSleep()` («успевать её покрасить выделением при тапе по ней,
и только потом запускать алгоритмы сна», the owner 2026-11-09).

## Fix

Firmware (uncommitted at writing): `sleepTileTapped` (atomic, set by the input loop, read by render) draws «Сон»
filled; `runTile` sets it, `requestUpdateAndWait()`, then `requestSleep()`. `TWINS:` searched `requestSleep()` in
`src/` — Home (fixed in debug8) and the shade (this); no other caller paints a button first.

## Verification

- [ ] Independent judge over the diff.
- [ ] Simulator: a tap on «Сон» in the shade — the log order and a shot of the filled button.
- [ ] The owner on the reader.

## Decisions made without the owner

- `[AI]` «Pressed» = the same fill as an enabled toggle (the Home row uses its own selection look; the shade has none).

## Links

Home's fix: debug8 `c072214b` · epic 01 Ф3 · `bugs/12_shade_row_gaps.md` (the same row)
