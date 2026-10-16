// PNG por sección con logo, portadas y logos de terceros ocultos, para medir mezcla rojo/azul. Uso: node capturar_auditoria.mjs <salida> <url>
import { chromium } from 'playwright'; import fs from 'fs';
const out = process.argv[2], base = process.argv[3]; fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch();
for (const w of [1440, 390]) { const p = await b.newPage({ viewport: { width: w, height: w > 800 ? 900 : 844 } }); await p.goto(base, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: '.plate img,.logoplate img,.card img,.roundel img,.cv,.mk,.brand img{visibility:hidden!important}' });
  const ids = ['inicio','marcas','catalogo','streaming','ia','sellos','marca','cromo','cortes','contacto'];
  for (const id of ids) { await p.evaluate(id => { const e = document.getElementById(id); scrollTo({ top: e.getBoundingClientRect().top + scrollY - 60, behavior: 'instant' }); }, id); await p.waitForTimeout(300); await p.screenshot({ path: `${out}/${w}-${id}.png` });
   await p.evaluate(() => scrollBy({ top: 500, behavior: 'instant' })); await p.waitForTimeout(250); await p.screenshot({ path: `${out}/${w}-${id}-b.png` }); }
  await p.close(); }
await b.close();
