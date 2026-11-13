# Idea 03 — never split an image from its caption across pages

> **Created:** 2026-11-13 (the owner's request, chat — tossed mid-task while idea 02 was in recon) · **Parent:** — ·
> **Status:** 🆕 the owner's original, verbatim · **Outbound:** —

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
