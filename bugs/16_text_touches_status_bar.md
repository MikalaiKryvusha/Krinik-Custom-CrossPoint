# Bug 16 — the last line of a book page touches the status bar, while the top gap is large

**Status:** 🔴 OPEN — mock-ups first (`[OWNER] 2026-11-20 09:40 · chat: «макеты нарисуешь»`, said for the shade circle and the
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

## Fix plan

1. Mock-ups on the owner's stand: today · status bar + `screenMargin` · status bar + 2 × `screenMargin` (the page of
   «ГЛАВА II» p. 25), shown to the owner.
2. Then the setting he asked for (a minimum gap above the status bar), default by his pick; the twins — every reader that
   reserves the status bar (`git grep -n "getStatusBarHeight()" -- src`) — follow the same rule.
3. The line-spacing idea («играться межстроковым отступом») is a vertical-justification feature; it is shown to the owner
   as an option only if the plain gap is not enough.

## Decisions made without the owner

- `[AI]` Severity S2: every full page of every book shows it.

## Links

`interviews/decisions/reader_screens_2026-11-20.decision.json`; `bugs/14_DONE_lonely_heading.md` (the same stand).
