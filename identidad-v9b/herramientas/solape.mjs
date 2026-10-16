// Busca capas de arte (.ly) o tarjetas que tapen texto/controles fuera de su lienzo y mide solapes de texto con texto, barriendo el scroll. Uso: node solape.mjs <ancho> <url>
import { chromium } from 'playwright';
const w = +process.argv[2], url = process.argv[3]; const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: w, height: w > 800 ? 900 : 844 } });
await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500);
const r = await p.evaluate(() => {
  const T = [...document.querySelectorAll('h1,h2,h3,h4,.lead,.btn,.chip,.fine,.kick,.row-ctl button,.cnt,.nav a,.shead span,.tiles span,.pl b,.pl p,.pl small,.rules p,.sw span,.types p,.speeds li,.dl a,figcaption,.card p,.card .n,.plate .lbl')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden'; });
  const hit = (a, b) => { const x = Math.min(a.right, b.right) - Math.max(a.left, b.left), y = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top); return x > 3 && y > 3; };
  const out = []; const abs = e => { const r = e.getBoundingClientRect(); return { left: r.left + scrollX, right: r.right + scrollX, top: r.top + scrollY, bottom: r.bottom + scrollY }; };
  const R = T.map(e => [e, abs(e)]);
  for (let i = 0; i < R.length; i++) for (let j = i + 1; j < R.length; j++) { const [a, ra] = R[i], [c, rc] = R[j]; if (a.contains(c) || c.contains(a)) continue; if (hit(ra, rc)) out.push(`${a.tagName}.${a.className} "${a.textContent.trim().slice(0, 18)}" x ${c.tagName}.${c.className} "${c.textContent.trim().slice(0, 18)}"`); }
  // capas de arte que salgan de su lienzo hacia texto: el lienzo recorta (overflow:hidden); verificar que ningún .stage se cruce con texto
  const S = [...document.querySelectorAll('.stage')].map(abs); const cross = [];
  R.forEach(([e, r]) => { if (e.closest('.stage')) return; S.forEach((s, i) => { if (hit(r, s)) cross.push(`stage${i} x ${e.tagName}.${e.className} "${e.textContent.trim().slice(0, 18)}"`); }); });
  return { textoConTexto: out, arteConTexto: cross, desborde: [document.documentElement.scrollWidth, innerWidth], tamanoMinimoBoton: Math.min(...[...document.querySelectorAll('.btn,.row-ctl button')].map(e => Math.min(e.offsetWidth, e.offsetHeight))) };
});
console.log(w, JSON.stringify(r, null, 1)); await b.close();
