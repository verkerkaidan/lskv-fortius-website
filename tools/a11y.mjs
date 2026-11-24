import {chromium} from 'playwright-core';
const base=process.argv[2];const pages=['/','/over-ons/','/contact/','/lid-worden/','/%F0%9F%87%AC%F0%9F%87%A7/','/nieuws/','/commissies/'];
const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:1440,height:900}});
const res={};
for(const u of pages){await p.goto(base+u,{waitUntil:'load'});await p.waitForTimeout(500);
const r=await p.evaluate(()=>{
 const parse=c=>{const m=c.match(/[\d.]+/g).map(Number);return {r:m[0],g:m[1],b:m[2],a:m[3]??1}};
 const lum=({r,g,b})=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(r)+.7152*f(g)+.0722*f(b)};
 const bg=e=>{let x=e;while(x){const c=parse(getComputedStyle(x).backgroundColor);if(c.a>0.9)return c;if(getComputedStyle(x).backgroundImage!=='none')return null;x=x.parentElement}return {r:255,g:255,b:255,a:1}};
 const out=[],seen=new Set();
 for(const e of document.querySelectorAll('body *')){
  if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))continue;
  const cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0)continue;
  const r=e.getBoundingClientRect();if(!r.width||!r.height)continue;
  const B=bg(e);if(!B)continue;const F=parse(cs.color);
  const L1=lum(F),L2=lum(B),ratio=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
  const size=parseFloat(cs.fontSize),bold=+cs.fontWeight>=700;const large=size>=24||(size>=18.66&&bold);
  if(ratio<(large?3:4.5)){const k=e.className+cs.color+JSON.stringify(B);if(seen.has(k))continue;seen.add(k);out.push(`${e.tagName}.${String(e.className).slice(0,40)} "${e.textContent.trim().slice(0,25)}" ${cs.color} on rgb(${B.r},${B.g},${B.b}) = ${ratio.toFixed(2)} (${size}px)`)}
 }
 const imgs=[...document.images].filter(i=>!i.alt.trim()).map(i=>i.src.split('/').pop().slice(0,40)+(i.closest('a')?' [in link]':''));
 return {out,imgs};});
res[u]=r;}
for(const [u,r] of Object.entries(res)){console.log('##',u);r.out.forEach(x=>console.log('  LOW',x));r.imgs.forEach(x=>console.log('  NOALT',x))}
await b.close();
