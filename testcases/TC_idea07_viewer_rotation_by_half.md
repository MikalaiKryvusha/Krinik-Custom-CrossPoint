# Test cases — idea 07: in the image viewer a long tap turns the picture toward its half of the screen

**Created:** 2026-11-13 · **Under test:** `wip/krinik-debug10` (`firmware/`) — `BmpViewerActivity` long tap ·
**Version/build:** simulator `simulator_x4_pro_win` first, then `1.1.1-debug10` on the owner's X4 Pro (with idea 05)
**Test basis:** the owner's words, verbatim in `ideas/07_viewer_long_tap_rotation_by_half.md` (2026-11-13 13:51 +03:00):
«лонгтам в правой половине экрана вращал картинку по часовой» (R1) · «а лонгтам в левой половине экрана - против
часовой» (R2); R3 follows from R1 + R2 (one turn each way returns the view); R4 is the unchanged viewer input (control).

## 1. Goal vector

Achieve: the owner turns a picture in the viewer toward the side he long-taps, and one long tap the other way undoes it.

## 2. Requirements under test

| # | Requirement (EARS sentence) | Fit criterion |
|---|---|---|
| R1 | WHEN the reader long-taps the right half of the screen in the viewer, the viewer shall turn the picture 90° clockwise. | the shot after the long tap: the orientation triangle moved from the top-left corner to the top-right; log `long tap` names the right half |
| R2 | WHEN the reader long-taps the left half of the screen in the viewer, the viewer shall turn the picture 90° counterclockwise. | the shot: the triangle moved from the top-left corner to the bottom-left; log names the left half |
| R3 | WHEN a right long tap is followed by a left long tap, the viewer shall show the picture as before the first one. | the third shot equals the first by eye: the triangle back in the top-left |
| R4 | The viewer's short taps and swipes shall act as in debug9: swipe Back returns to the book page. | the shot after the swipe shows the book page the picture was opened from |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| long-tap position | right half (x = 0.75) · left half (x = 0.25) | the middle column (x = 0.5) — the boundary is the middle by the owner's words; one side by construction |
| entry into the viewer | a tapped book picture (idea 02) | an image file from the file browser — the same activity and the same `loop()`; not run |
| orientation | landscape CCW (the owner's `orientation: 3`) | portrait, inverted, landscape CW — the long-tap point comes in the reading orientation (`holdOrientation()`), the halves follow it; not run |
| turn state | first turn from 0 · the way back | four turns in a row (wrap-around of `viewTurns`) — modulo arithmetic, read in the judge pass |
| device | simulator | the direction on the panel — the owner's reader is the last stand |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| D0 | debug9 (`35dc070c`): the book's page 1 → `TAP` picture 1 → viewer shot → long tap right → shot → long tap left → shot: both long taps turn the SAME way (control: the feature is what changes it; also tells which way `+1` turns on screen) | control | pass — [TESTED: 2026-11-13 · debug9: right and left long taps both turned clockwise (triangle top-left → top-right → bottom-right) · testcases/reports/2026-11-13_idea07_simulator.md] |
| C1 | debug10: page 1 → `TAP` picture 1 → viewer, triangle top-left (shot `v0`) | smoke | pass — [TESTED: 2026-11-13 · simulator, triangle top-left · testcases/reports/2026-11-13_idea07_simulator.md] |
| C2 | C1 → long tap at (0.75, 0.5), 800 ms → triangle top-right (shot `r1`), log names the right half | use case (R1) | pass — [TESTED: 2026-11-13 · triangle top-right, log `right half` · testcases/reports/2026-11-13_idea07_simulator.md] |
| C3 | C2 → long tap at (0.25, 0.5), 800 ms → triangle top-left again (shot `l1`) | state transition (R3) | pass — [TESTED: 2026-11-13 · triangle back top-left, log `left half` · testcases/reports/2026-11-13_idea07_simulator.md] |
| C4 | C1 → long tap at (0.25, 0.5) → triangle bottom-left (shot `l0`), log names the left half | use case (R2) | pass — [TESTED: 2026-11-13 · triangle bottom-left, log `left half` · testcases/reports/2026-11-13_idea07_simulator.md] |
| C5 | C3 → `SWIPE` Back from the left edge → book page 1 (shot `back`) | control (R4) | pass — [TESTED: 2026-11-13 · book page 1/8, log `Popped` · testcases/reports/2026-11-13_idea07_simulator.md] |

## 5. Not covered — said aloud

- The second fast Back swipe and the heap under the viewer stay with homework 04 (debug9), unchanged by this idea.

## 6. Second set — every gesture follows the picture (the owner, 2026-11-13 14:54 and 15:05)

Basis: «половины давай считать по картинке, убедил» (R5) · «как смотришь на картинку, так и управляешь, да, логично»
(R6) — `ideas/07` → the two last sections. The first set (C1–C5) ran on `9f02db5f`, where the halves followed the
orientation set in Settings; this set runs on the code where the renderer stays in the picture's orientation.

| # | Requirement (EARS) | Fit criterion |
|---|---|---|
| R5 | WHEN the picture is turned and the reader long-taps the right half OF THE PICTURE as it stands upright, the viewer shall turn it clockwise again. | log: the second right long tap names the right half and the turn count rises to 2 |
| R6 | WHILE a picture is turned, the viewer shall read every touch in the picture's orientation. | the simulator shot after a turn is in the picture's orientation (portrait for a quarter turn from landscape) with the picture upright; the Back swipe from the picture's left edge returns to the book |

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| C6 | C1 → long tap at (0.75, 0.5) → log `right half`, turns 1; the shot is portrait, the picture upright, triangle top-left | state transition (R6) | pass — [TESTED: 2026-11-13 · portrait shot, picture upright, turns 1 · testcases/reports/2026-11-13_idea07_08_simulator.md] |
| C7 | C6 → long tap at (0.75, 0.5) of the NEW frame → log `right half`, turns 2 | use case (R5) | pass — [TESTED: 2026-11-13 · log x=359 of 480 right half, turns 2 / x=199 left, turns 1 · testcases/reports/2026-11-13_idea07_08_simulator.md] |
| C8 | C7 → long tap at (0.25, 0.5) → log `left half`, turns 1 | use case (R5) | pass — [TESTED: 2026-11-13 · log x=359 of 480 right half, turns 2 / x=199 left, turns 1 · testcases/reports/2026-11-13_idea07_08_simulator.md] |
| C9 | C8 → `SWIPE` from the left edge of the current frame → book page 1 | control (R6) | pass — [TESTED: 2026-11-13 · Back from the turned frame → page 1/8 · testcases/reports/2026-11-13_idea07_08_simulator.md] |
