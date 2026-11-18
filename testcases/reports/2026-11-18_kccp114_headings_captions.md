# Test run report — KCCP 1.1.4: bug 14 (a lonely heading), bug 15 (a heading's first-line indent), the captions in Krinik EPUB Linter

**Created:** 2026-11-18 09:31 +03:00 · **Run by:** the agent (Claude Opus 5.5) · **Version/build:** firmware `wip/kccp-1.1.4` (from the
1.1.3 release `c1c38089`, uncommitted at the runs, committed after them); Krinik EPUB Linter `epub-linter/` `8ef77a9` (+
the linear blank-text fix in the same commit)

## 1. Work

The owner's word 2026-11-18 08:44 «давай скорее делать 1.1.4 … ужас с этими заголовками, и переносами подписей картинок на
следующие страницы»: `bugs/14_lonely_heading.md`, `bugs/15_heading_first_line_indent.md` (their fix plans and FORK lines)
and the caption binder of `plans/14_epic07_p3_retypeset_tool.md`, moved into the linter on his word 08:49. Basis: his
words in the two bugs (headings never alone at a page bottom; no first-line indent on a heading) and epic 07 («подпись
ВСЕГДА рядом с картинкой», no indent, centred). Stand rule: `HOUSE_RULES.md` П4 (his settings, his GEB copy).

## 2. Contour

Windows simulator `simulator_x4_pro_win` (rebuilt 2026-11-18 ≈ 09:22 +03:00 from the working tree; «before» = the binary
of 2026-11-17 21:55, the 1.1.3 layout code). Card `.tmp/b14_sd`: the owner's `settings.json` from his card (orientation 3
= landscape 180°, Literata 16 from `/.fonts/Literata/*.ttf`, paragraph indent 5 spaces, alignment «as in the book»,
embedded style on), his GEB copy `.tmp/bug09/geb.epub` (EPUB 2.0, md5 `0e91a974…`) at `/geb.epub`, `progress.bin` set
per run. GEB never enters the repository: the runs' folders move to `.tmp/b14_runs/` after the report. Fidelity: page 1 of
«ГЛАВА I» (spine 9) is line for line the owner's screenshot `ch10_p1`; from page ~19 the simulator runs one line (one
page) ahead of his reader. The device is not involved — not verified on the reader.

## 3. Runs

| # | Moment | Command | Exit / outcome |
|---|---|---|---|
| 1 | 2026-11-18 09:03–09:04 +03:00 (log mtimes) | «before» binary: `sh .tmp/b14_runs.sh b14_before` (pages 1, 20, 28), `PAGES="19 27" sh .tmp/b14_runs.sh b14_before` — each `SD_TEMPLATE=../.tmp/b14_sd SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh <run> '0:WAIT:Entering activity: EpubReader;9000:SHOT:page;10000:QUIT' ''` | bug 15 seen on page 1, bug 14 on page 27 |
| 2 | 2026-11-18 08:58 +03:00 (≈, until 09:01) | host tests of the two touched programs; four mutants (`.tmp/mutants.sh`) | all new tests green; each mutant red |
| 3 | 2026-11-18 08:57 +03:00 (≈, the report at 09:08) | the judge (fresh agent, read-only) over the firmware diff | VERIFIED WITH CAVEATS; the major (keep inherited by every block of any `break-after: avoid` wrapper) fixed: only a wrapper with `break-inside: avoid` too reaches inside |
| 4 | 2026-11-18 09:12 +03:00 (≈) | `TARGETS="ChapterHtmlSlimParserTest CssParserTest" sh tools/host_tests.sh` (after the fix of run 3), the fifth mutant | 172/175 + 31/32, the failures = the known list; the mutant red |
| 5 | 2026-11-18 09:22 +03:00 (≈) | `pio run -d firmware -e simulator_x4_pro_win` | SUCCESS |
| 6 | 2026-11-18 09:24 +03:00 (log mtimes) | `PAGES="1 19 20 27 28" sh .tmp/b14_runs.sh b14_after` | see Checks |
| 7 | 2026-11-18 09:15 +03:00 (≈, until 09:20) | linter: `pytest -q` (157), five + one mutants, `ruff check`; on a copy of GEB `survey`, `check`, `fix -o .tmp/kel_out`, `check` again; `.tmp/kel_list.py` (every caption listed); `.tmp/xml_ok.py` (well-formed XML, mimetype) | see Checks |
| 8 | 2026-11-18 09:27–09:29 +03:00 (log mtimes) | `CROSSPOINT_SIM_SCREEN_TEXT=1 sh .tmp/b14_pages.sh cap_orig <GEB> 7 116 UP`, the same `cap_kel` on the linter's output (stopped at page 41 by `SIM_TIMEOUT` 90 s) | see Checks |
| 9 | 2026-11-18 09:33–09:35 +03:00 (log mtimes) | `CROSSPOINT_SIM_SCREEN_TEXT=1 SIM_TIMEOUT=400 START=40 sh .tmp/b14_pages.sh cap_orig2 <GEB> 7 76 UP`, the same `cap_kel2` on the linter's output — pages 41–115 of spine 7 | see Checks |
| 10 | 2026-11-18 09:35 +03:00 (ctest log mtime) | `sh tools/host_tests.sh` | 978 tests, 10 failed = the known list, «no new failure» |
| 11 | 2026-11-18 09:38–09:44 +03:00 (log and build-log mtimes) | at `21671e33` (version 1.1.4-debug1): `pio run … simulator_x4_pro_win`; `sim_run.sh d114_1_smoke_home` (Home → the shade by its swipe → Back); `PAGES="1 27 28" sh .tmp/b14_runs.sh d114_1_smoke_geb`; `pio run -d firmware -e x4pro-krinik-debug` | SUCCESS ×2; Home 0 `[ERR]`, the shade with its four default buttons, GEB 10 `[ERR]` (the simulator's TTF autohint lines, as before the change); RAM 34.3 %, Flash 83.0 % |

## 4. Checks

- Hygiene: host programs of the parser and CSS — every new test green, each of five mutants red (no CSS `avoid`, no
  inheritance, no indent rule, a keep leaking past the wrapper, a keep from a `break-after`-only wrapper); the linter —
  157 tests, six mutants red, ruff clean; `stamp_guard` on each commit.
- Functional run: the owner's GEB on his settings opened in the simulator at the pages of his screenshots, each page's
  shot READ; the linter run on his GEB copy, its 151 captions READ (151 of 153 — corrected below after the judge;
  with linter `6343dcc` 153 of 153).

| Case | Before (1.1.3 code) | After |
|---|---|---|
| Bug 15 — «ГЛАВА I: Головоломка MU» (page 1, his `ch10_p1`) | first line indented, «MU» alone on the second line from the left edge | **pass** — no indent; the title fits one line |
| Bug 14 — «Прыжки за пределы системы» (page 27 here = his page 28) | the heading is the last line of page 27, its text on page 28 | **pass** — page 27 ends with text; the heading opens page 28 with its text |
| Bug 14 — «Внутри и снаружи системы» (his page 20) | on this stand the heading already opened page 20 (one line of offset) | **pass** — still at the top with its text |
| Linter on GEB — `survey` / `check` | 151 captions as plain paragraphs after a picture; `check` exit 1 naming them | **partial** at `8ef77a9` (corrected 2026-11-18 10:14 +03:00 after the judge: the book has 153 captions right after a picture; «Рис. I.» in a bare `<span>` and the typo «Ри. 27.» stayed unbound while `check` read clean — the detector judged its own misses; the second picture of figure 43 only) → **pass** at `6343dcc`: 153 in 44 files, both pictures of figure 43 in one block, `check` clean, 68 XML well-formed, the input unchanged. At `8ef77a9`: `fix` bound 151 in 43 files (148 «Рис.» + 3 «РИС.» — the census's 148 counted only «Рис»), EPUB 2 `<div>` form, the CSS rule once; `check` clean; 68 XML files well-formed; mimetype first and stored; the input's SHA256 unchanged |
| Caption look — «Рис. 2. Адольф фон Мензель…» (spine 7, page 16) | justified, first-line indent | **pass** — centred, no indent, under the picture |
| Caption keep — «Рис. 5. М. К. Эшер. «Водопад»» (spine 7, page 55) | the picture alone on page 55, its caption opens page 56 — the owner's complaint seen | **pass** — the picture shrunk 406 → 392 px, the caption centred under it on page 55 (log `Figure picture shrunk 406 -> 392 px for its caption`) |
| Caption keep — «Рис. 7. … «Рука с зеркальным шаром»» (page 59) | the picture alone on page 59, its caption at the top of page 60 | **pass** — shrunk 447 → 395 px, the caption under it on page 59 |
| Control — the original GEB on the new firmware | — | the same two splits (the firmware alone does not bind a plain «Рис.» paragraph; the binding is the book's, by the linter — the owner's word 08:49) |
| Smoke at `21671e33` (debug1) | — | **pass** — Home, the shade, GEB pages 1 / 27 / 28 as in run 6 |

## 5. Found

- Krinik EPUB Linter: the blank-text regex of the caption binder (inherited from `tools/figure_retypeset.py`) backtracked
  exponentially on runs of no-break spaces — `survey` on GEB did not finish in 5 min. Fixed, guarded (EXP-0038).
- A hand-typed test environment sent four test files to `F:\Temp` (EXP-0037) — removed; `TARGETS=` mode of
  `tools/host_tests.sh`. pytest's own temp folders landed there too (`F:\Temp\pytest-of-krinik`, removed) —
  `tools/kel_tests.sh`.
- The judge over the linter (VERIFIED WITH CAVEATS): 2 of 153 captions missed while `check` read clean; the tests built
  their expected markup from the code's constants, so a justified, indented caption passed — both fixed in `6343dcc`
  (literal expectations, mutants M7–M12 red).

## 6. Traces

`qa_runs/b14_before_*`, `b14_after_*`, `cap_orig*`, `cap_kel*` (moved to `.tmp/b14_runs/` — GEB text); the owner's
screenshots `.tmp/bug14/shots/`; the linter output `.tmp/kel_out/`; the caption list `.tmp/geb_captions.txt`.

## 7. Verdict

**pass on the simulator** (headings: bugs 14, 15; captions: the linter's binding + the 1.1.3 keep group, on the owner's
book and settings); image `firmware-builds/cp-2.0.0-kccp-1.1.4-debug1.bin` (5 447 376 B, SHA256 `928442f2…`) built
after the smoke of the same commit. Not verified on the reader: the reader is not on the wire (no removable volume,
09:00); the image and the re-typeset GEB go to the card when it is.
