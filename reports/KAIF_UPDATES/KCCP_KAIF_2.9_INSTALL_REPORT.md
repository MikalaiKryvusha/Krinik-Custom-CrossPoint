# KCCP — KAIF 2.9 (+2.10 WIP) install report

**Delivered upstream:** https://github.com/MikalaiKryvusha/KAIF/issues/195

Project: Krinik Custom CrossPoint (KCCP) — reader workspace repo (docs, images, evidence; firmware lives in forks).
Host: Windows 11, Claude Code (VS Code extension), model Claude Opus 5.5, auto permission mode. Node v24.15.0.
Source: `--source https://raw.githubusercontent.com/MikalaiKryvusha/KAIF/d2f21274d3964d2d246bdc75d4e9f5b3e844e9af/dist`
(manifest `version 2.9`, `prerelease 2.10`, source tree `3aa4b346ba3b`, 216 files). Params: `--lang ru`, mode standard.

## 1. Chronology (2026-11-09, +03:00)

- 14:16 `KAIF.md` fetched from `main`; main SHA recorded via `gh api repos/MikalaiKryvusha/KAIF/commits/main`.
- 14:17 `KAIF-LOADER.mjs` extracted verbatim (149 lines) from the FILE block.
- First loader run — DENIED by the Claude Code auto-mode classifier (no reason given). Owner approved in chat, verbatim: «разрешаю»; second run exit 0.
  Loader: 2 artifacts sha256 ok; core wrote 8 owner docs (ru), 37 skills × 5 agent systems, `KAIF_ADAPTATION_TASK.md` (11 items).
  Existing `STATUS.md` kept (`= kept existing STATUS.md`).
- 14:24 study done (9 re-read core docs read in full; refresh marker stamped by `date -Iseconds`).
- project-name → "Krinik Custom CrossPoint" (owner, chat question); 6 seeded H1s corrected by hand.
- placeholders filled (build: `pio run -d firmware -e x4pro-krinik-debug`; harness: ctest + simulator + device); 175 mirrors re-synced.
- owner-voice: public snapshot copied from the KAIF repo, `/AUTHOR_STYLOMETRY.md` ignored in the same step (repo is public).
- wire-hooks — DENIED by the auto-mode classifier; recorded with `checkpoint wire-hooks --verdict`.
- sphere programming; GOAL via a 3-question owner interview (`interviews/interview_002_goal.md`); MASTER_PLAN derived.
- `check` flagged 7 template slots in end-chat-soft/end-chat-force/release; filled with project commands.

## 2. Friction and rakes

1. **`checkpoint maps` passes on untouched templates.** Both map Writes failed (`File has been modified since read`,
   after a `sed` heading fix) and the agent ran `checkpoint maps` in the same parallel batch: `✔ recorded: KAIF-ADAPT:
   maps done` while both maps still held `<path>` / `<name>` placeholders. Caught by the agent, maps then filled.
   Improvement: the maps checkpoint could refuse while the shipped placeholder rows (`| \`<path>\` |`, `| \`<name>\` |`)
   are present — the placeholders checkpoint already scans this way.
2. **The shipped ru `KAIF_FRAMEWORK.md` fails the shipped voice lint.** `kaif-voice-lint check KAIF_FRAMEWORK.md` on
   the seeded template: `✖ KAIF_FRAMEWORK.md:23 — «здесь»`, `:30 — «здесь»` (headings «Зачем он здесь», «Как это
   работает здесь»). Every ru install with the public portrait hits it. Fixed locally (headings renamed).
3. **Fresh install already warns on budget:** `⚠ entry cost: AGENT_GUIDE.md ~ 36k tokens — over the 25k one Read call
   returns`. The agent cannot act on it at install (the size is the shipped canon).
4. **Hooks need a settings write the harness may refuse.** In Claude Code auto mode both `node KAIF-LOADER.mjs` and
   `node .kaif/kaif-core.mjs wire-hooks` were denied with no reason. The verdict path worked as designed; the owner
   gets one command (`node .kaif/kaif-core.mjs wire-hooks`).
5. Worked as designed: `voice-lint check` refused `MASTER_PLAN.md` as "written past the portrait" (template mtime
   before the first load) — correct, the file was then rewritten.

Separate tickets for items 1–2 were NOT filed; they are listed here for the KAIF owner to triage.

## 3. What confused a cold agent (top 3)

1. "2.9 release + 2.10 WIP": `--channel main` vs a pinned `--source <sha>`; the manifest answers it (`version 2.9`,
   `prerelease 2.10`), but only after fetching it by hand.
2. The study item says "record findings" without naming where; the agent put them into AGENT_GUIDE Build/Test/Git
   sections and the maps.
3. The placeholders item lists `.kaif/spheres/<sphere>.md` before the sphere item runs; order of items vs dependencies.

## 4. Final state and judge verdict

- `node .kaif/kaif-core.mjs check`: `✅ manifest satisfied: 110 files + 152 agent artifacts present`; warnings: 15 hooks
  not wired · AGENT_GUIDE entry cost.
- `node .kaif/tools/kaif-voice-lint.mjs selftest`: 66 cases OK. `check GOAL.md MASTER_PLAN.md KAIF_FRAMEWORK.md`: 0 findings.
- Owner text: GOAL/MASTER_PLAN written after `voice-lint load`, machine check 0 findings, then a clean-subagent §7B pass:
  19 findings reported; verified against the files — 5 factual (wrong PR queue counts, a misquoted menu defect, a
  proofread PR listed as unread, two decisions stated as done while still planned) and the rest stylistic; all
  applied, re-checked 0 findings. One finding rejected (CodeRabbit source = the owner's chat, unseen by the subagent).
- `/fable-judge` pass over the install: **VERIFIED WITH CAVEATS.**
  - Re-run: placeholders grep → 0 hits in AGENT_GUIDE and all 5 skill trees; template `\`<` slots in maps/GOAL/
    MASTER_PLAN/KAIF_FRAMEWORK → 0; `git check-ignore` → portrait, markers, `KAIF.md`, loader all ignored; `check` above.
  - Caveat 1 (closed 2026-11-09 14:38 +03:00): hooks were not wired by the agent (harness refusal); the owner ran
    `node .kaif/kaif-core.mjs wire-hooks` himself — `15 of 15 KAIF hooks added`; `check` no longer warns.
  - Caveat 2: `checkpoint maps` was recorded before the maps were filled (friction 1); filled later in the session.
  - Caveat 3: build/test commands in AGENT_GUIDE are documented, NOT run — no `pio`, `cmake`, `firmware/` on this PC
    (UNVERIFIABLE here; Task 0 step 2).
  - Caveat 4: pre-existing, untouched: `kaif-attribution-lint` flags `STATUS.md:65`; `kaif-provenance check` fails on
    nested `[AI]` marks in `researches/2026-11-05_additional_upstream_candidates.md`.
  - Caveat 5: GOAL text sits in `[AI]` marks awaiting the owner's acceptance.
  - Experience recall: `EXPERIENCE.md` is the fresh template — no relevant lessons.
