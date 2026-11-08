from pathlib import Path
import hashlib, json, os, plistlib, subprocess
root=Path('/Users/kryvusha/Xteink')
run=root/'qa_runs/debug5-sleep-menu-2026-11-06'
fw=root/'firmware'
version='cp-2.0.0-krinik-1.1.1-debug5'
source=fw/'.pio/build/x4pro-krinik-debug/firmware.bin'
data=source.read_bytes()
assert data[0]==0xe9 and version.encode() in data
assert b'cp-2.0.0-krinik-1.1.1-debug4' not in data
assert len(data)<6553600
info=subprocess.run(['/Users/kryvusha/.platformio/penv/bin/python','/Users/kryvusha/.platformio/packages/tool-esptoolpy/esptool.py','image-info',str(source)],capture_output=True,text=True,check=True)
(run/'image-info.txt').write_text(info.stdout+info.stderr)
assert info.stdout.lower().count('(valid)')>=2,info.stdout
image=root/'firmware-builds'/(version+'.bin')
assert not image.exists()
image.write_bytes(data)
sha=hashlib.sha256(data).hexdigest()
(image.parent/(version+'.SHA256SUMS.txt')).write_text(sha+'  '+image.name+'\n')
meta={'version':version,'bytes':len(data),'sha256':sha,'build_env':'x4pro-krinik-debug','battery_log_interval_seconds':1200,'charge_events_min_seconds':10,'feature':'home menu item Сон under Фонарик','hardware_tested':False,'installed':False}
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

