"""Prepare the delayed redraw candidate on top of the cleaning submenu."""
from pathlib import Path

ROOT = Path('/Users/kryvusha/Xteink')
WORK = ROOT / 'pr-fixes/screen-redraw-delay'
PERSONAL = ROOT / 'pr-fixes/krinik'

def edit(relative, old, new):
    path = WORK / relative
    text = path.read_text()
    if new in text:
        assert text.count(new) == 1, (relative, 'already applied more than once')
        return
    assert text.count(old) == 1, (relative, old)
    path.write_text(text.replace(old, new))

edit('src/CrossPointSettings.h', '  uint8_t textAntiAliasing = 1;', '''  enum REDRAW_DELAY { REDRAW_OFF = 0, REDRAW_1_MIN, REDRAW_2_MIN, REDRAW_5_MIN, REDRAW_DELAY_COUNT };
  static uint32_t redrawDelayMinutes(const uint8_t value) {
    static constexpr uint32_t minutes[] = {0, 1, 2, 5};
    return minutes[value < REDRAW_DELAY_COUNT ? value : 0];
  }
  uint8_t sleepSettledRedraw = REDRAW_OFF;
  uint8_t imageSettledRedraw = REDRAW_OFF;
  uint8_t textAntiAliasing = 1;''')
edit('src/SettingsList.cpp', '  // --- Reader ---', '''  if (BoardConfig::isX4Pro()) {
    emit(SettingInfo::Enum(StrId::STR_SLEEP_SETTLED_REDRAW, &CrossPointSettings::sleepSettledRedraw,
                           {StrId::STR_STATE_OFF, StrId::STR_AFTER_1_MIN, StrId::STR_AFTER_2_MIN, StrId::STR_AFTER_5_MIN},
                           "sleepRedrawDelay", StrId::STR_CAT_DISPLAY));
  }
  emit(SettingInfo::Enum(StrId::STR_IMAGE_SETTLED_REDRAW, &CrossPointSettings::imageSettledRedraw,
                         {StrId::STR_STATE_OFF, StrId::STR_AFTER_1_MIN, StrId::STR_AFTER_2_MIN, StrId::STR_AFTER_5_MIN},
                         "imageRedrawDelay", StrId::STR_CAT_DISPLAY));

  // --- Reader ---''')
edit('src/activities/settings/SettingsActivity.cpp', 'setting.valuePtr == &CrossPointSettings::fadingFix)',
'''setting.valuePtr == &CrossPointSettings::fadingFix ||
      setting.valuePtr == &CrossPointSettings::sleepSettledRedraw ||
      setting.valuePtr == &CrossPointSettings::imageSettledRedraw)''')
for language in ('english', 'russian'):
    path = WORK / f'lib/I18n/translations/{language}.yaml'
    lines = (PERSONAL / f'lib/I18n/translations/{language}.yaml').read_text().splitlines()
    keys = ('STR_SLEEP_SETTLED_REDRAW:', 'STR_IMAGE_SETTLED_REDRAW:', 'STR_AFTER_1_MIN:', 'STR_AFTER_2_MIN:', 'STR_AFTER_5_MIN:')
    path.write_text(path.read_text().rstrip() + '\n' + '\n'.join(line for line in lines if line.startswith(keys)) + '\n')

# The renderer owns all image paints, including the one requested by the timer
# and the repaint after a child sheet returns. No timer task draws directly.
edit('src/activities/util/BmpViewerActivity.h', '  void loop() override;',
'''  void loop() override;
  void render(RenderLock&&) override;''')
edit('src/activities/util/BmpViewerActivity.h', '  std::string filePath;',
'''  unsigned long paintedAtMs = 0;
  bool settledRedrawDone = false;
  std::string filePath;''')
edit('src/activities/util/BmpViewerActivity.cpp', '  const auto pageWidth = renderer.getScreenWidth();',
'''  settledRedrawDone = false;
  requestUpdate();
}

void BmpViewerActivity::render(RenderLock&&) {
  const ScopedCleanup recordPaint{[this]() { paintedAtMs = millis(); }};
  const auto pageWidth = renderer.getScreenWidth();''')
edit('src/activities/util/BmpViewerActivity.cpp', '  Activity::loop();',
'''  Activity::loop();
  const uint32_t settleMs = CrossPointSettings::redrawDelayMinutes(SETTINGS.imageSettledRedraw) * 60000UL;
  if (settleMs > 0 && !settledRedrawDone && millis() - paintedAtMs >= settleMs) {
    settledRedrawDone = true;
    LOG_DBG("BMP", "Settled image redraw");
    requestUpdate();
  }''')

edit('src/activities/boot_sleep/SleepActivity.h', '  void onEnter() override;',
'''  void onEnter() override;
  static const std::string& lastCustomImagePath();
  static bool redrawCustomImage(GfxRenderer& renderer, MappedInputManager& input, const std::string& path);''')
edit('src/activities/boot_sleep/SleepActivity.cpp', 'void SleepActivity::onEnter() {',
'''namespace {
std::string lastCustomSleepPath;
}

const std::string& SleepActivity::lastCustomImagePath() { return lastCustomSleepPath; }

bool SleepActivity::redrawCustomImage(GfxRenderer& renderer, MappedInputManager& input, const std::string& path) {
  const SleepActivity painter(renderer, input);
  display.setInverted(false);
  if (painter.renderCustomSleepBmp(path)) return true;
  painter.renderDefaultSleepScreen();
  return false;
}

void SleepActivity::onEnter() {''')
# The declaration must precede renderCustomSleepBmp, which records successful draws.
path = WORK / 'src/activities/boot_sleep/SleepActivity.cpp'
text = path.read_text()
text = text.replace('namespace {\nstd::string lastCustomSleepPath;\n}\n\n', '')
position = text.index('namespace {') + len('namespace {')
text = text[:position] + '\nstd::string lastCustomSleepPath;\n' + text[position:]
path.write_text(text)
edit('src/activities/boot_sleep/SleepActivity.cpp', '  Activity::onEnter();',
     '  Activity::onEnter();\n  lastCustomSleepPath.clear();')
edit('src/activities/boot_sleep/SleepActivity.cpp', '        renderBitmapSleepScreen(bitmap);\n        return true;',
     '        renderBitmapSleepScreen(bitmap);\n        lastCustomSleepPath = path;\n        return true;')
edit('src/activities/boot_sleep/SleepActivity.cpp', '  renderBitmapSleepScreen(bitmap);\n  return true;',
     '  renderBitmapSleepScreen(bitmap);\n  lastCustomSleepPath = path;\n  return true;')

edit('src/main.cpp', '#include "activities/settings/SdFirmwareUpdateActivity.h"',
'''#include "activities/settings/SdFirmwareUpdateActivity.h"
#if FREEINK_DEVICE_X4PRO && !defined(SIMULATOR)
#include <esp_sleep.h>
#include "activities/boot_sleep/SleepActivity.h"
#endif''')
edit('src/main.cpp', '// Enter deep sleep mode',
'''#if FREEINK_DEVICE_X4PRO && !defined(SIMULATOR)
RTC_DATA_ATTR char sleepRedrawPath[192];
static bool bootWasPanic = false;
static volatile bool settledRedrawPress = false;
static void IRAM_ATTR onSettledRedrawPress() { settledRedrawPress = true; }
#endif

// Enter deep sleep mode''')
edit('src/main.cpp', '  halTiltSensor.deepSleep();\n  display.deepSleep();\n  Storage.prepareForDeepSleep();\n  LOG_DBG("MAIN", "Entering deep sleep");',
'''#if FREEINK_DEVICE_X4PRO && !defined(SIMULATOR)
  sleepRedrawPath[0] = '\\0';
  const auto& imagePath = SleepActivity::lastCustomImagePath();
  const uint32_t minutes = CrossPointSettings::redrawDelayMinutes(SETTINGS.sleepSettledRedraw);
  if (minutes > 0 && !isQuickResumeSleep && !bootWasPanic && powerManager.getBatteryPercentage() >= 15 &&
      !imagePath.empty() && imagePath.size() < sizeof(sleepRedrawPath)) {
    memcpy(sleepRedrawPath, imagePath.c_str(), imagePath.size() + 1);
    if (esp_sleep_enable_timer_wakeup(static_cast<uint64_t>(minutes) * 60000000ULL) != ESP_OK) {
      sleepRedrawPath[0] = '\\0';
      LOG_ERR("MAIN", "Could not arm the sleep-image redraw");
    }
  }
#endif
  halTiltSensor.deepSleep();
  display.deepSleep();
  Storage.prepareForDeepSleep();
  LOG_DBG("MAIN", "Entering deep sleep");''')
edit('src/main.cpp', 'void setupDisplayAndFonts(bool seamless = false) {',
'''void setupDisplayAndFonts(bool seamless = false) {
  static bool initialized = false;
  if (initialized) return;
  initialized = true;''')
edit('src/main.cpp', '  const bool rebootedFromPanic = HalSystem::isRebootFromPanic();',
'''  const bool rebootedFromPanic = HalSystem::isRebootFromPanic();
#if FREEINK_DEVICE_X4PRO && !defined(SIMULATOR)
  bootWasPanic = rebootedFromPanic;
#endif''')
edit('src/main.cpp', '  const auto wakeupReason = gpio.getWakeupReason();', '  auto wakeupReason = gpio.getWakeupReason();')
edit('src/main.cpp', '  const bool isSleepWake = wakeupReason == HalGPIO::WakeupReason::PowerButton;',
     '  bool isSleepWake = wakeupReason == HalGPIO::WakeupReason::PowerButton;')
edit('src/main.cpp', '  const bool isPersistedSleepWake = isSleepWake && !APP_STATE.showBootScreen;',
     '  bool isPersistedSleepWake = isSleepWake && !APP_STATE.showBootScreen;')
edit('src/main.cpp', '  // Brightness and warmth are always restored.',
'''#if FREEINK_DEVICE_X4PRO && !defined(SIMULATOR)
  const bool timerRedraw = esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_TIMER && sleepRedrawPath[0] != '\\0';
  if (timerRedraw && !rebootedFromPanic && !isSilentReboot) {
    const std::string path = sleepRedrawPath;
    sleepRedrawPath[0] = '\\0';
    settledRedrawPress = false;
    const int8_t pin = BoardConfig::ACTIVE.input.power;
    if (pin >= 0) attachInterrupt(pin, onSettledRedrawPress, BoardConfig::ACTIVE.input.powerActiveHigh ? RISING : FALLING);
    setupDisplayAndFonts(/*seamless=*/true);
    SleepActivity::redrawCustomImage(renderer, mappedInputManager, path);
    if (pin >= 0) detachInterrupt(pin);
    const bool clickWakes = settledRedrawPress && SETTINGS.shortPwrBtn == CrossPointSettings::SHORT_PWRBTN::SLEEP;
    if (!clickWakes && !gpio.verifyPowerButtonWakeup()) {
      halTiltSensor.deepSleep();
      display.deepSleep();
      Storage.prepareForDeepSleep();
      powerManager.startDeepSleep(gpio);
    }
    wakeupReason = HalGPIO::WakeupReason::PowerButton;
    isSleepWake = true;
    isPersistedSleepWake = !APP_STATE.showBootScreen;
  }
  sleepRedrawPath[0] = '\\0';
#endif

  // Brightness and warmth are always restored.''')
print('Delayed redraw source prepared; final verification pending')
