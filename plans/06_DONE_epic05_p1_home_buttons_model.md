# Plan 06 — epic 05, phase 1: the Home button model and its storage

> **Created:** 2026-11-14 · **Parent:** `plans/05_EPIC_home_buttons.md` → «Ф1 — модель кнопок и хранение» · **Status:**
> ✅ phase closed 2026-11-14 15:56 +03:00 — firmware `be6e9a16`; host test 11/11 × plain + mama (red on an unlocked and on a row-keyed
> lock), shade 12/12, full suite 795/803 (the 8 known), simulator plain build (`testcases/reports/2026-11-14_epic05_p1.md`);
> judge: VERIFIED WITH CAVEATS, no blockers, findings fixed · **Outbound:** —

## Goal vector (Achieve)

Home (Ф2, Ф3), the settings screen (Ф4) and the long-tap entry (Ф5) need ONE source of truth for which Home buttons
exist in this build, which are on, and in what order. Phase 1 builds it as a pure, host-tested model plus its
persistence, with no visible change yet. The token-level storage algorithm is shared with the shade model.

Anchor (meta-plan, Ф1): «кнопки со строковыми именами; список по умолчанию для обычной и маминой сборки; «Настройки»
всегда включена; разбор и запись ключа `homeButtons`; кнопка из будущей прошивки встаёт в конец выключенной. Алгоритм
хранения общий с моделью шторки (`ShadeTiles.h`). Хранение в `settings.json`.»

## Acceptance criteria (phase)

1. **Default.** WHEN no `homeButtons` value was saved, the model shall list files, library, plugins_opds, transfer,
   settings, flashlight, sleep — all ON, in today's Home order — and, in the mama build only, mama ON last. Check: host
   tests `HomeMenuButtonsTest.DefaultIsTodaysOrder` in the plain and the mama executable.
2. **Normalize.** WHEN a saved list holds an unknown id, a duplicate, or misses a known id, the model shall drop the
   unknown, keep the first occurrence, and append the missing id OFF at the end. Check: host tests per case.
3. **Settings stays on.** WHEN a saved list marks settings OFF or lacks it, the model shall hold settings ON (a missing
   settings goes to the end ON); a request to toggle settings shall be refused. Check: host tests; proven red against a
   model whose lock is removed.
4. **Build scope.** The plain build's model shall have no mama entry; a mama-build string loaded by the plain build
   shall drop `mama` as unknown. Check: host test in the plain executable.
5. **Round trip.** `format(parse(s)) == s` for the default and a reordered list. Check: host test.
6. **Visible buttons.** For a list and the runtime fact «the plugins/OPDS slot exists», the model shall return the ON
   buttons in list order, without plugins_opds when the slot does not exist. Check: host test.
7. **Shade unchanged.** The shade model's 12 host tests stay green after the shared part moves out. Check: ctest
   `ShadeTilesTest`.
8. **Storage.** `CrossPointSettings` shall save `homeButtons` only while it differs from the default and log the
   loaded list at boot (`Home buttons: …`). Check: simulator run → the log line; `settings.json` without the key after
   a run that changes nothing; a hand-written value is reported back normalised.

## Steps

- [x] P1.1 `src/util/IdOrderList.h` (pure): `trimmed`, `forEachToken(stored, onToken(id, on))`, `moveUp/moveDown/
      countOn` over any `std::array` of entries with `.on`. `ShadeTiles.h` calls them; its API stays as is. Anchor:
      «Алгоритм хранения общий с моделью шторки».
- [x] P1.2 `src/util/HomeMenuButtons.h` (pure), namespace `homemenu`: `enum class Button` (append-only; `Mama` only
      under `KRINIK_MAMA`), `kIds`, `Entry {Button button; bool on;}`, `List`, `defaults()`, `isLocked()`,
      `canToggle()`, `parse()`, `format()`, `isDefault()`, `moveUp/moveDown`, `visible(list, hasPluginsOpdsSlot)`,
      `indexIn()`.
      Comments `[NOT-TESTED]`. Anchor: «кнопки со строковыми именами … «Настройки» всегда включена».
- [x] P1.3 Host test `test/home_menu_buttons/` — TWO executables from one source (plain, `-DKRINIK_MAMA=1`): criteria
      1–6; the mutation: the lock removed → criterion 3 red; restored → green. Anchor: «хост-тест … краснеет на нарочно
      сломанном правиле».
- [x] P1.4 `CrossPointSettings`: field `homemenu::List homeButtons`; save when not default; load + `LOG_INF`. Anchor:
      «Хранение в `settings.json`».
- [x] P1.5 Judge (a fresh agent: the diff + this plan + the meta-plan) BEFORE the build; fix findings.
- [x] P1.6 `sh tools/host_tests.sh` (no new failure, CRLF guard); simulator smoke on the same commit (boot → Home, the
      log line, 0 `[ERR]`), `settings.json` read; a hand-written value on the card read back; a shade shot (risk 3).
      Plain build only: this PC has no Windows mama simulator env, so the mama storage path is host-tested only
      (`HomeMenuButtonsMamaTest`); `simulator_x4_pro_mama_win` (`-DKRINIK_MAMA=1`) goes into `platformio.local.ini`
      before Ф3 (meta-plan criterion 4).
- [x] P1.7 Run report, commit on `wip/kccp-1.1.3-debug2`, tick Ф1 in the meta-plan, write the Ф2 plan
      (`plans/08_DONE_epic05_p2_home_by_model.md`).

## Verification

Host test `test/home_menu_buttons/` (born in P1.3, proven red in P1.3), `ShadeTilesTest` 12/12, the full suite by
`tools/host_tests.sh`, the simulator smoke with `settings.json` read (P1.6), the judge's report (P1.5). Run report
`testcases/reports/2026-11-14_epic05_p1.md`.

## Risks

1. **An older firmware on the card saves settings without `homeButtons`** (the shade's risk 1, same mechanism): the
   owner's Home order resets to the default. Said in the image's homework.
2. **A mama-build card read by a plain build** keeps the order without mama. Back on the mama build: if the plain build
   saved a non-default list, mama is appended OFF (criterion 2); if the plain list equals the plain default, the key
   is dropped on save and mama comes back ON and last — a hidden or moved mama loses that state (the judge, 15:4x).
   The mother's reader runs the mama build only, so this needs a card moved between builds.
3. **Shared code regresses the shade** — guarded by the shade's 12 tests (criterion 7) and a shade smoke shot.

## Decisions made without the owner

- `[AI]` The storage algorithm is SHARED with the shade (`IdOrderList.h`) and the shade's API is kept by thin wrappers
  (its unused internals `kOffMark`, `kSeparator`, `trimmed` moved to `idorder`) — the meta-plan's «Алгоритм хранения
  общий с моделью шторки», chosen over a templated model because the shade code reads `.tile` in 7 places.
- `[AI]` Ids: `files`, `library`, `plugins_opds`, `transfer`, `settings`, `flashlight`, `sleep`, `mama`; the plugins/OPDS
  slot is ONE id (interview #004, «Решаю сам», unchanged by the owner).
- `[AI]` The mama button exists only under `KRINIK_MAMA` (kCount 7 or 8 per build), so a plain build drops `mama` as an
  unknown id — the owner's «Есть только в маминой сборке» (Q2) read as «absent from the plain model».
- `[AI]` A missing «Настройки» in a hand-edited value goes to the end ON (in the mama build below mama) — documented in
  the parse comment, not special-cased (the judge's finding 5: only a hand edit reaches it).
- `[AI]` `visible()`/`indexIn()` land in Ф1 with their host tests so Ф2 consumes a tested function.
- PENDING settled: none were opened.
