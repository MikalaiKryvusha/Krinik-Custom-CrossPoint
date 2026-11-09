# Krinik Custom CrossPoint — Project History (the chronicle)

> The APPEND-ONLY chronicle of how this project lived and grew: closed sessions, shipped phases,
> releases, big decisions in the order they happened. This is where `STATUS.md` sheds its past —
> STATUS stays a short live summary of NOW; everything finished moves HERE (the "bonsai trim" step
> of `/end-chat-soft`).
>
> **Not required reading.** This file is NOT part of `/resume`'s canon set and not in the
> before-every-task minimum — open it only when you actually need the archaeology: how a decision
> came to be, what an old phase contained, when something shipped.
>
> **Chronicle rules (ADR discipline):**
> - **Append-only, newest on top.** A recorded entry is never edited to say something else —
>   history that can be rewritten is not history. Corrections come as NEW entries that reference
>   and supersede the old one.
> - An entry moves here VERBATIM from `STATUS.md` when its work closes — move, don't rewrite;
>   the entry already carries its dates, counters and file pointers.
> - Entries mention versions and dates freely — a chronicle legitimately speaks of old versions,
>   and the update machinery's stale-claims scan knows to leave this file alone.
> - When the file grows unwieldy, split by era: keep the newest era here, move older ones to
>   `PROJECT_HISTORY_<era>.md` files, and leave a one-line index at the top of this file
>   (the pattern large changelogs use).
>
> Living document — never DONE-tagged.

---

## Entries (newest first)

### 2026-11-09 — STATUS trim: closed hardware research (charging, measurements) ✅
- Charging cannot be stopped in software at 4.1 V or N %: no charger on I²C, no CE/EN line to the ESP32. Only a board modification
  could do it. **Not doing it** (owner, 2026-11-08: «это не будет делаться»). Available now: a "unplug the charger" reminder at N % in firmware. Analysis:
  `researches/2026-11-06_stock_batinfo_charger_analysis.md` (its raw inputs — vendor firmware, disassembly, third-party photos —
  stayed on the laptop, see below).
- Measurements, do not repeat without a goal: charge 50→100 % in 1:07:06, gauge max 4.381 V
  (`qa_runs/debug2-charge-2026-11-06-180555/`); awake hour: light off ≈ 4–5 pp, light 100 % ≈ 8–9 pp
  (`qa_runs/debug2-light-hours-2026-11-06-201434/`).

### 2026-11-09 — KAIF deployed on the owner's PC (Task 0 step 3) ✅
- **Task 0 step 3 done 2026-11-09:** KAIF 2.9 (+2.10 WIP) deployed from KAIF commit d2f21274d396, commits 8a78058,
  2924afa; field report KAIF issue #195. Steps 1 (firmware clone — done 2026-11-09), 2, 4–6 open.

Earlier history (laptop era, Russian): `legacy/PROJECT_HISTORY.ru.md`.
