// Capturas de verificación (Playwright/Chromium headless, gratis). Uso: node capturar.mjs <carpeta_salida> <url_base>
import { chromium } from 'playwright'; import fs from 'fs';
const out = process.argv[2], base = process.argv[3]; fs.mkdirSync(out, { recursive: true });
const secs = [['hero', '#inicio'], ['logo', '#logo'], ['paleta', '#paleta'], ['cromo', '#cromo'], ['grabado', '#grabado'], ['parallax', '#parallax'], ['cortes', '#cortes'], ['filas', '#filas'], ['ejemplo-catalogo', '#ej-catalogo'], ['ejemplo-streaming', '#ej-streaming'], ['ejemplo-ia', '#ej-ia']];
const b = await chromium.launch(); const report = {};
for (const w of [1440, 390]) {
  const n = String(w), h = w > 800 ? 900 : 844;
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, hasTouch: w < 800 });
  const p = await ctx.newPage(); const errs = [];
  p.on('console', m => { if (['error', 'warning'].includes(m.type())) errs.push(m.type() + ': ' + m.text()); }); p.on('pageerror', e => errs.push('pageerror: ' + e.message)); p.on('requestfailed', r => errs.push('requestfailed: ' + r.url()));
  await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(700);
  report[n] = { flecha: await (async () => { const q = await ctx.newPage(); await q.goto(base, { waitUntil: 'networkidle' }); const r = await q.evaluate(async () => { const row = document.querySelector('[data-row=juegos]'); const t = row.querySelector('.track'); row.scrollIntoView(); await new Promise(s => setTimeout(s, 500)); row.querySelector('.next').click(); await new Promise(s => setTimeout(s, 1500)); const a = t.scrollLeft; row.querySelector('.prev').click(); await new Promise(s => setTimeout(s, 1500)); return [a > 100, t.scrollLeft < a]; }); await q.close(); return r; })(), overflow: await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]) };
  const go = async (sel, off = 64) => { await p.evaluate(([s, o]) => { const e = document.querySelector(s); window.scrollTo({ top: e.getBoundingClientRect().top + scrollY - o, behavior: 'instant' }); }, [sel, off]); await p.waitForTimeout(350); };
  for (const [name, sel] of secs) { await go(sel); await p.screenshot({ path: `${out}/${n}-${name}.jpg`, type: 'jpeg', quality: 84 }); }
  // parallax del hero y de la sección parallax en varios scrolls
  for (const y of [0, 300, 600]) { await p.evaluate(y => scrollTo({ top: y, behavior: 'instant' }), y); await p.waitForTimeout(300); await p.screenshot({ path: `${out}/${n}-hero-parallax-scroll${y}.jpg`, type: 'jpeg', quality: 84 }); }
  for (const dy of [-250, 0, 250]) { await go('#parallax', 64 - dy); await p.screenshot({ path: `${out}/${n}-parallax-seccion-${dy < 0 ? 'm' : ''}${Math.abs(dy)}.jpg`, type: 'jpeg', quality: 84 }); }
  // logo solo (claro y oscuro)
  for (const [k, sel] of [['oscuro', '.logo-stage .osc'], ['claro', '.logo-stage .cla']]) { const el = await p.$(sel); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(250); await el.screenshot({ path: `${out}/${n}-logo-solo-${k}.jpg`, type: 'jpeg', quality: 90 }); }
  // final de filas
  for (const [name, i] of [['catalogo', 1], ['plataformas', 0], ['streaming', 2], ['ia', 3]]) {
    const row = (await p.$$('[data-row]'))[i]; await row.scrollIntoViewIfNeeded(); await p.evaluate(el => { const t = el.querySelector('.track'); t.style.scrollSnapType = 'none'; t.scrollLeft = t.scrollWidth; }, row); await p.waitForTimeout(500);
    await row.screenshot({ path: `${out}/${n}-fila-${name}-final.jpg`, type: 'jpeg', quality: 84 });
  }
  // página completa (fondo fijo aplanado)
  await p.evaluate(() => document.documentElement.classList.add('flat')); await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300);
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo({ top: y, behavior: 'instant' }); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); }); await p.waitForTimeout(500);
  await p.screenshot({ path: `${out}/${n}-pagina-completa.jpg`, type: 'jpeg', quality: 70, fullPage: true });
  await p.evaluate(() => document.documentElement.classList.remove('flat'));
  report[n].errores = errs; await ctx.close();
}
// movimiento reducido
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }); const p = await ctx.newPage(); await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(500);
report.reducido = await p.evaluate(() => ({ clase: document.documentElement.classList.contains('reduce'), anim: [...document.querySelectorAll('.pz img')].every(i => getComputedStyle(i).animationName === 'none'), parallax: [...document.querySelectorAll('.pz,.ly')].every(e => !e.style.getPropertyValue('--py')) }));
await p.screenshot({ path: `${out}/1440-movimiento-reducido.jpg`, type: 'jpeg', quality: 84 });
await b.close(); console.log(JSON.stringify(report, null, 1));
