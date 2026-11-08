# Frontlight — low-brightness colour changes and fade flicker

[AI]
Owner observation: «вроде бы стало плавнее, не уверен, но словно на разных процентах, 5, 6, 7 - по разному ведут себя холодный и теплый светодиоды. и анимация мерцает цветами. Проверь по коду - может такое быть? или я все же на старой прошивке».
Scope: read-only code investigation and numerical reproduction, no firmware fix/flash/publication.
Candidate: firmware nikolai-debug 2ccdbe38, SDK krinik-debug f75cf959, current image SHA256 66b9958cfa6fed1b3bf921ec013e76aa085ba0eef988fa56946078e7fa66d1a0.
Own prior work: STATUS.md records the original low-brightness step defect and the later duty-space dithering fade. Installed image remains unknown: debug revisions share one visible version string.
Sources: lib/hal/HalFrontlight.cpp; freeink-sdk/libs/hardware/FrontlightManager/src/FrontlightManager.cpp; platformio.ini.

Checklist:
- [x] Read current source and relevant history.
- [x] Calculate steady-state and fade channel duties from current production formulas.
- [x] Compare previous debug fade mechanism.
- [x] Record findings and distinguish code evidence from unmeasured hardware behaviour.
Findings [TESTED: 2026-11-06 · compile/run extracted production formulas on host]:
- Log brightness curve produces total duties 5, 6, 7 for UI brightness 5%, 6%, 7% (11-bit full=2047).
- SDK lines 546–547 round warm=(total*warmth+50)/100, cold=total-warm. At warmth=50, these are cold/warm 2/3, 3/3, 3/4. At total=1 the cold output is 0 and warm is 1.
- HAL lines 237–248 dither the combined total, then SDK rounds the channel split anew. This does not dither each channel's ideal fractional duty. Thus smooth mean total does not preserve the intended channel ratio.
- Reproduction compiles the current perceptualDuty, channel split and fractional fade block extracted from source, with source SHA-256 recorded. 1000ms 0->5% fade at 50% warmth: for requested total in (0,1), cold is always off (595 lit warm-only ticks); for total in [1,2), averaged warm fraction is ~68%, versus requested 50%. These are electrical duty calculations, not measured optical brightness/chromaticity or hardware timing.
- Previous debug SDK 121765c and latest f75cf959 have identical channel-splitting code. Previous firmware 54f95f52 uses 20ms integer-level steps; latest uses 250us duty dithering. Both may shift colour. Symptoms cannot establish which image is installed.
- The claim that a 4kHz tick alone guarantees imperceptible dithering is too broad: rare accumulator carry pulses can repeat slower than the tick. No measured flicker frequency or sole optical root cause is claimed.
- Cold/warm LED efficiencies, minimum driver pulse lengths and update skew are not measured here. Rounding alone already demonstrates a code mechanism consistent with the report.

Evidence: qa_runs/frontlight-colour-2026-11-06/{probe.py,probe.cpp,result.txt,source-digests.txt}.
No firmware/SDK source edits, flash, build, commit or publication in this investigation.
Installed image remains unknown; exact same debug version string cannot distinguish the builds.
[/AI]
