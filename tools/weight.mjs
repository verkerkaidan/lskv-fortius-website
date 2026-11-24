import {chromium} from 'playwright-core';
const b=await chromium.launch({channel:'chrome'});
for (const [name,w,h] of [['desktop',1440,900],['mobile',390,844]]){
 const ctx=await b.newContext({viewport:{width:w,height:h}});const p=await ctx.newPage();
 for (const u of process.argv.slice(2)){
  const imgs=[];p.on('response',async r=>{const ct=r.headers()['content-type']||'';if(ct.startsWith('image/')){const len=+r.headers()['content-length']||0;imgs.push([r.url().replace(/^https:\/\//,'').slice(0,80),len])}});
  await p.goto('https://lskvfortius.nl'+u,{waitUntil:'networkidle'});
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,150))}});await p.waitForTimeout(800);
  const tot=imgs.reduce((a,x)=>a+x[1],0);
  console.log(name,u,'images:',imgs.length,'KB:',Math.round(tot/1024));
  imgs.sort((a,b)=>b[1]-a[1]).slice(0,3).forEach(x=>console.log('   ',Math.round(x[1]/1024)+'KB',x[0]));
  p.removeAllListeners('response');
 }
}
await b.close()
