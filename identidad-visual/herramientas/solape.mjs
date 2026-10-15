// Busca masas rojas del frente (.pz) y placas azules (.bp) que tapen texto/controles, barriendo el scroll. Uso: node solape.mjs <ancho>
import { chromium } from 'playwright';
const w=+process.argv[2];const b=await chromium.launch();const p=await b.newPage({viewport:{width:w,height:w>800?900:844}});
await p.goto('http://localhost:8766/index.html',{waitUntil:'networkidle'});
const H=await p.evaluate(()=>document.body.scrollHeight);const found=new Map();
for(let y=0;y<H;y+=120){await p.evaluate(y=>scrollTo({top:y,behavior:'instant'}),y);await p.waitForTimeout(60);
 const r=await p.evaluate(()=>{const out=[];const T=[...document.querySelectorAll('h1,h2,h3,h4,.lead,.btn,.chip,.hint,.note,.row-head button,.nav a,.plate-head span,.stage .tag,.stage figcaption,.tile figcaption,.sw,.planes-key li,.ty p,.rl p,.logo-hero,.var small,.card-s p,.card-g h4')];
 const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight};
 for(const z of document.querySelectorAll('.pz,.bp')){if(getComputedStyle(z).display==='none')continue;const zi=+getComputedStyle(z).zIndex||0;if(zi<1)continue;let zr=z.getBoundingClientRect();if(!vis(z))continue;{const sc=z.closest('section,.cut')?.getBoundingClientRect();if(sc)zr={left:Math.max(zr.left,sc.left),right:Math.min(zr.right,sc.right),top:Math.max(zr.top,sc.top),bottom:Math.min(zr.bottom,sc.bottom),width:0,height:0}}
  const im=z.querySelector('img')?zr:zr;
  for(const t of T){if(!vis(t)||t.closest('.hdr')||t.classList.contains('cut-tag')||(z.classList.contains('bp')&&t.closest('.stage')))continue;const tr=t.getBoundingClientRect();const ix=Math.min(zr.right,tr.right)-Math.max(zr.left,tr.left),iy=Math.min(zr.bottom,tr.bottom)-Math.max(zr.top,tr.top);
   if(ix>10&&iy>10&&(ix*iy)/(tr.width*tr.height)>.04){const sec=z.closest('section,.cut');out.push((sec&&sec.id||'cut')+' | '+(z.querySelector('img')?z.querySelector('img').src.split('/').pop():z.textContent.trim())+' x '+t.tagName+'.'+(t.className||'')+' "'+t.textContent.trim().slice(0,22)+'"')}}}
 return out});
 for(const k of r) found.set(k,(found.get(k)||0)+1)}
console.log(w,'solapes:',found.size);for(const [k,v] of found)console.log(v,k);
console.log('overflow',await p.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]));
await b.close();
