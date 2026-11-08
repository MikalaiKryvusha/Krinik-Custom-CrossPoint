# Единый судья: итоговое delta review — 05.11.2026

[AI]
VERIFIED WITH CAVEATS. Тот же один независимый судья проверил EPUB delta после начального REFUTED. Новых P1/P2/P3 нет; P2/P3 устранены.

- Synthetic fallback полностью завершается до последующих source IDs, поэтому одинаковый canonical offset не связывает их с ранней страницей.
- Обычный inline ID распознаётся и в пустом ParsedText; риск позднего pendingAnchorId устранён.
- Canonical offsets и формат ParsedText/TextBlock не менялись; syntheticTextOffsets удалён.
- Осознанное изменение переносов: alt — отдельный завершённый блок, далее parent style. Проверка anchor==TARGET в прежнем тесте сохранена при переходе ожидаемой страницы 1→2.
- v74 документирует completed/partial cache rebuild и fallback blocks.
- Прочитаны три исходных падения и полный зелёный прогон 918/918; тесты before/after, no-space, two images, long target, parent style/source range.
- SDK/Sleep git tree совпадают с рассмотренными; About меняет только ссылку на SDK с тем же деревом.

Заключение: по коду все три исправления пригодны для отправки в существующие PR. Перед готовностью остаются две финальные EPUB-сборки, а перед About push — доступность SDK SHA через URL подмодуля. Аппаратные пограничные проверки не проводились.
[/AI]
