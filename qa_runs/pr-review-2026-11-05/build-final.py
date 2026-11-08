from pathlib import Path
import subprocess, concurrent.futures
ROOT = Path('/Users/kryvusha/Xteink/pr-fixes')
LOGS = Path('/Users/kryvusha/Xteink/qa_runs/pr-review-2026-11-05')
PIO = '/Users/kryvusha/.platformio/penv/bin/pio'
JOBS = [('epub', ['default', 'x4pro']), ('about', ['default', 'x4pro']), ('sleep', ['default', 'x4pro'])]
def build(job):
    name, targets = job
    for target in targets:
        log = LOGS / (name + '-firmware-' + target + '.log')
        with log.open('w') as out:
            run = subprocess.run([PIO, 'run', '-e', target, '-j', '6'], cwd=ROOT / name, stdout=out, stderr=subprocess.STDOUT)
        print(name, target, 'exit', run.returncode, flush=True)
        print('\n'.join(log.read_text(errors='replace').splitlines()[-7:]), flush=True)
        if run.returncode:
            return False
    return True
if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        results = list(pool.map(build, JOBS))
    print('ALL_FIRMWARE_GREEN', all(results), flush=True)
    raise SystemExit(0 if all(results) else 1)
