from pathlib import Path
import hashlib, json, os, plistlib, subprocess
root=Path('/Users/kryvusha/Xteink')
run=root/'qa_runs/debug4-2026-11-06'
fw=root/'firmware'
version='cp-2.0.0-krinik-1.1.1-debug4'
source=fw/'.pio/build/x4pro-krinik-debug/firmware.bin'
data=source.read_bytes()
assert data[0]==0xe9 and version.encode() in data
assert b'cp-2.0.0-krinik-1.1.1-debug3' not in data
assert len(data)<6553600
info=subprocess.run(['/Users/kryvusha/.platformio/penv/bin/python','/Users/kryvusha/.platformio/packages/tool-esptoolpy/esptool.py','image-info',str(source)],capture_output=True,text=True,check=True)
(run/'image-info.txt').write_text(info.stdout+info.stderr)
assert info.stdout.lower().count('(valid)')>=2,info.stdout
image=root/'firmware-builds'/(version+'.bin')
assert not image.exists()
image.write_bytes(data)
sha=hashlib.sha256(data).hexdigest()
(image.parent/(version+'.SHA256SUMS.txt')).write_text(sha+'  '+image.name+'\n')
meta={'version':version,'bytes':len(data),'sha256':sha,'build_env':'x4pro-krinik-debug','battery_log_interval_seconds':1200,'charge_events_min_seconds':10,'hardware_tested':False,'installed':False}
(run/'image.json').write_text(json.dumps(meta,indent=2)+'\n')
card=Path('/Volumes/X4-KRINIK')
volume=plistlib.loads(subprocess.check_output(['diskutil','info','-plist',str(card)]))
assert volume['MountPoint']==str(card) and volume['VolumeName']=='X4-KRINIK'
destination=card/'.firmware'/image.name
assert destination.parent.is_dir() and not destination.exists()
with destination.open('wb') as out:
 out.write(data);out.flush();os.fsync(out.fileno())
for dotfile in destination.parent.glob('._*'):
 if dotfile.is_file():dotfile.unlink()
subprocess.run(['sync'],check=True)
assert hashlib.sha256(destination.read_bytes()).hexdigest()==sha
meta.update({'image':str(image),'destination':str(destination),'copied':True,'readback_verified':True,'ejected':False})
(run/'card-delivery.json').write_text(json.dumps(meta,indent=2)+'\n')
ejected=subprocess.run(['diskutil','eject',volume['ParentWholeDisk']],capture_output=True,text=True)
(run/'eject.txt').write_text(ejected.stdout+ejected.stderr)
ejected.check_returncode()
meta['ejected']=True
(run/'card-delivery.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta,ensure_ascii=False))

from datetime import datetime
from zoneinfo import ZoneInfo
stamp=datetime.now(ZoneInfo('Europe/Minsk')).strftime('%Y-%m-%d %H:%M %z')
status=root/'STATUS.md'
s=status.read_text()
a=s.index('## FIRST: debug4');b=s.index('## После debug4:',a)
block=f"""## FIRST: debug4 доставлена на SD — проверить установку
**{stamp}: debug4 собрана и скопирована на карту**, {len(data)} байт, SHA256 `{sha}`. Образ `{image.relative_to(root)}`. Сборка x4pro-krinik-debug SUCCESS, ESP image checksum/hash valid, версия debug4 найдена в образе; чтение с карты сверено, AppleDouble в /.firmware удалён, карта безопасно извлечена. **Установка на устройство НЕ подтверждена**: Николай выбирает debug4 в меню обновления с SD. Последняя подтверждённая установленная версия остаётся debug2.

Периодический `tick` теперь раз в20минут от последней успешной записи. Отдельные события boot/sleep/charge сохранены; charge может записываться чаще, с прежним ограничением10секунд, и сбрасывает отсчёт. Изменены только BatteryLog.cpp, комментарии BatteryLog.h и версия в platformio.ini; прежние firmware/SDK debug3-правки сохранены. Host-проверки границы20минут, отсутствияминутныхтиков, charge и переполнения millis PASS; четыре независимых read-only ревью без замечаний. Аппаратные20минут ещё не измерены.

Доказательства: `qa_runs/debug4-2026-11-06/` — build.log, candidate.diff, image.json, card-delivery.json, review.md, before/. Коммит/push не выполнялись: корень Xteink не Git-репозиторий; сохранённые firmware/SDK изменения не коммитились.

**Дальше:** подтвердить установку debug4; далее продолжить MIC/PowerService ниже, не пересобирать без новой причины.

"""
s=s[:a]+block+s[b:]
s=s.replace('«Лог раз в20мин» — предложение, НЕреализовано. Debug3пишетразв60с.','«Лог раз в20мин» реализован в debug4, доставленной на SD; установка не подтверждена. Историческая Debug3пишетразв60с.')
s+=f'\n[AI] ⚠️ Форс-закрытие {stamp} по прямому поручению Николая сразу после доставки debug4. Передача сохранена; тяжёлые ритуалы закрытия и общий аудит отложены до следующего спокойного /end-chat-soft. QA-репозиторий не менялся. Неисправленных ложных утверждений: нет. [/AI]\n'
status.write_text(s)
readme=root/'README.md';s=readme.read_text()
s=s.replace('На карте в `/.firmware/` три образа: debug3, krinik1.1.2 и официальная CrossPoint2.0.0; debug3 скопирована и сверена чтением06.11.2026, карта безопасно извлечена.','На карте в `/.firmware/` четыре образа: debug4, debug3, krinik1.1.2 и официальная CrossPoint2.0.0; debug4 скопирована и сверена чтением06.11.2026, карта безопасно извлечена.')
s=s.replace('Заказана debug4 с интервалом20минут, ещё не собрана.','Debug4 с периодическим интервалом20минут собрана и доставлена наSD; отдельные события boot/sleep/charge сохранены, установка не подтверждена. Доказательства — `qa_runs/debug4-2026-11-06/`.')
readme.write_text(s)
with (root/'HANDOVER.md').open('a') as out:out.write('\n[AI] '+stamp+' — debug4 собрана, скопирована в /.firmware SD, SHA256 и чтение сверены, карта безопасно извлечена. Установка НЕ подтверждена. Интервал tick20минут; boot/sleep/charge сохранены. FIRST читать STATUS.md; далее MIC/PowerService. Форс-закрытие по прямому поручению владельца; тяжёлые ритуалы отложены. [/AI]\n')
print('STATUS and handover saved; force-close now')
