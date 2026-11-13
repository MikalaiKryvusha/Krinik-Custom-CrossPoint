# Krinik Custom CrossPoint — Internal architecture map

> **The INTERNAL map: the project's logical architecture** — the abstraction objects the project's sphere
> works in, their essence, and how they interact. Where `PROJECT_STRUCTURE_EXTERNAL_MAP.md` says *where
> things live*, this says *how the system thinks*. A fresh session reads this to understand the model, not
> just the file layout.
>
> **Adapt the abstractions to the sphere:**
> - *Programming* — modules, interfaces, objects, data structures, data flows, state, protocols.
> - *Science* — hypotheses, variables, models, datasets, methods, inference chains.
> - *Sociology* — subjects, objects, institutions, roles, the relations between them.
> - *Business* — actors, processes, value flows, resources, constraints.
> - …and so on for any sphere. If unsure, describe the domain's nouns and the verbs that connect them.
>
> **Living reference — never DONE-tagged.**

---

## The core abstractions

| Abstraction | What it *is* (essence) | Responsibility |
|-------------|------------------------|----------------|
| **Upstream CrossPoint** | `crosspoint-reader/crosspoint-reader`, branch `develop` | the base KCCP builds on and gives back to |
| **The fork** | `MikalaiKryvusha/crosspoint-reader` (+ `freeink-sdk`) | carries `pr/*` branches for upstream PRs; KCCP lines (`nikolai`, `release/*`, `wip/*`) are moving out |
| **KCCP build** | a firmware image from a fork branch (`x4pro-krinik[-debug]`) | what the owner's and his mother's X4 Pro readers run |
| **Debug line** | `wip/krinik-debug5` (debug2–5) | features tested on the reader before a release |
| **Upstream PR** | one `pr/<topic>` branch + body + before/after frames | moves a feature proven on the reader into CrossPoint |
| **Reader setup** | `restore.mjs` + `settings.json` + fonts + guide EPUBs | reproduces the owner's reader state |
| **Panel curve** | `panel_curve.txt` from KEINKT Calibrator | maps gray levels to how the e-ink panel really shows them |
| **Evidence** | `qa_runs/<run>/` | proves what a build or a PR does (logs, shots, measurements) |

## How they interact

```
upstream develop ──fork──▶ pr/* ──PR (owner proofreads text)──▶ upstream review ──merge──▶ upstream develop
        │
        └──▶ KCCP branches ──pio run──▶ image ──SD card──▶ X4 Pro (owner tests) ──proven──▶ pr/* candidate
                                         │
                                         └──▶ firmware-builds/ + GitHub release (this repo)
KEINKT Calibrator ──phone photos──▶ panel_curve.txt ──card──▶ KCCP draws pictures / sleep screens through it
simulator (tools/sim_run.sh) ──shots + log──▶ qa_runs/ ──▶ PR frames, regression checks
```

## Firmware code the PR work touches (in `firmware/`, not this repo)

- `src/main.cpp` — boot `setup()` (wake cause, X4 Pro timer-redraw wake) and `enterDeepSleep()` (sleep screen via
  `ActivityManager::goToSleep()`, then the redraw timer is armed from `SleepActivity::lastCustomImagePath()`).
- `src/activities/boot_sleep/SleepActivity.cpp` — draws the sleep screen; records the custom image path for the
  delayed redraw (#4376) and repaints it on the timer wake (`redrawCustomImage`).
- `lib/Epub/Epub/parsers/ChapterHtmlSlimParser.cpp` — expat XHTML → text blocks → pages; queues anchor ids and
  places them on pages (#4328); a malformed chapter is a parse error, `finishParse()` closes the last page.
- `src/activities/reader/EpubReaderActivity.cpp` — the EPUB reader: `loop()` routes input in priority order (overlay →
  long press = clip selection → Home-button actions → link tap (`currentPageLinks`, beats the zones) → centre tap = menu →
  Back → side taps / swipes / buttons = page turn); the page render keeps the current page's links for hit-testing.
- `src/activities/util/BmpViewerActivity.cpp` — the file browser's full-screen image viewer (BMP/JPEG/PNG through the
  panel curve, cache `/.crosspoint/view_*.bmp`, siblings of the folder, long tap rotates); opened by
  `ActivityManager` (`ActivityManager.cpp:345`).
- `firmware/platformio.local.ini` (ignored) — this PC's native Windows simulator envs (research 01).
- `simulator/src/HalStorage.cpp` — the simulator's SD card over a host folder (`CROSSPOINT_SIM_SD`); `replaceFile`
  mirrors the device's remove-then-rename (a bare `rename` cannot overwrite on Windows, found 2026-11-09).

## Invariants & rules of the model

- A feature reaches upstream only after it works on the real reader (the owner's word on the device).
- At most five open upstream PRs per author; PRs are never closed to free a slot.
- No outward text (PR, issue, review reply) without the owner's proofreading.
- The reader is eFuse-locked: SD card is the only flashing path.
- Debug-only aids never ship in a release image.

## Key decisions embedded in the architecture

- Firmware lives in forks, the workspace in this repo — the fork stays clean for upstream review
  (`[OWNER] 2026-11-08 · STATUS.md → code map`).
- Name: KCCP (Krinik Custom CrossPoint); `krinik-*` tags and image names stay as history
  (`[OWNER] 2026-11-08 · STATUS.md → "Next after Task 0"`).

---

> Keep this in sync with the real logic: when you LEARN how a part works, or see it differ from this map, and
> when you introduce, retire or rewire an abstraction — the line here changes in the same turn. File/directory placement belongs in
> `PROJECT_STRUCTURE_EXTERNAL_MAP.md`.
