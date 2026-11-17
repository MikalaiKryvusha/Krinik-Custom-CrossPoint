# Idea 10 — the shade without buttons: every shade button can be off, and then the button row is gone

> **Created:** 2026-11-17 · the owner in chat 2026-11-17 21:31 +03:00 (his decision, not the agent's proposal) ·
> **Parent:** epic 01 (`plans/01_EPIC_shade_tiles.md`) · **Status:** 🔧 built in the firmware, the judge reading;
> simulator run next · **Outbound:** —

## The owner's words (verbatim, committed first in `1a87373`)

> давай сделаем так, что можно ВСЕ кнопки из шторки выключить - тогда область под кнопки из шторки исчезает. Если
> добавили хоть одну кнопку - опять появляется эта область и кнопки в ней. То есть можно сделать минималистичную шторку
> без кнопок

## Goal vector (Achieve) and acceptance

A minimal shade: the light sliders only, when the owner wants no buttons.
- Situation. «Настройки → Экран → Кнопки в шторке», every button checked off.
- Action. The user opens the shade.
- Result. The shade shows brightness and warmth and no button row; the sheet ends right under the warmth slider.
- Check. A simulator shot of the shade: no button squares between the warmth slider and the grabber; the sheet's
  bottom is higher than with buttons by the row's height (56 px).
- And: one button checked again → the row is back with that one button (centred, equal ends).

## What changes (firmware)

- `shadetiles::canTurnOff` lets the last button go off; `parse` keeps an all-off list off (an empty string is still the
  default list). Before: at least one stayed on — an `[AI]` rule of epic 01 (a way back to the screen by a long tap).
- «Кнопки в шторке» no longer refuses the last checkbox; its note above the rows: «Без отмеченных кнопок в шторке
  остаются только яркость и теплота.» (`[AI]` wording — was «Хотя бы одна кнопка остаётся включённой: долгий тап по
  кнопке в шторке открывает этот экран.»).
- The shade: no row and no row height when no button is shown.

## Decisions made without the owner

- `[AI]` The note's new second sentence (above).
- `[AI]` With no buttons the screen is reached only from Settings → Display (no long tap target left) — the owner's
  word implies it.

## Links

Epic 01 · `src/util/ShadeTiles.h` · `FrontlightPanelActivity` · `ShadeTilesActivity`

## Дополнение владельца (2026-11-17 21:46, дословно)

> в сборке KCCP по умолчанию в шторке
> - Тема
> - Ориентация
> - Фонарик
> - Сон
