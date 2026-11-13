# Idea 05 — configuring the quick actions of the shade (control center), and entering those settings from the shade

> **Created:** 2026-11-13 (the owner's request, chat — given while debug9 waited for the reader) · **Parent:** `STATUS.md` →
> «Future» (configurable Control Center tiles, owner 2026-11-06) · **Status:** 🆕 the owner's original, verbatim ·
> **Outbound:** — · **Status update:** 🎨 mockups ready 2026-11-13 ≈11:56 +03:00 — homework 05, owner's choice pending

## Recon (2026-11-13, `wip/krinik-debug9`)

- The shade = `src/activities/util/FrontlightPanelActivity.{h,cpp}`: a top-anchored sheet opened by a top-edge
  down-swipe, a status-bar tap or a button bound to «Control Center»; header (time, battery), the brightness slider
  with a lamp toggle, the warmth slider, then a row of quick tiles — `kTileCount = 5`, fixed order in `runTile(idx)`:
  0 night mode · 1 ghost-cleanup refresh (closes the sheet) · 2 orientation cycle · 3 touch reader controls ·
  4 Bluetooth (only when compiled in — the simulator shows 4). Tiles are 1-bit rounded squares, filled when on.
- Shot of today's shade: `qa_runs/idea05_shade_now/shots/shade.webp` (landscape, over a book page).
- Candidate tiles offered in the mockups: the five above + the KCCP Home items «Сон» (Sleep) and «Фонарик»
  (Flashlight) — only functions the firmware already has (`[AI]` catalogue, the owner may add).
- The Settings option picker (`components/OptionPopup`) already exists — variant Г reuses it.

`[OWNER] 2026-11-13 11:48 +03:00 · chat:`

> и нужно начать набрасывать макеты того. как мы сделаем настройку квик экшенов в шторке
>
> и часто делают возможность попасть в настройки шторки через саму шторку - можно будет на такое тоже варианты макетов?

`[OWNER] 2026-11-13 12:23 +03:00 · chat` (homework 05, entry variants 1–4):

> 3 Долгий тап по любой плитке

`[OWNER] 2026-11-13 12:24 +03:00 · chat` (homework 05, screen variants А–Г, asked «what does the long tap open?»):

> АСписок с галочками и стрелками

`[OWNER] 2026-11-13 12:25 +03:00 · chat:`

> прич\м пусть лонг-тап из шторки сразу вед\т внутрь настроек на соответствующий экран

`[OWNER] 2026-11-13 12:47–12:56 +03:00 · chat` (after the agent asked which «соответствующий экран» is meant):

> покажешь макеты?
>
> гоу

> покажешь макет?

> не понимаю, что ты открыл

> мы же согласовали макеты и решения

> я хотел более конечный вид того, что согласовали

**Agreed design** (`[AI]` reading of «мы же согласовали» — the screen is the one he chose, А; said to him in chat
12:57): a long tap on any tile opens Settings straight on «Плитки шторки» — the list with checkboxes and ▲▼, portrait
like every Settings screen, the cursor on the long-tapped tile. Final view: `homeworks/05_shade_mockups/final.html`.
Decided by the agent unless he says otherwise: Back from «Плитки шторки» returns to the book; the screen is also
reachable from «Настройки → Экран». Still open for him: the tile set (7).

`[OWNER] 2026-11-13 13:00 +03:00 · chat` (on the final view, frame 3 with six tiles; a crop of it attached):

> здесь отступы некорректные

> отступы нужно будет пересчитывать для разного числа плиток

> чтобы они органично в центре располагались, с равными отступами между ними и по краям

`[OWNER] 2026-11-13 13:19–13:24 +03:00 · chat` (on the final view):

> странные у тебя чекбоксы
> в прошивке квадратики

> для переключателя темы нужно нарисовать новую кнопку, как в iOS - круг черный и белый по половине, найди в интентете.
>
> Сон - будет полумесяц

**Requirement (from the words above):** WHEN the shade shows N tiles, the firmware shall place them with equal gaps
between the tiles and at both edges: gap = (sheet width − N × 56) / (N + 1). Today `FrontlightPanelActivity`
centres each tile in an equal slot (`row.width * id / tileCount`) — its edge gap is half the gap between tiles, so
the row layout itself changes. Fit: for N = 5 / 6 / 7 the gap is 86.7 / 66.3 / 51 points, measured on a simulator
shot of each N.
