# TC — idea 14: «Чистить фон чертежей» — the line-art filter on the page, in the viewer and in the file browser

> **Created:** 2026-11-20 · **Parent:** `ideas/14_viewer_smart_filter_bw_lowres.md` (the owner's words 14:16–14:37) ·
> **Status:** written before the run; executed 2026-11-20 15:04–15:14 +03:00 on the simulator, all pass
> (`testcases/reports/2026-11-20_idea14_smart_filter.md`); the reader not verified · **Outbound:** —

## Test basis

- «вьювер картинок при открытии маленьких картинок из книги - их масштабирует - и очень много грязи на белом вокруг черных
  объектов» (14:16) → the formula GEB `i_016.jpg` (36×91) loses the gray squares around its digits.
- «вес 90% вроде хорошо сработал, но, фото, конечно же, не нужно гонять таким алгоритмом» (14:25) → line art: lighter
  than the 90 % darkness-weight cut → white; a photo (`i_140.jpg`, Turing) is drawn exactly as before.
- «Будет опцией в настройках, чекбокс» · «Чистить фон чертежей» · «по читалке, а не по экрану» · «включен» (14:27–14:30)
  → Settings → «Чтение» shows the checkbox, on by default.
- «везде» · «и на странице, и во фулл скрин просмотрщике, и в просмотре картинок из обзора файлов» (14:30–14:31) → the
  page (`ImageBlock`) and the viewer (`BmpViewerActivity`, shared by the book-picture tap and the file browser).
- «480×800 пикселей · Да, согласен» · «не строго такая длина такая высота» (14:37) → only pictures up to 384 000 px of
  area are filtered (host case).

## Dimensions

Picture {line art `i_016`, photo `i_140`} × setting {on (default), off} × place {viewer, page}; the owner's settings and
GEB copy for the page (П4, `.tmp/b14_sd`: «Калибровка книг» off, so the page has no curve). Consciously not covered on
the stand: BMP files (not filtered by design), PNG line art on the stand (host decode path shared with JPEG's logic; the
GEB PNGs are 1-bit and skipped), the reader itself (eFuse; the image after the smoke).

## Cases

| # | Kind | Steps (simulator `simulator_x4_pro_win`) | Expected | Status |
|---|---|---|---|---|
| 1 | smoke | card `.tmp/b17_i_016_on`: boot opens `/i_016.jpg` in the viewer | log `Line art 36x91: lighter than 203 -> white`; the shot has no gray squares around the digits | pass — run report 2026-11-20 |
| 2 | control | card `.tmp/b17_i_016_off` (the setting off) | no `Line art` line; the shot shows the gray squares (today) | pass — run report 2026-11-20 |
| 3 | smoke | card `.tmp/b17_i_140_on` (photo) | no `Line art` line; the shot equals case 4's (`tools/shot_diff.py` TOTAL 0) | pass — run report 2026-11-20 |
| 4 | control | card `.tmp/b17_i_140_off` | the photo as today | pass — run report 2026-11-20 |
| 5 | smoke | GEB chapter II (spine 10) on the owner's settings, the page with `i_016` (≈ p. 22–31), the setting on | log `Line art 36x91` from `IMG`; the picture on the page clean | pass — run report 2026-11-20 |
| 6 | control | the same page, the setting off | no `Line art` line from `IMG` | pass — run report 2026-11-20 |
| 7 | smoke | Settings → «Чтение» (`CROSSPOINT_SIM_SCREEN_TEXT=1`) | the row «Чистить фон чертежей», checked | pass — run report 2026-11-20 |
| 8 | measure | the logs of cases 1, 5 | `Gray histogram … ms` beside `render time … ms` — the extra decode's price | pass — run report 2026-11-20 |
| 9 | hygiene | `TARGETS="LineArtFilterTest" sh tools/host_tests.sh` (6 cases, mutation-proven); the full `sh tools/host_tests.sh` | 6/6; no new failure | pass — run report 2026-11-20 |

### BMP in the viewer (point 3; the owner 2026-11-20 16:30 «нет, чистим всё в полноэкранном вьювере»)

Dimensions: the format (8-bit grayscale BMP · 24-bit RGB BMP · ≤ 2-bit BMP), the content (line art · photo), the setting
(on · off), the path (N enlarged ≥ ×2 · the converter). Not covered: a BMP line art enlarged < ×2 or larger than the
screen (the converter path with the filter) — host case 14 covers the converter's filter.

| # | Kind | Steps (simulator `simulator_x4_pro_win`) | Expected | Status |
|---|---|---|---|---|
| 10 | smoke | card `.tmp/b17_bmp_016_on` (`i_016` as an 8-bit grayscale BMP): boot opens `/i_016.bmp` in the viewer | log `Line art 36x91: lighter than 203 -> white` and `Sharp upscale 36x91 -> 316x800`; the viewer cache equals Pillow N on the BMP's grays: `.tmp/bug17/compare_view_cache_file.py` 0 mismatching pixels at the 480×800 offset | — |
| 11 | smoke | card `.tmp/b17_bmp_140_on` (`i_140` as a 24-bit BMP, a photo) | `Gray histogram` counted, no `Line art`, no `Sharp upscale` | — |
| 12 | control | card `.tmp/b17_bmp_016_off` (the setting off) | no `Gray histogram`, no `Line art`, no `Sharp upscale` | — |
| 13 | regression | the JPEG cards of cases 1 and 3 on the new build | the same log lines as on `fc97043d`; `tools/shot_diff.py` against the `d114_3_*` shots TOTAL 0 | — |
| 14 | hygiene | `TARGETS="BmpToBmpTest" sh tools/host_tests.sh` (`SourceFilterCleansBeforeScaling`, mutation-proven); the full suite | 5/5; no new failure | pass (BmpToBmpTest 5/5, mutant red) — the full suite after the build |
