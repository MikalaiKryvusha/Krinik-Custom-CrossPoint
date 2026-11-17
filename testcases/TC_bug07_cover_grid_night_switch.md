# Test cases — bug 07: Cover Grid covers after a night ↔ day switch on Home

**Created:** 2026-11-17 · **Under test:** `HomeCoverCache::prepare()` invalidating on a polarity change (port of upstream
`b9c23473`, #4494) · **Version/build:** `wip/kccp-1.1.3-debug2`, simulator `simulator_x4_pro_win`
**Test basis:** upstream #4329 comments of itsthisjustin, 2026-11-16 19:10 / 19:12 UTC («inverted covers when switching
from dark to light mode at the home screen» · «your fix was specific to the single covers not the grid»); the owner
2026-11-17 10:04 +03:00: «Перенести правку Justin в debug2. Сначала на симуляторе получить негатив на старой сборке,
потом убедиться, что на новой его нет» (his reply quoting the agent's offer, then «Всё делаем»); `bugs/07_cover_grid_negative_after_night_switch.md`.

## 1. Goal vector

Avoid: a recent-book cover on Home shown as a negative after night mode is switched while Home stays alive under the
shade. Working = after the shade closes, every cover reads as paper (light page, dark print) in the new mode, as a
fresh boot in that mode shows it.

## 2. Requirements under test

| # | Requirement (EARS sentence) | Fit criterion (Scale · Meter · Target) |
|---|---|---|
| R1 | WHEN night mode changes while Home with the Cover Grid theme is under the shade and the shade closes, the firmware shall paint every cover in the polarity of the new mode. | cover page tone vs the boot shot of the same mode · `after.webp` read by eye against `before`/probe shots · light page, dark print in both modes |
| R2 | WHEN the same happens on a single-cover theme (Lyra), the firmware shall keep painting the cover positive (the #4329 path). | the same meter on the Lyra card · positive |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| direction of the switch | night → day · day → night | — |
| theme | Cover Grid (theme 4) · Lyra (theme 1) | Classic, Lyra Extended, RoundedRaff — the #4329 path they share with Lyra was tested at #4329 time (low) |
| entry to the switch | the shade's night button over Home | the Settings night item (not observed; whether Home stays alive under Settings was not traced — low: `prepare()` runs on every grid draw either way); the slide switch (no switch on the simulator; it changes the same `screenInverted`, so the same `prepare()` runs — not observed) |
| build | the plain simulator build | the mama build (same Home code; low) · the device (the owner's reader, with the debug2 image) |
| covers | two own EPUBs with photo-like JPEG covers (`РУКОВОДСТВО.epub`, `КАЛИБРОВКА.epub`) | a book without a cover (placeholder art reads the same in both polarities — nothing to see) |

## 4. Cases

Card: `.tmp/sd_grid_night` (theme 4, night on, the two guides as recents) and its day / Lyra copies. Script per case:
`0:WAIT:Entering activity: Home;8000:SHOT:before;9000:SWIPE:0.5,0.0,0.5,0.5,300;9000:WAIT:Entering activity: FrontlightPanel;2000:TAP:0.1875,0.3525;4500:SHOT:shade;5500:BACK;9000:SHOT:after;10000:QUIT`
(the Lyra case opens the book once first, so its thumb exists). Machinery: `tools/sim_run.sh`; read: the WebP shots and
`settings.json` → `screenInverted` after the run.

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| C1 smoke | grid, night on → shade → night off → Back → covers positive in day | state transition | old: fail (negative) `qa_runs/grid_night_red`; new: see the run report |
| C2 | grid, day → shade → night on → Back → covers positive in night | state transition (reverse) | old: fail (negative) `qa_runs/grid_day_red`; new: see the run report |
| C3 | Lyra, night on → open the book, Back → shade → night off → Back → cover positive in day | regression (#4329) | old: pass `qa_runs/lyra_night_old`; new: see the run report |

## 5. Control cases

| # | Control → expected: the behaviour is absent | Status + evidence |
|---|---|---|
| K1 | C1 and C2 on the binary WITHOUT the fix (`2fa20f3f` code) → negative covers | pass — the negative seen in `grid_night_red/after.webp` and `grid_day_red/after.webp` |

## 6. Verdict

In the run report `testcases/reports/2026-11-17_bug07_grid_night.md`.
