// Upload sleep images to the reader and switch «Экран сна» to «Свой».
// node sleep_upload.mjs <IP> <dir with .bmp> [--pin <file.bmp>]   --pin also puts that one as /sleep.bmp (beats the .sleep folder)
import fs from 'node:fs'; import path from 'node:path';
const args = process.argv.slice(2); const pinI = args.indexOf('--pin'); const pin = pinI >= 0 ? args.splice(pinI, 2)[1] : null;
const [ip, dir] = args; const base = `http://${ip}`;
const list = async p => (await fetch(base + '/api/files?path=' + encodeURIComponent(p) + '&_=' + Date.now())).json();
const up = async (d, name, buf) => { const fd = new FormData(); fd.append('file', new Blob([buf]), name); const r = await fetch(base + '/upload?path=' + encodeURIComponent(d), { method: 'POST', body: fd }); return r.status + ' ' + (await r.text()).slice(0, 60); };
const down = async p => Buffer.from(await (await fetch(base + '/download?path=' + encodeURIComponent(p))).arrayBuffer());
const del = async p => (await fetch(base + '/delete', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: 'paths=' + encodeURIComponent(JSON.stringify([p])) })).status;
const DIR = '/sleep'; // «.sleep» is preferred by the firmware, but the web server refuses dot names (403); «sleep» is the documented fallback
if (!(await list('/')).some(e => e.name === 'sleep')) { const fd = new FormData(); fd.append('name', 'sleep'); fd.append('path', '/'); console.log('mkdir sleep', (await fetch(base + '/mkdir', { method: 'POST', body: fd })).status); }
const have = new Set((await list(DIR)).map(e => e.name));
const put = async (d, name, buf) => { const p = (d === '/' ? '' : d) + '/' + name; if (have.has(name) && d !== '/') console.log('  replace', name, await del(p)); console.log(' ', p, await up(d, name, buf)); const back = await down(p); console.log('    проверка:', back.equals(buf) ? 'файл совпадает' : 'НЕ СОВПАДАЕТ'); };
for (const n of fs.readdirSync(dir).filter(n => /\.bmp$/i.test(n)).sort()) await put(DIR, n, fs.readFileSync(path.join(dir, n)));
if (pin) { if ((await list('/')).some(e => e.name === 'sleep.bmp')) console.log('  old /sleep.bmp', await del('/sleep.bmp')); await put('/', 'sleep.bmp', fs.readFileSync(pin)); }
const s = (await (await fetch(base + '/api/settings')).json()).find(x => x.key === 'sleepScreen');
const want = s.options.indexOf('Свой');
if (s.value !== want) console.log('Экран сна:', s.options[s.value], '→ Свой', (await fetch(base + '/api/settings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ sleepScreen: want }) })).status);
const s2 = (await (await fetch(base + '/api/settings')).json()).find(x => x.key === 'sleepScreen');
console.log('Экран сна сейчас:', s2.options[s2.value]);
