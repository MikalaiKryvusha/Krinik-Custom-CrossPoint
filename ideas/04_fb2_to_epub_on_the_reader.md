# Idea 04 — an FB2 → EPUB converter on the reader itself

> **Created:** 2026-11-13 (the owner's request, chat — tossed mid-task while ideas 02/03 were in work) · **Parent:** — ·
> **Status:** 🔬 first recon 2026-11-13 10:58 +03:00; heavy (→ `/plan-epic`), after ideas 02/03 · **Outbound:** —

`[OWNER] 2026-11-13 10:54 +03:00 · chat:`

> Второе: можно ли сделать конверер FB2->EPUB прямо на читалке?
>
> Да, читалка не умеет читать FB2, но можно сделать конвертер? чтобы она конвертировала FB2 в корректный качественный EPUB?

## First recon (2026-11-13, `gh` over upstream + the firmware tree)

- **Upstream CrossPoint has said no to FB2 three times:** issue #592 «Feature Request: fb2 support» — closed NOT_PLANNED
  2026-05-25, «as it impacts memory», open to a PR from the papyrix developer; PR #755 «feat: Add FB2 format support» —
  closed for inactivity 2026-04-18 (a reviewer asked for text-only first, images separately); PR #2484 «in-browser Fb2
  to Epub conversion on FilesPage.html» — closed 2026-07-12: «out of scope for crosspoint itself … belongs in it's own
  web tool». So: a KCCP feature, not an upstream PR.
- **A proven FB2 parser exists:** `bigbag/papyrix-reader` (MIT, 511 stars, pushed 2026-11-13) `lib/Fb2/` —
  `Fb2Parser.cpp` 19.7 KB, `Fb2.cpp` 36.8 KB, `Base64Decoder.h` — «metadata extraction, TOC, and page layout via
  Expat XML». It READS FB2 directly (no EPUB is written).
- **What the firmware already has for a converter:** expat (the EPUB parser's XML), miniz (zip), an on-device TXT → HTML
  conversion (`lib/Txt`, `test/txt_to_html`) — the precedent of converting on the reader.
- **Why conversion (the owner's ask) and not direct reading:** the converted book is an ordinary EPUB — the whole
  proven EPUB path works on it (images, footnotes, hyphenation, the picture tap of idea 02, `<figure>` of idea 03), and
  the memory cost is paid ONCE at conversion, not on every page. The converter can write `<figure>`/`<figcaption>` for
  a picture followed by a «Рис. N…» paragraph — the same rule as the idea 03 re-typeset tool.
- **Price:** ~300 KB RAM, a book of several MB — strictly streaming (FB2 is one XML with base64 pictures inside);
  writing a valid EPUB (mimetype first, stored; OPF, nav, XHTML chapters, pictures). Heavy by the heaviness test
  (new subsystem, external format truth) → `/plan-epic` with an industry recon (FictionBook 2.0 schema, FBReader,
  calibre's FB2 input, papyrix) before any code.
