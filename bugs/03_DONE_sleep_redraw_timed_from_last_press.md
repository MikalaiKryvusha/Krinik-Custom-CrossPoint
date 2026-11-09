# Bug 03 — the sleep-image redraw is timed from the last non-waking press (debug line) or lost (PR #4376)

**Status:** ✅ DONE 2026-11-09 23:22 +03:00 — verified on the reader (debug7) · **Severity:** S2 (a feature
silently does the wrong thing) · **Version/build:** debug line `wip/krinik-debug6` `e7a29dd4` (KCCP 1.1.1-debug6, on
the owner's reader); PR #4376 `pr/screen-redraw-delay` `2dbfff7d` · **When/context:** 2026-11-09 22:39 +03:00, the
repeat of homework 01 with «Короткое нажатие PWR» = «Игнорировать», on the owner's X4 Pro.
**Owner's report (verbatim):** `[OWNER] 2026-11-09 22:39 +03:00 · chat: «делал короткие нажатия ДО перерисовки. в
минутном интервале - читалка не проснулась, но и перерисовку НЕ ВЫПОЛНИЛА, хотя в настройках стоит перерисока через
минуту. Такое ощущение, что читалка сделала перерисвоку от последнего короткого нажатия PWR, а не от ухода в сон - а
должна была делать именно от ухода в сон. и не важно чем он был вызван»`.

## Goal vector and acceptance

Achieve: the redraw comes N minutes after the reader went to sleep, whatever caused the sleep; presses that do not wake
the reader neither shift nor cancel it.
- Check (owner's reader): «Обновлять заставку» = «через 1 мин», «Короткое нажатие PWR» = «Игнорировать»; sleep, click
  power a few times during the minute → the reader stays asleep AND the image is redrawn about 1 min after the sleep.

## Repro

As in the check above, on debug6: the redraw did not come at 1 min.

## Forensics (code, 2026-11-09 22:40)

- debug6 `src/main.cpp` (failed power-wake branch in `setup()`): «A brushed button before the delay ran out: keep the
  settled sleep redraw (the full delay again)» → `esp_sleep_enable_timer_wakeup(sleepSettleUs())` — the FULL delay from
  each press. Written so on purpose in `f01b56db` (2026-11-05).
- PR #4376 `src/main.cpp:800-805`: the same branch calls `powerManager.startDeepSleep(gpio)` with no timer at all —
  the timer wake source does not survive the wake, so the redraw is lost.

## Fix (2026-11-09 22:45–22:50, not built)

The due moment is kept in RTC memory on the RTC counter (`esp_rtc_get_time_us()`, runs through deep sleep); the failed
power-wake branch re-arms only the time left (1 s if overdue). debug7 `f52de583`, PR #4376 `266340d8` — both local.
Next: the independent judge's verdict (owner's rule, AGENT_GUIDE → "Order after a code change"), then build, simulator
smoke, image, the owner's check.

## Independent judge, round 1 (2026-11-09 22:53 +03:00)

- PR `266340d8` **REFUTED**, verified by me in the code: `src/main.cpp:764` cleared `sleepRedrawPath` on every boot
  BEFORE `switch (wakeupReason)`, so the new re-arm never ran — the redraw was still lost. Fixed in `94e1c3a2`
  (amend): the clear moved after the switch; also a redraw timer wake with an SD failure now sleeps again (judge,
  should-fix, outside the original diff).
- debug7 `f52de583` **VERIFIED WITH CAVEATS**; taken in `2b150595` (amend): the due moment stamped just before
  `startDeepSleep` (stamped at arming it ran up to the linger length early after a press), `ESP_OK` checked.
- Round 2 on `94e1c3a2` / `2b150595` — running.

## ✅ STATUS: DONE (2026-11-09 23:22 +03:00)

Verified on the owner's X4 Pro with debug7 `2b150595` — homework 02, `[OWNER] 2026-11-09 23:22 +03:00 · chat: «все кейсы PASS, всё ок»`.
