// Mide el peso transferido de la página (todas las respuestas, tras recorrer el scroll). Uso: node peso.mjs [ancho]
import { chromium } from 'playwright';
const w=+(process.argv[2]||1440);const b=await chromium.launch();const p=await b.newPage({viewport:{width:w,height:w>800?900:844}});
const sizes=new Map();p.on('response',async r=>{try{const buf=await r.body();sizes.set(r.url().split('/identidad-visual/').pop().replace('http://localhost:8766/',''),buf.length)}catch{}});
await p.goto('http://localhost:8766/index.html',{waitUntil:'networkidle'});
const H=await p.evaluate(()=>document.body.scrollHeight);for(let y=0;y<H;y+=300){await p.evaluate(y=>scrollTo({top:y,behavior:'instant'}),y);await p.waitForTimeout(40)}
await p.waitForTimeout(800);let t=0,f=0,s=0,pn=0;for(const [k,v] of sizes){t+=v;if(/\.(woff2?|ttf)$/.test(k))f+=v;if(/\.svg$/.test(k))s+=v;if(/\.(png|webp|jpg)$/.test(k))pn+=v}
console.log(JSON.stringify({ancho:w,archivos:sizes.size,total:t,fuentes:f,svg:s,raster:pn}));await b.close();
