# Krinik Custom CrossPoint — Project History (the chronicle)

> The APPEND-ONLY chronicle of how this project lived and grew: closed sessions, shipped phases,
> releases, big decisions in the order they happened. This is where `STATUS.md` sheds its past —
> STATUS stays a short live summary of NOW; everything finished moves HERE (the "bonsai trim" step
> of `/end-chat-soft`).
>
> **Not required reading.** This file is NOT part of `/resume`'s canon set and not in the
> before-every-task minimum — open it only when you actually need the archaeology: how a decision
> came to be, what an old phase contained, when something shipped.
>
> **Chronicle rules (ADR discipline):**
> - **Append-only, newest on top.** A recorded entry is never edited to say something else —
>   history that can be rewritten is not history. Corrections come as NEW entries that reference
>   and supersede the old one.
> - An entry moves here VERBATIM from `STATUS.md` when its work closes — move, don't rewrite;
>   the entry already carries its dates, counters and file pointers.
> - Entries mention versions and dates freely — a chronicle legitimately speaks of old versions,
>   and the update machinery's stale-claims scan knows to leave this file alone.
> - When the file grows unwieldy, split by era: keep the newest era here, move older ones to
>   `PROJECT_HISTORY_<era>.md` files, and leave a one-line index at the top of this file
>   (the pattern large changelogs use).
>
> Living document — never DONE-tagged.

---

## Entries (newest first)

### 2026-11-18 — STATUS trim 8 (2026-11-18 10:47 +03:00): the 08:44 chat closing (KCCP 1.1.4 in work)

- **Chat 2026-11-18 08:44 → 10:47 closed** on the owner's word 10:41 «пока этот чат закрывать. Сразу после твоего суб-агента, без судейства». Done: bugs 14, 15 DONE (headings), the captions in Krinik EPUB Linter (sub-project `epub-linter/`, 153 GEB captions), idea 11 (shade buttons, cap 8), idea 12 (the update channel), the П5 image names, debug1 image, GEB proofreading (42 fixes), epic 16 planned. Blocks moved from STATUS verbatim:

#### From «Where to continue» — the 1.1.3 release and the 2026-11-17 handover (verbatim)

- **KCCP 1.1.3 RELEASED 2026-11-17 22:04 +03:00** on the owner's word 21:42 «Версию 1.1.3 готовим Релиз и выпускаем
  релиз в GitHub KCCP» · 21:56 «скорее выпускаем релиз и закрываем мягко чат»:
  https://github.com/MikalaiKryvusha/Krinik-Custom-CrossPoint/releases/tag/kccp-1.1.3 (Latest; tag `kccp-1.1.3`, commit
  `0ac2031`). Image `firmware-builds/cp-2.0.0-krinik-1.1.3.bin` (env `x4pro-krinik`, firmware `c1c38089`, SHA256
  `0f958152…`, Flash 83.0 %); assets: the image, `RUKOVODSTVO-krinik.epub` (edition 1.1.2), `SHA256SUMS.txt`, the source
  archives `crosspoint-reader-kccp-1.1.3-src.tar.gz` + `freeink-sdk-kccp-1.1.3-src.tar.gz` (the owner 21:59 «у нас есть
  KCCP проект в гите» — the fork is for upstream PRs only, `HOUSE_RULES.md` П3). Notes kept in
  `docs/releases/kccp-1.1.3.md`. Not looked at in a browser — only the body read back through the API.
- **The handover — do first, in order:**
  1. `node D:/work/ai_sandbox/_tools/machine-lock.mjs status`; `ListAgents`.
  2. The DEBT above: the release judge pass over the published notes and the README 1.1.3 rows; correct what is refuted
     (`gh release edit kccp-1.1.3 --notes-file docs/releases/kccp-1.1.3.md` after fixing the file).
  3. The full 1.1.3 regression pass on the simulator (both builds), its report in `testcases/reports/`.
  4. Move the KCCP firmware branches out of the fork into the KCCP project (the owner 21:59, decision journal) — how is a
     plan to write first; until then `firmware/` `wip/kccp-1.1.3-debug2` stays local, never pushed to the fork.
  5. KCCP 1.1.4: bugs 14 (a lonely heading — `page-break-after: avoid` ignored, `CssParser.cpp:1069`) and 15 (a heading's
     first-line indent — CSS `text-indent: 0` loses to the reader's indent, `ParsedText::resolveFirstLineIndent`), idea
     11 (shade Settings / File Transfer / Library), idea 12 (update channel KCCP / CrossPoint, KCCP by default), plan 14
     the EPUB 2 form A (GEB is EPUB 2), homework 09 asked in chat as theses (the owner's answer awaited).
  KNOWLEDGE: written today into the documents — HOUSE_RULES П2 · П3 · the voice-engine and reader-on-the-wire rows;
  the internal map (anchors and span ids, `progress.bin`, `SimScreenText`); `researches/2026-11-17_shade_row_spacing.md`;
  EXPERIENCE 0032–0036; the simulator X4 Pro profile has 3 px side insets (the reader 7 px) — `tools/shade_gaps.py` header.

#### From «Where to continue» — the older handover list and the epic 07 line (verbatim)

- **Where to continue (the handover):**
  1. `node D:/work/ai_sandbox/_tools/machine-lock.mjs status`; `ListAgents` (shared PC: KUMM, KAGO).
  2. DONE 2026-11-17: interviews #005 and #006 shown and answered (above). **Epic 07 Ф1 DONE on the simulator 11:16**
     (`plans/12_DONE_epic07_p1_layout.md`, report `testcases/reports/2026-11-17_epic07_p1.md`: a `<figure>` /
     `break-inside: avoid` block keeps picture + caption on one page, the picture shrinks; old books unchanged; the parser
     host suite now runs on Windows, 963 host tests). **Ф2 indent + centring DONE 11:42** (firmware `90406599`,
     `testcases/reports/2026-11-17_epic07_p2.md`; after the debug3 image); open P2.4 — the owner's A–D (homework 08).
     **Ф3 tool DONE on the test book** (`f8d213a`, plan 14); open P3.6: the owner's two books when the reader is on the
     wire (`--list` read + census). The owner's books change only after the tool re-typesets them (Ф4 homework).
  3. **Epic 05 Ф5 DONE on the simulator** (`de8feb20`); next Ф6 (acceptance: judge over the epic, image, homework) and
     epic 01 Ф4 — only on the owner's word about the image (13.11 19:01 «со сборкой не торопись»).
  4. The on-device guide (open work 9 below) — rewrite «Настройки: Экран» from `SettingsActivity::sectionFor()`.
  5. Every firmware change: the judge BEFORE the build; `sh tools/host_tests.sh` before the commit (EXP-0018/0019);
     simulator scripts: keys `UP/DOWN/CONFIRM/BACK` (not `NEXT`), fast list swipes `SWIPE:…,60` (`HOUSE_RULES.md`).
- **Epic 07 «подпись всегда с картинкой» (idea 03) — meta-plan `plans/07_EPIC_figure_caption.md` (2026-11-14).**
  Ф1 layout DONE · Ф2 caption look (centring + no indent DONE; italic × size waits for homework 08) · Ф3 the re-typeset
  tool DONE on the test book (the owner's books wait for the reader) · Ф4 acceptance. Interview #005 answered 10:40 (A).

#### «START HERE — Task 0» (verbatim; its open boxes — the KEINKT clone, the left-on-laptop decision, retiring `~/Xteink` — stay open in this record)

## START HERE — Task 0: bring the project up on the owner's PC and deploy KAIF 2.9 + 2.10 WIP

This is the first and only task until it is closed. Do it in order; each step has an exit you can check.

1. **Clone the workspace.**
   - [x] `git clone https://github.com/MikalaiKryvusha/Krinik-Custom-CrossPoint.git` into the owner's chosen folder.
   - [x] Inside it, clone the firmware fork with its SDK submodule (it is ignored by this repo's `.gitignore`):
     `git clone --recurse-submodules https://github.com/MikalaiKryvusha/crosspoint-reader.git firmware`,
     then `git -C firmware remote add upstream https://github.com/crosspoint-reader/crosspoint-reader.git`.
   - [ ] Clone KEINKT beside it if calibration work is planned: `https://github.com/MikalaiKryvusha/KEINKT.git` (separate project,
     its own STATUS).
   - Exit: `git -C firmware branch -r` lists `origin/wip/krinik-debug5` and `origin/release/krinik-1.1.2`.

2. **Restore the toolchain.** The laptop was macOS; the PC may not be — adapt, do not copy paths.
   - [ ] Python 3 + PlatformIO Core (a venv inside the workspace, ignored by git), Node.js ≥ 20, CMake for host tests, `gh` logged in
     as MikalaiKryvusha.
   - [ ] Build check on `wip/krinik-debug5`: `pio run -e x4pro-krinik-debug` → SUCCESS, image ≈ 5.4 MB.
   - [ ] Host tests: configure `firmware/test` with CMake, build, `ctest` (run serially if `ParserStopTest` flakes under `-j`;
     the last laptop run was 936/936).
   - [ ] Simulator: `pio run -e simulator_x4_pro` builds and opens.
   - Exit: the three commands above pass; record versions of PlatformIO, Node, CMake in the closing report.

3. **Deploy KAIF from `main` (2.9 release + 2.10 WIP).**
   - [x] Download the entry file into the workspace root:
     `curl -fsSL https://raw.githubusercontent.com/MikalaiKryvusha/KAIF/main/KAIF.md -o KAIF.md`.
   - [x] Run it with the owner's phrasing: **"Deploy KAIF from KAIF.md, my working language is Russian"** — payload English,
     owner-facing documents Russian, tracking to the origin.
   - [x] Record the exact KAIF commit SHA that was installed (`main` moves daily; 2.10 is unreleased). If the 2.10 WIP installer
     fails, report the failure upstream (KAIF field report, see step 5) and fall back to the `v2.9` tag:
     `https://raw.githubusercontent.com/MikalaiKryvusha/KAIF/v2.9/KAIF.md`.
   - [x] `GOAL.md` comes from the owner, not from the agent: KAIF asks for it after the install — run that as a Russian interview.
   - Exit: `.kaif/kaif.json` exists with the version and origin; the KAIF self-check of the install summary is green.

4. **Adapt the legacy material into the KAIF canon** (KAIF's own adaptation task drives this; the inputs are below).
   - [ ] The backlog below and `legacy/STATUS.ru.md` + the head of `legacy/HANDOVER.ru.md` → the new `STATUS.md` backlog, in English.
   - [ ] `legacy/PROJECT_HISTORY.ru.md` → `PROJECT_HISTORY.md` (archive, may stay Russian, mark it so).
   - [ ] `legacy/README.ru.md` is the device setup guide (`restore.mjs`, fonts, settings) → the owner-facing README section,
     Russian; the agent-facing parts in English.
   - [ ] Lessons scattered in the legacy docs (flaky `ctest -j`, `pio run -e x4pro` wiping the simulator binary, SD-only flashing
     because the reader is eFuse-locked, the 5-open-PR limit upstream) → `EXPERIENCE.md` entries.
   - Exit: no active rule lives only in `legacy/`; `legacy/` is referenced as archive.

5. **Owner decisions — via a Russian interview, never decided by the agent.**
   - [ ] What happens to the private bulk that stayed on the laptop (see "Left on the laptop").
   - [ ] Whether `wip/krinik-debug5` becomes the next krinik release line.
   - KAIF defects found during the install go upstream by KAIF's own field-report route; they contain nothing personal beyond
     what is already public here.

6. **Close Task 0.**
   - [ ] Commit and push; the closing report (Russian) names the KAIF SHA, toolchain versions, build/test results.
   - [ ] Tell the owner the laptop can now clone this repo. `~/Xteink` on the laptop is retired only on the owner's word, after a <!-- attribution-ok: verbatim Task 0 text moved from STATUS in trim 8; written by the 2026-11-08 laptop handover, kept as it stood -->
     by-name check that everything listed in `legacy/left-on-laptop.tsv` is either moved or knowingly dropped.


### 2026-11-17 — STATUS trim 7 (2026-11-17 22:10 +03:00): the 19:45 chat (bugs 09–13, ideas 10–12, debug4, debug5, the KCCP 1.1.3 release), the 14:40 day loop and the items closed by the release (moved verbatim)

- **Chat 2026-11-17 19:45 → 22:10 closed** (full entry: `PROJECT_HISTORY.md` → STATUS trim 7). Done and on the
  simulator: bug 09 span footnote targets (`df4fab1a`), bug 11 note backlink (`87b8ead1`), bug 12 shade row from the
  visible edges + bug 13 shade Sleep pressed (`3db21be8`), idea 10 shade without buttons (`1897783f`), the default shade
  Night · Orientation · Flashlight · Sleep (`c1c38089`); images debug4 and debug5 put on the owner's card. Bug 10 (GEB
  notes lost punctuation) — in the FB2 source, not our tools. New rules: П2 testing is the agent's, never the owner's;
  П3 the fork only for upstream PRs; the voice engine is the shared `D:/work/ai_sandbox/tools/silero_tts`
  (`.claude/settings.local.json`, gitignored).
## Carry-over backlog (state on 2026-11-08, from the laptop)

### Upstream contributions to crosspoint-reader

- Open PRs (all 14/14 checks green on 2026-11-07, all waiting for maintainer review): #4328 `pr/epub-anchor-first-line`,
  #4332 `pr/sleep-image-order`, #4375 `pr/screen-clean-menu`, #4376 `pr/screen-redraw-delay` (depends on #4375),
  #4377 `pr/screen-calibration` (calibration with KEINKT; reconcile overlaps with #4375 when it lands).
- Merged: #4329, #4330, #4331.
- Upstream allows five open PRs per author. Do not close PRs to free a slot.
- Ready locally, waiting for a free slot: **04** `pr/screen-clean-return` (text already proofread by the owner) — send command at
  the end of `qa_runs/prs-2026-11-06/SEND_WHEN_READY.md`.
- Ready, texts waiting for the owner's proofreading: **11** `pr/night-epub-images` (584c04e0), **12** `pr/lyra-title-lines`
  (9d8bd77e), **13** `pr/viewer-reader-controls` (636126c5), **14** `pr/sleep-skip-truncated-bmp` (5977ce1e). Bodies:
  `qa_runs/prs-2026-11-07-batch2/bodies/`; queue: `qa_runs/prs-2026-11-06/queue.json`. Builds and before/after frames were made on
  those HEADs — do not rewrite the branches without a reason.
- Two issue drafts for `lib/hal/` changes (upstream wants agreement first), unpublished, waiting for proofreading:
  `qa_runs/prs-2026-11-07-batch2/issue-frontlight-park-before-sleep.md`, `issue-fat-dates-from-clock.md`.
- Rule: no PR or issue text goes out without the owner's proofreading. Candidate analysis:
  `researches/2026-11-08_krinik_upstream_candidates_batch2.md`.

### Device (Xteink X4 Pro, eFuse-locked: firmware only from the SD card)

- Last build confirmed on the reader: **1.1.1-debug8** (2026-11-09 23:46, homework 03); **debug9** is on the card since
  2026-11-13 11:47, the owner 13:51: picture opening works (homework 04 steps 1, 3); the rest is superseded by the debug10 image. Debug2–8 history: `PROJECT_HISTORY.md`.
- [ ] Precise temperature rework (owner, 2026-11-08): dithering only at brightness **≤ 9 %**, off at **10 %** (now it runs up to the
  duty of 10 %).
- **KCCP 1.1.2** (frontlight) is published: https://github.com/MikalaiKryvusha/Krinik-Custom-CrossPoint/releases/tag/kccp-1.1.2 (2026-11-08,
  bilingual notes, Latest; the image still says `cp-2.0.0-krinik-1.1.2` inside).
- "Mama" build with OPDS/plugins: the Home menu has 8 rows and the "Mama" row runs off the screen — fixed by epic 05 Ф3 (`a47582b0`,
  the list scrolls) on the simulator; the reader check comes with the mama image.

- **Chat 2026-11-17 19:45 — `resume`; the owner's bug 09 + KCCP 1.1.3-debug4.** The owner filed `bugs/09_ssylka.md`
  (GEB footnote links open the notes chapter's page 0) and put the reader on the wire (H:, KCCP 1.1.1-debug9): the
  book, its caches and card state copied read-only to `.tmp/bug09/` (no log file, no serial port). Cause found and
  fixed in the firmware (uncommitted at writing): `<span id>` footnote targets were dropped by upstream #2303's filter
  (upstream #3667 open). His GEB screenshots of 13.11 (ch8 p57/p58): `[OWNER] 2026-11-17 19:48 «на одном снимке нет
  подписи картинки» · «на втором - она переехала на новую страницу и там абзац, который не нужен подписям картинок»` —
  epic 07's case; GEB needs the Ф3 tool's re-typeset (plain `<p>` captions), T9 of plan 14 runs on this copy. His
  question 19:50 «мы близки к тому чтобы собрать очередную дебаг сборку…?» → answered: **debug4 = debug3 + epic 07
  Ф2 + epic 05 Ф5 + bug 09 + bug 11** (his 20:01 «ТОЧНО ЛИ НУЖНО ДЕЛАТЬ ССЫЛКИ В ПРИМЕЧАНИЯХ ПОЛНОЦЕННЫМИ???» →
  `bugs/11_note_backlink_grows_jump_stack.md`: a note's backlink now closes the jump). **Image
  `firmware-builds/cp-2.0.0-krinik-1.1.3-debug4.bin` built 2026-11-17 20:32 +03:00** (firmware `3e223b4d`, 5 446 624 B,
  SHA256 `e38a9338…`, RAM 34.3 %, Flash 83.0 %), the same commit's smoke clean (`testcases/reports/
  2026-11-17_bug09_bug11_debug4.md`). **On the card 2026-11-17 20:43 +03:00** (the owner 20:42 «на проводе»):
  `/.firmware/` = debug4 (SHA256 on the card = `e38a9338…`) + debug9 (fallback) + 1.1.2; debug8 removed (its copy in
  `firmware-builds/`); ejected, `Test-Path H:\` False. **the owner flashes it for his own use** (the checklist I gave was wrong — testing is mine, `HOUSE_RULES.md` П2) — given in
  chat (GEB [4] [5] [6] → their notes; a note's «[N]» → back to the text; captions in GEB unchanged until the
  re-typeset); a homework document for debug4 is not written yet (supersedes homework 07). The punctuation part of his report → `bugs/10_geb_notes_lost_punctuation.md`: the
  owner 20:47 gave the originals on D: — the notes lost their punctuation IN THE FB2 SOURCE (2010), our tools made 27
  corrections and lost nothing; open: a punctuation check for books, the book itself only from another edition.
  **His debug4 test, two shade bugs:** `bugs/12_shade_row_gaps.md` (20:51: huge ends, tight gaps — the row was spaced
  inside the sliders' 16 px inset; research `researches/2026-11-17_shade_row_spacing.md` on his order; guard
  `shade_gaps.py` now measures from the sheet's edge, red on debug4) and `bugs/13_shade_sleep_no_highlight.md` (20:53:
  «Сон» in the shade not shown pressed before sleep — Home's debug8 fix ported). Both fixed (`3db21be8`, three judge
  rounds), seen working on the simulator; **image `firmware-builds/cp-2.0.0-krinik-1.1.3-debug5.bin` built 2026-11-17
  21:24 +03:00** (firmware `e4afb337`, 5 446 704 B, SHA256 `554f811a…`), the same commit's smoke clean
  (`testcases/reports/2026-11-17_bug12_bug13_debug5.md`). **On the card 2026-11-17 21:27 +03:00** (the owner 21:27
  «на проводе»): `/.firmware/` = debug5 (SHA256 on the card = `554f811a…`) + debug4 (fallback) + 1.1.2; debug9 removed
  (its copy in `firmware-builds/`); ejected, `Test-Path H:\` False. **The owner flashes debug5 for his own use; the tests are mine** (П2: the 1.1.3 regression pass on the simulator, both builds, is not done yet). The voice
  call said his name twice («Mikalai, Николай, …» since at least 16:10) — the owner 21:26 «Почему НИКОЛАЙ НИКОЛАЙ???» ·
  «Нахуя два раза имя произносить???»: the door adds `callName` (default: git's «Mikalai») and the phrase opened with
  «Николай»; fixed `.kaif/kaif.json` → `contour.callName = «Николай»` (the door then drops a leading «Николай,»; dry run
  checked). Next: GEB re-typeset (plan 14 T9, the EPUB 2 form A). Homework 09 not raised.
- **Chat 2026-11-17 14:40 — DAY LOOP** on the owner's word 14:42 «работай автономно в дейлупк» (`/dayloop`, no end time
  named). Done: homework 08 — the clean §7B pass applied, committed `e7d5119`, the mock-up page shown (window on the
  screen, screenshot ≈ 14:50; the owner's letter A–D awaited there); the contour's decision-name collision guarded and
  filed (`b171cd6`, KAIF #199, EXP-0028); **epic 07 Ф3 tool** `tools/figure_retypeset.py` (`f8d213a`, plan 14, report
  `testcases/reports/2026-11-17_epic07_p3.md`: the test book pass, the judge's loose-label finding fixed; T9 the owner's
  two books blocked — the reader not on the wire); **epic 05 Ф5 DONE on the simulator** — firmware `de8feb20` (local),
  `plans/11_DONE_epic05_p5_home_long_tap.md`, report `testcases/reports/2026-11-17_epic05_p5.md` (five themes + mama; the
  judge's FIX FIRST — the grid's bottom-edge band — fixed and proven red on a mutant); EXP-0029 (CRLF again).
- **KCCP 1.1.3-debug3 image built 2026-11-17 11:29** on the owner's word 11:21 «сделаешь мне дебаг3? накопилось фичей и
  фиксов на неё?»: `firmware-builds/cp-2.0.0-krinik-1.1.3-debug3.bin` (5 445 104 B, SHA256 `4774fee2…`), firmware
  `0d56b23a` (debug2 line + version bump; epic 07 Ф2 parked in `git stash` «epic07-p2-caption-wip» — its judge said FIX
  FIRST: the caption inherits the figure's alignment, a nested `<p>` gets the indent, the test cannot fail on the indent);
  simulator smoke of the same commit 0 errors (`qa_runs/debug3_smoke_home`, `…_book`); RAM 34.3 %, Flash 83.0 %.
  **superseded by debug4** (the reader came on the wire 2026-11-17 19:46 as H:; debug4 goes instead): copy to `/.firmware/`, check SHA256,
  eject; homework `homeworks/07_kccp_1.1.3_debug3.md`. This is the image of epic 01 Ф4 and epic 05 Ф6 (acceptance: the
  agent's own test pass — `HOUSE_RULES.md` П2, never the owner's check).
- **Homework 08 — the caption look ANSWERED** 2026-11-17 16:43 +03:00 on the mock-up page: «Готово», no remarks, no
  letter (`interviews/decisions/caption_look.decision.json`, `noRemarks`); recorded in the homework 16:44 as `[AI]`
  «nothing to change — the caption stays A (upright, the book's size)»; a letter B–D from the owner reopens it. Epic 07
  Ф2 P2.4: the plan's tick and the Ф2 closure wait for the next epic-07 step (bug 09 came first).
- **Release-time debt (the 13.11 judge):** `README.md` / `USER_GUIDE.md` describe fractional mixing as always on and
  battery as «still being measured» — fix before KCCP 1.1.3 ships (the day-loop entry of 13.11 is in `PROJECT_HISTORY.md`,
  «STATUS trim 5»). Draft homework for the image: `homeworks/06_kccp_1.1.3_debug1.md`.
- **Epic 01 Ф2 + Ф3 closed** on `wip/kccp-1.1.3-debug2`: «Кнопки в шторке» `41718c61` (19:33, C1–C8) and the shade
  `261e5c63` (20:06, D1–D8: the owner's row with equal gaps measured by `tools/shade_gaps.py`, «Сон», «Фонарик» over
  the book, the long tap → the screen on that button → Back → the book). **Ф4 waits for the owner's word on the image**
  (the whole-epic judge, the device build, smoke, homework — `homeworks/06_kccp_1.1.3_debug1.md` grows into the
  1.1.3-debug2 homework). **Idea 09 built** (`9027b99a`, 20:24): every picture opens by its shape, simulator E1–E10
  pass (`testcases/reports/2026-11-13_idea09.md`).
- **KCCP 1.1.3 = the next release** (the owner 2026-11-13 17:07, `MASTER_PLAN.md` → decision journal); 1.1.3-debug1 assembled, judged, host tests green; no device build, no image.

### 2026-11-17 — STATUS trim 6 (2026-11-17 16:07 +03:00): closed items of 14.11 and the KNOWLEDGE lines of 13–14.11 (moved verbatim)

- **2026-11-17 09:49 chat (the owner: «нам ответили по фиксу бага с инверсией обложки… у него воспроизвелось»):**
  upstream #4329 comments read (itsthisjustin 2026-11-16 19:10/19:12 UTC: the negative covers came back on «Сетка
  обложек»). Cause read in the code: the grid theme has its own snapshot cache `HomeCoverCache`, not covered by #4329;
  upstream fixed it in #4494 (`b9c23473`). Ported onto debug2 on the owner's word (10:04 «Всё делаем»): `07df1501`
  (author Justin), simulator red on the old build and green both ways, host 795/803 = the 8 known
  (`testcases/reports/2026-11-17_bug07_grid_night.md`); bug 07 waits only for the reader check with the debug2 image.
  Lessons EXP-0023, EXP-0024 (the contour server killed under `timeout` AGAIN — a guard is owed, see the entry).
  **Owner's debt / open from this chat:** (a) interview #006 answered 10:18 — **A, «Для Мамы» only on «Кнопки домашнего
  экрана»** → DONE 10:36: firmware `da382c2f`, plan 10 → `plans/10_DONE_…`, epic 05 Ф4 closed; (b) interview #005 —
  the owner's remark 10:18 «покажи картинками. пока не увижу глазами - не о чем мне тут ответ давать» → the three
  variants rendered on a book page and shown 10:31 as one picture (`qa_runs/caption005_compare/compare.webp`, mockup page);
  answered 10:40 — **A, the author's text**, and repeated: «НЕ НУЖНА КРАСНАЯ СТРОКА… подпись ВСЕГДА должна быть рядом с
  картинкой» → **epic 07 started now** (the owner's debt before the plan); epic 05 Ф5 parked then (planned, no code;
  built in the 14:42 day loop — `plans/11_DONE_epic05_p5_home_long_tap.md`); (c) DONE 10:24 — the reply to itsthisjustin posted in #4329 (the
  owner: «Да, оба одобрено» · «отправляй»); (d) `bugs/08` (the shade's night button leaves pictures under the sheet
  negative) — the owner 10:21: «Пофиксить бы, в будущем. Пока как баг заведи и нам и в апстрим»; upstream issue #4515
  opened 10:24 (watch it for answers); the fix itself — later.
- **Chat 2026-11-14 15:26 → 17:39 (day loop, the owner 15:26: «работай автономно над прошивкой в автономном цикле
  дневном») — closed by the 90 % context window.** Done: interview #004 applied (`b856ce2`); **epic 05 «Кнопки домашнего
  экрана» Ф1–Ф4 on `wip/kccp-1.1.3-debug2`** (local, not pushed, NO image): Ф1 model `homemenu` + key `homeButtons`
  (`be6e9a16`), Ф2 Home draws it in all five themes (`f9ae704b`), Ф3 the button list scrolls — the mama button reachable,
  0 off-screen draws (`a47582b0`), Ф4 the screen «Кнопки домашнего экрана» + «Кнопки в шторке» on one shared base
  `ToggleRowsActivity` (`2fa20f3f`). Run reports `testcases/reports/2026-11-14_epic05_p1…p4.md`. Epic 07 (idea 03)
  planned. Windows mama simulator env `simulator_x4_pro_mama_win` added (`firmware/platformio.local.ini`). The closing
  device build `x4pro-krinik-debug` of `2fa20f3f` compiles (RAM 34.3 %, Flash 83.0 %) — a compile check, no image made.
- KNOWLEDGE (14.11): the X4 Pro simulator's Home geometry (top 314, content bottom 797) → the code comment of
  `HomeActivity::visibleMenuRows` + EXP-0022; `-Wswitch` is off in the firmware build → EXP-0021; the shade screen is
  now a shared base → `PROJECT_ARCHITECTURE_INTERNAL_MAP.md`; the mama simulator stand and script key verbs →
  `HOUSE_RULES.md`; the environment dossier → `HOUSE_RULES.md` §3.
- KNOWLEDGE (13.11): the facts of the chats live in the maps, `EXPERIENCE.md` (EXP-0012…0019) and
  `HOUSE_RULES.md`; the 13:51 → 16:21 KNOWLEDGE paragraph moved verbatim to `PROJECT_HISTORY.md` («STATUS trim 4»).

### 2026-11-14 — STATUS trim 5 (2026-11-14 17:39 +03:00): closed items of 13.11 (moved verbatim)

- **Day loop 2026-11-13 19:01 +03:00 — the owner:** «работай автономно над читалкой, со сборкой не торопись, она
  мне пока не особо нужна. Работаем по фичам KCCP» · «дневной цикл». The debug1 IMAGE waits (no build, no card, no
  homework delivery until asked); the loop works the KCCP features: epic 01 Ф2 → Ф3, idea 06, idea 09, idea 03.
  The debug1 judge (19:00) found `frontlight_dither` red at `d56b53e9` (a fade check kept the old 10 % threshold) —
  observed red, fixed (threshold = the 9 % duty), green on all three configurations, red on the old gate (control).
  Draft homework for the image: `homeworks/06_kccp_1.1.3_debug1.md` (build data placeholders ⟨…⟩). Release-time debt
  (judge): `README.md` / `USER_GUIDE.md` describe fractional mixing as always on and battery as «still being
  measured» — fix before KCCP 1.1.3 ships.
- **Chat 2026-11-13 13:51 → 16:21 closed** — its summary moved verbatim to `PROJECT_HISTORY.md` (entry «STATUS trim
  4»); debug10 `wip/krinik-debug10` is the base of the 1.1.3 line below.
- **The shade's elements are «кнопки»** (the owner 17:06) — applied; the record is in `plans/01_EPIC_shade_tiles.md`
  → «Решения владельца» (the verbatim block moved to `PROJECT_HISTORY.md`, «STATUS trim 4»).

- **First steps next chat:**
  1. `node D:/work/ai_sandbox/_tools/machine-lock.mjs status` and `ListAgents` (shared PC: KUMM, KAGO).
  2. **Epic 01 Ф4** only on the owner's word (the image); meanwhile epic 05 by its meta-plan's status, on <!-- attribution-ok: the owner 2026-11-13 19:01 «со сборкой не торопись» — the day-loop entry of this trim -->
     `wip/kccp-1.1.3-debug2`. Before any firmware commit: `sh tools/host_tests.sh` (new failures + CRLF,
     EXP-0018/0019); a shade shot is measured by `tools/shade_gaps.py`.
  3. **Idea 06 = epic 05 «Кнопки домашнего экрана»** (`plans/05_EPIC_home_buttons.md`) reuses the epic 01 Ф2 screen;
     the next phase is the one its status names.
  4. The owner's debug9 check (homework 04, steps 2, 4–7) is superseded by the debug10 image (it carries everything of
     debug9); his verdict on picture opening (13:51 «работает») is recorded.

#### What is in this repo (moved from STATUS)

- `restore.mjs`, `settings.json`, `fonts/`, `РУКОВОДСТВО.epub`, `КАЛИБРОВКА.epub`, `covers/`, `guide_settings_section.xhtml` —
  the owner's reader setup (how-to in `legacy/README.ru.md`).
- `firmware-builds/` — own krinik images with SHA256 files (sources in the forks above).
- `tools/` — font build, image and analysis scripts. `kuips-runner/` — `npm install` restores it.
- `researches/`, `research/`, `interviews/` — analyses and owner interviews (Russian).
- `qa_runs/` — evidence of builds, tests, PR preparation (logs, diffs, frames), filtered for publication.
- `sleep/` — sleep-screen previews; the BMP files themselves stayed on the laptop.
- `legacy/` — the laptop-era README, STATUS, HANDOVER, PROJECT_HISTORY (Russian) and `left-on-laptop.tsv`.

#### Left on the laptop — not published (moved from STATUS)

Moved verbatim to `PROJECT_HISTORY.md` (entry 2026-11-08, "Left on the laptop") on 2026-11-09; per-file list in
`legacy/left-on-laptop.tsv`.

- **KCCP 1.1.3 = the next release; 1.1.3-debug1 NOW for the reader — the owner 2026-11-13 17:07 +03:00:** «да, всё, что
  сейчас есть, собираем в 1.1.3 - это будет наш очередной релиз. соответственно, для меня, для тестов на железе. пока
  можешь собрать отладочкую сборку 1.1.3-debug1» (the answer to the agent's 17:05 question «называем 1.1.3-debug1 и
  вливаем 1.1.2?»; earlier 17:03 «какие фичи поставит мне 1.1.3-debug1 ?»). Done 17:12–19:22: the line
  `wip/kccp-1.1.3-debug1` (debug10 `ed5e2f0d` + release 1.1.2 merged + version 1.1.3 / `-debug1` + two test fixes),
  judged, host tests green; the image waits for the owner's word (19:01). `[AI]` the «Кнопки в шторке» screen (epic 01 Ф2) is
  NOT in debug1: the shade does not read its row until Ф3 — it comes with Ф3 in debug2 (said to the owner 17:08).

### Hardware research and the tiles idea

- Closed 2026-11-13; moved verbatim to `PROJECT_HISTORY.md` (entry 2026-11-13, STATUS trim 2). The configurable
  shade tiles are `ideas/05` now.

### 2026-11-13 — STATUS trim 4 (2026-11-13 19:45 +03:00): the summary of the closed chat 13:51 → 16:21 (moved verbatim)

- **Chat 2026-11-13 13:51 → 16:21 closed** (the owner's word 16:21 «закрывай чат, и продолжим в новом»). Done — detail in
  `PROJECT_HISTORY.md` (entry «STATUS trim 3»):
  - **debug10** = `wip/krinik-debug10` in `firmware/` (local, NOT pushed, NO image yet — the owner 16:02 «пока нет»):
    `9f02db5f` idea 07 long-tap rotation · `435d2493` epic 01 Ф1 (shade tile model + storage) · `551173b8` comment fix ·
    `52212d81` idea 08 «Настройки сна» · `8538f3dd` viewer: every TOUCH follows the picture as it stands, the KEYS keep
    the reading orientation, the book holds touch after a turned picture · `085c70d9` keys: short press pages, LONG press
    turns (`[AI]` forward clockwise, back counterclockwise) · `ed5e2f0d` a comment fix. All judged; simulator reports in `testcases/reports/2026-11-13_*`.
    The device env `x4pro-krinik-debug` builds on `085c70d9`: SUCCESS 2026-11-13 16:33, RAM 34.3 %, Flash 82.7 % — no image
    copied to `firmware-builds/` (the image comes with the shade, Ф4).
  - **msys64 moved to `F:\ai_sandbox\msys64`** (the owner 14:06); the old copy `D:\msys64.moved-2026-11-13` waits for his
    double-click on `Udalit staryj msys64 (KCCP).cmd` (desktop) — the agent's delete is refused by the permission rules.
  - Ideas recorded: 07 (rotation: built, simulator-tested), 08 (sleep settings: built, simulator S3 — the value-change part, S4 and S6 open), 09 (the viewer opens a picture in the orientation that
    fits its shape — verbatim only), epic 01 planned (`plans/01_EPIC_shade_tiles.md`, Russian).

- **The shade's elements are «кнопки» — the owner 2026-11-13 17:06 +03:00:** «Плитки шторки - переименовать в "Кнопки в
  шторке"» · «это не плитки, это Кнопки». Applied 17:07: the screen and the on-device strings, the meta-plan, MASTER_PLAN,
  plan 03, the cases, the map, code comments. Russian texts say «кнопка»; code identifiers (`ShadeTiles`, `Tile`) and
  English agent docs keep "tile"; the owner's own past quotes are left verbatim.
- KNOWLEDGE: the image viewer keeps the renderer in the picture's orientation and the keys in the reading orientation
  (internal map, `ideas/07`); one physical gesture has several input names and consumers — gate the touch frame
  (EXP-0016); simulator scripts need `<ms>:` on every item and rising times inside a WAIT segment — now a guard in
  `tools/sim_run.sh` (EXP-0015); the clock placeholder is filled only by Write/Edit, not by scripts (EXP-0012); the full
  host-test suite on this PC is 773/781 with 8 native-Windows failures (research 01); MSYS2 lives in `F:\ai_sandbox\msys64`
  (AGENT_GUIDE Build); Settings sub-screens past `SettingsSection::End` (internal map); `python -I` ignores `PYTHONUTF8`
  — use `-X utf8`; Settings screens are portrait while the reader and its shade follow the reading orientation.

### 2026-11-13 — STATUS trim 3: chat 13:51 → 16:21 closed, its «Where to continue» body (moved verbatim)

- **msys64 moved (owner 14:06 «D:\msys64\ давай переместим в F:\ai_sandbox\»)** — now `F:\ai_sandbox\msys64`
  (robocopy 14:09, 60 379 files / 2 293 125 441 bytes both sides); paths fixed: `firmware/platformio.local.ini`,
  `tools/sim_run.sh`, AGENT_GUIDE Build, research 01, Start-menu shortcuts, HKCU uninstall entry. The old folder is
  RENAMED `D:\msys64.moved-2026-11-13`; checked on F: alone — clean simulator build 271 files (0 from cache) SUCCESS,
  host tests 761/769 (the 8 are native-Windows portability, research 01), simulator runs with SDL2.dll from F:. The
  agent's delete of the old copy was refused by the permission rules → **`Udalit staryj msys64 (KCCP).cmd` on the
  owner's desktop** (checks F: first, removes the old copy, deletes itself) — waits for his double-click. Not ours to
  fix: Vibepollo/KAST build caches name `D:/msys64` (KAST's own MSYS2 was removed 2026-10-15; its plan 01 reinstalls to `D:\msys64`).
- **Idea 07 built and simulator-tested** on `wip/krinik-debug10` `9f02db5f` (from debug9, local): right-half long tap
  clockwise, left-half counterclockwise; judge no blockers; cases D0, C1–C5 pass
  (`testcases/reports/2026-11-13_idea07_simulator.md`). **Open with the owner:** after he turns the reader in his hands,
  whose halves — the owner chose B 14:54 «половины давай считать по картинке, убедил», then 15:05 every viewer gesture by the picture «как смотришь на картинку, так и управляешь, да, логично» (code change in flight). The
  device image comes with idea 05 (his «делаем» = one debug10).
- **debug10 now (firmware, local, not pushed):** `435d2493` epic 01 Ф1 · `52212d81` idea 08 «Настройки сна» (simulator
  S3 pass) · `8538f3dd` viewer: every TOUCH follows the picture as it stands (halves, swipes, Back), the KEYS keep the
  reading orientation (`MappedInputManager::setKeysFollowReadingOrientation`; the owner 15:20–15:21 «НЕТ! ФИзические
  кнопки крутят в одном направлении» · «одна кнопка в одном, вторая - в противоположном»), and after a turned book
  picture closes the book skips screen touches until its page repaints (≤ 3 s; device time is logged). Simulator C6–C9
  pass (`testcases/reports/2026-11-13_idea07_08_simulator.md`); five judge passes, two shapes refused (EXP-0016).
  The keys PAGE the pictures as before — the owner 16:01 «А — листают картинки, как и было» (no code change).
- **Idea 07 keys done 16:14** (firmware `085c70d9`): a short press of a page key pages the pictures on the release, a
  LONG press turns the picture (`[AI]` forward clockwise, back counterclockwise); judge no blockers; simulator C10–C12
  pass (`testcases/reports/2026-11-13_idea07_keys_simulator.md`). No interim image (the owner 16:02 «пока нет. работаем
  дальше»). **Next: epic 01 Ф2 P2.3** (`plans/03_epic01_p2_tiles_screen.md`). Context window 80 % at 16:03 — close the
  chat soon (`/end-chat-soft`).
- **Idea 05 = epic 01** (heaviness 2 of 5): research `researches/2026-11-13_idea05_shade_tiles_epic.md` (AOSP tile
  list, WCAG 2.5.7 up/down, CSS space-evenly, long tap → tile settings); meta-plan `plans/01_EPIC_shade_tiles.md`
  (Russian; phases Ф1 model+storage → Ф2 the «Плитки шторки» screen → Ф3 the shade row, new tiles, icons, long tap →
  Ф4 acceptance + image). **Ф1 closed 15:02** (firmware `435d2493`: `src/util/ShadeTiles.h` + host test 12/12 +
  storage; report `testcases/reports/2026-11-13_epic01_p1.md`). **Next: idea 08 «Настройки сна»** (plan inside the idea),
  then the Ф2 plan — written: `plans/03_epic01_p2_tiles_screen.md`, P2.1 recon done (a UiAppHost screen, not a
  UiListActivity: the list hides row rects); P2.2 icons — `tools/make_icon.py` draws ▲ ▼ and the half-filled circle
  (1-bit `freeink::Icon`); **next: paste them into `customListIcons.h`, then P2.3 `ShadeTilesActivity`.** Waiting on the owner: whether ALL viewer gestures (swipes, side taps, Back, the shade) follow the
  picture like the long-tap halves (asked 14:56, recommended yes — one rule; it also suits idea 09).
- **Chat 2026-11-13 10:34 → 13:35 closed — features for KCCP 1.1.3** (the owner's task under `resume`). Results:
  - **Idea 02 (tap a book picture → full screen, swipe Back → the same page): built.** `wip/krinik-debug9`
    (`526c7452` + `35dc070c`, local in `firmware/`, not pushed) = debug8 + the picture tap + battery log OFF; judged
    three times; host test `test/page_image_target/` 4/4 (red on a `<=` mutation); simulator C1–C5, C7, K1–K3 pass
    (`testcases/reports/2026-11-13_idea02_simulator.md`; C6 — the second fast Back swipe — only on the reader). Image
    `firmware-builds/cp-2.0.0-krinik-1.1.1-debug9.bin` (SHA256 `6b5f4f36…`) is on the reader's card since 11:47
    (card = debug9 + debug8 + 1.1.2). **On the reader 2026-11-13 13:51 +03:00 the owner: «открытие картинок на
    фулскрин работает»** (homework 04 steps 1, 3); steps 2, 4–7 (Back to the same page, the second fast Back, text taps,
    page brightness, long-tap rotation) not reported yet; no serial log taken.
  - **Bug 06** — the simulator kept its absolute gray mode after the image viewer (pages dark); fixed in the simulator
    clone on the LOCAL branch `fix/gray-absolute-reset` (`49ded1a`); PR #62 (`windows`, `087cb54`) untouched.
  - **Idea 03 (caption stays with its picture):** recon + research (`researches/2026-11-13_figure_caption_keep_together.md`,
    СТП 01-2017 БГУИР 2.5 read verbatim); direction by the owner: re-typeset the books to `<figure>`/`<figcaption>` +
    the firmware keeps a figure on one page (picture shrinks if needed); no first-line indent (owner 11:13);
    `[AI]` caption centred under the picture — the reading of СТП 2.5.5, not his word.
  - **Idea 04 (FB2 → EPUB on the reader):** first recon (upstream declined FB2 three times; papyrix-reader `lib/Fb2`,
    MIT); heavy → `/plan-epic`; test FB2 `D:\Hofshtadter_Gyodel-Esher-Bah-Eta-beskonechnaya-girlyanda.9y7ehg.198312.fb2.zip`.
  - **Idea 05 (shade tiles): AGREED, go-ahead 13:28** — a long tap on any tile opens Settings straight on «Плитки
    шторки» (list: icon · name · ▲▼ · firmware square checkbox; portrait; cursor on the tapped tile); seven tiles
    (night mode — new iOS-style half-filled circle icon, cleanup, orientation, touch, Bluetooth, Sleep — crescent,
    Flashlight); EQUAL gaps between tiles and at the edges for any count (today the edge gap is half). Final view
    `homeworks/05_shade_mockups/final.html`. `[AI]` defaults: Back returns to the book; also in «Настройки → Экран».
  - **Idea 06 (Home buttons settings)** — the same screen kind for the Home menu items (owner 13:29); verbatim only.
- **Chat 2026-11-13 13:51 → (open).** The owner on debug9: picture opening works; «подписи … всё ещё открываются от
  картинок» — `[AI]` read as «отрываются», expected (idea 03 has no code; recorded there). New **idea 07** (owner 13:51):
  in the viewer a long tap on the right half turns the picture clockwise, on the left half counterclockwise — code recon
  in the idea (`BmpViewerActivity::loop()` already gets the long-tap point in reading-orientation coordinates and ignores
  it; `rotate()` turns one way); answered «можно», offered for debug10 together with idea 05 — **go-ahead 14:03 «делаем»**: debug10 = debug9 +
  idea 07 + idea 05.
- **First steps next chat:**
  1. `node D:/work/ai_sandbox/_tools/machine-lock.mjs status` and `ListAgents` (shared PC: KUMM, KAGO).
  2. **The rest of the owner's debug9 check (homework 04, steps 2, 4–7).** When he says the reader is on the cable (book screen, NOT USB drive):
     `.pio-venv/Scripts/python.exe -I -X utf8 tools/serial_log.py <scratch>/serial_debug9.log` in the background; watch
     `Image tap`, `Back swipe`, `[ERR]`, `OOM` (the debug image logs at LOG_LEVEL=1 — INF and up). His verdict → homework
     04 «Итог», `ideas/02` closure, `testcases/TC_idea02…` C6.
  3. **Epic 01 (idea 05) by `plans/01_EPIC_shade_tiles.md`** — the phase in flight and its plan are named at the top
     of this list; the «Плитки шторки» screen of Ф2 is reused later by idea 06 «Кнопки главного экрана».
- **Open work, in order:**
  1. Idea 05 + 06 (one list component); 2. Idea 03 (re-typeset tool + firmware `<figure>`); 3. KCCP 1.1.3 assembly:
     merge release 1.1.2 (`198d385e`) into the debug line (conflicts `lib/hal/HalFrontlight.{cpp,h}`,
     `test/frontlight_dither/`); the owner's open choice: light-linger hold (400 ms) vs timer-redraw hold; 4. Idea 04
     (epic). 5. Bug 01 PR `pr/library-tab-fit` (`d2b45c0e`, `d0c99508`) — a free upstream slot (5/5) + proofreading.
     6. `bugs/05`, `bugs/06` (a simulator PR for 06 needs the owner's proofreading). 7. The test hook does not see
     `tools/sim_run.sh` runs: a `testHook` block in `.kaif/kaif.json` — to be asked (the auto-mode
     classifier refused the agent's edit). 8. Proofread `GOAL.md`. 9. Delete the partial `C:\msys64` (check the machine lock).
  - Reviews to read: simulator PR #62 and firmware PRs #4328 #4332 #4375 #4376 #4377
    (`gh api repos/<owner>/<repo>/pulls/<n>/comments --jq '.[]|select(.created_at>"<last read>")'`).
- KNOWLEDGE: `python -I` ignores `PYTHONUTF8` — use `-X utf8` (AGENT_GUIDE Code style, updated);
  the simulator's reader takes the OVERLAY gray path, only the viewer uses absolute (`bugs/06`); Settings screens are
  portrait while the reader and its shade follow the reading orientation; the firmware checkbox is a square with a
  filled inner square (FreeInkUI `list.h`); a launched Edge window is not a shown window (EXP-0014); a page server under
  `timeout` dies (EXP-0013); `pdftotext` is at `/mingw64/bin` (Git for Windows); the debug image number lives in
  `platformio.ini` (AGENT_GUIDE Build, updated). Reader clock may run ≈ 40 min fast (unverified, PROJECT_HISTORY).

### 2026-11-13 — STATUS trim 2: closed hardware research, the tiles idea, old debug-line notes (moved verbatim)

### Hardware research

- Closed 2026-11-08: no charging cut-off (needs a board modification); the charger analysis and the battery/light
  measurements moved verbatim to `PROJECT_HISTORY.md` (entry 2026-11-09, STATUS trim).
- **Closed [2026-11-13 10:36 +03:00]: battery-discharge measurements stop; no more search for ways to cut the current
  through the frontlight** — `[OWNER] 2026-11-13 10:36 +03:00 · chat: «там ты замерял разряд батареи, я думаю, что можно
  прекратить эти замеры. Подсветка не много кушает заряда батареи, и можно перестать искать способы снижения тока через
  подсветку»`. Open: whether the debug-only 20-minute battery log leaves the debug builds (asked in chat, same turn).
- LED driver/current/ratings stay unknown — no longer researched (decision above).

### Future (owner, 2026-11-06: "on the future")

- Configurable Control Center tiles in a separate menu (add Sleep/Flashlight, hide Bluetooth/Clean). Recon:
  `src/activities/util/FrontlightPanelActivity.*`, `kTileCount`, `runTile(idx)`, `buildPanelScreen`.

From «Device»:

- Battery log every 20 min is a **DEBUG ONLY** aid — keep it out of release builds.
- Debug line: debug3 (precise temperature), debug4 (battery log tick every 20 min), debug5 (= debug4 + "Sleep" item in the Home
  menu under "Flashlight"). Images and SHA256 in `firmware-builds/`; evidence in
  `qa_runs/precise-temperature-2026-11-06/`, `qa_runs/debug4-2026-11-06/`, `qa_runs/debug5-sleep-menu-2026-11-06/`.
- The debug2–5 code was uncommitted on the laptop; it is now `wip/krinik-debug5` in both forks (see the code map). The debug2 image
  itself is in `firmware-builds/` (`cp-2.0.0-krinik-1.1.1-debug2.bin`).

### 2026-11-13 — STATUS trim: the 2026-11-10 chat's handover lines (moved verbatim from STATUS "Where to continue")

- **Chat 2026-11-09 20:30 → 2026-11-10 (CodeRabbit round 3, debug7/8, simulator PR #62) closed** — its full log moved
  verbatim to `PROJECT_HISTORY.md` (entry 2026-11-10). Result: #4377 books-card title fix pushed (`c9d69cbd`); #4376
  redraw-timer fix pushed (`94e1c3a2`) after the owner's reader check; debug7 (bugs 03/04) and debug8 (idea 01) PASS on
  the reader; native Windows simulator PR **#62** opened and its CodeRabbit round 1 fixed (`087cb54`).
- **Rules born this chat** (all in `AGENT_GUIDE.md`): reviewer bots can be wrong — trace a finding in code before
  acting; after a code change an independent judge first, build after; a PR description carries no AI-participation
  line and nothing sent out carries AI authorship (no `Co-Authored-By` trailer on pushed commits).
- KNOWLEDGE: Windows UCRT `TZ` — three-letter names only, DST on US dates (simulator README, research 01); Winsock
  sockets cannot be `dup()`-ed and `_execvp` does not replace the process (research 01); `MoveFileEx` for an
  overwrite-safe replace; lessons EXP-0008…0010 (`EXPERIENCE.md`): Git Bash grep crashes on long pipes, a "defect" that
  was my script quitting first, parallel shell calls must not rely on `cd`.

### 2026-11-13 — battery research closed; the debug battery log's final numbers ✅

The owner closed it (`[OWNER] 2026-11-13 10:36 +03:00 · chat: «…можно прекратить эти замеры. Подсветка не много кушает
заряда батареи…»`, 11:04 «логи можно отключать в следующей дебаг сборке. чтобы они не кушали батарею и флешку не
изнашивали»): `KRINIK_BATTERY_LOG` is off from `1.1.1-debug9`. The final log — 7.0 days, 2026-11-06 11:05 →
2026-11-13 11:18 by the reader's clock, 732 rows (`qa_runs/battery_log-2026-11-13-final.csv`; summary
`python -I -X utf8 tools/battery_summary.py <csv>`):

| Mode (not charging) | Hours | Drain | One charge lasts |
|---|---|---|---|
| reading, light off | 3.7 | 3.56 %/h | ~28 h |
| light on 11–50 % (UI) | 2.5 | 4.01 %/h | ~25 h |
| light on > 50 % (UI) | 11.3 | 8.46 %/h | ~12 h |
| sleep (40 periods) | 111.5 | 0.43 %/day | months |

Sleep periods ≥ 6 h: 8, 86.8 h, 0 % lost. Caveats: the gauge counts in 1 % steps; few light-off hours; page turns
are mixed into the awake rows. Side finding, not checked: the log's last row is a boot at 11:18 by the reader's
clock, while the reader was on the wire at ≈ 10:37 PC time — the reader's clock may run ≈ 40 min fast.

### 2026-11-10 — CodeRabbit round 3, debug7/8, simulator PR #62 (moved verbatim from STATUS "Where to continue")

- **Chat 2026-11-09 (resume → CodeRabbit round 2) closed 20:20 +03:00** — its full log moved verbatim to
  `PROJECT_HISTORY.md` (entry 2026-11-09, "CodeRabbit round 2"). Result: all 14 CodeRabbit comments answered or fixed,
  `pr/screen-redraw-delay` and `pr/screen-calibration` pushed to the fork, 12 replies posted (research 02 → "Reply
  drafts"); the owner checked the power-hold fix on his reader (debug6). Interviews #001 and #003 closed.
- **First steps next chat:**
  1. `node D:/work/ai_sandbox/_tools/machine-lock.mjs status` and `ListAgents` — the PC is shared with KUMM (Conan
     benchmarks) and KAGO; during another agent's quiet window: no builds, no simulator, no GUI windows.
  2. Read CodeRabbit / maintainer answers on #4328 #4332 #4375 #4376 #4377:
     `gh api repos/crosspoint-reader/crosspoint-reader/pulls/<n>/comments --jq '.[]|select(.in_reply_to_id!=null)'`.
     READ [2026-11-09 20:30 +03:00]: all 12 replied threads resolved by CodeRabbit, no maintainer comments, CI green on #4376/#4377.
     OPEN: #4377 new round on `d8573ad5`, two Minor — `CalibrationCardStorage.cpp:17` (books card keeps the old-language
     title, written once) and `:104` (v1 EPUB's `/.crosspoint/epub_<hash>/` cache not removed); #4376 asks for an X4 Pro
     hold/short-press check (owner did it on debug6 — reply); #4328 asks whether to open a follow-up issue (post-table OOM).
     Traced by me (not taken on CodeRabbit's word): `:17` holds — the title is baked into the EPUB (`CalibrationCard.cpp`
     dc:title/nav/page) and shown via `epub->getTitle()`; a fix must also drop the card's `epub_<hash>` cache (title is
     cached in `book.bin`). `:104` is true but low value — v1 existed only inside this unmerged PR.
     Owner 20:33 «да, это наш промах. Доработать нужно»; on `:104` «можно сделать строку для перестраховки, но написать,
     что это несущественно». DONE: fix `c9d69cbd` pushed to the fork 22:17 (#4377 head) — `booksCard()` reuses the
     card only while `Epub::loadMetadata()` title == current language, else `clearBookCache` + rewrite via
     `Storage.replaceFile`; v1 cache cleared. Simulator: RU→EN title, reuse, control on `d8573ad5` red (testcases
     `TC_coderabbit_round2_calibration.md` §7). Found on the way: simulator `replaceFile` could not overwrite on Windows
     — fixed `ba46fb7` on simulator `windows` (LOCAL, its push is the owner's open question). 4 replies POSTED
     22:17–22:22 (owner «отправляй», #4328 «A»). WAITING FOR THE OWNER (research 02 → "Round 3 — posted"): #4376 —
     owner 22:26 «Питание коротко: сон стоит»; his repeat with «Игнорировать» 22:31–22:39 (homework 01): hold during the
     redraw wakes ✅, click during the redraw sleeps ✅, and TWO defects → `bugs/03` (redraw timed from the last
     non-waking press on debug6; LOST entirely on PR #4376) and `bugs/04` (click in the light linger cancels the
     sleep; owner A1: click only with «Сон», else a hold). Fixes judged twice by an independent agent (round 1 REFUTED
     the PR fix — the path was cleared before the re-arm), both now VERIFIED WITH CAVEATS: debug7 `2b150595`
     (`wip/krinik-debug7`, local) built → `firmware-builds/cp-2.0.0-krinik-1.1.1-debug7.bin` (SHA256 `8662b4db…368f`),
     smoke `qa_runs/smoke_2b150595`; PR `94e1c3a2` local, NOT pushed (x4pro compile check running). x4pro compile of
     `94e1c3a2` SUCCESS. 23:14 debug7 on the card (SHA256 checked there), card cleaned to debug7 + debug6 + 1.1.2,
     reader ejected. 23:22 owner: homework 02 «все кейсы PASS, всё ок» → bugs 03/04 DONE. NEXT: push `94e1c3a2` + reply CodeRabbit #4376 (owner's word); idea 01 (Home «Сон» highlight on tap, owner 23:22).
     Owner's open choice: the linger hold (400 ms) vs the redraw hold (≈ reset-to-sample) rules differ.
     #4377 `:115` truncated-card finding — decline draft to proofread. CI on `c9d69cbd`.
  3. Card cleanup DONE 2026-11-09 23:14 (`[OWNER] 20:09 «и образы старые поудаляй»`; rule: current debug + previous
     debug + latest release): `/.firmware/` = debug7 + debug6 + 1.1.2; reader ejected.
- **Open work, in order:**
  0. **debug8 DONE** 2026-11-09 23:46 (idea 01, Home «Сон» highlight on tap): `c072214b` on `wip/krinik-debug8`
     (local), judged, simulator + control, on the owner's reader «да, работает» (homework 03). Card = debug8 + debug7 +
     1.1.2. #4376 fix `94e1c3a2` PUSHED 23:26 + CodeRabbit reply 4517595666 (owner «1 да»).
  1. **Simulator upstream PR** (owner «делай» 20:13; order agreed 23:29): the «SHOT stalls after a second WAIT»
     defect is NOT A DEFECT (23:50, research 01 — my probe had QUIT at 500 ms before SHOT at 800 ms). Windows checks
     2026-11-10 00:02–00:35 (research 01): HTTP ✅, clock = UTC as documented, X4 env ✅; File Transfer (empty reply,
     `dup()` of a Winsock socket) and sleep/wake (caller not waiting, exit status lost) fixed in `dfd450a` (local,
     judged twice, runs pass with controls, kill-the-waiter PASS after the owner's «РАЗРЕШАЮ» 00:46). `bugs/05` (firmware
     UDP `close()` on Windows) — found by reading, not reproduced. SQUASHED 00:51 → `ad131dc` (backup branch `windows-unsquashed`). On firmware `develop` `f8db833f`: builds, web_manager_smoke 8/8 (pre-fix ❌), the sample ini as written builds (+ the #60-style substitutions), system curl.exe HTTPS ✅. PR draft `qa_runs/pr-simulator-windows/body.md`, images pr-assets `15-windows-simulator/` (HTTP 200). Owner proofread «no remarks» 01:07, «отправляем» 01:08 → `windows` pushed, **PR #62 OPENED** 01:09 https://github.com/crosspoint-reader/crosspoint-simulator/pull/62 (mergeable, CodeRabbit running; AI footer removed per owner 01:09). `firmware/` back on `wip/krinik-debug8`. CodeRabbit round 1 on #62 (5 findings, all traced valid) → fix `2c34be9`+ judged (VERIFIED WITH CAVEATS; ANSI TEMP path regression found and fixed). AUTH: `[OWNER] 2026-11-10 01:38 +03:00 · chat: «на все отпраки ДАЮ РАЗРЕШЕНИЕ» · «на все твои сообщения ДАЮ РАЗРЕШЕНИЯ»` (pushes, PR replies, the closing push of this repo). OWNER 01:36 «работай автономно»: push the fixes, read CodeRabbit ~20 min later, fix until no remarks and the PR waits for a maintainer, then close the chat. 01:40–01:47 round-1 fixes run (injection probe: verbatim, no marker; control on ad131dc ran the command; replaceFile probe; web_manager_smoke 8/8; HTTPS via the new launcher; WebDAV backslash escape rejected), commits reworded without AI trailers (owner «только без авторства ИИ» 01:39), force-pushed `087cb54`, 5 replies posted, PR body updated. NEXT: ~02:08 read CodeRabbit round 2 on #62; was: squash 8 local commits, PR text for the
     owner's proofreading, his word to push `windows`.
  2. **Bug 01 PR** `pr/library-tab-fit` (`d2b45c0e`, `d0c99508`) — five themes checked; waits for a free upstream
     slot (5/5 open) and the owner's proofreading of the PR text.
  3. **Debug line**: `wip/krinik-debug6` (`e7a29dd4`, local in `firmware/`, not pushed) = debug5 + the hold fix, on
     the owner's reader now. BACKLOG: merge release 1.1.2 (`198d385e`) into the debug line (conflicts in
     `lib/hal/HalFrontlight.{cpp,h}`, `test/frontlight_dither/`), then `1.1.2-debugN`.
  4. Owner's open questions: proofread `GOAL.md`; the push of this repo is done each closing.
  5. Delete the partial `C:\msys64` left by the killed 14:44 install (KAGO said it is safe) — check the machine lock first.
- **Rules born this chat** (all in `AGENT_GUIDE.md`): screenshots WebP q90, viewed as WebP; simulator window 480×800
  1:1, borderless, top-left; images to the reader only after a simulator smoke of the same commit, only KCCP
  debug/release builds, eject the reader after copying; build from PowerShell with `PYTHONUTF8=1`; the `firmware/`
  clone keeps `core.autocrlf=false`.
- KNOWLEDGE: native Windows simulator works (research 01, `AGENT_GUIDE.md` → Build/Test harness); debug line is on
  1.1.1 without 1.1.2 (this file); seven lessons EXP-0001…0007 (`EXPERIENCE.md`); bug 01 (`bugs/01_…`), bug 02 not a
  defect (`bugs/02_DONE_…`).

### 2026-11-09 — CodeRabbit round 2, native Windows simulator (moved verbatim from STATUS "Where to continue")

- **Active task (owner, chat 2026-11-09 14:39):** «чиним замечания, которые нам сделаны в наших ПР» — the 14 CodeRabbit
  inline comments on PRs #4328 (3), #4332 (1), #4375 (1), #4376 (4), #4377 (5); «тестируем на симуляторе на этой машине».
  Comments dumped by `gh api repos/crosspoint-reader/crosspoint-reader/pulls/<n>/comments` (filter `coderabbit`).
  Fixes go to the fork's `pr/*` branches in `firmware/`; no push and no reply text without the owner's word.
  Progress 2026-11-09 14:56: all 14 triaged in `researches/2026-11-09_coderabbit_pr_review.md` — 2 addressed earlier
  (#4328), 1 already fixed on the branch (#4332, ca5d9fa0), **5 local fixes committed, NOT built, NOT pushed**:
  `pr/screen-redraw-delay` d101e463 · 2d5bb845; `pr/screen-calibration` b6477e41 · 75b92fc0 · 7addf5be. Open: #4328-3
  (defensive fix proposed), #4375 string (owner's wording), #4376 main.cpp:541 and :722, #4377 ImageBlock and
  orientations (replies proposed). Correction: commit 338f0b7 says "6 local fixes" — the count is 5.
  Progress 2026-11-09 15:25: re-dump — still 14 CodeRabbit comments, no human review comments. #4376 main.cpp:541
  fixed locally `9448f2a5` (6 local fixes now); #4328-3 → reply, no code (path unreachable; research 02). Interview
  #001 closed (both answers were already in code). Still open: #4375 string, #4376 main.cpp:722, #4377 ImageBlock —
  owner answered interview #003 at 15:43: Q1 D (no change, reply), Q2 B → `b661b6be` on `pr/screen-calibration`,
  Q3 B → `4818dba0` on `pr/screen-redraw-delay` (device check is the owner's). 8 local fixes, none pushed.
  2026-11-09 18:35–18:47: KAIF marks stripped (`2dbfff7d`, `d8573ad5`; grep → 0 on every `pr/*`); simulator runs
  done for both branches with controls — `testcases/TC_coderabbit_round2_redraw_delay.md`,
  `testcases/TC_coderabbit_round2_calibration.md`; status per comment in research 02. Not observable here:
  `9448f2a5`, `4818dba0` (`!SIMULATOR`), `75b92fc0` (OOM). Owner's word on sending, 2026-11-09 18:50 +03:00, after
  seeing all 12 reply texts in the question preview: `[OWNER] «давай протестируем кнопку, и всё тправим»` (typed
  first in the wrong layout: «jnghfdkztv jndtns» = «отправляем ответы»). Order: device image of
  `pr/screen-redraw-delay` → the owner checks the power hold during the timer redraw on his reader → push both
  branches → post the 12 replies of research 02 → "Reply drafts".
  19:05–19:12: the owner ran step 4 on the bare-upstream PR image — the hold woke the reader (bug 02 closed, not a
  defect) — and then ruled: test images are KCCP debug/release builds only (`AGENT_GUIDE.md` → The device). New:
  `wip/krinik-debug6` = debug5 + the #4376 hold fix ported by hand (`e7a29dd4`, firmware fork, local; the other three
  #4376 fixes do not apply to the KCCP code). Next, after KUMM's «замеры закончены»: build `x4pro-krinik-debug` →
  simulator smoke of `e7a29dd4` → image to the card → homework 01 steps 4–5 on debug6 → push + replies.
  20:10: debug6 built, smoke pass, on the card (SHA256 bf9f0a9f…), reader ejected. PENDING on the next connect: delete
  from the card's `/.firmware/` debug3, debug4, `crosspoint-2.0.0-x4pro.bin`, `cp-2.0.0-pr4376-2dbfff7d.bin` (owner:
  keep debug6 + debug5 + 1.1.2), then eject.
  Owner asked 20:10 why the debug builds say 1.1.1 («давно вышел релиз 1.1.2»): the debug line forked from 1.1.1
  (`a06a20d6`); the 1.1.2 release is one commit `198d385e` NOT in it; a merge conflicts in `lib/hal/HalFrontlight.{cpp,h}`
  and `test/frontlight_dither/FrontlightDitherTest.cpp` (both sides reworked the frontlight). Owner: test debug6 as it
  is now. BACKLOG: merge 1.1.2 into the debug line → `1.1.2-debugN` (frontlight conflicts, the owner's reader check).
- **DONE 2026-11-09 20:15 +03:00:** the owner confirmed the power button on debug6 («если нажать во время
  перерисовки - перерисовка выполняется и устройство просыпается»); pushed `pr/screen-redraw-delay` d7cc4e83..2dbfff7d
  and `pr/screen-calibration` f90b29b4..d8573ad5 to the fork; posted the 12 CodeRabbit replies (texts of research 02,
  first reply https://github.com/crosspoint-reader/crosspoint-reader/pull/4328#discussion_r4515664220). Next: watch for
  CodeRabbit/maintainer answers.
- **Owner's bug 01 (2026-11-09 16:55):** Library tab «Недав...» → `bugs/01_library_tab_label_truncated.md`; fix
  `d2b45c0e` on the new branch `pr/library-tab-fit` (cut from `upstream/develop` f8db833f), red/green WebP shots in
  `qa_runs/tab_fit_before|after/`; the owner wants it as an upstream PR — it waits for a free slot (5/5 open).
- Runs 2026-11-09 17:27–17:48 (after the KUMM windows): bug 01 English control pixel-identical; #4376 C1 pass (X4
  Pro shows «Обновлять заставку» in «Настройки очисток экрана»), C2 pass + K1 red (X4 keeps `sleepRedrawDelay`; the
  pre-fix `d7cc4e83` drops it). Bug 01 later widened per the owner (`d0c99508`, content-width pills, five themes).
  KUMM may ask for more quiet windows: then no builds and no GUI windows until its «замеры закончены».
- **Simulator upstream PR** — owner «окей» 2026-11-09 17:25 +03:00 to the plan: after the KUMM window run the
  unobserved parts (File Transfer, curl, sleep/wake relaunch, clock, X4 env), add `sample-platformio-windows.ini` +
  README, squash, bring the PR text for proofreading; sending only on his word (research 01 → "Upstream PR readiness").
- **Simulator:** WORKS natively on Windows since 2026-11-09 16:52 (`simulator` `0431782` + window placement). Build
  from PowerShell with `$env:PYTHONUTF8="1"`; run `SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh …` from Git Bash.
  Native Windows build of our fork `MikalaiKryvusha/crosspoint-simulator`, branch `windows`, clone in
  `simulator/` — route and POSIX inventory in `researches/2026-11-09_native_windows_simulator.md`. WSL is never used.
- Toolchain installed 2026-11-09 15:18–15:24 (lock `kccp` taken until 16:03): MSYS2 UCRT64 in `D:\msys64`,
  PlatformIO 6.2.0 in `.pio-venv/`, envs `simulator_win` / `simulator_x4_pro_win` in the ignored
  `firmware/platformio.local.ini` (research 01 → "Installed on this PC"). Partial `C:\msys64` still to delete.
- **Next:** finish the runs of `pr/screen-redraw-delay` and `pr/screen-calibration` → strip the marks → device image
  for the owner's Q3 check → ask the owner before any push or reply. Owner's open questions: proofread GOAL.md; push
  of this repo (`git log --oneline origin/main..HEAD`); the CodeRabbit reply texts (after the runs).
- KNOWLEDGE: the simulator needs a native-Windows port, WSL is never used · `AGENT_GUIDE.md` → Build, research 01;
  the PC is shared with the KAGO agent (machine lock) · `AGENT_GUIDE.md` → Build, `EXPERIENCE.md` EXP-0002.

### 2026-11-08 — Left on the laptop (moved verbatim from STATUS on 2026-11-09)


The repo is public, so this stayed in `~/Xteink` on the laptop (≈ 3.2 GB, 3 162 files; per-file list with sizes in
`legacy/left-on-laptop.tsv`):

| Size | Files | What | Why not here |
|---|---|---|---|
| 1 650 MB | 1 162 | test books (EPUB) | third-party texts |
| 1 466 MB | 1 462 | BMP sleep screens and panel test images | third-party art, size |
| 86 MB | 195 | SD-card and simulator binaries in `qa_runs/` | rebuildable |
| 19 MB | 125 | stock-firmware research: vendor firmware, disassembly, certification and teardown photos, datasheet | vendor/third-party material |
| 8 MB | 212 | reader cache copied from the card (book chapters, images) | third-party texts |
| — | 3 | `.crosspoint/wifi.json` copies | Wi-Fi credentials |

Also stayed: the local clones `firmware/`, `fw-pr/`, `pr-fixes/*` (all branches are on the fork — checked 2026-11-08), `pr-assets/`,
`KEINKT/`, `keinkt-fixes/` (on GitHub), the PlatformIO venv, `.kaif/` scratch of the old setup. The Home Wi-Fi network name was
replaced with a placeholder in `restore.mjs` and the legacy README.


### 2026-11-09 — STATUS trim: closed hardware research (charging, measurements) ✅
- Charging cannot be stopped in software at 4.1 V or N %: no charger on I²C, no CE/EN line to the ESP32. Only a board modification
  could do it. **Not doing it** (owner, 2026-11-08: «это не будет делаться»). Available now: a "unplug the charger" reminder at N % in firmware. Analysis:
  `researches/2026-11-06_stock_batinfo_charger_analysis.md` (its raw inputs — vendor firmware, disassembly, third-party photos —
  stayed on the laptop, see below).
- Measurements, do not repeat without a goal: charge 50→100 % in 1:07:06, gauge max 4.381 V
  (`qa_runs/debug2-charge-2026-11-06-180555/`); awake hour: light off ≈ 4–5 pp, light 100 % ≈ 8–9 pp
  (`qa_runs/debug2-light-hours-2026-11-06-201434/`).

### 2026-11-09 — KAIF deployed on the owner's PC (Task 0 step 3) ✅
- **Task 0 step 3 done 2026-11-09:** KAIF 2.9 (+2.10 WIP) deployed from KAIF commit d2f21274d396, commits 8a78058,
  2924afa; field report KAIF issue #195. Steps 1 (firmware clone — done 2026-11-09), 2, 4–6 open.

Earlier history (laptop era, Russian): `legacy/PROJECT_HISTORY.ru.md`.
