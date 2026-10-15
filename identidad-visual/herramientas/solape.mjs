// Busca piezas rojas del frente (z>=3) que tapen texto/controles, barriendo el scroll. Uso: node solape.mjs <ancho>
import { chromium } from 'playwright';
const w=+process.argv[2];const b=await chromium.launch();const p=await b.newPage({viewport:{width:w,height:w>800?900:844}});
await p.goto('file:///workspace/scratch/gm-identidad/identidad-visual/index.html',{waitUntil:'networkidle'});
const H=await p.evaluate(()=>document.body.scrollHeight);const found=new Map();
for(let y=0;y<H;y+=120){await p.evaluate(y=>scrollTo({top:y,behavior:'instant'}),y);await p.waitForTimeout(60);
 const r=await p.evaluate(()=>{const out=[];const T=[...document.querySelectorAll('h1,h2,h3,h4,.lead,.kicker,.btn,.chip,.card p,.card h3,.panel p,.panel span,.panel b,.hint,.row-head button,.nav a,.cut-tag,figcaption,.sw span,.plane-key li,.rule p')];
 const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight};
 for(const z of document.querySelectorAll('.pz.v5,.hero .pz,.pxs .pz,.planes .pz')){if(getComputedStyle(z).display==='none')continue;const zi=+getComputedStyle(z).zIndex||0;if(zi<3)continue;let zr=z.getBoundingClientRect();if(!vis(z))continue;{const sc=z.closest('section,.cut')?.getBoundingClientRect();if(sc)zr={left:Math.max(zr.left,sc.left),right:Math.min(zr.right,sc.right),top:Math.max(zr.top,sc.top),bottom:Math.min(zr.bottom,sc.bottom),width:0,height:0}}
  const im=z.querySelector('img')?zr:zr;
  for(const t of T){if(!vis(t)||t.closest('.hdr')||t.classList.contains('cut-tag'))continue;const tr=t.getBoundingClientRect();const ix=Math.min(zr.right,tr.right)-Math.max(zr.left,tr.left),iy=Math.min(zr.bottom,tr.bottom)-Math.max(zr.top,tr.top);
   if(ix>10&&iy>10&&(ix*iy)/(tr.width*tr.height)>.04){const sec=z.closest('section,.cut');out.push((sec&&sec.id||'cut')+' | '+(z.querySelector('img')?z.querySelector('img').src.split('pieza-')[1]:z.textContent.trim())+' x '+t.tagName+'.'+(t.className||'')+' "'+t.textContent.trim().slice(0,22)+'"')}}}
 return out});
 for(const k of r) found.set(k,(found.get(k)||0)+1)}
console.log(w,'solapes:',found.size);for(const [k,v] of found)console.log(v,k);
console.log('overflow',await p.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]));
await b.close();
