# Debug4 review

[AI]
Requirement: preserve debug3 and use a 20-minute periodic battery log; change version to debug4; deliver to SD.
Delta: BatteryLog.cpp interval, BatteryLog.h comments, platformio.ini version only.
Four independent read-only reviewers: correctness, architecture, embedded, i18n/docs. All reported no findings.
Events boot/sleep/charge retain existing behavior. Charge transitions are throttled at 10 seconds; successful explicit events reset the periodic timer.
No new timer, task, heap allocation, SDK change, or persistence format. Inherited debug3 firmware/SDK changes preserved.
Timing host checks PASS with ESP32-width uint32_t: 60-second suppression, 20-minute boundary, charge throttle/reset, wraparound.
Formatting wrapper completed successfully. Device behavior not tested. Build and delivery recorded separately.
Human authorization: STATUS FIRST quotes instruction to change to 20 minutes, build debug4 and copy to SD without asking again.
[/AI]
