# TC — bug 16: the gap above the status bar taken from the page's own line gaps

> **Created:** 2026-11-20 · **Parent:** `bugs/16_text_touches_status_bar.md` (the owner's verdict 2026-11-20 10:36) ·
> **Status:** written before the run; executed 2026-11-20 11:21–11:27 +03:00, all pass · **Outbound:** the shots of gaps 0 / 5 / 10 go to the owner for the default

## Test basis

- «текст внизу к строке состояния слишком близко. Желательно ввести настройку отступа внизу минимального» (09:46).
- «нет, мне не нравится, что ради двух пикселей целую строку перенесли на следующую страницу. Я за то, чтобы чуть-чуть
  пикселей получать от изменения динамически межстрочного интервала того, что сейчас на экране, уплотнения» (10:36).
- Expectation derived: with the setting «Отступ над строкой состояния» = G, the gap between the lowest text pixel and the
  status bar text is ≥ G px on a full page, the page holds the SAME lines as with G = 0, and G = 0 is today's page.

## Dimensions

G ∈ {0 (control), 5 (the default), 10}; the owner's page «ГЛАВА II» p. 25 (full: 11 lines + a paragraph gap) and a page
with free space at the bottom (no-op); landscape (the owner's). Consciously not covered: pages with a picture or a
border box at the very bottom (GEB p. 25 has none — the judge reads that path), portrait, other fonts.

## Cases

| # | Kind | Steps (simulator, `.tmp/ui_sd`, `settings.json` → `statusBarGap`) | Expected | Status |
|---|---|---|---|---|
| 1 | control | G = 0, open «ГЛАВА II» p. 25 | pixel-identical to the pre-change page (`tools/shot_diff.py` TOTAL 0); 3 px under the last line | pass — `shot_diff … 32` (the status bar's clock cut) TOTAL 0; 2 px under the last ink on the simulator |
| 2 | smoke | G = 5 | the same 11 lines, first line at the same y; the gap under the last line ≥ 5 px (`tools/shot_rows.py`) | pass — run report 2026-11-20 |
| 3 | boundary | G = 10 | the same 11 lines; gap ≥ 10 px; no line gap shrinks by more than 1 px | pass — run report 2026-11-20 |
| 4 | no-op | G = 5 on a page whose text ends ≥ 5 px above the bar | pixel-identical to G = 0 | pass — run report 2026-11-20 |
| 5 | promise | G = 5, page count of the chapter in the status bar | the same «N/105» as G = 0 (no re-pagination) | pass — run report 2026-11-20 |
| 6 | setting | Settings → Чтение → «Отступ над строкой состояния» | the row shows 5, steps 0…20 | pass for the row and its 5 (screen text); the 0…20 steps read in the code, not walked |
| 7 | hygiene | `TARGETS="PageSqueezeTest" sh tools/host_tests.sh`; a mutant (no proportional spread) red; the full suite | 4/4; red; no new failure | pass — 5/5 (a case added with the judges' fixes), the mutant red ×2, 995 no new failure |
