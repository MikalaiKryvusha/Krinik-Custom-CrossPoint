"""Install the verified release; preserve reading state and three rollback choices."""
from pathlib import Path
import hashlib
import json
import os
import struct

ROOT = Path('/Users/kryvusha/Xteink')
RUN = ROOT / 'qa_runs/krinik-1.1.1-2026-11-05'
CARD = Path('/Volumes/X4-KRINIK')
BACKUP = RUN / 'card-before'
FW = CARD / '.firmware'
EXPECTED = {
    'cp-2.0.0-krinik-1.1.1.bin': 'a9104bc7b7b7ae2eea252e4d552cce0b936c2e4d414bb5f93a27ccd88bfdee99',
    'cp-2.0.0-krinik-1.0.0.bin': '59f27896ba5066caa69fd975fe5bb221c965da1fa39c8c53217d7c84edbc9b6a',
    'crosspoint-2.0.0-x4pro.bin': 'eec8b22b96202da31c91ec73f4af3fa9e3149658c3cf38dab7aa2b810ff34b44',
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def install(data, path):
    temp = path.with_name(path.name + '.install-tmp')
    assert not temp.exists(), temp
    with temp.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == data
    os.replace(temp, path)
    assert path.read_bytes() == data

assert CARD.is_dir() and FW.is_dir()
assert not BACKUP.exists(), 'Inspect the saved run before repeating'
BACKUP.mkdir()
protected = [p for p in (CARD / '.crosspoint').rglob('*') if p.is_file() and
             (p.suffix == '.json' or p.name in ('progress.bin', 'panel_curve.txt', 'panel_curve_book.txt'))]
protected += [CARD / 'КАЛИБРОВКА.epub']
protected_data = {str(p.relative_to(CARD)): p.read_bytes() for p in protected}
index_path = CARD / '.crosspoint/library.idx'
index_before = index_path.read_bytes()
guide_path = CARD / 'РУКОВОДСТВО.epub'
guide_before = guide_path.read_bytes()
old_images = {p.name: p.read_bytes() for p in FW.iterdir() if p.is_file() and not p.name.startswith('._')}
assert set(old_images) == {'cp-2.0.0-krinik-1.1.0.bin',
                          'crosspoint-2.0.0-krinik-1.1.0-curvereload-x4pro.bin',
                          'crosspoint-2.0.0-krinik-x4pro.bin', 'crosspoint-2.0.0-x4pro.bin'}, old_images.keys()
assert digest(old_images['crosspoint-2.0.0-krinik-x4pro.bin']) == EXPECTED['cp-2.0.0-krinik-1.0.0.bin']
assert digest(old_images['crosspoint-2.0.0-x4pro.bin']) == EXPECTED['crosspoint-2.0.0-x4pro.bin']
backup_data = dict(protected_data)
backup_data.update({'.crosspoint/library.idx': index_before, 'РУКОВОДСТВО.epub': guide_before})
backup_data.update({'.firmware/' + name: data for name, data in old_images.items()})
for relative, data in backup_data.items():
    target = BACKUP / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    assert target.read_bytes() == data
(RUN / 'card-before-hashes.json').write_text(json.dumps({p: digest(d) for p, d in backup_data.items()}, ensure_ascii=False, indent=2))

new_fw = (RUN / 'release-assets/cp-2.0.0-krinik-1.1.1.bin').read_bytes()
assert digest(new_fw) == EXPECTED['cp-2.0.0-krinik-1.1.1.bin']
guide = (RUN / 'RUKOVODSTVO-krinik.epub').read_bytes()
assert digest(guide) == '8a3b93abe43fcc92183c7fc86cc8c694bbc25fab5f0fb5841a64fd44418cd5c3'
index = bytearray(index_before)
h = struct.unpack_from('<4s4B4H7I20s', index)
assert h[:3] == (b'CLX1', 2, 4)
count, folder_count = h[5:7]
folder_start, folder_len, record_start, perm_start, name_start, name_len, size = h[9:16]
assert count == 6 and size == len(index)
folders = []
pos = folder_start
for _ in range(folder_count):
    length = index[pos]
    pos += 1
    folders.append(index[pos:pos+length].decode())
    pos += length
assert pos == folder_start + folder_len
updated = []
for row in range(count):
    offset = record_start + row * 128
    name_offset, old_size, _, folder, length = struct.unpack_from('<IIHHB', index, offset)
    blob = name_start + name_offset
    name = index[blob+8:blob+8+length].decode()
    if name == 'РУКОВОДСТВО.epub':
        assert folder < len(folders) and folders[folder] == '/'
        struct.pack_into('<I', index, offset+4, len(guide))
        struct.pack_into('<I', index, offset+124, 0)
        updated.append(row)
assert len(updated) == 1
assert index[:record_start] == index_before[:record_start]
assert index[perm_start:] == index_before[perm_start:]
for row in range(count):
    if row not in updated:
        offset = record_start + row * 128
        assert index[offset:offset+128] == index_before[offset:offset+128]

# Preparations succeeded. Write new files before removing the superseded images.
install(new_fw, FW / 'cp-2.0.0-krinik-1.1.1.bin')
stable = FW / 'cp-2.0.0-krinik-1.0.0.bin'
assert not stable.exists()
os.rename(FW / 'crosspoint-2.0.0-krinik-x4pro.bin', stable)
install(guide, guide_path)
install(index, index_path)
for name in ('cp-2.0.0-krinik-1.1.0.bin', 'crosspoint-2.0.0-krinik-1.1.0-curvereload-x4pro.bin'):
    assert (BACKUP / '.firmware' / name).read_bytes() == old_images[name]
    (FW / name).unlink()

images = {p.name: digest(p.read_bytes()) for p in FW.iterdir() if p.is_file() and not p.name.startswith('._')}
assert images == EXPECTED, images
assert all((CARD / p).read_bytes() == data for p, data in protected_data.items())
assert guide_path.read_bytes() == guide and index_path.read_bytes() == index
paths = []
for row in range(count):
    off, file_size, _, folder, length = struct.unpack_from('<IIHHB', index, record_start + row * 128)
    blob = name_start + off
    name = index[blob+8:blob+8+length].decode()
    path = folders[folder].rstrip('/') + '/' + name
    assert (CARD / path.lstrip('/')).stat().st_size == file_size, path
    paths.append(path)
assert len(set(paths)) == 6
recent = json.loads((CARD / '.crosspoint/recent.json').read_bytes())
assert len(recent['books']) == len({b['path'] for b in recent['books']})
result = {'firmware_images': images, 'guide_sha256': digest(guide), 'index_records': count,
          'index_row_updated': updated, 'protected_files_verified': len(protected_data),
          'backup': str(BACKUP), 'flashed': False, 'hardware_back_check': 'pending owner'}
(RUN / 'card-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps(result, ensure_ascii=False, indent=2))
