# Idea 09 — the image viewer opens a picture in the orientation that fits its shape

> **Created:** 2026-11-13 (the owner's request, chat — given while idea 07's halves question was being explained) ·
> **Parent:** `ideas/07_viewer_long_tap_rotation_by_half.md` (the same viewer) · **Status:** 🔧 written 2026-11-13 on `wip/kccp-1.1.3-debug2` (S1–S2, judged, uncommitted), simulator next; the owner's original,
> verbatim · **Outbound:** —

`[OWNER] 2026-11-13 14:51 +03:00 · chat` (on idea 07's question, the option A wording «как ты держал читалку при чтении»):

> А (сделано сейчас): прошивка делит экран на левую и правую половины так, как ты держал читалку при чтении,
>
> Только не "как держал читалку", а как настроена ориентация в ОС читалки

`[OWNER] 2026-11-13 14:53 +03:00 · chat:`

> и можно было бы определять соотношение сторон картинки и если
> А) она горизонтальная, и читалка в горизонтальной ориентации - картинка открывается во вьювере в этой горизонтальной ориентации
> Б) она горизонтальная, а читалка в вертикальной ориентации - картинка открывается во врювере в ориентации Альбомная 180
> В) она вертикальная, и читалка в вертикальной ориентации - картинка открывается во вьювере в этой вертикальной ориентации
> Г) она вертикальная, а читалка в горизонтальной ориентации - картинка открывается в классической портретной ориентации.
>
> Это же касатеся вьювера, отрываеющего как картинки из хранилища устройства, так и картинки через читалку

## Goal vector (Achieve)

The image viewer opens every picture the way its shape reads best, without a long tap: a wide picture in a landscape
orientation, a tall one in a portrait orientation. Today the viewer always opens in the reading orientation set in
Settings, and a wide picture in a portrait reader (or a tall one in a landscape reader) needs a long tap first. The rule
covers both entries: a picture from the file browser and a picture tapped in a book (the owner, 14:53: «Это же
касатеся вьювера, отрываеющего как картинки из хранилища устройства, так и картинки через читалку»).

## Acceptance criteria (the owner's four cases, 14:53; orientation names as Settings shows them)

| # | Situation | Opens in | Check (simulator) |
|---|---|---|---|
| А | wide picture, reading orientation landscape («Альбомная» or «Альбомная 180°») | that reading orientation | shot: the picture fills the landscape frame; log `View turns: 0` |
| Б | wide picture, reading orientation portrait («Книжная» or «Инверсия») | «Альбомная 180°» | shot landscape; log names the turn |
| В | tall picture, reading orientation portrait | that reading orientation | shot portrait; `View turns: 0` |
| Г | tall picture, reading orientation landscape | «Книжная» (the classic portrait) | shot portrait; log names the turn |

Plus: a square picture (or one whose size cannot be read) opens in the reading orientation `[AI]`; a long tap turns
from there as today (idea 07); the halves, swipes and Back follow the picture as it stands (idea 07, unchanged).

## Code facts (read 2026-11-13 on `wip/kccp-1.1.3-debug2` `84c33f85`)

- `BmpViewerActivity::drawOrientation()` = the reading orientation (`holdOrientation()`, from `SETTINGS.orientation`)
  turned by `viewTurns` along `ROTATION_ORDER` {Portrait, LandscapeCounterClockwise, PortraitInverted,
  LandscapeClockwise}; `rotate()` changes `viewTurns`; `viewTurns` today survives paging to a sibling.
- Settings values: `PORTRAIT=0` «Книжная», `LANDSCAPE_CW=1` «Альбомная», `INVERTED=2` «Инверсия», `LANDSCAPE_CCW=3`
  «Альбомная 180°» (the panel's native orientation, `GfxRenderer::LandscapeCounterClockwise`).
- A new picture is set in two places: `onEnter()` (both entries: the file browser and the book picture of idea 02) and
  `openSibling()` (page keys / swipes in the file browser).
- Sizes: `JpegToFramebufferConverter`, `PngToFramebufferConverter`, `GifToFramebufferConverter` have
  `getDimensionsStatic(path, ImageDimensions&)`; a BMP reads its size from `Bitmap::parseHeaders()` (as `prepareCache`).
  The sleep cover «By Image» already chooses wide → LandscapeCounterClockwise, else Portrait (`BmpViewerActivity.cpp`
  ~540) — the same mapping as the owner's Б and Г.

## Plan (ordinary — heaviness 0 of 5: one module, no external truth, one session, KCCP only, the owner asked)

- [x] S1 `shapeTurns()`: read the picture's size; wide = w > h, tall = h > w; return the quarter turns from the reading
      orientation to the target of the table above (0 for А, В, square, unreadable). Comment `[NOT-TESTED]`.
- [x] S2 `applyShape()` (sets `viewTurns` by the shape, remembers the orientation it was set for): the FIRST `onEnter()`
      (it is re-called after the sleep-cover dialog — a manual turn must survive), every `openSibling()`, and the
      «back from a sheet» repaint when the reading orientation changed under it. Every picture opens by its own shape;
      a long-tap turn of one picture does not carry to the next `[AI]`.
- [x] S3 Judge (fresh agent: the diff + this document) before the build — 2026-11-13: the 16 orientation × shape cases
      match А–Г; fixed: the re-entry lost a manual turn, the shade's «Ориентация» drew a wide picture portrait in a
      landscape reader, open-time decisions left no log; EXIF is ignored by the painter and by `shapeTurns` alike.
- [ ] S4 Simulator: a card with one wide and one tall picture in a folder and in the test book; cases А–Г in both
      reading orientations of each kind (8 runs), the shot and `View turns:` read; a run report.
- [ ] S5 Commit on the 1.1.3 debug line; the owner's check comes with the next image's homework.

## Decisions made without the owner (open — to be confirmed)

- `[AI]` A square or unreadable picture opens in the reading orientation.
- `[AI]` Each picture applies the rule when it is shown; a long-tap turn is not carried to the next picture.
- `[AI]` A change of the reading orientation from the shade while a picture is open applies the rule again for the new
  orientation (changed 2026-11-13 after the judge: keeping the turn drew a wide picture portrait in a landscape reader,
  against case А). A manual long-tap turn survives a shade that does not change the orientation.
