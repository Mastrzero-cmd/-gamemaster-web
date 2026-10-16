// Capturas y pruebas (Playwright/Chromium headless, gratis). Uso: node capturar.mjs <carpeta_salida> <url_base>
import { chromium } from 'playwright'; import fs from 'fs';
const out = process.argv[2], base = process.argv[3]; fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch(); const report = {};
for (const w of [1440, 390]) {
  const n = String(w), h = w > 800 ? 900 : 844;
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, hasTouch: w < 800 });
  const p = await ctx.newPage(); const errs = [];
  p.on('console', m => { if (['error', 'warning'].includes(m.type())) errs.push(m.type() + ': ' + m.text()); }); p.on('pageerror', e => errs.push('pageerror: ' + e.message)); p.on('requestfailed', r => errs.push('requestfailed: ' + r.url()));
  let bytes = 0; p.on('response', async r => { try { const bf = await r.body(); bytes += bf.length; } catch {} });
  await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(600); report[n] = { pesoInicialKB: Math.round(bytes / 1024) };
  const ids = await p.$$eval('.sec', e => e.map(s => s.id));
  const go = async (id, off = 62) => { await p.evaluate(([i, o]) => { const e = document.getElementById(i); window.scrollTo({ top: e.getBoundingClientRect().top + scrollY - o, behavior: 'instant' }); }, [id, off]); await p.waitForTimeout(350); };
  for (const id of ids) { await go(id); await p.screenshot({ path: `${out}/${n}-${id}.jpg`, type: 'jpeg', quality: 84 }); await p.screenshot({ path: `${out}/_png_${n}-${id}.png` }); }
  // parallax: tres posiciones de scroll en el inicio y en catálogo
  for (const y of [0, 300, 600]) { await p.evaluate(y => scrollTo({ top: y, behavior: 'instant' }), y); await p.waitForTimeout(300); await p.screenshot({ path: `${out}/${n}-parallax-scroll${y}.jpg`, type: 'jpeg', quality: 84 }); }
  report[n].parallax = await p.evaluate(async () => { const r = {}; for (const y of [0, 600]) { scrollTo({ top: y, behavior: 'instant' }); await new Promise(a => setTimeout(a, 250)); r[y] = ['bk', 'fr'].map(c => document.querySelector('#inicio .' + c).style.getPropertyValue('--py')); } return r; });
  // filas
  for (const row of await p.$$('[data-row]')) { const name = await row.getAttribute('data-row'); await row.scrollIntoViewIfNeeded(); await p.waitForTimeout(250); await row.screenshot({ path: `${out}/${n}-fila-${name}-inicio.jpg`, type: 'jpeg', quality: 84 });
    await p.evaluate(el => { const t = el.querySelector('.track'); t.style.scrollSnapType = 'none'; t.scrollLeft = t.scrollWidth; }, row); await p.waitForTimeout(500); await row.screenshot({ path: `${out}/${n}-fila-${name}-final.jpg`, type: 'jpeg', quality: 84 });
    await p.evaluate(el => { const t = el.querySelector('.track'); t.style.scrollSnapType = ''; t.scrollLeft = 0; }, row); }
  const fila = await p.evaluate(async () => { const wait = ms => new Promise(r => setTimeout(r, ms)), row = document.querySelector('[data-row=juegos]'), t = row.querySelector('.track'); row.scrollIntoView(); t.scrollLeft = 0; await wait(300);
    const r = {}; row.querySelector('.next').click(); await wait(900); r.flecha = t.scrollLeft > 100; const a = t.scrollLeft; t.focus(); t.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true })); await wait(900); r.teclado = t.scrollLeft > a; r.snap = getComputedStyle(t).scrollSnapType; r.contador = row.querySelector('.cnt').textContent; return r; });
  let drag = null; if (w > 800) { const t = await p.$('[data-row=juegos] .track'); await p.evaluate(() => document.querySelector('[data-row=juegos] .track').scrollLeft = 0); await p.waitForTimeout(400); const bx = await t.boundingBox(); const s0 = await t.evaluate(e => e.scrollLeft);
    await p.mouse.move(bx.x + 600, bx.y + 100); await p.mouse.down(); await p.mouse.move(bx.x + 300, bx.y + 100, { steps: 8 }); await p.mouse.up(); await p.waitForTimeout(900); drag = (await t.evaluate(e => e.scrollLeft)) > s0 + 100; }
  report[n].fila = { ...fila, arrastre: drag }; report[n].desborde = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo({ top: y, behavior: 'instant' }); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); }); await p.waitForTimeout(500);
  report[n].pesoTotalKB = Math.round(bytes / 1024);
  await p.screenshot({ path: `${out}/${n}-pagina-completa.jpg`, type: 'jpeg', quality: 70, fullPage: true });
  report[n].errores = errs; await ctx.close();
}
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }); const p = await ctx.newPage(); await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(500);
await p.evaluate(() => scrollTo(0, 500)); await p.waitForTimeout(300);
report.reducido = await p.evaluate(() => ({ clase: document.documentElement.classList.contains('reduce'), capasSinMover: [...document.querySelectorAll('.ly')].every(e => ['none', 'matrix(1, 0, 0, 1, 0, 0)'].includes(getComputedStyle(e).transform)), scrollBehavior: getComputedStyle(document.documentElement).scrollBehavior }));
await p.evaluate(() => scrollTo(0, 0)); await p.screenshot({ path: `${out}/1440-movimiento-reducido.jpg`, type: 'jpeg', quality: 84 });
await b.close(); console.log(JSON.stringify(report, null, 1));
