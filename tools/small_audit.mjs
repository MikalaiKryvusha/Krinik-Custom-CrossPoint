// Find shrunk elements in an unpacked EPUB: CSS rules with font-size below 0.85,
// where they are used, and the effective size of footnote markers (nested shrink).
import fs from 'node:fs';
import path from 'node:path';

const dir = process.argv[2];
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const files = walk(dir);
const css = files.filter(f => /\.css$/i.test(f)).map(f => fs.readFileSync(f, 'utf8')).join('\n')
  + files.filter(f => /\.x?html?$/i.test(f)).map(f => (fs.readFileSync(f, 'utf8').match(/<style[^>]*>([\s\S]*?)<\/style>/gi) || []).join('\n')).join('\n');

const factor = v => {
  v = v.trim().toLowerCase();
  const named = { 'xx-small': 0.6, 'x-small': 0.75, small: 0.89, smaller: 0.83, medium: 1, large: 1.2, larger: 1.2 };
  if (v in named) return named[v];
  let m = v.match(/^([\d.]+)(em|rem)$/); if (m) return +m[1];
  m = v.match(/^([\d.]+)%$/); if (m) return +m[1] / 100;
  m = v.match(/^([\d.]+)(pt|px)$/); if (m) return +m[1] / (m[2] === 'pt' ? 12 : 16);
  return null;
};
const size = {}; // selector -> factor
for (const m of css.replace(/\/\*[\s\S]*?\*\//g, '').matchAll(/([^{}]+)\{([^}]*)\}/g)) {
  const fsz = m[2].match(/font-size\s*:\s*([^;]+)/i);
  if (!fsz) continue;
  const f = factor(fsz[1]);
  if (f == null) continue;
  for (const sel of m[1].split(',').map(s => s.trim()).filter(Boolean)) size[sel] = f;
}
const small = Object.entries(size).filter(([, f]) => f < 0.85);

const html = files.filter(f => /\.x?html?$/i.test(f)).map(f => fs.readFileSync(f, 'utf8')).join('\n');
const report = [];
for (const [sel, f] of small) {
  let re;
  const cls = sel.match(/^(?:([a-z0-9]+))?\.([\w-]+)$/i);
  if (cls) re = new RegExp(`<${cls[1] || '[a-z0-9]+'}\\b[^>]*class="[^"]*\\b${cls[2]}\\b[^"]*"[^>]*>([^<]{0,30})`, 'gi');
  else if (/^[a-z0-9]+$/i.test(sel)) re = new RegExp(`<${sel}\\b[^>]*>([^<]{0,30})`, 'gi');
  else { report.push(`${sel}: ${f}em (сложный селектор)`); continue; }
  const hits = [...html.matchAll(re)];
  if (!hits.length) continue;
  const sample = [...new Set(hits.map(h => h[1].trim()).filter(Boolean))].slice(0, 3).join(' | ');
  report.push(`${sel}: ${f}em × ${hits.length}   пример: ${sample}`);
}
// Footnote markers: <sup>/<a> with short numeric text, effective size = product of nested shrinks.
const markers = [...html.matchAll(/((?:<(?:sup|span|a|small)\b[^>]*>\s*){1,3})\[?\d{1,4}\*?\]?\s*</gi)];
const eff = {};
for (const m of markers) {
  let f = 1;
  for (const t of m[1].matchAll(/<(\w+)\b([^>]*)>/g)) {
    const tag = t[1].toLowerCase();
    const classes = (t[2].match(/class="([^"]*)"/) || [, ''])[1].split(/\s+/).filter(Boolean);
    let tf = size[tag] ?? (tag === 'sup' || tag === 'small' ? 0.83 : 1); // reader default for sup unknown, browsers ~0.83
    for (const c of classes) tf = size[`.${c}`] ?? size[`${tag}.${c}`] ?? tf;
    f *= tf;
  }
  const key = m[1].replace(/\s+(href|id|title)="[^"]*"/g, '').replace(/\s+/g, ' ').trim();
  eff[key] = eff[key] || { f: +f.toFixed(2), n: 0 };
  eff[key].n++;
}
console.log('Мелкие правила:', report.length ? '\n  ' + report.join('\n  ') : 'нет');
console.log('Номера сносок (итоговый размер от текста):');
for (const [k, v] of Object.entries(eff).sort((a, b) => b[1].n - a[1].n).slice(0, 6)) console.log(`  ${v.f} × ${v.n}  ${k}`);
