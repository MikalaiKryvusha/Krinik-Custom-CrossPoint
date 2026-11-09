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
