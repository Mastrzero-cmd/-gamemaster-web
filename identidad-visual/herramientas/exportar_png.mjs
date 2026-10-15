// Exporta los SVG del logo a PNG con fondo transparente (Playwright/Chromium, gratis).
// v3: antes de exportar ajusta el viewBox al contenido real (caja de alfa) + 3 % de margen por lado,
// para que el glitch y el contorno nunca se recorten. Uso: node exportar_png.mjs ../assets/logo
import { chromium } from 'playwright';
import fs from 'fs'; import path from 'path'; import { pathToFileURL } from 'url';
const dir = path.resolve(process.argv[2] || '../assets/logo');
const sizes = [256, 512, 1024, 2048], MARGIN = 0.03;
const b = await chromium.launch();
async function render(file, w, h, tmpName) {
  const p = await b.newPage({ viewport: { width: w, height: h } });
  const tmp = path.join(dir, tmpName);
  fs.writeFileSync(tmp, `<style>html,body{margin:0;background:transparent}img{display:block;width:${w}px;height:${h}px}</style><img src="${file}">`);
  await p.goto(pathToFileURL(tmp).href); await p.waitForLoadState('load'); await p.waitForTimeout(150);
  const buf = await p.screenshot({ omitBackground: true }); await p.close(); return buf;
}
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg') && !f.startsWith('.'))) {
  let svg = fs.readFileSync(path.join(dir, f), 'utf8');
  const m = () => svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"/);
  // 1) caja real de alfa a 1600 px de ancho
  const vb0 = m().slice(1).map(Number); const pd = 0.4;  // marco ampliado: si el glitch se salía del viewBox, aquí sí se ve
  let vb = [vb0[0] - vb0[2] * pd, vb0[1] - vb0[3] * pd, vb0[2] * (1 + 2 * pd), vb0[3] * (1 + 2 * pd)];
  fs.writeFileSync(path.join(dir, '.probe.svg'), svg.replace(/viewBox="[^"]+"/, `viewBox="${vb.join(' ')}"`));
  const PW = 1600, PH = Math.round(PW * vb[3] / vb[2]);
  const probe = (await render('.probe.svg', PW, PH, '.tmp-probe.html')).toString('base64');
  const pg = await b.newPage(); await pg.setContent('<canvas id=c></canvas>');
  const bb = await pg.evaluate(async ([b64, w, h]) => {
    const im = new Image(); im.src = 'data:image/png;base64,' + b64; await im.decode();
    const c = document.getElementById('c'); c.width = w; c.height = h; const x = c.getContext('2d'); x.drawImage(im, 0, 0);
    const d = x.getImageData(0, 0, w, h).data; let x0 = w, y0 = h, x1 = -1, y1 = -1;
    for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) if (d[(j * w + i) * 4 + 3] > 8) { if (i < x0) x0 = i; if (i > x1) x1 = i; if (j < y0) y0 = j; if (j > y1) y1 = j; }
    return [x0, y0, x1 + 1, y1 + 1];
  }, [probe, PW, PH]); await pg.close();
  const k = vb[2] / PW; const cw = (bb[2] - bb[0]) * k, ch = (bb[3] - bb[1]) * k, mx = Math.max(cw, ch) * MARGIN;
  const nvb = [vb[0] + bb[0] * k - mx, vb[1] + bb[1] * k - mx, cw + 2 * mx, ch + 2 * mx];
  svg = svg.replace(/viewBox="[^"]+"/, `viewBox="${nvb.map(v => v.toFixed(1)).join(' ')}"`);
  fs.writeFileSync(path.join(dir, f), svg); vb = nvb;
  for (const w of sizes) {
    const h = Math.round(w * vb[3] / vb[2]);
    fs.writeFileSync(path.join(dir, f.replace('.svg', `-${w}.png`)), await render(f, w, h, '.tmp-export.html'));
  }
}
await b.close(); for (const t of ['.tmp-export.html', '.tmp-probe.html', '.probe.svg']) try { fs.unlinkSync(path.join(dir, t)); } catch {}
