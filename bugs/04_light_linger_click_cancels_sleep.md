# Bug 04 — a short click in the sleep light linger cancels the sleep with «Короткое нажатие PWR» = «Игнорировать»

**Status:** 🔧 fix written, under independent review — not built, not on the reader · **Severity:** S2 · **Version/build:**
debug line `wip/krinik-debug6` `e7a29dd4` (KCCP only; the linger is not in any upstream PR) · **When/context:**
2026-11-09 22:39 +03:00, the repeat of homework 01, on the owner's X4 Pro.
**Owner's report (verbatim):** `[OWNER] 2026-11-09 22:39 +03:00 · chat: «короткое нажатие на задержке подсветки перед
сном - разбудило, баг»`; earlier, 22:35: «не должно будить при Игнорировать».
**Owner's decision:** `[OWNER] 2026-11-09 22:43 +03:00 · chat: A1 «как с пробуждением. При «Сон» отменяет любой щелчок,
при остальных значениях — только удержание, как когда будишь читалку. Короткий щелчок ничего не делает.»`

## Goal vector and acceptance

Achieve: in the light-linger window the power button follows the wake rule.
- Check (owner's reader): «Подсветка на засыпании» on, «Короткое нажатие PWR» = «Игнорировать»: a click in the window →
  the reader goes to sleep; a hold → the sleep is cancelled. With «Сон»: a click cancels, as before.

## Forensics

debug6 `src/main.cpp` `enterDeepSleep()`: any new press of 3 samples × 20 ms after a release set `cancelSleep`, with no
look at `shortPwrBtn` — written so in the 1.1.0 linger work (2026-11-04/05); the wake rule was not carried over.

## Fix (2026-11-09 22:47, not built)

debug7 `f52de583`: with «Сон» 3 samples as before; otherwise `getPowerButtonDuration()` (400 ms, the firmware's own
short/long boundary for this button) rounded up to 20 ms samples. The 400 ms value is the agent's pick, said to the
owner; the wake threshold itself is not measured. Next as bug 03.

## Independent judge, round 1 (2026-11-09 22:53 +03:00)

`f52de583` VERIFIED WITH CAVEATS for this bug. Taken in `2b150595`: 20 samples measured ≈ 360–400 ms (N samples span
N − 1 intervals) → now `400 / 20 + 1` = 21 samples; the two comments that promised "any press cancels" corrected.
Open (owner's call, said in chat): this hold rule (400 ms) differs from the timer-redraw rule (`holdWakes`: hold ≥ the
time from reset to the wake sample).
