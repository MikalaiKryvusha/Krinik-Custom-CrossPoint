# STATUS — Krinik Custom CrossPoint (KCCP)

Updated 2026-11-17 15:39 +03:00 (the 14:42 day loop: homework 08 shown, epic 07 Ф3 tool, epic 05 Ф5, plan 15 the guide). Licence: MIT (owner, 2026-11-08: «как у оригинального CP, или MIT»); fonts OFL, firmware images GPLv3.
 Moved off the owner's laptop, where it lived as a loose folder (`~/Xteink`) beside an unrelated
work project. From now on it is a standalone project.

## Where to continue

- **DEBT — the 1.1.3 release judge pass** (`/fable-judge` over the published `kccp-1.1.3` notes and the README 1.1.3
  rows: every claim against firmware `c1c38089` vs `198d385e`, the Known list, EN = RU) — skipped on the owner's word
  `[OWNER] 2026-11-17 22:00 · chat: «судью отзывай, нет на него времени» · «судейство - наш долг на потом»`; a refuted
  claim is corrected where it stands (the release body via `gh release edit`, the README). Also not done before the
  release: the full 1.1.3 regression pass on the simulator (features were run phase by phase) and the owner's
  proofreading of the README and the notes.

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
- **Bug 08** (the shade's night button leaves pictures under the sheet negative, `bugs/08_…`): upstream issue
  #4515 opened 2026-11-17 10:24 +03:00 — `[OWNER] 2026-11-17 10:21 «Пофиксить бы, в будущем. Пока как баг заведи и нам
  и в апстрим»` (`bugs/08_…`); watch it, the fix waits for its answer.
- **❓ homework 09** (`homeworks/09_guide_settings_proofread.md`): the page did not work for the owner (21:49 «Кратко
  блять и тезисно»); the four lines and three A/B questions went to him in chat 21:51 as theses — his answer awaited.
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
