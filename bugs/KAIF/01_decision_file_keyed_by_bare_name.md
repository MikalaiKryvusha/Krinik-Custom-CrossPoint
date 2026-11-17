# KAIF bug: the review contour names a decision file by the document's BARE file name — two documents with one name in two folders share it, and the second verdict overwrites the first

kaif-fp: .kaif/tools/contour/core.mjs#decisionPaths :: decision-overwritten-by-name-collision :: v2.9
**Delivered upstream:** https://github.com/MikalaiKryvusha/KAIF/issues/199
**Autocapture** (from `.kaif/kaif.json` + update receipt): KAIF 2.9 (+ 2.10 WIP, `d2f21274`) · project anonymized ·
sphere programming · language ru · tracking origin · agent system claude-code · OS Windows 11 Pro 10.0.26200 · Node 24.15.0
**Dedup attestation:** searched `bugs/KAIF/` (directory did not exist → no tickets) and origin issues, all states
(`gh issue list --repo MikalaiKryvusha/KAIF --state all --search "decisionPaths basename"` → none; `"decision.json overwrite"`
→ #121 only, a 2.7 → 2.8 update field report whose body mentions neither a name collision nor `decisionPaths`;
`"mockup same name"` → none; `"docBase collision"` → none). No match found.

## Expected per canon

> `// ── C6/I2: the decision is written to THREE places with derived names` — `.kaif/tools/contour/core.mjs:812`

and the contract that a recorded owner's answer is never lost: «the owner's answer is UNTOUCHABLE: new text only as a dated
follow-up (I2)» — `core.mjs` → `recordDecision`. The mock-up face promises a record per image: «decision.json named after
the image» (`review.mjs` selftest).

## Got in the field

The project has two mock-up pictures, each `compare.webp`, in two folders: `qa_runs/caption005_compare/compare.webp`
(answered by the owner 2026-11-17 10:40 → `interviews/decisions/compare.decision.json`, `"document":
"qa_runs/caption005_compare/compare.webp"`) and a new `qa_runs/caption_look_compare/compare.webp` about to be shown. The
name is derived without the folder:

```js
const docBase = (docPath) => basename(docPath).replace(/\.[^.]+$/u, '');   // core.mjs:813
decision: resolve(root, cfg.decisionsDir, base + '.decision.json'),          // core.mjs:817
```

A probe with two documents `a/compare.webp` and `b/compare.webp` on the unpatched `core.mjs`:

```
refused second: false · b reads: B answer · a reads: B answer -> GUARD RED
```

— the second verdict replaced place 2 of the first; `readDecision` of `a/compare.webp` returns B's answer. Caught before
the show: the new picture was renamed `caption_look.webp`.

## Repro (deterministic)

1. In a scratch root with `interviews/decisions/`: create `a/compare.webp` and `b/compare.webp`.
2. `recordDecision(root, 'a/compare.webp', { kind: 'mockup', comment: 'A answer' })`.
3. `recordDecision(root, 'b/compare.webp', { kind: 'mockup', comment: 'B answer' })`.
4. `readDecision(root, 'a/compare.webp').comment` → `'B answer'` (expected `'A answer'`); the queue's `--list` and the
   page's "already answered" state of either document read the other one's record the same way (`review.mjs:744`, `:1539`).

## Cost and violated invariant

Near-miss: the owner's recorded answer to interview #005 (a taste decision on a mock-up page) would have been replaced in
place 2 by the next mock-up's verdict; the archive (place 3) keeps a copy, but every reader of place 2 — the queue, the
debt list, the page — would have shown the wrong answer. Violates **owner-decisions** (a recorded answer is untouchable)
and **honest-green** (the page of the second document would open as "answered" by the first one's verdict).

## What in KAIF led to this

`docBase` drops the directory: the decision namespace is flat (`interviews/decisions/`) while documents live in many
folders. Names collide naturally for mock-ups (`compare.webp`, `preview.png`, `mock.png`) — generated pictures get generic
names. `recordDecision` writes place 2 without checking whose record already stands there, and `readDecision` returns it
without checking its `document` field, though every record carries that field.

## Local remediation (per the "defect in KAIF itself" contour, if applied)

`core.mjs` (KCCP, 2026-11-17): `recordDecision` throws when the existing place-2 record's `document` differs («decision
file … belongs to …, rename one»); `readDecision` returns `null` for a record of another document. Mutation-proved: the
probe above is GREEN on the patched file (`refused second: true · b reads: null · a reads: A answer`) and RED on the
original (`git show HEAD:.kaif/tools/contour/core.mjs`). Contour selftest after the patch: 186 checks green. A fuller fix
(a decision name that carries the folder, with a migration of existing records) is the origin's choice; this local guard
refuses the collision loudly and is reconcilable with any such fix at the next `/kaif-update`.
