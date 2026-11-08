// Footnote references in an unpacked EPUB → « [N] »: number in square brackets, a space on both sides.
// node bracket_footnotes.mjs <unpacked-dir>
// Punctuation . , : ; ! ? … ) ] » ” goes tight after the marker («[4], слово», «[4]. Новое»); a dash keeps its space («[4] — …»).
// A reference = <a href="…#…"> whose text is a number (or *), with any wrapping <span>/<sup>/<sub>.
// The link stays a link (quick return works); brackets go inside it, spaces outside.
// A number at the start of a block (<p>, <li>, <h1>…) is the note's own label or a TOC entry — left alone.
// Markers carry no italic/bold: taken out of a formatted phrase (the phrase keeps its formatting).
// Plain-text «слово[12]» (no link, e.g. a heading copied into the TOC) gets the spaces too.
// Check after: node bracket_audit.mjs <dir>.
import fs from 'node:fs';
import path from 'node:path';

const dir = process.argv[2];
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const BLOCK_TAG = /^<\/?(p|div|li|ul|ol|h[1-6]|br|tr|td|th|table|blockquote|body|section|dt|dd|nav)\b/i;
const NUM = /^\s*[\[\(]?\s*(\d{1,4}\*?|\*{1,3})\s*[\]\)]?\s*$/;
const WS = /[\s ]/;
const TIGHT = /[.,;:!?…)\]»”]/;

// Rendered text character next to position i, skipping inline tags; '\n' = block boundary, '' = none.
const textCharBefore = (t, i) => {
  while (i > 0) {
    const c = t[i - 1];
    if (c === '>') { const s = t.lastIndexOf('<', i - 1); if (BLOCK_TAG.test(t.slice(s, i))) return '\n'; i = s; continue; }
    if (c === ';') { const m = t.slice(Math.max(0, i - 8), i).match(/&(#\d+|#x[0-9a-f]+|[a-z]+);$/i); if (m) return /^&(nbsp|#160|#xa0);$/i.test(m[0]) ? ' ' : 'x'; }
    return c;
  }
  return '';
};
const textCharAfter = (t, i) => {
  while (i < t.length) {
    const c = t[i];
    if (c === '<') { const e = t.indexOf('>', i) + 1; if (BLOCK_TAG.test(t.slice(i, e))) return '\n'; i = e; continue; }
    if (c === '&') { const m = t.slice(i, i + 8).match(/^&(#\d+|#x[0-9a-f]+|[a-z]+);/i); if (m) return /^&(nbsp|#160|#xa0);$/i.test(m[0]) ? ' ' : 'x'; }
    return c;
  }
  return '';
};

let refs = 0, bracketed = 0, spaced = 0, plain = 0, files = 0, italic = 0;
for (const f of walk(dir).filter(f => /\.x?html?$/i.test(f))) {
  const src = fs.readFileSync(f, 'utf8');
  const body = src.search(/<body\b/i);
  if (body < 0) continue;
  let t = src;
  const edits = []; // [pos, deleteLen, insert], applied from the end
  for (const m of src.matchAll(/<a\b[^>]*href="[^"]*#[^"]*"[^>]*>((?:(?!<\/a>).){0,80}?)<\/a>/gs)) {
    if (m.index < body) continue;
    const inner = m[1];
    const txt = inner.replace(/<[^>]+>/g, '');
    if (!NUM.test(txt)) continue;
    // widen over wrappers: <span|sup|sub …> A </span|sup|sub> with nothing else inside
    let s = m.index, e = m.index + m[0].length;
    for (;;) {
      const open = src.slice(0, s).match(/<(span|sup|sub|em|i|b|strong)\b[^>]*>\s*$/i);
      const close = open && src.slice(e).match(new RegExp(`^\\s*</${open[1]}>`, 'i'));
      if (!open || !close) break;
      s -= open[0].length; e += close[0].length;
    }
    const before = textCharBefore(src, s);
    if (before === '\n' || before === '') continue; // note label / TOC entry
    refs++;
    // brackets: rewrite the text part of the anchor
    const want = '[' + txt.match(NUM)[1] + ']';
    if (txt.trim() !== want) {
      const innerStart = m.index + m[0].indexOf('>') + 1;
      const newInner = inner.replace(/(^|>)([^<]*)/g, (all, gt, piece) => piece.trim() && NUM.test(piece) ? gt + piece.replace(/\S.*\S|\S/s, want) : all);
      edits.push([innerStart, inner.length, newInner]); bracketed++;
    }
    const after = textCharAfter(src, e);
    // «[4] ,» → «[4],»; the space may sit inside an inline tag: «[4]<em> .</em>»
    const gap = src.slice(e, e + 80).match(/^(?:[ \t\r\n\u00a0]|&nbsp;|&#160;|<(?:em|i|b|strong|span)\b[^>]*>)+(?=[.,;:!?…)\]»”])/);
    const gapWs = gap && gap[0].replace(/<[^>]*>/g, '') !== '';
    if (gapWs) { edits.push([e, gap[0].length, gap[0].replace(/[ \t\r\n\u00a0]|&nbsp;|&#160;/g, (w, o) => /<[^>]*$/.test(gap[0].slice(0, o)) ? w : '')]); spaced++; }
    else if (!WS.test(after) && !TIGHT.test(after) && after !== '\n' && after !== '') { edits.push([e, 0, ' ']); spaced++; }
    if (!WS.test(before)) { edits.push([s, 0, ' ']); spaced++; }
  }
  edits.sort((a, b) => b[0] - a[0]);
  for (const [p, del, ins] of edits) t = t.slice(0, p) + ins + t.slice(p + del);
  // plain-text references outside links: «слово[12]» → «слово [12]»
  const b2 = t.search(/<body\b/i);
  const head = t.slice(0, b2);
  let tail = t.slice(b2).replace(/>([^<]+)</g, (all, txt) => {
    const out = txt.replace(/([^\s \[])\[(\d{1,4})\]/g, '$1 [$2]').replace(/\[(\d{1,4})\](?=[^\s .,;:!?)\]»”…–—-])/g, '[$1] ');
    if (out !== txt) plain++;
    return '>' + out + '<';
  });
  t = head + tail;
  // markers upright: a phrase stays italic/bold, the marker is taken out of it
  // «<em>Входят могильщики <a>[60]</a>. Дальше</em>» → «<em>Входят могильщики </em><a>[60]</a><em>. Дальше</em>»
  const upright = [];
  for (const m of t.matchAll(/<a\b[^>]*href="[^"]*#[^"]*"[^>]*>(?:<[^>]+>)*\[(?:\d{1,4}\*?|\*{1,3})\](?:<[^>]+>)*<\/a>/g)) {
    let s = m.index, e = s + m[0].length;
    // an <em>/<i>/<b>/<strong> wrapping only the marker is dropped
    const strip = [];
    for (;;) {
      const open = t.slice(Math.max(0, s - 200), s).match(/<(span|sup|sub|em|i|b|strong)\b[^>]*>\s*$/i);
      const close = open && t.slice(e, e + 40).match(new RegExp(`^\\s*</${open[1]}>`, 'i'));
      if (!open || !close) break;
      if (/^(em|i|b|strong)$/i.test(open[1])) strip.push([e, close[0].length, ''], [s - open[0].length, open[0].length, '']);
      s -= open[0].length; e += close[0].length;
    }
    if (strip.length) { upright.push(...strip); italic++; continue; }
    // formatting still open around the marker in this block → close before, reopen after
    const blockStart = Math.max(...['<p', '<div', '<li', '<h1', '<h2', '<h3', '<h4', '<td'].map(b => t.lastIndexOf(b, s)));
    const stack = [];
    for (const tg of t.slice(Math.max(0, blockStart), s).matchAll(/<(\/?)(em|i|b|strong)\b[^>]*>/gi)) tg[1] ? stack.pop() : stack.push(tg[0]);
    if (!stack.length) continue;
    upright.push([e, 0, stack.join('')]);
    upright.push([s, 0, stack.map(o => `</${o.match(/^<(\w+)/)[1]}>`).reverse().join('')]);
    italic++;
  }
  upright.sort((a, b) => b[0] - a[0]);
  for (const [p, del, ins] of upright) t = t.slice(0, p) + ins + t.slice(p + del);
  if (upright.length) t = t.replace(/<(em|i|b|strong)\b[^>]*>(\s*)<\/\1>/g, '$2'); // empty left after the cut
  if (t !== src) { fs.writeFileSync(f, t); files++; }
}
console.log(`сносок: ${refs}; скобки добавлены: ${bracketed}; пробелов поправлено: ${spaced}; текстовых мест без ссылки: ${plain}; вынесено из курсива/жирного: ${italic}; файлов изменено: ${files}`);
