# Frontlight colour fix — debug2

[AI]
Requirement: Nikolai accepted the proposed separate-channel calculation with «давай сделаем».
Base: firmware nikolai-debug 2ccdbe38, SDK krinik-debug f75cf959; both clean before work.
Recon: researches/2026-11-06_frontlight_colour_flicker.md and its executable reproduction.
Lesson: identical debug version labels hid which build was installed; give this candidate a unique debug2 label and filename.
INTENT: preserve the requested mean warm/cool duty ratio during fades and at steady low brightness; keep ordinary krinik and other boards' behaviour.
AUTH: edit and produce a local test image. No release, flash, upstream PR or new outward message requested. Existing one-judge instruction applies.
FORK: hardware fractional registers versus per-channel error diffusion on the existing timer. Chosen: documented integer LEDC writes, existing timer; avoid undocumented fractional-register behaviour. Price: steady fractional mixtures keep a 4kHz timer running, physical power/flicker needs measurement. Sources: installed Arduino/IDF LEDC helpers; official ESP-IDF LEDC API (integer duty); prior working timer implementation.
Design: SDK owns two bounded fractional accumulators and exposes whether further samples are needed. Its raw-duty setter retains a fractional total. HAL owns its existing timer and continues sampling only for active fades or fractional channel targets. Neutral mix produces equal channels on every sample. Off/deep sleep cancels the timer; queued callbacks must not relight parked pins. No new task, no per-tick allocation, no changed PWM frequency/resolution/brightness endpoints.

Acceptance/checklist:
- [x] Add the per-channel quantizer and exercise actual production logic across brightness/warmth, fractional fades, endpoints and channel symmetry.
- [x] Integrate SDK float duty and HAL timer lifecycle; test real HAL+SDK with host timer/register adapters (brightness, warmth, reversal, off, sleep, resume).
- [x] Unique version/filename cp-2.0.0-krinik-1.1.1-debug2.bin; prior image kept.
- [x] Format, run targeted and surrounding checks, one independent reviewer, resolve findings.
- [x] Final debug2 firmware build, image SHA, test instructions and reader STATUS/HANDOVER.

Limits: no optical/power/device measurements yet. At extreme low fractional targets rare single-channel pulses may remain perceptible; the 4kHz timer alone is not a guarantee of a flicker-free optical result. Confirm 5/6/7% at warmth 50%, then 0/30/70/100; toggle/fade/sleep/reverse. Observe colour, steps, flashes, sound and battery separately.
Observed checks: 936/936 host (host.log). Real HAL+SDK across 100 brightness percentages x 101 warmth percentages, plus neutral fade/reversal, off/sleep/queued callback, raw-level zero/restore and timer-start failure; compile both non-dither X4 Pro and no-frontlight C3. SDK Picco and independent quantizer sweeps passed. Baseline SDK Picco host test had an existing missing LOG_DBG stub; fixed the stub rather than suppressing that error. C3 host compilation excludes Clang's existing unused-private-field diagnostic for SDK fields absent with CAP_FRONTLIGHT=0; ordinary warning checks remain enabled.
Review round 1: one P2 (early division rounded mathematically integral targets, 535 total/warmth combinations kept timer active). Fixed multiplication-before-division; added all-integral-target pending checks and actual HAL timer-state checks, repeated targeted suites PASS. Round 2 VERIFIED WITH CAVEATS, no remaining findings. Final debug2 build started.
TWINS: searched warmDuty/coolDuty split, ditherAcc, setTotalDuty across firmware HAL/src and SDK frontlight. One other total-rounding split remains deliberately in the non-dither fallback for stable/other boards; covered by a compiled fallback test.
TWINS-MECH: rounding the combined signal before channel sampling discards per-channel fractions. Searched combined-dither accumulators and both warm/cool split formulas; the debug path now splits first, old HAL accumulator removed.
AFTER-WORK: timerRunning changes only after start success or stop; queued callbacks check it before any PWM write. An interrupted build cannot replace the previous test image; debug2 has its own path.
BOTH-WAYS: debug behaviour is guarded by FREEINK_FRONTLIGHT_DITHER && FREEINK_DEVICE_X4PRO; non-dither X4 Pro and C3 are compiled in the host harness. The old debug filename and stable release files are preserved.
Final result 06.11.2026 14:33 +03:00: debug2 firmware SUCCESS, 211.76s, flash 5415050/6553600, static RAM 112380/327680.
Copied the ESP app image to a new debug2 filename, verified embedded version and SHA256 0076ec028760615fcbdda93537576655b1a0aceafa00c0603b8befe68f6e277d; prior image hash unchanged.
Source hashes still match the final reviewed candidate. image.json and test-instructions.md stored with logs. Local changes intentionally remain uncommitted; no push, release or hardware flash performed.
Owner follow-up «на проводе»: USB volume X4-KRINIK verified by UUID 649C18D8-130F-3C63-AD1A-F6396E1014A6. Added only /.firmware/cp-2.0.0-krinik-1.1.1-debug2.bin, verified expected SHA; all 153 previous owner files unchanged. Reading state/index/calibration and current battery log backed up. AppleDouble cleaned per local card procedure, diskutil eject succeeded. No actual firmware flash performed. Owner reports 68%, discharging to ~50% before charge test. Evidence: card-result.json and card-before-hashes.json.
[/AI]

[AI]
Owner visual acceptance: «стало плавно, красиво». Also confirmed flashlight in the personal build works well. Battery/physical power measurement remains pending; stable1.1.2 is now prepared separately. Current-device debug2 and its data were not changed after the card copy.
[/AI]
