# Четыре подготовленных PR — очередь отправки

[AI]
**Обновление 07.11.2026:** 01 опубликован как #4375; 03 как #4376 (зависимость обозначена); 02 как #4377. Выбранная пара и дополнительный третий PR отправлены по слову Николая. Дальнейшая очередь — 04, после освобождения слота и согласования базы.

07.11.2026 Николай выбрал следующую связанную пару: **01 меню очистки + 03 отложенная перерисовка** (ответ на уточнение: «Меню очистки + отложенная перерисовка»). Сначала 01; после его слияния — 03. Калибровка 02 и очистка Home/после шторки 04 остаются в очереди. Выбор сделан в обсуждении; автоматически не открывать. Ветки уже в его форке, чистые локальные деревья и SHA перечислены в queue.json. Описания с иллюстрациями — bodies/; ссылки на изображения проверены живым HEAD (assets-check.json). Код и ранее прошедшие сборки не переписывались. Повторить подготовительную проверку: python3 prepare_queue.py.

Выбранная пара: 01 подменю → 03 отложенная перерисовка. Остальная очередь: 02 калибровка; 04 очистка Home/после шторки. 02 независим; 03 ждёт слияния 01, 04 — 03. В апстрим нельзя открыть PR на ветку нашего форка как base: целимся в develop после слияния зависимостей, сверяем итоговый diff.

Когда Николай попросит отправлять:
1. gh pr list --repo crosspoint-reader/crosspoint-reader --author MikalaiKryvusha --state open — при пяти открытых остановиться, лимит не обходить.
2. Для первого готового пункта сверить remote SHA с queue.json и отсутствие уже открытого PR этой ветки; fetch upstream/develop, проверить mergeability и итоговый diff. Если база/контракты изменились — проверить затронутую часть, не обещать прежние результаты на новом коде.
3. Подставить известные номера зависимостей в отдельную копию описания; ссылки на ещё не созданные PR заменить названиями. Исходные одобренные тексты не терять.
4. gh pr create --repo crosspoint-reader/crosspoint-reader --base develop --head MikalaiKryvusha:<branch> --title <title> --body-file <resolved-body.md>. Рецензентам личные сообщения не отправлять.
5. Прочитать созданный PR и diff, сохранить URL/номер в queue.json; проверки GitHub запустятся автоматически. После появления следующих номеров дополнить перекрёстные ссылки.

Если upstream/develop существенно не разошёлся, отправка — короткая операция по готовой ветке/описанию. При конфликте или новой семантике не форсировать отправку ради пяти минут.
[/AI]

[AI]
**07.11.2026 23:43 +03:00 — 04 готов локально, ждёт слота.** `gh pr create` отклонён GitHub (нет прав на CreatePullRequest: пять открытых PR — лимит апстрима). Николай: «нет свободных мест … готовь локально». Ветка pr/screen-clean-return 8e063ced = remote, мёрдж с develop чистый, PR этой ветки нет. Описание — `../pr-publication-2026-11-07/04-home-control-center-clean.md` (#4375/#4376 подставлены, «пакет перерисовок», аппаратная проверка Николая). Когда слот освободится:
`cd ~/Xteink/pr-fixes/screen-clean-return && gh pr create --repo crosspoint-reader/crosspoint-reader --base develop --head MikalaiKryvusha:pr/screen-clean-return --title "feat: add Clean Home Screen and Clean After Control Center" --body-file ~/Xteink/qa_runs/pr-publication-2026-11-07/04-home-control-center-clean.md`
[/AI]

[AI]
**08.11.2026 00:27 +03:00 — вторая партия 11–13 готова локально** (заказ Николая «готовь, все равно будем их отправлять»). Ветки от develop 1d3536f0, в форке, сливаются чисто; сборки x4pro/default/симулятор SUCCESS, host 898/898; независимый судья: 11 и 12 без багов, по 13 два риска исправлены (выход свайпом от края возвращён, «наклон» убран). Кадры симулятора — pr-assets 11/12/13, ссылки HTTP 200. Описания — `../prs-2026-11-07-batch2/bodies/`. **Перед отправкой — вычитка текста Николаем.** Все три независимы, каждая занимает одно место из пяти.
- 11 `pr/night-epub-images` — fix(reader): dither EPUB images in Night Mode
- 12 `pr/lyra-title-lines` — feat(lyra): show up to five lines of the recent book title
- 13 `pr/viewer-reader-controls` — feat(viewer): turn images with the reader's page-turn settings
Команда (подставить id): `python3 -c "import json;e=[x for x in json.load(open('$HOME/Xteink/qa_runs/prs-2026-11-06/queue.json')) if x['id']=='11'][0];print(e['branch'],e['title'],e['body'],sep='\n')"`, затем `gh pr create --repo crosspoint-reader/crosspoint-reader --base develop --head MikalaiKryvusha:<branch> --title "<title>" --body-file <body>`.
[/AI]

[AI] **08.11.2026 00:38 +03:00 — добавлен 14** `pr/sleep-skip-truncated-bmp` — fix(sleep): skip truncated BMPs when picking from the sleep folders. Сборки SUCCESS, host 906/906 с новым тестом, судья без багов; описание `../prs-2026-11-07-batch2/bodies/14-sleep-skip-truncated-bmp.md`, кадр pr-assets/14 (HTTP 200). Тоже ждёт вычитки текста Николаем. [/AI]
