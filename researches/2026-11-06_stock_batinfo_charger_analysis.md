# X4 Pro stock 7.0.8: BATINFO, charge status and rear LED

[AI]
## Question and scope

Owner hypothesis: a different BATINFO makes CW2017 report 100% at 4.1 V, which might stop charging. Determine which links actually exist. Input: the already acquired OEM EN7.0.8 application, not CrossPoint and not an image installed on the device. This pass disassembles selected Xtensa functions offline; it is not full decompilation or electrical verification.

Evidence directory: `qa_runs/charger-source-2026-11-06/`.
Reproduction: `python3 qa_runs/charger-source-2026-11-06/analyze_stock.py`.
Observed result: PASS for image identity, matching profile, RTTI/vtable, 17 GPIO constructor records, GPIO21 read chain and SOC_ALERT=10 in the profile-upload path. Raw instructions: `disassembly/`; machine inventory: `offline-findings.json`.

## Observations from the actual binary

The SHA256 remains `369cfee91881f7bac2fac14269baad44362c8f1280d4d089b52e02186e6141be`. The image has eight segments. DROM file offset 0x20 maps to 0x3c2b0020; IROM file offset 0x3b0020 maps to 0x42000020. These mappings were parsed from the image headers. Old addresses below were accepted only after checking their bytes and references in this image.

| Finding | Address and observed path |
|---|---|
| CW2017 type identity | RTTI name at 0x3c5d8b78, type record 0x3c5d8b6c; vtable address point 0x3c5d8bac, static object 0x3fc9e198 |
| OEM BATINFO | Exactly one 80-byte match at DROM 0x3c5d8d00 / file offset 0x328d00, byte-for-byte equal to SDK `CW2017_BATINFO` |
| Gauge initialization | 0x4215071c checks the running version, profile-ready state, reads and compares 80 bytes, conditionally calls uploader 0x421504f4 |
| Upload registers | 0x421504f4 writes profile bytes to 0x10+i, then writes `0x80 | min(threshold,100)` to register 0x0b |
| Actual upload-call threshold | 0x421507cb–0x421507d4 passes table pointer, length 80, threshold **10**; this path therefore writes **0x8a** to SOC_ALERT |
| Percentage reading | 0x421505e8 reads register 0x04, accepts values <=100 and returns -1 on failure |
| Battery record | vtable slot 3, 0x4214f410, obtains voltage, another gauge measurement and percentage, assigns icon buckets and separately reads the charging GPIO |
| Charging GPIO | board init 0x4214eeb0 assigns pin 21, mode 0, args 0/0 to GPIO record 0x3fcb4b08 at 0x4214f11a–0x4214f128 |
| Charging read chain | 0x4214f48a loads 0x3fcb4b08; 0x4214f495 calls 0x4214f67c, which reads the record's pin through GPIO getter 0x421ec9e4 and returns a nonzero-level boolean |

Important qualification: **10 is the threshold passed when uploading the profile**, not a measurement of the live register. If the resident profile passes the existing checks, that upload can be skipped. The current SDK uploader uses 0x80 (threshold zero), a separate behavior from the OEM uploader. Neither write programs the charger's regulation voltage.

In `power-read.txt`, SoC controls returned percentage and icon buckets (>94, >74, >49, >24, >4). No branch in this function issues a charge-stop command at 100%. Both record bytes at offsets 8 and 9 are populated from the same GPIO21 reading; this is not an independently observed USB-presence input.

## The electrical output the gauge actually documents

Read the manufacturer's **CW2017-DS V1.1**, pp. 3, 7, 8, 10. Local original: `cw2017-v1.1.pdf`, extracted text: `cw2017-datasheet.txt`, source/hash: `cw2017-source.json`. Downloaded from the [Oneyac mirror of the Cellwise document](https://uploadcdn.oneyac.com/upload/document/1737612108523_8373.pdf). The manufacturer's currently indexed V1.3 URL failed retrieval; the downloaded document identifies itself as **V1.1**, and findings here are scoped to it.

The pinout documents INT_N as an MCU alarm output. INT_CONF (0x0a) enables SOC/temperature events; SOC_ALERT (0x0b) chooses the percentage threshold. Reaching that percentage in either direction can produce an event, so 100 is representable as a threshold. INT_N produces an approximately 1 ms low pulse; status flags require host handling. This is not a documented sustained charge-enable output.

Battery profiles characterize the cell for SOC estimation at different maximum charging voltages. The document directs users to Cellwise for profile details; it does not expose an 80-byte field layout for constructing a 4.1 V profile. The pinout and register map do not document an integrated charger or a charger-voltage control register. One generic I2C paragraph mentions “charging parameters”; it does not identify such a register and is insufficient evidence of charge control.

Consequently, an interrupt at 100% is possible in principle, but **not from the threshold-10 upload setting just recovered**. Using an interrupt to stop charging would additionally require an actual receiving/control circuit or an MCU handler and an identified charger-enable route. This pass has not established those board connections.

## Rear LED: what was and was not found

The inspected board-init function constructs 17 GPIO records: 3, 0, 7, 1, 11, 12, 13, 18, 14, 6, 5, 4, 10, 2, 8, 9, 21. These correspond to already documented buttons, rails, display, touch, frontlight and charger status. GPIO8/9 are the frontlight; GPIO21 is input. This function provides no identified extra rear-LED output or gauge-interrupt input.

That inventory is scoped to **this function**. It does not exclude a different initialization path, direct register operations elsewhere, an expander, or direct charger/LED wiring. The owner's color-change observation is preserved; no electrical connection is inferred from color alone. The rear LED's driver and the charger IC remain unidentified.

## Answer supported by this pass

The chain now established is:

```text
OEM BATINFO -> CW2017 SOC calculation -> percentage/icon in the application
charger status source -> GPIO21 INPUT -> charging boolean in the application
CW2017 SOC_ALERT -> documented INT_N pulse -> board destination UNKNOWN
rear LED <- source UNKNOWN
charger CE/EN <- source UNKNOWN
```

Changing the gauge profile is not established as a way to stop charging at 4.1 V. The binary evidence demonstrates profile loading and status reading; it does not demonstrate a 100% -> charge-stop action. No matching 4.1 V profile has been found or generated. This does not prove that the PCB has no usable charger control path.

The next decisive evidence is charger identification and routing: its enable/status outputs, the CW2017 INT_N destination, and the rear LED connections. Start with board documentation or readable component markings/board traces. A future software command needs an identified line and polarity first; only then can a controlled stop/restart experiment distinguish actual battery-charge current from USB consumption and status/LED changes. Do not blindly toggle GPIO1/2/5 or flash OEM firmware.

## Preservation and verification boundaries

Only research files, an offline analyzer and personal STATUS were changed. Firmware and SDK source, debug2/debug3 images and device configuration were not changed. No connection to the device, charging cycle, flash, commit, push or external publication was performed. Existing debug3 validation was not rerun because no firmware code changed.

[TESTED: 2026-11-06 · offline analyzer passes on the downloaded 7.0.8 image; instruction windows inspected against the call arguments and GPIO getter. Not tested electrically; rear LED and charge-stop behavior remain unverified.]

## Follow-up: broader reference scan and real board photographs

Owner continuation: «ну гоу». Applied `kaif-go` to the saved next step. Relevant CW2017/Xteink lessons were not found in the QA experience journal; the prior sections above are the existing project evidence. QA artifacts remain untouched.

### Additional binary evidence

Reproduction: `python3 qa_runs/charger-source-2026-11-06/trace_power_xrefs.py`.
Observed result: **PASS: 15 selected literal loads and 65 selected direct calls validated against objdump**, including 23 calls to the GPIO-write wrapper, seven calls to the gauge-register-write helper, and four direct literal loads of the GPIO21 record. Output: `followup/validated-xrefs.json` and `followup/trace-function-*.txt`.

This scans the entire extracted IROM byte range for specific CALL8 targets and L32R literal values, then confirms each candidate at its exact instruction address. ENTRY patterns provide candidate function windows, not recovered symbols. It does not resolve arbitrary indirect calls, inlined register writes, other helpers or IRAM. It is broader than inspecting the battery getter, but still not a whole-program proof of absence.

All seven found **direct** calls to the CW2017 write helper 0x4215040c have manually inspected register arguments:

| Call sites | Register and effect |
|---|---|
| 0x42150438 / 0x42150452 / 0x42150466 | 0x08: reset sequence 0xf0 -> 0x30 -> 0x00 |
| 0x42150522 | 0x10+i: the 80 BATINFO bytes |
| 0x4215053d | 0x0b: profile flag plus percentage alert threshold |
| 0x42150654 / 0x4215066f | 0x08: restart sequence 0x30 -> 0x00 |

No INT_CONF 0x0a write or threshold-100 setup was found through that helper's direct calls. This is not a live register dump and does not exclude writes through another path.

The four direct GPIO21-record loads belong to initialization/application (0x4214ee74, 0x4214f11a, 0x4214f12b) and battery status reading (0x4214f48a). Inspecting `applyPinConfig` at 0x4214f6e4 also confirms its initial-level write happens only for mode 1, whereas GPIO21 has mode 0. Thus the configuration application does not silently turn GPIO21 into an output.

The five selected literal calls to the underlying GPIO output function belong to the GPIO-write wrapper, initial-level application, the touch reset/address-selection routine 0x42150114, and two I2C pin-setup sites in 0x421516fc. The last two identify themselves with `i2c.common`, `s_hp_i2c_pins_config`, and `i2c sda pin set level failed` strings. They do not provide a newly identified charger control.

The 23 wrapper call sites additionally include parameterized high/low methods, display/SPI-style transfers, SD mounting using pins 41/42/40, touch reset and peripheral shutdown. Some generic receivers remain unresolved; they must not be advertised as a fully classified whole-program GPIO graph. No charge-stop route was identified in this pass.

### New physical evidence: another X4 Pro has a 4.35 V cell

Primary source: [DeathKringle's X4 Pro disassembly photographs](https://www.reddit.com/r/XTEINK/comments/1wdxcrx/x4_pro_internals_and_cracked_display_pics/). Downloaded three full-resolution originals; JPEG decoding verified. Files and hashes are in `followup/sources.json`.

The battery photograph (`followup/teardown-battery.jpg`) clearly reads:

- Model **TW 236257**; capacity **1100 mAh**; nominal voltage **3.8 V**; energy **4.18 Wh**.
- Charging limit **4.35 V**, printed as `Limited Voltage: 4.35V`.
- Chemistry **LiNiCoMnO2**; manufacturer **SHENZHEN TAIWOO BATTERY CO., LTD.**; date code **260722**.

The exposed board photograph shows **X4-2 PRO V07 4.28**. It provides a readable board layout, but the small power-IC markings cannot be read confidently in the supplied photograph. The six-image gallery was checked by its image descriptions: the other closeups concern display/touch FPCs, not a clear reverse side of the main PCB. Neither the charger IC nor a connection from gauge INT_N to charger CE/EN is established by these photos.

This is a real photographed X4 Pro battery, **not Nikolai's battery**. It demonstrates that a 4.20 V ceiling cannot be assumed for every X4 Pro. It does not establish this unit's charge limit, explain the measured 4.381 V exactly, or establish sensor/charger accuracy. Do not silently substitute the photographed battery's identity for the owner's cell.

The [manufacturer's X4 Pro manual, mirrored PDF](https://manuals.plus/m/90a2a68e9a663c4f8f2ba1a92f9abae6a0280d4b9ba06fa173f534f8fa0a420f_optim.pdf) labels the rear indicator red while charging and white when full. This corroborates the owner's observation; it does not specify the electrical driver. The web tool could read the PDF; local curl returned HTTP403, so no local PDF acquisition is claimed.

### Other source checks and remaining boundary

- [FCC filing index](https://fccid.io/2BTR9-X4PRO), rechecked: internal photos remain metadata-only, availability shown as 2026-12-12; schematics and block diagram remain metadata-only. No inaccessible exhibit was obtained.
- [TuyaOpen board config](https://github.com/tuya/TuyaOpen/blob/master/boards/ESP32/XTEINK_X4_PRO/board_config.h) explicitly attributes its hardware map to FreeInk/CrossPoint. It is not independent confirmation and exposes no newly identified charger-enable signal.
- [developing-today factory notes](https://github.com/developing-today/hardware-doc/blob/main/devices/xteink/x4-pro/factory-firmware.md) explicitly derive their firmware facts from FreeInk notes. They are not another decompilation of the stock image.
- [Launcher X4 Pro implementation](https://github.com/bmorcelli/Launcher/blob/main/boards/xteink-x4pro/interface.cpp) uses the same profile and known rails; no charging control was identified in the viewed implementation. No firmware was installed to investigate it.
- Direct Reddit JSON returned HTTP403. The large Tuya repository tree download timed out and produced truncated JSON; it was not used as evidence. Full original Reddit images and the small Tuya board header were successfully obtained instead.

**Current decision:** the proposed BATINFO-only charge cutoff is still unsupported. The next discriminating input is readable charger identification plus board routing, including the reverse side if needed. A component part number cannot be safely reconstructed from these blurry markings or from the older X4's components. No hardware actions, firmware edits, build, flash or publication occurred.

[TESTED: 2026-11-06 · exact candidate PCs decoded by objdump; two offline analyzers pass; all three original JPEGs decode; battery label visually read. PCB continuity, this unit's battery identity, rear LED driver and current interruption are NOT verified.]

## Continued investigation: MIC photos acquired and PowerService inspected

Owner explicitly objected to stopping at an intermediate checkpoint: «ты опять остановился....», then requested continued work despite the context-budget hook. This is a continuation of the same investigation, not a request to flash, probe pins or publish anything.

### Public internal photos were available in another certification

The earlier FCC finding remains correct for that filing, but it was **not a sufficient reason to stop looking for internal photographs**. The Japanese MIC certificate **220-J11880**, dated 2026-06-26, has a separate public photo attachment.

Discovery and source: [MIC certificate indexed by FCCID](https://fccid.io/giteki/220-J11880), [photo attachment 220-J11880_01_002.pdf](https://fccid.io/giteki/220-J11880/220-J11880_01_002). Downloaded the actual PDF from [this mirror](https://fccid.io/m/8bfb9aff70426996d7132aa9000ecf7118a5bbf502d54a23196ff5f17a38fdd2.pdf).

Local file: `certification/japan-internal.pdf`, 1,051,835 bytes, SHA256 **8bfb9aff70426996d7132aa9000ecf7118a5bbf502d54a23196ff5f17a38fdd2**. Three pages rendered and visually inspected, with original watermarks retained:

- Page 1: open reader and battery stamped **TW236257 3.8V / 1100mAh / 4.18Wh**, date code appears **2604**.
- Page 2: **both sides of the main PCB**, Photos 3 and 4. This corrects the previous acquisition boundary: a reverse-side photograph is now available locally.
- Page 3: closer component view, Photo 5, PCB clearly marked **X4-2 PRO V05**. The previously acquired Reddit unit has a **V07** PCB. Do not merge their wiring claims without comparison.

The closer view visibly identifies ESP32-S3, external flash and a BM8563-marked RTC beside its crystal. The charger marking is still **not identified confidently**. Numerical resemblances on other tiny ICs are not a part-number identification; no TP/SGM/ME charger model is asserted. The maximum source photograph size is about 1135×851 pixels, so a larger PDF render does not add missing character detail. Analytical crops/rotations live beside the full pages; they are not AI enhancement or new evidence.

This attachment supplies a real new source for board-routing analysis. The relevant next action is to compare its V05 component layout and visible traces with the V07 Reddit photo; **do not repeat the request for the owner's photographs before using these files**.

Acquisition record: `certification/source.json`. Direct device.report download, direct MIC endpoint and browser attempts failed with HTTP403/challenge; the FCCID PDF mirror succeeded. The mirror file's SHA256 equals the URL hash. External-photo attachment `220-J11880_01_001.pdf` was also acquired through the FCCID mirror after resuming the interrupted download; inspect its validity before relying on it.

### The layer above the gauge: PowerService

Recovered RTTI for `XTEink::Domain::Power::PowerService` at **0x3c2ecb58**, type record **0x3c2ecb80**, vtable address point **0x3c2ecb94**. Nine slots are now verified in `analyze_stock.py` and `offline-findings.json`; method windows and related dispatchers are saved in `disassembly/` (provisional reading copies also in `power-service/`):

| Address | Observed behavior / bounded interpretation |
|---|---|
| 0x4202463c | Getter builds a battery record from cached voltage/percentage/status fields |
| 0x422803a0 | Compares battery-record fields |
| 0x42024830 | Dispatches power-state choices |
| 0x42024890 | Shutdown/display policy; literal labels include Off, Wallpaper, InfoScreen |
| 0x4202492c | Sleep request through platform dispatcher |
| 0x42024720 | Reports wake/reset reason |
| 0x420246b0 | Builds light-sleep request and calls platform wrapper 0x42299774 |

The remaining two slots are trivial/destruction-related code. No charger-enable method or percentage-100 charge-stop action was identified in the inspected PowerService methods.

Also inspected the remaining CW2017 HAL power-lifecycle slots and their immediate helpers: wake cause 0x42150ea4, light sleep 0x42150ed0, deep sleep 0x4215119c and boot-release guard 0x421510a8. Helper **0x42151168** logs **cutLdo / keepLdo** and can write LOW to the known **GPIO1** record. This is a peripheral/power-rail action, not identification of a charger CE pin. It must not be repurposed as a charge-stop experiment.

Battery background loop **0x4214f1d4** invokes HAL vtable slot 3, updates charging-status cache and periodically copies the battery record; it also invokes a callback from platform object offset 4 at **0x4214f21e–0x4214f222**. This callback's full policy chain remains a useful software follow-up. The complete firmware call graph and arbitrary indirect calls are still not reconstructed.

Reproduction after extending the analyzer: `python3 qa_runs/charger-source-2026-11-06/analyze_stock.py` passes with the additional RTTI/vtable and method windows. `trace_power_xrefs.py` retains the previously checked direct-reference scope. No firmware source or image was changed.

### Exact continuation point

1. Read this section first, then visually use `certification/internal-page-2.jpg` and `internal-page-3.jpg`, plus the V07 originals in `followup/`. The reverse-side photo is already acquired.
2. Identify the charger from actual readable markings/package/layout and primary component documentation; treat ambiguous characters as hypotheses. Verify differences between V05 and V07 before claiming routing for Nikolai's unit.
3. Trace the remaining background callback at platform offset 4 and any consumers of the cached battery record, using the recovered PowerService vtable. Do not describe the existing partial graph as a complete decompilation.
4. Only after an actual CE/EN or equivalent route is identified, consider a controlled hardware stop/restart test. No blind GPIO writes, no OEM flashing, no changes to BATINFO on the device.

The scientific conclusion is unchanged: no 4.1 V profile or demonstrated BATINFO-only cutoff exists. The **work is still open**, and the new certification photographs create concrete work that can proceed without asking Nikolai to open his reader.
[/AI]

## Verdict 2026-11-06 22:00 +03:00 — can the firmware stop charging at 4.1 V or at N %?

[AI]
Owner's question: «можно ли отключать контроллер заряда на 4.1 · или на проценте каком-то». Voltage vs percent is the same question: the
firmware already knows both (CW2017 regs 0x02/0x03 and 0x04); what is missing is an actuator.

**Answer: no software-only path exists on this board as wired.** Evidence chain:
1. The I²C bus 39/38 was scanned on hardware (`freeink-sdk/docs/xteink-x4pro-support.md` § I²C): only 0x51 RTC, 0x63 CW2017, 0x5D GT911.
   No register-programmable charger (BQ25xxx/SGM4156x class) is present — nothing to send «stop at 4.1 V» to.
2. Stock 7.0.8 board init constructs exactly 17 pin objects (`offline-findings.json` → `board_pin_constructors`): outputs 1,2,4,5,8,9,11,12,13,14,18
   (rails, touch, SD, frontlight, display), inputs 0,3,6,7,10,21. Every output has a hardware-confirmed function; GPIO21 is the charger STAT input.
   No pin object for 15/16/17/43–48. The 23 GPIO writes (`trace_power_xrefs.py`) go through these objects; the two direct callers of the low-level
   GPIO helpers (0x421dfb66, 0x421ecbc6) take runtime pin arguments, not a charger constant. Stock therefore never drives a charge-enable line.
3. CW2017 is a gauge only: BATINFO changes the reported percent, not the charge current; INT_N/SOC_ALERT is a ~1 ms pulse with no proven route
   to the charger.
4. Public sources: no X4 Pro charger identification anywhere (MIC 220-J11880 photos ≤1135×851 px are unreadable; FCC has no internals;
   the X4 (C3) teardowns name no charger either). Upstream CrossPoint issue #2537 «charge limit 80%» is open with no implementation.
   One English digest claims «4056» on the original X4; the Chinese originals do not say this — unconfirmed, not carried over.
   Conclusion: a standalone linear charger with a STAT output (GPIO21 + rear LED red/white); its CE/EN, if it has one, is not routed to the MCU.

**What would make it possible:** a hardware mod — open the reader, macro-photo the charger near the USB/pogo input, and if the part has CE/EN,
route it to a GPIO that is verified unconnected (15/16/17 are candidates, NOT verified) with the right pull. Then a firmware cutoff at any % or
voltage is ordinary code. Owner's decision; not started.
**Available now without hardware:** a firmware reminder at a chosen % («отключи зарядку»), or an external USB timer/smart plug.

[TESTED: 2026-11-06 · pin list read from offline-findings.json; direct-caller scan of 0x421EC94C/0x421EC49C over stock-irom.bin (2 hits, runtime args);
I²C map quoted from SDK doc (on-hardware scan by its author, not re-run by me). Charger part, PCB routing of 15/16/17, CE presence — NOT verified.]
[/AI]
