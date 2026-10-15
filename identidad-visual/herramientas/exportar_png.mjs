// Exporta los SVG del logo a PNG con fondo transparente (Playwright/Chromium, gratis).
// Uso: node exportar_png.mjs ../assets/logo   (requiere `playwright` instalado donde se ejecute)
import { chromium } from 'playwright';
import fs from 'fs'; import path from 'path'; import { pathToFileURL } from 'url';
const dir = path.resolve(process.argv[2] || '../assets/logo');
const sizes = [256, 512, 1024, 2048];
const b = await chromium.launch();
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg'))) {
  const svg = fs.readFileSync(path.join(dir, f), 'utf8');
  const vb = svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"/).slice(1).map(Number);
  for (const w of sizes) {
    const h = Math.round(w * vb[3] / vb[2]);
    const p = await b.newPage({ viewport: { width: w, height: h } });
    const tmp = path.join(dir, '.tmp-export.html');
    fs.writeFileSync(tmp, `<style>html,body{margin:0;background:transparent}img{display:block;width:${w}px;height:${h}px}</style><img src="${f}">`);
    await p.goto(pathToFileURL(tmp).href); await p.waitForLoadState('load'); await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(dir, f.replace('.svg', `-${w}.png`)), omitBackground: true });
    await p.close();
  }
}
await b.close(); try { fs.unlinkSync(path.join(dir, '.tmp-export.html')); } catch {}
