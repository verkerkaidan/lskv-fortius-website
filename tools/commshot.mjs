import {chromium} from 'playwright-core';
import fs from 'fs';
const html=fs.readFileSync('/tmp/commissies_content.html','utf8');
const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('https://lskvfortius.nl/?x='+Date.now(),{waitUntil:'networkidle'});
await p.evaluate((h)=>{
  const ec=document.querySelector('.entry-content'); ec.innerHTML=h;
  document.querySelector('.fortius-quote-marquee')?.remove();
  const st=document.createElement('style'); st.textContent=`
  .wp-block-columns{flex-wrap:nowrap;gap:2rem 40px}
  .wp-block-column.is-layout-flow>*{margin-block-start:0;margin-block-end:0}
  .wp-block-column.is-layout-flow>*+*{margin-block-start:16px}
  .wp-block-group.is-layout-flow>*{margin-block:0}
  @media (max-width:781px){.wp-block-columns{flex-wrap:wrap}}`;
  document.head.appendChild(st);
},html);
await p.waitForTimeout(1500);
await p.screenshot({path:'/tmp/commissies-full2.png',fullPage:true});
await b.close();
