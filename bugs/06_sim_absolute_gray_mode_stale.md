# Bug 06 — simulator: after the image viewer every book page shows dark (stale absolute gray mode)

**Status:** 🔧 fixed locally, pending the owner's word on an upstream PR · **Severity:** S2 (a run lost, ~10 min)
**Version/build:** simulator `MikalaiKryvusha/crosspoint-simulator` `windows` `087cb54` (PR #62 head) with firmware
`wip/krinik-debug9` · **When/context:** 2026-11-13, idea 02 simulator run C3 · **Fixing:** this session — `49ded1a`
on the local branch `fix/gray-absolute-reset`

## Symptom

Tap a picture in a book → the image viewer (absolute gray pass) → swipe Back: the book page, and every page after
it, shows as a near-negative (black field, light text). The file browser after the same viewer is light.

## Repro (deterministic)

`SD_TEMPLATE=sd_book_images SIM_ENV=simulator_x4_pro_win sh tools/sim_run.sh idea02_dark '3000:TAP:0.5,0.40;6000:SWIPE:0.05,0.5,0.6,0.5,300;10000:SWIPE:0.8,0.6,0.3,0.6,300;17000:QUIT' '9500:b3;12000:next'`
→ `b3.webp`, `next.webp` dark (on `087cb54`); light on `49ded1a`.

## Root cause

`simulator/src/HalDisplay.cpp`: `displayGrayscaleBase(GrayscaleMode::Absolute, …)` sets
`grayscalePreviewState.absolute = true`; nothing reset it on a plain `refreshDisplay()`. The reader in the simulator
takes the OVERLAY path (its log never shows «UC8279 image page»), starting its gray pass with a plain
`displayBuffer()`; `composeGrayscalePreview()` then read the overlay planes as absolute, where empty = black.
The device was not involved: on the X4 Pro the reader itself selects the absolute mode for every picture page.

## Fix

`refreshDisplay()` resets `absolute`; `displayGrayscaleBase(mode, …)` sets it AFTER its own base refresh (and resets
it on the combined-overlay branch). Verified: runs `idea02_c2c3_fix`, `idea02_c4_k1_k2`, `idea02_c5` light.
Guard: the simulator repo has no tests; the case C3 of `testcases/TC_idea02_image_fullscreen_tap.md` reddens on the
old library (proven: runs `idea02_dark`, `idea02_dark_fix`).
`TWINS: searched "grayscalePreviewState.absolute" in simulator/src — 3 sites (declaration, the two base functions); all handled.`

## Decisions made without the owner

- `[AI]` The fix lives on a separate local branch, not on `windows`: PR #62 (head `087cb54`) waits for a maintainer
  and stays untouched. Sending it upstream is a PR text for the owner's proofreading — not done.
- `[AI]` The firmware also starts the first page after the viewer from a clean base (`pagesUntilFullRefresh = 1`) —
  for the real panel's ghosting, not for this bug (that hypothesis was refuted by run `idea02_dark_fix`).

## Links

`ideas/02_image_fullscreen_on_tap.md` · `testcases/reports/2026-11-13_idea02_simulator.md` · `bugs/05` (the other open
simulator bug)
