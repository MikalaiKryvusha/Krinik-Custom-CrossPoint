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
>      field-dropped-in-rebuild, shared-machine-not-checked, ritual-run-by-hand -->
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
