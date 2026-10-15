import { chromium } from 'playwright';
const b=await chromium.launch();const out={};
for(const w of [1440,390]){const p=await b.newPage({viewport:{width:w,height:900}});await p.goto('http://localhost:8766/index.html',{waitUntil:'networkidle'});
out[w]=await p.evaluate(()=>{
 const lum=c=>{const [r,g,bb]=c.map(v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4});return .2126*r+.7152*g+.0722*bb};
 const cr=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
 const parse=s=>{const m=s.match(/[\d.]+/g).map(Number);return {c:m.slice(0,3),a:m[3]===undefined?1:m[3]}};
 const bgOf=e=>{while(e){const cs=getComputedStyle(e);const p=parse(cs.backgroundColor);if(p.a>.9)return {c:p.c,el:e};if(cs.backgroundImage!=='none'&&!cs.backgroundImage.includes('repeating'))return {c:[43,63,214],el:e,grad:true};e=e.parentElement}return {c:[5,7,31]}};
 const res=[];
 const sel='h1,h2,h3,h4,p,.kicker,.btn,.chip,.cut-tag,.rt span,figcaption b,figcaption span,.sw span,.nav a,small,.hint,li';
 for(const e of document.querySelectorAll(sel)){const r=e.getBoundingClientRect();if(!r.width||!r.height||getComputedStyle(e).display==='none')continue;if(e.closest('.rstrip'))continue;
  const fg=parse(getComputedStyle(e).color);const bg=bgOf(e);res.push({k:(e.className&&e.className.toString().split(' ')[0])||e.tagName,t:e.textContent.trim().slice(0,28),ratio:+cr(fg.c,bg.c).toFixed(2),big:parseFloat(getComputedStyle(e).fontSize)>=24||(parseFloat(getComputedStyle(e).fontSize)>=18.6&&+getComputedStyle(e).fontWeight>=700)})}
 const by={};for(const r of res){const o=by[r.k]=by[r.k]||{min:99,n:0,t:''};o.n++;if(r.ratio<o.min){o.min=r.ratio;o.t=r.t}}
 return by});await p.close()}
console.log(JSON.stringify(out[1440],null,0));
await b.close();
