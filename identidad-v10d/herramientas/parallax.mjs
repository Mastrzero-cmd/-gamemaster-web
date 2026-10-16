// Mide el desplazamiento propio de cada capa (translate3d Y) al recorrer 600 px de scroll. Uso: node parallax.mjs <url> [ancho]
import { chromium } from 'playwright';
const url = process.argv[2], w = +(process.argv[3] || 1440);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: w, height: w > 800 ? 900 : 844 } });
await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600);
const out = {};
for (const id of ['inicio', 'catalogo', 'streaming', 'ia']) {
  const read = () => p.evaluate(id => { const s = document.getElementById(id); const o = {}; for (const el of s.querySelectorAll('.stage .ly')) { const k = el.classList.contains('bk') ? 'azul fondo (.02)' : el.classList.contains('md') ? 'negro medio (.08)' : el.classList.contains('fr') ? 'rojo frente (.30)' : 'piezas rojas (.55)'; o[k] = +(parseFloat(el.style.getPropertyValue('--py')) || 0).toFixed(1); } return o; }, id);
  // centra la ventana en el centro de la sección y mide; luego baja 600 px
  await p.evaluate(id => { const s = document.querySelector('#' + id + ' .stage'); const r = s.getBoundingClientRect(); scrollTo({ top: scrollY + r.top + r.height / 2 - innerHeight / 2, behavior: 'instant' }); }, id); await p.waitForTimeout(1500);
  const a = await read(); await p.evaluate(() => scrollBy({ top: 600, behavior: 'instant' })); await p.waitForTimeout(1800); const c = await read();
  out[id] = {}; for (const k of Object.keys(a)) out[id][k] = { centro: a[k], mas600: c[k], delta: +(c[k] - a[k]).toFixed(1), pctScroll: +(100 * (c[k] - a[k]) / 600).toFixed(1) };
}
console.log(JSON.stringify(out, null, 1)); await b.close();
