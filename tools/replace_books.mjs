// Replace books on the reader keeping reading progress. node replace_books.mjs <ip> <dir with fixed .epub> <backup dir> '{"title fragment":"epub_<hash>"}'
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
const [ip, outDir, bak] = process.argv.slice(2); const base = `http://${ip}`;
const sha = b => crypto.createHash('sha1').update(b).digest('hex');
const list = async p => (await fetch(base + '/api/files?path=' + encodeURIComponent(p) + '&_=' + Date.now())).json();
const del = async p => { const r = await fetch(base + '/delete', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: 'paths=' + encodeURIComponent(JSON.stringify([p])) }); return r.status + ' ' + (await r.text()).slice(0, 80); };
const up = async (dir, name, buf) => { const fd = new FormData(); fd.append('file', new Blob([buf]), name); const r = await fetch(base + '/upload?path=' + encodeURIComponent(dir), { method: 'POST', body: fd }); return r.status + ' ' + (await r.text()).slice(0, 80); };
const mkdir = async (dir, name) => { const fd = new FormData(); fd.append('name', name); fd.append('path', dir); const r = await fetch(base + '/mkdir', { method: 'POST', body: fd }); return r.status + ' ' + (await r.text()).slice(0, 80); };
const down = async p => Buffer.from(await (await fetch(base + '/download?path=' + encodeURIComponent(p))).arrayBuffer());
// progress folders to keep: book title fragment → /.crosspoint/epub_<hash> (find by book.bin in the backup)
const keep = JSON.parse(process.argv[5] || "{}");
for (const name of fs.readdirSync(outDir).filter(n => n.endsWith('.epub'))) {
  const buf = fs.readFileSync(path.join(outDir, name)); const p = '/Книги/' + name;
  console.log('==', name.slice(0, 60));
  console.log('  delete', await del(p));
  console.log('  upload', await up('/Книги', name, buf));
  const back = await down(p); console.log('  sha', sha(back) === sha(buf) ? 'совпадает' : 'НЕ СОВПАДАЕТ', back.length);
  const k = Object.keys(keep).find(x => name.includes(x)); if (!k) continue; const d = keep[k];
  const have = (await list("/.crosspoint")).some(e => e.name === d);
  console.log("  progress folder after delete:", have ? "остался" : "стёрт");
  if (have) console.log("  старый кэш удалён", await del("/.crosspoint/" + d)); // stale page cache would show old text
  console.log("  mkdir", await mkdir("/.crosspoint", d));
  const pb = fs.readFileSync(path.join(bak, ".crosspoint", d, "progress.bin"));
  console.log("  progress.bin", await up("/.crosspoint/" + d, "progress.bin", pb));
  const pb2 = await down("/.crosspoint/" + d + "/progress.bin"); console.log("  progress", pb2.equals(pb) ? "возвращён: " + pb.toString("hex") : "НЕ СОВПАДАЕТ");
  console.log("  папка:", (await list("/.crosspoint/" + d)).map(e => e.name).join(", "));
}
