# STATUS — Krinik Custom CrossPoint (KCCP)

Updated 2026-11-13 16:41 +03:00 (chat 13:51 → 16:21 closed: debug10 = ideas 07/08 + epic 01 Ф1). Licence: MIT (owner, 2026-11-08: «как у оригинального CP, или MIT»); fonts OFL, firmware images GPLv3.
 Moved off the owner's laptop, where it lived as a loose folder (`~/Xteink`) beside an unrelated
work project. From now on it is a standalone project.

## Where to continue

- **Day loop since 2026-11-13 19:01 +03:00 — the owner:** «работай автономно над читалкой, со сборкой не торопись, она
  мне пока не особо нужна. Работаем по фичам KCCP» · «дневной цикл». The debug1 IMAGE waits (no build, no card, no
  homework delivery until asked); the loop works the KCCP features: epic 01 Ф2 → Ф3, idea 06, idea 09, idea 03.
  The debug1 judge (19:00) found `frontlight_dither` red at `d56b53e9` (a fade check kept the old 10 % threshold) —
  observed red, fixed (threshold = the 9 % duty), green on all three configurations, red on the old gate (control).
  Draft homework for the image: `homeworks/06_kccp_1.1.3_debug1.md` (build data placeholders ⟨…⟩). Release-time debt
  (judge): `README.md` / `USER_GUIDE.md` describe fractional mixing as always on and battery as «still being
  measured» — fix before KCCP 1.1.3 ships.
- **Unparked 19:06:** debug1 got its test fix (`84c33f85`); the Ф2 screen was popped from the stash onto the new line
  `wip/kccp-1.1.3-debug2` (= debug1 + Ф2, then Ф3) and the stash is dropped. Next: judge of the whole Ф2 diff →
  simulator cases `testcases/TC_epic01_p2_tiles_screen.md` → commit.
- ~~**PARKED: epic 01 Ф2 screen «Кнопки в шторке»**~~ ([NOW]) — the owner 18:52 «может ты готов мне сборку 1.1.3-debug1
  собрать? Или там много работч ещё?» → the debug1 image first. The screen's uncommitted work (the rework of
  `ShadeTilesActivity` to the mockup `homeworks/05_shade_mockups/final.html` step 2 + the first judge's findings, cut
  mid-way by the 17:19 limit) is `git -C firmware stash list` → «epic01 F2 screen WIP …» on `wip/krinik-debug10` (the only
  copy: the patch backup lay in `D:\Temp`, which the owner deleted 18:56 — temp files now live in `.tmp/`,
  `HOUSE_RULES.md` П1). Resume: `git -C firmware checkout wip/krinik-debug10`
  → `git -C firmware stash pop` → finish the rework → judge → build → simulator.
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
- **KCCP 1.1.3 = the next release; 1.1.3-debug1 NOW for the reader — the owner 2026-11-13 17:07 +03:00:** «да, всё, что
  сейчас есть, собираем в 1.1.3 - это будет наш очередной релиз. соответственно, для меня, для тестов на железе. пока
  можешь собрать отладочкую сборку 1.1.3-debug1» (the answer to the agent's 17:05 question «называем 1.1.3-debug1 и
  вливаем 1.1.2?»; earlier 17:03 «какие фичи поставит мне 1.1.3-debug1 ?»). In work: a new line from debug10 `ed5e2f0d`
  + release 1.1.2 `198d385e` merged (frontlight conflicts) + `[krinik] version = 1.1.3`, env suffix `-debug1` → judge →
  build → host tests → simulator smoke → image + SHA256 + homework. `[AI]` the «Кнопки в шторке» screen (epic 01 Ф2) is
  NOT in debug1: the shade does not read its row until Ф3 — it comes with Ф3 in debug2 (said to the owner 17:08).
- **The shade's elements are «кнопки» — the owner 2026-11-13 17:06 +03:00:** «Плитки шторки - переименовать в "Кнопки в
  шторке"» · «это не плитки, это Кнопки». Applied 17:07: the screen and the on-device strings, the meta-plan, MASTER_PLAN,
  plan 03, the cases, the map, code comments. Russian texts say «кнопка»; code identifiers (`ShadeTiles`, `Tile`) and
  English agent docs keep "tile"; the owner's own past quotes are left verbatim.
- **First steps next chat:**
  1. `node D:/work/ai_sandbox/_tools/machine-lock.mjs status` and `ListAgents` (shared PC: KUMM, KAGO).
  2. **Epic 01 Ф2, step P2.2-end / P2.3** by `plans/03_epic01_p2_tiles_screen.md`: paste the ▲ ▼ icons from
     `python -I -X utf8 tools/make_icon.py tri_up icon_tri_up_32` (and `tri_down`) into
     `firmware/src/components/icons/customListIcons.h`; write `ShadeTilesActivity` on `UiAppHost` (not `UiListActivity` —
     the list hides row rects; see the plan's P2.1 findings), the entries (`SettingsSection::ShadeTiles` after idea 08's
     pattern; `goToShadeTiles(tile, fromBook)`), strings; judge BEFORE the build; simulator run; then Ф3 (the shade row,
     «Сон», «Фонарик», icons, the long tap), Ф4 (the debug10 image + homework).
  3. **Idea 06 «Кнопки главного экрана»** reuses the Ф2 screen — its own epic after epic 01 (the owner asked 16:21
     whether it comes in the next chat: yes, if the window allows after the shade).
  4. The owner's debug9 check (homework 04, steps 2, 4–7) is superseded by the debug10 image (it carries everything of
     debug9); his verdict on picture opening (13:51 «работает») is recorded.
- **Open work, in order:**
  1. Epic 01 (idea 05) + idea 06; 2. Idea 09 (open a picture in the orientation that fits its shape — plan; the halves and
     touches then follow that orientation, `ideas/07`); 3. Idea 03 (re-typeset tool + firmware `<figure>`); 4. KCCP 1.1.3
     assembly: merge release 1.1.2 (`198d385e`) into the debug line (conflicts `lib/hal/HalFrontlight.{cpp,h}`,
     `test/frontlight_dither/`); the owner's open choice: light-linger hold (400 ms) vs timer-redraw hold; 5. Idea 04
     (epic). 6. Bug 01 PR `pr/library-tab-fit` — a free upstream slot (5/5) + proofreading. 7. `bugs/05`, `bugs/06`.
     8. The test hook does not see `tools/sim_run.sh` / ctest runs: a `testHook` block in `.kaif/kaif.json` — to be asked.
     9. Idea 08 S6: the on-device guide `guide_settings_section.xhtml` (the nine sleep options now under «Настройки сна»).
     10. Proofread `GOAL.md`. 11. Delete the partial `C:\msys64` (check the machine lock).
  - Reviews to read: simulator PR #62 and firmware PRs #4328 #4332 #4375 #4376 #4377
    (`gh api repos/<owner>/<repo>/pulls/<n>/comments --jq '.[]|select(.created_at>"<last read>")'`).
- KNOWLEDGE: the image viewer keeps the renderer in the picture's orientation and the keys in the reading orientation
  (internal map, `ideas/07`); one physical gesture has several input names and consumers — gate the touch frame
  (EXP-0016); simulator scripts need `<ms>:` on every item and rising times inside a WAIT segment — now a guard in
  `tools/sim_run.sh` (EXP-0015); the clock placeholder is filled only by Write/Edit, not by scripts (EXP-0012); the full
  host-test suite on this PC is 773/781 with 8 native-Windows failures (research 01); MSYS2 lives in `F:\ai_sandbox\msys64`
  (AGENT_GUIDE Build); Settings sub-screens past `SettingsSection::End` (internal map); `python -I` ignores `PYTHONUTF8`
  — use `-X utf8`; Settings screens are portrait while the reader and its shade follow the reading orientation.

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
| 1.1.3-debug2 (in work) = debug1 + epic 01 Ф2 screen «Кнопки в шторке» (uncommitted in `firmware/`, judge running) → then Ф3 | crosspoint-reader · `wip/kccp-1.1.3-debug2` | 84c33f85 + tree |
| 1.1.3-debug1 = debug10 + release 1.1.2 merged (`c6998e86`) + version 1.1.3 / `-debug1` + «Точная температура» ≤ 9 % (`d56b53e9`) + the dither test fix (`84c33f85`) — local, not pushed; two judges passed; NO image (the owner 19:01: not needed yet) | crosspoint-reader · `wip/kccp-1.1.3-debug1` | 84c33f85 |
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
