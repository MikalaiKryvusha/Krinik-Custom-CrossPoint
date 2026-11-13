# Idea 02 — tap on an image in a book opens it full screen

> **Created:** 2026-11-13 (the owner's request, chat) · **Parent:** — · **Status:** 🔧 planned 2026-11-13 10:50 +03:00, in
> work · **Outbound:** — (KCCP only for now; an upstream PR is a later question)

## Goal vector (Achieve)

The owner reads books with many pictures (sample: Hofstadter, «Гёдель, Эшер, Бах», on his reader) and cannot look at a
picture closer than its in-page size. A tap on a picture on the page shall show it full screen; the swipe Back shall
return to the same book page. Target: KCCP 1.1.3, tested first as a KCCP debug build (`x4pro-krinik-debug`).

## Acceptance criteria (scenario form)

1. Tap on a picture.
   - Situation. A book page with one picture, touch controls on, any reading orientation (the owner reads landscape 180).
   - Action. The reader taps inside the picture, in the centre zone or in a side zone.
   - Result. The picture fills the screen in the image viewer; no menu opens, no page turns.
   - Check. Simulator run: `TAP` at the picture's centre → shot shows the viewer; log has `ERS: Image tap` and no `[ERR]`.
2. Swipe Back returns to the book.
   - Situation. The viewer shows a picture opened from a book page N.
   - Action. The reader swipes Back (left to right from the left quarter of the screen).
   - Result. The same book page N is on screen.
   - Check. Simulator run: `SWIPE` from x < 120 to the right → shot equals the page shot taken before the tap.
3. Taps outside pictures keep working (control case).
   - Situation. The same page.
   - Action. The reader taps the centre zone on text, then a side zone on text.
   - Result. The centre tap opens the reader menu; the side tap turns the page.
   - Check. Simulator run with both taps → shots show the menu, then the next page.
4. Hit-test on the oriented page. Check: host test `ctest -R PageImageTarget` → passed (inside, edges, outside, margins).

## Plan

1. [ ] Firmware branch `wip/krinik-debug9` from `wip/krinik-debug8` (`c072214b`), local in `firmware/`.
2. [ ] `lib/Epub/Epub/PageImageTarget.h`: a picture's path + rect on the page, `contains()` and `imageAtPoint()` — the
   same page-relative coordinates and oriented margins as `PageLink` / `linkAtPoint`.
3. [ ] `EpubReaderActivity`: when a page is shown, keep its picture targets beside `currentPageLinks`; in `loop()` one
   tap query serves links first, then pictures, BEFORE the centre-tap menu and the side-tap turns (the owner: the picture
   tap beats the navigation taps). A hit opens the viewer with `startActivityForResult`; its return repaints the page.
4. [ ] `BmpViewerActivity`: a book-picture mode — one picture, no folder siblings, Back = `finish()` (back into the
   book) instead of the file browser.
5. [ ] Host test `test/page_image_target/` (the hit-test, guard proven red on a broken `contains`).
6. [ ] Independent judge on the diff (owner's order: review first, build after), fixes.
7. [ ] Builds when the machine lock is free: simulator `simulator_x4_pro_win`, run criteria 1–3 on an OWN generated test
   book (third-party books stay off the repo), WebP shots read; then `x4pro-krinik-debug` → `1.1.1-debug9` image →
   card `/.firmware/` → eject → homework for the owner; his serial log read during his check.
8. [ ] KCCP 1.1.3 itself (debug line + release 1.1.2 merged + this feature) is assembled after the owner's check —
   `STATUS.md` → Open work 2.

## Risks

- (a) RAM: the viewer opens on top of a live reader (the reader stays on the activity stack). Seen on the device only —
  watch the owner's serial log for `OOM`; fallback: the viewer reports «not enough memory» and the book stays.
- (b) A page that is all picture: side taps on it open the picture instead of turning (the owner's priority); buttons
  and swipes still turn the page.
- (b) A picture whose file was not extracted (decode failed): the tap falls through to the zones as today.
- (c) Tiny inline pictures (a formula glyph) become tap targets too — watch the sample book.

`[OWNER] 2026-11-13 10:34 +03:00 · chat:`

> есть задание на фичу для KCCP 1.1.3
>
> Тап по изображению в книге должен открывать изображение на Full Screen

`[OWNER] 2026-11-13 10:39 +03:00 · chat:`

> жест свайп Назад - должен вести из Full Screen просмотра картинки назад в книгу

> можно переиспользовать вьювер картинок из проводника?

`[OWNER] 2026-11-13 10:40–10:41 +03:00 · chat:`

> что тап попал в картинку - вероятно, этого нет и придётся делать

> сейчас ридер тап в центре воспринимает как жест "тап в центре"

> нужно, чтобы была новая фича - тап в область миниатюры изодражения в книге - и это важнее, чем тамы навигации по книжке

`[OWNER] 2026-11-13 10:35 +03:00 · chat` (test material and the reader on the wire):

> могу дать тебе пример книги, где много таких изображений внутри книжки - дам читалку на провод, почитаешь. И сможешь почитать логи с читалки, давно не читали

> читалка на проводе
>
> Эшлек, Бах - книга на читалке

> там много картинок внутри книги
