// Safe repairs of conversion leftovers (fb2 → epub via calibre etc.) in an unpacked EPUB; text and layout untouched.
// node epub_repair.mjs <unpacked-dir>
// - <img> without alt → alt="";
// - a link to a #fragment that does not exist → the first link of its sub-list (TOC group), else the file itself;
// - a class-less <span> wrapping blocks (<div>, <p>…) → <div> with the same id (no style, so the page looks the same);
// - a <p> holding a block (picture <div> inside a paragraph) → <div> with the same class (check: no CSS rule on the bare p element);
// - inline-only content right inside <blockquote> (epigraph author) → wrapped in a plain <div>;
// - OPF: empty <guide/> removed; guide references to non-XHTML (cover image) removed.
// Check after: epubcheck book.epub (brew install epubcheck) and node epub_lint.mjs book.epub.
import fs from 'node:fs'; import path from 'node:path';
const dir = process.argv[2];
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const files = walk(dir); const docs = files.filter(f => /\.x?html?$/i.test(f));
const ids = new Map(docs.map(f => [path.resolve(f), new Set([...fs.readFileSync(f, 'utf8').matchAll(/\bid="([^"]+)"/g)].map(m => m[1]))]));
let alt = 0, frag = 0, guide = 0, spans = 0, quotes = 0;
const BLOCKS = /^(div|p|h[1-6]|ul|ol|li|table|blockquote|section|hr|pre|dl)$/i;
const spanToDiv = t => {
  const tags = [...t.matchAll(/<(\/?)([a-zA-Z][\w:-]*)\b[^>]*?(\/?)>/g)];
  const stack = []; const ren = new Set();
  for (const m of tags) {
    const [all, close, name, self] = m; if (self || /^(br|img|hr|meta|link)$/i.test(name) && !close) { if (BLOCKS.test(name)) stack.forEach(s => s.block = true); continue; }
    if (!close) { if (BLOCKS.test(name)) stack.forEach(s => s.block = true); stack.push({ name, i: m.index, len: all.length, cls: /\bclass=/.test(all), block: false }); continue; }
    const o = stack.pop(); if (!o) continue;
    if (o.block && (o.name.toLowerCase() === "span" && !o.cls || o.name.toLowerCase() === "p")) { ren.add(o.i); ren.add(m.index); }
  }
  if (!ren.size) return t;
  let out = "", last = 0;
  for (const m of tags) if (ren.has(m.index)) { out += t.slice(last, m.index) + m[0].replace(/^<(\/?)(span|p)\b/i, "<$1div"); last = m.index + m[0].length; spans++; }
  return out + t.slice(last);
};
for (const f of docs) {
  let t = fs.readFileSync(f, 'utf8'); const src = t;
  t = t.replace(/<img\b(?![^>]*\balt=)([^>]*?)(\/?)>/g, (all, a, sl) => { alt++; return `<img${a} alt=""${sl}>`; });
  t = t.replace(/<a\b([^>]*?)href="([^"#]*)#([^"]+)"([^>]*)>/g, (all, pre, p, fr, post, off, whole) => {
    const target = p ? path.resolve(path.dirname(f), decodeURIComponent(p)) : path.resolve(f);
    if (!ids.has(target) || ids.get(target).has(fr)) return all;
    const after = whole.slice(off + all.length, off + all.length + 600);
    const sub = after.match(/^[^<]*<\/a>\s*<ul\b[^>]*>\s*<li\b[^>]*>\s*<a\b[^>]*href="([^"]+)"/);
    frag++;
    return `<a${pre}href="${sub ? sub[1] : (p || path.basename(f))}"${post}>`;
  });
  t = spanToDiv(t);
  t = t.replace(/(<blockquote\b[^>]*>)(\s*)((?:(?!<\/?(?:div|p|h[1-6]|ul|ol|blockquote|table)\b)[\s\S])*?)(\s*<\/blockquote>)/g, (all, o, sp, inner, c) => inner.trim() && /<(i|em|b|strong|span|a)\b|[^\s<]/.test(inner) ? (quotes++, `${o}${sp}<div>${inner}</div>${c}`) : all);
  if (t !== src) fs.writeFileSync(f, t);
}
for (const f of files.filter(f => /\.opf$/i.test(f))) {
  let t = fs.readFileSync(f, 'utf8'); const src = t;
  t = t.replace(/<reference\b[^>]*href="[^"]*\.(jpe?g|png|gif|svg)"[^>]*\/>\s*/gi, () => { guide++; return ''; });
  t = t.replace(/<guide\b[^>]*>\s*<\/guide>|<guide\s*\/>/g, () => { guide++; return ''; });
  if (t !== src) fs.writeFileSync(f, t);
}
console.log(`alt добавлен: ${alt}; якорей перенаправлено: ${frag}; правок guide: ${guide}; span/p→div: ${spans / 2}; эпиграфов обёрнуто: ${quotes}`);
