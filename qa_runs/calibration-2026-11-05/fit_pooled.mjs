import { readFileSync, writeFileSync } from 'node:fs';
import vm from 'node:vm';
const S = process.argv[2], D = process.env.HOME + '/Xteink/qa_runs/calibration-2026-11-05';
const html = readFileSync(process.env.HOME + '/Xteink/KEINKT/calibrator/index.html', 'utf8');
const core = html.split('// ===== CORE-BEGIN')[1].split('// ===== CORE-END')[0];
const ctx = { globalThis: {} }; vm.runInNewContext(core.slice(core.indexOf('\n')) + '\nglobalThis.Calib = Calib;', ctx);
const C = ctx.globalThis.Calib, L = Array.from(C.LEVELS);
function bmp(p) { const b = readFileSync(p), off = b.readUInt32LE(10), w = b.readInt32LE(18), hh = b.readInt32LE(22), by = b.readUInt16LE(28) / 8;
  const h = Math.abs(hh), row = Math.ceil(w * by / 4) * 4, d = new Float32Array(w * h);
  for (let y = 0; y < h; y++) { const sy = hh > 0 ? h - 1 - y : y; for (let x = 0; x < w; x++) { const i = off + sy * row + x * by; d[y * w + x] = 0.299 * b[i + 2] + 0.587 * b[i + 1] + 0.114 * b[i]; } }
  return { w, h, d }; }
const txt = (f) => readFileSync(f, 'utf8').match(/\d+/g).map(Number);
// one photo → points (file 0..1, seen 0..1); `curve` = the table the card went through (check photo), else identity
function points(f, curve) {
  const seen = C.analyze(bmp(`${S}/cal/${f}.bmp`)).seen, mono = C.isotonic(seen), lo = mono[0], hi = mono[mono.length - 1];
  return seen.map((v, i) => ({ x: (curve ? curve[L[i]] : L[i]) / 255, y: (v - lo) / (hi - lo), f }));
}
const N = 64;
function fit(pts, sigma) {
  const s = [...pts].sort((a, b) => a.x - b.x), iso = C.isotonic(s.map((p) => p.y));
  let r = [];
  for (let g = 0; g <= N; g++) {
    const x = g / N;
    if (!sigma) { // plain: linear interpolation of the isotonic points
      let k = s.findIndex((p) => p.x >= x); if (k < 0) k = s.length - 1;
      r.push(k === 0 || s[k].x === s[k - 1].x ? iso[k] : iso[k - 1] + (iso[k] - iso[k - 1]) * (x - s[k - 1].x) / (s[k].x - s[k - 1].x)); continue; }
    let sw = 0, sy = 0; s.forEach((p, i) => { const w = Math.exp(-((p.x - x) ** 2) / (2 * sigma * sigma)); sw += w; sy += w * iso[i]; });
    r.push(sy / sw);
  }
  r = C.isotonic(r); const r0 = r[0], r1 = r[N]; r = r.map((v) => (v - r0) / (r1 - r0));
  for (let g = 1; g <= N; g++) r[g] = Math.max(r[g], r[g - 1] + 1e-3);
  const top = r[N]; return r.map((v) => v / top);
}
const at = (r, x) => { const u = Math.min(N - 1e-9, Math.max(0, x * N)), i = Math.floor(u), t = u - i; return r[i] * (1 - t) + r[i + 1] * t; };
function invert(r) { const t = new Uint8Array(256);
  for (let k = 0; k < 256; k++) { const want = k / 255; let lo = 0, hi = 1; for (let it = 0; it < 30; it++) { const m = (lo + hi) / 2; if (at(r, m) < want) lo = m; else hi = m; } t[k] = Math.round(255 * hi); }
  t[0] = 0; t[255] = 255; for (let k = 1; k < 256; k++) if (t[k] < t[k - 1]) t[k] = t[k - 1]; return t; }
const sets = {
  pictures: { plain: ['135812', '141931', '142030'], check: [['141026', txt(`${D}/panel_curve.txt`)]], old: txt(`${D}/panel_curve.txt`), file: 'panel_curve.txt' },
  books: { plain: ['135832', '141943', '142012'], check: [['141059', txt(`${D}/panel_curve_book.txt`)]], old: txt(`${D}/panel_curve_book.txt`), file: 'panel_curve_book.txt' },
};
const res = {};
for (const [kind, st] of Object.entries(sets)) {
  const groups = [...st.plain.map((f) => points(f)), ...st.check.map(([f, c]) => points(f, c))];
  console.log(`== ${kind}: ${groups.length} кадров, ${groups.flat().length} точек`);
  // leave-one-photo-out: fit the others, predict the held-out photo
  for (const sigma of [0, 0.01, 0.02, 0.03, 0.05]) {
    const errs = groups.map((g, i) => { const r = fit(groups.filter((_, j) => j !== i).flat(), sigma); return g.reduce((a, p) => a + Math.abs(at(r, p.x) - p.y), 0) / g.length * 100; });
    console.log(`  sigma ${sigma}: ошибка предсказания отложенного кадра ${errs.map((e) => e.toFixed(1)).join(' / ')} → среднее ${(errs.reduce((a, b) => a + b) / errs.length).toFixed(2)} п.п.`);
  }
  res[kind] = { groups, st };
}
writeFileSync(`${S}/fit_state.json`, JSON.stringify({}));
export {};
const fmt = (t) => { const a = Array.from(t), l = []; for (let i = 0; i < 256; i += 16) l.push(a.slice(i, i + 16).join(' ')); return l.join('\n') + '\n'; };
const shape = (t) => { let jump = 0, run = 1, flat = 1; for (let k = 1; k < 256; k++) { jump = Math.max(jump, t[k] - t[k - 1]); run = t[k] === t[k - 1] ? run + 1 : 1; flat = Math.max(flat, run); } return `макс скачок ${jump}, самая длинная площадка ${flat}`; };
const out = {};
for (const [kind, { groups, st }] of Object.entries(res)) {
  const r = fit(groups.flat(), 0.02), t = invert(r);
  const pred = (tab) => { let mx = 0, s = 0; for (let k = 0; k < 256; k++) { const d = Math.abs(at(r, tab[k] / 255) - k / 255) * 100; mx = Math.max(mx, d); s += d; } return `среднее ${(s / 256).toFixed(1)}, макс ${mx.toFixed(0)}`; };
  console.log(`== ${kind}`);
  console.log(`  на карте сейчас: ${shape(st.old)}; ожидаемое отклонение экрана ${pred(st.old)} п.п.`);
  console.log(`  новая:           ${shape(t)}; ожидаемое отклонение экрана ${pred(t)} п.п.`);
  let mx = 0, s = 0; for (let k = 0; k < 256; k++) { const d = Math.abs(t[k] - st.old[k]); mx = Math.max(mx, d); s += d; }
  console.log(`  разница таблиц: среднее ${(s / 256 / 2.55).toFixed(1)}, макс ${(mx / 2.55).toFixed(0)} п.п.`);
  writeFileSync(`${S}/cal/v2_${st.file}`, fmt(t)); out[kind] = { r, t, old: st.old, groups };
}
writeFileSync(`${S}/fit_out.json`, JSON.stringify(Object.fromEntries(Object.entries(out).map(([k, v]) => [k, { r: v.r, t: Array.from(v.t), old: v.old, pts: v.groups.map((g) => g.map((p) => [p.x, p.y])) }]))));
