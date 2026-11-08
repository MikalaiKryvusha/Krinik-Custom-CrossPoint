"""Keep exactly the two firmware images explicitly requested by Nikolai."""
from pathlib import Path
import hashlib,json,os,plistlib,subprocess

BASE=Path('/Users/kryvusha/Xteink')
RUN=Path(__file__).resolve().parent
CARD=Path('/Volumes/X4-KRINIK')
FW=CARD/'.firmware'
EXPECTED={'cp-2.0.0-krinik-1.1.2.bin':'3e0cc45bbb3dec91052070edce51e5c5c3bda5ffe03440e6ea2ea05b26216d6a','crosspoint-2.0.0-x4pro.bin':'eec8b22b96202da31c91ec73f4af3fa9e3149658c3cf38dab7aa2b810ff34b44'}
info=plistlib.loads(subprocess.check_output(['diskutil','info','-plist',str(CARD)]))
assert info.get('VolumeUUID')=='649C18D8-130F-3C63-AD1A-F6396E1014A6'
assert info.get('BusProtocol')=='USB' and info.get('Writable') is True
assert FW.is_dir() and (CARD/'.crosspoint').is_dir()
backup=RUN/'card-before';assert not backup.exists(), 'Inspect prior run before repeating';backup.mkdir()
sources={}
for name,sha in EXPECTED.items():
 data=(BASE/'firmware-builds'/name).read_bytes();assert hashlib.sha256(data).hexdigest()==sha
 sources[name]=data
before={};firmware_before=[]
for parent,dirs,files in os.walk(CARD):
 dirs[:]=[d for d in dirs if d not in {'.Spotlight-V100','.fseventsd','.Trashes'}]
 for name in files:
  if name.startswith('._'): continue
  p=Path(parent)/name;rel=p.relative_to(CARD);data=p.read_bytes();digest=hashlib.sha256(data).hexdigest()
  before[str(rel)]=digest
  if rel.parts[0]=='.firmware': firmware_before.append(p.name)
  if rel.parts[0]=='.firmware' or rel.parts[0]=='.crosspoint' and (p.suffix=='.json' or p.name in {'progress.bin','library.idx','battery_log.csv','panel_curve.txt','panel_curve_book.txt'}):
   target=backup/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
   assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
(RUN/'before-hashes.json').write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n')
print(f'Backup verified: {len(firmware_before)} old firmware files; owner-file hashes: {len(before)}',flush=True)
for name,data in sources.items():
 target=FW/name
 if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==EXPECTED[name]: continue
 temp=target.with_name(name+'.install-tmp');assert not temp.exists()
 with temp.open('xb') as stream: stream.write(data);stream.flush();os.fsync(stream.fileno())
 assert hashlib.sha256(temp.read_bytes()).hexdigest()==EXPECTED[name]
 os.replace(temp,target)
 assert hashlib.sha256(target.read_bytes()).hexdigest()==EXPECTED[name]
print('Both requested images verified on card; removing backed-up superseded images.',flush=True)
removed=[]
for p in FW.iterdir():
 if not p.is_file() or p.name in EXPECTED or p.name.startswith('._'): continue
 saved=backup/'.firmware'/p.name
 assert saved.is_file() and hashlib.sha256(saved.read_bytes()).hexdigest()==before[str(p.relative_to(CARD))]
 p.unlink();removed.append(p.name)
subprocess.run(['sh',str(BASE/'tools/card_clean.sh'),str(CARD)],check=True)
remaining={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in FW.iterdir() if p.is_file() and not p.name.startswith('._')}
assert remaining==EXPECTED,remaining
preserved=0
for rel,sha in before.items():
 if Path(rel).parts[0]=='.firmware': continue
 assert hashlib.sha256((CARD/rel).read_bytes()).hexdigest()==sha,rel
 preserved+=1
result={'firmware_images':remaining,'removed_from_card':removed,'backup':str(backup),'protected_owner_files_unchanged':preserved,'battery_log_backup':str(backup/'.crosspoint/battery_log.csv'),'ejected':False,'flashed':False}
(RUN/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False),flush=True)
