# Bug 16 — the last line of a book page touches the status bar, while the top gap is large

**Status:** 🔧 fix committed, pending the owner's default and the reader — firmware `7173e6bd` (2026-11-20), run report
`testcases/reports/2026-11-20_bug16_status_bar_gap_squeeze.md` (all pass on the simulator); the default value page shown
2026-11-20 ≈ 11:30 (`.tmp/mock/out2/status_bar_gap_2026-11-20.md`). Earlier: 🔴 OPEN — mock-ups first (`[OWNER] 2026-11-20 09:40 · chat: «макеты нарисуешь»`, said for the shade circle and the
toolbar lists; the same way taken here)
**Severity:** S2 · **Version/build:** KCCP 1.1.3 on the reader; the same code in `wip/kccp-1.1.4` (`78d89fcd`) and upstream
`develop` · **When/context:** the owner's screenshots 2026-11-19 13:08 and 15:07 (GEB, «ГЛАВА II», pages 25 and 45),
remarks on the review page 2026-11-20 09:46 · **Fixing:** this session, after the owner picks a mock-up

## The owner's words (verbatim, `interviews/decisions/reader_screens_2026-11-20.decision.json`, commit `1d1c67c`)

> текст внизу к строке состояния слишком близко. Желательно ввести настройку отступа внизу минимального, и не прижимать
> текст так близко. Вероятно, тут нужно было чуть-чуть играться межстроковым отступом в строках выше, чтобы обеспечить
> больший зазор внизу.
>
> При этом вверху огромный зазор.

## Goal vector

Avoid: a page whose last line's descenders sit 3 px above the status bar text. Achieve: a reserved gap between the text
area and the status bar, set by the owner in Settings («настройку отступа внизу минимального»).

Acceptance: on the owner's settings and GEB copy (`HOUSE_RULES.md` П4), «ГЛАВА II» page 25 — the gap between the lowest
dark pixel of the text and the top of the status bar text, measured on a full-size simulator shot by a row profile, equals
the setting's value ± 2 px; with the setting at its lowest value the page lays out as today (control case).

## Symptom (measured)

Row profile of the reader's own screenshots (upright, 800×480): the first text line starts at y = 26; the last text line
ends at y = 446 and the status bar text starts at y = 450 — a 3 px gap (shots `ch11_p25`, `ch11_p45`). On a page where the
next line did not fit (`ch9_p54`) the gap is 37 px. The simulator on the owner's settings reproduces it
(`qa_runs/ui_before/shots/page.webp`, 2026-11-20).

## Root cause (read in the code)

`EpubReaderActivity.cpp:1687–1700` (render path): top = the panel's viewable inset + `SETTINGS.screenMargin`; bottom =
viewable inset + `max(SETTINGS.screenMargin, statusBarHeight)`. With the status bar on, `statusBarHeight` (19 = the theme's
`statusBarVerticalMargin`, the text lane itself) replaces the margin instead of adding to it, so the text area ends exactly
where the status bar text begins. The top gap is the margin plus the first line's half-leading.

## The stand did not match the reader (found 2026-11-20)

The first mock-up run printed the page pixel-identical to «today»: on the simulator the page sat 4 px higher and the status
bar 4 px lower than on the reader (text 22…443 and bar 454 on the simulator, 26…446 and 450 on the reader). The cause is the
simulator's X4 Pro profile: `simulator/src/BoardConfig.h` gave it the default viewable insets `{9, 3, 3, 3}` while the
device profile (`freeink-sdk/.../BoardConfig.h` `XTEINK_X4_PRO`) has `{9, 7, 3, 7}`; in landscape the side insets become the
top and the bottom. Fixed on the simulator branch `fix/x4pro-viewable-insets` (local); the page is to be compared with the
reader's own screenshot again on the rebuilt stand.

TWINS: searched `getStatusBarHeight()` in `src/` — `EpubReaderActivity.cpp:1700` is the only text-area reservation (plus
its auto-page-turn branch at :1694); `XtcReaderActivity.cpp:110` draws the bar over a pre-rendered page (no text area);
`StatusBarSettingsActivity.cpp` and `BaseTheme.cpp:839` draw the bar itself.

## Fix plan

1. ✅ Mock-ups shown 2026-11-20 10:33 (`.tmp/mock/out/mockups_1_1_4_2026-11-20.md`): the reader's screenshot vs a 5 px gap
   on the corrected stand — the gap carried the page's last line to the next page (11 → 10 lines, 43 px at the bottom).
2. **The owner's verdict** (10:36, verbatim, `interviews/decisions/mockups_1_1_4_2026-11-20.decision.json` p13): «нет, мне
   не нравится, что ради двух пикселей целую строку перенесли на следующую страницу. Я за то, чтобы чуть-чуть пикселей
   получать от изменения динамически межстрочного интервала того, что сейчас на экране, уплотнения».
3. The design (`[AI]`, to be shown with its run): pagination stays as today (no line is ever carried for the gap). At
   RENDER time, a page whose content bottom comes closer than the gap G to the status bar has its lines moved up
   progressively — line k of n by round(k × need / (n − 1)), need = contentBottom − (H − G) ≤ G — so the last line ends G
   above the bar; the link/footnote hit rects take the same shift. With G = 5 and 11 lines that is < 1 px per line gap.
   FORK: options <squeeze at pagination (cache format, page counts change) | squeeze at render (pages unchanged)> · price of
   error <reflowed pages and moved bookmarks vs a sub-pixel shift> · consulted <the owner's word «динамически … того, что
   сейчас на экране» · KISS — the render-time form changes no cache>.
4. G is the setting he asked for earlier («настройку отступа внизу минимального»); its default and range go to him with
   the run's shots. Twins: only `EpubReaderActivity.cpp:1700` reserves the text area (see TWINS above).
5. Built 2026-11-20 (uncommitted, firmware `wip/kccp-1.1.4`): `PageSqueeze.h` (+ host test), `Page::squeezeBottom`,
   `Section::loadPage` squeezes every page, setting «Отступ над строкой состояния» (`statusBarGap`, 0..20, default 5 `[AI]`).
   Three judges: (1) the setting was hidden (`withTextSettings`), the spaced line box was not the glyph bottom, a gap next
   to a picture could overlap — fixed; (2) drop caps, tight spacing — fixed. **The first simulator run (gap 5/10) moved
   only 1 px:** the air check used the parser's glyph bottom = the font's whole advanceY, larger than the 37 px pitch,
   so no gap inside a paragraph qualified although the ink had 3 px of air; and the gap was measured from the text area's
   bottom while the status text is drawn 4 px above it. Fixed: `PageLine::inkBottom` (ascender + descender from the
   baseline), the limit = the status text's top via `UITheme::statusTextRise()` (shared with `BaseTheme::drawStatusBar`).
   Control: gap 0 is pixel-identical to the page before the change (row profile of `b16_g0` = `d114_2_land`).

## Decisions made without the owner

- `[AI]` Severity S2: every full page of every book shows it.

## Links

`interviews/decisions/reader_screens_2026-11-20.decision.json`; `bugs/14_DONE_lonely_heading.md` (the same stand).
