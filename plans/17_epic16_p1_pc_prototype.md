# Plan 17 — epic 16, phase 1: the PC FB2 → EPUB 3 converter in Krinik EPUB Linter

> **Created:** 2026-11-18 · **Parent:** `plans/16_EPIC_fb2_converter.md` → «Ф1 — прототип на ПК» (criteria 1–3) ·
> **Status:** 📐 planned 2026-11-18 09:52 +03:00 · **Outbound:** the linter's own repo (`MikalaiKryvusha/Krinik-EPUB-Linter`), pushed with
> its README after the owner's proofreading

## Goal vector (Achieve)

The owner gets EPUB 3 from an FB2 on the PC in one command, already carrying the linter's rules (a caption bound to its
picture, `[N]` notes with a link back, headings kept with their text), and every defect of the source FB2 handled and
reported — then read in the simulator on his settings (`[OWNER]` 2026-11-18 09:46 «когда конвертер на ПК будет работать -
тестируем его на симуляторе»).

Anchor (meta-plan, Ф1): «Команда `fb2` в Krinik EPUB Linter: FB2 и FB2.zip → EPUB 3 (оглавление `nav` и NCX), гибрид
открытых наработок с правилами линтера, своя обработка ошибок, отчёт.» Gate: «критерии 1–3; тесты и мутанты; судья без
блокеров».

## Acceptance criteria (phase)

1. **The owner's test book converts.** `krinik-epub-linter fb2 D:/Hofshtadter_…9y7ehg.198312.fb2.zip -o .tmp/fb2_out`
   writes one EPUB 3 whose `check` is clean, with 180 images, 91 notes each linked both ways, 153 captions bound, 0
   broken internal links, every XHTML well-formed, mimetype first and stored. Check: the linter's `check` + a count script
   + `.tmp/xml_ok.py`-style well-formedness, all printed in the run report.
2. **The text is complete.** Every paragraph text of the FB2's main body appears in the EPUB in order (whitespace and the
   linter's `[N]` labels aside). Check: a text-sameness script (FB2 paragraphs vs EPUB paragraphs) prints 0 missing.
3. **Negative set.** Each synthetic broken FB2 (windows-1251 declared · no declaration in cp1251 · koi8-r · an unclosed
   tag · a stray `&` · a note link to a missing id · an image to a missing binary · bad base64 · an empty section ·
   duplicate ids · an unknown element · a zip with no `.fb2` · an empty file) gives a readable EPUB or a named refusal,
   and the report names each handled defect with its place. Check: `pytest tests/test_fb2.py`; each handler's test red on
   a mutant.
4. **The simulator reads it.** The converted GEB on the owner's-settings card (`HOUSE_RULES.md` П4, `tools/sim_pages.sh`):
   a chapter with pictures (captions under their pictures), a note tap → the note → back. Check: shots read, the log
   without new `[ERR]` lines against the library EPUB's run.
5. **Idempotent and safe.** The FB2 is never changed; a second run writes the same EPUB bytes (fixed timestamps).
   Check: SHA-256 of input before/after; two runs diffed.

## Design (to be confirmed by the recon step)

- **Where:** `epub-linter/krinik_fb2.py`, command `fb2 BOOK.fb2[.zip] … -o DIR` in `krinik_epub_linter.py`. Python stdlib.
- **Hybrid, without a second copy of the rules:** the converter writes a «classic» FB2 → EPUB layout (the markup the
  common converters and the library's own `.fb2.epub` produce: notes as a notes body with numbered titles, pictures in a
  `div.image`, captions as the paragraph after) and then runs the linter's own pipeline on the in-memory book —
  `fix_book` (notes → `[N]` with backlinks) and `krinik_figures.bind_book` (captions). The linter's rules stay in one
  place.
- **Mapping sources (MIT/BSD only, code may be ported with notice):** `KiberBomzh/fb2epub` (Rust, EPUB 3.3,
  `html_builder.rs`), `johnfactotum/foliate-js` `fb2.js` (12 KB element mapping), `alpzoloto-sudo/inkmod` `lib/Fb2`
  (notes on these readers), the FictionBook 2.0 XSD (`gribuser/fb2`, BSD-2). GPL projects (fb2cng, calibre, pandoc) are
  behaviour references only — their output may be compared, their code is not copied.
- **Error handling (custom, each a named class with a report line):** E1 encoding (declared / sniffed: UTF-8 BOM, the
  XML declaration, else UTF-8 then cp1251 fallback) · E2 malformed XML (strict parse first; on failure a lenient
  tokenizer that auto-closes, reports the line) · E3 note link without a target (link dropped, text kept) · E4 image
  without a binary (alt text placeholder) · E5 bad base64 (binary skipped) · E6 empty section/body (skipped) · E7 duplicate
  ids (renamed) · E8 unknown elements (text kept, tag dropped, counted).
- **Output:** EPUB 3 `version="3.0"`, `dcterms:modified` from the FB2's `document-info/date` (deterministic), `nav.xhtml`
  + `toc.ncx`, one XHTML per top-level section (large ones split), images under `images/` with their FB2 ids, the cover
  from `coverpage`, headings as `h1`–`h3` by depth plus the KCCP CSS (`page-break-after: avoid`), file name
  `Author. Title.epub` as `fix` names it.

## Steps

- [ ] P1.1 Recon of the MIT mapping sources (fb2epub `html_builder.rs`, foliate-js `fb2.js`, the XSD) and the library's
      `.fb2.epub` of the test book (its markup = the «classic» layout the linter already understands); findings appended
      to `researches/2026-11-18_fb2_to_epub3_converters.md` → «Mapping». Anchor: «гибрид открытых наработок».
- [ ] P1.2 Case set `testcases/TC_epic16_p1_fb2.md` (criteria 1–5, the negative set listed, the control: the library's
      `.fb2.epub` through `check`). Anchor: «своя обработка ошибок, отчёт».
- [ ] P1.3 `krinik_fb2.py` — parse (E1, E2), model, XHTML/OPF/nav/NCX writer, images, notes body; `tests/test_fb2.py`
      with synthetic FB2s (positive + the negative set), each handler proven red on a mutant.
- [ ] P1.4 The pipeline: the in-memory book through `fix_book` + `bind_book`; the `fb2` command, its report (`.md`).
- [ ] P1.5 The owner's book: run, counts, text sameness, `check`, idempotence; compare with the library's `.fb2.epub`
      (notes, images, chapters).
- [ ] P1.6 The simulator (criterion 4) on the П4 card; run report `testcases/reports/<date>_epic16_p1.md`.
- [ ] P1.7 The judge (fresh agent: the diff + the meta-plan criteria); fixes; commit in the linter; Ф2 operational plan.

## Risks

1. The lenient XML path hides real defects → every repair is a report line with the place; a test per repair.
2. The «classic» layout must match what `fix_book` recognises → P1.1 reads the library EPUB's notes markup first; a test
   runs `fix_book` on the converter's raw output.
3. Large books in memory on the PC are fine (7.9 MB); the firmware port (Ф2) must stream — the PC design keeps the
   two-pass order (index, then write) so Ф2 can mirror it.

## Decisions made without the owner

(filled at the phase's close)
