// Structural EPUB lint (no Java needed). node epub_lint.mjs <book.epub>...
// mimetype first & stored · container → OPF · manifest files exist · spine idrefs · every internal href/#id resolves ·
// XHTML well-formed (xmllint) · the same number of links as the reference copy (--ref <orig.epub>, optional).
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os'; import { execFileSync } from 'node:child_process';
const args = process.argv.slice(2); const refI = args.indexOf('--ref'); const ref = refI >= 0 ? args.splice(refI, 2)[1] : null;
const unzip = f => { const d = fs.mkdtempSync(path.join(os.tmpdir(), 'epl-')); execFileSync('unzip', ['-q', '-o', f, '-d', d]); return d; };
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const linkCount = dir => walk(dir).filter(f => /\.x?html?$/i.test(f)).reduce((n, f) => n + (fs.readFileSync(f, 'utf8').match(/<a\b[^>]*href=/g) || []).length, 0);
let bad = 0;
for (const book of args) {
  const errs = [];
  const raw = fs.readFileSync(book);
  // local header of the first entry: name, compression method
  const nameLen = raw.readUInt16LE(26), method = raw.readUInt16LE(8), first = raw.slice(30, 30 + nameLen).toString();
  if (first !== 'mimetype') errs.push('первый файл не mimetype: ' + first);
  if (method !== 0) errs.push('mimetype сжат');
  const d = unzip(book);
  if (fs.readFileSync(path.join(d, 'mimetype'), 'utf8').trim() !== 'application/epub+zip') errs.push('mimetype неверный');
  const cont = fs.readFileSync(path.join(d, 'META-INF/container.xml'), 'utf8');
  const opfRel = cont.match(/full-path="([^"]+)"/)[1]; const opfPath = path.join(d, opfRel); const opfDir = path.dirname(opfPath);
  const opf = fs.readFileSync(opfPath, 'utf8');
  const manifest = new Map([...opf.matchAll(/<item\b[^>]*>/g)].map(m => [m[0].match(/\bid="([^"]+)"/)[1], decodeURIComponent(m[0].match(/\bhref="([^"]+)"/)[1])]));
  for (const [id, h] of manifest) if (!fs.existsSync(path.join(opfDir, h))) errs.push('нет файла манифеста: ' + h);
  for (const m of opf.matchAll(/<itemref\b[^>]*idref="([^"]+)"/g)) if (!manifest.has(m[1])) errs.push('spine ссылается на нет id: ' + m[1]);
  const files = walk(d); const docs = files.filter(f => /\.(x?html?|ncx)$/i.test(f));
  const ids = new Map(docs.map(f => [path.resolve(f), new Set([...fs.readFileSync(f, 'utf8').matchAll(/\bid="([^"]+)"/g)].map(m => m[1]))]));
  let links = 0;
  for (const f of docs) {
    const t = fs.readFileSync(f, 'utf8');
    if (/\.x?html?$/i.test(f)) { try { execFileSync('xmllint', ['--noout', f], { stdio: 'pipe' }); } catch (e) { errs.push('XHTML: ' + path.basename(f) + ' ' + String(e.stderr).split('\n')[0]); } }
    for (const m of t.matchAll(/<(?:a|content)\b[^>]*\b(?:href|src)="([^"]*)"/g)) {
      const h = m[1]; if (/^[a-z]+:/i.test(h) || h === '') continue; links++;
      const [p, frag] = h.split('#'); const target = p ? path.resolve(path.dirname(f), decodeURIComponent(p)) : path.resolve(f);
      if (!fs.existsSync(target)) { errs.push(`ссылка в никуда: ${path.basename(f)} → ${h}`); continue; }
      if (frag && ids.has(target) && !ids.get(target).has(frag)) errs.push(`нет якоря: ${path.basename(f)} → ${h}`);
    }
  }
  let refNote = '';
  if (ref) { const rd = unzip(path.join(ref, path.basename(book))); const a = linkCount(d), b = linkCount(rd); refNote = `; ссылок <a>: ${a} (в оригинале ${b})`; if (a !== b) errs.push(`число ссылок изменилось: ${b} → ${a}`); }
  console.log(`${errs.length ? '✗' : '✓'} ${path.basename(book).slice(0, 55)}: ошибок ${errs.length}; проверено ссылок ${links}${refNote}`);
  for (const e of errs.slice(0, 8)) console.log('    ' + e);
  if (errs.length) bad++;
}
process.exitCode = bad ? 1 : 0;
