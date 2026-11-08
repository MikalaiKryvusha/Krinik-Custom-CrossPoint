// Back up books + /.crosspoint from the reader. node backup.mjs <ip> <outdir>
import fs from 'node:fs'; import path from 'node:path';
const [ip, out] = process.argv.slice(2); const base = `http://${ip}`;
const list = async p => (await fetch(base + '/api/files?path=' + encodeURIComponent(p))).json();
const get = async (p, dst) => { const r = await fetch(base + '/download?path=' + encodeURIComponent(p)); if (!r.ok) { console.log('skip', p, r.status); return; }
  fs.mkdirSync(path.dirname(dst), { recursive: true }); fs.writeFileSync(dst, Buffer.from(await r.arrayBuffer())); };
let n = 0;
const walk = async p => { for (const e of await list(p)) { const q = (p === '/' ? '' : p) + '/' + e.name;
  if (e.isDirectory) await walk(q); else { await get(q, path.join(out, q)); n++; } } };
await walk('/.crosspoint'); await walk('/Книги');
console.log('files:', n);
