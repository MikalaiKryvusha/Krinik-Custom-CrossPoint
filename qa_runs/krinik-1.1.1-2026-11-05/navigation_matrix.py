from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess

from PIL import Image

ROOT = Path('/Users/kryvusha/Xteink')
RUN = ROOT / 'qa_runs/krinik-1.1.1-2026-11-05'
WORK = ROOT / 'pr-fixes/krinik'
PROGRAM = WORK / '.pio/build/simulator_x4_pro/program'
BASE_SETTINGS = json.loads((ROOT / 'qa_runs/card-final-2026-11-05/before/.crosspoint/settings.json').read_text())
CARDS = {
    'pictures': ROOT / 'qa_runs/cal_back3/sd/.crosspoint/calibration/pictures_landscape_v2.bmp',
    'books': ROOT / 'qa_runs/cal_books2/sd/.crosspoint/calibration/books_card_v1.epub',
}
SCRIPT = ';'.join(f'{t}:SWIPE:0.02,0.6,0.6,0.6,120' for t in [2000, 3000, 4000, 5000]) + ';6000:QUIT'
SHOTS = [(1800, 'card'), (2700, 'calibration'), (3700, 'display'), (4700, 'settings'), (5700, 'home')]
SHOTS += [(t, f'transition-{t}') for t in range(2050, 2501, 10)]

def pixel_hash(image):
    # The clock is independent of navigation; exclude its band, retain titles and all rows.
    return hashlib.sha256(image.crop((0, 40, image.width, image.height)).tobytes()).hexdigest()

results = []
for kind, fixture in CARDS.items():
    for orientation in range(4):
        case = RUN / f'navigation-{kind}-{orientation}'
        if not case.exists():
            (case / 'shots').mkdir(parents=True)
            sd = case / 'sd'
            (sd / '.crosspoint/calibration').mkdir(parents=True)
            settings = dict(BASE_SETTINGS, orientation=orientation, sleepTimeoutMinutes=30)
            (sd / '.crosspoint/settings.json').write_text(json.dumps(settings, ensure_ascii=False))
            path = '/.crosspoint/calibration/' + fixture.name
            shutil.copyfile(fixture, sd / path.lstrip('/'))
            (sd / '.crosspoint/state.json').write_text(json.dumps({
                'openEpubPath': path, 'lastSleepFromReader': True,
                'readerActivityLoadCount': 0, 'showBootScreen': True,
            }))
            env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_RENDER_DRIVER='software',
                       CROSSPOINT_SIM_SD=str(sd), CROSSPOINT_SIM_INPUT_SCRIPT=SCRIPT,
                       CROSSPOINT_SIM_SCREENSHOTS=';'.join(f'{t}:{case / "shots" / (name + ".bmp")}' for t, name in SHOTS),
                       CROSSPOINT_SIM_HTTP_PORT='18191')
            (case / 'scenario.json').write_text(json.dumps({
                'script': SCRIPT, 'shots': SHOTS, 'orientation': orientation,
                'card': path, 'headless': True,
            }, indent=2))
            with (case / 'run.log').open('w') as stream:
                proc = subprocess.run([str(PROGRAM)], cwd=WORK, env=env,
                                      stdout=stream, stderr=subprocess.STDOUT, timeout=20)
            assert proc.returncode == 0, (kind, orientation, proc.returncode)
        for bmp in (case / 'shots').glob('*.bmp'):
            with Image.open(bmp) as image:
                image.save(bmp.with_suffix('.webp'), 'WEBP', lossless=True)
            bmp.unlink()
        hashes = {}
        sizes = {}
        for _, name in SHOTS:
            with Image.open(case / 'shots' / (name + '.webp')) as image:
                hashes[name] = pixel_hash(image)
                sizes[name] = image.size
        transition = {hashes[name] for _, name in SHOTS if name.startswith('transition-')}
        assert transition <= {hashes['card'], hashes['calibration']}, (kind, orientation, 'intermediate frame')
        assert hashes['card'] != hashes['calibration']
        assert hashes['calibration'] != hashes['display'] != hashes['settings']
        # Settings are portrait: ReaderActivity::onExit and the image viewer restore UI orientation.
        assert sizes['calibration'] == (480, 800)
        log = (case / 'run.log').read_text(errors='replace')
        assert '[ERR]' not in log and 'Segmentation' not in log and 'panic' not in log.lower()
        lines = log.splitlines()
        first_settings = next(i for i, line in enumerate(lines) if 'Entering activity: SettingsList' in line)
        first_draw = next(i for i in range(first_settings + 1, len(lines)) if 'displayBuffer' in lines[i])
        assert sum('Entering activity: Settings' in s for s in lines[first_settings:first_draw]) == 3
        assert 'Entering activity: Home' in log
        result = {'card': kind, 'orientation': orientation, 'screenshots': len(SHOTS),
                  'return_content_states': len(transition), 'no_intermediate_frames': True,
                  'return_size': sizes['calibration'], 'headless': True,
                  'route_before_first_draw': lines[first_settings:first_draw + 1]}
        (case / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
        results.append(result)
        (RUN / 'navigation-results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
        print(kind, orientation, 'PASS: card → calibration → display → settings → home; no intermediate return frames', flush=True)
assert len(results) == 8
print('ALL_8_NAVIGATION_CASES_GREEN', flush=True)
