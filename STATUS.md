# STATUS — Krinik Custom CrossPoint (KCCP)

Updated 2026-11-08 10:40 UTC. Licence: MIT (owner, 2026-11-08: «как у оригинального CP, или MIT»); fonts OFL, firmware images GPLv3.
 Moved off the owner's laptop, where it lived as a loose folder (`~/Xteink`) beside an unrelated
work project. From now on it is a standalone project.

## Where to continue

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
     smoke `qa_runs/smoke_2b150595`; PR `94e1c3a2` local, NOT pushed (x4pro compile check running). NEXT: reader on
     `G:` → copy debug7 + card cleanup + eject → owner runs homework 02 → push `94e1c3a2`, reply CodeRabbit #4376.
     Owner's open choice: the linger hold (400 ms) vs the redraw hold (≈ reset-to-sample) rules differ.
     #4377 `:115` truncated-card finding — decline draft to proofread. CI on `c9d69cbd`.
  3. Card cleanup, PENDING (`[OWNER] 2026-11-09 20:09 «и образы старые поудаляй»`; rule: current debug + previous
     debug + latest release): on the next reader connect (`G:`) delete from `/.firmware/` `…-debug3.bin`,
     `…-debug4.bin`, `…-debug5.bin`, `crosspoint-2.0.0-x4pro.bin`, `cp-2.0.0-pr4376-2dbfff7d.bin`; keep debug7 + debug6 +
     1.1.2; then eject (`AGENT_GUIDE.md` → The device).
- **Open work, in order:**
  1. **Simulator upstream PR** (owner «делай» 20:13): research 01 → "Upstream PR readiness" — the in-script `SHOT`
     after a second `WAIT` saves nothing (reproduced 20:14, `qa_runs/shot_probe2`; main loop `simulator_main.cpp:17-32`
     next to read), then File Transfer, curl, sleep/wake relaunch, clock, the sample ini as written, squash, PR text.
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

Moved verbatim to `PROJECT_HISTORY.md` (entry 2026-11-08, "Left on the laptop") on 2026-11-09; per-file list in
`legacy/left-on-laptop.tsv`.
