// Verificaciones v9d: (1) PNG de cada sección con logos/portadas ocultos para medir mezcla rojo/azul, (2) solapes de íconos rojos con texto/controles,
// (3) contraste AA del texto, (4) peso de la página inicial. Uso: node verificar.mjs <url> <carpeta_png>
import { chromium } from 'playwright'; import fs from 'fs';
const base = process.argv[2], out = process.argv[3]; fs.mkdirSync(out, { recursive: true });
const ids = ['inicio', 'marcas', 'catalogo', 'streaming', 'ia', 'marca', 'sistema', 'contacto'];
const b = await chromium.launch(); const res = {};
for (const w of [1440, 390]) {
  const ctx = await b.newContext({ viewport: { width: w, height: w > 800 ? 900 : 844 } }); const p = await ctx.newPage();
  let bytes = 0; p.on('response', async r => { try { const l = r.headers()['content-length']; bytes += l ? +l : (await r.body()).length; } catch {} });
  await p.goto(base, { waitUntil: 'networkidle' }); await p.waitForTimeout(500);
  res[w] = { pesoKB: Math.round(bytes / 1024) };
  // contraste
  res[w].contraste = await p.evaluate(() => {
    const lum = c => { const [r, g, bb] = c.map(v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4 }); return .2126 * r + .7152 * g + .0722 * bb };
    const cr = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05) };
    const parse = s => { const m = s.match(/[\d.]+/g).map(Number); return { c: m.slice(0, 3), a: m[3] === undefined ? 1 : m[3] } };
    const bgOf = e => { while (e) { const p = parse(getComputedStyle(e).backgroundColor); if (p.a > .9) return p.c; e = e.parentElement } return [5, 5, 5] };
    const by = {};
    for (const e of document.querySelectorAll('h1,h2,h3,h4,p,.btn,.chip,li,em,small,b,span,a,figcaption')) {
      const r = e.getBoundingClientRect(); if (!r.width || !r.height || !e.childNodes.length || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
      const cs = getComputedStyle(e); if (cs.webkitTextFillColor === 'rgba(0, 0, 0, 0)') continue;
      const ratio = cr(parse(cs.color).c, bgOf(e)); const k = e.tagName + '.' + (e.className || '').toString().split(' ')[0];
      if (!by[k] || ratio < by[k].min) by[k] = { min: +ratio.toFixed(2), t: e.textContent.trim().slice(0, 24) };
    }
    return Object.fromEntries(Object.entries(by).filter(([, v]) => v.min < 4.5));
  });
  // solapes de íconos rojos con texto
  const H = await p.evaluate(() => document.body.scrollHeight); const found = new Set();
  const iconos = await p.evaluate(async () => {
    const out = [];
    for (const img of document.querySelectorAll('.stage>.box>.ly.fr,.stage>.box>.ly.pc')) {
      const t = await (await fetch(img.src)).text(); const vb = t.match(/viewBox="([-\d. ]+)"/)[1].split(' ').map(Number);
      const gs = [...t.matchAll(/<g transform="translate\(([-\d.]+) ([-\d.]+)\) rotate\(([-\d.]+)\) scale\(([\d.]+)\)/g)].map(m => ({ x: +m[1], y: +m[2], r: 200 * +m[4] * 1.05 }));
      out.push({ id: img.closest('section').id, cls: img.className, vb, gs });
    }
    return out;
  });
  res[w].iconos = iconos.length;
  for (let y = 0; y < H; y += 150) {
    await p.evaluate(y => scrollTo({ top: y, behavior: 'instant' }), y); await p.waitForTimeout(70);
    const r = await p.evaluate(iconos => {
      const out = []; const T = [...document.querySelectorAll('h1,h2,h3,h4,.lead,.btn,.chip,.row-ctl button,.nav a,.num,.cta,.dl a,.fine,.plate img,.logoplate,.tiles li,.card,.sw,.types>div,.rules>div')];
      const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < innerHeight };
      for (const im of document.querySelectorAll('.stage>.box>.ly.fr,.stage>.box>.ly.pc')) {
        const rc = im.getBoundingClientRect(); const sec = im.closest('section').id; const spec = iconos.find(i => i.id === sec && im.className.includes(i.cls.includes('fr') ? 'fr' : 'pc'));
        if (!spec) continue;
        for (const g of spec.gs) {
          const cx = rc.left + (g.x - spec.vb[0]) / spec.vb[2] * rc.width, cy = rc.top + (g.y - spec.vb[1]) / spec.vb[3] * rc.height, rad = g.r / spec.vb[2] * rc.width;
          for (const t of T) {
            if (!vis(t) || t.closest('.bar') || t.closest('.stage')) continue; const tr = t.getBoundingClientRect();
            const nx = Math.max(tr.left, Math.min(cx, tr.right)), ny = Math.max(tr.top, Math.min(cy, tr.bottom));
            if ((nx - cx) ** 2 + (ny - cy) ** 2 < (rad * .85) ** 2) out.push(sec + ' ícono(' + Math.round(g.r) + ') × ' + t.tagName + '.' + (t.className || '') + ' "' + t.textContent.trim().slice(0, 20) + '"');
          }
        }
      }
      return out;
    }, iconos);
    r.forEach(k => found.add(k));
  }
  res[w].solapes = [...found]; res[w].overflow = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
  // PNG de auditoría
  await p.addStyleTag({ content: '.bar,.logoplate img,.plate img,.cv img,.mk img,.disc img,.chapa img{visibility:hidden!important}' });
  for (const id of ids) {
    await p.evaluate(id => { const e = document.getElementById(id); scrollTo({ top: e.getBoundingClientRect().top + scrollY, behavior: 'instant' }); }, id);
    await p.waitForTimeout(250); await p.screenshot({ path: `${out}/${w}-${id}.png` });
    await p.evaluate(() => scrollBy(0, innerHeight * .6)); await p.waitForTimeout(200); await p.screenshot({ path: `${out}/${w}-${id}-b.png` });
  }
  await ctx.close();
}
await b.close(); console.log(JSON.stringify(res, null, 1));
