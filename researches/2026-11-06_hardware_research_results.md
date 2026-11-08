# X4 Pro hardware research: PWM, battery indicator, charge cap, frontlight current — results

[AI]
Date: 2026-11-06. Follows `2026-11-05_hardware_research_backlog.md`. Source tree: krinik firmware
`~/Xteink/firmware` (SDK 50196ef). Nothing below is measured on the device yet; every statement is
marked **code**, **doc** (vendor/SDK documentation), or **inference**.

## 1. PWM: more than 1024 steps?

Facts:
- **code** X4 Pro profile `FrontlightConfig{8, 25000, 10, true, 9}`: cool GPIO8, warm GPIO9, 25 kHz, 10 bit,
  active-high (`freeink-sdk/libs/hardware/BoardConfig/include/BoardConfig.h:1946`). Stock 7.0.8 uses the
  same 25 kHz / 10 bit (`freeink-sdk/docs/xteink-x4pro-support.md`, «Frontlight»).
- **code** The krinik build does not define `FREEINK_FRONTLIGHT_LS`, so the Arduino 3 path
  `ledcAttach(gpio, 25000, 10)` is used (`FrontlightManager.cpp:133-135`); the IDF auto-selects the clock.
- **code** Brightness → duty: gamma 1.6554 table so that 1 % = exactly 1 LSB on 10 bit
  (`FrontlightManager.cpp:33-51`). Warm/cool split the same total duty (`:510-514`).
- **doc** ESP32-S3 LEDC clocks: APB 80 MHz, XTAL 40 MHz, RC_FAST ~17.5-20 MHz. Max resolution =
  floor(log2(clock / frequency)); S3 counter is 14 bit
  ([ESP-IDF LEDC, ESP32-S3](https://docs.espressif.com/projects/esp-idf/en/v5.3/esp32s3/api-reference/peripherals/ledc.html)).

Answer:
| Steps | Frequency | Feasible | Cost |
|---|---|---|---|
| 1024 (now) | 25 kHz | yes | — |
| 2048 | 25 kHz (80 MHz / 25 kHz = 3200 ≥ 2048) | yes | change `10` → `11` in the profile; the gamma table scales by `full` |
| 4096 | ≤ 19.5 kHz | yes | near the audible range: a boost inductor may whine; needs listening on the device |
| 8192 / 16384 | ≤ 9.8 / 4.9 kHz | technically | audible, visible on camera — not recommended |

**inference** One LSB at 25 kHz / 10 bit is a 39 ns pulse (19.5 ns at 11 bit). An LED driver (boost or
switch) very likely does not respond to pulses that short, so the dark end is probably the driver's turn-on
threshold, not quantization. More steps would then add levels only above the threshold. This is the
question to measure first: the smallest raw duty that lights the LEDs, with the curve rebuilt from that
floor (the SDK already has `minStartPermille` / `minHoldPermille` for exactly this, `BoardConfig.h:686-697`).

## 2. Battery indicator: what voltages are 0 % and 100 %?

Facts:
- **code** The percentage is the CW2017 gauge's SoC register 0x04, read as is; no firmware mapping from volts
  (`BatteryMonitor.cpp:231-260, 469+`). The gauge runs the OEM 80-byte BATINFO battery model
  (`BatteryMonitor.cpp:248-256`).
- **code** The gauge also gives VCELL (regs 0x02/0x03, `mV = (raw·5+8)>>4`) — `BatteryMonitor::readMillivolts()`
  exists, but the firmware does not show it anywhere.
- **doc** CW2017 estimates SoC from open-circuit voltage plus its model (FastCali); profiles exist for
  4.20 / 4.35 / 4.40 V full-charge cells ([CW2017 datasheet](https://uploadcdn.oneyac.com/upload/document/1737612108523_8373.pdf)).
- **doc** Battery 1100 mAh ([X4 Pro FAQ](https://www.xteink.com/blogs/product/x4-pro-faq-specs-support)).

Answer: 0 % and 100 % are not fixed voltages. They are model states of the gauge: 100 % is the full-charge
point of the profile, 0 % its empty point, and both move with load and temperature. The BATINFO format is not
public, so the profile cannot be decoded from documentation. **The only reliable answer is a log** of
VCELL + SoC + charging over a full discharge and a charge.

## 3. Charge cap at 80 %

Facts:
- **code / doc** No charger on I²C: the only charger signal is STAT on GPIO21, input, read as «charging»
  (`BoardConfig.h`, X4 Pro profile; `xteink-x4pro-support.md` «RTC / USB / battery»). The CW2017 has no
  current register and cannot control charging.
- **doc** Stock firmware only reads this pin; no charge-enable output was found in the recovered board init.
- **doc** No public teardown names the charger IC; charging is through a magnetic pogo dongle.

Correction 2026-11-06, evening: the current SDK/OEM mapping identifies no charger-control route. The
actual charger part, CE/EN routing and any alternative digital interface are unknown. Firmware feasibility
is UNCONFIRMED; absence of a mapped GPIO does not establish physical impossibility. Identification of the
charger and tracing its control path are required. A changed percentage display does not stop charging.
See `2026-11-06_power_controls_followup.md`.

## 4. Frontlight current at 100 %, and an 80 % cap

Facts:
- **code** Two PWM pins drive the LEDs; the driver part and current-set resistor are unknown. Follow-up: public X4 Pro teardown photographs were found, but their small IC markings are not readable confidently; see `2026-11-06_stock_batinfo_charger_analysis.md`.

Correction 2026-11-06, evening: the hourly log measures gauge-percentage changes, not LED current.
Multiplying by nominal1100mAh gives only a model-dependent estimate of battery draw, not LED peak or DC
current. The100%/50% debug2 stage also includes4000Hz software dithering. Driver and LED ratings are
unknown, so the need for wear protection is UNCONFIRMED. UI80% is nonlinear and does not imply80% current
or80% light. A duty ceiling is possible; the actual change in peak/average LED current requires driver
identification and physical measurement. See `2026-11-06_power_controls_followup.md`.

## Proposed next step (needs Nikolai's flashing)

One krinik diagnostic build:
1. A battery log: every minute append `time, VCELL mV, SoC %, charging, brightness, warmth` to
   `/.crosspoint/battery_log.csv`. Answers items 2 and 4 (and 3's «where charging ends»).
2. A raw-duty test row in the light panel or a hidden screen: step the duty 1, 2, 3 … and mark where light
   appears. Answers item 1's real question.
Then, if wanted: 11-bit PWM (2048 steps) with the floor from step 2.
[/AI]

[AI]
## Update 2026-11-06 10:35 +03 — board search, debug build

- **doc** FCC ID 2BTR9-X4PRO (Shenzhen Xiaohu Xingtong, application 2026-06-16). Internal photos are filed
  under short-term confidentiality and become public on **2026-12-12** ([fccid.io](https://fccid.io/2BTR9-X4PRO));
  schematics/BOM are long-term confidential (the X4 filing marks them so). FCC mirrors answer 403 from this Mac (VPN).
- **doc** Original X4 teardown: charger marked «4056» — TP4056-class standalone linear charger, fixed 4.2 V
  termination, CHRG/STDBY outputs, CE input ([min.news teardown](https://min.news/en/digital/3d78670f66f36741698fd086320d6488.html),
  page itself 403 here; from the search summary). Fits the X4 Pro's single STAT pin; the X4 Pro part is unconfirmed
  until the photos. If it is a 4056 with CE tied high, an 80 % cap is impossible in firmware.
- Nikolai 06.11: brightness scale logarithmic, 1 % = the shortest PWM pulse, 100 % = no PWM (constant current).
  Done in `1.1.1-debug` (firmware nikolai-debug 96f890d8, SDK krinik-debug 25615e0): 11 bit at 25 kHz,
  duty(pct) = 2047^((pct-1)/99) with one-LSB minimum steps (1-58 % linear 1..58 LSB, 75 % = 299, 90 % = 948,
  100 % = full → Arduino LEDC writes 2^n = constant on), battery log `/.crosspoint/battery_log.csv`.
  Constant on holds only when one channel carries all the light (warmth 0 or 100).
- Next: the log over a full discharge and charge gives 0 %/100 % voltages and the light's current
  (SoC drop per hour light 100 % vs off × 1100 mAh).
[/AI]
