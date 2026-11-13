# STATUS — Krinik Custom CrossPoint (KCCP)

Updated 2026-11-13 13:54 +03:00 (new chat: debug9 verdict, idea 07). Licence: MIT (owner, 2026-11-08: «как у оригинального CP, или MIT»); fonts OFL, firmware images GPLv3.
 Moved off the owner's laptop, where it lived as a loose folder (`~/Xteink`) beside an unrelated
work project. From now on it is a standalone project.

## Where to continue

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
  it; `rotate()` turns one way); answered «можно», offered for debug10 together with idea 05 — waits for his go-ahead.
- **First steps next chat:**
  1. `node D:/work/ai_sandbox/_tools/machine-lock.mjs status` and `ListAgents` (shared PC: KUMM, KAGO).
  2. **The rest of the owner's debug9 check (homework 04, steps 2, 4–7).** When he says the reader is on the cable (book screen, NOT USB drive):
     `.pio-venv/Scripts/python.exe -I -X utf8 tools/serial_log.py <scratch>/serial_debug9.log` in the background; watch
     `Image tap`, `Back swipe`, `[ERR]`, `OOM` (the debug image logs at LOG_LEVEL=1 — INF and up). His verdict → homework
     04 «Итог», `ideas/02` closure, `testcases/TC_idea02…` C6.
  3. **Idea 05 → `/plan-task`** (the agreed design above; code map `researches/2026-11-13_idea05_06_code_map.md`), then code on `wip/krinik-debug10` from debug9: settings
     storage of tile order/visibility, the «Плитки шторки» screen (reuse it for idea 06 «Кнопки главного экрана»), the
     shade row (variable tiles, equal gaps, long tap → Settings), icons, strings; judge → simulator → image.
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
  2026-11-13 11:47, not checked yet (homework 04). Debug2–8 history: `PROJECT_HISTORY.md`.
- [ ] Precise temperature rework (owner, 2026-11-08): dithering only at brightness **≤ 9 %**, off at **10 %** (now it runs up to the
  duty of 10 %).
- **KCCP 1.1.2** (frontlight) is published: https://github.com/MikalaiKryvusha/Krinik-Custom-CrossPoint/releases/tag/kccp-1.1.2 (2026-11-08,
  bilingual notes, Latest; the image still says `cp-2.0.0-krinik-1.1.2` inside).
- "Mama" build with OPDS/plugins: the Home menu has 8 rows and the "Mama" row runs off the screen — fix before the next mama build.

### Hardware research and the tiles idea

- Closed 2026-11-13; moved verbatim to `PROJECT_HISTORY.md` (entry 2026-11-13, STATUS trim 2). The configurable
  shade tiles are `ideas/05` now.

## Code map — where the code lives

**Rule (owner, 2026-11-08):** the fork `MikalaiKryvusha/crosspoint-reader` exists only to send pull requests to upstream `develop` — keep it
clean. KCCP releases live in **this repo** (all of them: `kccp-1.1.2` and the historical `krinik-*` / `v2.0.0-krinik.1`).
- [ ] Owner decision (Russian interview on the PC): where the KCCP firmware branches (`nikolai`, `release/*`, `wip/*`, `pr-assets`) live
  instead of the fork, then move them and leave the fork with `develop` and `pr/*` only.

The firmware code is not in this repo; it is in the owner's public forks.

| What | Repo · branch | HEAD |
|---|---|---|
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
