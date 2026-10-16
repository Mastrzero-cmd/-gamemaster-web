// Capturas v9b (Playwright/Chromium, gratis). Uso: node capturar.mjs <salida> <url>
import { chromium } from 'playwright'; import fs from 'fs';
const out = process.argv[2], base = process.argv[3]; fs.mkdirSync(out, { recursive: true });
const ids = ['inicio', 'marcas', 'catalogo', 'streaming', 'ia', 'marca', 'sistema', 'cortes', 'contacto'];
const b = await chromium.launch(); const rep = {};
for (const w of [1440, 390]) {
  const ctx = await b.newContext({ viewport: { width: w, height: w > 800 ? 900 : 844 }, hasTouch: w < 800 }); const p = await ctx.newPage(); const errs = [];
  p.on('console', m => { if (['error', 'warning'].includes(m.type())) errs.push(m.text()); }); p.on('pageerror', e => errs.push(e.message)); p.on('requestfailed', r => errs.push('fail ' + r.url()));
  await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(600);
  rep[w] = { overflow: await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]) };
  for (const id of ids) { await p.evaluate(id => { const e = document.getElementById(id); scrollTo({ top: e.getBoundingClientRect().top + scrollY - 64, behavior: 'instant' }); }, id); await p.waitForTimeout(350); await p.screenshot({ path: `${out}/${w}-${id}.jpg`, type: 'jpeg', quality: 82 }); }
  for (const [name, i] of [['juegos', 0], ['plataformas', 1], ['streaming', 2], ['ia', 3]]) {
    const row = (await p.$$('[data-row]'))[i]; await row.scrollIntoViewIfNeeded(); await p.waitForTimeout(300); await row.screenshot({ path: `${out}/${w}-fila-${name}-inicio.jpg`, type: 'jpeg', quality: 82 });
    await p.evaluate(el => { const t = el.querySelector('.track'); t.style.scrollSnapType = 'none'; t.scrollLeft = t.scrollWidth; }, row); await p.waitForTimeout(450); await row.screenshot({ path: `${out}/${w}-fila-${name}-final.jpg`, type: 'jpeg', quality: 82 });
  }
  for (const y of [0, 300, 600]) { await p.evaluate(y => scrollTo({ top: y, behavior: 'instant' }), y); await p.waitForTimeout(300); await p.screenshot({ path: `${out}/${w}-parallax-scroll${y}.jpg`, type: 'jpeg', quality: 82 }); }
  await p.evaluate(() => scrollTo(0, 0)); await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo({ top: y, behavior: 'instant' }); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); }); await p.addStyleTag({ content: '.hud{position:absolute!important}' }); await p.waitForTimeout(400);
  await p.screenshot({ path: `${out}/${w}-pagina-completa.jpg`, type: 'jpeg', quality: 68, fullPage: true });
  rep[w].errores = errs; await ctx.close();
}
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }); const p = await ctx.newPage(); await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(400);
await p.evaluate(() => scrollTo({ top: 500, behavior: 'instant' })); await p.waitForTimeout(300);
rep.reducido = await p.evaluate(() => ({ py: [...document.querySelectorAll('.ly')].every(e => !e.style.getPropertyValue('--py')), parpadeo: getComputedStyle(document.querySelector('.blink')).animationName, clase: document.documentElement.classList.contains('reduce') }));
await p.screenshot({ path: `${out}/1440-movimiento-reducido.jpg`, type: 'jpeg', quality: 82 });
await b.close(); console.log(JSON.stringify(rep, null, 1));
