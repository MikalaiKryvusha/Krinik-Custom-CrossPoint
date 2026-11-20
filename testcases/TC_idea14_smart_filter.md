# TC — idea 14: «Чистить фон чертежей» — the line-art filter on the page, in the viewer and in the file browser

> **Created:** 2026-11-20 · **Parent:** `ideas/14_viewer_smart_filter_bw_lowres.md` (the owner's words 14:16–14:37) ·
> **Status:** written before the run · **Outbound:** —

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
| 1 | smoke | card `.tmp/b17_i_016_on`: boot opens `/i_016.jpg` in the viewer | log `Line art 36x91: lighter than 203 -> white`; the shot has no gray squares around the digits | — |
| 2 | control | card `.tmp/b17_i_016_off` (the setting off) | no `Line art` line; the shot shows the gray squares (today) | — |
| 3 | smoke | card `.tmp/b17_i_140_on` (photo) | no `Line art` line; the shot equals case 4's (`tools/shot_diff.py` TOTAL 0) | — |
| 4 | control | card `.tmp/b17_i_140_off` | the photo as today | — |
| 5 | smoke | GEB chapter II (spine 10) on the owner's settings, the page with `i_016` (≈ p. 22–31), the setting on | log `Line art 36x91` from `IMG`; the picture on the page clean | — |
| 6 | control | the same page, the setting off | no `Line art` line from `IMG` | — |
| 7 | smoke | Settings → «Чтение» (`CROSSPOINT_SIM_SCREEN_TEXT=1`) | the row «Чистить фон чертежей», checked | — |
| 8 | measure | the logs of cases 1, 5 | `Gray histogram … ms` beside `render time … ms` — the extra decode's price | — |
| 9 | hygiene | `TARGETS="LineArtFilterTest" sh tools/host_tests.sh` (6 cases, mutation-proven); the full `sh tools/host_tests.sh` | 6/6; no new failure | — |
