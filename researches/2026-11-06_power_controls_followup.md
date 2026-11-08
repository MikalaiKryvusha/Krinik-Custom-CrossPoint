# X4 Pro: charge control, LED limits and CPU cost — follow-up

[AI]
Owner priority: establish whether ESP32 can disable the battery charger and whether reducing maximum LED current is useful. The 20-minute log proposal is secondary and remains unimplemented.

## Confirmed from local source, not measured electrically
- debug2 image identity: qa_runs/frontlight-colour-fix-2026-11-06/image.json; firmware env x4pro-krinik-debug uses11bits,39062Hz, logarithmic scale, per-channel dither. APB80MHz gives a nominal12.5ns tick and2048-tick/25.6us PWM period, about39.0625kHz. Single-channel brightness1% maps to duty1/2048. This describes the GPIO command, not the actual LED-current waveform.
- FrontlightManager.cpp applies FrontlightPwmDither after mixing. At50% warmth and total duty2047, each target is1023.5. HalFrontlight.cpp:14,219–239 schedules a250us ESP_TIMER_TASK callback while fractional channels remain. Thus the100%/50% stage also requests4000software callbacks/s. Each callback takes a mutex, setsTotalDuty and updates channels. Perceptual pow() builds its lookup table once per resolution, not on every dither callback. Which fraction of power comes from arithmetic, task scheduling, peripheral updates or prevented idle needs profiling/measurement; source alone does not quantify it.
- With light off, channels become integral zero and updateDitherTimerLocked stops the periodic timer (after any fade). The light-off hour is therefore not evidence of continuous frontlight-dither CPU cost. It still includes normal awake-board operation and minute battery logging.
- The second measured hour includes LED/driver consumption AND any additional CPU work from the dither. The difference between hours is not a pure LED-current measurement.

## Battery charger control
X4 Pro BoardConfig profile has charger STAT GPIO21 as an INPUT, CW2017 gauge@0x63, chargerAddr=0 and power{1}, leaving chargeEnable unassigned. This is no identified software control path, NOT proof that the physical charger has no controllable input. Identify the exact charger IC and trace CE/EN or another control input to the SoC; alternatively identify a documented digital charger interface in the actual board/OEM firmware. If CE/EN is hard-wired and there is no routed control interface, changing firmware alone cannot interrupt charge by that route. A register write to the fuel gauge or a changed percentage display is not charge control. Any implementation needs the real active polarity, state across deep sleep/reset, and lower restart threshold; no invented GPIO numbers. Battery maximum permitted charge voltage and voltage accuracy remain unknown.

## LED current limit
Identify LED driver, LED strings, current-setting components and LED ratings before claiming wear protection is needed. The two-hour percentage log does not establish LED peak current or junction temperature. A ceiling on commanded PWM duty is implementable in software; its electrical effect depends on the driver. True PWM usually preserves pulse current while reducing its on-time; PWM-to-analog drivers instead convert the command into a DC-current target. Neither mechanism has been established for X4 Pro.
The actual log brightness curve is nonlinear: UI80%=439/2048≈21.44% of one-channel PWM period, while UI100% is special-cased constant-on. UI80% is therefore not a known20% reduction in light or current. A requested80% electrical ceiling must specify its physical target and be calibrated, not reuse the UI percentage blindly. No limiter implemented.

## Primary sources checked
- Espressif LEDC, ESP32-S3, source clocks and duty: https://docs.espressif.com/projects/esp-idf/en/v5.3/esp32s3/api-reference/peripherals/ledc.html (80MHz APB, resolution/frequency relationship).
- TI SNVA768, section1 and2: https://www.ti.com/lit/an/snva768/snva768.pdf (true PWM vs PWM-to-analog; not identification of our driver).
- TI bq2510x datasheet: https://www.ti.com/lit/ds/symlink/bq25100.pdf (an example of charger CE; NOT identification of X4 Pro charger).
- FCC filing index https://fccid.io/2BTR9-X4PRO still lists internal photos as metadata-only until2026-12-12; it does not expose the part numbers today. The older X4 charger marking must not be assigned to X4 Pro.

## Next evidence
1. Identify battery charge rating and verify voltage independently; identify charger and LED-driver markings/wiring from board documentation or actual hardware. Do not run blind GPIO writes or request another full charge as a substitute.
2. Determine whether an actual SoC→charger control route exists; then design charge-stop/restart policy.
3. Measure driver/LED current at high light output, compare against component ratings and temperature. Separately isolate the4000Hz software-dither cost at nearly equal channel duties; isolate minute logging in its own control.
Status: source investigation complete to the present evidence boundary; physical part identities, routing and currents unverified. No firmware changes, builds, flash or publication.
[/AI]

[AI]
## Charger status follow-up after debug3
Repeated primary-source search on2026-11-06: no new identified X4 Pro charger part or routed charge-enable signal found in the checked material. SolarOS board documentation also lists charger STAT GPIO21 as reserved and does not advertise USB/VBUS detection (https://github.com/nilseuropa/solar_os/blob/main/doc/manual/boards.md). This is corroboration of the documented mapping, not an independent electrical verification or evidence of hardware absence. Existing SDK profile still has chargerAddr0 and no assigned chargeEnable. Current answer: programmable stop is unconfirmed; obtain actual charger marking/CE or digital-interface routing and battery charge rating before implementing an80% cutoff. No device probing or firmware changes for charger control performed.
[/AI]

[AI]
## Latest owner hypothesis and actual stock input — 06.11.2026 20:54 +03:00
Owner: «можно просто другой профиль передавать. Чтобы тот контроллер напряжение4.1В считал100% заряда». Investigate this exact hypothesis; do not dismiss it based only on missing SDK chargeEnable, and do not promise that a display remap controls current. Prove or refute the chain BATINFO→CW2017SoC/outputs→charger stop. The current code verifies/loads80-byte OEM BATINFO at0x10..0x5f; UI reads SoC0x04. The current CrossPoint code has no SoC-full→charger-disable action. Whether the board has an electrical CW2017→charger connection remains unknown. The threshold100%@4.1V has not been encoded or tested; BATINFO format is not yet decoded.
Owner also reports rear LED changes color when fully charged. Identify its driver/path (charger status outputs or ESP32) and correlate its transition with GPIO21 and actual input/charge current. Color alone is not evidence of a controllable CE.
Concrete progress: downloaded actual OEM X4Pro EN stock image from CrossPoint Tools public/firmware/x4pro-stock-en.bin, app descriptor7.0.8/xteink_app,6 792 544bytes. SHA256369cfee91881f7bac2fac14269baad44362c8f1280d4d089b52e02186e6141be; git blob SHA172494155fec2123058386f8ab48a784f6ac898af verified against API treeddb8bd268e9cef6723873458308e273a4eff3e7a. Saved qa_runs/charger-source-2026-11-06/x4pro-stock-en.bin + stock-image.json + crosspoint-tools-tree.json. This is stock Xteink, distinct from the official CrossPoint2.0.0 image on the SD card. Offline acquisition ONLY; not flashed, no decompilation yet. Published Ghidra notes for Cw2017PowerHal are in freeink-sdk/docs/xteink-x4pro-support.md; the exact downloaded7.0.8 binary must be analyzed rather than assuming old note offsets apply.
Transport notes: Python urllib failed local CA validation; curl with normal certificate validation worked. GitHub default branch is master; guessed main gave404 and is not an access failure.
Critical device constraint discovered in personal README: this unit is eFuse-locked; firmware installation is via SD only. Do not attempt USB bootloader/JTAG recovery or flash stock. Current volume/serial device absent at the latest probe. Existing application serial handler only implements CMD:SCREENSHOT; no GPIO/I2C diagnostic command exists. Hardware charge experiment has NOT been run; no pins or gauge configuration changed.
[/AI]
