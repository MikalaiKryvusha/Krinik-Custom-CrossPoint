"""Record the narrow port from the released personal fork to upstream develop."""
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path('/Users/kryvusha/Xteink')
WORK = ROOT / 'pr-fixes/calibration'
SOURCE = ROOT / 'pr-fixes/krinik'

def edit(relative, old, new):
    path = WORK / relative
    text = path.read_text()
    assert text.count(old) == 1, (relative, old)
    path.write_text(text.replace(old, new))

pure = [
    'lib/BmpToBmpConverter', 'lib/Epub/Epub/converters',
    'lib/Epub/Epub/blocks/ImageBlock.cpp', 'lib/Epub/Epub/blocks/ImageBlock.h',
    'src/activities/reader/ReaderActivity.cpp', 'src/activities/reader/ReaderUtils.h',
    'src/activities/settings/SettingsListActivity.cpp', 'src/activities/settings/SettingsListActivity.h',
    'src/network/CrossPointWebServer.cpp',
]
patch = subprocess.check_output(['git', 'diff', '5936f485', 'nikolai', '--', *pure], cwd=SOURCE)
subprocess.run(['git', 'apply', '--check', '-'], input=patch, cwd=WORK, check=True)
subprocess.run(['git', 'apply', '-'], input=patch, cwd=WORK, check=True)
for relative in ['src/util/PanelCurve.cpp', 'src/util/PanelCurve.h', 'src/util/CalibrationCard.cpp',
                 'src/util/CalibrationCard.h', 'src/util/CalibrationCardStorage.cpp']:
    shutil.copyfile(SOURCE / relative, WORK / relative)
for directory in ['test/calibration_card', 'test/panel_curve']:
    shutil.copytree(SOURCE / directory, WORK / directory)
edit('test/CMakeLists.txt', 'add_subdirectory(bmp_to_bmp)',
     'add_subdirectory(bmp_to_bmp)\nadd_subdirectory(calibration_card)\nadd_subdirectory(panel_curve)')

# A curve measured on one physical panel must not become the upstream default.
path = WORK / 'src/util/PanelCurve.cpp'
text = path.read_text()
text, n = re.subn(r'// Inverse of this X4 Pro.*?constexpr uint8_t (?:BUILT_IN|BOOK_BUILT_IN)\[256\] = \{.*?\};\n', '', text, flags=re.S)
assert n == 2
text = text.replace('PATH, BUILT_IN}', 'PATH, IDENTITY}').replace('BOOK_PATH, BOOK_BUILT_IN}', 'BOOK_PATH, IDENTITY}')
text = text.replace('Built-in curve %s', 'Identity fallback %s')
path.write_text(text)
path = WORK / 'src/util/PanelCurve.h'
text = path.read_text()
start = text.index('// The pictures curve')
end = text.index('bool load(', start)
text = text[:start] + '// Pictures and custom sleep images: identity when disabled or no valid card curve exists.\n' + text[end:]
text = text.replace('panel_curve_book.txt or the built-in book curve;', 'panel_curve_book.txt or identity;')
path.write_text(text)

edit('src/CrossPointSettings.h', '  uint8_t textAntiAliasing = 1;',
     '  uint8_t panelCalPictures = 0;\n  uint8_t panelCalBooks = 0;\n  uint8_t textAntiAliasing = 1;')
edit('src/SettingsList.cpp', '  // --- Reader ---',
'''  emit(SettingInfo::Toggle(StrId::STR_PANEL_CAL_PICTURES, &CrossPointSettings::panelCalPictures,
                           "panelCalPictures", StrId::STR_CAT_DISPLAY));
  emit(SettingInfo::Toggle(StrId::STR_PANEL_CAL_BOOKS, &CrossPointSettings::panelCalBooks,
                           "panelCalBooks", StrId::STR_CAT_DISPLAY));

  // --- Reader ---''')
edit('src/activities/settings/SettingsSection.h', 'Network, End };', 'Network, End, ScreenCalibration };')
with (WORK / 'src/activities/settings/SettingsSection.h').open('a') as stream:
    stream.write('\n// Consumed when Display rebuilds the return path before its first render.\n'
                 'inline SettingsSection pendingSettingsSubSection = SettingsSection::End;\n')
edit('src/activities/settings/SettingsActivity.h', '  None,\n',
     '  None,\n  ScreenCalibrationSettings,\n  CalibrationPicturesScreen,\n  CalibrationBooksScreen,\n')
edit('src/activities/settings/SettingsActivity.cpp', '#include "util/PluginEvents.h"',
     '#include "util/PluginEvents.h"\n#include "util/CalibrationCard.h"\n#include "util/PanelCurve.h"')
edit('src/activities/settings/SettingsActivity.cpp', '  if (setting.valuePtr == &CrossPointSettings::sleepTimeoutMinutes)',
'''  if (setting.valuePtr == &CrossPointSettings::panelCalPictures ||
      setting.valuePtr == &CrossPointSettings::panelCalBooks) return SettingsSection::ScreenCalibration;
  if (setting.valuePtr == &CrossPointSettings::sleepTimeoutMinutes)''')
edit('src/activities/settings/SettingsActivity.cpp', '  for (auto& setting : all) {',
'''  addAction(SettingsSection::ScreenCalibration, StrId::STR_CAL_PICTURES_SCREEN,
            SettingAction::CalibrationPicturesScreen);
  addAction(SettingsSection::ScreenCalibration, StrId::STR_CAL_BOOKS_SCREEN, SettingAction::CalibrationBooksScreen);
  for (auto& setting : all) {''')
edit('src/activities/settings/SettingsActivity.cpp', '  addAction(SettingsSection::General, StrId::STR_ABOUT, SettingAction::About);',
'''  addAction(SettingsSection::Display, StrId::STR_PANEL_CALIBRATION, SettingAction::ScreenCalibrationSettings);
  addAction(SettingsSection::General, StrId::STR_ABOUT, SettingAction::About);''')
needle = '  rebuildSettings();\n}\n\n// Rebuilds rowValues_'
edit('src/activities/settings/SettingsActivity.cpp', needle,
'''  rebuildSettings();
  if (section == SettingsSection::Display && pendingSettingsSubSection != SettingsSection::End) {
    const SettingsSection sub = pendingSettingsSubSection;
    pendingSettingsSubSection = SettingsSection::End;
    if (auto activity = makeUniqueNoThrow<SettingsActivity>(renderer, mappedInput, sub)) {
      startActivityForResult(std::move(activity), [this](const ActivityResult&) { requestUpdate(); });
    }
  }
}

// Rebuilds rowValues_''')
edit('src/activities/settings/SettingsActivity.cpp', 'const char* SettingsActivity::headerTitle() const {\n',
'''const char* SettingsActivity::headerTitle() const {
  if (section == SettingsSection::ScreenCalibration) return tr(STR_PANEL_CALIBRATION);
''')
edit('src/activities/settings/SettingsActivity.cpp', '    SETTINGS.*(setting.valuePtr) = !currentValue;',
'''    SETTINGS.*(setting.valuePtr) = !currentValue;
    if (setting.valuePtr == &CrossPointSettings::panelCalPictures ||
        setting.valuePtr == &CrossPointSettings::panelCalBooks) panelcurve::forget();''')
source_text = (SOURCE / 'src/activities/settings/SettingsActivity.cpp').read_text()
start = source_text.index('      case SettingAction::ScreenCalibrationSettings:')
end = source_text.index('      case SettingAction::HomeButton:', start)
edit('src/activities/settings/SettingsActivity.cpp', '      case SettingAction::HomeButton:',
     source_text[start:end] + '      case SettingAction::HomeButton:')
start = source_text.index('  // What this sub-screen is for')
end = source_text.index('  // rowItems_', start)
note = source_text[start:end]
note = note.replace('  // What this sub-screen is for, above its rows (Nikolai 05.11.2026).\n', '')
note = note.replace('section == SettingsSection::ScreenClean || section == SettingsSection::ScreenCalibration',
                    'section == SettingsSection::ScreenCalibration')
note = note.replace('section == SettingsSection::ScreenClean ? tr(STR_SCREEN_CLEAN_NOTE) : tr(STR_PANEL_CAL_NOTE)',
                    'tr(STR_PANEL_CAL_NOTE)')
edit('src/activities/settings/SettingsActivity.cpp', '  // rowItems_ (label/actionValue) was built by rebuildRowItems(); only the',
     note + '  // rowItems_ (label/actionValue) was built by rebuildRowItems(); only the')

edit('src/activities/ActivityManager.cpp', '#include <BlePageTurner.h>',
     '#include <BlePageTurner.h>\n#include <Epub/blocks/ImageBlock.h>\n#include "util/PanelCurve.h"')
edit('src/activities/ActivityManager.cpp', '  auto activity = ReaderActivity::create(',
'''  uint32_t bookCurveHash = 0;
  const uint8_t* bookCurve = panelcurve::bookCurve(bookCurveHash);
  ImageBlock::setToneCurve(bookCurve, bookCurveHash);
  auto activity = ReaderActivity::create(''')
edit('src/activities/ActivityManager.cpp', 'void ActivityManager::goHome(HomeMenuItem initialMenuItem, bool cleanInitialRefresh) {',
'''void ActivityManager::goHome(HomeMenuItem initialMenuItem, bool cleanInitialRefresh) {
  pendingSettingsSubSection = SettingsSection::End;''')
edit('src/activities/reader/EpubReaderActivity.cpp', '#include "util/BookmarkUtil.h"',
     '#include "util/BookmarkUtil.h"\n#include "util/CalibrationCard.h"')
edit('src/activities/reader/EpubReaderActivity.cpp', '  if (SETTINGS.removeReadBooksFromRecents) {',
     '  if (SETTINGS.removeReadBooksFromRecents && !calibcard::isCalibrationPath(epub->getPath())) {')
edit('src/activities/reader/EpubReaderActivity.cpp',
     '    pendingReadFolderMove = SETTINGS.moveFinishedToReadFolder && !isInReadFolder(epub->getPath());',
'''    pendingReadFolderMove = SETTINGS.moveFinishedToReadFolder && !isInReadFolder(epub->getPath()) &&
                            !calibcard::isCalibrationPath(epub->getPath());''')

# Reuse the released card text; other languages retain the normal English fallback.
keys = ('STR_PANEL_CALIBRATION:', 'STR_CAL_PICTURES_SCREEN:', 'STR_CAL_BOOKS_SCREEN:',
        'STR_PANEL_CAL_PICTURES:', 'STR_PANEL_CAL_BOOKS:', 'STR_PANEL_CAL_NOTE:', 'STR_CAL_CARD_FAILED:')
for path in (WORK / 'lib/I18n/translations').glob('*.yaml'):
    lines = (SOURCE / 'lib/I18n/translations' / path.name).read_text().splitlines()
    additions = [line for line in lines if line.startswith(keys)]
    if additions:
        path.write_text(path.read_text().rstrip() + '\n' + '\n'.join(additions) + '\n')
print('Calibration core, settings, reader and converter port prepared; viewer/sleep wiring pending')
