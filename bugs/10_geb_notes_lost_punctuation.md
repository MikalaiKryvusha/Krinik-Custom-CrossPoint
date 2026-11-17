# Bug 10 — «Гёдель, Эшер, Бах» on the owner's reader lost punctuation in its notes, and our book checks did not see it

**Status:** 🔴 OPEN · **Severity:** S2
**Version/build:** the book file on the owner's card, `/Книги/Дуглас Хофштадтер. Гёдель, Эшер, Бах. Эта бесконечная
гирлянда.epub` (4 340 647 B, SHA256 `1fa7c1ca…`, copied 2026-11-17 19:47 +03:00 to `.tmp/bug09/geb.epub`, never committed —
a third-party book) · **When/context:** the owner's «Дополнение 2» to bug 09, 2026-11-17 · **Fixing:** after bug 09 and
the 1.1.3-debug4 image

## The owner's words (verbatim, `bugs/09_ssylka.md`, commit `6cc642b`)

> Дополнение 2: в это йже книге много предложений не закрыты точкой! Это проблема наших инструментов по проверке книг на
> адекватность!

## Goal vector (Avoid) and acceptance

A book that lost its punctuation never reaches the reader unnoticed. Done when:
- our book check (`tools/epub_lint.mjs` or a sibling) reports the GEB notes as damaged — Check: the command on
  `.tmp/bug09/geb.epub` exits non-zero and names `ch3.xhtml`;
- the owner's GEB on the card reads with its punctuation, from a clean source or a repaired copy — the owner's word.

## Symptom (measured 2026-11-17 19:59 +03:00 on the copy)

The notes chapter `OPS/ch3.xhtml` (91 notes) lost commas, colons, full stops, dashes and opening brackets:

| Note | On the card | What the punctuation says it was |
|---|---|---|
| [1] | `H. D. David and A Mendel «The Bach Reader» стр. 305 6` | `… «The Bach Reader», стр. 305–6.` |
| [4] | `Charles Babbage «Passages from the Life of a Philosopher» стр 145 6` | `…, стр. 145–6.` |
| [8] | `… в журнале «Mind» n s 4 1895) стр. 255 6` | `… «Mind», n.s. 4 (1895), стр. 255–6.` |
| [12] | `Leonard В. Meyer «Music The Arts and Ideas» стр. 87 8` | `… «Music, the Arts, and Ideas», стр. 87–8.` |
| [15] | `(Princeton N J Princeton University Press 1975)` | `(Princeton, N.J.: Princeton University Press, 1975)` |

The right column is `[AI]` inference from the remains (an unclosed `)`, page pairs `305 6`), not a source — the original
text is not in hand. The main text keeps its commas on a sample; paragraphs ending without `.!?…:;»)` — 339 of 5 711
(≥ 40 chars), many of them verse lines and headings — not yet sorted into damage and normal.

## Hypotheses

1. The book came this way (a converter dropped punctuation in the notes) — our checks never compare against meaning,
   only structure (`epub_lint.mjs`: links, manifest, well-formedness).
2. One of our repair tools dropped the characters (`bracket_footnotes.mjs` rewrote these note markers into «[N]»; the
   class `krinik-fn` on every note link is ours) — `tools/text_same.mjs <orig> <fixed>` would show it, given the
   original file.

## Next steps

- [ ] Find the original file of the book (the source the owner downloaded) — needed for hypothesis 2.
- [ ] A punctuation check for books: notes without a final stop, page pairs `стр. N N`, an unmatched `)` — red on this
      copy, green on a clean book (the test book `qa_runs/sd_book_images/image_test.epub`).

## Decisions made without the owner

- `[AI]` Split from bug 09 (one document per defect).

## Links

`bugs/09_ssylka.md` · `tools/epub_lint.mjs` · `tools/text_same.mjs` · `tools/bracket_footnotes.mjs`
