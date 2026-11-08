# Independent review — reader_judge

[AI]
Owner standing instruction: one judge for firmware/PR/KEINKT, reused; overrides four-reviewer skill default.
Reviewer was read-only and did not run tests/builds or write files.
Base firmware 2ccdbe38, SDK f75cf959; complete candidate patches preserved here.
Round 1: one P2 in FrontlightPwmDither's division-before-multiplication. Host probe confirmed 535 mathematically integral mixtures unnecessarily requiring timer updates. Fixed the evaluation order and added exhaustive integer-target checks plus real HAL timer-state assertions.
Round 2: VERIFIED WITH CAVEATS, no new findings. Final patches: firmware-final.patch SHA256 1fab2e047a7018d9bf12f161c41c44e178ad480a4b312247319f60ce0083d015; sdk-final.patch SHA256 99d92b0d5ff17abe6bd42d4342553c28f146fdcfa83f99b91977d7575cc7d979.
Coverage: correctness, state ownership/architecture, embedded resource/lifecycle and docs/version in one review. SDK owns fractional errors; HAL owns existing timer/mutex. No new task or per-tick allocation. Other boards/non-dither stay outside the new quantizer; Picco LUT change only formatting.
Recorded checks: 936/936 host; SDK Picco and quantizer; real HAL/SDK debug X4Pro, non-dither X4Pro, C3-no-frontlight PASS.
Physical colour/flicker, shortest pulses, LEDC update skew, and battery consumption remain unmeasured. Final debug2 firmware build performed by main agent after fixes.
The owner approved the described per-channel mean-duty correction with «давай сделаем». The continuous timer for fractional steady targets and its power caveat were explained in chat; optical acceptance remains the device test.
[/AI]
