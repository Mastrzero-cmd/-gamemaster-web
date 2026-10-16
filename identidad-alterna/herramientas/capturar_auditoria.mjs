// PNG sin pérdida de cada sección con el logo y las portadas ocultos (exentos), para medir mezcla rojo/azul con medir_mezcla.py.
// Uso: node capturar_auditoria.mjs <carpeta_salida> <url>
import { chromium } from 'playwright'; import fs from 'fs';
const out = process.argv[2], base = process.argv[3]; fs.mkdirSync(out, { recursive: true });
const ids = ['inicio', 'marcas', 'catalogo', 'streaming', 'ia', 'marca', 'cromo', 'parallax', 'cortes', 'contacto'];
const b = await chromium.launch();
for (const w of [1440, 390]) {
  const p = await (await b.newContext({ viewport: { width: w, height: w > 800 ? 900 : 844 } })).newPage();
  await p.goto(base, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: '.logoplate img,.plates img,.brand img,.cv img{visibility:hidden!important}' });
  for (const id of ids) {
    await p.evaluate(id => { const e = document.getElementById(id); scrollTo({ top: e.getBoundingClientRect().top + scrollY - 56, behavior: 'instant' }); }, id);
    await p.waitForTimeout(250); await p.screenshot({ path: `${out}/${w}-${id}.png` });
    await p.evaluate(() => scrollBy(0, innerHeight * .6)); await p.waitForTimeout(200); await p.screenshot({ path: `${out}/${w}-${id}-b.png` });
  }
}
await b.close(); console.log('ok');
