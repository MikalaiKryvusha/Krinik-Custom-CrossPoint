// Declare a cover image in an unpacked EPUB (2 or 3): copy it next to the OPF as cover.jpg, add a manifest item
// (properties="cover-image" in EPUB 3) and <meta name="cover"> for EPUB 2 readers. No cover page in the spine.
// node add_cover.mjs <unpacked-dir> <cover.jpg>
import fs from 'node:fs'; import path from 'node:path';
const [dir, cover] = process.argv.slice(2);
const container = fs.readFileSync(path.join(dir, 'META-INF/container.xml'), 'utf8');
const opfPath = path.join(dir, container.match(/full-path="([^"]+)"/)[1]);
let opf = fs.readFileSync(opfPath, 'utf8');
const v3 = /<package[^>]*version="3/.test(opf);
if (/properties="[^"]*cover-image|<meta[^>]*name="cover"/.test(opf)) { console.log('уже есть обложка:', opfPath); process.exit(0); }
fs.copyFileSync(cover, path.join(path.dirname(opfPath), 'cover.jpg'));
const item = `<item id="cover-img" href="cover.jpg" media-type="image/jpeg"${v3 ? ' properties="cover-image"' : ''}/>`;
opf = opf.replace(/<manifest([^>]*)>/, m => `${m}\n    ${item}`);
opf = opf.replace(/<\/metadata>/, '    <meta name="cover" content="cover-img"/>\n  </metadata>');
fs.writeFileSync(opfPath, opf);
console.log('обложка добавлена:', path.relative(dir, opfPath), v3 ? 'EPUB 3' : 'EPUB 2');
