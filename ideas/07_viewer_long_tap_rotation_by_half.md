# Idea 07 — in the image viewer a long tap on the right half turns the picture clockwise, on the left half counterclockwise

> **Created:** 2026-11-13 (the owner's request, chat — asked under `resume`, right after his debug9 check) · **Parent:**
> `ideas/02_image_fullscreen_on_tap.md` (the same viewer) · **Status:** 🔧 built and simulator-tested 2026-11-13 14:31 +03:00 on `wip/krinik-debug10` `9f02db5f` (report `testcases/reports/2026-11-13_idea07_simulator.md`); the image comes with idea 05; recon of the code done 2026-11-13 13:53 +03:00; answered
> «можно» in chat, implementation offered for debug10 together with idea 05; the owner's go-ahead 2026-11-13 14:03 +03:00
> («делаем») · **Outbound:** —

`[OWNER] 2026-11-13 13:51 +03:00 · chat:`

> Ещё вопрос по вьюверу картинок: можно сделать, чтобы лонгтам в правой половине экрана вращал картинку по часовой, а лонгтам в левой половине экрана - против часовой?

## Goal vector (Achieve)

Today every long tap in the image viewer turns the picture the same way, so getting back costs three more long taps
(each a full repaint of the e-ink screen). The long tap shall turn the picture toward the side it was made on: the right
half of the screen — clockwise, the left half — counterclockwise.

## Acceptance criteria

1. WHEN the owner long-taps the right half of the screen (halves by the orientation set in the reader's settings), the viewer shall turn the picture
   90° clockwise. Check: simulator, a picture with an arrow/asymmetric shape, shots before and after.
2. WHEN the owner long-taps the left half, the viewer shall turn the picture 90° counterclockwise. Check: the same.
3. A right long tap followed by a left long tap shall return the picture to its first view. Check: the shot equals the first shot.
4. Short taps and swipes in the viewer shall behave as in debug9 (next/previous picture, swipe Back). Check: debug9 cases
   of `testcases/TC_idea02_image_fullscreen_tap.md` re-run.

## Code facts (read 2026-11-13 on `wip/krinik-debug9` `35dc070c`)

- `src/activities/util/BmpViewerActivity.cpp` → `loop()`: `mappedInput.wasScreenLongPress(touchX, touchY)` → `rotate()`;
  the coordinates are read and then ignored. `rotate()` does `viewTurns = (viewTurns + 1) % 4` — one direction only.
- The coordinates are logical in the READING orientation: after painting, the viewer sets the renderer back to
  `holdOrientation()` (the line after the paint in `render`), and `GfxRenderer::tapToLogical` maps by the renderer's
  current orientation. So "left / right half" follows the orientation set in the reader's settings, whatever turn the picture has.
- `ROTATION_ORDER` carries the comment "a long tap turns the picture clockwise"; the VISIBLE direction of `+1` was never
  observed (homework 04 step 7: the rotation was not checked on the simulator). It is observed first, then the halves
  get their signs.
- The size of the change: `rotate(int step)` with `(viewTurns + step + 4) % 4` and one comparison
  `touchX < renderer.getScreenWidth() / 2` in `loop()`.

## Decisions made without the owner (open — to be confirmed)

- `[AI]` The same rule in both viewer entries — a picture from a book (idea 02) and an image file from the file browser:
  they are one activity, `BmpViewerActivity`.
- `[AI]` The halves are split by the middle of the screen width in the orientation set in the reader's settings (the owner's wording, 14:51), not as the picture is turned.

## Plan (ordinary — heaviness 0 of 5: one module, no external truth, one session, KCCP debug only, the owner said «делаем»)

**Goal:** a long tap in the viewer turns the picture toward the side it was made on — right half clockwise, left half
counterclockwise (criteria 1–4 above; the checks run on the simulator, the owner's reader is the last stand).

**Steps:**
- [x] S1. Test pictures get an orientation mark: `tools/make_image_test_epub.py` draws a filled black triangle in the
      top-left corner of every picture (sizes unchanged → the book's pages unchanged); regenerate
      `qa_runs/sd_book_images/image_test.epub`. Reason: the diagonal bands look the same after a quarter turn either way.
- [x] S2. Observe the CURRENT direction on debug9 (`35dc070c`, the built simulator binary): open picture 1, long tap,
      shot. This fixes which sign of `viewTurns` is clockwise on screen.
- [x] S3. Firmware `wip/krinik-debug10` from `wip/krinik-debug9`: `rotate(int quarterTurns)`; `loop()` takes the sign
      from `touchX` against half the screen width (reading orientation); an `LOG_INF` line names the half and the
      direction; the comment carries `[NOT-TESTED]`; `CROSSPOINT_VERSION` → `-debug10`.
- [x] S4. Independent judge (a fresh agent with the diff and this idea, not my conclusions) BEFORE the build; fix findings.
- [x] S5. Build `simulator_x4_pro_win`; run the case set `testcases/TC_idea07_viewer_rotation_by_half.md`:
      R (right long tap → clockwise), L (left → counterclockwise), RL (right then left → the first view),
      K1 (short side tap in the viewer still pages, swipe Back still returns to the book page), control (debug9: a left
      long tap turns the same way as a right one). Run report `testcases/reports/2026-11-13_idea07_simulator.md`.
- [x] S6. Commit locally; the device image waits for idea 05 in the same debug10 (the owner: one build for both).

**Verification:** the case set and the run report above (both born in S5); the shots `qa_runs/idea07_*/shots/*.webp`
show the triangle's corner after each long tap; the log shows the `LOG_INF` line with the half.

**Risks:**
1. The simulator's scripted point frame differs from the firmware's touch frame in the viewer → R and L swap. Reaction:
   the shots and the `LOG_INF` x value show it at once; read both, never only the log.
2. The direction is mirrored on the device against the simulator (the panel is mounted rotated). Reaction: the
   owner's step-7-style check on the reader is the last stand; the homework names the triangle-free way to check
   (a picture with text).
3. A long tap near the middle lands on the "wrong" half. Reaction: none needed — the owner asked for halves; the
   boundary is the middle by his words.

## Judge (S4, a fresh agent on the uncommitted diff vs `35dc070c`, 2026-11-13 14:19 +03:00) — no blockers

- Checks done by derivation: every viewer path ends on `holdOrientation()` before `loop()` reads a touch (paint,
  message, sleep cover, return from the control center), so `tapToLogical` and `getScreenWidth()` share one frame;
  `+1` is clockwise and `-1` counterclockwise for all four reading orientations and every `viewTurns`; the modulo stays
  in 0..3; the input order of `loop()` is unchanged; the `LOG_INF` arguments match.
- NIT fixed: the `drawOrientation()` comment now says "net clockwise quarter turns (a left-half long tap counts -1)".
- MINOR (meaning, not code): the halves are judged in the READING orientation. If the owner turns the reader in his
  hands to look at a turned picture upright, the next long tap's halves run across his new view. The two readings —
  A: the halves by the orientation set in the reader's settings (built; the owner corrected «как держал читалку» to «как настроена ориентация в ОС читалки», 14:51) · B: the halves of the picture as it stands upright — put
  to the owner in chat 2026-11-13 14:20 +03:00, recommendation B; the first long tap is the same under both, so S5
  runs meanwhile.

## The owner's decision on the halves (B)

`[OWNER] 2026-11-13 14:54 +03:00 · chat:`

> половины давай считать по картинке, убедил

So: the right half is the right half of the PICTURE as it stands upright, whatever turn it has and whatever orientation
the viewer opened it in (idea 09 will choose that orientation by the picture's shape). In the reading-orientation frame
of the touch point the picture's right side faces screen-right, -down, -left, -up for `viewTurns` 0, 1, 2, 3 (`+1` =
clockwise, observed in run D0). The code maps the long-tap point by `viewTurns`; the cases C3' and C6 below check it.

## The owner's decision: every viewer gesture follows the picture

Asked 2026-11-13 14:56 (should the swipes, side taps, Back and the shade follow the picture like the halves?),
recommended yes. `[OWNER] 2026-11-13 15:05 +03:00 · chat` — first my recommendation quoted back («рекомендую да: одно
правило на весь вьювер, и оно сразу подходит для идеи 09.»), then:

> как смотришь на картинку, так и управляешь, да, логично

So: after painting, the viewer keeps the renderer in the picture's orientation (`drawOrientation()`), and every touch —
the long-tap halves, the side taps and swipes to the next / previous picture, the Back swipe from the left edge, the
top-edge swipe that opens the shade (the shade then draws in that orientation too) — is mapped in the frame of the
picture as it stands upright. The long-tap code keeps `touchX >= width / 2`, now in that frame; no extra mapping.

## Judge on "every gesture follows the picture" (2026-11-13 15:20 +03:00) — no blockers

- Checked by derivation: every exit restores the saved orientation; the shade over the viewer draws in the picture's
  frame and repaints the viewer on return; the halves are the picture's halves for every base and every turn; +1 is
  clockwise in any frame; no touch is read before the first paint.
- MINOR fixed: after a TURNED book picture closes, a second fast swipe made in the picture's frame was read by the book
  in its own frame — two turns → the next page, one turn → the control center. Fix: while the picture is still on the
  glass the book acts on no touch gesture (not only Back), and the activity manager opens no control center over a
  screen that holds touch gestures (`Activity::holdsTouchGestures()`, the reader returns its window flag). Buttons
  still turn pages. The fix delta goes to a judge of its own before the build.
- NIT fixed: two stale comments (the class comment, the Back swipe "left quarter of the screen").
- ~~`[AI]` The side and front keys follow the picture too~~ — REFUTED by the owner the same minute:
  `[OWNER] 2026-11-13 15:20 +03:00 · chat:` «НЕТ! ФИзические кнопки крутят в одном направлении» · 15:21 «одна кнопка в
  одном, вторая - в противоположном». The keys are read in the reading orientation set in Settings (as in debug9);
  only touches follow the picture. Asked 15:22 whether the keys PAGE the pictures or ROTATE the picture — the answer
  `[OWNER] 2026-11-13 16:01 +03:00 · chat:` «А — листают картинки, как и было». No code change: the keys page the
  pictures (`openSibling`) in the reading orientation, as built in `8538f3dd`.
