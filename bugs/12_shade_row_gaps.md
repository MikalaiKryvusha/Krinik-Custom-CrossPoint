# Bug 12 — the shade's buttons: huge ends, tight gaps — the row was spaced inside the sliders' inset

**Status:** 🔧 fix pending verification · **Severity:** S2
**Version/build:** KCCP 1.1.3-debug4 on the owner's reader (firmware `3e223b4d`); the row since epic 01 Ф3 `261e5c63`
· **When/context:** the owner in chat 2026-11-17 20:51 +03:00, testing debug4 · **Fixing:** this session

## The owner's words (chat, verbatim, committed first in `fcdb35a`)

> отступы в шторке неверно между кнопками расчитываются. Слева и справа огромные остаются, а кнопки десно друг к
> дружке.
>
> Иди ищи в интернете, как дизайнеры расстояния считают для таких кейсов

## Goal vector (Avoid) and acceptance

The shade's button row never shows ends wider than the gaps between its buttons.
- Situation. The shade is open over Home (portrait), every button the board has is on (the simulator: 6).
- Action. The agent shoots the shade.
- Result. The two end gaps (from the sheet's visible edge) and the gaps between the buttons differ by ≤ 2 px at half
  scale.
- Check. `.pio-venv/Scripts/python.exe -I -X utf8 tools/shade_gaps.py <shot> port` exits 0 (debug4: `gaps [19, 10, 10,
  10, 10, 10, 18], spread 9`, exit 1).

## Root cause

`shadetiles::tileLeft` is space-evenly, but `FrontlightPanelActivity::buildPanelScreen` passed it the row INSIDE
`insetContent(kPanelSideMargin = 16)` — the sliders' inset. The eye measures from the sheet's edge: 16 px + gap at each
end, gap between. Portrait, 56 px buttons: 5 buttons → 44 vs 28; 7 buttons → 23 vs 7 (the owner's «тесно»). The
guard `tools/shade_gaps.py` measured from the sliders' edges — the same inset — so epic 01 Ф3 «equal gaps» passed: a
guard proved against the wrong frame.

## Research

`researches/2026-11-17_shade_row_spacing.md` (the owner's order): space-evenly for a full-width icon row, the ends
counted from the container's VISIBLE edge (padding = gap), ≥ 8 px between touch targets.

## Fix

Firmware (uncommitted at writing): the row given to `tileLeft`/`tileSlot` is widened by `kPanelSideMargin` on both
sides — the sheet's visible edges. 7 buttons portrait: 11 px everywhere. Guard: `shade_gaps.py` measures from the
shot's edges by default (`--frame content` = the old frame); proven red on the debug4 shot (`qa_runs/bug12_before`).

## Verification

- [x] Independent judge over the diff — three rounds, OK WITH NOTES (the stale `[TESTED]` tag replaced; my claim that the
      sheet ignores the safe area refuted — the simulator's X4 Pro profile has 3 px sides, the reader 7 px). Firmware
      `3db21be8`.
- [x] Simulator (`testcases/reports/2026-11-17_bug12_bug13_debug5.md`): portrait `[9, 9, 9, 10, 10, 9, 9]` spread 1,
      landscape `[33, 32, 32, 33, 32, 31, 31]` spread 2 (debug4: `[15, 7, 7, 7, 7, 7, 15]`, spread 8). The guard also
      measures through the buttons' middles now (a row near the rounded corners inflated the inner gaps).
- [ ] The owner's look on the reader, image 1.1.3-debug5 (the taste is his; 7 buttons on the reader: ≈ 9 px everywhere).

## Decisions made without the owner

- `[AI]` Space-evenly from the sheet's visible edges (option A of the research's FORK line) over space-between inside
  the sliders' inset (B) and a fixed centred gap (C). The buttons no longer line up with the sliders' «−» / lamp boxes.

## Links

`researches/2026-11-17_shade_row_spacing.md` · epic 01 Ф3 (`plans/01_EPIC_shade_tiles.md`) · `tools/shade_gaps.py`
