// Text of two unpacked EPUBs is the same letter by letter (whitespace and [ ] ignored). node text_same.mjs <orig-dir> <fixed-dir>
import fs from 'node:fs'; import path from 'node:path';
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const text = d => walk(d).filter(f => /\.x?html?$/i.test(f)).sort().map(f => fs.readFileSync(f, 'utf8').replace(/<head\b.*?<\/head>/s, '').replace(/<[^>]+>/g, '').replace(/&nbsp;|&#160;|[\s \[\]]/g, '')).join('');
const [a, b] = [text(process.argv[2]), text(process.argv[3])];
let i = 0; while (i < a.length && a[i] === b[i]) i++;
console.log(a === b ? `✓ текст совпадает: ${a.length} знаков` : `✗ расхождение на знаке ${i}: «${a.slice(i - 30, i + 30)}» → «${b.slice(i - 30, i + 30)}»`);
process.exitCode = a === b ? 0 : 1;
