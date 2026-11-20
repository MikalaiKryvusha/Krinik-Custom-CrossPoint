`[OWNER] 2026-11-20 14:16 +03:00 · chat:` «и есть баг - вьювер картинок при открытии маленьких картинок из книги - их
масштабирует - и очень много грязи на белом вокруг черных объектов. Я фото сфотографировал со своей читалки.

Нужно разобраться, или изначально картинка такая грязная, или вьювер так делает»

`[OWNER] 2026-11-20 14:18 +03:00 · chat:` «ну да, там есть мусор, она грязная в исходнике» · «для такиех картинок нужен
фильтр»

`[OWNER] 2026-11-20 14:19 +03:00 · chat:` «у которых только ЧБ палитра, и низкое разрешение - их нашим рендером нужно
повышать контрастрность, или как это правильно назвать, ну ты понял» · «это не баг, это импрувмент вьювера картинок» ·
«добавляется интеллектуальный фильтр»

`[OWNER] 2026-11-20 14:20 +03:00 · chat:` (on «всё темнее — чисто чёрным») «но так ты уничтожишь аньтиалиасинг, который
заложен в картинку изначально»

The photo from his reader: `ideas/14_owner_photo_dirty_upscale.jpg` (filed first as `bugs/17_…`, commit `3d2df81`; the
owner reclassified it as an improvement 14:19).

---

# Idea 14 — the picture viewer cleans black-and-white low-resolution pictures with a smart filter

> **Created:** 2026-11-20 (the owner's words and photo above) · **Parent:** — · **Status:** 🔬 cause measured
> 2026-11-20 14:20 +03:00 (the source is dirty, the viewer magnifies the dirt); next — the stand run and the filter
> mock-ups · **Outbound:** the filter's look → the owner (mock-ups, taste class)

## Goal vector

**Achieve.** A black-and-white book picture of low resolution (a formula, a diagram, a line drawing) opened in the
viewer shows black on clean white: the faint JPEG noise of the source is gone, the lines stay sharp, and the
anti-aliasing the picture carries on its edges stays (the owner 14:20 — no hard black/white threshold). Photos and
real grayscale pictures look as today.

## Acceptance criteria

1. **WHEN** the viewer opens GEB's `OPS/images/i_016.jpg` (36×91, «12 × 12 = 144»), the background around the digits
   shall carry no gray dots: Scale — share of light-gray (level 2) pixels outside the digits' ink in the viewer's cached
   BMP · Meter — a script over the simulator run's `/.crosspoint/view_*.bmp` · Target — ≤ 1 % (today: to be measured).
2. **WHEN** the viewer opens a photo of the same book (`i_140.jpg`, Turing, 198×247, L), its cached BMP shall equal
   today's (the filter does not fire): Meter — a byte compare of the two caches · Target — identical.
3. The filter's look on the owner's picture is his verdict (mock-ups first; the taste class).

## What was measured (2026-11-20 14:17–14:20 +03:00)

- **The picture.** GEB (the owner's copy `.tmp/geb_in.epub`, the same bytes in the linted copy) `OPS/images/i_016.jpg`:
  JPEG, RGB, 36×91, 3 920 B. Its gray bands (`.tmp/bug17/inspect_source.py`): white 251–255 — 58.4 %, near-white
  240–250 — 15.8 %, light 192–239 — 7.5 %, mid 128–191 — 5.3 %, dark 64–127 — 4.3 %, black 0–63 — 8.6 %. The near-white
  and light bands are JPEG ringing around the digits — invisible on a monitor, visible when the near-white band is
  stretched (`.tmp/bug17/source_x10_stretched.png`). **The source is dirty** (the owner agreed 14:18).
- **The viewer magnifies it** (firmware `wip/kccp-1.1.4`, read, not yet run): `BmpViewerActivity::prepareCache` →
  `fitImage(…, enlarge=true)` scales 36×91 to the screen (×8.8 on 480×800) → `JpegToFramebufferConverter` upscales
  bilinearly, passes every gray through the panel tone curve, then a 4×4 Bayer dither to 4 levels
  (`DitherUtils.h::applyBayerDither4Level`, levels 0/85/170/255). This repo's `panel_curve.txt` maps 240 → 176,
  244 → 181, 248 → 188, 252 → 198: the invisible near-white noise becomes a gray that the dither draws mostly as level 2
  (light gray) — the gray squares on the photo, each JPEG 8×8 block enlarged to ~70 screen px.
- **Open:** the same curve maps 255 → 217, which would dot even pure white at 3/16 of the pixels — yet the photo's
  background far from the digits looks clean. Either the curve on his card differs from this repo's file, or the
  absolute-gray level 2 is lighter on the panel than assumed. Settled by the stand run below and the card's
  `panel_curve.txt` when the reader is on the wire — not by reasoning.

## The owner's darkness-weight rule — the first mock-up (2026-11-20 14:22–14:23 +03:00)

`[OWNER] 2026-11-20 14:22 +03:00 · chat:` «наверное, нужен такой алгоритм, который считает "весс" темноты на картинке, и
диапазон ниже 80% от этого веса - рисуется белам» · «можешь набрасать такой алгоритм тут локально и эту картинку
прогдать?» · «открыть мне обработанный вариант в вс коде» · «я примерно тебе сказал» · «вероятно. я говорю некорректно»

Read as `[AI]`: every pixel weighs its darkness (255 − gray); walking the levels from black to white, the levels that hold
the first P % of the picture's darkness stay as they are, every lighter level becomes white. The mock-up
`.tmp/bug17/mock_viewer.py` copies the viewer's path of `wip/kccp-1.1.4` (fit + bilinear + `panel_curve.txt` + 4×4 Bayer to
4 levels) and renders «today» and P = 80 / 90 / 95 % for GEB `i_016.jpg` and the photo `i_140.jpg` (Turing):
`.tmp/bug17/idea14_darkness_weight_mock.webp` (lossless, opened in VS Code 14:23). The «today» column reproduces the gray
squares of the owner's photo.

| P | formula `i_016` (cut, look) | photo `i_140` (cut, look) |
|---|---|---|
| 80 % | lighter than 155 → white; background clean, digit edges ragged | lighter than 153 → white; posterized, ruined |
| 90 % | lighter than 203 → white; background clean, edges smooth — `[AI]` the best | lighter than 192 → white; face burnt out |
| 95 % | lighter than 239 → white; dirt halos stay near the digits | lighter than 225 → white; background torn |

So the rule cleans line art and needs a DETECTOR that keeps photos out (the «smart» part). Still seen in every column: the
white inside the picture's frame carries faint dots — this repo's curve maps 255 → 217 (the open question above).

## The smart filter — the second mock-up (2026-11-20 14:25–14:26 +03:00)

`[OWNER] 2026-11-20 14:23 +03:00 · chat:` «и такие алгоритмы уже формально существуют и описаны» →
`researches/2026-11-20_line_art_cleanup_algorithms.md` (white point / contrast stretch; background-only cleaning;
line-art vs photo by the histogram's two ends plus a second feature).
`[OWNER] 2026-11-20 14:25 +03:00 · chat:` «вес 90% вроде хорошо сработал, но, фото, конечно же, не нужно гонять таким
алгоритмом. Алгоритм сам должен понимать, фото нужно гонять алгоритмом, или нет»

- **The detector** `[AI]` (`.tmp/bug17/detector_scan.py` over all 180 GEB pictures, table `.tmp/bug17/detector_scan.txt`):
  line art = middle grays (96..223) < 20 % AND white (≥ 224) ≥ 50 %. 113 of 180 pass. The middle share alone let in dark
  pictures (the cover, Bach `i_003`, the painting `i_004`, the film stills `i_100`, dark Escher patterns) — the white
  background feature removes them all; conservative misses: the bold blob text `i_019`, the pattern `i_021`, PNG with
  alpha `i_091` (needs its own handling), notes `i_052`/`i_053` (middle 20–24 %).
- **The mock-up** `.tmp/bug17/idea14_smart_filter_mock.webp` (opened in VS Code 14:26): detector + darkness weight 90 % on
  `i_016` (cut 203), `i_078` (181), `i_088` (178) — cleaned; `i_177` Babbage engraving, `i_140` Turing, `i_003` Bach —
  detected as photos, untouched (identical frames).
- **Still in every frame:** faint dots on the white inside the picture's frame — this repo's curve maps 255 → 217. Option
  `[AI]`: what the filter turned white is drawn pure white past the curve. Open until the card's curve is read.

## The setting (2026-11-20 14:27 +03:00)

`[OWNER] 2026-11-20 14:27 +03:00 · chat:` «Будет опцией в настройках, чекбокс» · «Что-то типа
Чистить фон чертежей»

- The filter is a checkbox in Settings; its label — «Чистить фон чертежей» (the owner's words, «что-то типа»).
- The place: «Настройки → Чтение» — `[OWNER] 2026-11-20 14:28 +03:00 · chat:` «нет, это идет опцией по читалке» · «а не по
  экрану» (on the agent's proposal «Экран → Калибровка экрана», voice call 14:28).
- The default: on — `[OWNER] 2026-11-20 14:30 +03:00 · chat:` «включен» (on the proposal «включён по умолчанию и чистит
  картинки книги везде — и на странице, и в просмотрщике»).
- The scope: everywhere — `[OWNER] 2026-11-20 14:30 +03:00 · chat:` «везде» · 14:31 «и на странице, и во фулл скрин
  просмотрщике, и в просмотре картинок из обзора файлов». In the code that is two paths: the page — `ImageBlock`
  (pixel cache `.pxc`, key `_k<curve hash>`, curve «Калибровка книг», off by default); the viewer — `BmpViewerActivity`
  (book picture tap AND the file browser; cache `view_*.bmp`, curve «Калибровка картинок», on by default; JPEG/PNG through
  the decoders, BMP through `BmpToBmpConverter`).

## Plan

Done before the firmware work: [x] recon (research 2026-11-20) · [x] mock-ups (the owner picked 90 %, 14:25) · [x] the
setting's label, place, default and scope (the owner, 14:27–14:31).

`FORK: options <white point by a fixed band | white point by the picture's darkness weight> · price of error <a photo
loses its tones; noise wider than the band stays> · consulted <research 2026-11-20 (white point / contrast stretch is the
established cure; the detector by the histogram's two ends + a second feature) · the owner 14:22–14:25: his darkness
weight at 90 %, photos left alone>` — decided: the darkness weight at 90 % behind the two-feature detector.

Branch `wip/kccp-line-art-filter` from `wip/kccp-1.1.4` `8a8b44bc` (mergeable into 1.1.4 or 1.1.5 — the owner decides
which release carries it).

- [ ] **F1 — the core**, `src/util/LineArtFilter.h` (pure, host-testable): `isLineArt(hist)` (middle 96..223 < 20 % AND
      white ≥ 224 ≥ 50 %), `whiteCut(hist, 90)` (the darkness-weight cut), `composeTone(curve, cut, out[256])` (filter
      then the panel curve — the decoders already take one 256-entry tone table, so no decoder pixel loop changes). Host
      test `test/line_art_filter/` on the histograms of GEB `i_016` (line art, cut 203), `i_140` (photo), `i_003` (dark),
      a bilevel picture (no-op), all-white, all-black, empty; mutation proof (detector inverted, cut at 80 %).
- [ ] **F2 — the histogram pass**: one gray histogram per picture before its render — JPEG (JPEGDEC at a reduced scale
      for big pictures), PNG, BMP; 1 KB of counters, no new heap beyond the decoder's own.
- [ ] **F3 — the viewer** (`BmpViewerActivity::prepareCache`, book picture and file browser): when the setting is on and
      the picture is line art, the composed tone table; the cache key carries the cut.
- [ ] **F4 — the page** (`ImageBlock`): the same; the `.pxc` name carries `_f<cut>`.
- [ ] **F5 — the setting**: `CrossPointSettings::cleanLineArt = 1`, key `cleanLineArt`, a Toggle in «Чтение»
      (`STR_CAT_READER`), `STR_CLEAN_LINE_ART` «Чистить фон чертежей» / «Clean drawing background».
- [ ] **F6 — verification**: the independent review BEFORE the build (the owner's rule); the full host suite; simulator
      runs — the file browser opens `i_016.jpg` (clean), `i_140.jpg` (identical to today), the setting off = today (the
      control case), a GEB page with `i_016` on the owner's settings (П4); the run report in `testcases/reports/`.
