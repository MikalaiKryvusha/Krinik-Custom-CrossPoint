# Idea 02 — tap on an image in a book opens it full screen

> **Created:** 2026-11-13 (the owner's request, chat) · **Parent:** — · **Status:** 🔧 planned 2026-11-13 10:45 +03:00;
> built — debug9 image 11:32, on the reader's card 11:47; NOT verified on the reader yet (homework 04) · **Outbound:** —
> (KCCP only for now; an upstream PR is a later question)

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

1. [x] Firmware branch `wip/krinik-debug9` from `wip/krinik-debug8` (`c072214b`), local in `firmware/`.
2. [x] `lib/Epub/Epub/PageImageTarget.h`: a picture's path + rect on the page, `contains()` and `imageAtPoint()` — the
   same page-relative coordinates and oriented margins as `PageLink` / `linkAtPoint`.
3. [x] `EpubReaderActivity`: when a page is shown, keep its picture targets beside `currentPageLinks`; in `loop()` one
   tap query serves links first, then pictures, BEFORE the centre-tap menu and the side-tap turns (the owner: the picture
   tap beats the navigation taps). A hit opens the viewer with `startActivityForResult`; its return repaints the page.
4. [x] `BmpViewerActivity`: a book-picture mode — one picture, no folder siblings, Back = `finish()` (back into the
   book) instead of the file browser.
5. [x] Host test `test/page_image_target/` — 4/4 pass; red on the `<=` edge mutation (2 of 4 fail), 2026-11-13 11:10.
6. [x] Independent judge on the diff (owner's order: review first, build after) — APPROVE WITH FIXES, no blocker,
   2026-11-13 ≈11:06; findings traced in the code and answered below («Judge findings»).
7. [~] Simulator done 2026-11-13 11:12–11:27 (report `testcases/reports/2026-11-13_idea02_simulator.md`: C1–C5,
   K1–K3 pass, C6 skipped there; the dark page after the viewer was the simulator's own defect — `bugs/06`, fixed in
   the simulator `49ded1a`); firmware `526c7452` + `35dc070c` (the judge's last delta: no forced clean base); C7 (a PNG
   picture) pass 11:34. Done: `x4pro-krinik-debug` → `1.1.1-debug9` image 11:32 (SHA256 `6b5f4f36…`) → card
   `/.firmware/` 11:47 (SHA256 checked on the card) → reader ejected → homework 04. Left: the owner's check on the
   reader and his serial log read during it (`tools/serial_log.py`).
8. [ ] KCCP 1.1.3 itself (debug line + release 1.1.2 merged + this feature) is assembled after the owner's check —
   `STATUS.md` → Open work 2.

## Risks

- (a) RAM: the viewer opens on top of a live reader (the reader stays on the activity stack). Seen on the device only —
  watch the owner's serial log for `OOM`; fallback: the viewer reports «not enough memory» and the book stays.
- (b) A page that is all picture: side taps on it open the picture instead of turning (the owner's priority); buttons
  and swipes still turn the page.
- (b) A picture whose file was not extracted (decode failed): the tap falls through to the zones as today.
- (c) Tiny inline pictures (a formula glyph) become tap targets too — watch the sample book.

## Judge findings (independent review of the diff, 2026-11-13) and what was done

| # | Finding | Done |
|---|---|---|
| 1 | `width > 0 && height > 0` in `contains()` is dead code | removed; the empty-rectangle test stays — it reddens on `<=` |
| 2 | with touch controls off a centre tap on a picture opens the menu | kept: the same gate as links (`touchReaderControls`); the owner's setting is on |
| 3 | during auto page turn a centre tap only stops the auto turn | kept: stopping the auto turn first is the existing rule for every centre tap |
| 4 | GIF pictures are drawn in books but the viewer cannot open them | known gap (the viewer reads BMP/JPEG/PNG); the tap falls through to the zones |
| 5 | no minimum picture size | kept, risk (c); watched on the sample book |
| 6 | free heap under the viewer is not measured | the tap logs `heap free / max block` at INF — read in the owner's serial log |
| 7 | a second quick Back swipe, while the picture is still on the glass, pages one page back | fixed: until the page is repainted a Back swipe turns no page (`backSwipeBelongsToViewer`); the owner turns pages by tap AND swipe (`pageTurnGesture=0`) |
| 8 | sleeping from the viewer gives the plugin sleep event no book info | existing pattern of every screen pushed over the book; not changed |
| NIT | wrong reason in the lock comment | fixed |
| NIT | Confirm in the viewer still offers «set as sleep cover» for a book picture | kept: the viewer's own feature, behind its confirmation dialog |
| Δ1 | the Back-swipe flag set before the push can be cleared by a last repaint before the viewer shows | fixed: set in the pop handler |
| Δ2 | `pagesUntilFullRefresh = 1` at the pop is a no-op on the owner's settings and a flash in night mode / B/W images | removed (`35dc070c`) |
| Δ3 | the simulator fix (reset of the absolute gray mode on a plain refresh) — any path broken? | none found: no refresh between an absolute base and its gray pass in the viewer, the reader or the sleep screen |

## Decisions made without the owner (so far)

- `[AI]` In the viewer a book picture is alone: no prev/next through the book's pictures (the cache folder is not a
  gallery); the long tap still rotates, Confirm still offers «set as sleep cover».
- `[AI]` The full-screen picture goes through the viewer's own «pictures» tone curve (Калибровка картинок), not the
  books curve — the viewer's render path is the one that curve was measured for.
- `[AI]` With touch controls off the picture tap is off too (the same switch as links).
- `[AI]` A GIF picture is not opened (the viewer reads BMP/JPEG/PNG). The sample book holds 103 JPEG + 77 PNG and no
  GIF (counted on its local copy 2026-11-13); the owner's other books were not counted (the reader left the wire).
- `[AI]` The image-tap log line is INF (visible in the debug image's serial log), with the free heap.

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
