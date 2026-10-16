// Contraste WCAG (AA: 4.5 texto normal, 3 texto grande) de todo el texto visible. Los números fantasma (.ghost) y los contornos (.out) son decorativos/titulares. Uso: node contraste.mjs <url>
import { chromium } from 'playwright';
const b = await chromium.launch(); const out = {};
for (const w of [1440, 390]) { const p = await b.newPage({ viewport: { width: w, height: 900 } }); await p.goto(process.argv[2], { waitUntil: 'networkidle' });
 out[w] = await p.evaluate(() => {
  const lum = c => { const [r, g, bb] = c.map(v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }); return .2126 * r + .7152 * g + .0722 * bb; };
  const cr = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  const parse = s => { const m = s.match(/[\d.]+/g).map(Number); return { c: m.slice(0, 3), a: m[3] === undefined ? 1 : m[3] }; };
  const bgOf = e => { while (e) { const p = parse(getComputedStyle(e).backgroundColor); if (p.a > .9) return p.c; e = e.parentElement; } return [5, 5, 5]; };
  const res = []; const sel = 'h1,h2,h3,h4,p,.kick,.btn,.chip,.nav a,small,.fine,li,.n,b,span,.dl a,figcaption,.lbl,button,.mono';
  for (const e of document.querySelectorAll(sel)) { const r = e.getBoundingClientRect(); if (!r.width || !r.height || getComputedStyle(e).display === 'none' || e.closest('.ghost,.tiles .more')) continue; if (!e.childNodes.length || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
   const cs = getComputedStyle(e); if (cs.color === 'rgba(0, 0, 0, 0)' || cs.webkitTextFillColor === 'rgba(0, 0, 0, 0)') continue;
   const fg = parse(cs.color); const fs = parseFloat(cs.fontSize), big = fs >= 24 || (fs >= 18.66 && +cs.fontWeight >= 700);
   const ratio = cr(fg.c, bgOf(e)); res.push({ k: (e.className && e.className.toString().split(' ')[0]) || e.tagName, t: e.textContent.trim().slice(0, 24), ratio: +ratio.toFixed(2), ok: ratio >= (big ? 3 : 4.5) }); }
  const bad = res.filter(r => !r.ok); return { elementos: res.length, minimo: Math.min(...res.map(r => r.ratio)), fallan: bad.slice(0, 12), nFallan: bad.length }; }); await p.close(); }
await b.close(); console.log(JSON.stringify(out, null, 1));
