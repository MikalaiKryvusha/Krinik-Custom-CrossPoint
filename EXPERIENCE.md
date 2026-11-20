# EXPERIENCE — the agent's accumulated experience

> The agent's growing log of lessons. **Externalized memory of *what works and what doesn't*** — so a
> fresh, context-less session (or an autonomous loop) never repeats a dead end. Consult it BEFORE a task;
> append to it AFTER a meaningful attempt (success **or** failure). Grep, don't scroll.
>
> **Tags live inline on every entry** (not in a central list) — so one grep finds the experiences directly:
> `grep '#loop' EXPERIENCE.md` · `grep -i '#context\|#build' EXPERIENCE.md` · `grep '❌' -A4 EXPERIENCE.md`
> · `grep 'EXP-0007' EXPERIENCE.md`. Reuse an existing tag where one fits (grep to see what's in use).
>
> **Entry format (keep it short and grep-friendly).** Newest on top. Every entry starts with a stable id,
> an ISO date, an outcome marker (`✅` / `❌` / `❌→✅`), and inline `#tags`:
>
> ```
> ### EXP-0001 · 2026-01-01 · ✅ · #tag #area
> class: <slug from the class list below — the UNIT OF RECURRENCE>
> **Context:** one line — what was being done.
> **Tried / did:** the approach, briefly.
> **Result:** ✅/❌ — what happened.
> **Lesson:** the reusable takeaway (the reason this entry exists).   → link: bugs/NN · ideas/NN · plans/NN
> **Repro:** the ready-to-run command/check that verifies or applies the lesson — a weak session
>   executes a pasted command reliably, an essay it won't act on. REQUIRED since 2.1: a lesson
>   with no Repro line is not accepted (field-proven: lessons with a Repro command get executed,
>   essay-lessons get read and ignored). If the lesson genuinely has no command, say what to
>   OBSERVE instead — but say it as an action.
> **Trigger:** for class-level lessons — the decision point that must invoke this lesson, as
>   "writing X → run Y" (the lesson names WHERE it applies, instead of hoping to be remembered).
> **Not for:** the lesson's validity range — where it does NOT apply. A documented lesson is still a
>   hypothesis; applied outside its range it kills good ideas.
> ```
>
> **A lesson that repeats is a lesson that failed as text.** When the same class recurs in NEW code
> after its entry was recorded, the journal has proven insufficient — the lesson MUST become
> executable (a linter rule, a guard, a gate), and the entry gains the line
> `mechanized: <the tool>`. Two strikes → a mechanism, never a third reminder.
>
> **The deadline is RUN, not remembered** (2.7, epic EL; origin issue #69 — a field audit of one
> project's journal: 14 of 15 failure classes recurred AFTER their lesson was written, five lessons
> written 6–17 times in different words, 5.8 % mechanized): `node .kaif/tools/kaif-experience-lint.mjs
> check` reads the `class:` field as the UNIT of recurrence and reddens on the SECOND failure entry of
> one class with no `mechanized:`, naming the class and both entries by id. Two fates clear it, both
> WRITTEN: name the guard in the entry (`mechanized: <the tool>`), or re-check the price once for the
> WHOLE class and declare it — `<!-- class-ok: <slug> — <why it is not cheaply possible> -->` (an empty
> declaration is itself a finding; the declared classes are printed on the summary line and that list
> only shrinks). A third record is never a fate. It also warns when
> `mechanized:` names a command this project does not contain, and when a slug is outside the list
> below; `--shrink EXP-NNNN` collapses a MECHANIZED entry to one line pointing at its guard (shows by
> default, `--yes` writes — the text itself stays in the git history). The command belongs in the
> closing ritual (`/end-chat-soft`).
>
> **The class list of this journal** — a CONTROLLED list, not a closed one: pick a slug from it, and
> when a lesson genuinely brings a new class, add the slug here in the same write (the linter warns
> about an unlisted slug, it never refuses). The starter list below is what a field audit had already
> measured (origin issue #69) — replace and grow it with your project's own classes.
>
> <!-- classes: question-already-answered, guard-not-proven-against-threat, shown-as-link,
>      claim-before-evidence, owner-decision-not-applied, text-in-agents-world,
>      etalon-from-dirty-tree, shell-lied, escaping-layer, twins-missed,
>      field-dropped-in-rebuild, shared-machine-not-checked, ritual-run-by-hand,
>      overwrote-tracked, tool-crash, false-defect, wrong-directory, missing-dependency, own-process-killed,
>      wrote-outside-project, suite-not-run, owner-as-tester, guessed-instead-of-measured, fixture-not-real-data -->
>
> | Class slug | The failure it names |
> |---|---|
> | `question-already-answered` | the owner is asked what his own past word, the goal doc or a run already decided |
> | `guard-not-proven-against-threat` | a guard shipped without being seen red on the threat it claims to stop |
> | `shown-as-link` | showing replaced by a link or a path instead of the thing itself |
> | `claim-before-evidence` | a claim written wider than the observation behind it |
> | `owner-decision-not-applied` | a decision the owner gave is recorded and not carried into the artifact |
> | `text-in-agents-world` | text written for the agent's own world instead of the owner's |
> | `etalon-from-dirty-tree` | a reference/etalon captured from a tree that was not clean |
> | `shell-lied` | the shell or the tool swallowed/rewrote what was passed to it |
> | `escaping-layer` | one escaping level lost between the tool and the file |
> | `twins-missed` | one of two layers/copies moved and the twin stayed behind |
> | `field-dropped-in-rebuild` | a field or section silently lost when an artifact was regenerated |
>
> The `#tags` are **trigger-tags**: before a task, grep by the task's tags and QUOTE the relevant
> lessons in your report (id + one line) — or state "no relevant lessons". An unquoted recall is
> unverifiable; `/fable-judge` checks for this line.
>
> Skill: `/experience` (capture a lesson · recall relevant lessons).

## Entries

### EXP-0043 · 2026-11-20 · ❌ · #owner #wording #translation #bugs
class: text-in-agents-world
none-cheap: a chat sentence is not machine-checkable; the carrier is the Trigger below
**Context:** /resume entry; the canon term «the owner's debt» (a bug he flagged, a decision he answered) rendered in the
chat as «твой долг: новый баг 17» and the photo as «твой новый баг».
**Result:** ❌ the owner, 2026-11-20 14:16 +03:00: «МОЕГО БАГА???? Я НИ СТРОЧКИ КОДА НЕ НАПИСАЛ!» · «ПРОЕКТ ТВОЙ!». In
Russian «твой баг» reads as «the bug you made»; the code, the project and every defect in it are the agent's.
**Lesson:** a bug the owner found is «баг, который ты нашёл»; «the owner's debt» is «долг перед тобой»; a defect is
never attributed to the owner in any wording — the canon's English possessive is translated by meaning, not by word.
**Repro:** before sending, read every «твой/твоя/твоё» in the reply next to «баг», «долг», «ошибка» aloud — none may stand.
**Trigger:** writing to the owner about a bug, a defect or a debt.
**Not for:** his decisions and his words («твой ответ», «твоё слово») — those are his.
**Second face, same day (16:11):** three questions put in the agent's terms («нижняя граница порога 160», «BMP в обзоре
файлов», «порог ×2 для N») → «1 не понимаю · 2 не понимаю · 3 не полнимаю»; re-asked as what he will see (the dark tree
whose edges break; .bmp sleep pictures left as they are; soft vs sharp by how much a picture is enlarged). Before sending a
question: name what he sees on the screen, not the parameter (`/interview` step 3a, the scenario lines).

### EXP-0042 · 2026-11-20 · ❌→✅ · #fonts #metrics #geometry #judge #simulator
class: guessed-instead-of-measured
none-cheap: the carrier is the run — a geometry rule is accepted only with its simulator shot measured by tools/shot_rows.py
**Context:** bug 16 squeeze — two judges proposed an «air» gate between lines from font metrics (the advance; then
ascender + descender + 1 px); both were built.
**Result:** ❌ on the owner's page both gates blocked every gap inside a paragraph: Literata's max ascender + descender (and
its advance) exceed the 37 px pitch of his «+10 %» spacing, while the rendered ink keeps 3 px between lines — the squeeze
moved 1 px instead of 7–10. ✅ the gate removed; the text-only rule and the 1 px cap guard collisions.
**Lesson:** font metrics are maxima of the whole font, not the ink of a line; a spacing rule derived from them (mine or a
judge's) is accepted only after the stand shows its effect on the owner's page in numbers.
**Repro:** `.pio-venv/Scripts/python.exe -I -X utf8 tools/shot_rows.py <before.webp> <after.webp>` → the line bands moved as
the rule promises.
**Trigger:** writing a layout condition on ascender / descender / advance / line height.
**Not for:** the parser's own pagination clamp (it frames the full glyph box on purpose).

### EXP-0041 · 2026-11-20 · ❌→✅ · #simulator #stand #geometry #real-data
class: fixture-not-real-data
mechanized: `simulator/src/BoardConfig.h` XTEINK_X4_PRO viewableInsets = the SDK device profile {9, 7, 3, 7} (branch `fix/x4pro-viewable-insets`); proven by the row profile below
**Context:** bug 16 mock-up — a 5 px gap above the status bar printed a page pixel-identical to «today» on the simulator.
**Result:** ❌ the stand's X4 Pro had the default insets {9, 3, 3, 3}; the device has {9, 7, 3, 7}: in landscape the page sat
4 px higher and the bar 4 px lower than on the reader (sim text 22…443 / bar 454 vs reader 26…446 / 450), so a 3 px defect
looked like 11 px. ✅ the simulator profile = the device's; the bar now lands on 450–465 as on the owner's screenshot.
**Lesson:** a geometry bug is reproduced only after the stand's frame is matched to the owner's screenshot by numbers
(row profile of both); a stand board profile is checked against the SDK device profile, not trusted.
**Repro:** `.pio-venv/Scripts/python.exe -I -X utf8 tools/shot_rows.py <reader shot.webp> <sim shot.webp>` → the status bar band equal.
**Trigger:** any spacing/margin bug judged on the simulator.
**Not for:** content bugs (which line breaks where) — those also need the owner's book (П4), not just the frame.

### EXP-0040 · 2026-11-20 · ❌ · #build #wait #subagent #owner
class: claim-before-evidence
none-cheap: a turn ended to wait is a chat act no repository tool sees; the carrier is the Trigger below
**Context:** a background agent built upstream `develop` (`x4pro`) in its own worktree `.tmp/upstream_develop` for the flash
report; I held my simulator build and ended two turns «waiting», reading «one PlatformIO build at a time» as a machine lock.
**Result:** ❌ the owner: «тебя это не держит. у тебя хватает работы». The rule's reason is the SAME tree: `pio run -e x4pro`
in `firmware/` wipes `firmware/.pio/build/simulator_*`; a worktree has its own `.pio`, so the two builds do not touch.
**Lesson:** before waiting on another job, name what exactly it blocks (a file, a folder, a lock); a build in another tree
blocks nothing of mine — start my build and take the next task in the same turn.
**Repro:** `ls <worktree>/.pio/build` vs `ls firmware/.pio/build` — different folders → build in parallel.
**Trigger:** about to end a turn «waiting for» a background agent or build.
**Not for:** two builds in the same `firmware/` tree (they do wipe each other's outputs).

### EXP-0039 · 2026-11-18 · ❌→✅ · #qa_runs #glob #mv #tracked
class: overwrote-tracked
mechanized: `sh tools/park_runs.sh <dest> <run…>` — moves named runs to `.tmp/<dest>/`, refuses a run git tracks (proven on `cap_look_A`)
**Context:** parking today's GEB runs (third-party text) out of `qa_runs/` with `mv qa_runs/cap_* .tmp/b14_runs/`.
**Result:** ❌ the glob also took the tracked homework-08 runs `cap_look_A…D`; caught at once by EXP-0031's
`git status --short | grep '^ D'` (8 files); ✅ moved back. EXP-0031's tool covers `rm` of `sd/`, not `mv` of runs.
**Lesson:** moving or deleting runs goes through a script that checks each run against git, never a prefix glob.   → link: EXP-0031
**Repro:** `sh tools/park_runs.sh probe cap_look_A` → `REFUSED`.
**Trigger:** any `mv`/`rm` of whole runs under `qa_runs/`.
**Not for:** files inside `.tmp/`.

### EXP-0038 · 2026-11-18 · ❌→✅ · #regex #python #linter #epub #real-data
class: fixture-not-real-data
mechanized: `epub-linter/tests/test_figures.py::test_no_break_space_runs_stay_linear` (red on the old regex in 15 s, green 0.5 s budget) + `HOUSE_RULES.md` П4
**Context:** the caption binder moved from `tools/figure_retypeset.py` into Krinik EPUB Linter; its self-test (9 mutants)
had passed on our own test book on 2026-11-17.
**Result:** ❌ `survey` on the owner's GEB ran > 5 min: the blank-text regex `(?:\s|&nbsp;|…|\xa0)*$` — `\s` already
matches U+00A0, so a run of N no-break spaces (GEB's poem indents) backtracks 2^N ways (22 → 0.27 s, ×4 per 2 more). ✅
`not ENTITY.sub('', t).strip()`; the whole book binds in 0.12 s.
**Lesson:** a tool proven on our fixture is not proven on the owner's book; and a regex `(A|B)*` whose alternatives can
match the same character is exponential on a long run of it — keep alternatives disjoint or drop the regex.
**Repro:** `epub-linter/.venv/Scripts/python.exe -m pytest -q epub-linter/tests/test_figures.py -k linear`.
**Trigger:** writing a `*`/`+` over an alternation; finishing any book tool before a run on the owner's copy.
**Not for:** regexes whose alternatives start with distinct literal characters.

### EXP-0037 · 2026-11-18 · ❌→✅ · #temp #env #host-tests #shell
class: wrote-outside-project
mechanized: `TARGETS="<Test …>" sh tools/host_tests.sh` — targeted host tests with the script's own PATH/TEMP/TMP (red on a known list missing one name)
**Context:** bugs 14/15 — running two host-test programs by hand, the environment typed in one line:
`export PATH=… TEMP=$(cygpath -w …) TMP=$TEMP`.
**Result:** ❌ `$TEMP` expanded BEFORE the assignment, so `TMP` kept the harness's `F:\Temp`; the parser tests (which take
`std::filesystem::temp_directory_path()`, TMP first on Windows) left four files there. ✅ removed; the script mode written.
**Lesson:** a second strike of EXP-0017's class: temp paths come from the project's script, never from a hand-typed
environment; in one `export` a variable cannot feed the next.   → link: EXP-0017
**Repro:** `TARGETS="ChapterHtmlSlimParserTest CssParserTest" sh tools/host_tests.sh` → `no new failure`; `ls /f/Temp/crosspoint-*` → none.
**Trigger:** running any host-test program outside the full `sh tools/host_tests.sh`.
**Not for:** the simulator (`tools/sim_run.sh` sets its own folders).

### EXP-0036 · 2026-11-17 · ❌ · #fork #release #owner-rule #repeat
class: question-already-answered
mechanized: `HOUSE_RULES.md` П3 (read at every entry)
**Context:** the 1.1.3 release needed its firmware source published.
**Result:** ❌ I asked the owner «A — archive in the KCCP release / B — a branch in the fork, as 1.1.2», though his rule
(2026-11-08, STATUS code map) says the fork is for upstream PRs only. The owner: «сколько раз тебе повторять».
**Lesson:** an option that breaks a standing owner rule is never offered; the house rules are checked before writing a
question's options.
**Repro:** `grep -n "П3" HOUSE_RULES.md`.
**Trigger:** any question whose options touch the fork, a release or where code lives.
**Not for:** —

### EXP-0035 · 2026-11-17 · ❌ · #testing #owner #release #gate
class: owner-as-tester
mechanized: `HOUSE_RULES.md` П2; the AGENT_GUIDE device line rewritten
**Context:** the owner asked «мы готовы выпускать релиз 1.1.3?»; earlier the same evening I sent him «что проверить на
читалке» lists with debug4 and debug5.
**Result:** ❌ I named «your check on the reader» as the release's first condition; the owner: «с каких это пор Я бля
тестировщик у тебя, а НЕ ТЫ???». The canon already said it (TESTING_FRAMEWORK: «never "the owner will test"»), but the
AGENT_GUIDE device line («the functional run on the real reader is the owner's») and the [AI] GOAL line («релиз, который
я проверил на устройстве») taught the opposite.
**Lesson:** readiness = the agent's own test pass with its report; the owner's use is not a test and never a gate; what
the simulator cannot show is said as «not verified on the reader» with the agent's own next way to observe it.
**Repro:** `grep -n -i "owner's check\|проверил на устройстве" STATUS.md GOAL.md MASTER_PLAN.md bugs/*.md` → empty.
**Trigger:** writing a readiness answer, a release gate or a «what to check» line.
**Not for:** taste verdicts (look, sound, text) — those are his.

### EXP-0034 · 2026-11-17 · ❌→✅ · #guard #frame #layout #shade
class: guard-not-proven-against-threat
mechanized: `tools/shade_gaps.py` measures the end gaps from the shot's edges (the sheet's visible edges) by default
**Context:** epic 01 Ф3 (13.11) «equal gaps» in the shade's button row, measured by `shade_gaps.py`.
**Result:** ❌ the guard measured from the slider row's edges — the same 16 px inset the layout used — so it passed a
row whose ends were 16 px + gap; the owner saw it on the reader (bug 12, 20:51). ✅ the guard's frame = the eye's frame,
red on the debug4 shot (spread 9), green on the fix.
**Lesson:** a layout guard measures in the frame the PERSON sees (the visible edge), never in the frame the code laid
out in — the same frame cannot disagree with the code.
**Repro:** `tools/shade_gaps.py qa_runs/bug12_before/shots/shade_home.webp port` → exit 1.
**Trigger:** writing a guard for spacing, alignment or centring.
**Not for:** guards over values the person never sees.

### EXP-0033 · 2026-11-17 · ❌→✅ · #reader #claim #owner #back
class: claim-before-evidence
<!-- class-ok: claim-before-evidence — the class lives in chat sentences and handover prose, which no repository tool reads; the price was re-checked 2026-11-17 22:08: the guard is the judge's claim-wider-than-observation hunt (both entries were caught by a judge or a command run), a text linter would not see the chat -->

none-cheap: a chat sentence is not machine-checkable; the judge read the code
**Context:** bug 11 (a note's backlink); telling the owner what he will see after the fix.
**Result:** ❌ I wrote «the next Back swipe then leaves the book» from memory; the judge read `ReaderUtils.h:277` — at
footnote depth 0 the X4 Pro's edge swipe is not a Back (it turns the page back, seen in run `bug11_green`). ✅ corrected
in chat and in `bugs/11`.
**Lesson:** what the owner will SEE after a change is read from the code path or a run before it is said, never
reasoned from how a gesture «usually» works.
**Repro:** `grep -n wasBackGesture firmware/src/activities/reader/ReaderUtils.h`.
**Trigger:** promising the owner a screen or a gesture result.
**Not for:** behaviour already shown in a run's shots or log.

### EXP-0032 · 2026-11-17 · ❌→✅ · #simulator #tap #coordinates #shots
class: guessed-instead-of-measured
none-cheap: a coordinate read off a shot by eye has no check except the run itself
**Context:** bug 09 runs on the owner's book: tapping a footnote link «[4]» in landscape (orientation 3).
**Result:** ❌ six runs missed: the link's place guessed by eye on the half-scale shot was ≈ 80 px off, and I chased
rotation theories instead. ✅ `simulator/src/HalGPIO.cpp` `logicalToPanelNormalized`: a script's 0–1 TAP is LOGICAL in
the CURRENT orientation (= the shot's own axes); a 6× grid crop of the shot gave the exact box, the next tap hit.
**Lesson:** TAP x,y = (shot px ×2) / (800−1, 480−1) for landscape, (480−1, 800−1) for portrait — measure the target's box
on a grid crop of the shot, never by eye.
**Repro:** `.pio-venv/Scripts/python.exe -I -X utf8 tools/shot_crop.py <shot> .tmp/crop.png x0 y0 x1 y1`; then the TAP.
**Trigger:** a TAP on a small target (a link, a marker) in a simulator script.
**Not for:** big targets (Home rows, buttons) the earlier reports already give coordinates for.

### EXP-0031 · 2026-11-17 · ❌→✅ · #qa_runs #glob #cleanup #tracked
class: overwrote-tracked
mechanized: `tools/clean_run_cards.sh <run…>` — removes only named runs' `sd/`, refuses tracked files and globs (proven on `guide_after`)
**Context:** plan 15 captures named `qa_runs/guide_*`; their card copies removed with `rm -rf qa_runs/guide_*/sd`.
**Result:** ❌ the glob also hit `qa_runs/guide_after/sd` and `guide_before/sd` — a 2026-11-08 run committed WITH its card
(`7a52b12`); 8 tracked files deleted in the tree (not committed: the commits named their paths). ✅ `git checkout --`.
**Lesson:** a cleanup names the runs it made, never a prefix glob; `git status --short | grep '^ D'` after any `rm -rf`
under `qa_runs/`.
**Repro:** `git status --short | grep '^ D'` → empty after a cleanup.
**Trigger:** `rm -rf` with a glob under `qa_runs/`.
**Not for:** `.tmp/` (ignored, nothing tracked there).

### EXP-0030 · 2026-11-17 · ❌→✅ · #stamps #clock #recurrence #guard
class: claim-before-evidence
mechanized: `tools/stamp_guard.py` — staged lines with a stamp ahead of the clock → exit 1 (proven on a staged probe)
**Context:** the 14:42 day loop — plan 15 progress lines written through `sed` and a Python script.
**Result:** ❌ EXP-0027 twice more in one session: «15:33» at a real 15:32, «15:46» at a real 15:45 — the lesson was
in the journal and in context. ✅ both replaced by a log mtime / «≈»; a guard written.   → link: EXP-0027
**Lesson:** a text lesson does not hold a stamp typed by feel; the stamp guard runs before every commit that carries
stamps written outside Write/Edit (the clock hook covers those).
**Repro:** `.pio-venv/Scripts/python.exe -I -X utf8 tools/stamp_guard.py` after `git add`.
**Trigger:** a commit whose staged text carries a moment written by `sed`/`python`.
**Not for:** stamps the clock hook filled (the NOW placeholder in Write/Edit).

### EXP-0029 · 2026-11-17 · ❌→✅ · #crlf #python #firmware #windows #recurrence
class: shell-lied
mechanized: `tools/host_tests.sh` refuses CRLF in firmware sources (EXP-0019) — but only when it runs; this time the edit came AFTER the host run
**Context:** epic 05 Ф5 — flipping `[NOT-TESTED]` markers in four firmware files with a one-off `pathlib.write_text` script,
after the host suite had already run green.
**Result:** ❌ all four files became CRLF (`git diff --stat` +1425/−1320) — EXP-0019 repeated: the recall grep before the
script covered the task's tags (home, long tap), not the tool (python writing firmware). ✅ caught by the diff stat before
the commit; `sed -i 's/\r$//'`; `git ls-files --eol` → `i/lf w/lf`.   → link: EXP-0019
**Lesson:** a scripted edit in `firmware/` writes bytes (`write_bytes(t.encode())`) and is followed at once by
`git -C firmware ls-files --eol -- <files>`; a green host run before the edit proves nothing about it.
**Repro:** `git -C firmware diff --stat` after the script — a whole-file count means line endings.
**Trigger:** any script that rewrites a file under `firmware/`.
**Not for:** Edit/Write tool edits (they keep the file's endings).

### EXP-0028 · 2026-11-17 · ❌→✅ · #contour #review #mockup #decision #names
class: overwrote-tracked
mechanized: `.kaif/tools/contour/core.mjs` refuses to overwrite another document's decision record (bugs/KAIF/01, origin #199; probe red on the original, green on the patch)
**Context:** epic 07 Ф2 — a second mock-up picture made by the same compose script as #005's, both named `compare.webp`
in two `qa_runs/` folders, about to be shown on the contour's mock-up face.
**Result:** ❌ the contour names a decision file by the BARE file name (`interviews/decisions/compare.decision.json`): the
new verdict would have replaced the owner's #005 answer for every reader of it. ✅ Caught by reading `decisionPaths` before
the show; the picture renamed `caption_look.webp`; a local guard; ticket delivered.
**Lesson:** a picture or page that goes to the owner gets a name unique across the project — the record of his verdict is
keyed by it; before a show, `ls interviews/decisions/<name>.decision.json` must say «No such file».
**Repro:** `ls interviews/decisions/$(basename <picture> | sed 's/\.[^.]*$//').decision.json` → must not exist.
**Trigger:** `review.mjs <picture> --mockup` (and any `review.mjs <doc>` show of a new document).
**Not for:** a document shown again for the SAME question (its own record is expected there).

### EXP-0027 · 2026-11-17 · ❌→✅ · #stamps #clock #reports
class: claim-before-evidence
mechanized: .kaif/hooks/clock-now.mjs fills the NOW placeholder — on Write/Edit only; this face is the bypass
**Context:** epic 07 Ф1/Ф2 run reports and statuses filled by `python` text replacement during a fast loop.
**Result:** ❌ moments typed by feel, some ahead of the clock (11:44–11:51 written at a real 11:42); the clock-now hook never
saw them — it fills the placeholder only in Write/Edit. ✅ Replaced by log mtimes / commit times or marked ≈ (`5807c28`).
**Lesson:** a run's moment comes from its artifact — `date -r <log> '+%H:%M'`, the commit's `%ad` — or a probe in the same
call; a stamp written through a script bypasses the clock hook, so the script reads the moment itself.
**Repro:** `for f in qa_runs/<run>/log.txt; do date -r $f '+%H:%M'; done`; `git log -1 --format=%ad --date=format:%H:%M`.
**Trigger:** writing a run table or a status stamp through `python`/`sed`.
**Not for:** stamps written with Write/Edit and the NOW placeholder (the hook fills those).

### EXP-0026 · 2026-11-17 · ❌→✅ · #simulator #webp #golden #shots
class: false-defect
mechanized: tools/shot_diff.py (threshold 32, status bar cut; proven to fail on two different runs)
**Context:** epic 07 Ф1 — «books with no figure lay out as before»: the default test book's 8 pages shot before and after.
**Result:** ❌ a raw pixel diff said pages 2, 5, 7 changed (6434 / 7022 / 814 px) though they looked the same. The cause:
WebP q90 is lossy and its encoder segments the whole frame — the status-bar clock changed (07:55 → 08:11) and shifted other
blocks by up to 11 levels. ✅ With a threshold of 32 and the status bar cut: 0 px on all 8 pages; the control (two books)
8067 px.
**Lesson:** a golden over WebP shots compares content above a noise threshold with the clock cut, never bytes; read the
diff's magnitude before calling a layout changed.
**Repro:** `.pio-venv/Scripts/python.exe -I -X utf8 tools/shot_diff.py <before>/shots <after>/shots` → `TOTAL 0`; on two
different runs → exit 1.
**Trigger:** any «nothing else moved» claim made from simulator shots.
**Not for:** a byte check of a file the tool writes (there bytes are the contract).

### EXP-0025 · 2026-11-17 · ✅ · #tests #windows #host #parser
class: suite-not-run
none-cheap: one-off; the known-failures list now names the three remaining tests instead of the whole target
**Context:** epic 07 Ф1 needed parser host tests; `ChapterHtmlSlimParserTest` stood in the known-failures list as
`_NOT_BUILT` since the Windows port (2026-11-09) — the whole layout suite (157 tests) had never run on this PC.
**Tried / did:** read the build errors: 10 lines `file.open(path.c_str(), …)` with a `std::filesystem::path` (`wchar_t*`
on Windows); `path.string().c_str()` on those lines only.
**Result:** ✅ the suite builds and runs here: 155 pass, 3 fail only because Windows cannot delete an open file; the list
names those three; the host count went 803 → 960.
**Lesson:** a `_NOT_BUILT` entry in a known-failures list hides a whole suite; before trusting the host suite for a module,
look at what its `_NOT_BUILT` entries cover and how cheap the build fix is.
**Repro:** `grep NOT_BUILT tools/host_tests_known_failures.txt`; for each, `cmake --build firmware/build/test --target <name>`
and read the first errors in the log.
**Trigger:** starting work on a module whose host test is listed as `_NOT_BUILT`.
**Not for:** targets that fail to build for a missing library (a real port, not a line fix).

### EXP-0024 · 2026-11-17 · ❌→✅ · #contour #review #server #timeout #recurrence
class: own-process-killed
none-cheap: the guard is written and self-tested — `tools/hooks/pretool-deny-server-timeout.mjs` (`--selftest` 6/6) — but wiring a hook into `.claude/settings.json` is refused to the agent by the auto-mode classifier (KAIF_FRAMEWORK.md, 2026-11-09); the wiring waits for the owner (STATUS)
**Context:** showing interviews 005/006 with `timeout 20 node .kaif/tools/contour/review.mjs --queue --silent` — the
second time after EXP-0013 (2026-11-13), whose lesson was in this journal; the session's recall grep covered only the
task's own tags (cover, invert, dark), not the tool it was about to launch.
**Result:** ❌ the page server died at 20 s; the owner saw «СЕРВЕР КОНТУРА НЕДОСТУПЕН» («контур ты сломал», 10:18).
✅ relaunched in the background on the same port 58794, HTTP 200; the owner's answer to #006 was recorded at 10:18.
**Lesson:** EXP-0013 failed as text: recall by the task's tags misses the lesson of the TOOL used mid-task. A launch of
a page server needs a guard that refuses it under `timeout` — a text reminder has now been passed twice.   → link: EXP-0013
**Repro:** before any `review.mjs` call: `grep -n "review.mjs" EXPERIENCE.md`; launch only with `run_in_background`, then
`curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>/` → `200`.
**Trigger:** any `review.mjs` call that is not `--list` / `--check` / `--call` / `--mark-*`.
**Not for:** the print-and-exit flags named above.

### EXP-0023 · 2026-11-17 · ❌ · #upstream #pr #cache #night #twins #firmware
class: twins-missed
none-cheap: the twin is a second cache of the same pixels in another component; the carrier is the Repro grep below
**Context:** upstream PR #4329 (2026-11-04) — the Home cover pasted back as a negative after a night ↔ day switch.
**Tried / did:** the polarity check went into `HomeActivity` around its own snapshot `coverBuffer`; tested on the
single-cover themes. No search for other snapshot caches of the same screen.
**Result:** ❌ merged, then the maintainer reproduced it on «Сетка обложек» (2026-11-16): that theme keeps its own
PSRAM snapshots in `HomeCoverCache`, and `HomeActivity::render` returns into the grid branch before our check. He fixed
it upstream in #4494 (`b9c23473`); KCCP still carries it — bugs/07.
**Lesson:** a fix to a pixel snapshot (store → paste back later) is a fix to EVERY snapshot of that screen: list all
store/paste sites first and walk every theme/branch that reaches them; a theme switch at the top of `render()` is a
second code path, not a detail.   → link: bugs/07
**Repro:** `git -C firmware grep -n -E "copyRegionToBuffer|copyBufferToRegion|storeBwBuffer|restoreBwBuffer" -- src lib`
→ every hit that survives across renders gets the same invalidation; then one run per Home theme (0–4).
**Trigger:** fixing anything that caches framebuffer bytes (covers, overlay pages, bands) against a state change.
**Not for:** store/restore pairs inside one frame with no state change between them.

### EXP-0022 · 2026-11-14 · ❌→✅ · #geometry #judge #simulator #home
class: claim-before-evidence
mechanized: LOG_DBG «Menu geometry» in HomeActivity::onEnter (firmware a47582b0) — the measured numbers are one grep away in every simulator run
**Context:** epic 05 Ф3 — the judge simulated the Home row count for a 480×800 screen and proposed taking
`verticalSpacing` off for Classic, «X4 Pro counts unchanged».
**Result:** ❌ applied: Lyra lost its 7th row on the simulator — the real content bottom is 797 (a 3 px viewable inset),
not 800, so (797 − 314 − 16 + 8) / 68 = 6.98 → 6. Found by a shot (6 rows) and then a `LOG_DBG` line with the numbers.
✅ reverted; the measured geometry is in the code comment.
**Lesson:** a geometry fix, mine or a judge's, is accepted only after the REAL numbers are printed on the stand; a
simulation with assumed screen sizes proves the arithmetic, not the screen.
**Repro:** `grep -a "Menu geometry" qa_runs/<run>/log.txt` → `top=314 contentBottom=797 … visible=7` on Lyra.
**Trigger:** any change to a count of rows, pixels or slots derived from screen metrics.
**Not for:** values the code reads at run time from the same source it draws with (no assumption to check).

### EXP-0021 · 2026-11-14 · ❌→✅ · #build #warnings #guard #firmware
class: guard-not-proven-against-threat
mechanized: #pragma GCC diagnostic error "-Wswitch" in src/activities/home/HomeActivity.cpp and src/components/CoverGridHomeUi.cpp (red on a removed case, 2026-11-14)
**Context:** epic 05 Ф2 — comments and plan 08 claimed «-Wswitch names a new button» for the exhaustive switches over
`homemenu::Button`.
**Result:** ❌ the judge: the firmware build (device and simulator) has no `-Wall`, so `-Wswitch` never fires; a button
without its label case would draw one row fewer than the tapped list. ✅ the files turn `-Wswitch` into an error; a
removed case stops the build: «enumeration value 'Sleep' not handled in switch [-Werror=switch]».
**Lesson:** a compiler warning named as a guard is checked in the REAL build's flags (`platformio.ini`, the framework's
`cpp_flags`) and seen red there, never assumed from the warning's name.
**Repro:** remove one `case homemenu::Button::…:` from `tabIconOf` in `CoverGridHomeUi.cpp`, `pio run -e
simulator_x4_pro_win` → `[-Werror=switch]`, `[FAILED]`; restore.
**Trigger:** writing «the compiler will catch it» in a comment, a plan or a commit.
**Not for:** host tests (CMake sets its own flags — check them there separately).

### EXP-0020 · 2026-11-14 · ❌→✅ · #tests #mutation #model #firmware
class: guard-not-proven-against-threat
none-cheap: the test itself is the guard now; the carrier is the Repro mutation below
**Context:** epic 05 Ф1, the Home button model: «Настройки» may not be switched off (`homemenu::canToggle`); the host test
checked the refusal over `defaults()` only, and the mutation proof removed the lock entirely.
**Result:** ❌ the judge's mutant `return index != 4;` (refuse by ROW, not by button) passed all 11 tests in both builds —
Ф4 calls `canToggle` at a row after the owner moves «Настройки» with ▲ ▼. ✅ the test now also checks «Настройки» moved
up and parsed first; the positional mutant goes red (`SettingsStaysOn`, plain and mama).
**Lesson:** a rule keyed on an ITEM of a reorderable list is tested with the item at a moved position too, and the
mutation proof includes the "keyed on the position" mutant, not only "rule removed".
**Repro:** in `src/util/HomeMenuButtons.h` replace `return !isLocked(list[index].button);` with `return index != 4;`,
rebuild `HomeMenuButtonsTest HomeMenuButtonsMamaTest`, `ctest -R HomeMenuButtons` → `SettingsStaysOn` Failed ×2; restore.
**Trigger:** writing a test for a per-item rule of any user-ordered list (shade tiles, Home buttons).
**Not for:** rules that are positional by design (the first/last row of a list).

### EXP-0019 · 2026-11-13 · ❌→✅ · #crlf #python #firmware #windows
class: shell-lied
mechanized: tools/host_tests.sh — refuses CRLF in firmware src/ lib/ test/ (tracked or new), red on a header turned CRLF (2026-11-13)
**Context:** patching firmware sources with `pathlib.Path.write_text(...)` from `python -I -X utf8` on Windows.
**Result:** ❌ text mode turned every `\n` into `\r\n`; the firmware clone has `core.autocrlf=false`, so
`ShadeTilesActivity.{h,cpp}` went into `41718c61` as CRLF and the shade's diff showed 1 068 changed lines. Git Bash
`grep -c $'\r'` printed 0 on those files — `git ls-files --eol` told the truth. ✅ `sed -i 's/\r$//'`, `376bcf11`.
**Lesson:** a Python script that writes a source file on Windows passes `newline="\n"` (or writes bytes); line endings are
read with `git ls-files --eol`, never with grep.
**Repro:** `git -C firmware ls-files --eol -- src lib test | grep -E 'i/crlf|w/crlf'` → only the upstream OFL/UFL/hyphenation texts.
**Trigger:** a script that rewrites a file in `firmware/`.
**Not for:** this KCCP repo (`core.autocrlf=true` normalises on commit).

### EXP-0018 · 2026-11-13 · ❌→✅ · #host-tests #suite #firmware
class: suite-not-run
mechanized: tools/host_tests.sh — the full suite diffed against tools/host_tests_known_failures.txt, exit 1 on a new failure (red on a list missing one known name, 2026-11-13)
**Context:** debug10 `8538f3dd` (idea 07, keys keep the reading orientation) added `keyOrientationOf()` to
`src/MappedInputManager.cpp`; its checks were simulator runs and targeted tests.
**Result:** ❌ `RemoteButtonInputIntegration` cuts that file by text and went red; nobody ran the full suite until the
1.1.3-debug1 check (772 of 781 read as «the usual 8 failures» would have hidden it). ✅ the test's stubs fixed (`bcbd6dab`).
**Lesson:** a change in `src/` or `lib/` is followed by the FULL host suite before its commit, compared with the known
failures by a script, never by recalling a count.
**Repro:** `sh tools/host_tests.sh` → `no new failure (known list: 8)`, exit 0.
**Trigger:** about to commit firmware code.
**Not for:** a commit that touches only docs or `qa_runs/`.

### EXP-0017 · 2026-11-13 · ❌ · #disk #temp #scratchpad #owner
class: wrote-outside-project
none-cheap: a PreToolUse hook refusing writes outside the project is a settings change the owner makes; the carrier is HOUSE_RULES.md П1
**Context:** KCCP chats used the harness scratchpad `D:\Temp\claude\…` (named in the system prompt) for a firmware
`git worktree` (`wt113`, the debug1 merge) and a patch backup of uncommitted work.
**Result:** ❌ the owner found `D:\Temp` full of agents' folders: «а что это за свалка? … я не разрешал агентам там
работать» and deleted it himself; the rule since 18:56: temp files inside the project.
**Lesson:** a folder the harness OFFERS is not a folder the owner ALLOWED; the agent's temp files live in `<project>/.tmp/`.
**Repro:** before any temp write, the path starts with `D:/work/ai_sandbox/KCCP/.tmp/`; `git check-ignore -v .tmp/x` → `.gitignore:…:/.tmp/`.
**Trigger:** about to create a worktree, a backup, a download or a script output.
**Not for:** files the harness writes itself (background outputs, subagent transcripts) — their folder is a harness setting.

### EXP-0016 · 2026-11-13 · ❌→✅ · #input #gesture #twins #firmware
class: twins-missed
none-cheap: the twin is a second consumer of one physical gesture; the carrier is the Repro grep below
**Context:** idea 07 — after a turned book picture closes, a second fast swipe must not act in the book. First fix: the
activity manager skipped its control-center swipe while the reader held touch.
**Result:** ❌ the judge: the reader's own menu gesture (`isTouchMenuGesture` → `wasMenuGesture`) is the SAME top-edge
swipe (`wasLightPanelGesture` and `wasMenuGesture` both = `wasTopEdgeDownSwipe`) — silencing one consumer handed the
swipe to the other; link, picture and long-press taps also still acted. ✅ Rework: one gate over the whole touch frame
(`gpio.wasTouchActivity()` → skip + `suppressTouchContact()`), bounded in time.
**Lesson:** to silence touch for a while, gate the touch FRAME before any consumer reads it — never one gesture by
name: one physical motion has several names in the input layer and several consumers.
**Repro:** before silencing a gesture `X`, `git grep -n "was.*Swipe\|Gesture()" -- src lib/hal | grep -i "<the motion>"`
lists every alias and consumer.
**Trigger:** writing any "ignore gesture X while Y" condition.
**Not for:** a gesture with exactly one consumer and no alias (checked by the grep).

### EXP-0015 · 2026-11-13 · ❌→✅ · #simulator #script #wait
class: false-defect
mechanized: tools/sim_run.sh — the script guard refuses an item without `<ms>:` and an item earlier than the one before it in its WAIT segment (red on both scripts below, 2026-11-13)
**Context:** idea 07, the debug9 control run in the image viewer: open a picture, long tap right, long tap left, shots.
**Tried / did:** (1) `WAIT:Entering activity: BmpViewer` with no time — the simulator ran the rest at once: the first shot
and a long tap landed in the book (`ClipSelection`), one turn looked "lost"; (2) after that fix, `1000:TAP` written after
`1500:SHOT` in one WAIT segment — the tap ran before the shot, and `QUIT` before the last shot (EXP-0009's class again).
**Result:** ❌→✅ caught by the ORDER of the log lines (`Saved screenshot` before `Entering activity: BmpViewer`), not by
the shots; the third run with increasing times passed.
**Lesson:** an input that seems lost is first checked against the script grammar: `<ms>:WAIT:<regex>`, times count from
the last WAIT and never go down inside a segment.
**Repro:** `sh tools/sim_run.sh x "1000:TAP:0.5,0.5;WAIT:y;500:QUIT" ''` → exit 2 and the reason, no run folder.
**Trigger:** writing `CROSSPOINT_SIM_INPUT_SCRIPT` with WAIT.
**Not for:** the timed screenshot schedule (the third argument of `sim_run.sh`), which counts from the process start.

### EXP-0014 · 2026-11-13 · ❌→✅ · #show #window #edge #screen
class: shown-as-link
none-cheap: one launch recipe; the carrier is the Repro below
**Context:** showing the shade mockups with `Start-Process msedge --app=file:///…` — the owner: «не понимаю, что ты открыл».
**Result:** ❌ a screenshot showed VS Code in front; the page window was not on his screen. ✅ Relaunched with a position
and size and brought forward with `AppActivate` — the next screenshot shows the page window over VS Code.
**Lesson:** a launched window is not a shown window: bring it forward by its title and look at the screen before saying
it is open. On this PC a plain `CopyFromScreen` captures 1280×720 = only the top-left third of the 4K TV at 300 %.
**Repro:** `Start-Process $edge -ArgumentList '--app=file:///<page>','--window-position=0,0','--window-size=1280,720'`;
`(New-Object -ComObject WScript.Shell).AppActivate("<page title>")` → `True`; then a screenshot shows the title bar.
**Trigger:** any page or picture opened for the owner.
**Not for:** the review contour's own window (it reports its launch; still look before claiming it is seen).

### EXP-0013 · 2026-11-13 · ❌→✅ · #contour #review #server #timeout
class: own-process-killed
none-cheap: one launch rule; the carrier is the Repro below
**Context:** showing homework 04 to the owner with `timeout 60 node .kaif/tools/contour/review.mjs <doc>` — the
`timeout` was meant to keep the tool call from hanging.
**Result:** ❌ `review.mjs <doc>` keeps the page's HTTP server alive; `timeout` killed it at 60 s and the owner saw the
page die («контур упал», 11:45). ✅ Relaunched in the background, page answers HTTP 200.
**Lesson:** a tool that SERVES something the owner looks at runs as a background process, never under `timeout`;
"the call returned" is checked by asking the server, not by the exit of the launcher.
**Repro:** launch with the Bash tool's `run_in_background`, then `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>/` → `200`.
**Trigger:** any `review.mjs <doc>` / page / server launch for the owner.
**Not for:** `review.mjs --queue --list`, `--check`, `--call` — they print and exit.

### EXP-0012 · 2026-11-13 · ❌→✅ · #stamps #clock
class: claim-before-evidence
mechanized: .kaif/hooks/clock-now.mjs — write the NOW placeholder (the word NOW in white square brackets), the hook fills the machine's time on Write/Edit
**Context:** status stamps in ideas 02/04 and a research header, typed by feel while the work ran fast.
**Result:** three stamps 2–4 minutes off (10:50 for a 10:45 plan, 10:58 for 10:56, 11:06 for 11:02) — caught the
same hour against `git log --format='%h %ci'` and corrected in place.
**Repro:** after writing stamps, `git log --format='%h %ci %s' -10` → each stamp ≤ the commit time of its document.
**Trigger:** typing any `HH:MM` of our own moment into a document.
**Not for:** the owner's message times quoted from the clock hook's line. The hook fills the placeholder only in a
Write / Edit / MultiEdit of the file — a script (sed, a heredoc, Python) that writes it leaves it raw: there, put
`$(date …)` into the script instead (2026-11-13: a raw placeholder in `ideas/08`, caught by grep the same minute).
The placeholder is the word NOW in WHITE square brackets — U+27E6 … U+27E7 — an ASCII `[NOW]` is left raw even by
Write/Edit (2026-11-13 19:43 +03:00: two raw `[NOW]` in STATUS and plan 04, found by `git grep -n '\[NOW\]'`).

### EXP-0011 · 2026-11-13 · ❌→✅ · #epub #lint #tools
class: missing-dependency
none-cheap: one-line S3 note; the lint itself should say «xmllint not found» — fix it when the tool is next touched
**Context:** `node tools/epub_lint.mjs` on the generated test book `qa_runs/sd_book_images/image_test.epub`.
**Result:** «✗ … XHTML: ch1.xhtml undefined» — not a book defect: no `xmllint` on this PC (neither PATH nor `D:\msys64`).
**Repro:** well-formedness without xmllint: `.pio-venv/Scripts/python.exe -I -c "import zipfile,sys,xml.dom.minidom as m;z=zipfile.ZipFile(sys.argv[1]);[m.parseString(z.read(n)) for n in z.namelist() if n.endswith(('.xhtml','.opf','.xml'))];print('ok')" <book.epub>`
**Trigger:** an `undefined` in the XHTML lines of `epub_lint.mjs`.
**Not for:** the link/manifest checks of the same lint, which do not need xmllint.

<!-- class-ok: twins-missed — three unlike faces (EXP-0005 a regex rename matching extra C++ sites; EXP-0016 two consumers of one input gesture under different names; EXP-0023 two snapshot caches of one screen in two components); each face carries its own grep Repro, and a guard for the whole class would be a general code-search policy, not cheaply possible; the judge pass before every build is what caught EXP-0016 -->
<!-- class-ok: own-process-killed — two faces of one launch (EXP-0013, EXP-0024: the review page under `timeout`); the guard tools/hooks/pretool-deny-server-timeout.mjs exists and passes its selftest, and only its wiring into .claude/settings.json is the owner's (the agent's hook writes are refused by the classifier) — once wired, this declaration becomes `mechanized:` -->
<!-- class-ok: guessed-instead-of-measured — two unlike faces (EXP-0032 a tap target read by eye on a shot; EXP-0042 a spacing rule derived from font metrics); each face has its measuring tool (tools/shot_crop.py, tools/shot_rows.py) named in its Repro, and a guard against «guessing» in general is not cheaply possible; price re-checked 2026-11-20 -->
<!-- class-ok: shell-lied — two unlike faces of Windows defaults (cp1251 stdout for Python, CRLF checkout); each is closed at its source (PYTHONUTF8=1 in the AGENT_GUIDE Build line, core.autocrlf=false in the firmware clone); a build wrapper that sets both is the mechanism to add next -->

### EXP-0010 · 2026-11-10 · ❌→✅ · #shell #cwd #parallel
class: wrong-directory
none-cheap: absolute paths in every command; the carrier is the Trigger below
**Context:** several Bash calls sent in one message, each starting with `cd <dir> && …` (simulator runs, ini swap).
**Tried / did:** three times the command ran in another folder: `tools/sim_run.sh: No such file`, `./.pio-venv/…: No such
file`, and once my restore `cp …bak platformio.local.ini` wrote the firmware's local ini into the KCCP root while the
firmware kept the swapped-in sample (caught by `git status`; the original was not lost).
**Lesson:** a command that depends on its directory uses absolute paths for every file it writes; parallel calls never
rely on a `cd` — and a restore is checked at its target (`diff`/`grep` on the absolute path) in the same call.
**Repro:** after any swap/restore: `git -C <repo> status --short` for both repos → nothing unexpected.
**Trigger:** batching several shell calls, or any backup → swap → restore of a config file.
**Not for:** single sequential calls whose `cd` succeeded (the cwd persists).

### EXP-0009 · 2026-11-09 · ❌→✅ · #simulator #script #false-defect
class: false-defect
mechanized: tools/sim_run.sh — the script guard (times inside a WAIT segment never go down; added 2026-11-13 when the class recurred, EXP-0015)
none-cheap: one re-read of the tool's README before naming a defect; the carrier is the Repro below
**Context:** the native Windows simulator; a "defect" carried for 6 hours and into the chat handover: «an in-script
`SHOT` stalls after a second `WAIT`», blocking the upstream PR.
**Tried / did:** the probe was `…;800:SHOT:…;500:QUIT`. Script times count from the last matched WAIT (the README says
so), so QUIT ran at 500 ms, before the SHOT — no BMP, no message. I read it as a stall and later "narrowed" it to "after
the second WAIT" from one more probe written the same wrong way.
**Result:** ✅ 2026-11-09 23:50 — 3+ variants on the current binary: SHOT before QUIT saves (one and two WAITs), the old
script verbatim does not, a missing folder logs `Cannot save screenshot`. Not a defect; research 01 corrected.
**Lesson:** before calling a tool broken, check that the input obeys the tool's documented semantics, and make the
probe able to fail for one reason only (a QUIT far after the action under test).
**Repro:** in a script, every time after a WAIT must be larger than the action's it should follow — QUIT last, by a margin.
**Trigger:** writing `CROSSPOINT_SIM_INPUT_SCRIPT`, or concluding "the simulator hangs".
**Not for:** the timed `CROSSPOINT_SIM_SCREENSHOTS` schedule (counts from process start).

### EXP-0008 · 2026-11-09 · ❌→✅ · #shell #grep #stackdump
class: tool-crash
none-cheap: use the Grep tool or `git grep`; the carrier is the Trigger below
**Context:** reading code of other branches with `git show <branch>:<file> | grep …` in Git Bash (CodeRabbit round 3).
**Tried / did:** three times `grep` died with «Aborted (core dumped)» mid-pipe (exit 134) and left a
`grep.exe.stackdump` in the current folder (`firmware/`, the KCCP root) — untracked garbage in the tree.
**Result:** ✅ the output was re-read another way (`sed -n`, `git grep <branch>`); the dumps were moved to `D:\Temp` and deleted.
**Lesson:** Git Bash `grep` on a long piped input is unreliable here; search branch code with `git grep <branch> -- <path>`
or the Grep tool, and check `git status` for `*.stackdump` after a crash.
**Repro:** `git status --short | grep -c stackdump` → 0 after any search session.
**Trigger:** piping `git show` / big output into `grep` from Git Bash.
**Not for:** the Grep tool and `git grep`, which did not crash.

### EXP-0007 · 2026-11-09 · ❌→✅ · #build #git #crlf
class: shell-lied
none-cheap: one clone setting; the carrier is AGENT_GUIDE.md → Build
**Context:** first device build `pio run -e x4pro` on this PC.
**Tried / did:** the build failed: «SdFat patch does not apply: 0001-invalidate-failed-cache-fill.patch» — the
patch file was CRLF in the working tree (global `core.autocrlf=true`), the downloaded SdFat source LF.
**Lesson:** a Windows clone that feeds patches or byte-exact files to a build keeps the repository's line endings.
**Repro:** `git -C firmware config core.autocrlf false`, delete the tracked files, `git -C firmware checkout -- .`
→ `file scripts/sdfat_patches/*.patch` shows no CRLF; the build prints «Applied SdFat patch».
**Trigger:** a fresh clone on Windows that builds firmware or applies patches.
**Not for:** text documents of this KCCP repo.

### EXP-0006 · 2026-11-09 · ❌→✅ · #qa_runs #overwrite #fixtures
class: overwrote-tracked
none-cheap: a one-line check before the write; the carrier is the Repro below
**Context:** making theme cards for the bug 01 runs: `shutil.rmtree` + copy into `qa_runs/sd_theme0…4`.
**Tried / did:** the folders were tracked laptop fixtures (commit 7a52b12); they were overwritten and later deleted as
"scratch" — `git status` showed ` D`; restored with `git checkout -- qa_runs/sd_theme*`.
**Lesson:** a folder name the agent "makes up" may already exist in the repo; look before writing or deleting.
**Repro:** `git ls-files <dir> | head -1` → empty before creating or removing a fixture folder.
**Trigger:** creating, copying over or deleting any folder under `qa_runs/`.
**Not for:** run folders `sim_run.sh` itself recreates (`qa_runs/<run>`), which are the script's by design.

### EXP-0005 · 2026-11-09 · ❌→✅ · #sed #rename #twins
class: twins-missed
none-cheap: one-off bulk rename; the carrier is the Repro grep below
**Context:** porting the simulator's socket shims to Winsock: `sed 's/::close(/simCloseSocket(/g'` over three files.
**Tried / did:** the pattern meant global `::close(fd)` calls; it also matched the method definition
`WebSocketsServer::close()`, which became `WebSocketsServersimCloseSocket()` — caught only by the compiler (build 4).
**Lesson:** a qualified-name pattern (`::name(`) also matches `Class::name(` definitions; anchor it to what precedes.
**Repro:** after a bulk rename, `grep -nE "[A-Za-z0-9_]<new>|<new>\(\)" <files>` → 0 hits.
**Trigger:** writing a `sed`/regex rename of a C++ name.
**Not for:** renames done by a compiler-aware tool.

### EXP-0004 · 2026-11-09 · ❌→✅ · #build #shell #encoding
class: shell-lied
none-cheap: one shell rule; the carrier is AGENT_GUIDE.md → Build
**Context:** `pio run -e simulator_x4_pro_win` started from Git Bash in the background.
**Tried / did:** the `gen_i18n.py` pre-script wrote Cyrillic through cp1251 → `UnicodeEncodeError`; `pio` did not
exit and sat idle for 15 minutes; the owner asked «ну?». The same build from PowerShell had passed four times.
**Lesson:** on this PC build from PowerShell and set `PYTHONUTF8=1`; a background build gets a monitor that also
matches a stall, not only the exit line.
**Repro:** `$env:PYTHONUTF8 = "1"; .pio-venv\Scripts\pio.exe run -d firmware -e simulator_x4_pro_win` → `[SUCCESS]`.
**Trigger:** starting any PlatformIO build here.
**Not for:** the simulator run itself — `sh tools/sim_run.sh` from Git Bash works.

### EXP-0003 · 2026-11-09 · ❌→✅ · #closing #ritual #hooks
class: ritual-run-by-hand
none-cheap: the hook keys on the Skill call by design; the carrier is the Trigger below and the KAIF ticket (issue #195 comment)
**Context:** closing the chat at the owner's named time (15:00) with `/end-chat-soft`.
**Tried / did:** read `.claude/skills/end-chat-soft/SKILL.md` with `sed` and walked its steps by hand — never called the
skill through the Skill tool.
**Result:** ❌→✅ — `stop-farewell-capture.mjs` saw no closure in the turn and wrote no
`FAREWELL_MESSAGE_FROM_THE_PREVIOUS_CHAT.md`; the owner asked «Почему это не написано в прощальный документ?»; the file
was then written by hand with the farewell verbatim.
**Lesson:** a KAIF ritual is RUN through its skill invocation (Skill tool `end-chat-soft` / `end-chat-force` / `resume`),
never re-enacted from the file: the hooks recognise the ritual by that call.
**Repro:** after a closing, `ls FAREWELL_MESSAGE_FROM_THE_PREVIOUS_CHAT.md` → exists, its text = the farewell.
**Trigger:** the owner names a closing, or a named time arrives → call the Skill tool with `end-chat-soft` first.
**Not for:** reading a skill to prepare (that is fine) — only the execution must go through the call.

### EXP-0002 · 2026-11-09 · ❌→✅ · #machine #install #kago
class: shared-machine-not-checked
none-cheap: a hook gating winget/pacman needs a settings change by the owner; the lock command stands in AGENT_GUIDE.md -> Build
**Context:** installing MSYS2 (`winget`) while the KAGO agent ran a `wbadmin` image of C: and planned an SSD-firmware
power cycle; the owner stopped it («а как ты это всё поставишь сейчас? если идет дамп C?»).
**Tried / did:** started the install without asking; killed it — a partial `C:\msys64` stayed. Then asked KAGO via
`SendMessage`; it answered with the backup's state and its machine lock.
**Result:** ❌→✅ — install parked until the lock is free; nothing broken (the image reads a VSS snapshot).
**Lesson:** this PC is shared by agents of several projects; anything that changes the machine (install, heavy run,
reboot-sensitive work) checks the machine lock first and asks its holder.   → link: AGENT_GUIDE.md → Build
**Repro:** `node D:/work/ai_sandbox/_tools/machine-lock.mjs status` (exit 3 = busy: wait or ask the holder);
`ListAgents` → `kago-*` / `kumm-*` sessions.
**Trigger:** about to run `winget`, `pacman`, `pip install` into a system location, a long build or a reboot → run
the status command first.
**Not for:** reading, git, editing sources inside the project folder.

### EXP-0001 · 2026-11-09 · ❌ · #counts #stamps #checkpoint
class: claim-before-evidence
none-cheap: free-text numbers in chat and commit messages are not machine-readable; the Repro commands are the carrier
**Context:** KAIF install and the CodeRabbit triage in one session.
**Tried / did:** four claims written from memory instead of from a command: "13 CodeRabbit comments" (gh said
5+4+1+1+3 = 14); "6 local fixes" in commit 338f0b7 (git log shows 5); a stamp "14:50" (the probe said 14:47);
`checkpoint maps` run in the same parallel batch as the map Writes that FAILED — recorded "done" on empty templates.
**Result:** ❌ — all four caught and corrected in place within the session (chat, STATUS, the research doc).
**Lesson:** a number, a count, a moment or a "done" is copied from the output of a command run in the same call —
never summed or felt; a checkpoint runs only after the result of the work it certifies is read.
**Repro:** counts — `node -e` / `wc -l` over the dump; fixes — `git -C firmware log --oneline <base>..<branch>`;
moment — `date '+%Y-%m-%d %H:%M %z'` in the same call as the write; checkpoint — never in the same tool batch as
the edit it certifies.
**Trigger:** writing any number or time into chat, a commit message, STATUS or a report.
**Not for:** numbers quoted verbatim from a source document (cite the source instead).
