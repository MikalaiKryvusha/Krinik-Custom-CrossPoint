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
>      wrote-outside-project, suite-not-run -->
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

### EXP-0011 · 2026-11-13 · ❌→✅ · #epub #lint #tools
class: missing-dependency
none-cheap: one-line S3 note; the lint itself should say «xmllint not found» — fix it when the tool is next touched
**Context:** `node tools/epub_lint.mjs` on the generated test book `qa_runs/sd_book_images/image_test.epub`.
**Result:** «✗ … XHTML: ch1.xhtml undefined» — not a book defect: no `xmllint` on this PC (neither PATH nor `D:\msys64`).
**Repro:** well-formedness without xmllint: `.pio-venv/Scripts/python.exe -I -c "import zipfile,sys,xml.dom.minidom as m;z=zipfile.ZipFile(sys.argv[1]);[m.parseString(z.read(n)) for n in z.namelist() if n.endswith(('.xhtml','.opf','.xml'))];print('ok')" <book.epub>`
**Trigger:** an `undefined` in the XHTML lines of `epub_lint.mjs`.
**Not for:** the link/manifest checks of the same lint, which do not need xmllint.

<!-- class-ok: twins-missed — two unlike faces (EXP-0005 a regex rename matching extra C++ sites; EXP-0016 two consumers of one input gesture under different names); each face carries its own grep Repro, and a guard for the whole class would be a general code-search policy, not cheaply possible; the judge pass before every build is what caught EXP-0016 -->
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
