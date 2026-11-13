# Test cases — epic 01, phase 2: the settings screen «Кнопки в шторке»

**Created:** 2026-11-13 · **Under test:** `wip/kccp-1.1.3-debug2` (`firmware/`, on `bcbd6dab`) — `ShadeTilesActivity`, its
row in Settings → Display · **Version/build:** simulator `simulator_x4_pro_win` (built without Bluetooth), then
`1.1.3-debug2` on the owner's X4 Pro with phase 3
**Test basis:** `plans/03_epic01_p2_tiles_screen.md` → acceptance criteria 1–6; the meta-plan row Ф2 of
`plans/01_EPIC_shade_tiles.md` («Список из семи строк: иконка, имя, квадратик прошивки, ▲ ▼. Книжная ориентация. …
Пункт в «Настройки → Экран».»); the epic rule «Хотя бы одна плитка остаётся включённой: последний квадратик не
снимается, строка текста поясняет почему».

## 1. Goal vector

Achieve: the owner turns the shade's tiles on and off and puts them in his order on one screen, and the row is kept in
`settings.json`.

## 2. Requirements under test

| # | Requirement (EARS sentence) | Fit criterion |
|---|---|---|
| R1 | WHEN the owner opens Settings → «Экран» → «Кнопки в шторке», the screen shall list the shown tiles in the stored order, each row with icon, name, checkbox (filled = on), ▲ ▼. | shot: header «Кнопки в шторке», the note, six rows on the simulator in the default order, four checked |
| R2 | WHEN he taps a row, the tile shall turn on / off. | shot after the tap: the checkbox changed |
| R3 | IF the tapped row is the last shown tile that is on, THEN the screen shall keep it on; the note above the rows says why. | shot: the checkbox stays filled |
| R4 | WHEN he taps ▲ (▼), the row shall move one shown place up (down); every row shows ▲ ▼ (the mockup `homeworks/05_shade_mockups/final.html`, step 2), and ▲ on row 1 / ▼ on the last row do nothing. | shots: the order after each move; a tap on the dead arrow changes nothing and does not toggle the row |
| R5 | WHEN he leaves the screen after any edit, the screen shall save the settings and log the row; `settings.json` shall hold `shadeTiles` only while the row differs from the default. | the card's `settings.json` read after the run; log `Shade tiles saved:` |
| R6 | WHEN the screen was opened from Settings, Back shall return to «Экран». | shot after Back: «Экран» |
| R7 | The keys shall move the cursor (Up / Down, wrapping) and check / uncheck the cursor row (Confirm). | shots: the pill row and the checkbox |

## 3. Coverage matrix

| Dimension | Values covered | Explicitly NOT covered (risk named) |
|---|---|---|
| board | simulator: no Bluetooth → six rows, the hidden tile stepped over by ▲ | seven rows with Bluetooth — the owner's reader (homework with the debug10 image) |
| entry | Settings → «Экран» | from the shade by a long tap, cursor on the tapped tile, Back to the book — phase 3 builds that entry |
| orientation | portrait (Settings) | the screen over a landscape book — phase 3 (the code sets portrait and restores the caller's) |
| tile count on | 4 (default) · 1 shown + hidden Bluetooth on (boundary) · 2 | 0 — impossible by R3 |
| Back | swipe from the left edge · header arrow tap · the Back key | — |
| stored row | default (no key) → changed → default again (no write) | an old card from debug9 — phase 1 run 4 covered the missing key |

## 4. Cases

| # | Case (steps → expected) | Technique | Status + evidence |
|---|---|---|---|
| C1 | Home → Settings → «Экран»: «Кнопки в шторке» is the second row (shot `display`); tap it → `Entering activity: ShadeTiles`; shot `tiles0`: header, note, rows «Ночной режим» ☑, «Очистка экрана» ☑, «Ориентация чтения» ☑, «Сенсор» ☑, «Сон» ☐, «Фонарик» ☐; each row: icon, name, ▲, ▼, the checkbox at the right edge (the mockup); the cursor pill on row 1 | smoke (R1, R6 entry) | not run |
| C2 | C1 → tap the «Сон» row → «Сон» ☑ (shot) | use case (R2) | not run |
| C3 | C2 → ▲ on «Сон» three times, each after the previous move is on the screen (a tap on a frame that does not show the last move is dropped by design) → order «Ночной режим», «Сон», «Очистка экрана», «Ориентация чтения», «Сенсор», «Фонарик» (shot); the first ▲ steps over the hidden Bluetooth | state transition (R4) | not run |
| C4 | C3 → ▼ on «Ночной режим» → «Сон» first, «Ночной режим» second (shot); then ▲ on «Сон» (row 1) → the order and the checkboxes unchanged (shot) | state transition, boundary (R4) | not run |
| C5 | C4 → swipe Back from the left edge → `Popped`, shot = «Экран»; log `Shade tiles saved: sleep,night,cleanup,orientation,touch,bluetooth,-flashlight`; the card's `settings.json` holds that string | use case (R5, R6) | not run |
| C6 | C1 → uncheck «Очистка экрана», «Ориентация чтения», «Сенсор» → only «Ночной режим» ☑ among the rows (Bluetooth hidden but on); tap «Ночной режим» → stays ☑ (shot) | boundary (R3) | not run |
| C7 | C6 → tap «Сон» (☑), tap «Ночной режим» → «Ночной режим» ☐ now (two were on) (shot); header arrow tap → `Popped`; `settings.json`: `-night,-cleanup,-orientation,-touch,bluetooth,sleep,-flashlight` | control of C6 (R3), header Back (R6) | not run |
| C8 | C1 → Down, Down → pill on row 3 (shot); Confirm → «Ориентация чтения» ☐ (shot); Confirm → ☑; Up ×3 → pill wraps to «Фонарик» (shot); Back key → `Popped`; log `Shade tiles saved:` with the default row (an edit was made — the save is by the edit flag, by design: a shade opened in between may have saved an intermediate row), and NO `shadeTiles` key in `settings.json` (the row equals the default) | keys (R7), control of R5 (the default row is never written) | not run |

## 5. Not covered — said aloud

- Seven rows with Bluetooth, the panel's look of the light pill and the icons — the owner's reader.
- The phase 3 entry (long tap in the shade, cursor on that tile, Back to the book page, landscape book underneath).
- Moving a row by keys — not built (an open detail of phase 2, said in the report).
