# Возврат из калибровочных карточек

[AI]
Николай сообщил: возврат ведёт в меню калибровки, но по дороге видны экраны
настроек. Вопрос был о причине и возможности прямого возврата; исправление
в этой задаче не выполнялось.

Исследованы исходники выпущенной 1.1.0 (firmware/nikolai 8dd71e19):
- SettingsActivity.cpp:349: карточки открываются через goToReader(path).
- ActivityManager.cpp:215: Replace уничтожает предыдущую activity и её стек.
- BmpViewerActivity.cpp:614 и ReaderUtils.h:269: возвращение задаёт pending
  ScreenCalibration и вызывает goToSettings(Display).
- ActivityManager.cpp:307: создаётся SettingsListActivity(openSection).
- SettingsListActivity.cpp:38: Display открывается из loop(), после onEnter.
- SettingsActivity.cpp:242: подраздел калибровки открывается ещё одним
  отложенным переходом из handleCustomInput().

По коду подтверждена цепочка SettingsList → Display → ScreenCalibration.
Сообщение владельца согласуется с возможной отрисовкой промежуточных activity;
кадры устройства в этой сессии не снимались, число перерисовок не измерено.
Это маршрут нашего расширения, а не обязательный интерфейсный контракт
CrossPoint. Upstream уже имеет pushActivity/popActivity/Activity::finish.

Направление исправления: прямое открытие требуемого подраздела с правильной
последующей цепочкой Back, без показа промежуточных экранов. Не выбирать
вслепую сохранение всех settings activity за EPUB: reader Replace освобождает
их память; при реализации требуется проверить C3 baseline и обе карточки.
Один и тот же судья проверяет будущую навигационную правку отдельно от путей
кривых.
[/AI]
