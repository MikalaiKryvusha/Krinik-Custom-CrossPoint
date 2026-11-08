#!/usr/bin/env node
// Настроить читалку CrossPoint как сохранено в этой папке.
// node restore.mjs [IP] [--dry-run] [--settings-only]
// Читалка должна быть в File Transfer → Join a Network (или Hotspot, IP 192.168.4.1).
import fs from 'node:fs';
import path from 'node:path';

const here = path.dirname(new URL(import.meta.url).pathname);
const args = process.argv.slice(2);
const dry = args.includes('--dry-run');
const settingsOnly = args.includes('--settings-only');
const ip = args.find(a => !a.startsWith('--')) || '192.168.1.7';
const base = `http://${ip}`;

const getJson = async p => { const r = await fetch(base + p); if (!r.ok) throw new Error(`${p}: HTTP ${r.status}`); return r.json(); };
const post = async (p, init) => {
  if (dry) { console.log('  [dry-run] POST', p); return { ok: true }; }
  const r = await fetch(base + p, { method: 'POST', ...init });
  const text = await r.text();
  if (!r.ok) throw new Error(`${p}: HTTP ${r.status} ${text}`);
  return text;
};
const fileBlob = p => new Blob([fs.readFileSync(p)]);

const status = await getJson('/api/status');
console.log(`Читалка: ${status.device}, прошивка ${status.firmwareFamily} ${status.version}, IP ${status.ip}`);

if (!settingsOnly) {
  // Шрифты: на карте только семейства из fonts/, остальные удаляются.
  const wanted = fs.readdirSync(path.join(here, 'fonts'), { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name);
  const have = (await getJson('/api/fonts')).families;
  for (const f of have.filter(f => !wanted.includes(f.name))) {
    console.log('Удаляю шрифт', f.name);
    await post('/api/fonts/delete', { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ family: f.name }) });
  }
  for (const fam of wanted) {
    const present = new Set((have.find(f => f.name === fam)?.files || []).map(x => x.name));
    for (const file of fs.readdirSync(path.join(here, 'fonts', fam)).filter(n => /\.(ttf|otf|cpfont)$/i.test(n))) {
      if (present.has(file)) continue;
      console.log('Загружаю шрифт', file);
      const fd = new FormData();
      fd.append('family', fam);
      fd.append('file', fileBlob(path.join(here, 'fonts', fam, file)), file);
      await post('/api/fonts/upload', { body: fd });
    }
  }
  // Руководство в корень.
  const root = await getJson('/api/files?path=' + encodeURIComponent('/'));
  const guide = 'РУКОВОДСТВО.epub';
  if (!root.some(f => f.name === guide)) {
    console.log('Загружаю', guide);
    const fd = new FormData();
    fd.append('file', fileBlob(path.join(here, guide)), guide);
    await post('/upload?path=' + encodeURIComponent('/'), { body: fd });
  }
}

// Настройки: enum сопоставляется по названию варианта, а не по номеру —
// номер шрифта зависит от того, какие шрифты стоят.
const saved = JSON.parse(fs.readFileSync(path.join(here, 'settings.json'), 'utf8'));
const current = new Map((await getJson('/api/settings')).map(s => [s.key, s]));
const changes = {};
for (const s of saved) {
  const c = current.get(s.key);
  if (!c) { console.log('  нет на этой прошивке:', s.key); continue; }
  if (s.type === 'string' && s.value === null) continue; // скрытые пароли не сохраняются
  let v = s.value;
  if (s.type === 'enum') {
    const label = s.options[s.value];
    v = c.options.indexOf(label);
    if (v < 0) { console.log(`  ${s.name}: варианта «${label}» нет, пропускаю`); continue; }
  }
  if (c.value !== v) changes[s.key] = v;
}
console.log(`Настроек к изменению: ${Object.keys(changes).length}`, Object.keys(changes).join(', '));
if (Object.keys(changes).length) console.log(' ', await post('/api/settings', { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(changes) }));
console.log('Готово. Wi-Fi: добавь сеть <your Wi-Fi network> с паролем вручную (Settings → Connectivity → Wi-Fi).');
