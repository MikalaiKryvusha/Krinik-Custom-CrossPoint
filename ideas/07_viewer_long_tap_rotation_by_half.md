# Idea 07 — in the image viewer a long tap on the right half turns the picture clockwise, on the left half counterclockwise

> **Created:** 2026-11-13 (the owner's request, chat — asked under `resume`, right after his debug9 check) · **Parent:**
> `ideas/02_image_fullscreen_on_tap.md` (the same viewer) · **Status:** 🔬 recon of the code done 2026-11-13 13:53 +03:00; answered
> «можно» in chat, implementation offered for debug10 — waits for the owner's go-ahead · **Outbound:** —

`[OWNER] 2026-11-13 13:51 +03:00 · chat:`

> Ещё вопрос по вьюверу картинок: можно сделать, чтобы лонгтам в правой половине экрана вращал картинку по часовой, а лонгтам в левой половине экрана - против часовой?

## Goal vector (Achieve)

Today every long tap in the image viewer turns the picture the same way, so getting back costs three more long taps
(each a full repaint of the e-ink screen). The long tap shall turn the picture toward the side it was made on: the right
half of the screen — clockwise, the left half — counterclockwise.

## Acceptance criteria

1. WHEN the owner long-taps the right half of the screen (as he holds the reader), the viewer shall turn the picture
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
  current orientation. So "left / right half" is as the owner holds the reader, whatever turn the picture has.
- `ROTATION_ORDER` carries the comment "a long tap turns the picture clockwise"; the VISIBLE direction of `+1` was never
  observed (homework 04 step 7: the rotation was not checked on the simulator). It is observed first, then the halves
  get their signs.
- The size of the change: `rotate(int step)` with `(viewTurns + step + 4) % 4` and one comparison
  `touchX < renderer.getScreenWidth() / 2` in `loop()`.

## Decisions made without the owner (open — to be confirmed)

- `[AI]` The same rule in both viewer entries — a picture from a book (idea 02) and an image file from the file browser:
  they are one activity, `BmpViewerActivity`.
- `[AI]` The halves are split by the middle of the screen width as the owner holds the reader, not as the picture is turned.
