// PNG sin pérdida de cada sección con el logo, las portadas y los logos de terceros ocultos (exentos), para medir mezcla rojo/azul.
// Uso: node capturar_auditoria.mjs <carpeta_salida> <url>
import { chromium } from 'playwright'; import fs from 'fs';
const out = process.argv[2], base = process.argv[3]; fs.mkdirSync(out, { recursive: true });
const ids = ['inicio', 'logo', 'paleta', 'cromo', 'grabado', 'parallax', 'cortes', 'filas', 'ej-catalogo', 'ej-streaming', 'ej-ia'];
const b = await chromium.launch();
for (const w of [1440, 390]) {
  const p = await (await b.newContext({ viewport: { width: w, height: w > 800 ? 900 : 844 } })).newPage();
  await p.goto(base, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: '.logo-stage,.variants,.dl,.logo-plate,.hdr .brand,footer img,.cover img,.card-s .plate{visibility:hidden!important}' });
  for (const id of ids) {
    await p.evaluate(id => { const e = document.getElementById(id); scrollTo({ top: e.getBoundingClientRect().top + scrollY - 64, behavior: 'instant' }); }, id);
    await p.waitForTimeout(250); await p.screenshot({ path: `${out}/${w}-${id}.png` });
    // segunda toma, media pantalla más abajo (otra posición del parallax)
    await p.evaluate(() => scrollBy(0, innerHeight * .6)); await p.waitForTimeout(200); await p.screenshot({ path: `${out}/${w}-${id}-b.png` });
  }
}
await b.close(); console.log('ok');
