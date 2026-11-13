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
