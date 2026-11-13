# Plan 02 — epic 01, phase 1: the shade tile model and its storage

> **Created:** 2026-11-13 · **Parent:** `plans/01_EPIC_shade_tiles.md` → «Ф1 — модель плиток и хранение» · **Status:**
> 📐 planned; not started · **Outbound:** —

## Goal vector (Achieve)

The shade, the settings screen (phase 2) and the tile row (phase 3) need ONE source of truth for which tiles exist,
which are on, in what order, and where each tile sits in its row. Phase 1 builds it as a pure, host-tested model plus
its persistence, with no visible change yet.

Anchor (meta-plan, Ф1): «Чистая модель: семь плиток со строковыми именами, список по умолчанию, разбор и запись ключа
`shadeTiles`, правило «хотя бы одна плитка включена», функция раскладки с равными отступами. Хранение в
`settings.json`.»

## Acceptance criteria (phase)

1. **Default.** WHEN no `shadeTiles` value was saved, the model shall list night, cleanup, orientation, touch,
   bluetooth ON in that order, then sleep, flashlight OFF. Check: host test `ShadeTilesTest.DefaultList`.
2. **Normalize.** WHEN a saved list holds an unknown id, a duplicate, or misses a known id, the model shall drop the
   unknown, keep the first duplicate, and append the missing id OFF at the end. Check: host tests per case.
3. **At least one on.** WHEN a saved list has every tile OFF, the model shall switch the first tile of the list ON; the
   "clear the last checkbox" request shall be refused. Check: host tests.
4. **Round trip.** The saved JSON of a list shall parse back to the same list. Check: host test over the default and a
   reordered list.
5. **Equal gaps.** FOR n = 1…7 tiles of size s in a row of width w ∈ {800, 480} (minus the shade's insets), every gap —
   the two edge gaps and the inner ones — shall differ from the others by at most 1 px; tiles stay inside the row;
   the touch slots cover the row with no overlap and no hole. Scale: px · Meter: host test `ShadeTilesTest.Layout*` ·
   Target: max gap − min gap ≤ 1. Proven red on the old slot formula (`row.width * id / n`, centred tile).
6. **Storage.** `CrossPointSettings` shall save `shadeTiles` only when it differs from the default (an old firmware
   reading the file is unaffected; a debug9 file loads the default) and shall load it when present. Check: simulator
   run that changes nothing in the tiles → `settings.json` has no `shadeTiles`; a card with a hand-written value →
   the model reports it (log line at load).

## Steps

- [ ] P1.1 Re-read the patterns: `test/page_image_target/` (CMake + gtest), a hand-saved settings field
      (`keyboardLayouts`, `src/CrossPointSettings.cpp:119-120, 307-308`), ArduinoJson array handling (`bleRemotes`,
      `BlePageTurnerJson.h`).
- [ ] P1.2 `src/util/ShadeTiles.h` (pure, header-only like `PageImageTarget.h`): `enum class ShadeTile` (7 values,
      append-only), `kShadeTileIds[]` = "night", "cleanup", "orientation", "touch", "bluetooth", "sleep", "flashlight";
      `struct ShadeTileEntry {ShadeTile tile; bool on;}`; `using ShadeTileList = std::array<ShadeTileEntry, 7>`;
      `defaultShadeTiles()`, `normalizeShadeTiles(ids/ons in) → ShadeTileList`, `isDefault()`, `canTurnOff(list, i)`,
      `moveUp/moveDown(list, i)`; layout `shadeTileLeft(rowX, rowW, size, n, i)` and `shadeTileSlot(…)`; comments
      `[NOT-TESTED]`. Anchor: «чистая модель … функция раскладки с равными отступами».
- [ ] P1.3 Host test `test/shade_tiles/ShadeTilesTest.cpp` + `CMakeLists.txt` + the `add_subdirectory` line: criteria
      1–5; then the mutation: the old slot formula in the layout → the gap test red; restore → green. Anchor: «хост-тест
      зелёный и краснеет на нарочно сломанной раскладке».
- [ ] P1.4 `CrossPointSettings`: field `ShadeTileList shadeTiles`; save as a JSON array of `["id", 0|1]` pairs only when
      not default; load if present → normalize; `[NOT-TESTED]`. Anchor: «Хранение в `settings.json`».
- [ ] P1.5 Judge (a fresh agent, the diff + this plan + the meta-plan, not my conclusions) BEFORE the build; fix findings.
- [ ] P1.6 Host tests: the new suite + the full suite count stays 761 passing (the 8 Windows-portability failures known);
      simulator smoke on the same commit: boot into the book, open the shade, 0 errors; `settings.json` read after the run.
- [ ] P1.7 Commit on `wip/krinik-debug10`; tick Ф1 in the meta-plan; write the phase 2 plan with what phase 1 taught.

## Verification

The host test `test/shade_tiles/` (born in P1.3, proven red in P1.3), the full ctest count (P1.6), the simulator smoke
with `settings.json` read (P1.6), the judge's report (P1.5). A run report
`testcases/reports/2026-11-13_epic01_p1.md` (or the date of the run).

## Risks

1. **The JSON shape breaks an older firmware reading the same card** (the owner keeps debug9 and 1.1.2 on the card).
   Reaction: the key is written only when not default and is unknown to older builds, which ignore unknown keys —
   checked by booting the debug9 simulator binary on a card carrying the key.
2. **Pixel rounding makes one gap 2 px wider at n = 7, w = 480.** Reaction: distribute the remainder one pixel at a
   time from the left; the test's Target (≤ 1 px) holds by construction.
3. **The Bluetooth tile is absent in a build without BLE** (the simulator). Reaction: the model keeps all seven; the
   row (phase 3) and the list (phase 2) skip a tile whose function the build lacks — a phase 2/3 rule, noted there.
