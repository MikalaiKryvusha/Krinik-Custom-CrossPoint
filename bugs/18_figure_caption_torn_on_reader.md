`[OWNER] 2026-11-20 17:33 +03:00 · chat:` «я открыл рисунок 15, он весь грязный...» · «почему не сработало?»

`[OWNER] 2026-11-20 17:34 +03:00 · chat:` «от рисунка 17 отобрава подпись....» · «пиздец» · «нахуй» · «чиним две недели это»

`[OWNER] 2026-11-20 17:35 +03:00 · chat:` «и хуй починили»

`[OWNER] 2026-11-20 17:36 +03:00 · chat:` «отвратительная работа. Клод» · «рисунка 18 тоде подпись оторвана отрисунка.... если
подпись длянная, нужно хотя бы две строки её помещать на страницу с картинкой, а осальное переносить на следующие
страницы»

# Bug 18 — on the owner's reader (1.1.4-debug3) the captions of figures 17 and 18 are torn from their pictures, and figure 15 is dirty

**Status:** 🔴 OPEN · **Severity:** S1 (the owner's trust: «чиним две недели это» · «отвратительная работа») ·
**Version/build:** `cp-2.0.0-kccp-1.1.4-debug3` (firmware `fc97043d`) on his X4 Pro, his GEB copy, his settings ·
**When/context:** 2026-11-20 17:33–17:36 +03:00, minutes after debug3 reached his card · **Fixing:** this session

## Goal vector

**Achieve.** In GEB on the owner's reader every figure stands on the same page as at least the first two lines of its
caption, and a black-and-white figure (15, 17) opens in the viewer clean.

**Acceptance.**
- C1. The owner's rule: WHEN a caption does not fit on the picture's page whole, the reader SHALL put at least its first
  two lines on that page and carry the rest to the next page(s). Source: the owner 17:36 above. Check: the simulator on
  his settings and his book, the pages of figures 17 and 18 (`CROSSPOINT_SIM_SCREEN_TEXT=1`): «Рис. 17» on the same
  page as the picture.
- C2. Figure 15 (`i_019`) and figure 17 (`i_021`) open in the viewer with `Line art` in the log.

## Forensics (2026-11-20 17:33–17:38 +03:00)

1. **Figure 15 dirty — the detector refused it.** `i_019.jpg` 220×40: middle grays 8.9 %, white 47.1 %, black 44.0 %; the
   line-art rule needs white ≥ 50 % (`lineart::kMinWhitePercent`) → «not line art» → no filter, no N; ×2.2 bilinear
   enlargement shows the JPEG noise. Figure 17 (`i_021.jpg`, 194×320): middle 8.6 %, white 42.1 %, black 49.2 % — the same
   miss. Over the 174 GEB pictures within the area: a rule «white ≥ black» flips only `i_019` and `i_144` (figure 117, a
   halftone townscape — not line art) and still misses `i_021` → rejected.
2. **The captions — the book on his card has no binding.** His GEB marks a figure as `<div class="image"><img/></div>`
   followed by a plain `<p><em>Рис. 17. …</em></p>`: nothing ties the two. The Krinik EPUB Linter output of 2026-11-18
   (`.tmp/kel_out3/…epub`, 153 captions bound) wraps them in `<div class="krinik-figure" style="break-inside:avoid">` —
   figures 15 and 17 included — but that book was NEVER copied to his card (STATUS: «not copied yet» since 2026-11-18).
3. **The run, 2026-11-20 17:35–17:40 +03:00** — firmware `fc97043d` (debug3) on the simulator, his settings, chapter III
   (spine 11) pages 0–59, `CARD=.tmp/b18_geb_<orig|kel> CROSSPOINT_SIM_SCREEN_TEXT=1 SIM_TIMEOUT=140 sh tools/sim_pages.sh
   b18_<orig|kel> 11 60`, runs parked in `.tmp/b18_runs/`:
   - his book (`orig`): figure 17 at the bottom of page 29, «Рис. 17. …» at the top of page 30 — **reproduced**;
   - the linter's book (`kel`): page 29 ends after the text, figure 17 and its caption together on page 30; figure 18 on page
     35 shrunk, its caption's first four lines under it, the rest carried to page 36 — the keep-together group works on the
     bound book; how small the picture gets is his eye's.

   **H1 confirmed by the run; H2 partly:** the bound book keeps the captions; a long caption shrinks the picture and carries
   the rest — close to C1, the shrink not yet shown to him.

## Root cause / Hypotheses

- H1 (confirmed by reading): the fixed book was not delivered — the process leak (a «to the card» item left in STATUS).
- H2 (to verify by the run): with the bound book the firmware's keep-together group (epic 07 Ф1) keeps the picture and the
  caption; a LONG caption that cannot fit with its picture is handled by shrinking the picture (floor viewport/4) — not by
  the owner's rule C1 (two lines with the picture, the rest carried).
- H3 (measured): the detector's white ≥ 50 % misses dark-heavy black-and-white drawings.

## Fix plan

1. The run on both books: reproduce the torn caption on the original book; observe the bound book.
2. C1 in the firmware's figure group: a caption longer than what fits keeps ≥ 2 lines with the picture (independent
   review before the build).
3. The detector: a rule that accepts `i_019`, `i_021` and still refuses photos — measured over all GEB pictures, the
   flipped pictures shown to the owner.
4. The bound book + the new image to his card, both in one go.

## Links

- `plans/07_EPIC_figure_caption.md` (epic 07 — figure keep-together); `ideas/14_viewer_smart_filter_bw_lowres.md` (the
  detector); `epub-linter/` (the caption binder); STATUS «not copied yet» line of 2026-11-18.
