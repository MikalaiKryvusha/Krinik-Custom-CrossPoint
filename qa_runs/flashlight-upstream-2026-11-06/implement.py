from pathlib import Path
import re,shutil,json
repo=Path('/Users/kryvusha/Xteink/pr-fixes/flashlight')
source=Path('/Users/kryvusha/Xteink/firmware')
def edit(name,old,new):
 p=repo/name;s=p.read_text();assert old in s,(name,old);p.write_text(s.replace(old,new))
edit('lib/hal/HalFrontlight.h','  void setOn(bool on);','''  void setOn(bool on);
  // Temporary perceptual output (0..255), without changing the saved brightness/on state.
  void setOutputLevel(uint8_t level);
  void restoreOutput();''')
p=repo/'lib/hal/HalFrontlight.cpp';p.write_text(p.read_text()+'''
void HalFrontlight::setOutputLevel(const uint8_t level) {
  if (manager.present()) manager.setBrightnessLevel(level);
}

void HalFrontlight::restoreOutput() { manager.setBrightness(lit ? lastBrightness : 0); }
''')
p=repo/'src/activities/util/FlashlightActivity.h';p.write_text('''#pragma once

#include "activities/Activity.h"

// Temporary white screen and full frontlight output. Exit restores the saved light state.
class FlashlightActivity final : public Activity {
 public:
  explicit FlashlightActivity(GfxRenderer& renderer, MappedInputManager& mappedInput)
      : Activity("Flashlight", renderer, mappedInput) {}
  void onEnter() override;
  void onExit() override;
  void loop() override;
  void render(RenderLock&& lock) override;
};
''')
s=(source/'src/activities/util/FlashlightActivity.cpp').read_text()
s=s.replace('Frontlight.rampOutputTo(255);  // full output over «Плавная подсветка»; saved brightness and on/off untouched','Frontlight.setOutputLevel(255);')
s=s.replace('Frontlight.restoreOutput(/*smooth=*/true);  // back to the saved brightness (or dark) over the same ramp','Frontlight.restoreOutput();')
s=s.replace('"Выйти");','tr(STR_FLASHLIGHT_EXIT));')
s=s.replace('''  // White page with the usual header band on top: back arrow + «Выйти», so the way out is plain (Nikolai
  // 04.11.2026). The rest of the glass stays white for light; a tap anywhere still leaves.''','''  // Keep the page white in either UI polarity; the header supplies the shared Back target.''')
s=s.replace('''  // Night mode inverts the whole output (the render task applies it before render()): pre-invert the buffer so the
  // glass shows this page as drawn — white, black header text — in either theme.''','''  // The render task applies night-mode polarity globally.''')
s=s.replace('#ifndef SIMULATOR  // the simulator HAL (external dependency, not ours to edit) has no raw light output','#ifndef SIMULATOR')
(repo/'src/activities/util/FlashlightActivity.cpp').write_text(s)
edit('src/activities/ActivityManager.h','SETTINGS_MENU };','SETTINGS_MENU, FLASHLIGHT };')
# Match the existing public navigation declaration rather than importing the fork's manager.
p=repo/'src/activities/ActivityManager.h';s=p.read_text();at=s.index('  void goToSettings(');s=s[:at]+'  void goToFlashlight();\n'+s[at:];p.write_text(s)
edit('src/activities/ActivityManager.cpp','#include "util/FrontlightPanelActivity.h"','#include "util/FrontlightPanelActivity.h"\n#include "util/FlashlightActivity.h"')
p=repo/'src/activities/ActivityManager.cpp';s=p.read_text();at=s.index('void ActivityManager::goToSettings(');s=s[:at]+'''void ActivityManager::goToFlashlight() {
  if (Frontlight.present()) replaceActivity(std::make_unique<FlashlightActivity>(renderer, mappedInput));
}

'''+s[at:];p.write_text(s)
p=repo/'src/activities/home/HomeActivity.cpp';s=p.read_text();s=s.replace('#include <HalDisplay.h>','#include <HalDisplay.h>\n#include <HalFrontlight.h>') if '#include <HalDisplay.h>' in s else s.replace('#include "HomeActivity.h"','#include "HomeActivity.h"\n\n#include <HalFrontlight.h>')
s=s.replace('int count = 4;  // File Browser, Library, File transfer, Settings','int count = 4 + (Frontlight.present() ? 1 : 0);  // Base actions and an optional flashlight')
s=s.replace('coverGridUi->begin(recentBooks, hasLibrarySlot(), hasContinueReading);','coverGridUi->begin(recentBooks, hasLibrarySlot(), hasContinueReading, Frontlight.present());')
s=s.replace('menuItemToIndex(initialMenuItem, hasLibrarySlot())','menuItemToIndex(initialMenuItem, hasLibrarySlot(), Frontlight.present())')
s=s.replace('indexToMenuItem(menuIndex, hasLibrarySlot())','indexToMenuItem(menuIndex, hasLibrarySlot(), Frontlight.present())')
s=s.replace('''      case HomeMenuItem::SETTINGS_MENU:
        onSettingsOpen();
        break;''','''      case HomeMenuItem::SETTINGS_MENU:
        onSettingsOpen();
        break;
      case HomeMenuItem::FLASHLIGHT:
        activityManager.goToFlashlight();
        break;''')
anchor='  std::vector<UIIcon> menuIcons = {Folder, Library, Transfer, Settings};'
assert anchor in s;s=s.replace(anchor,anchor+'''
  if (Frontlight.present()) {
    menuItems.push_back(tr(STR_FLASHLIGHT));
    menuIcons.push_back(Flashlight);
  }''')
p.write_text(s)
p=repo/'src/activities/home/HomeActivity.h';s=p.read_text().replace('HomeMenuItem item, bool hasOpdsUrl)','HomeMenuItem item, bool hasOpdsUrl, bool hasFlashlight)').replace('int idx, bool hasOpdsUrl)','int idx, bool hasOpdsUrl, bool hasFlashlight)')
s=s.replace('''    if (item == HomeMenuItem::SETTINGS_MENU) return i;
    return 0;''','''    if (item == HomeMenuItem::SETTINGS_MENU) return i;
    ++i;
    if (hasFlashlight && item == HomeMenuItem::FLASHLIGHT) return i;
    return 0;''')
s=s.replace('''    if (idx == i) return HomeMenuItem::SETTINGS_MENU;
    return HomeMenuItem::NONE;''','''    if (idx == i++) return HomeMenuItem::SETTINGS_MENU;
    if (hasFlashlight && idx == i) return HomeMenuItem::FLASHLIGHT;
    return HomeMenuItem::NONE;''')
p.write_text(s)
edit('src/components/themes/BaseTheme.h','  Blocks\n};','  Blocks,\n  Flashlight\n};')
shutil.copyfile(source/'src/components/icons/flashlight.h',repo/'src/components/icons/flashlight.h')
p=repo/'src/components/icons/flashlight.h';s=p.read_text().replace(' outline, krinik «Фонарик»',' outline');p.write_text(s)
p=repo/'src/components/themes/lyra/LyraTheme.cpp';s=p.read_text();s=s.replace('#include "icons/folder.h"','#include "icons/folder.h"\n#include "icons/flashlight.h"');s=s.replace('''    case UIIcon::Blocks:
      return BlocksIcon;''','''    case UIIcon::Blocks:
      return BlocksIcon;
    case UIIcon::Flashlight:
      return FlashlightIcon;''');p.write_text(s)
p=repo/'src/components/CoverGridHomeUi.h';s=p.read_text().replace('bool hasContinueReading);','bool hasContinueReading, bool hasFlashlight);').replace('  bool hasContinueReading = false;','  bool hasContinueReading = false;\n  bool hasFlashlight = false;').replace('TabItem, 5>','TabItem, 6>');p.write_text(s)
p=repo/'src/components/CoverGridHomeUi.cpp';s=p.read_text().replace('#include "icons/folder.h"','#include "icons/folder.h"\n#include "icons/flashlight.h"');s=s.replace('bool hasContinueReading) {','bool hasContinueReading, bool hasFlashlight) {').replace('  this->hasContinueReading = hasContinueReading;','  this->hasContinueReading = hasContinueReading;\n  this->hasFlashlight = hasFlashlight;');s=s.replace('TransferIcon, Settings2Icon};','TransferIcon, Settings2Icon, FlashlightIcon};').replace('for (int i = 0; i < 5; ++i) {','for (int i = 0; i < 6; ++i) {\n    if (i == 5 && !hasFlashlight) continue;');p.write_text(s)
words={'arabic':'مصباح يدوي','azerbaijani':'Fənər','belarusian':'Ліхтарык','bosnian':'Svjetiljka','bulgarian':'Фенерче','catalan':'Llanterna','czech':'Svítilna','danish':'Lommelygte','dutch':'Zaklamp','english':'Flashlight','finnish':'Taskulamppu','french':'Lampe torche','german':'Taschenlampe','hebrew':'פנס','hungarian':'Zseblámpa','indonesia':'Senter','italian':'Torcia','kazakh':'Қолшам','lithuanian':'Žibintuvėlis','norwegian':'Lommelykt','orangutan':'Flashlight','persian':'چراغ‌قوه','polish':'Latarka','portuguese-BR':'Lanterna','portuguese-PT':'Lanterna','romanian':'Lanternă','russian':'Фонарик','slovak':'Baterka','slovenian':'Svetilka','spanish':'Linterna','swedish':'Ficklampa','turkish':'El feneri','ukrainian':'Ліхтарик','valencian':'Llanterna','vietnamese':'Đèn pin'}
for p in (repo/'lib/I18n/translations').glob('*.yaml'):
 assert p.stem in words,p.stem
 s=p.read_text();assert 'STR_FLASHLIGHT:' not in s
 match=re.search(r'^STR_EXIT: "(.*)"$',s,re.M)
 exit=match.group(1).strip('«» ') if match else 'Exit'
 s+='\nSTR_FLASHLIGHT: '+json.dumps(words[p.stem],ensure_ascii=False)+'\nSTR_FLASHLIGHT_EXIT: '+json.dumps(exit,ensure_ascii=False)+'\n'
 p.write_text(s)
print('Focused flashlight candidate added with runtime capability gate and 35 locale entries.')
