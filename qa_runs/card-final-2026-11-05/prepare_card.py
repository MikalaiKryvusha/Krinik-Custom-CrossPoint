"""One recorded card repair; fail before eject if any invariant does not hold."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import struct
import unicodedata
import zipfile

ROOT = Path('/Users/kryvusha/Xteink')
CARD = Path('/Volumes/X4-KRINIK')
RUN = ROOT / 'qa_runs/card-final-2026-11-05'
BACKUP = RUN / 'before'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fnv(path):
    value = 14695981039346656037
    for byte in path.encode():
        value = ((value ^ byte) * 1099511628211) & ((1 << 64) - 1)
    return value

def identity(path):
    return unicodedata.normalize('NFC', path).casefold()

def install(data, target):
    temp = target.with_name(target.name + '.repair-tmp')
    assert not temp.exists(), temp
    with temp.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == data
    os.replace(temp, target)
    assert target.read_bytes() == data

firmware = ROOT / 'firmware-builds/cp-2.0.0-krinik-1.1.0.bin'
guide = ROOT / 'РУКОВОДСТВО.epub'
expected_fw = 'c351f56e9ee3ebe18d1c01c69d451848b08bab615f2a37bb53a3a84af3520dd5'
expected_guide = '03c69a1fc2c9ebcb20e1a8b99eca2969c3c51ccf162dcd253ba75834360fe122'
assert sha(firmware) == expected_fw
assert sha(guide) == expected_guide
assert firmware.read_bytes()[0] == 0xE9
with zipfile.ZipFile(guide) as archive:
    assert archive.testzip() is None

recent_path = CARD / '.crosspoint/recent.json'
index_path = CARD / '.crosspoint/library.idx'
recent = json.loads(recent_path.read_bytes())
index_before = index_path.read_bytes()
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

protected = [CARD / 'panel_curve.txt', CARD / 'panel_curve_book.txt', CARD / '.crosspoint/state.json']
protected += [p for p in (CARD / 'Книги').rglob('*') if p.is_file()]
protected += list((CARD / '.crosspoint').rglob('progress.bin'))
protected += [p for p in (CARD / '.crosspoint/bookmarks').rglob('*') if p.is_file()]
protected_hashes = {str(p.relative_to(CARD)): sha(p) for p in protected}
assert not BACKUP.exists(), 'Already ran: inspect the saved result before repeating'
BACKUP.mkdir()
for relative in ['.crosspoint/recent.json', '.crosspoint/library.idx', '.crosspoint/state.json',
                 '.crosspoint/settings.json', 'РУКОВОДСТВО.epub', 'КАЛИБРОВКА.epub',
                 'panel_curve.txt', 'panel_curve_book.txt']:
    source = CARD / relative
    destination = BACKUP / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    assert sha(source) == sha(destination)
(RUN / 'protected-hashes.json').write_text(json.dumps(protected_hashes, ensure_ascii=False, indent=2))

changed_rows = []
for row in range(count):
    offset = record_start + row * 128
    record = struct.unpack_from('<IIHH4B96s12sI', index, offset)
    name_offset, old_size, first_seen, folder, length = record[:5]
    blob = name_start + name_offset
    name = index[blob+8:blob+8+length].decode()
    if name not in ('Калибровка.epub', 'РУКОВОДСТВО.epub'):
        continue
    new_name = 'КАЛИБРОВКА.epub' if name == 'Калибровка.epub' else name
    assert len(new_name.encode()) == length
    path = folders[folder].rstrip('/') + '/' + new_name
    assert (CARD / path.lstrip('/')).is_file()
    new_size = guide.stat().st_size if new_name == 'РУКОВОДСТВО.epub' else (CARD / new_name).stat().st_size
    struct.pack_into('<Q', index, blob, fnv(path))
    index[blob+8:blob+8+length] = new_name.encode()
    # Same folded title/sort order; update the existing equal-length title blob.
    title_pos = blob + 8 + length
    title_pos += 1 + index[title_pos]
    title_length = index[title_pos]
    title = new_name.removesuffix('.epub').encode()
    assert title_length == len(title)
    index[title_pos+1:title_pos+1+title_length] = title
    struct.pack_into('<I', index, offset+4, new_size)
    struct.pack_into('<I', index, offset+124, 0)
    changed_rows.append({'row': row, 'old_path': name, 'path': path, 'old_size': old_size, 'size': new_size})
assert len(changed_rows) == 2
assert index[:record_start] == index_before[:record_start]
assert index[perm_start:name_start] == index_before[perm_start:name_start]
for row in range(count):
    if row not in [r['row'] for r in changed_rows]:
        start = record_start + row * 128
        assert index[start:start+128] == index_before[start:start+128]

books = []
seen = set()
for entry in recent['books']:
    if identity(entry['path']) == identity('/КАЛИБРОВКА.epub'):
        entry.update(path='/КАЛИБРОВКА.epub', title='КАЛИБРОВКА', coverBmpPath='')
    elif entry['path'] == '/РУКОВОДСТВО.epub':
        entry['coverBmpPath'] = ''
    key = identity(entry['path'])
    assert (CARD / entry['path'].lstrip('/')).is_file(), entry['path']
    if key not in seen:
        books.append(entry)
        seen.add(key)
assert len(recent['books']) == 7 and len(books) == 6
recent['books'] = books

# All preparations and backups succeeded. Perform the small replacements.
install(guide.read_bytes(), CARD / 'РУКОВОДСТВО.epub')
install(index, index_path)
install(json.dumps(recent, ensure_ascii=False, separators=(',', ':')).encode(), recent_path)
target_fw = CARD / '.firmware' / firmware.name
assert not target_fw.exists(), 'Do not overwrite an uninspected firmware image'
install(firmware.read_bytes(), target_fw)
assert sha(target_fw) == expected_fw
assert sha(CARD / 'РУКОВОДСТВО.epub') == expected_guide

# Verify persisted identities independently against actual files and recent paths.
persisted = index_path.read_bytes()
paths = []
for row in range(count):
    name_offset, file_size, _, folder, length = struct.unpack_from('<IIHHB', persisted, record_start + row * 128)
    pos = name_start + name_offset
    stored_hash = struct.unpack_from('<Q', persisted, pos)[0]
    name = persisted[pos+8:pos+8+length].decode()
    path = folders[folder].rstrip('/') + '/' + name
    actual = CARD / path.lstrip('/')
    assert actual.is_file() and actual.stat().st_size == file_size, path
    assert stored_hash == fnv(path), path
    paths.append(path)
assert len(set(map(identity, paths))) == 6
assert set(map(identity, paths)) == set(map(lambda b: identity(b['path']), books))
assert all(sha(CARD / name) == digest for name, digest in protected_hashes.items())
result = {'firmware_sha256': expected_fw, 'guide_sha256': expected_guide, 'index_updates': changed_rows,
          'recent_before': 7, 'recent_after': 6, 'index_records': 6,
          'protected_files_verified': len(protected_hashes), 'backup': str(BACKUP),
          'physical_flash': 'pending owner action', 'visual_ghost_check': 'pending owner observation'}
(RUN / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps(result, ensure_ascii=False, indent=2))
