"""Add debug2 to the owner's mounted reader, preserving existing card contents."""
from pathlib import Path
import hashlib,json,os,plistlib,subprocess

BASE=Path('/Users/kryvusha/Xteink')
RUN=BASE/'qa_runs/frontlight-colour-fix-2026-11-06'
CARD=Path('/Volumes/X4-KRINIK')
NAME='cp-2.0.0-krinik-1.1.1-debug2.bin'
EXPECTED='0076ec028760615fcbdda93537576655b1a0aceafa00c0603b8befe68f6e277d'
info=plistlib.loads(subprocess.check_output(['diskutil','info','-plist',str(CARD)]))
assert info.get('VolumeUUID')=='649C18D8-130F-3C63-AD1A-F6396E1014A6',info.get('VolumeUUID')
assert info.get('FilesystemType')=='msdos' and info.get('MountPoint')==str(CARD)
assert info.get('BusProtocol')=='USB' and info.get('Writable') is True
FW=CARD/'.firmware'
assert FW.is_dir() and (CARD/'.crosspoint').is_dir()
source=BASE/'firmware-builds'/NAME
data=source.read_bytes()
assert hashlib.sha256(data).hexdigest()==EXPECTED
assert b'cp-2.0.0-krinik-1.1.1-debug2\0' in data
assert not (FW/NAME).exists(), 'Inspect existing target before replacing'

def owner_files():
    result={}
    for parent, dirs, files in os.walk(CARD):
        dirs[:]=[d for d in dirs if d not in {'.Spotlight-V100','.fseventsd','.Trashes'}]
        for name in files:
            if name.startswith('._'): continue
            path=Path(parent)/name
            result[str(path.relative_to(CARD))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return result
before=owner_files()
(RUN/'card-before-hashes.json').write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n')
backup=RUN/'card-state-before'
assert not backup.exists(), 'Inspect prior card run before repeating'
backup.mkdir()
for rel in before:
    p=Path(rel)
    if p.parts[0]=='.crosspoint' and (p.suffix=='.json' or p.name in {'progress.bin','panel_curve.txt','panel_curve_book.txt','library.idx','battery_log.csv'}):
        dest=backup/p
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes((CARD/p).read_bytes())
        assert hashlib.sha256(dest.read_bytes()).hexdigest()==before[rel]
temp=FW/(NAME+'.install-tmp')
assert not temp.exists()
with temp.open('xb') as f:
    f.write(data)
    f.flush()
    os.fsync(f.fileno())
assert hashlib.sha256(temp.read_bytes()).hexdigest()==EXPECTED
os.replace(temp,FW/NAME)
assert hashlib.sha256((FW/NAME).read_bytes()).hexdigest()==EXPECTED
subprocess.run(['sh',str(BASE/'tools/card_clean.sh'),str(CARD)],check=True)
after=owner_files()
assert all(after.get(rel)==sha for rel,sha in before.items()), 'Existing owner data changed'
assert set(after)-set(before)=={'.firmware/'+NAME}
result={'card':str(CARD),'uuid':info['VolumeUUID'],'device':info['DeviceIdentifier'],'new_firmware':NAME,'sha256':EXPECTED,'existing_files_unchanged':len(before),'battery_log_backup':str(backup/'.crosspoint/battery_log.csv'),'flashed':False,'ejected':False}
(RUN/'card-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
