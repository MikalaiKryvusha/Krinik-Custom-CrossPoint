# Research — how a row of equal icon buttons is spaced (the shade's button row, bug 12)

> **Created:** 2026-11-17 · on the owner's word 2026-11-17 20:51 +03:00 «Иди ищи в интернете, как дизайнеры расстояния
> считают для таких кейсов» · **Parent:** `bugs/12_shade_row_gaps.md` · **Status:** done 2026-11-17 ≈ 21:00 +03:00 ·
> **Outbound:** —

## Question

A row of n fixed-size icon buttons across a sheet: how are the gaps between the buttons and at the two ends computed so
the row looks even? (The owner on debug4: «Слева и справа огромные остаются, а кнопки тесно друг к дружке».)

## Found (web, 2026-11-17)

1. **`space-evenly` for a full-width icon row.** Equal gaps between the items AND at both edges; `space-between` puts
   the first and last flush to the edges and «looks unbalanced with few icons». Flutter's `MainAxisAlignment.spaceEvenly`
   vs `spaceBetween` is the same distinction. Sources:
   [gurubase — ButtonBar spacing in Flutter](https://gurubase.io/g/flutter/best-practices-spacing-buttons-buttonbar-flutter),
   [Educative — space-between + centering](https://www.educative.io/courses/css-design-patterns/lta/space-between-centering-three-items).
2. **The edge counts from the container's visible edge.** A flex/grid `gap` adds no space before the first item or after
   the last, so when the edges must match the gap the container's padding is SET EQUAL to the gap (MDN); design systems
   add that mathematically equal spacing may still look uneven and is corrected optically (Configura, Atlassian).
   Sources: [MDN — Defining CSS gaps](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gaps/Defining_gaps),
   [Configura — Spacing & Layout](https://dev-docs.configura.com/design-system/spacing-and-layout),
   [Atlassian — Spacing](https://atlassian.design/foundations/spacing).
3. **A floor for the gap.** Touch targets ≥ 48 × 48 dp with ≥ 8 dp between them (Material, Google accessibility);
   distributed spacing can push icons far apart on wide screens — a fixed gap is the alternative there. Sources:
   [Google — Touch target size](https://support.google.com/accessibility/android/answer/7101858),
   [Material — Applying density](https://material.io/design/layout/applying-density.html),
   [Apple HIG — Toolbars](https://developer-mdn.apple.com/design/human-interface-guidelines/components/menus-and-actions/toolbars),
   [Primer — Action bar](https://primer.style/product/components/action-bar/accessibility).

No source prescribes one formula for a quick-settings row; the three points above are consistent.

## What KCCP did (debug4) and why it looks wrong

`shadetiles::tileLeft` is `space-evenly` — but over the row INSIDE the sheet's content inset (`kPanelSideMargin` = 16 px
each side, `FrontlightPanelActivity::buildPanelScreen`). The visible edge is the sheet's edge, so the eye sees
`16 + gap` at the ends and `gap` between. Portrait, 56 px buttons, width 480:

| Buttons on | gap (debug4) | visible end (debug4) | gap = end, from the sheet edge |
|---|---|---|---|
| 5 (the reader's default, Bluetooth on) | 28 | 44 | 33 |
| 6 (the simulator's maximum) | 16 | 32 | 20.6 |
| 7 (all on, the reader) | 7 | 23 | 11 |

The guard `tools/shade_gaps.py` measured the gaps from the slider row's edges (the same inset), so it passed.

## Decision

`FORK: options <A space-evenly from the sheet's visible edges | B space-between inside the content inset (aligned to
the sliders) | C fixed gap + centred row> · price of error <a row the owner reads as uneven again; a taste call> ·
consulted <web sources above; the owner's words (equal ends and gaps)>` → **A**: it is the found rule (1, 2) and the
owner's complaint is exactly the ends vs the gaps; with 7 buttons the gap is 11 px ≥ 8 (point 3). `[AI]` — the look is
the owner's taste: he judges it on the reader. The guard measures from the sheet's edge from now on.
