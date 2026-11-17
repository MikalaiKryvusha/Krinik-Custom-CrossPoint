# STATUS — Krinik Custom CrossPoint (KCCP)

Updated 2026-11-17 15:39 +03:00 (the 14:42 day loop: homework 08 shown, epic 07 Ф3 tool, epic 05 Ф5, plan 15 the guide). Licence: MIT (owner, 2026-11-08: «как у оригинального CP, или MIT»); fonts OFL, firmware images GPLv3.
 Moved off the owner's laptop, where it lived as a loose folder (`~/Xteink`) beside an unrelated
work project. From now on it is a standalone project.

## Where to continue

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
  `firmware-builds/`); ejected, `Test-Path H:\` False. **❓ the owner flashes and tests** — the checklist was given in
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
  (`testcases/reports/2026-11-17_bug12_bug13_debug5.md`). **❓ waits for the reader on the wire** (copy, SHA256 on the
  card, keep debug5 + debug4 + 1.1.2 — debug9 leaves, eject). Next: GEB re-typeset (plan 14 T9, the EPUB 2 form A).
  Homework 09 not raised.
- **Chat 2026-11-17 14:40 — DAY LOOP** on the owner's word 14:42 «работай автономно в дейлупк» (`/dayloop`, no end time
  named). Done: homework 08 — the clean §7B pass applied, committed `e7d5119`, the mock-up page shown (window on the
  screen, screenshot ≈ 14:50; the owner's letter A–D awaited there); the contour's decision-name collision guarded and
  filed (`b171cd6`, KAIF #199, EXP-0028); **epic 07 Ф3 tool** `tools/figure_retypeset.py` (`f8d213a`, plan 14, report
  `testcases/reports/2026-11-17_epic07_p3.md`: the test book pass, the judge's loose-label finding fixed; T9 the owner's
  two books blocked — the reader not on the wire); **epic 05 Ф5 DONE on the simulator** — firmware `de8feb20` (local),
  `plans/11_DONE_epic05_p5_home_long_tap.md`, report `testcases/reports/2026-11-17_epic05_p5.md` (five themes + mama; the
  judge's FIX FIRST — the grid's bottom-edge band — fixed and proven red on a mutant); EXP-0029 (CRLF again).
- **Bug 08** (the shade's night button leaves pictures under the sheet negative, `bugs/08_…`): upstream issue
  #4515 opened 2026-11-17 10:24 +03:00 on the owner's word — watch it; the fix waits for its answer (the 09:49 chat's
  full entry: `PROJECT_HISTORY.md`, STATUS trim 6).
- **KCCP 1.1.3-debug3 image built 2026-11-17 11:29** on the owner's word 11:21 «сделаешь мне дебаг3? накопилось фичей и
  фиксов на неё?»: `firmware-builds/cp-2.0.0-krinik-1.1.3-debug3.bin` (5 445 104 B, SHA256 `4774fee2…`), firmware
  `0d56b23a` (debug2 line + version bump; epic 07 Ф2 parked in `git stash` «epic07-p2-caption-wip» — its judge said FIX
  FIRST: the caption inherits the figure's alignment, a nested `<p>` gets the indent, the test cannot fail on the indent);
  simulator smoke of the same commit 0 errors (`qa_runs/debug3_smoke_home`, `…_book`); RAM 34.3 %, Flash 83.0 %.
  **superseded by debug4** (the reader came on the wire 2026-11-17 19:46 as H:; debug4 goes instead): copy to `/.firmware/`, check SHA256,
  eject; homework `homeworks/07_kccp_1.1.3_debug3.md`. This is the image of epic 01 Ф4 and epic 05 Ф6 (acceptance by
  the owner's check).
- **Homework 08 — the caption look ANSWERED** 2026-11-17 16:43 +03:00 on the mock-up page: «Готово», no remarks, no
  letter (`interviews/decisions/caption_look.decision.json`, `noRemarks`); recorded in the homework 16:44 as `[AI]`
  «nothing to change — the caption stays A (upright, the book's size)»; a letter B–D from the owner reopens it. Epic 07
  Ф2 P2.4: the plan's tick and the Ф2 closure wait for the next epic-07 step (bug 09 came first).
- **❓ homework 09 — the guide's five new lines** (`homeworks/09_guide_settings_proofread.md`, plan 15 G5): the owner
  proofreads the five `[AI]` lines of `guide_settings_section.xhtml` (the epub's settings chapters + the reader's
  changes) and decides his two text questions (the second «Проверить обновление» description; the separate file's
  role); then the chapter goes into `РУКОВОДСТВО.epub`. Filed 2026-11-17 15:59 +03:00, its clean §7B pass applied
  (`9db2811`); NOT shown yet — the contour raises one page at a time (I48) and the caption mock-up page (homework 08)
  is open waiting for his letter: raise 09 with `review.mjs homeworks/09_guide_settings_proofread.md --proofread` (in the
  background, never under `timeout`) once 08 is answered or closed.
- **❓ awaiting the owner (one action):** wire the guard `tools/hooks/pretool-deny-server-timeout.mjs` (refuses
  `timeout … review.mjs` page launches — the contour server died that way twice, EXP-0013/0024) into
  `.claude/settings.json` → `hooks.PreToolUse`, matcher `Bash|PowerShell` (the exact block is in the script's header);
  the agent's hook writes are refused by the auto-mode classifier.
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
   - [ ] Tell the owner the laptop can now clone this repo. `~/Xteink` on the laptop is retired only on the owner's word, after a
     by-name check that everything listed in `legacy/left-on-laptop.tsv` is either moved or knowingly dropped.

## Next after Task 0 — rename the firmware krinik → KCCP

Owner, 2026-11-08: the custom firmware is renamed from **krinik** to **KCCP** (Krinik Custom CrossPoint). Docs of this repo
already say KCCP. In the firmware fork it is still krinik:
- [ ] version string `2.0.0-krinik…` → `…-kccp…` (the OTA check compares the CrossPoint part — keep it working), env names
  `x4pro-krinik*` / `simulator_x4_pro_mama`, on-device strings, the fork README, the Russian guide `РУКОВОДСТВО.epub`;
- [ ] next releases and tags as `kccp-<version>`; released `krinik-*` tags, branch names and image file names stay as history;
- [ ] build, host tests, simulator, then the owner checks on the reader before any release.

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

## Code map — where the code lives

**Rule (owner, 2026-11-08):** the fork `MikalaiKryvusha/crosspoint-reader` exists only to send pull requests to upstream `develop` — keep it
clean. KCCP releases live in **this repo** (all of them: `kccp-1.1.2` and the historical `krinik-*` / `v2.0.0-krinik.1`).
- [ ] Owner decision (Russian interview on the PC): where the KCCP firmware branches (`nikolai`, `release/*`, `wip/*`, `pr-assets`) live
  instead of the fork, then move them and leave the fork with `develop` and `pr/*` only.

The firmware code is not in this repo; it is in the owner's public forks.

| What | Repo · branch | HEAD |
|---|---|---|
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
