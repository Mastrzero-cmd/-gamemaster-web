// Capturas de verificación v9d (Playwright/Chromium headless, gratis). Uso: node capturar.mjs <carpeta_salida> <url_base> [solo]
import { chromium } from 'playwright'; import fs from 'fs';
const out = process.argv[2], base = process.argv[3], solo = process.argv[4]; fs.mkdirSync(out, { recursive: true });
const secs = [['inicio', '#inicio'], ['marcas', '#marcas'], ['catalogo', '#catalogo'], ['streaming', '#streaming'], ['ia', '#ia'], ['logo', '#marca'], ['sistema', '#sistema'], ['contacto', '#contacto']];
const b = await chromium.launch(); const report = {};
for (const w of (solo ? [+solo] : [1440, 390])) {
  const n = String(w), h = w > 800 ? 900 : 844;
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, hasTouch: w < 800 });
  const p = await ctx.newPage(); const errs = [];
  p.on('console', m => { if (['error', 'warning'].includes(m.type())) errs.push(m.type() + ': ' + m.text()); }); p.on('pageerror', e => errs.push('pageerror: ' + e.message)); p.on('requestfailed', r => errs.push('requestfailed: ' + r.url()));
  await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(600);
  report[n] = { overflow: await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]) };
  const go = async (sel, off = 0) => { await p.evaluate(([s, o]) => { const e = document.querySelector(s); window.scrollTo({ top: e.getBoundingClientRect().top + scrollY - o, behavior: 'instant' }); }, [sel, off]); await p.waitForTimeout(1100); };
  for (const [name, sel] of secs) { await go(sel); await p.screenshot({ path: `${out}/${n}-${name}.jpg`, type: 'jpeg', quality: 84 }); }
  for (const y of [0, 300, 600, 1200]) { await p.evaluate(y => scrollTo({ top: y, behavior: 'instant' }), y); await p.waitForTimeout(900); await p.screenshot({ path: `${out}/${n}-parallax-scroll${y}.jpg`, type: 'jpeg', quality: 84 }); }
  for (const [name, i] of [['plataformas', 0], ['juegos', 1], ['streaming', 2], ['ia', 3]]) {
    const row = (await p.$$('[data-row]'))[i]; await row.scrollIntoViewIfNeeded(); await p.waitForTimeout(400); await row.screenshot({ path: `${out}/${n}-fila-${name}-inicio.jpg`, type: 'jpeg', quality: 84 });
    await p.evaluate(el => { const t = el.querySelector('.track'); t.style.scrollSnapType = 'none'; t.scrollLeft = t.scrollWidth; }, row); await p.waitForTimeout(500);
    await row.screenshot({ path: `${out}/${n}-fila-${name}-final.jpg`, type: 'jpeg', quality: 84 });
    await p.evaluate(el => { const t = el.querySelector('.track'); t.style.scrollSnapType = ''; t.scrollLeft = 0; }, row);
  }
  report[n].flecha = await p.evaluate(async () => { const row = document.querySelector('[data-row=juegos]'); const t = row.querySelector('.track'); row.scrollIntoView(); await new Promise(s => setTimeout(s, 500)); row.querySelector('.next').click(); await new Promise(s => setTimeout(s, 1500)); const a = t.scrollLeft; row.querySelector('.prev').click(); await new Promise(s => setTimeout(s, 1500)); return [a > 100, t.scrollLeft < a]; });
  await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(900);
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { scrollTo({ top: y, behavior: 'instant' }); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); }); await p.waitForTimeout(500);
  await p.screenshot({ path: `${out}/${n}-pagina-completa.jpg`, type: 'jpeg', quality: 70, fullPage: true });
  report[n].errores = errs; await ctx.close();
}
if (!solo) {
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }); const p = await ctx.newPage(); await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(500);
  await p.evaluate(() => scrollTo(0, 500)); await p.waitForTimeout(400);
  report.reducido = await p.evaluate(() => [...document.querySelectorAll('.ly')].every(e => !e.style.getPropertyValue('--py') && getComputedStyle(e).transform === 'none'));
  await p.screenshot({ path: `${out}/1440-movimiento-reducido.jpg`, type: 'jpeg', quality: 84 });
}
await b.close(); console.log(JSON.stringify(report, null, 1));
