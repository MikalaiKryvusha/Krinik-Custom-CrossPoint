// Note labels in an unpacked EPUB → «[N] текст сноски»: the note's own number in square brackets, text size, at the
// start of the note text (Nikolai 04.11.2026: «чтобы текст ссылки начинался с этого номера в обрамлении [012]»).
// node bracket_note_labels.mjs <unpacked-dir>
// A note = the element a reference «[N]» links to (run bracket_footnotes.mjs first). Its label shapes, seen in our books:
//   A  <p id><span class="sup"><a [href] class="a">012</a></span> text      → <p id><a [href] class="a">[012]</a> text
//   B  <h1 id><a id/>… N <br/></h1> <div class="paragraph">text           → <div class="paragraph" id><a id/>…[N] text
//   C  <div id><div class="title1"> <p class="p">N</p> </div><p class="p1">text → <div id><p class="p1">[N] text
// Ids stay (links and the TOC keep working); a back-link on the number stays a link. Unknown shapes are listed, not
// touched. Check after: node text_same.mjs <original> <dir> (brackets and spaces don't count), epubcheck.
import fs from 'node:fs';
import path from 'node:path';

const dir = process.argv[2];
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const files = walk(path.resolve(dir)).filter(f => /\.x?html?$/i.test(f));
const text = new Map(files.map(f => [f, fs.readFileSync(f, 'utf8')]));
const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// targets of «[N]» references: file → set of ids
const targets = new Map();
for (const [f, t] of text) {
  for (const m of t.matchAll(/<a\b[^>]*href="([^"#]*)#([^"]+)"[^>]*>\s*(?:<[^>]+>\s*)*\[(\d{1,4}\*?)\]/g)) {
    const target = m[1] ? path.resolve(path.dirname(f), decodeURIComponent(m[1])) : f;
    // a back-link from a note to its reference («[012]» in the note → the <a id> in the text) is not a note
    const tt = text.get(target);
    if (tt && new RegExp(`<a\\b[^>]*\\bid="${esc(m[2])}"[^>]*\\bhref=|<a\\b[^>]*\\bhref=[^>]*\\bid="${esc(m[2])}"`).test(tt)) continue;
    if (!targets.has(target)) targets.set(target, new Set());
    targets.get(target).add(m[2]);
  }
}

const done = { A: 0, B: 0, C: 0, already: 0 };
const unknown = [];
for (const [f, ids] of targets) {
  let t = text.get(f);
  if (t === undefined) { unknown.push(`${path.basename(f)}: файла нет`); continue; }
  for (const id of ids) {
    const I = esc(id);
    // already bracketed (a rerun)
    if (new RegExp(`id="${I}"[^>]*>(?:\\s*<[^>]+>)*\\s*\\[\\d{1,4}\\*?\\]`).test(t)) { done.already++; continue; }
    const a = new RegExp(`(<p\\b[^>]*\\bid="${I}"[^>]*>)\\s*<span\\b[^>]*class="sup"[^>]*>\\s*(<a\\b[^>]*>)\\s*(\\d{1,4}\\*?)\\s*</a>\\s*</span>\\s*`);
    const b = new RegExp(`<h1\\b[^>]*\\bid="${I}"[^>]*>((?:\\s*<a\\b[^>]*>\\s*</a>)*)\\s*(\\d{1,4}\\*?)\\s*(?:<br\\b[^>]*/?>)?\\s*</h1>\\s*<div class="paragraph">`);
    const c = new RegExp(`(<div\\b[^>]*\\bid="${I}"[^>]*>)\\s*<div class="title1">\\s*<p class="p">\\s*(\\d{1,4}\\*?)\\s*</p>\\s*</div>\\s*(<p\\b[^>]*>)`);
    if (a.test(t)) { t = t.replace(a, (_, open, link, n) => `${open}${link}[${n}]</a> `); done.A++; }
    else if (b.test(t)) { t = t.replace(b, (_, anchors, n) => `<div class="paragraph" id="${id}">${anchors.trim()}[${n}] `); done.B++; }
    else if (c.test(t)) { t = t.replace(c, (_, open, n, p) => `${open}${p}[${n}] `); done.C++; }
    else {
      const i = t.indexOf(`id="${id}"`);
      unknown.push(`${path.basename(f)}#${id}: ${i < 0 ? 'id не найден' : t.slice(i, i + 140).replace(/\s+/g, ' ')}`);
    }
  }
  text.set(f, t);
}
for (const [f, t] of text) if (targets.has(f)) fs.writeFileSync(f, t);
console.log(`метки: A ${done.A}, B ${done.B}, C ${done.C}, уже в скобках ${done.already}, не распознано ${unknown.length}`);
for (const u of unknown.slice(0, 20)) console.log('  ?', u);
process.exitCode = unknown.length ? 1 : 0;
