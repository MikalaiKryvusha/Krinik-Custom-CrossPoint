"""Recompute the owner's two logged discharge stages; source CSV stays untouched.
Run: python3 -s analyze.py (system NumPy 1.x matches installed matplotlib).
"""
import csv
import hashlib
import json
import statistics
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent
ZONE = ZoneInfo('Europe/Minsk')
raw = (BASE / 'battery_log.csv').read_bytes()
meta = json.loads((BASE / 'acquisition.json').read_text())
assert hashlib.sha256(raw).hexdigest() == meta['sha256']
rows = [{k: (v if k == 'event' else int(v)) for k, v in r.items()}
        for r in csv.DictReader(raw.decode().splitlines())]
start = max(i for i, r in enumerate(rows) if r['event'] == 'boot')
on = next(i for i in range(start + 1, len(rows)) if rows[i]['light_on'] == 1)
end = next(i for i in range(on + 1, len(rows)) if rows[i]['light_on'] == 0)
off_rows, on_rows = rows[start:on], rows[on:end]
window = rows[start:end + 1]
assert all(r['charging'] == 0 for r in window)
assert all(r['event'] == 'tick' for r in window[1:])
assert all(r['light_on'] == 0 for r in off_rows)
assert all(r['light_on'] == 1 and r['brightness_pct'] == 100 and r['warm_pct'] == 50 for r in on_rows)
gaps = [b['uptime_s'] - a['uptime_s'] for a, b in zip(window, window[1:])]
assert min(gaps) >= 60 and max(gaps) <= 61
assert 3540 <= rows[on]['epoch'] - rows[start]['epoch'] <= 3660
assert 3540 <= rows[end]['epoch'] - rows[on]['epoch'] <= 3660

def stamp(r):
    return datetime.fromtimestamp(r['epoch'], ZONE).strftime('%H:%M:%S')

def stats(stage):
    t = [r['uptime_s'] for r in stage]
    y = [r['soc_pct'] for r in stage]
    tx, ty = statistics.mean(t), statistics.mean(y)
    slope = sum((a - tx) * (b - ty) for a, b in zip(t, y)) / sum((a - tx) ** 2 for a in t) * 3600
    return {'samples': len(stage), 'first': stage[0], 'last': stage[-1],
            'sample_span_seconds': stage[-1]['epoch'] - stage[0]['epoch'],
            'observed_soc_drop_pp': y[0] - y[-1], 'linear_fit_pp_per_hour': slope}

result = {'source_sha256': meta['sha256'], 'total_rows': len(rows),
          'off': stats(off_rows), 'on_100_warm_50': stats(on_rows),
          'first_on': rows[on], 'first_off_after_test': rows[end],
          'phase_marker_elapsed_seconds': [rows[on]['epoch'] - rows[start]['epoch'], rows[end]['epoch'] - rows[on]['epoch']],
          'boundary_soc_before_after': [rows[on - 1]['soc_pct'], rows[on]['soc_pct']],
          'total_soc_drop_pp': rows[start]['soc_pct'] - rows[end]['soc_pct'],
          'max_sample_gap_seconds_uptime': max(gaps),
          'voltage_on_transition_adjacent_samples_mv': rows[on]['vcell_mv'] - rows[on - 1]['vcell_mv'],
          'voltage_off_transition_adjacent_samples_mv': rows[end]['vcell_mv'] - rows[end - 1]['vcell_mv'],
          'logging_energy_isolated': False, 'current_measured': False,
          'owner_proposal': 'Periodic log interval 20 minutes; not implemented or tested.'}
(BASE / 'analysis.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
fig, axes = plt.subplots(2, 1, figsize=(11.4, 7.5), sharex=True, layout='constrained')
fig.suptitle('Читалка debug2 · два часовых этапа разряда\n6 ноября 2026 · без кабеля, в бодрствовании', fontsize=16)
t0 = rows[start]['epoch']
x = [(r['epoch'] - t0) / 60 for r in window]
cut, last = (rows[on]['epoch'] - t0) / 60, x[-1]
for ax in axes:
    ax.axvspan(0, cut, color='#2474b5', alpha=.07)
    ax.axvspan(cut, last, color='#df7c17', alpha=.09)
    ax.axvspan((rows[on-1]['epoch'] - t0)/60, cut, color='#333333', alpha=.12)
    ax.grid(alpha=.2)
    ax.spines[['top','right']].set_visible(False)
    ax.axvline(cut, color='#666666', lw=1, ls='--')
axes[0].plot(x, [r['soc_pct'] for r in window], color='#24374b', marker='.', ms=4, lw=1.4)
axes[0].set_ylabel('Показание заряда, %')
axes[0].set_ylim(85, 102)
axes[0].text(4, 101, 'Свет выключен', color='#2474b5', va='top')
axes[0].text(cut + 4, 101, 'Яркость 100% · тёплость 50%', color='#ac5a08', va='top')
axes[0].annotate('100 → 96% до переключения', xy=(52,96), xytext=(9,92), arrowprops={'arrowstyle':'->','color':'#2474b5'}, color='#2474b5')
axes[0].annotate('95 → 87% после переключения', xy=(110,87), xytext=(67,94), arrowprops={'arrowstyle':'->','color':'#ac5a08'}, color='#ac5a08')
axes[1].plot(x, [r['vcell_mv']/1000 for r in window], color='#24374b', marker='.', ms=4, lw=1.4)
axes[1].set_ylabel('Показание напряжения, В')
axes[1].set_xlabel('Минуты от первой записи этапа · начало 18:13:40, Минск')
axes[1].annotate('Включение: −29 мВ\nмежду соседними записями', xy=(cut,4.187), xytext=(12,4.09), arrowprops={'arrowstyle':'->','color':'#666666'}, fontsize=10)
axes[1].annotate('Свет выключен:\n+30 мВ', xy=(last,4.087), xytext=(92,4.20), arrowprops={'arrowstyle':'->','color':'#666666'}, fontsize=10)
axes[1].set_xlim(-1,122)
axes[1].set_xticks(range(0,121,20))
fig.savefig(BASE / 'comparison.svg')
fig.canvas.draw()
Image.frombuffer('RGBA', fig.canvas.get_width_height(), fig.canvas.buffer_rgba(), 'raw', 'RGBA', 0, 1).convert('RGB').save(BASE / 'comparison.webp', quality=94)
plt.close(fig)

report = f'''# Два часа разряда debug2 — 06.11.2026

[AI]
**Работа:** два этапа по одному часу по просьбе Николая, сначала без света, затем яркость100%/тёплость50%. Владелец подтвердил ровно по часу; минуты в таблице — наблюдаемые границы CSV, не секундомер владельца.
**Контур:** установленная debug2 по слову владельца; та же читалка и накопленный лог. Новый фрагмент добавлен к прежним436строкам без изменений старого префикса. 561строка всего,125новых. Копия22 209байт, SHA256 `{meta['sha256']}`; два чтения источника идентичны. disk6 безопасно извлечён после копии.
**Запуск:** `python3 -s qa_runs/debug2-light-hours-2026-11-06-201434/analyze.py`; разбор реального CSV, контроль исходного хеша, выделение состояний и построение графика. Время снятия: {meta['captured_at']}.

| Режим | Записи, Минск | Заряд по датчику | Напряжение по датчику |
|---|---|---|---|
| Свет выключен | {stamp(off_rows[0])}–{stamp(off_rows[-1])} |100→96%|4,311→4,216 В|
| Свет100%, тёплость50% | {stamp(on_rows[0])}–{stamp(on_rows[-1])} |95→87%|4,187→4,057 В|
| Выключение света в конце |{stamp(rows[end])}|87%|4,087 В|

**Проверки:** по60записей каждого состояния, интервалы60–61с; внутри двухчасового окна нет сна, перезагрузок или charging=1. Перед началом был сон18:10:28 и boot18:13:40 — этот сон не входит в часовой замер. От boot до первой записи света прошло60мин05с; от первой записи света до первой записи выключенного света ещё60мин05с. Настройки света100/50 подтверждены во всех60строках второго этапа.

**Граница этапов:** последняя строка без света96%, первая со светом95%; точный заряд в момент нажатия между минутными строками неизвестен. Поэтому результат первого часа ориентировочно4–5процентных пунктов, второго8–9пунктов. Сумма за два этапа13пунктов. Это пограничная неопределённость выборки, не статистический доверительный интервал.

**Интерпретация:** расход по индикатору со светом выше. Первые18минут первого этапа датчик держит100%, хотя напряжение меняется: целые проценты и состояние сразу после зарядки ограничивают точность сравнения. Линейная аппроксимация всех точек даёт5,12 и8,63п.п./ч, но она не измеряет ток и не делает индикатор линейным. Не объявлять точный множитель расхода, ток в мА, ёмкость или продолжительность работы до нуля. Разность между соседними строками при включении света−29мВ, при выключении+30мВ; это наблюдаемая реакция показания на смену нагрузки, а не самостоятельный амперметр. После отключения кабеля напряжение в начале теста ещё выше4,3В; проверка допустимого предела конкретной АКБ и точности датчика остаётся открытой.

**Гипотеза Николая о логе:** «словно 5% заряда без подсветки съело» и подозрение на запись на флешку. По BatteryLog.cpp каждая минутная запись читает датчик, открывает CSV на SD, дописывает строку и закрывает файл. Во время первого часа таких записей60, второго60; нет контрольного этапа без логирования. Наблюдаемые4–5пунктов включают всё потребление бодрствующей читалки с диагностикой. Доля SD и диагностики НЕ установлена; все5пунктов им не приписывать.

**Предложение владельца:** «можно сделать логирование, например, раз в 20 минут». Это уменьшит периодические записи с60до3вчас. События boot/sleep/charge можно сохранить отдельно. Изменение НЕ реализовано и экономия НЕ измерена; часовой лог станет реже. Чистый контроль влияния диагностики: та же исходная сборка с единственным различием в логировании, сравнимый диапазон заряда/настройки/радио/бодрствование. Точно отделить физический ток потребления по нынешнему CSV нельзя. Не уменьшать надёжность записей откладыванием сброса буфера: обсуждается частота наблюдений, не сохранность уже записанного.

**Находки:** дефект логирования этим прогоном не установлен. Гипотеза о большом расходе логирования остаётся непроверенной.
**Следы:** battery_log.csv, acquisition.json, analysis.json, comparison.svg, comparison.webp, analyze.py рядом с отчётом; разведка researches/2026-11-06_debug2_light_hour_comparison.md.
**Вердикт:** данные обоих часовых этапов получены и разобраны; готовы к обсуждению. Прошивка и её настройки агентом не менялись.
[/AI]
'''
(BASE / 'report.md').write_text(report)
(BASE / 'comparison.html').write_text('''<!doctype html><html lang="ru"><meta charset="utf-8"><title>Читалка · два часа разряда</title><style>body{margin:24px auto;max-width:1140px;font:17px system-ui;color:#24374b;padding:0 16px}img{width:100%}p{line-height:1.5}a{color:#2474b5}</style><img src="comparison.svg" alt="График заряда и напряжения за два часа"><p>Минутные записи: без света около 4–5 процентных пунктов за час, со светом 100% и тёплостью 50% — около 8–9. Между этапами показание меняется с 96% до 95%; точная граница не записана. Доля потребления самой диагностики этим прогоном не выделена.</p><p><a href="report.md">Полный разбор</a> · <a href="battery_log.csv">Исходный лог</a></p></html>''')
print(json.dumps({'off_samples':len(off_rows),'on_samples':len(on_rows),'phase_seconds':result['phase_marker_elapsed_seconds'],'boundary_soc':result['boundary_soc_before_after'],'total_drop_pp':result['total_soc_drop_pp'],'report':str(BASE/'report.md'),'chart':str(BASE/'comparison.webp')},ensure_ascii=False))
