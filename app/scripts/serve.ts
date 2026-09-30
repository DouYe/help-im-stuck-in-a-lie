#!/usr/bin/env bun
// Vite-free dev/export server: bundles src/main.ts with Bun and serves it with the assets.
//   bun scripts/serve.ts [port]      (default 5173; rebuilds on every page load)
// Stands in for `bunx vite` where the npm registry is unreachable. Handles the two Vite-only
// features the engine uses: import.meta.glob (scene discovery) and import.meta.hot (live reload).
import path from 'node:path';
import { readdirSync, existsSync } from 'node:fs';
import type { BunPlugin } from 'bun';

const APP = path.resolve(import.meta.dir, '..');
const ROOT = path.resolve(APP, '..');
const port = +(process.argv[2] ?? 5173);

const viteShim: BunPlugin = {
  name: 'vite-shim',
  setup(b) {
    b.onLoad({ filter: /src[\\/](timeline|main)\.ts$/ }, async (args) => {
      let src = await Bun.file(args.path).text();
      // import.meta.glob('./scenes/*.ts') -> a static map of lazy imports
      src = src.replace(/import\.meta\.glob(?:<[^>]*>)?\(\s*'\.\/scenes\/\*\.ts'\s*\)/, () => {
        const files = readdirSync(path.join(APP, 'src/scenes')).filter((f) => f.endsWith('.ts'));
        return '{' + files.map((f) => `'./scenes/${f}': () => import('./scenes/${f}')`).join(',') + '}';
      });
      src = src.replace(/import\.meta\.hot/g, 'undefined');
      return { contents: src, loader: 'ts' };
    });
  },
};

async function build() {
  const r = await Bun.build({ entrypoints: [path.join(APP, 'src/main.ts'), path.join(APP, 'src/figtest.ts')], target: 'browser', format: 'esm', splitting: true, plugins: [viteShim], sourcemap: 'inline' });
  if (!r.success) { console.error(r.logs); throw new Error('build failed'); }
  const out = new Map<string, Blob>();
  for (const o of r.outputs) out.set('/dist/' + path.basename(o.path), o);
  return out;
}
let bundle = await build();

Bun.serve({
  port,
  async fetch(req) {
    const u = new URL(req.url);
    let p = decodeURIComponent(u.pathname);
    if (p === '/' || p === '/index.html') {
      bundle = await build();
      const html = (await Bun.file(path.join(APP, 'index.html')).text()).replace('/src/main.ts', '/dist/main.js');
      return new Response(html, { headers: { 'content-type': 'text/html' } });
    }
    if (p === '/figtest.html') {
      bundle = await build();
      return new Response('<!doctype html><html><body style="margin:0;background:#000"><canvas id="c" style="width:1920px;height:1080px"></canvas><script type="module" src="/dist/figtest.js"></script></body></html>', { headers: { 'content-type': 'text/html' } });
    }
    if (bundle.has(p)) return new Response(bundle.get(p)!, { headers: { 'content-type': 'text/javascript' } });
    const base = /^\/(audio|data)\//.test(p) ? ROOT : path.join(APP, 'public');
    const f = path.join(base, p);
    if (f.startsWith(base) && existsSync(f)) return new Response(Bun.file(f));
    return new Response('not found', { status: 404 });
  },
});
console.log(`serving on http://localhost:${port}`);
