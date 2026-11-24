import { chromium } from 'playwright-core';
const [,, base, outDir] = process.argv;
const pages = { home:'/', 'over-ons':'/over-ons/', contact:'/contact/', 'lid-worden':'/lid-worden/', english:'/%F0%9F%87%AC%F0%9F%87%A7/' };
const sizes = { desktop:[1440,900], mobile:[390,844] };
const browser = await chromium.launch({ channel:'chrome' });
for (const [s,[w,h]] of Object.entries(sizes)) {
  const ctx = await browser.newContext({ viewport:{width:w,height:h} });
  const page = await ctx.newPage();
  for (const [name,path] of Object.entries(pages)) {
    await page.goto(base+path, { waitUntil:'networkidle' });
    await page.addStyleTag({ content:'*{animation:none!important;transition:none!important}' });
    await page.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}window.scrollTo(0,0);});
    await page.waitForTimeout(500);
    await page.screenshot({ path:`${outDir}/${name}-${s}.png`, fullPage:true });
    console.log(name, s);
  }
  await ctx.close();
}
await browser.close();
