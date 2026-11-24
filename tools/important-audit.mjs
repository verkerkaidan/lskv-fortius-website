// node tools/important-audit.mjs src/additional.css > /tmp/audit.json
// For each rule containing !important: strips it from that rule alone and checks whether computed styles of matched elements change.
import { chromium } from 'playwright-core';
import fs from 'fs';
const cssPath = process.argv[2];
const css = fs.readFileSync(cssPath, 'utf8');
// --- tiny rule parser: returns [{start,end,selector,body,media}] for style rules containing !important
const rules = [];
(function parse() {
  let i = 0, depth = 0, stack = [];
  let selStart = 0;
  while (i < css.length) {
    if (css.startsWith('/*', i)) { i = css.indexOf('*/', i) + 2; selStart = i; continue; }
    const c = css[i];
    if (c === '{') {
      const head = css.slice(selStart, i).trim();
      stack.push({ head, open: i });
      selStart = i + 1;
    } else if (c === '}') {
      const top = stack.pop();
      if (top && !top.head.startsWith('@')) {
        const body = css.slice(top.open + 1, i);
        if (body.includes('!important')) {
          const media = stack.filter(s => s.head.startsWith('@')).map(s => s.head).join(' ');
          rules.push({ start: top.open + 1, end: i, selector: top.head, media });
        }
      }
      selStart = i + 1;
    } else if (c === ';' && stack.length === 0) selStart = i + 1;
    i++;
  }
})();
const PROPS = ['color','background-color','background-image','font-family','font-size','font-weight','line-height','letter-spacing','text-transform','text-decoration-line','text-align','display','position','padding-top','padding-right','padding-bottom','padding-left','margin-top','margin-right','margin-bottom','margin-left','border-top-width','border-right-width','border-bottom-width','border-left-width','border-top-color','border-bottom-color','border-radius','opacity','gap','flex-direction','grid-template-columns','width','max-width','height','box-shadow','flex-basis','overflow-x','transform'];
const base = process.argv[3] || 'http://localhost:8881';
const pages = ['/', '/over-ons/', '/contact/', '/lid-worden/', '/%F0%9F%87%AC%F0%9F%87%A7/', '/nieuws/', '/?s=test', '/404-nope/', '/?p=1', '/category/uncategorized/'];
const sizes = [[1440, 900], [390, 844]];
const browser = await chromium.launch({ channel: 'chrome' });
const unsafe = new Map(); // rule index -> reason
const matched = new Map();
const marker = css.slice(0, 120);
for (const [w, h] of sizes) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  const page = await ctx.newPage();
  for (const p of pages) {
    await page.goto(base + p, { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: '*{animation:none!important;transition:none!important}' });
    const res = await page.evaluate(({ css, rules, PROPS, marker }) => {
      const tag = [...document.querySelectorAll('style')].find(s => s.textContent.includes(marker.slice(0, 60)));
      if (!tag) return { error: 'style tag not found' };
      const full = tag.textContent;
      const off = full.indexOf(css.slice(0, 200));
      if (off < 0) return { error: 'css offset not found' };
      const snap = (els) => els.map(el => { const cs = getComputedStyle(el), r = el.getBoundingClientRect(); const o = PROPS.map(p => cs.getPropertyValue(p)).join('|'); return o + '|' + Math.round(r.width) + 'x' + Math.round(r.height); });
      const out = [];
      rules.forEach((r, idx) => {
        let els;
        const sel = r.selector.replace(/::?[a-z-]+(\([^)]*\))?/gi, m => /^:(hover|focus|focus-visible|active|not|is|where|has|first-child|last-child|nth-child|first-of-type|last-of-type|nth-of-type|only-child)/.test(m) ? m : '');
        try { els = [...document.querySelectorAll(sel.replace(/:(hover|focus-visible|focus|active)/g, ''))]; } catch (e) { out.push({ idx, n: -1 }); return; }
        const pseudo = /::/.test(r.selector);
        if (!els.length) { out.push({ idx, n: 0, pseudo }); return; }
        const before = snap(els);
        const body = css.slice(r.start, r.end);
        const nb = body.replace(/\s*!important/g, '');
        const text = css.slice(0, r.start) + nb + css.slice(r.end);
        tag.textContent = full.slice(0, off) + text + full.slice(off + css.length);
        const after = snap(els);
        tag.textContent = full;
        let changed = 0; for (let i = 0; i < before.length; i++) if (before[i] !== after[i]) changed++;
        out.push({ idx, n: els.length, changed, pseudo });
      });
      return { out };
    }, { css, rules, PROPS, marker });
    if (res.error) { console.error(p, res.error); continue; }
    for (const o of res.out) {
      const k = o.idx;
      const m = matched.get(k) || 0; matched.set(k, m + Math.max(o.n, 0));
      if (o.n === -1) unsafe.set(k, 'bad-selector');
      else if (o.changed > 0) unsafe.set(k, `changed ${o.changed}/${o.n} @${w} ${p}`);
      else if (o.pseudo && !unsafe.has(k)) unsafe.set(k, 'pseudo-unchecked');
    }
    console.error('done', w, p);
  }
  await ctx.close();
}
await browser.close();
const report = rules.map((r, k) => ({ k, selector: r.selector.replace(/\s+/g, ' ').slice(0, 90), media: r.media, start: r.start, end: r.end, matched: matched.get(k) || 0, verdict: unsafe.get(k) || ((matched.get(k) || 0) === 0 ? 'unmatched' : 'safe') }));
console.log(JSON.stringify(report));
