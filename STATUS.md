# STATUS — Krinik Custom CrossPoint (KCCP)

Updated 2026-11-20 17:18 +03:00 (the 17:03 chat: idea 14 merged into 1.1.4, image debug3 built). Licence: MIT (owner, 2026-11-08: «как у оригинального CP, или MIT»); fonts OFL, firmware images GPLv3.
 Moved off the owner's laptop, where it lived as a loose folder (`~/Xteink`) beside an unrelated
work project. From now on it is a standalone project.

## Where to continue

- **The 2026-11-20 14:14 chat (in work):** `/resume` on the owner's word; the owner's photo from his reader → **idea 14**
  (`ideas/14_viewer_smart_filter_bw_lowres.md`, the owner 14:19 «это не баг, это импрувмент вьювера картинок»): a smart
  filter (auto levels, NOT binarization — it destroys the picture's anti-aliasing, the owner 14:20) for black-and-white
  low-resolution pictures in the viewer; measured: the source (GEB `i_016.jpg`, 36×91) carries JPEG noise, the viewer
  enlarges ×8.8 and the panel curve turns the near-white noise into light gray. Interview #007 status closed (Q1–Q3/Q5 →
  the plan, Q4 waits). EXP-0043: a bug the owner found is never «твой баг» (`[OWNER] 2026-11-20 14:16 · chat: «ПРОЕКТ ТВОЙ!»`).
  **Built:** firmware `5a9e1624` on the local branch `wip/kccp-line-art-filter` (from `wip/kccp-1.1.4` `8a8b44bc`, П3):
  «Настройки → Чтение → Чистить фон чертежей», on by default, page + viewer + file browser, pictures ≤ 480×800 of area; two
  independent reviews applied; simulator run report `testcases/reports/2026-11-20_idea14_smart_filter.md` all pass; host
  suite 1002, no new failure; NO reader image yet. The floor 160 stays (`[AI]` under his 14:20 rule; 16:29 «я утвердил
  вариант»). The scaler: the owner picked N (bicubic + unsharp 3/160/2) for line art only (15:26–15:28); a byte-exact Pillow replica
  in rings — `lib/Epub/Epub/converters/SharpUpscale.h`, host test `test/sharp_upscale` 6/6 byte-exact against Pillow
  goldens; wired into the viewer: firmware `353cb8b5` (same branch, local) — enlarged ≥ ×2 line art ≤ 8192 source px,
  photos keep the bilinear; simulator: the viewer cache vs Pillow N 26/252 800 and 5/239 040 pixels differ (JPEG decoders),
  shown to the owner ≈ 15:58 (`.tmp/bug17/idea14_n_simulator.webp`); report `testcases/reports/2026-11-20_idea14_sharp_upscale.md`;
  host suite 1008, no new failure. NO reader image yet; the reader's N time unmeasured.
- **The repo's GitHub issues #1–#4 (filed 2026-11-11, never tracked in `bugs/` or here)** — checked against the code
  2026-11-20 15:39 +03:00 on the owner's question «из этого мы всё починили?»: #1 (Library duplicates / stale book cache after
  USB Drive) not fixed — `UsbDriveActivity::onExit` marks nothing, the EPUB cache is keyed by path only; #2 (`text-align:
  inherit` → left) not fixed — `CssParser::interpretAlignment` falls to `Left`; #3 (`text-indent: 0` ignored) partly — 1.1.4
  bug 15 keeps the indent off headings, body paragraphs with `text-indent: 0` still get it; #4 (SVG cover small) not fixed —
  the «never enlarge» clamp at `ChapterHtmlSlimParser.cpp` ≈ 1893. Release: 1.1.5 — `[OWNER] 2026-11-20 16:11 +03:00 ·
  chat: «4 в 1.1.5»`.
- **Idea 14 — next, in order** (the owner's words 16:30–16:52, idea 14 «N by content, not by scale»):
  1. BMP in the full-screen viewer gets the filter and N too — `[OWNER] 2026-11-20 16:30 · chat: «нет, чистим всё в
     полноэкранном вьювере. Это работа с рендером изображения во вьювере»` (`BmpToBmpConverter`, `Bitmap::readRowGray`).
  2. N by content: text and diagrams → N, drawings with hatching → the bilinear — `[OWNER] 2026-11-20 16:52 · chat: «1
     справа луче, так как это рисунок, не чертеж · 2 слева лучше, так как это текста · 3 слева лучше, так как мелкие
     текста»`; a third detector class (recon → GEB mock-up → his eye); the `[AI]` ×2 minimum goes.
  3. N for big sources: stream the source rows from the decoder (the 8192-px whole-source limit drops `i_056`, `i_078`).
  4. The release: the filter + N go into **1.1.4** — `[OWNER] 2026-11-20 16:59 +03:00 · chat: «фильтры давай в 1.1.3,
     сейчас новый чат открою»` → «1.1.4» (corrected the same minute). **Done 2026-11-20 17:18 +03:00 up to the card:**
     `wip/kccp-1.1.4` fast-forwarded to `f06f8850`, version `-debug3` `fc97043d` (the otatest unflag follows); host suite
     1008, no new failure; smoke of `fc97043d` on his settings and GEB (boot → book → toolbar → shade → Home, 9 known TTF
     `[ERR]`) and the viewer (filter + N, photo untouched, control off) — `testcases/reports/2026-11-20_kccp114_debug3.md`;
     image `firmware-builds/cp-2.0.0-kccp-1.1.4-debug3.bin` (SHA256 `5b13f6dc…`, 83.3 % of app0). **On his card**
     `/.firmware/` 2026-11-20 17:24 +03:00 (the card's copy hashed equal), the reader ejected; he installs it. The card also holds
     debug2, 1.1.3 and 1.1.2 (not removed: its earlier removal was refused by the auto-mode classifier). No new
     `/screenshots/` since 12:16. The stands' `settings.json` (`.tmp/b14_sd`, `.tmp/b17_geb_on`) refreshed from his card
     (14:31: `statusBarGap` 12, `updateChannel` 0, the 1.1.4 shade list). **The push of this repo was refused by the
     auto-mode classifier at 17:19** — local commits wait for his word. Points 1–3 next — the owner's order.
- **⚠️ Force-closed 2026-11-20 17:00 +03:00** (the owner 16:59 «сейчас новый чат открою»): ceremonies skipped (judge
  pass, bonsai trim, README, showcase linters) — the first `/end-chat-soft` pays this debt. Standing falsehood: none.
  KNOWLEDGE: the line-art filter and Pillow's N (`LineArtFilter.h`, `SharpUpscale.h`, the map); the simulator build needs
  UCRT64 on PATH (HOUSE_RULES); Pillow's unsharp threshold is strict (idea 14); EXP-0043 (never «твой баг»; questions in
  the owner's terms); the four GitHub issues #1–#4 now tracked here (1.1.5). Firmware branch `wip/kccp-line-art-filter`
  is local (П3), not pushed.
- **Handover — the 2026-11-20 09:38 chat closed 2026-11-20 12:19 +03:00** on the owner's word `[OWNER] 2026-11-20 12:15 · chat: «и пора закрывать
  чат»`; its full blocks moved verbatim to `PROJECT_HISTORY.md` → «STATUS trim 9». Firmware `wip/kccp-1.1.4` HEAD `8a8b44bc`
  (local, П3) = 1.1.3 + bugs 14/15 + ideas 11/12 + the version order (`b2b92ef5`) + toolbar lists variant 2 and the night
  circle (`48d7d52c`) + bug 16 the status-bar gap squeeze (`7173e6bd`, default 12 `8a8b44bc`). Image
  `firmware-builds/cp-2.0.0-kccp-1.1.4-debug2.bin` (SHA256 `f4e4937e…`) built from `8a8b44bc` after a smoke of the same
  commit (`.tmp/ui_mock_2026-11-20/d114_2_smoke`, parked: Boot → book → toolbar → shade → Home, 9 known TTF `[ERR]`), copied to the owner's card
  `/.firmware/` 2026-11-20 12:16 +03:00, the reader ejected; he installs it. The card still holds `cp-2.0.0-krinik-1.1.2.bin` (its
  removal was refused by the auto-mode classifier) and 1.1.3. The owner asked what to check on the device (12:16) — the list
  went to chat: install, the page bottom, headings, the toolbar lists under a finger, the shade circle and buttons,
  «Настройки → Чтение → Отступ над строкой состояния» 12. Simulator branch `fix/x4pro-viewable-insets` `190cff0` (local).
  **Next, in order:**
  1. The owner's device feedback on debug2 — read his card's `/screenshots/` when the reader is on the wire (HOUSE_RULES П4).
  2. Interview #007 answers (`5685f78`) → a plan (`/plan-epic`: build system, i18n, hyphenation, fonts, П5 names):
     language-variant builds — `interview #007 Q1: «можно пересобрать разные варианты сборки, типа RU, EN, PT, DE и так
     далее? Мне с мамой хватило бы _RU_EN»`, Q2 the same for hyphenation; Q3 one light built-in font, the full fonts
     (Literata and the approved ones) as an SD-card folder; Q4 Bluetooth — he asked «что это вообще такое???», answered in
     chat (a wireless page-turner; he switched its button off) — removal waits for his word; Q5 keep OPDS, plugins, KOReader,
     LCP. The numbers: `reports/2026-11-20_crosspoint_flash_budget.md` (upstream; the KCCP debug2 image is 83.2 % of app0, PlatformIO counts 83.1 %).
  3. The OTA test release `kccp-1.1.4-test1` (`AUTH: [OWNER] 2026-11-18 10:34 · chat: «разрешаю собрать и опубликовать
     тестовый релиз для тестирования обновления из GH по боевому пути»`): the judge's MAJOR is fixed (`b2b92ef5`); build env
     `x4pro-krinik-otatest` from the SAME commit as debug2 (`8a8b44bc`), smoke, publish non-prerelease Latest, check
     `gh api …/releases/latest`; a pre-release as Latest is offered to every older KCCP-channel reader (the mother's too) —
     put the release back right after, on his word. Notes `docs/releases/kccp-1.1.4-test1.md`.
  4. Still open from 2026-11-18 (moved blocks): his two answers — idea 11: Back from Settings/Library/Transfer opened over a
     book goes Home (A, as now) or to the book (B); idea 12: a warning before the CrossPoint channel installs upstream (B
     recommended); the GEB proofreading leftovers (spelling 953, punctuation 381 unreviewed); the README linking the three
     projects; the linter's GEB `.tmp/kel_out3/…epub` to the card (not copied yet; 1.1.4's cache bump re-lays it).
  5. Upstream issue #4515: the reply posted 2026-11-20 12:10 +03:00 (`#issuecomment-7035293194`) on `interview #007 Q6: A`;
     watch `AlmostGivingUp`'s answer.
  KNOWLEDGE: the simulator's X4 Pro insets = the device's (EXP-0041, HOUSE_RULES stand row, simulator `190cff0`); font
  metrics are not ink (EXP-0042, `Page.cpp`); a build in another worktree blocks nothing (EXP-0040, AGENT_GUIDE Build);
  HOUSE_RULES П5 item 6 (the pre-release order); `tools/shot_rows.py`; `shot_diff … 32` in landscape (HOUSE_RULES); the
  internal map (ReaderToolbarUi, Page.{h,cpp}, the squeeze); the flash report.

- **The closing judge of the 2026-11-20 chat** (the owner 12:21 «нет времени на судейство»; it had already run, finished
  12:22): VERIFIED WITH CAVEATS — no false claim of substance; fixed at once: the smoke path (parked), 83.2 % of app0 (not
  83.1), the bug 16 report's stale «default waits»; open: the flash report's block rows sum to 1 B less than its total.
- **DEBT — the closing judge pass of the 2026-11-18 08:44 chat** was skipped on the owner's word `[OWNER] 2026-11-18 10:41 ·
  chat: «пока этот чат закрывать. Сразу после твоего суб-агента, без судейства»` — the next `/end-chat-soft` runs
  `/fable-judge` over this chat's claims (the 1.1.4 block below, the two run reports of 2026-11-18, the linter `6343dcc`).
  KNOWLEDGE (this chat): HOUSE_RULES П4 (reading tests on the owner's settings and book) and П5 (image names, release
  content); the stand row «Книга Николая на его настройках» and `tools/sim_pages.sh`, `tools/park_runs.sh`,
  `tools/kel_tests.sh`, `TARGETS=` of `tools/host_tests.sh`; EXPERIENCE 0037–0039; the maps (BlockStyle heading keep, the
  shade model, `epub-linter/`); researches on FB2 converters and the update channel; ideas 11–13.

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
| KCCP 1.1.4 (in work) = release 1.1.3 + bugs 14, 15 (`d727eeef`) + version 1.1.4-debug1 (`21671e33`, image 2026-11-18 09:44) + idea 11 (`b493939b`, `fb217e8d`) + П5 names / debug2 (`253d5712`) + idea 12 (`357f2101`) + the otatest env (`78d89fcd`) + the version order (`b2b92ef5`) + lists variant 2 and the night circle (`48d7d52c`) + bug 16 the status-bar gap (`7173e6bd`, default 12 `8a8b44bc`) + idea 14 the line-art filter and N (`5a9e1624`, `353cb8b5`, `f06f8850`) + version debug3 (`fc97043d`, image 2026-11-20 17:16) — local, not pushed | crosspoint-reader · `wip/kccp-1.1.4` | fc97043d |
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
