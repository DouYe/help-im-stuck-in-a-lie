// Screenshot the figure debug page: bun scripts/figshot.ts out.png [query]
import { chromium } from 'playwright-core';
const out = process.argv[2] ?? '../out/wip/fig.png', q = process.argv[3] ?? '';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on('pageerror', (e) => console.log('pageerror', e.message));
await p.goto(`http://localhost:5190/figtest.html?${q}`);
await p.waitForFunction(() => (window as any).__done, null, { timeout: 60000 });
console.log('glyphs', await p.evaluate(() => (window as any).__done));
await p.screenshot({ path: out });
await b.close();
