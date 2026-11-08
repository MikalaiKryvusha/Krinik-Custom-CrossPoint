// Make footnote markers in an unpacked EPUB the size of body text, on the baseline
// (like the reference book «Мир как воля и представление»).
// node fix_footnotes.mjs <unpacked-dir>
// - <sup>/<sub> around a footnote link or [N] become <span> (the reader shrinks sup/sub itself);
// - CSS rules for those markers, and any rule with shrunk font + vertical-align super/sub,
//   get font-size: 1em and vertical-align: baseline.
import fs from 'node:fs';
import path from 'node:path';

const dir = process.argv[2];
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const files = walk(dir);
const markerClasses = new Set();
let converted = 0;

const toSpan = (attrs, inner) => {
  for (const c of (attrs.match(/class="([^"]*)"/) || [, ''])[1].split(/\s+/)) if (c) markerClasses.add(c);
  converted++;
  return `<span${attrs}>${inner}</span>`;
};
for (const f of files.filter(f => /\.x?html?$/i.test(f))) {
  let t = fs.readFileSync(f, 'utf8');
  const before = t;
  // <sup><a href>N</a></sup>, <sup>[N]</sup>
  t = t.replace(/<(sup|sub)\b([^>]*)>(\s*<a\b[^>]*>\s*\[?[^<]{1,12}?\]?\s*<\/a>\s*)<\/\1>/gi, (_, tag, a, inner) => toSpan(a, inner));
  t = t.replace(/<(sup|sub)\b([^>]*)>(\s*\[\d{1,4}\*?\]\s*)<\/\1>/gi, (_, tag, a, inner) => toSpan(a, inner));
  // <a href><sup>N</sup></a>
  t = t.replace(/(<a\b[^>]*href[^>]*>\s*)<(sup|sub)\b([^>]*)>([^<]{1,12})<\/\2>(\s*<\/a>)/gi, (_, open, tag, a, inner, close) => open + toSpan(a, inner) + close);
  // classes on footnote links themselves
  for (const m of t.matchAll(/<a\b[^>]*href="[^"]*#[^"]*"[^>]*class="([^"]*)"[^>]*>\s*\[?\d{1,4}\*?\]?\s*<\/a>|<a\b[^>]*class="([^"]*)"[^>]*href="[^"]*#[^"]*"[^>]*>\s*\[?\d{1,4}\*?\]?\s*<\/a>/gi))
    for (const c of (m[1] || m[2] || '').split(/\s+/)) if (c) markerClasses.add(c);
  if (t !== before) fs.writeFileSync(f, t);
}

const small = v => {
  const m = v.trim().match(/^([\d.]+)(em|%)$/i);
  if (m) return (m[2] === '%' ? +m[1] / 100 : +m[1]) < 0.95;
  return /^(x?x-small|smaller)$/i.test(v.trim());
};
let rules = 0;
for (const f of files.filter(f => /\.css$/i.test(f))) {
  let t = fs.readFileSync(f, 'utf8');
  const out = t.replace(/([^{}]+)\{([^}]*)\}/g, (all, sel, body) => {
    const fsz = body.match(/font-size\s*:\s*([^;}]+)/i);
    if (!fsz || !small(fsz[1])) return all;
    const classes = [...sel.matchAll(/\.([\w-]+)/g)].map(m => m[1]);
    const isMarker = classes.some(c => markerClasses.has(c));
    const raised = /vertical-align\s*:\s*(super|sub|top|text-top)/i.test(body);
    if (!isMarker && !raised) return all;
    rules++;
    let b = body.replace(/font-size\s*:\s*[^;}]+/i, 'font-size: 1em');
    b = /vertical-align/i.test(b) ? b.replace(/vertical-align\s*:\s*[^;}]+/i, 'vertical-align: baseline') : b.replace(/\s*$/, ';\n\tvertical-align: baseline\n');
    return `${sel}{${b}}`;
  });
  if (out !== t) fs.writeFileSync(f, out);
}
console.log(`сносок переведено в span: ${converted}; классов сносок: ${[...markerClasses].join(', ') || '—'}; правил CSS исправлено: ${rules}`);
