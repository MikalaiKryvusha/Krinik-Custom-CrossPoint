# Krinik Custom CrossPoint — External structure map

> **The EXTERNAL map: what the project looks like from the outside** — its directories, files, and the
> cross-references and dependencies between them. This is the "where things live" map a fresh session
> reads to navigate. Its companion is `PROJECT_ARCHITECTURE_INTERNAL_MAP.md` (the *internal* logical
> architecture — the abstractions and how they interact).
>
> Adapt the vocabulary to the project's **sphere**: for software — directories, files, modules; for a
> research/writing/business project — sections, documents, datasets, artifacts. Keep it in sync with the
> real tree. **Living reference — never DONE-tagged.**

---

## The tree

```
KCCP/                         # the reader workspace — NO firmware source here (code map: STATUS.md)
├── restore.mjs               # sets up a CrossPoint reader over Wi-Fi from this folder (settings, fonts, books)
├── settings.json             # the owner's reader settings, read by restore.mjs
├── panel_curve.txt           # panel tone curve (256 levels) the firmware reads from the card
├── fonts/                    # reader fonts (Literata …), OFL; build: tools/build_fonts.py
├── РУКОВОДСТВО.epub · КАЛИБРОВКА.epub · guide_settings_section.xhtml   # Russian on-device guide + calibration book
├── covers/ · sleep/ · docs/  # book covers, sleep-screen previews, README images
├── firmware-builds/          # KCCP/krinik images *.bin + *.SHA256SUMS.txt (sources in the forks)
├── tools/                    # EPUB repair/lint, sleep-image prep, fonts, reader backup, simulator runner
├── kuips-runner/             # package.json pinning KUIPS v1.3.0 (UI test runner); `npm install` restores it
├── qa_runs/                  # evidence: simulator runs (log + shots), build logs, PR preparation, measurements
├── researches/ · research/   # analyses (dated, mostly Russian); research/ is the older spelling
├── interviews/               # owner interviews + recorded decisions (decisions/*.json)
├── legacy/                   # laptop-era README/STATUS/HANDOVER/HISTORY (Russian archive) + left-on-laptop.tsv
├── STATUS.md · GOAL.md · MASTER_PLAN.md · AGENT_GUIDE.md …   # KAIF canon (KAIF_FRAMEWORK.md lists it)
├── plans/ ideas/ bugs/ homeworks/ reports/   # KAIF working dirs (each with its README)
├── testcases/                # case sets TC_<feature>.md + reports/<date>_<work>.md (run reports, kaif-testrun-lint)
├── .kaif/ · .claude/ .agents/ .grok/ .cline/ .roo/   # KAIF machinery and agent skills
├── simulator/                # (ignored) clone of MikalaiKryvusha/crosspoint-simulator, branch windows (native Windows port)
├── epub-linter/              # (ignored) sub-project: clone of MikalaiKryvusha/Krinik-EPUB-Linter (Python CLI that checks and
│                             #   repairs the owner's books; developed here, lives in its own GitHub repo)
├── .pio-venv/                # (ignored) PlatformIO Core venv for this PC
└── firmware/                 # (ignored) clone of MikalaiKryvusha/crosspoint-reader + freeink-sdk submodule;
                              #   firmware/platformio.local.ini (ignored) holds this PC's simulator envs
```

## What each part is

| Path | What it is | Depends on / references |
|------|-----------|-------------------------|
| `restore.mjs` | one-command reader setup over the reader's File Transfer web server | `settings.json`, `fonts/`, the reader's IP |
| `firmware-builds/` | released and debug images with checksums | built in `firmware/` (`pio run`), published as GitHub releases of THIS repo |
| `tools/sim_run.sh` | one simulator run: fresh card copy → scripted input → shots + log; refuses a script item without `<ms>:` or earlier than the one before it in its WAIT segment (exit 2); an in-script `<ms>:SHOT:<name>` with a bare name is saved to `qa_runs/<run>/shots/<name>.bmp` (2026-11-13; before, the simulator wrote it into `firmware/` with no extension) | `firmware/.pio/build/simulator_x4_pro*/program`, `qa_runs/sd_template` (or `SD_TEMPLATE`), `tools/shot_webp.py`, `F:\ai_sandbox\msys64\ucrt64\bin` (SDL2.dll) |
| `tools/host_tests.sh` | the full host suite of `firmware/` (build + `ctest -j1`, temp files in `.tmp/`) diffed against `tools/host_tests_known_failures.txt`; exit 1 on a new failure | `firmware/build/test` (CMake, Ninja), `F:\ai_sandbox\msys64\ucrt64\bin` |
| `tools/shade_gaps.py` | measures a shade shot: the content edges, the buttons, the gaps; exit 1 when the gaps spread more than 2 half-scale px (the old equal-slot row: 34) | Pillow in `.pio-venv/` |
| `tools/shot_diff.py` | compares the same-named WebP shots of two simulator runs (status bar cut, threshold for WebP noise); exit 1 on a difference — the layout golden | Pillow in `.pio-venv/` |
| `tools/shot_crop.py` | crops a shot around a box, ×6 with a 10 px labelled grid — to measure a simulator TAP target (EXP-0032) | Pillow in `.pio-venv/` |
| `epub-linter/` | sub-project Krinik EPUB Linter (`krinik_epub_linter.py`: `survey` · `fix` · `check` · `proofread` · `textfix`; pytest in `tests/`) — the owner's books are checked and repaired here, including the figure caption pairs (`krinik_figures.py`, run by `fix`; moved from the removed `tools/figure_retypeset.py`, the owner 2026-11-18 08:49); venv `epub-linter/.venv` (`pip install -e ".[dev]"`), tests `epub-linter/.venv/Scripts/python.exe -m pytest -q`; commits go to its own repo `MikalaiKryvusha/Krinik-EPUB-Linter` | Python 3 stdlib; LanguageTool for `proofread` |
| `tools/guide_screens_check.py` | every `<b>name</b>` of the guide's «Настройки: X» chapters must appear on a simulator screen of that chapter (runs `qa_runs/guide_*` with `CROSSPOINT_SIM_SCREEN_TEXT=1`); exit 1 on a miss; `--selftest` (plan 15) | the capture runs; Python stdlib |
| `tools/clean_run_cards.sh` | removes `qa_runs/<run>/sd` (the card copy) of NAMED runs before their evidence is committed; refuses globs and runs whose `sd/` git tracks (EXP-0031) | git, sh |
| `tools/stamp_guard.py` | before a commit: the staged lines' moment stamps (`YYYY-MM-DD HH:MM ±HH:MM`, ISO) must not be ahead of the clock (EXP-0027/0030); exit 1 on one; `--selftest` | git; Python stdlib |
| `tools/hooks/pretool-deny-server-timeout.mjs` | PreToolUse hook (not wired yet — the owner's step): refuses a review-page launch under `timeout` | Node; `.claude/settings.json` |
| `.tmp/` | (ignored) the agents' temporary files and the tools' logs — the only temp place (`HOUSE_RULES.md` П1) | — |
| `qa_runs/` | dated evidence per run, PR bodies and queue (`prs-2026-11-06/queue.json`) | written by the tools and by the agent; filtered for publication |
| `README.md` | bilingual storefront (English, then Russian) with the roadmap table | `docs/`, releases, upstream PR list |
| `legacy/` | archive — read, never extended | — |

## Cross-references & dependency rules

- Firmware code changes happen in `firmware/` (the fork) and never land in this repo; this repo gets only the
  built image, its SHA256 and the evidence.
- Private or third-party bulk (test books, BMP art, Wi-Fi files, vendor firmware) stays off this public repo —
  `legacy/left-on-laptop.tsv` lists what stayed on the laptop.
- `legacy/` is an archive: active rules move into the KAIF canon (Task 0 step 4), never edited in place.

## Entry points

1. `STATUS.md` — where we are, Task 0, the code map.
2. `README.md` — what KCCP is, the roadmap.
3. `legacy/README.ru.md` — the device setup guide (until it moves into README).

---

> Keep this map honest: when you add, move or rename a file/directory, or LEARN that the tree or the table
> says otherwise than the disk, fix them in the same turn. The *internal* logic (abstractions, data/interaction flows) belongs in
> `PROJECT_ARCHITECTURE_INTERNAL_MAP.md`.
