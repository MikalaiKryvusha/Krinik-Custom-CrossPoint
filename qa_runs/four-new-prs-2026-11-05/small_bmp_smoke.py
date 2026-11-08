from pathlib import Path
import json
import os
import struct
import subprocess
from PIL import Image

BASE = Path('/Users/kryvusha/Xteink/qa_runs/four-new-prs-2026-11-05')
PROGRAM = '/Users/kryvusha/Xteink/pr-fixes/calibration/.pio/build/simulator_x4_pro/program'
width = height = 100
row = (width * 3 + 3) // 4 * 4
# A deterministic renderer test fixture, not a photograph or a mock screenshot.
bmp = (b'BM' + struct.pack('<IHHI', 54 + row * height, 0, 0, 54) +
       struct.pack('<IiiHHIIiiII', 40, width, height, 1, 24, 0, row * height, 2835, 2835, 0, 0) +
       bytes(row * height))
results = []
for enabled in (0, 1):
    run = BASE / f'cal-small-bmp-fixed-{enabled}'
    (run / 'sd/.crosspoint').mkdir(parents=True)
    (run / 'shots').mkdir()
    (run / 'sd/test.bmp').write_bytes(bmp)
    settings = {'language': 'EN', 'panelCalPictures': enabled, 'sleepTimeoutMinutes': 30}
    state = {'openEpubPath': '/test.bmp', 'lastSleepFromReader': True,
             'readerActivityLoadCount': 0, 'showBootScreen': True}
    (run / 'sd/.crosspoint/settings.json').write_text(json.dumps(settings))
    (run / 'sd/.crosspoint/state.json').write_text(json.dumps(state))
    script = '2500:QUIT'
    (run / 'scenario.json').write_text(json.dumps({'settings': settings, 'state': state, 'script': script}, indent=2))
    env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_RENDER_DRIVER='software',
               CROSSPOINT_SIM_SD=str(run / 'sd'), CROSSPOINT_SIM_INPUT_SCRIPT=script,
               CROSSPOINT_SIM_SCREENSHOTS=f'2000:{run}/shots/image.bmp', CROSSPOINT_SIM_HTTP_PORT='18194')
    with (run / 'run.log').open('w') as stream:
        proc = subprocess.run([PROGRAM], env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=10)
    assert proc.returncode == 0
    path = run / 'shots/image.bmp'
    with Image.open(path) as image:
        image.save(path.with_suffix('.webp'), 'WEBP', lossless=True)
        region = image.convert('L').crop((0, 64, image.width, image.height - 100))
        box = region.point(lambda x: 255 if x < 128 else 0).getbbox()
        bbox = [box[0], box[1] + 64, box[2], box[3] + 64] if box else None
    path.unlink()
    results.append({'calibration': bool(enabled), 'bbox': bbox})
assert results[0]['bbox'] == results[1]['bbox'] == [190, 350, 290, 450], results
(BASE / 'cal-small-bmp-results.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results))
