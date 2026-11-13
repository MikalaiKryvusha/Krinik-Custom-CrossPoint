# Research — idea 03: caption standards (ГОСТ, БГУИР, EPUB figure/figcaption)

> **Created:** 2026-11-13 · **Parent:** ideas/03_keep_image_caption_with_image.md · **Status:** recon · **Outbound:** —

**What this is.** The second sweep for idea 03, ordered by the owner's words of 2026-11-13 11:13 +03:00 («подписи
картинок - это не параграф, они не обязаны слушаться правила отступа для красной строки параграфа» · «читай ГОСТЫ» ·
«особенно кост оформления пояснительных записок БГУИР, курсовых и дипломных работ»). It builds on the first sweep
`researches/2026-11-13_figure_caption_keep_together.md` (СТП 01-2017 read verbatim there; ГОСТ 7.32 only through a cut
mirror; crengine unknown) and closes its gaps: ГОСТ 7.32-2017 and both current editions of ГОСТ 2.105 are now read in
full text, the BSUIR standard is the current СТП 01–2024, and the reading-system claims rest on the engines' own code
and specs where those exist.

**Method.** Primary texts were downloaded into `.tmp/` (HOUSE_RULES П1) and read as text (`pdftotext -enc UTF-8
-layout` for PDFs, a tag-stripper for HTML), so every quote below is copied from the source file, not from a search
summary. Dash characters were counted by code point with a script, because the dash is one of the owner's rules.
Sources were read 2026-11-13 19:20–19:33 +03:00. `[AI]` marks the agent's reading of a source, never a source's words.

---

## 1. Russian and Belarusian standards for figure captions

### 1.1 ГОСТ 2.105 — two current editions, one per country

**ГОСТ 2.105-95 (interstate, «ЕСКД. Общие требования к текстовым документам», with Изм. № 1 of 2006)** — the edition
the BSUIR standard cites in 2024 (СТП 01–2024, 1.2.17: «Правила оформления приложений изложены в ГОСТ 2.105–95»).
Adopted by twelve states including Belarus (Wikisource front matter: voting table with BY; «Дата введения 1996—07—01»).
Text read from Wikisource (a transcription, not a scan): https://ru.wikisource.org/wiki/ГОСТ_2.105—95, clause 4.3.1:

- «Иллюстрации могут быть расположены как по тексту документа (возможно ближе к соответствующим частям текста), так и
  в конце его.»
- «Иллюстрации, за исключением иллюстраций приложений, следует нумеровать арабскими цифрами сквозной нумерацией. Если
  рисунок один, то он обозначается «Рисунок 1».»
- «Допускается нумеровать иллюстрации в пределах раздела. … Например — Рисунок 1.1.»
- «Допускается не нумеровать мелкие иллюстрации (мелкие рисунки), размещенные непосредственно в тексте и на которые в
  дальнейшем нет ссылок.»
- «Иллюстрации, при необходимости, могут иметь наименование и пояснительные данные (подрисуночный текст). Слово
  «Рисунок» и наименование помещают после пояснительных данных и располагают следующим образом: Рисунок 1 — Детали
  прибора.» — in the transcription the example is `Рисунок 1` + U+00A0 (no-break space) + U+2014 (em dash).
- Not in the text: alignment, spacing, font, splitting across pages. «располагают следующим образом» points at a printed
  layout of the example that the transcription does not show — **the printed layout was not seen**.

**ГОСТ Р 2.105-2019 (Russian national standard, same title)** — «Дата введения 1 февраля 2020 года» (later moved:
«Приказом Росстандарта от 30.12.2020 N 1437-ст дата введения в действие перенесена на 01.02.2021»), «4 ВВЕДЕН
ВПЕРВЫЕ», «6 ИЗДАНИЕ (июнь 2024 г.) с Поправкой (ИУС 9-2024)», amendments «Изменения N 1 … от 30.12.2020 N 1439-ст»
and «Изменения N 2 … от 08.11.2023 N 1361-ст». Read from the database copy on meganorm.ru (the scanned PDFs on guap.ru
and lib.uni-dubna.ru could not be read — see §6):
https://meganorm.ru/mega_doc/norm/gost-r_gosudarstvennyj-standart/0/gost_r_2_105-2019_natsionalnyy_standart_rossiyskoy.html

- 6.9.1: «Графический материал, содержащийся в документе (чертеж, схема, диаграмма, рисунок и т.п.), помещают в текст
  после первой ссылки на него одним из следующих способов: - в пункте или сразу после пункта, содержащего ссылку; - в
  конце раздела (подраздела, приложения), содержащего ссылку; …»
- 6.9.3: «… следует нумеровать арабскими цифрами сквозной нумерацией, приводя эти номера после слова "Рисунок". Если
  рисунок один, то его обозначают "Рисунок 1".» · «Допускается нумеровать графический материал в пределах раздела.» ·
  «Допускается не нумеровать небольшие рисунки, размещенные непосредственно в тексте и на которые в дальнейшем нет
  ссылок.»
- 6.9.4: «Графический материал, при необходимости, может иметь наименование и пояснительные данные (подрисуночный
  текст). Слово "Рисунок" и его наименование, отделенное тире, помещают после пояснительных данных: Пример - Рисунок 1 -
  Детали прибора.» — this copy renders EVERY dash as U+002D (hyphen-minus, 9 of 9), so the dash character of the
  official text is **not settled by this copy**; the words «отделенное тире» settle that a dash is required.
- 6.9.7: «Если графический материал выполнен на нескольких листах, то на каждом листе должен быть приведен его номер с
  указанием общего числа листов … Наименование графического материала указывают только на первом листе.» — examples
  «Рисунок 20 - Схема упаковки контейнера (лист 1 из 4)» · «Рисунок 20 (лист 2 из 4)».
- 5.1.1: fonts «размером 11 - 14 пт для основного текста, а для приложений, примечаний, таблиц, сносок и примеров - на
  1 - 2 пт меньше»; 5.1.4: «Абзацы в тексте начинают отступом, равным пяти знакам используемой гарнитуры шрифта (12,5 -
  17 мм).»
- Not in the text: where the caption is aligned, spacing to the picture, a period. Both editions end the example with
  «прибора.» — whether that full stop belongs to the caption or closes the sentence of the clause is **not settled**
  (ГОСТ 7.32 and БГУИР below say «без точки» in words).
- Unverified: one blog (teletype.in, from a search result) claims a «ГОСТ Р 2.105-2026» from 2027 — not checked.

### 1.2 ГОСТ 7.32-2017 («Отчет о научно-исследовательской работе. Структура и правила оформления»)

Read in full from an official-edition PDF («Издание официальное»), https://miem.hse.ru/mirror/pubs/share/1019235132.pdf.
Front matter: «введен в действие в качестве национального стандарта Российской Федерации с 1 июля 2018 г.», «5 ВЗАМЕН
ГОСТ 7.32—2001». **Voted for by Russia, Kyrgyzstan, Kazakhstan only — Belarus is not in the list**; its status in
Belarus was not found (§6). BSUIR's СТП 01–2024 does not cite it (grep: no «7.32»).

- 6.5.1: «Иллюстрации … следует располагать в отчете непосредственно после текста отчета, где они упоминаются впервые,
  или на следующей странице (по возможности ближе к соответствующим частям текста отчета). На все иллюстрации в отчете
  должны быть даны ссылки.»
- 6.5.4: «… следует нумеровать арабскими цифрами сквозной нумерацией. Если рисунок один, то он обозначается: Рисунок
  1.» · «П р и м е р — Рисунок 1 — Схема прибора»
- 6.5.5: «Иллюстрации каждого приложения обозначают отдельной нумерацией … Рисунок А.3.»
- 6.5.6: «Допускается нумеровать иллюстрации в пределах раздела отчета. … Рисунок 2.1.»
- 6.5.7: «Иллюстрации при необходимости могут иметь наименование и пояснительные данные (подрисуночный текст). Слово
  «Рисунок», его номер и через тире наименование помещают после пояснительных данных и располагают в центре под
  рисунком без точки в конце.»
- 6.5.8: «Если наименование рисунка состоит из нескольких строк, то его следует записывать через один межстрочный
  интервал. Наименование рисунка приводят с прописной буквы без точки в конце. Перенос слов в наименовании графического
  материала не допускается.»
- 6.1.1 (the whole text): «размер шрифта — не менее 12 пт. Рекомендуемый тип шрифта для основного текста отчета —
  Times New Roman» · «Использование курсива допускается для обозначения объектов (биология, геология, медицина,
  нанотехнологии, генная инженерия и др.) и написания терминов (например, in vivo, in vitro) и иных объектов и терминов
  на латыни.» · «Абзацный отступ должен быть одинаковым по всему тексту отчета и равен 1,25 см.»
- Dash: U+2014 (em dash), 2 of 2 caption examples in the PDF text.
- Not in the text: spacing between picture and caption, a rule against splitting the picture from its caption.

### 1.3 БГУИР — СТП 01–2024 «Дипломные проекты (работы). Общие требования» (current)

Read in full (178 pages), https://www.bsuir.by/m/12_100229_1_185586.pdf. Scope, verbatim: «Требования второго и
третьего разделов распространяются на курсовые проекты (работы), типовые расчеты, рефераты и отчеты по лабораторным
работам.» · «Является обязательным для работников и студентов (курсантов) БГУИР.» — so it is the standard for both the
course and the diploma notes the owner named.

- 2.1.1: «Шрифт в названиях и тексте пояснительной записки Times New Roman 14 пунктов, межстрочный интервал – 1,0 (18
  пунктов), абзацный отступ – 1,25 см, выравнивание текста пояснительной записки – по ширине страницы.» · «В названиях
  разделов, подразделов, таблиц и рисунков не допускаются переносы в словах»
- 2.5.3: «Рисунок следует располагать после абзаца, в котором дана первая ссылка на него.» · «Иллюстрацию, помещенную в
  тексте между абзацами, располагают по центру и отделяют от текста и подрисуночной подписи одной пробельной строкой
  (приложение Н).»
- 2.5.5: «Каждый рисунок сопровождают подрисуночной подписью. Подпись должна содержать слово «Рисунок» без сокращения и
  порядковый номер иллюстрации арабскими цифрами, например, «Рисунок 7» при сквозной нумерации или «Рисунок 2.7» при
  нумерации иллюстраций по разделам пояснительной записки.» · «При необходимости иллюстрациям можно давать
  наименования, которые записывают после номера рисунка через знак тире с прописной буквы. Точки после номера и
  наименования рисунка не ставят, например: Рисунок 2.1 – Структурная схема нескорректированной системы управления» ·
  «Подпись и наименование располагают, выравнивая по центру относительно рисунка.» · «Все пояснительные данные
  помещают между рисунком и подрисуночной подписью.» · «Все подрисуночные подписи в пояснительной записке следует
  выполнять единообразно.»
- 2.5.6: «Рисунок, как правило, выполняется на одной странице. Если рисунок не помещается на одной странице, то
  допускается перенос его части на другие страницы. В этом случае в подписях ко второй, третьей и другим частям
  изображения повторяют подпись «Рисунок» и номер иллюстрации, сопровождая словами «лист 2», «лист 3» и т. д.»
- Приложение Н (обязательное), the layout of a page «с иллюстрацией, расположенной между абзацами»: paragraph →
  picture → «Пробельная строка» → «Рисунок <номер рисунка – подрисуночная подпись>» (centred) → «Пробельная строка» →
  next paragraph.
- Dash: U+2013 (en dash), 55 of 55 «Рисунок N – …» in the text.
- **Change against СТП 01-2017** (quoted in the first sweep): 2017 «Все иллюстрации должны иметь наименования» → 2024
  «При необходимости иллюстрациям можно давать наименования». The rest of the caption rule is the same.

A BSUIR department guide built on it says the no-indent part in words — Кукин Д. П. и др., «Информационные системы и
технологии (в игровой индустрии). Дипломное проектирование», БГУИР 2024, «сформулированные с опорой на стандарт
предприятия СТП 01–2024», https://www.bsuir.by/m/12_100229_1_192200.pdf, 3.8: «Иллюстрацию, помещенную в тексте между
абзацами, располагают по центру страницы без абзацного отступа и отделяют от текста и подрисуночной подписи одной
пробельной строкой.» (en dash in its examples, 6 of 6).

`[AI]` What the three agree on for an e-reader: the caption stands UNDER the picture, centred on the picture, with no
first-line indent (centring leaves no place for one — the owner's 11:13 rule), starting with a capital, with no full
stop at the end; the explanatory data stand between the picture and the label. No source says in words «the caption
must not be separated from its picture»; the closest are БГУИР 2.5.6 (a figure is, as a rule, on one page, and each
continued part carries its own «Рисунок N, лист 2» caption) and ГОСТ Р 2.105-2019 6.9.7 (each sheet carries its
number) — a caption never stands on a page without (a part of) its picture.

---

## 2. EPUB 3 / HTML5 semantics and the CSS that keeps a block whole

### 2.1 HTML Living Standard — `figure`, `figcaption`

https://html.spec.whatwg.org/multipage/grouping-content.html:

- «The figure element represents some flow content, optionally with a caption, that is self-contained (like a complete
  sentence) and is typically referenced as a single unit from the main flow of the document.»
- Content model: «Either: one figcaption element followed by flow content. Or: flow content followed by one figcaption
  element. Or: flow content.»
- «The figcaption element represents a caption or legend for the rest of the contents of the figcaption element's parent
  figure element, if any.»

### 2.2 EPUB 3.3 and EPUB 2

- EPUB 3.3 (W3C Recommendation), 6.1.2: «An XHTML content document: MUST be an [html] document that conforms to the XML
  syntax.» — so `<figure>`/`<figcaption>` are part of EPUB 3 content. https://www.w3.org/TR/epub-33/
- EPUB Reading Systems 3.3 (W3C Recommendation 17 October 2024), 6.3: «If a reading system has a viewport, it MUST
  support the visual rendering of XHTML content documents via CSS» · «MUST support the official definition of CSS as
  described in the [csssnapshot]. SHOULD support all applicable modules in [csssnapshot] that have reached at least
  Candidate Recommendation status [w3cprocess] (and are widely implemented).» https://www.w3.org/TR/epub-rs-33/
- **EPUB 2 has no `figure`:** OPS 2.0.1 builds on «XHTML 1.1 Document Type Modules and DTBook as Preferred
  Vocabularies» (https://idpf.org/epub/20/spec/OPS_2.0.1_draft.htm); the DAISY page below lists «Applies To: EPUB 3 —
  Yes, EPUB 2 — No». `[AI]` A re-typeset tool that writes `<figure>` into an EPUB 2 book must also make the book EPUB 3
  (or write a `<div>` with the same CSS).

### 2.3 Accessibility guidance — DAISY Accessible Publishing Knowledge Base, «Figures»

https://kb.daisy.org/publishing/docs/html/figures.html:

- Summary: «Ensure that figures include a caption that identifies their purpose.» Technique: «Provide a caption. [WCAG
  1.3.1 - A]»
- Example 1: `<figure><img src="images/blob.jpeg" alt="the blob" aria-describedby="img01-desc"/><figcaption>Figure 3.7 —
  The blob is digesting …</figcaption></figure>` — the label «Figure 3.7 —» lives INSIDE `figcaption`.
- «Their central characteristic, however, is that they are secondary to the primary narrative (i.e., a figure does not
  have to be immediately read in order to follow the text). If images, charts and similar content is part of the primary
  narrative, do not enclose it in figure tags.»
- «The figcaption element now allows assistive technologies to announce the caption as soon as the reader enters the
  figure.» · «Note that the figcaption element must be the very first or last in the figure.»
- «Providing a caption is not a substitute for making the content within the figure accessible.» (alt stays needed)

### 2.4 CSS: `break-inside: avoid` and `page-break-inside: avoid`

- **CSS Fragmentation Level 3** (W3C Candidate Recommendation, 4 December 2018), https://www.w3.org/TR/css-break-3/:
  - 3.2 `break-inside`: «avoid — Avoid breaks within the box.» · «avoid-page — Avoid a page break within the box.»
  - 3.4: «UAs that conform to [CSS21] must alias the page-break-before, page-break-after, and page-break-inside
    properties to break-before, break-after, and break-inside by treating the page-break-* properties as legacy
    shorthands for the break-* properties» (mapping: `auto | left | right | avoid` → the same; `always` → `page`).
  - 4.4 Rule 2: «if all of them are auto and a common ancestor of all the elements has a break-inside value of avoid,
    then breaking here is not allowed.»
  - 4.4, when that cannot be met: «If the above doesn't provide enough break points to keep content from overflowing the
    fragmentainer, then rule 3 is dropped … If that still does not lead to sufficient break points, then rules 1, 2 and 4
    are dropped in order to find additional breakpoints.» · «Finally, if there are no possible break points below the top
    of the fragmentainer, and not all the content fits, the UA may break anywhere in order to avoid losing content off the
    edge of the fragmentainer. In such cases, the UA may also fragment the contents of monolithic elements by slicing the
    element's graphical representation. However, the UA must not break at the top of the page».
  - 4.5 (recommendations): «Break as few times as possible.» · «Avoid breaking inside a replaced element.»
- **CSS 2.1 §13.3** (https://www.w3.org/TR/CSS2/page.html): «avoid — Avoid a page break before (after, inside) the
  generated box.» · «Rule B: However, if all of them are 'auto' and a common ancestor of all the elements has a
  'page-break-inside' value of 'avoid', then breaking here is not allowed.» · «If the above does not provide enough
  break points to keep content from overflowing the page boxes, then rules A, B and D are dropped».
- **Which one EPUB RS 3.3 makes a MUST:** the CSS Snapshot 2026 (W3C Group Note, 22 June 2026, https://www.w3.org/TR/css/)
  lists «CSS Fragmentation Module Level 3 … Extends and supersedes CSS2§13.3» under «2.3. Fairly Stable Modules with
  limited implementation experience» («We hope to incorporate them into the official definition of CSS in a future
  snapshot»), not in «2.1 … The Official Definition». `[AI]` So the CSS 2.1 `page-break-inside` is what an EPUB 3.3
  reading system MUST support; `break-inside` is the SHOULD. Both say «avoid», and both let the engine break when the
  block cannot fit — set both, as Standard Ebooks does (§3).

### 2.5 What reading systems do with them

| Reading system | What the source says | Source type |
|---|---|---|
| **KOReader (crengine)** | Parses both names: `lvstsheet.cpp:224` «"page-break-inside"», `:227` «"break-inside"»; implements CSS 2.1 Rule B (`lvrend.cpp:6459`: «Rule B: "However, if all of them are 'auto' and a common ancestor of all the elements has a 'page-break-inside' value of 'avoid', then breaking here is not allowed"»), with a stated gap (`lvrend.cpp:8718`: «some test suites seem to indicate that an inner "break-inside: auto" can override an outer "break-inside: avoid". We don't ensure that.»). Its default `html5.css` gives `figure` only margins (`:162` `blockquote, figure { margin-top: 1em; … margin-left: 40px; … }`) and `page-break-inside: avoid` only to h1–h6 — so a figure is kept whole only when the BOOK's CSS asks. | engine code, `koreader/crengine` master `8d29401c` (2026-11-11) |
| **Kobo** | «Page-breaking CSS is only partially supported across Kobo's reading platforms.» Table row «inside:avoid — iOS N · Android N · EPD N · KDA N» (EPD = e-ink devices). Sideloaded `.epub` «will render using the Adobe Digital Editions WebKit»; `.kepub.epub` triggers «the Kobo WebKit». | vendor spec, `kobolabs/epub-spec` README, last commit 2026-07-30 |
| **Kindle** | KDP «Text Guidelines - Reflowable»: «Kindle now supports CSS attributes for page-break-inside:avoid and break-inside:avoid.» · «This allows publishers to group elements together so they do not break across pages.» · «Use cases include images with captions and headlines with paragraphs you want to keep together in your design.» https://kdp.amazon.com/en_US/help/topic/GH4DRT75GWWAGBTU — older third-party pages say the opposite (Jutoh KB0124, first sweep); the vendor page is newer and undated. | vendor guideline |
| **Readium** | «From experience, avoiding a `break-inside` elements flowing in 2 or 3 columns can also be problematic (the element vertical alignment is completely off).» · «CSS multicol relies on a complex (fragmentation) logic, and this logic varies for each browser.» — Readium paginates with CSS columns, so the result is the browser engine's. https://github.com/readium/readium-css/blob/master/docs/CSS04-multicolumn_layout.md (last commit 2025-08-29) | reading-system docs |
| **Adobe RMSDK / ADE** | No Adobe document found. A 2010 MobileRead post (search result, not opened): «ADE, at least, recognises this code and handles it correctly». | forum, unverified |
| **Apple Books** | No Apple statement on `break-inside` found. The Asset Guide (search summary only) says page breaks are supported in flowing books and recommends `page-break-after` at chapter ends; 2010–2011 blogs report `page-break-inside: avoid` working in iBooks. | NOT SETTLED |

### 2.6 A figure taller than a page

- The specs: when the avoid cannot be honoured, the rules are dropped and the box breaks; the UA «may also fragment the
  contents of monolithic elements by slicing» (css-break-3 §4.4, above). So by the spec the caption goes to the next
  page — exactly the owner's symptom when the picture is large.
- crengine caps an in-flow image at the page: `lvtextfm.cpp` (~1090): «We have to limit the image height so that the
  line that contains it does fit in the page without any uneeded page break» (`m_max_img_height =
  m_pbuffer->page_height`, minus the parents' margins), and ~2463 «Ensure they are constrained to this paragraph width
  and page height». `[AI]` A picture as tall as the page plus a caption is taller than a page → the avoid is dropped and
  the caption lands on the next page; crengine does not shrink the picture to make room for its caption.
- Third-party reports of the same (not primary): a tall image «forcing the caption onto the next page» (Adobe community
  thread, first sweep; MobileRead, search result).
- This firmware today (first sweep, code re-read 2026-11-13): a picture that does not fit the rest of the page moves
  whole to the next page and is never shrunk; `page-break-*: avoid` is not honoured.
- `[AI]` No engine found shrinks a picture so that its caption fits; the one practice that guarantees it is in the
  book's CSS — Standard Ebooks' `figure img { max-height: 100vh }` (§3) only keeps the picture within ONE screen, not the
  picture plus its caption. The owner's direction (2026-11-13 10:39 +03:00, `ideas/03`: «возможно это потребует
  уменьшения размера миниатюры картинки - но это и не важно») goes beyond the industry here.

---

## 3. Typesetting practice

- **Standard Ebooks Manual of Style 1.9.1** (`/manual/latest` redirects there), §7.8.5:
  https://standardebooks.org/manual/1.9.1/7-high-level-structural-patterns
  - «<img> elements that are meant to be aligned on the block level or displayed as full-page images are contained in a
    parent <figure> element, with an optional <figcaption> sibling.»
  - 7.8.5.1: «An optional <figcaption> element containing a concise context-dependent caption may follow the <img>
    element within a <figure> element. This caption depends on the surrounding context, and is not necessarily (or even
    ideally) identical to the <img> element's alt attribute.»
  - 7.8.5.2 «All <figure> elements have this CSS:»
    ```css
    figure{ break-inside: avoid; margin: 1em 2.5em; }
    figure img{ display: block; margin: auto; max-height: 100vh; max-width: 100%; }
    figcaption{ font-size: smaller; font-style: italic; margin: 1em; text-align: center; }
    figcaption p + p{ text-indent: 0; }
    ```
  - 7.8.5.3 full-page figures: `figure.full-page{ break-after: page; break-before: page; }`
  - 7.8.1.1: ids `illustration-N` through the whole book.
  - Their build adds the legacy names (`standardebooks/tools`, `se/se_epub_build.py`): «`page-break-*` is deprecated in
    favor of `break-*`. Add `page-break-*` aliases for compatibility in older ereaders.» — the built test output
    (`tests/build/epub/golden/…/core.css`) carries `page-break-inside: avoid`.
- **Kindle (KDP «Image Guidelines - Reflowable»)**, https://kdp.amazon.com/en_US/help/topic/G75V4YX5X8GRGXWV: «Please use
  figure blocks for images with captions and ensure that you do not raster the caption with the image.» · «It is best to
  have caption in text and not image format.» · «Figure caption, table, and title image should be in HTML.» — plus the
  `break-inside` sentence of §2.5.
- **DAISY KB** (§2.3): the numbered label inside `figcaption`, `alt` kept, caption first or last child.
- **Ace by DAISY:** no figure/caption rule looked up — not researched.

---

## 4. The table — rule → ГОСТ 2.105 → ГОСТ 7.32 → БГУИР → EPUB practice

| Rule | ГОСТ 2.105 (‑95 / Р ‑2019) | ГОСТ 7.32-2017 | БГУИР СТП 01–2024 | EPUB practice |
|---|---|---|---|---|
| Caption position | after the explanatory data (4.3.1 / 6.9.4); «под рисунком» not said in words | «в центре под рисунком» (6.5.7) | under the picture, after the explanatory data (2.5.5, прил. Н) | `figcaption` first or last child (HTML); SE: after `img` |
| Label word | «Рисунок» (example) | «Рисунок» (6.5.4) | «Рисунок» «без сокращения» (2.5.5) | any; DAISY «Figure 3.7 —» inside `figcaption` |
| Wording | «Рисунок 1 — Детали прибора» | «Рисунок 1 — Схема прибора» | «Рисунок 2.1 – Структурная схема …» | — |
| Dash between number and name | required («отделенное тире», 6.9.4); character: U+2014 in the ‑95 transcription, not settled for ‑2019 | U+2014 em dash | U+2013 en dash («знак тире») | — |
| Name | optional («при необходимости») | optional («при необходимости») | optional since 2024 (2017: mandatory) | SE: optional, «concise context-dependent» |
| Capital letter | not stated | «с прописной буквы» (6.5.8) | «с прописной буквы» (2.5.5) | — |
| Full stop at the end | example ends «прибора.» — not settled | «без точки в конце» (6.5.7, 6.5.8) | «Точки после номера и наименования рисунка не ставят» | — |
| Alignment | not stated in the text read | centre (6.5.7) | «по центру относительно рисунка» (2.5.5) | SE `text-align: center` |
| First-line indent | not stated (5.1.4 indent = text paragraphs) | not stated (6.1.1 indent = text) | none: centred; guide 3.8 «без абзацного отступа» (picture) | SE caption: none (`text-indent: 0` for 2nd p) |
| Font / style | Р‑2019: 11–14 pt main text, notes 1–2 pt smaller | ≥ 12 pt, Times New Roman; italic only for objects/Latin terms | Times New Roman 14 pt «в названиях и тексте» | SE: `font-size: smaller; font-style: italic` |
| Multi-line caption | not stated | single spacing, no hyphenation (6.5.8) | no hyphenation in figure names (2.1.1) | — |
| Spacing | not stated | not stated | one blank line picture↔text and picture↔caption (2.5.3, прил. Н) | SE: `figure` margin 1em 2.5em, `figcaption` margin 1em |
| Numbering | through the document; per section allowed; small unreferenced pictures may stay unnumbered | through; per section allowed; «Рисунок А.3» in appendices | «Рисунок 7» through or «Рисунок 2.7» per section; «Рисунок А.2» | SE ids `illustration-N` |
| Picture placement | near the text / after the first reference (Р‑2019 6.9.1) | after the first mention «или на следующей странице» (6.5.1) | after the paragraph with the first reference (2.5.3) | in flow, at the reference |
| Picture and caption on one page | not stated; multi-sheet: number on every sheet, name on the first (Р‑2019 6.9.7) | not stated | «как правило, … на одной странице»; continued parts repeat «Рисунок N … лист 2» (2.5.6) | `break-inside: avoid` + `page-break-inside: avoid` on `figure` (SE, KDP); engines drop it when the figure is taller than a page (css-break-3 §4.4) |

---

## 5. What the sources do NOT settle — for the owner

1. **The label text of the books.** The three standards govern reports, design documents and theses, not trade books;
   the owner's books say «Рис. 2. …». Whether the re-typeset tool rewrites the author's label («Рис. 2.» → «Рисунок 2 –»)
   or only changes the layout is his decision (the first sweep's default `[AI]`: keep the wording). Book-publishing
   references (e.g. Мильчин's «Справочник издателя и автора») were not read.
2. **Which dash, if the label is rewritten:** en dash (БГУИР, U+2013) or em dash (ГОСТ 7.32, U+2014).
3. **Italic and size of the caption.** The books wrap the caption in `<em>`; Standard Ebooks ships italic + smaller;
   ГОСТ 7.32 limits italic to objects and Latin terms; БГУИР gives captions the text font (14 pt, upright by default).
   Perception — the owner's taste (mock-up class).
4. **Picture + caption taller than a page.** The specs break, crengine breaks, no engine shrinks; the owner already said
   a smaller in-page picture is fine (10:39). Open: is there a smallest size below which the caption may go to the next
   page after all (the БГУИР «как правило»)?
5. **EPUB 2 books.** `<figure>` does not exist in EPUB 2 (XHTML 1.1). The package version of the owner's 10 books was
   not checked (it is not in the census). Check before the tool: `unzip -p <book>.epub '*.opf' | grep -o 'version="[^"]*"' | head -1`.
   Then: upgrade the book to EPUB 3, or write `<div class="figure">` with the same CSS.
6. **Firmware scope.** The specs attach the avoid to ANY block (`break-inside` on a `div`, a table, a heading pair), not
   only to `figure`; whether the firmware honours the property generally or keys on `<figure>` is a design fork for the
   plan (price: books from other producers that wrap captions in a `div` with `page-break-inside: avoid`).
7. **Status gaps:** ГОСТ 7.32-2017 in Belarus (Belarus did not vote for it; not found) · the claimed «ГОСТ Р 2.105-2026»
   (unverified) · Apple Books' behaviour (no Apple source).

---

## 6. What could not be found or opened

- ГОСТ Р 2.105-2019 official PDF: guap.ru and files.stroyinf.ru refused the TLS handshake (`curl: (35) schannel`) and
  WebFetch («Socket is closed»); the lib.uni-dubna.ru PDF is a scan with no text layer. The text above is from the
  meganorm.ru database copy, whose dashes are all hyphen-minus; the printed layout (centring of the example) was not seen.
- fmp.msu.ru (a ГОСТ Р 2.105-2019 copy named by a search): TLS handshake failed.
- ГОСТ 2.105-95: read from the Wikisource transcription only; its printed figure-caption layout not seen.
- Belarusian status of ГОСТ 7.32-2017 (or -2001): not found; the BSUIR standard does not cite either.
- Adobe RMSDK: no official document; Apple Books: no Apple statement on `break-inside`; Ace by DAISY: not looked up.
- Quotes of §1–§3 were copied from downloaded files, except the two KDP pages, which were read through WebFetch only
  (verbatim quotes returned by it, not re-checked against the raw page).
