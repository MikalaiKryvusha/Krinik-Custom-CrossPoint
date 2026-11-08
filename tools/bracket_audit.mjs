// Audit footnote markers in an unpacked EPUB by rendered text: every in-text reference must read « [N] ».
// Punctuation . , : ; ! ? … ) ] » ” must be tight after the marker; anything else — a space.
// node bracket_audit.mjs <dir> [--show N]
import fs from 'node:fs'; import path from 'node:path';
const dir = process.argv[2]; const show = +(process.argv[process.argv.indexOf('--show') + 1] || 0) || 0;
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const BLOCK = /<\/?(p|div|li|ul|ol|h[1-6]|br|tr|td|table|blockquote|body|section|dt|dd)\b[^>]*>/gi;
const REF = /<a\b[^>]*href="[^"]*#[^"]*"[^>]*>((?:(?!<\/a>).){0,80})<\/a>/gs;
const isNum = s => /^\s*[\[\(]?\s*\d{1,4}\*?\s*[\]\)]?\s*$|^\s*\*{1,3}\s*$/.test(s);
let refs = 0, noBr = 0, glued = 0; const ex = [];
for (const f of walk(dir).filter(f => /\.x?html?$/i.test(f))) {
  let t = fs.readFileSync(f, 'utf8').replace(/<head\b.*?<\/head>/s, '');
  // mark in-text references with sentinels, then render to text
  t = t.replace(REF, (all, inner) => { const txt = inner.replace(/<[^>]+>/g, ''); return isNum(txt) ? '\u0001' + txt + '\u0002' : all; });
  const text = t.replace(BLOCK, '\n').replace(/<[^>]+>/g, '').replace(/&nbsp;|&#160;/g, ' ').replace(/&[a-z]+;|&#\d+;/g, 'x');
  for (const m of text.matchAll(/(.?)\u0001([^\u0002]*)\u0002(\s*.?)/g)) {
    if (m[1] === '\n' || m[1] === '') continue; // label at the start of a block = the note itself, not a reference
    refs++;
    const badBr = !/^\[\d{1,4}\*?\]$|^\[\*{1,3}\]$/.test(m[2]);
    const badSp = !/\s/.test(m[1]) || !(m[3] === '' || /^[.,;:!?…)\]»”]$/.test(m[3]) || (/^\s/.test(m[3]) && !/[.,;:!?…)\]»”]$/.test(m[3])));
    if (badBr) noBr++; if (badSp) glued++;
    if ((badBr || badSp) && ex.length < show) ex.push(path.basename(f) + ': ' + text.slice(Math.max(0, m.index - 30), m.index + m[0].length + 20).replace(/\s+/g, ' ').replace(/[\u0001\u0002]/g, '|'));
  }
  // unlinked markers in text: word[12] or [12]word, superscript digits; a note label at a block start may be
  // followed by «…» (the note quotes a fragment): «[14] …кота»
  for (const m of text.replace(/\u0001[^\u0002]*\u0002/g, ' ').matchAll(/\S\[\d{1,4}\]|\[\d{1,4}\][^\s.,;:!?)\]»”…]|(?<!\n[ \t]*)\[\d{1,4}\][ \u00a0]+[.,;:!?)\]»”…]|[¹²³⁴⁵⁶⁷⁸⁹⁰]+/g)) { glued++; if (ex.length < show) ex.push(path.basename(f) + ' (без ссылки): ' + text.slice(Math.max(0, m.index - 30), m.index + 30).replace(/\s+/g, ' ')); }
}
console.log(`сносок в тексте: ${refs}; без [ ]: ${noBr}; прилипло или пробел перед знаком: ${glued}`);
for (const e of ex) console.log('  ' + e);
