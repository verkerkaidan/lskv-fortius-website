// Screenshots for the README: faceless, no admin bar (logged-out), crisp (2x).
// Usage: node tools/readme-shots.mjs https://lskvfortius.nl out-dir
import { chromium } from 'playwright-core';
import fs from 'fs';

const [, , base = 'https://lskvfortius.nl', out = 'screenshots-raw'] = process.argv;
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ channel: 'chrome' });
const still = '*{animation:none!important;transition:none!important}';

async function open(ctx, path) {
  const page = await ctx.newPage();
  await page.goto(base + path, { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: still });
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(400);
  return page;
}

// Desktop
const desktop = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
let page = await open(desktop, '/merch/');
await page.screenshot({ path: `${out}/merch-page.png`, clip: { x: 0, y: 0, width: 1440, height: 1280 } });

// Colour selector: the cuffed joggingbroek card in both colour states
const card = page.locator('.fortius-merch-card', { hasText: 'Cuffed' });
for (const [i, name] of [[0, 'zwart'], [1, 'donkergrijs']]) {
  await card.locator('.fortius-merch-color').nth(i).click();
  await page.mouse.move(5, 5);
  const r = await card.evaluate(e => { const b = e.getBoundingClientRect(); return { x: b.left, y: b.top + scrollY, w: b.width, h: b.height }; });
  await page.screenshot({ path: `${out}/colour-${name}.png`, fullPage: true, clip: { x: r.x - 20, y: r.y - 20, width: r.w + 40, height: r.h + 40 } });
}

// Navigation dropdown
await page.evaluate(() => window.scrollTo(0, 0));
await page.locator('.wp-block-navigation-submenu').first().hover();
await page.waitForTimeout(300);
await page.screenshot({ path: `${out}/nav-dropdown.png`, clip: { x: 0, y: 0, width: 1440, height: 320 } });

// Section variants (one element screenshot each)
const sections = [['home', '/', 3, 'section-quotes'], ['home', '/', 4, 'section-red'], ['over-ons', '/over-ons/', 2, 'section-values'], ['home', '/', 5, 'section-logos'], ['commissies', '/commissies/', 3, 'section-text-only']];
for (const [, path, idx, name] of sections) {
  const p = await open(desktop, path);
  const els = [];
  for (const s of await p.$$('main .wp-block-group.alignfull, main .fortius-hero')) {
    const b = await s.boundingBox();
    if (b && b.height >= 120) els.push(s);
  }
  await els[idx].screenshot({ path: `${out}/${name}.png` });
  await p.close();
}

// Mobile
const mobile = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
page = await open(mobile, '/merch/');
await page.screenshot({ path: `${out}/mobile-merch.png`, clip: { x: 0, y: 0, width: 390, height: 844 } });
await page.evaluate(() => window.scrollTo(0, 0));
await page.locator('.wp-block-navigation__responsive-container-open').first().click();
await page.waitForTimeout(500);
await page.evaluate(() => document.activeElement && document.activeElement.blur());
await page.screenshot({ path: `${out}/mobile-menu.png`, clip: { x: 0, y: 0, width: 390, height: 844 } });
await browser.close();
console.log('done');
