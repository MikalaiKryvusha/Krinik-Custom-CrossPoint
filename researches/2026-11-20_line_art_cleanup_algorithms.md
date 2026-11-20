# Research — cleaning the JPEG noise of low-resolution line art before an e-ink render, and telling line art from a photo

> **Created:** 2026-11-20 (the owner 14:23 «и такие алгоритмы уже формально существуют и описаны», idea 14) ·
> **Parent:** `ideas/14_viewer_smart_filter_bw_lowres.md` (plan step 2, the FORK's recon) · **Status:** first sweep
> 2026-11-20 14:25 +03:00 (web search, the sources below — summaries of search results, the full texts not read yet) ·
> **Outbound:** —

## The problem in one line

A small black-and-white book picture (GEB `i_016.jpg`, 36×91) carries faint JPEG ringing (240–250 gray) around its
strokes; the viewer enlarges it ×8.8 and the panel curve makes the ringing visible gray. Wanted: the ringing white, the
strokes and their anti-aliasing kept, photos untouched.

## Established techniques

1. **White point (levels / contrast stretch).** Map every gray lighter than a white point W to pure white and stretch
   [B..W] to [0..255]. W either a fixed level (`-level`) or a PERCENTILE of the pixels (`-contrast-stretch`: «makes a
   certain percentage of pixels white»; `-normalize` = `-contrast-stretch 2x99%`; Pillow `ImageOps.autocontrast(cutoff)`)
   — ImageMagick forum, fmw42. For a scanned book page a white-point move, not a noise filter, is the recommended cure
   for light-gray speckles. The owner's darkness-weight rule (idea 14) is this technique with the percentile taken over
   darkness mass instead of the pixel count.
2. **Background-only cleaning** (Xerox, US7532767 / US7634150 «Removing ringing and blocking artifacts from JPEG
   compressed document images»): separate the text from the background with an automatically found threshold and
   remove the ringing only in the background; the ringing near and inside the strokes is masked by the strokes and left
   alone — the strokes' edges keep their gray (the owner's anti-aliasing concern, 14:20).
3. **E-ink comic converters** — Kindle Comic Converter (`ciromattia/kcc`): autocontrast / auto-level for gray pages,
   gamma 1.8 by default to darken faded art; since v8.0.4 autocontrast is not applied to color content.

## Telling line art from a photo (the «smart» part)

- A bi-tonal picture clusters its grays at the two ends of the histogram; text-like when the count on the white side
  outweighs the rest (US6198841); the gap between the two highest histogram peaks as a feature (US8634650); per-cell
  gray spread with valley detection (US5546474); density slicing (US5812695).
- The patents warn: transitional grays of line art (anti-aliasing, JPEG) and high-contrast photos make a histogram-only
  test ambiguous — combine with a second feature (local gray spread, transition density, region size). Google's
  «Finding Images and Line Drawings in Document-Scanning Systems» is the same problem in a scanning pipeline.

## Sources

- ImageMagick forum, `-contrast-stretch` / white-point threads: https://magick.imagemagick.org/viewtopic.php?p=40517 ·
  https://jqmagick.imagemagick.org/discourse-server/viewtopic.php?p=115704
- Xerox patents: https://patents.google.com/patent/US7532767 · https://patents.google.com/patent/US7634150
- A scanned-book cleanup Q&A (white point in GIMP): https://www.uniquephoto.com/community/qa/how-can-i-clean-up-jpeg-compression-artifacts-in-a-scanned-book-image-using-gimp
- Kindle Comic Converter: https://github.com/ciromattia/kcc · release v8.0.4 https://newreleases.io/project/github/ciromattia/kcc/release/v8.0.4
- Line art vs photo: https://patents.google.com/patent/US5812695 · https://patents.google.com/patent/US6198841 ·
  https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8634650 · https://patents.google.com/patent/US5546474 ·
  https://research.google.com/pubs/pub35522.html
