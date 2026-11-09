# STATUS — Krinik Custom CrossPoint (KCCP)

Updated 2026-11-08 10:40 UTC. Licence: MIT (owner, 2026-11-08: «как у оригинального CP, или MIT»); fonts OFL, firmware images GPLv3.
 Moved off the owner's laptop, where it lived as a loose folder (`~/Xteink`) beside an unrelated
work project. From now on it is a standalone project.

## Where to continue

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

- Last install confirmed by the owner: **krinik 1.1.1-debug5** (owner, 2026-11-08: precise temperature and the Home "Sleep" item are
  done and tested on the reader).
- [ ] Precise temperature rework (owner, 2026-11-08): dithering only at brightness **≤ 9 %**, off at **10 %** (now it runs up to the
  duty of 10 %).
- Battery log every 20 min is a **DEBUG ONLY** aid — keep it out of release builds.
- Debug line: debug3 (precise temperature), debug4 (battery log tick every 20 min), debug5 (= debug4 + "Sleep" item in the Home
  menu under "Flashlight"). Images and SHA256 in `firmware-builds/`; evidence in
  `qa_runs/precise-temperature-2026-11-06/`, `qa_runs/debug4-2026-11-06/`, `qa_runs/debug5-sleep-menu-2026-11-06/`.
- The debug2–5 code was uncommitted on the laptop; it is now `wip/krinik-debug5` in both forks (see the code map). The debug2 image
  itself is in `firmware-builds/` (`cp-2.0.0-krinik-1.1.1-debug2.bin`).
- **KCCP 1.1.2** (frontlight) is published: https://github.com/MikalaiKryvusha/Krinik-Custom-CrossPoint/releases/tag/kccp-1.1.2 (2026-11-08,
  bilingual notes, Latest; the image still says `cp-2.0.0-krinik-1.1.2` inside).
- "Mama" build with OPDS/plugins: the Home menu has 8 rows and the "Mama" row runs off the screen — fix before the next mama build.

### Hardware research

- Closed 2026-11-08: no charging cut-off (needs a board modification); the charger analysis and the battery/light
  measurements moved verbatim to `PROJECT_HISTORY.md` (entry 2026-11-09, STATUS trim).
- LED driver/current/ratings still unknown; UI 80 % on the log scale ≈ 21.4 % duty, not 80 % current.

### Future (owner, 2026-11-06: "on the future")

- Configurable Control Center tiles in a separate menu (add Sleep/Flashlight, hide Bluetooth/Clean). Recon:
  `src/activities/util/FrontlightPanelActivity.*`, `kTileCount`, `runTile(idx)`, `buildPanelScreen`.

## Code map — where the code lives

**Rule (owner, 2026-11-08):** the fork `MikalaiKryvusha/crosspoint-reader` exists only to send pull requests to upstream `develop` — keep it
clean. KCCP releases live in **this repo** (all of them: `kccp-1.1.2` and the historical `krinik-*` / `v2.0.0-krinik.1`).
- [ ] Owner decision (Russian interview on the PC): where the KCCP firmware branches (`nikolai`, `release/*`, `wip/*`, `pr-assets`) live
  instead of the fork, then move them and leave the fork with `develop` and `pr/*` only.

The firmware code is not in this repo; it is in the owner's public forks.

| What | Repo · branch | HEAD |
|---|---|---|
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

- `restore.mjs`, `settings.json`, `fonts/`, `РУКОВОДСТВО.epub`, `КАЛИБРОВКА.epub`, `covers/`, `guide_settings_section.xhtml` —
  the owner's reader setup (how-to in `legacy/README.ru.md`).
- `firmware-builds/` — own krinik images with SHA256 files (sources in the forks above).
- `tools/` — font build, image and analysis scripts. `kuips-runner/` — `npm install` restores it.
- `researches/`, `research/`, `interviews/` — analyses and owner interviews (Russian).
- `qa_runs/` — evidence of builds, tests, PR preparation (logs, diffs, frames), filtered for publication.
- `sleep/` — sleep-screen previews; the BMP files themselves stayed on the laptop.
- `legacy/` — the laptop-era README, STATUS, HANDOVER, PROJECT_HISTORY (Russian) and `left-on-laptop.tsv`.

## Left on the laptop — not published

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
