# Research — keeping a picture and its caption on one page (idea 03)

> **Created:** 2026-11-13 · **Parent:** `ideas/03_keep_image_caption_with_image.md` · **Status:** 🔬 first sweep
> 2026-11-13 11:02 +03:00 (web + own code + the owner's books) · **Outbound:** the firmware half is an upstream PR
> candidate (standard semantics)

## The industry practice (web sweep, 2026-11-13)

- **The standard markup** is `<figure>` with `<img>` and `<figcaption>`, and the reader is asked not to split it:
  `break-inside: avoid` on the figure; the legacy name `page-break-inside: avoid` is an alias and is what older e-book
  engines honour — set both. MDN's own example of `break-inside: avoid` is a figure with its caption
  ([MDN break-inside](https://developer.mozilla.org/en/docs/Web/CSS/break-inside),
  [MDN multicol breaks](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_multicol_layout/Handling_content_breaks_in_multicol_layout),
  [modern-css.com page-break-inside](https://modern-css.com/reference/properties/page-break-inside/)).
- **E-book practice:** wrap picture + caption in one block with `page-break-inside: avoid`
  ([MobileRead wiki: Caption](https://wiki.mobileread.com/wiki/Caption),
  [MobileRead wiki: Figure](https://wiki.mobileread.com/wiki/Figure)); readers honour it unevenly, Kindle is the known
  exception ([Jutoh KB0124](https://www.jutoh.com/kb/html/section-0124.html),
  [Adobe community: captions split in Kindle Previewer](https://community.adobe.com/questions-671/book-epub-figures-captions-page-breaks-what-do-ereaders-see-883610),
  [InDesignSecrets: keep captions on same page, reflowable EPUB](https://indesignsecrets.com/topic/keep-captions-on-same-page-as-image-reflowable-epub/)).
- **The fallbacks named there:** the caption burnt into the picture (keeps them together; «not searchable and it may
  not scale very well») — the same price this project found; a table with a `<caption>`; a page break before the picture.
- **Not found:** how crengine (KOReader) treats `break-inside` on a figure — no source; an open question, not a claim.

## This firmware today (`wip/krinik-debug8`, re-read 2026-11-13)

- `figure` is a plain block (`ChapterHtmlSlimParser.cpp:56`), `figcaption` is unknown; `page-break-*: avoid` is not
  honoured (only forced breaks count); a picture that does not fit the rest of the page moves whole to the next page
  (`:1901-1913`) and is never shrunk; keep-with-next exists for h1–h6 only.

## The owner's books (census 2026-11-13 10:53 +03:00, 10 EPUB on his card)

0 `<figure>`, 0 `<figcaption>`; captions as a «Рис. N…» paragraph right after the picture in 2 books (148 + 98). The
FB2 source of one of them marks it the same way (`<image/>` then `<p><emphasis>Рис. …`), FB2 has no caption element.

## Conclusion for the plan

The standard answer has two halves, and both are ours to build: the books get the standard markup (a re-typeset tool;
an FB2 converter — idea 04 — writes it at birth), and the reader honours it (`<figure>` with `break-inside: avoid` kept
on one page, the picture shrunk when the two do not fit; the owner accepted a smaller in-page picture). Industry
confirms there is no third, engine-free way except burning the caption into the picture.
