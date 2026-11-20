# STATUS — Krinik Custom CrossPoint (KCCP)

Updated 2026-11-20 09:45 +03:00 (the 09:38 chat: the owner's screenshots page, tasks b–d below). Licence: MIT (owner, 2026-11-08: «как у оригинального CP, или MIT»); fonts OFL, firmware images GPLv3.
 Moved off the owner's laptop, where it lived as a loose folder (`~/Xteink`) beside an unrelated
work project. From now on it is a standalone project.

## Where to continue

- **The 2026-11-20 09:38 chat — the owner's tasks, in the order given** (they come before the 1.1.4 steps below):
  (a) the reader's screenshots (reader on the wire, card `H:`): the four never analysed — `ch11_p25`, `ch11_p45` (19.11),
  `ch9_p45`, `ch9_p54` (17–18.11; `ch10_p1/p20/p28` were bugs 14/15) — copied to `.tmp/screens_2026-11-20/` (WebP, upright),
  the page `reader_screens_2026-11-20.md` shown 2026-11-20 09:44 +03:00 through the contour (`--proofread`, a field under each shot);
  his remarks land in `interviews/decisions/reader_screens_2026-11-20.decision.json`. The card holds images 1.1.2 and 1.1.3
  only (no 1.1.4) and GEB of 11.11 (no linter fixes); his fresh `settings.json` → `.tmp/screens_2026-11-20/`.
  **Answered 2026-11-20 09:46 +03:00** (`1d1c67c`, verbatim): shots 1–2 — the bottom line touches the status bar while the top
  gap is huge, wants a minimum-bottom-gap setting (measured: 3 px under the last line's descenders vs 26 px above the first;
  `EpubReaderActivity.cpp:1700` reserves `max(screenMargin, statusBarHeight)` at the bottom — the margin is not added to
  the status bar's 19 px) → bug 16, mock-ups first; shot 3 — a heading off-centre with an indent (bug 15, fixed in 1.1.4,
  not on the reader); shot 4 — a caption carried over (fixed in the linter's GEB + keep-together, not on the card).
  (e) optional — `[OWNER] 2026-11-20 09:50 · chat: «написать отчёт о том, что там много места занимает в прошивке кроспоинт
  оригинальной, почти всю память программ занимает в ESP32 - побить на функциональные блоки и перечислить таблицей»` → a
  background agent builds upstream `develop` `x4pro` in a `.tmp/` worktree and writes
  `reports/2026-11-20_crosspoint_flash_budget.md`; no other PlatformIO build until it reports.
  (b) `[OWNER] 2026-11-20 09:39 · chat: «кружок кнопки переключения темы сделать больше радиусом, на прочентов 20»`;
  (c) `[OWNER] 2026-11-20 09:40 · chat: «В меню, вызываемое в книге по тапу в центре - меню, которое внизу открывается, есть
  три кнопки. по ним открываеются листаемые списки - в них почему-то огромные отступы, нужно сделать более тестно»`;
  (b) and (c) start with mock-ups — `[OWNER] 2026-11-20 09:40 · chat: «макеты нарисуешь»`.
  (d) upstream issue #4515 (bug 08): `AlmostGivingUp` (new to the project) asked the model 2026-11-18 12:01 UTC and on
  2026-11-19 14:54 UTC wrote he will try a fix — his read: Cover Grid's `HomeCoverCache` is not invalidated on a Night switch
  (that is the bug 07 class, fixed upstream inside #4494 `b9c23473`; #4515 is the frame under the OPEN sheet, book pictures
  too). Any reply goes out only after the owner's proofreading.

- **DEBT — the closing judge pass of the 2026-11-18 08:44 chat** was skipped on the owner's word `[OWNER] 2026-11-18 10:41 ·
  chat: «пока этот чат закрывать. Сразу после твоего суб-агента, без судейства»` — the next `/end-chat-soft` runs
  `/fable-judge` over this chat's claims (the 1.1.4 block below, the two run reports of 2026-11-18, the linter `6343dcc`).
  KNOWLEDGE (this chat): HOUSE_RULES П4 (reading tests on the owner's settings and book) and П5 (image names, release
  content); the stand row «Книга Николая на его настройках» and `tools/sim_pages.sh`, `tools/park_runs.sh`,
  `tools/kel_tests.sh`, `TARGETS=` of `tools/host_tests.sh`; EXPERIENCE 0037–0039; the maps (BlockStyle heading keep, the
  shade model, `epub-linter/`); researches on FB2 converters and the update channel; ideas 11–13.

- **KCCP 1.1.4 — in work since 2026-11-18 08:44 +03:00** on the owner's word «давай скорее делать 1.1.4, так как я вчера
  начал читать и ужас с этими заголовками, и переносами подписей картинок на следующие страницы»: (1) bugs 14 (a lonely
  heading) and 15 (a heading's first-line indent) in the firmware, branch `wip/kccp-1.1.4` from the 1.1.3 release
  `c1c38089`; (2) the captions are the book's markup and are fixed in Krinik EPUB Linter (`[OWNER]` 08:49), now the
  sub-project `epub-linter/` (`[OWNER]` 08:52, own repo) — the figure pairs move there from `tools/figure_retypeset.py`,
  with the EPUB 2 form (GEB is EPUB 2.0); (3) every reading test on the owner's settings and his GEB copy
  (`HOUSE_RULES.md` П4); (4) the READMEs of the three projects link each other — KCCP firmware, Krinik EPUB Linter,
  KEINKT (`[OWNER]` 08:53 «Три проекта в README их нужно будет "связать" - сослаться друг на друга, они всё друг друга
  дополняют»; the linter's README already links KCCP) — done with the 1.1.4 README. The 1.1.3 debts below wait behind it.
  **Done 2026-11-18 09:48 +03:00:** bugs 14, 15 DONE on the simulator (firmware `d727eeef`; the owner's GEB and settings, run report
  `testcases/reports/2026-11-18_kccp114_headings_captions.md`); image **`firmware-builds/cp-2.0.0-kccp-1.1.4-debug1.bin`**
  (`21671e33`, SHA256 `928442f2…`) — waits for the reader on the wire, with the linter's GEB (153 captions bound — `.tmp/kel_out2/`, linter `6343dcc`; copy over
  the old file under the same name: the cache bumps 21/78 re-lay it, the progress stays). The linter `6343dcc` (local,
  push with the 1.1.4 README after the owner's proofreading).
  **Done 2026-11-18 10:33 +03:00 (firmware, local, not pushed — П3):** idea 11 `b493939b` + `fb217e8d` — Settings / File Transfer /
  Library in the shade (off by default, Home's goTo* and glyphs; at most 8 buttons on, the ninth refused with «Достигнут
  лимит кнопок в шторке» [OK] — `[OWNER]` 10:10; no replace while Wi-Fi is on; HALF over the gray viewer); version names
  by П5 `253d5712` (`cp-…-kccp-…`, `-debug2`, mama `cp-…-kccpm-…`); idea 12 `357f2101` — «Канал обновлений: KCCP /
  CrossPoint» in Settings → System, KCCP releases by default (`researches/2026-11-18_idea12_update_channel.md`).
  Simulator runs `qa_runs/i11_*`, `i12_setting` (no report yet — write it with the debug2 smoke).
  **OTA test release — `AUTH: [OWNER] 2026-11-18 10:34 · chat: «разрешаю собрать и опубликовать тестовый релиз для
  тестирования обновления из GH по боевому пути»`:** tag `kccp-1.1.4-test1`, marked latest (the device reads
  `releases/latest`), one asset `cp-2.0.0-kccp-1.1.4-test1.bin` from env `x4pro-krinik-otatest` (`78d89fcd`), notes
  `docs/releases/kccp-1.1.4-test1.md`; the owner installs debug2 from SD, then «Проверить обновление» on the KCCP
  channel. Gate: the judge over `253d5712`/`357f2101`/`78d89fcd` (running 2026-11-18 10:36 +03:00), then the smoke, then both images.
  The second judge over `fb217e8d` came back VERIFIED WITH CAVEATS — MAJOR 1 fixed in `78d89fcd`; its minors are open:
  the dialog drawn over a stale frame (ToggleRowsActivity render), the Wi-Fi guard after the DRM-loan time sync,
  `canTurnOn` without a host test, «Up to 8 rows» comment, the 10-row screen never run (Bluetooth hidden on the simulator).
  **The chat closed on the owner's word** `[OWNER] 2026-11-18 10:41 · chat: «пока этот чат закрывать. Сразу после твоего
  суб-агента, без судейства»` — the closing judge pass is a debt; the test release was NOT built or published yet.
  **The idea 12 judge (10:43): GO with conditions** — the trace debug2 → `kccp-1.1.4-test1` works (sizes, JSON key order,
  board tag, `build_unflags` all checked). Before publishing: **MAJOR** — a reader on test1 is never offered the real
  `kccp-1.1.4` (`KccpVersion.h` drops the tag's suffix, only `-debug` counts as pre-release): count any suffix after the
  KCCP version («-test1», «-debugN») as pre-release and add host cases (tags `-test1` / final × images debug2 / test1 /
  release) — or tell the owner the way back from test1 is an SD flash; minors: the parser test sets the suffix before the
  feed (OtaUpdater sets it mid-stream), `x4pro-krinik-otatest` replaces base's `build_unflags` (take
  `${env:x4pro-krinik-debug.build_unflags}` + the version line; check the image's strings), «Нет обновлений» cannot tell
  «no asset» from «not newer» at LOG_LEVEL 1, the notes must say plainly it is a debug-env test build. Conditions: same
  commit for debug2 and test1 after a smoke; control — debug2 against `kccp-1.1.3` Latest shows «Нет обновлений»;
  publish non-draft, NOT prerelease; `gh api …/releases/latest --jq '.tag_name,.assets[].name'` must print the test tag and
  asset; Latest put right after the test only on the owner's word.
  **Next, in order:** (1) the idea 12 judge's MAJOR and minors above, then (2) the debug2 image `cp-2.0.0-kccp-1.1.4-debug2.bin` after a smoke of the same commit (the mama image only for
  the release, П5); (3) the owner's two answers asked 2026-11-18 ≈ 10:25 in chat — idea 11: Back from Settings/Library/
  Transfer opened over a book goes Home (A, as now) or back to the book (B); idea 12: a warning before the CrossPoint
  channel installs upstream (B recommended); (4) GEB proofreading below; (5) the README of the three projects; (6) the
  release on the owner's word (both release images, no debug — П5).
- **GEB proofreading (Krinik EPUB Linter)** — `[OWNER] 2026-11-18 10:10 · chat: «опечаток я много видел в книге, кстати. В
  основном - неверные формы слов, неверное согласование падежей, склонений и вот таких особенностий русского языка»`:
  run the linter's `proofread` (built-in checks + local LanguageTool, needs Java 17+ — probe) on the owner's GEB copy,
  review the report, apply the reviewed fixes with `textfix --apply` (logged); the book then goes to the card with the
  1.1.4 image. **Ran 2026-11-18 10:33 +03:00:** Java 21 found, LanguageTool 6.8 in `epub-linter/.venv/languagetool` (`LTP_PATH`); 7 528
  paragraphs, 1 950 remarks (spelling 953 — mostly names and terms, punctuation 381, grammar 155, typos 86) —
  `.tmp/geb_proof/`; the reviewer agent kept 42 real errors of 241 grammar/typo hits (`.tmp/geb_proof/fixes_grammar_typos.json`,
  every decision in `review_notes.md`; ~4 of 5 hits were false — formal systems, notation, style); read one by one and
  applied 2026-11-18 10:36 +03:00: `textfix --apply` 42 applied / 0 skipped, `check` clean, 68 XML well-formed. **The book for the
  owner's card:** `.tmp/kel_out3/Дуглас Хофштадтер. Гёдель, Эшер, Бах. Эта бесконечная гирлянда.epub` (153 captions
  bound + 42 fixes, log beside it). Left: 7 doubtful, the OCR letter mix-ups inside the TNT formulas (invisible on the
  reader), spelling (953) and punctuation (381) not reviewed.
- **Epic 16 «FB2 → EPUB converter» — the owner's word 2026-11-18 09:45** (`ideas/04`, verbatim): PC prototype first (a
  hybrid of the best open converters + Krinik EPUB Linter, custom error handling), tested on the simulator (09:46); the
  device only after the full extended simulator testing, positive and negative (09:46); then a seamless open on the reader
  (a converter screen with a progress bar and percent, the EPUB clone beside the FB2) and a «Настройки конвертора»
  section with few options. Research `researches/2026-11-18_fb2_to_epub3_converters.md`; meta-plan
  `plans/16_EPIC_fb2_converter.md`.
- **DEBT — the 1.1.3 release judge pass** (`/fable-judge` over the published `kccp-1.1.3` notes and the README 1.1.3
  rows: every claim against firmware `c1c38089` vs `198d385e`, the Known list, EN = RU) — skipped on the owner's word
  `[OWNER] 2026-11-17 22:00 · chat: «судью отзывай, нет на него времени» · «судейство - наш долг на потом»`; a refuted
  claim is corrected where it stands (the release body via `gh release edit`, the README). Also not done before the
  release: the full 1.1.3 regression pass on the simulator (features were run phase by phase) and the owner's
  proofreading of the README and the notes.

- **Moved 2026-11-18 (STATUS trim 8):** the 1.1.3 release record, the 2026-11-17 handovers and the epic 07 line →
  `PROJECT_HISTORY.md` → «STATUS trim 8». The 1.1.3 release: tag `kccp-1.1.3` (Latest), image
  `firmware-builds/cp-2.0.0-krinik-1.1.3.bin`, notes `docs/releases/kccp-1.1.3.md`.
- **Bug 08** (the shade's night button leaves pictures under the sheet negative, `bugs/08_…`): upstream issue
  #4515 opened 2026-11-17 10:24 +03:00 — `[OWNER] 2026-11-17 10:21 «Пофиксить бы, в будущем. Пока как баг заведи и нам
  и в апстрим»` (`bugs/08_…`); watch it, the fix waits for its answer.
- **❓ homework 09** (`homeworks/09_guide_settings_proofread.md`): the page did not work for the owner (21:49 «Кратко
  блять и тезисно»); the four lines and three A/B questions went to him in chat 21:51 as theses — his answer awaited.
- **❓ awaiting the owner (one action):** wire the guard `tools/hooks/pretool-deny-server-timeout.mjs` (refuses
  `timeout … review.mjs` page launches — the contour server died that way twice, EXP-0013/0024) into
  `.claude/settings.json` → `hooks.PreToolUse`, matcher `Bash|PowerShell` (the exact block is in the script's header);
  the agent's hook writes are refused by the auto-mode classifier.
- **Open work, in order:**
  1. Epic 05 (idea 06) Ф1–Ф5 done on the simulator; epic 01 Ф4 and epic 05 Ф6 on the owner's word about the image (13.11 19:01 «со сборкой не торопись»); 2. Idea 09 — built
     `9027b99a`, comes with the image; 3. Epic 07 (idea 03, `plans/07_EPIC_figure_caption.md`) after epic 05; 4. KCCP 1.1.3
     assembly: merge release 1.1.2 (`198d385e`) into the debug line (conflicts `lib/hal/HalFrontlight.{cpp,h}`,
     `test/frontlight_dither/`); the owner's open choice: light-linger hold (400 ms) vs timer-redraw hold; 5. Idea 04
     (epic). 6. Bug 01 PR `pr/library-tab-fit` — a free upstream slot (5/5) + proofreading. 7. `bugs/05`, `bugs/06`.
     8. The test hook does not see `tools/sim_run.sh` / ctest runs: a `testHook` block in `.kaif/kaif.json` — to be asked.
     9. Idea 08 S6: the on-device guide `guide_settings_section.xhtml` (the nine sleep options now under «Настройки сна»).
        Read 2026-11-17 15:02 +03:00: wider than S6 — the guide's «Настройки: Экран» is one flat list (file last changed `7a52b12`,
        2026-11-08 14:05); the
        sub-screens «Настройки сна», «Настройки очисток экрана», «Калибровка экрана», «Кнопки в шторке», «Кнопки
        домашнего экрана» are missing → `plans/15_guide_settings_for_1_1_3.md` (the screens captured on the simulator;
        corrected 2026-11-17 15:45 +03:00: the epub's guide is the NEWER text, the separate file the older one; the G4 draft reverted,
        G4 restarts from the epub; no build tool for the epub).
     10. Proofread `GOAL.md`. 11. Delete the partial `C:\msys64` (check the machine lock).
  - Reviews to read: simulator PR #62 and firmware PRs #4328 #4332 #4375 #4376 #4377
    (`gh api repos/<owner>/<repo>/pulls/<n>/comments --jq '.[]|select(.created_at>"<last read>")'`). Checked 2026-11-17 16:08 +03:00:
    all six OPEN, no activity after 2026-11-09 (the last entries are CI bots, CodeRabbit and the owner's own).

## Language contract

- Documents the agent reads (this file, plans, researches, code comments, commit messages) — **English**.
- Every word to the owner — chat, questions, reports — **Russian**.
- Interviews for the owner and owner-facing documents — **Russian**.
- Files under `legacy/` and older `researches/`, `interviews/`, `qa_runs/` notes are Russian; they are an archive, translate only
  what an active task needs.

## Task 0 — moved

The «START HERE — Task 0» checklist moved verbatim to `PROJECT_HISTORY.md` → «STATUS trim 8»; its open boxes (the KEINKT
clone, the owner's decision on the laptop bulk, retiring `~/Xteink`) wait there.

## Next after Task 0 — rename the firmware krinik → KCCP

Owner, 2026-11-08: the custom firmware is renamed from **krinik** to **KCCP** (Krinik Custom CrossPoint). Docs of this repo
already say KCCP. In the firmware fork it is still krinik:
- [ ] version string `2.0.0-krinik…` → `…-kccp…` (the OTA check compares the CrossPoint part — keep it working), env names
  `x4pro-krinik*` / `simulator_x4_pro_mama`, on-device strings, the fork README, the Russian guide `РУКОВОДСТВО.epub`;
- [ ] next releases and tags as `kccp-<version>`; released `krinik-*` tags, branch names and image file names stay as history;
- [ ] build, host tests, simulator, then the owner checks on the reader before any release.

## Carry-over backlog — moved

The 2026-11-08 laptop backlog moved verbatim to `PROJECT_HISTORY.md` → STATUS trim 7 (its device items shipped in 1.1.3).
Live from it: upstream PRs #4328 #4332 #4375 #4376 #4377 open (five per author, never closed to free a slot); 04
`pr/screen-clean-return` waits for a slot; 11–14 and two `lib/hal/` issue drafts wait for the owner's proofreading —
`qa_runs/prs-2026-11-06/queue.json`, `qa_runs/prs-2026-11-07-batch2/`.

## Code map — where the code lives

**Rule (owner, 2026-11-08):** the fork `MikalaiKryvusha/crosspoint-reader` exists only to send pull requests to upstream `develop` — keep it
clean. KCCP releases live in **this repo** (all of them: `kccp-1.1.2` and the historical `krinik-*` / `v2.0.0-krinik.1`).
- The 1.1.3 firmware source: `[OWNER] 2026-11-17 21:59 · chat: «у нас есть KCCP проект в гите»` (asked where to publish
  it) → the firmware and SDK source archives are attached to the `kccp-1.1.3` release of THIS repo; the fork untouched.
  `[OWNER] 2026-11-17 21:59 · chat: «форк оригинального кроспоинта нам ТОЛЬКО ДЛЯ ПОДГОТОВКИ АПСТРИМ ПР И ВСЁ»` → the
  decision below is taken: the KCCP firmware branches move into the KCCP project (how — a task for the next chat).
- [ ] Owner decision (Russian interview on the PC): where the KCCP firmware branches (`nikolai`, `release/*`, `wip/*`, `pr-assets`) live
  instead of the fork, then move them and leave the fork with `develop` and `pr/*` only.

The firmware code is not in this repo; it is in the owner's public forks.

| What | Repo · branch | HEAD |
|---|---|---|
| KCCP 1.1.4 (in work) = release 1.1.3 + bugs 14, 15 (`d727eeef`) + version 1.1.4-debug1 (`21671e33`, image 2026-11-18 09:44) + idea 11 (`b493939b`, `fb217e8d`) + П5 names / debug2 (`253d5712`) + idea 12 (`357f2101`) — local, not pushed | crosspoint-reader · `wip/kccp-1.1.4` | 357f2101 |
| Krinik EPUB Linter (sub-project, clone `epub-linter/`) = 1.0.0 + the figure captions (`krinik_figures.py`, 1.1.0; `8ef77a9`, the judge fixes `6343dcc`) — local, not pushed | `MikalaiKryvusha/Krinik-EPUB-Linter` · `main` | 6343dcc |
| 1.1.3-debug2 (in work) = debug1 + epic 01 Ф2 «Кнопки в шторке» (`41718c61`) + LF fix (`376bcf11`) + Ф3 the shade (`261e5c63`) + idea 09 the viewer opens by shape (`9027b99a`) + epic 05 Ф1 the Home button model (`be6e9a16`) + Ф2 Home draws the model (`f9ae704b`) + Ф3 the button list scrolls (`a47582b0`) + Ф4 «Кнопки домашнего экрана» on the shared rows screen (`2fa20f3f`) + comment fixes (`5da8f37f`) + bug 07 the Cover Grid polarity (port of upstream `b9c23473`, `07df1501`) + the mama row «Для Мамы» on the Home buttons screen (`da382c2f`, interview #006) + epic 07 Ф1 figure keep-together (`869a5bd3`) + version 1.1.3-debug3 (`0d56b23a`) — local, not pushed; image `cp-2.0.0-krinik-1.1.3-debug3.bin` 2026-11-17 11:29 + epic 07 Ф2 caption (`90406599`, after the image) + epic 05 Ф5 the long tap on a Home button (`de8feb20`) + bug 09 span footnote targets (`df4fab1a`) + bug 11 note backlink (`87b8ead1`) + version 1.1.3-debug4 (`3e223b4d`) — image `cp-2.0.0-krinik-1.1.3-debug4.bin` 2026-11-17 20:32 + bugs 12/13 the shade (`3db21be8`) + version 1.1.3-debug5 (`e4afb337`) — image `cp-2.0.0-krinik-1.1.3-debug5.bin` 2026-11-17 21:24 | crosspoint-reader · `wip/kccp-1.1.3-debug2` | e4afb337 |
| 1.1.3-debug1 = debug10 + release 1.1.2 merged (`c6998e86`) + version 1.1.3 / `-debug1` + «Точная температура» ≤ 9 % (`d56b53e9`) + the dither test fix (`84c33f85`) + the remote-button test stub fix (`bcbd6dab`, red since debug10 `8538f3dd`) — local, not pushed; two judges passed; host suite 773/781 = the 8 known (`sh tools/host_tests.sh`, 19:22); NO image (the owner 19:01: not needed yet) | crosspoint-reader · `wip/kccp-1.1.3-debug1` | bcbd6dab |
| debug10 = debug9 + ideas 07 (rotation, touch by the picture, keys), 08 (sleep settings) + epic 01 Ф1 — local, not pushed, no image | crosspoint-reader · `wip/krinik-debug10` | ed5e2f0d |
| debug9 = debug8 + idea 02 (picture tap → full screen), battery log off — local, not pushed | crosspoint-reader · `wip/krinik-debug9` | 35dc070c |
| simulator fix: a plain refresh ends the absolute gray mode (bugs/06) — local, not pushed | crosspoint-simulator · `fix/gray-absolute-reset` (from `windows` = PR #62) | 49ded1a |
| debug2–5 work (was uncommitted on top of `nikolai-debug`) | `MikalaiKryvusha/crosspoint-reader` · `wip/krinik-debug5` | 78cfbf36 |
| its SDK delta | `MikalaiKryvusha/freeink-sdk` · `wip/krinik-debug5` | 548b401 |
| base of the debug line (1.1.1-debug) | crosspoint-reader · `nikolai-debug` | 2ccdbe38 |
| KCCP 1.1.2 release (tag `kccp-1.1.2`) | crosspoint-reader · `release/krinik-1.1.2` | 198d385e |
| krinik stable | crosspoint-reader · `nikolai` | a06a20d6 |
| Home flashlight, uncommitted worktree state | crosspoint-reader · `wip/home-flashlight` (on top of `pr/home-flashlight`) | 98ec9cab |
| SDK release line | freeink-sdk · `krinik-1.1.2` | 40ce5c3 |
| PR branches | crosspoint-reader · `pr/*` (table above) | — |
| PR images (raw links in PR bodies) | crosspoint-reader · `pr-assets` | f5c4082 |
| calibration tool | `MikalaiKryvusha/KEINKT` · `main` | a176601 |
| UI test runner dependency | `MikalaiKryvusha/KUIPS` v1.3.0 (`kuips-runner/package.json`) | — |

## What is in this repo

The tree and each part's role: `PROJECT_STRUCTURE_EXTERNAL_MAP.md` (the old list moved to `PROJECT_HISTORY.md`, «STATUS
trim 5»).
