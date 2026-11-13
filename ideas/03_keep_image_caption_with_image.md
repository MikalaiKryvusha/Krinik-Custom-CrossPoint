# Idea 03 — never split an image from its caption across pages

> **Created:** 2026-11-13 (the owner's request, chat — tossed mid-task while idea 02 was in recon) · **Parent:** — ·
> **Status:** 🔬 recon done, direction set by the owner 2026-11-13 10:53 +03:00 (re-typeset to the standard + the
> firmware honours `<figure>`); plan next, after idea 02 · **Outbound:** the firmware half is an upstream PR candidate
> (standard HTML5 semantics)

`[OWNER] 2026-11-13 10:38 +03:00 · chat:`

> и было бы хорошо, чтобы программа читалки НЕ отрывала подписи изображения от изображения.
>
> Сейчас часто вижу, я читаю в лендскейпе 180, что картинка на одной странице, а подпись этой картинки - на следующей странице - это неправильно

`[OWNER] 2026-11-13 10:38 +03:00 · chat:`

> всегда нужно держать подпись рядом с картинкой

`[OWNER] 2026-11-13 10:39 +03:00 · chat:`

> возможно это потребует уменьшения размера миниатюры картинки - но это и не важно, так как мы сделаем возможность октрывать картинки на Full Screen для подробного рассмотрения

`[OWNER] 2026-11-13 10:49 +03:00 · chat` (after «требует правки движка раскладки»):

> и требует правки движка раскладки.
>
> может проще книги переверсать?

`[OWNER] 2026-11-13 10:50 +03:00 · chat:`

> или это баг движка?

`[OWNER] 2026-11-13 13:51 +03:00 · chat` (his debug9 check on the reader, homework 04):

> но подписи картинок  в дебаг9 всё ещё открываются от картинок

`[AI]` read as «отрываются» (a caption on another page than its picture). Expected: debug9 carries idea 02 only; this
idea has no code yet. The owner's observation confirms the defect is live on the reader with the debug9 build.

## Recon (2026-11-13, code `wip/krinik-debug8` + the sample book; a subagent's report, the key points re-read by the agent)

- **Not a bug — a missing rule.** The sample book (Hofstadter, «Гёдель, Эшер, Бах») marks a caption as a plain body
  paragraph right after the picture: `<div class="image"><img class="z1" …/></div><p class="p1"><em>Рис. 2. …</em></p>`
  (`OPS/ch1-6.xhtml:12-13`); `.image` has no `page-break-after: avoid` (`OPS/style.css:66-73`). 179 `<img>` in the
  chapters, 149 followed by an `<em>Ри…` caption paragraph, ~30 by body text. Upstream `develop` lays out the same way.
- **What the engine does** (`lib/Epub/Epub/parsers/ChapterHtmlSlimParser.cpp`): a picture that does not fit the rest
  of the page moves WHOLE to the next page (`:1901-1913`, re-read), never shrinks to the rest; a heading right above it
  moves with it (`:1905-1911`). Keep-with-next exists for h1–h6 only; `page-break-*: avoid` is not honoured at all;
  `max-width` is not parsed. The caption's first line can never pull the picture along (`canCarry` moves text lines only).
- **Re-typesetting the books** helps only by burning the caption INTO the picture (the one way two blocks cannot split
  today) — then the caption shrinks with the picture in landscape, is not searchable, and every book needs the tool.
- **The engine fix** (recommended `[AI]`): when the first line after a picture does not fit, the picture moves to the
  next page with it; when the two do not fit one page, the picture shrinks. Open owner question: what counts as the
  caption (any paragraph right after a picture, or only a «Рис. N…» one) — goes to `interviews/`.

`[OWNER] 2026-11-13 10:53 +03:00 · chat:`

> Что считать подписью
>
> В EPUB нет договорённого атрибута на подписи картинок?

> ну так вот я и говорю, что нужно бля книги корректно переверстать.

`[OWNER] 2026-11-13 11:13 +03:00 · chat` (seeing the simulator page of the test book, caption with a first-line indent):

> подписи картинок - это не параграф, они не обязаны слушаться правила отступа для красной строки параграфа

> читай ГОСТЫ

> особенно кост оформления пояснительных записок БГУИР, курсовых и дипломных работ

## The direction (the owner's word above; the split into two parts is `[AI]`, said to him in chat 10:54)

**The standard caption:** EPUB 3 content is XHTML5 — a picture with its caption is `<figure><img/><figcaption>…`
`</figcaption></figure>`, and CSS `break-inside: avoid` (old name `page-break-inside: avoid`) asks a reader not to split
the block. None of the owner's books uses it.

**Census of the owner's card** (2026-11-13 10:53 +03:00, `G:\Книги`, 10 EPUB, script
`tools/caption_census.py`):

| Book | `<img>` | `<figure>` | `<figcaption>` | «Рис…» paragraph right after a picture |
|---|---|---|---|---|
| Хофштадтер, «Гёдель, Эшер, Бах» | 180 | 0 | 0 | 148 |
| Тегмарк, «Наша математическая вселенная» | 117 | 0 | 0 | 98 |
| Шопенгауэр, «Мир как воля и представление…» | 97 | 0 | 0 | 0 |
| Дойч, «Начало бесконечности» | 51 | 0 | 0 | 0 |
| Дойч, «Структура реальности» | 34 | 0 | 0 | 0 |
| Шекспир, «Трагедии. Сонеты» | 12 | 0 | 0 | 0 |
| Докинз, «Эгоистичный ген» | 9 | 0 | 0 | 0 |
| Шопенгауэр, «О четверояком корне…» | 6 | 0 | 0 | 0 |
| Лю Цысинь; Лем | 1 each (cover) | 0 | 0 | 0 |

**Two parts:**
1. **Re-typeset tool** (`tools/`, runs on the PC): picture + the «Рис. N…» paragraph right after it →
   `<figure>…<figcaption>…</figcaption></figure>` with `break-inside: avoid`. What counts as a caption lives HERE, per
   book, not in the firmware. Books without such paragraphs (Дойч, Докинз…) are checked by eye for other caption forms.
2. **Firmware:** a `<figure>` is laid out on ONE page — picture and `<figcaption>` together; when they do not fit one
   page, the picture inside shrinks (the owner: a smaller in-page picture is fine, the full-screen view of idea 02 shows
   the detail). Today `figure` is a plain block and `figcaption` is unknown, so the tool alone changes nothing on the reader.
