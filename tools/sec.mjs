import {chromium} from 'playwright-core';
const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:1440,height:900}});
for (const u of process.argv.slice(2)){await p.goto(u,{waitUntil:'networkidle'});
console.log(u,await p.evaluate(()=>[...document.querySelectorAll(".entry-content > .alignfull, .entry-content > .wp-block-group")].map(e=>e.className.replace(/wp-block-group|alignfull/g,"").trim()+" | "+getComputedStyle(e).backgroundColor+" | "+((e.querySelector("h2,h1")||{}).textContent||"").slice(0,25))));}
await b.close()
