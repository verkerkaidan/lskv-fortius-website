// Usage: node tools/snapshot.mjs <base-url> <out.json>      -> computed-style snapshot of all key pages
// Usage: node tools/snapshot.mjs --diff a.json b.json       -> list elements whose computed styles differ
import { chromium } from 'playwright-core';
import fs from 'fs';
const PROPS = ['color','background-color','background-image','font-family','font-size','font-weight','line-height','letter-spacing','text-transform','text-decoration-line','text-align','display','position','padding-top','padding-right','padding-bottom','padding-left','margin-top','margin-right','margin-bottom','margin-left','border-top-width','border-right-width','border-bottom-width','border-left-width','border-top-color','border-bottom-color','border-radius','opacity','gap','flex-direction','grid-template-columns','width','height','box-shadow'];
if (process.argv[2] === '--diff') {
  const a = JSON.parse(fs.readFileSync(process.argv[3])), b = JSON.parse(fs.readFileSync(process.argv[4]));
  const tol = new Set(['width','height']);
  let total = 0;
  for (const key of Object.keys(a)) {
    const A = a[key], B = b[key];
    if (!B) { console.log(key, 'missing'); continue; }
    if (A.length !== B.length) console.log(key, 'element count', A.length, B.length);
    const seen = new Map();
    for (let i = 0; i < Math.min(A.length, B.length); i++) {
      const diffs = [];
      for (const p of PROPS) {
        const x = A[i].s[p], y = B[i].s[p];
        if (x === y) continue;
        if (tol.has(p) && Math.abs(parseFloat(x) - parseFloat(y)) < 1.5) continue;
        diffs.push(`${p}: ${x} -> ${y}`);
      }
      if (diffs.length) { total++; const k = A[i].sel + ' | ' + diffs.join('; '); seen.set(k, (seen.get(k) || 0) + 1); }
    }
    for (const [k, n] of [...seen].slice(0, 40)) console.log(`[${key}] x${n} ${k}`);
    if (seen.size > 40) console.log(`[${key}] ... ${seen.size - 40} more distinct`);
  }
  console.log('elements differing:', total);
  process.exit(0);
}
const [,, base, out] = process.argv;
const pages = { home:'/', 'over-ons':'/over-ons/', contact:'/contact/', 'lid-worden':'/lid-worden/', english:'/%F0%9F%87%AC%F0%9F%87%A7/', nieuws:'/nieuws/' };
const sizes = { desktop:[1440,900], mobile:[390,844] };
const browser = await chromium.launch({ channel:'chrome' });
const result = {};
for (const [s,[w,h]] of Object.entries(sizes)) {
  const ctx = await browser.newContext({ viewport:{width:w,height:h} });
  const page = await ctx.newPage();
  for (const [name,path] of Object.entries(pages)) {
    await page.goto(base+path, { waitUntil:'networkidle' });
    await page.addStyleTag({ content:'*{animation:none!important;transition:none!important}' });
    await page.waitForTimeout(300);
    result[`${name}-${s}`] = await page.evaluate((PROPS) => {
      const out = [];
      for (const el of document.body.querySelectorAll('*')) {
        if (['SCRIPT','STYLE','NOSCRIPT','PATH','SVG'].includes(el.tagName.toUpperCase())) continue;
        if (el.closest('.wp-block-jetpack-slideshow, .wp-block-jetpack-instagram-gallery')) continue;
        const cs = getComputedStyle(el);
        const s = {}; for (const p of PROPS) s[p] = cs.getPropertyValue(p);
        const r = el.getBoundingClientRect(); s.width = r.width + ''; s.height = r.height + '';
        const sel = el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0,3).join('.') : '');
        out.push({ sel, s });
      }
      return out;
    }, PROPS);
    console.log(name, s, result[`${name}-${s}`].length);
  }
  await ctx.close();
}
await browser.close();
fs.writeFileSync(out, JSON.stringify(result));
