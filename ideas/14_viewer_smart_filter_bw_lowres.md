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

## Plan

1. [ ] Stand: a simulator card with `i_016.jpg`, `i_140.jpg` and the owner's `panel_curve.txt` (the card's copy when
       the reader is on the wire; this repo's file until then), opened in the viewer; the cached BMPs read and measured
       (criteria 1–2 «today»).
2. [ ] Recon (the fork below): how readers and image tools clean line art — binarization (a threshold, Otsu), auto
       levels (white/black point), and how they DETECT a bilevel picture (histogram share near the two ends).
3. [ ] Mock-ups on the owner's picture and on the photo control: today · auto levels (the near-white band to white,
       the near-black band to black, the edge tones stretched, not cut) at two or three band widths, the same 480×800
       frame, blind labels — shown to the owner on a page. Hard binarization is out: it destroys the picture's
       anti-aliasing (`[OWNER] 2026-11-20 14:20 +03:00`, quoted above).
4. [ ] His pick → firmware: the detector + the filter in the viewer's decode path (`JpegToFramebufferConverter`,
       `PngToFramebufferConverter`), a host test on both pictures, the simulator run, the cache version bump.

`FORK: options <auto levels: white/black point at a fixed band | auto levels: band from the picture's own histogram>
· price of error <a photo or a gray drawing loses its tones; noise wider than the band stays> · consulted <the owner
14:20: binarization out · recon of step 2 — pending · the owner's eye on the mock-ups>` — not decided yet.
