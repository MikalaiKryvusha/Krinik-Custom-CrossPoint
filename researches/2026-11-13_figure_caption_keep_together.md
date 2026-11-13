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

## How a caption looks — the standards the owner named (2026-11-13 11:13 +03:00: «подписи картинок - это не параграф,
## они не обязаны слушаться правила отступа для красной строки параграфа» · «читай ГОСТЫ» · «особенно кост оформления
## пояснительных записок БГУИР, курсовых и дипломных работ»)

**СТП 01-2017 БГУИР «Дипломные проекты (работы). Общие требования»** — read in the primary text (PDF from
`library.bsuir.by/m/12_101945_1_141949.pdf` and `www.bsuir.by/m/12_100229_1_124328.pdf`, extracted with `pdftotext`;
the 2010 edition is the other PDF; a 2024 edition is mentioned by a 2023 BSUIR guide, not read), section 2.5, verbatim:

- 2.5.4: «Иллюстрацию, помещенную в тексте между абзацами, располагают по центру и отделяют от текста и подрисуночной
  подписи одной пробельной строкой (приложение Н).»
- 2.5.5: «Каждый рисунок сопровождают подрисуночной подписью. Подпись должна содержать слово «Рисунок» без сокращения
  и порядковый номер иллюстрации арабскими цифрами…» · «Все иллюстрации должны иметь наименования, которые записывают
  после номера рисунка через знак тире с прописной буквы. Точки после номера и наименования рисунка не ставят,
  например: Рисунок 2.1 – Структурная схема нескорректированной системы управления» · «Подпись и наименование
  располагают, выравнивая по центру относительно рисунка.» · «Все пояснительные данные помещают между рисунком и
  подрисуночной подписью.» · «Все подрисуночные подписи в пояснительной записке следует выполнять единообразно.»
- 2.5.6: «Рисунок, как правило, выполняется на одной странице.»

**ГОСТ 7.32-2017** (Отчет о НИР. Структура и правила оформления), 6.5 — read only through a mirror that cut the page
(legalacts.ru) and a model summary of the cut part, so NOT verbatim: 6.5.7 — the caption is centred under the figure,
«Рисунок 1 – Схема прибора», no full stop; 6.5.1 — the figure stands right after the text that first mentions it or on
the next page. Verbatim from the visible part, 6.1.1: «Абзацный отступ должен быть одинаковым по всему тексту отчета
и равен 1,25 см.» — the indent is a property of TEXT paragraphs; the caption rule is centring. Reading 6.5 verbatim
from an official copy stays open.

**What it gives the e-reader (`[AI]` reading, for the plan):** a caption is centred under its picture, with no
first-line indent, separated from the picture by one line, never ending with a full stop, kept on the picture's page.
Open for the owner: whether the re-typeset tool also rewrites the book's own label («Рис. 2.» → «Рисунок 2 –») — that
edits the book's text; the agent's default is to keep the author's wording and change only the layout.

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
