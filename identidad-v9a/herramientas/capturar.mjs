// Capturas de verificación (Playwright/Chromium, gratis). Uso: node capturar.mjs <salida> <url>
import { chromium } from 'playwright'; import fs from 'fs';
const out = process.argv[2], base = process.argv[3]; fs.mkdirSync(out, { recursive: true });
const secs = [['inicio','#inicio'],['marcas','#marcas'],['catalogo','#catalogo'],['streaming','#streaming'],['ia','#ia'],['sellos','#sellos'],['logo','#marca'],['sistema','#cromo'],['cortes','#cortes'],['contacto','#contacto']];
const b = await chromium.launch(); const report = {};
for (const w of [1440, 390]) {
  const n = String(w), h = w > 800 ? 900 : 844;
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, hasTouch: w < 800 });
  const p = await ctx.newPage(); const errs = [];
  p.on('console', m => { if (['error', 'warning'].includes(m.type())) errs.push(m.type() + ': ' + m.text()); }); p.on('pageerror', e => errs.push('pageerror: ' + e.message)); p.on('requestfailed', r => errs.push('requestfailed: ' + r.url()));
  await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(600);
  const go = async (sel, off = 70) => { await p.evaluate(([s, o]) => { const e = document.querySelector(s); window.scrollTo({ top: e.getBoundingClientRect().top + scrollY - o, behavior: 'instant' }); }, [sel, off]); await p.waitForTimeout(350); };
  for (const [name, sel] of secs) { await go(sel); await p.screenshot({ path: `${out}/${n}-${name}.jpg`, type: 'jpeg', quality: 86 }); }
  // medallón de cada sección (1 captura por sección con su estampa)
  const est = await p.$$('.estampa'); for (const [i, e] of est.entries()) { await e.scrollIntoViewIfNeeded(); await p.waitForTimeout(250); await e.screenshot({ path: `${out}/${n}-medallon-${i}.jpg`, type: 'jpeg', quality: 86 }); }
  for (const y of [0, 300, 600]) { await p.evaluate(y => scrollTo({ top: y, behavior: 'instant' }), y); await p.waitForTimeout(300); await p.screenshot({ path: `${out}/${n}-inicio-parallax-scroll${y}.jpg`, type: 'jpeg', quality: 84 }); }
  const rows = await p.$$('[data-row]');
  for (const row of rows) { const name = await row.getAttribute('data-row');
    await row.scrollIntoViewIfNeeded(); await p.waitForTimeout(250); await row.screenshot({ path: `${out}/${n}-fila-${name}-inicio.jpg`, type: 'jpeg', quality: 84 });
    await p.evaluate(el => { const t = el.querySelector('.track'); t.style.scrollSnapType = 'none'; t.scrollLeft = t.scrollWidth; }, row); await p.waitForTimeout(500);
    await row.screenshot({ path: `${out}/${n}-fila-${name}-final.jpg`, type: 'jpeg', quality: 84 });
    await p.evaluate(el => { const t = el.querySelector('.track'); t.style.scrollSnapType = ''; t.scrollLeft = 0; }, row); }
  const fila = await p.evaluate(async () => {
    const wait = ms => new Promise(r => setTimeout(r, ms)), row = document.querySelector('[data-row=juegos]'), t = row.querySelector('.track'); row.scrollIntoView(); t.scrollLeft = 0; await wait(300);
    const r = {}; row.querySelector('.next').click(); await wait(900); r.flecha = t.scrollLeft > 100; const a = t.scrollLeft;
    t.focus(); t.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true })); await wait(900); r.teclado = t.scrollLeft > a;
    r.snap = getComputedStyle(t).scrollSnapType; r.contador = row.querySelector('.cnt').textContent; return r; });
  let drag = null;
  if (w > 800) { const box = await (await p.$('[data-row=juegos] .track')).boundingBox(); const t = await p.$('[data-row=juegos] .track'); await p.evaluate(() => document.querySelector('[data-row=juegos] .track').scrollLeft = 0); await p.waitForTimeout(400); const s0 = await t.evaluate(e => e.scrollLeft);
    await p.mouse.move(box.x + 600, box.y + 100); await p.mouse.down(); await p.mouse.move(box.x + 300, box.y + 100, { steps: 8 }); await p.mouse.up(); await p.waitForTimeout(900); drag = (await t.evaluate(e => e.scrollLeft)) > s0 + 100; }
  report[n] = { fila: { ...fila, arrastre: drag }, desborde: await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]) };
  for (const [k, sel] of [['oscuro', '.big-plate.dk'], ['claro', '.big-plate.lt']]) { const el = await p.$(sel); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(250); await el.screenshot({ path: `${out}/${n}-logo-solo-${k}.jpg`, type: 'jpeg', quality: 90 }); }
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo({ top: y, behavior: 'instant' }); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); }); await p.waitForTimeout(500);
  await p.screenshot({ path: `${out}/${n}-pagina-completa.jpg`, type: 'jpeg', quality: 60, fullPage: true });
  report[n].errores = errs; await ctx.close();
}
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }); const p = await ctx.newPage(); await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(500);
await p.evaluate(() => scrollTo(0, 500)); await p.waitForTimeout(300);
report.reducido = await p.evaluate(() => ({ clase: document.documentElement.classList.contains('reduce'), capasSinMover: [...document.querySelectorAll('.ly')].every(e => getComputedStyle(e).transform === 'none' || getComputedStyle(e).transform === 'matrix(1, 0, 0, 1, 0, 0)'), scrollBehavior: getComputedStyle(document.documentElement).scrollBehavior }));
await p.evaluate(() => scrollTo(0, 0)); await p.screenshot({ path: `${out}/1440-movimiento-reducido.jpg`, type: 'jpeg', quality: 84 });
await b.close(); console.log(JSON.stringify(report, null, 1));
