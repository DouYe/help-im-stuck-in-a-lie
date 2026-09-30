import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';

// Read-only integrated-engine QA. This runs a private headless browser and only
// writes the sibling JSON report. No game hooks are replaced or patched.
const require = createRequire(import.meta.url);
const {chromium} = require('C:/Users/honkw/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core');
const folder = path.dirname(fileURLToPath(import.meta.url));
const errors = [];
const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    const relative = decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname);
    const target = path.resolve(folder, '.' + relative);
    if (!target.startsWith(folder + path.sep)) throw new Error('Outside QA source folder');
    const content = await fs.readFile(target);
    res.setHeader('Content-Type', target.endsWith('.js') ? 'text/javascript' : target.endsWith('.html') ? 'text/html' : 'application/octet-stream');
    res.end(content);
  } catch (error) { res.statusCode = 500; res.end(String(error)); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const browser = await chromium.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true,
  args: ['--disable-background-timer-throttling', '--disable-renderer-backgrounding']
});
try {
  const page = await browser.newPage({viewport: {width: 1920, height: 1080}, deviceScaleFactor: 1});
  page.on('pageerror', error => errors.push(String(error)));
  await page.goto(`http://127.0.0.1:${server.address().port}/?render=1`);
  await page.waitForFunction(() => window.demo?.ready);
  const report = await page.evaluate(() => {
    const checks = [], samples = [];
    const keys = ['ArrowRight','ArrowLeft','ArrowUp','ArrowDown','KeyW','KeyA','KeyS','KeyD','Space','KeyX','ShiftLeft','ShiftRight'];
    const key = (code, down) => dispatchEvent(new KeyboardEvent(down ? 'keydown' : 'keyup', {code, key: code, bubbles: true}));
    const release = () => keys.forEach(code => key(code, false));
    const setup = scene => { release(); demo.reset('manual', scene); };
    const step = (n = 1) => demo.renderAt(demo.state().time + n / 120 + 1e-8);
    const state = () => demo.state();
    const check = (name, passed, detail) => checks.push({name, passed: !!passed, detail});
    const near = (a, b, tolerance = 1e-5) => Math.abs(a - b) < tolerance;
    const snap = label => { const s = state(); samples.push({label, scene: s.scene, time: s.time, p: s.p, shots: s.shots.length}); return s; };

    setup(0);
    const x0 = state().p.x;
    key('ArrowRight', true); step(); const start = snap('factory snap start');
    check('One-step instant horizontal start', near(start.p.vx, 1320) && near(start.p.x - x0, 11), {vx: start.p.vx, displacement: start.p.x - x0});
    key('ArrowRight', false); key('ArrowLeft', true); step(); const reverse = snap('factory snap reversal');
    check('One-step instant reversal', near(reverse.p.vx, -1320) && near(reverse.p.x, x0), {vx: reverse.p.vx, x: reverse.p.x});
    key('ArrowLeft', false); const stopX = state().p.x; step(); const stop = snap('factory snap stop');
    check('One-step instant stop', stop.p.vx === 0 && near(stop.p.x, stopX), {vx: stop.p.vx, displacement: stop.p.x - stopX});

    setup(0); key('Space', true); step(); const first = snap('first jump');
    check('First jump launch', first.p.jumps === 1 && first.p.vy < -1400 && !first.p.grounded, {jumps: first.p.jumps, vy: first.p.vy});
    key('Space', false); step(); key('Space', true); step(); const second = snap('second jump');
    check('Second jump launches in air', second.p.jumps === 2 && second.p.vy < -1250 && demo.events().filter(e => e.kind === 'double-jump').length === 1, {jumps: second.p.jumps, vy: second.p.vy, events: demo.events()});
    key('Space', false); step(); key('Space', true); step(); const third = snap('blocked third jump');
    check('Third jump blocked', third.p.jumps === 2 && demo.events().filter(e => ['jump','double-jump'].includes(e.kind)).length === 2, {jumps: third.p.jumps, events: demo.events()});

    setup(0); key('ArrowRight', true); key('Space', true); step(); key('Space', false); key('KeyX', true); step(); const dash = snap('air dash');
    check('Dash launches at 2850 px/s', near(dash.p.vx, 2850) && dash.p.dashing === 1 && dash.p.dashAvailable === 0 && dash.p.dashTime > 0, {vx: dash.p.vx, vy: dash.p.vy, dashTime: dash.p.dashTime});
    key('KeyX', false); step(); key('KeyX', true); step();
    check('No repeated air dash during cooldown', demo.events().filter(e => e.kind === 'dash').length === 1, {events: demo.events()});
    release(); step(16); const afterDash = snap('dash released');
    check('Dash returns to normal motion', afterDash.p.dashTime <= 0 && afterDash.p.vx === 0 && afterDash.p.vy > 0, {dashTime: afterDash.p.dashTime, vx: afterDash.p.vx, vy: afterDash.p.vy});

    for (const scene of [2, 3]) {
      const speed = scene === 2 ? 1120 : 1220;
      for (const [code, expectedX, expectedY] of [['ArrowRight', speed, 0], ['ArrowLeft', -speed, 0], ['ArrowUp', 0, -speed], ['ArrowDown', 0, speed]]) {
        setup(scene); key(code, true); step(); const move = snap(`${scene === 2 ? 'water' : 'topdown'} ${code}`);
        check(`${move.scene} ${code}: one-step four-axis movement`, near(move.p.vx, expectedX) && near(move.p.vy, expectedY), {vx: move.p.vx, vy: move.p.vy});
        release(); const beforeStop = state().p; step(); const stopped = state().p;
        check(`${move.scene} ${code}: instant stop`, stopped.vx === 0 && stopped.vy === 0 && near(stopped.x, beforeStop.x) && near(stopped.y, beforeStop.y), {vx: stopped.vx, vy: stopped.vy});
      }
      setup(scene); key('ArrowRight', true); key('ArrowUp', true); step(); const diagonal = snap(`${scene === 2 ? 'water' : 'topdown'} diagonal`);
      check(`${diagonal.scene}: normalized diagonal speed`, near(Math.hypot(diagonal.p.vx, diagonal.p.vy), speed), {vx: diagonal.p.vx, vy: diagonal.p.vy, magnitude: Math.hypot(diagonal.p.vx, diagonal.p.vy)});
      key('KeyX', true); step(); const diagonalDash = snap(`${diagonal.scene} diagonal dash`);
      check(`${diagonal.scene}: four-axis dash`, diagonalDash.p.vx > 0 && diagonalDash.p.vy < 0 && near(Math.hypot(diagonalDash.p.vx, diagonalDash.p.vy), 2850), {vx: diagonalDash.p.vx, vy: diagonalDash.p.vy});
    }

    setup(3); key('Space', true); step(); const topJump = snap('topdown first jump');
    key('Space', false); step(); key('Space', true); step(); const topDouble = snap('topdown second jump');
    check('Topdown jump elevation and double jump', topJump.p.z > 0 && topDouble.p.z > topJump.p.z && topDouble.p.jumps === 2, {firstZ: topJump.p.z, secondZ: topDouble.p.z, jumps: topDouble.p.jumps});

    release(); demo.reset('auto');
    const film = [];
    for (let frame = 0; frame <= 240; frame++) {
      demo.renderAt(frame / 12);
      const s = state();
      const numeric = ['x','y','vx','vy','runPhase','dashing'].every(k => Number.isFinite(s.p[k])) && ['x','y','zoom'].every(k => Number.isFinite(s.cam[k]));
      if (!numeric) checks.push({name: `Finite film state at ${s.time}`, passed: false, detail: s});
      film.push({time: s.time, scene: s.scene, localTime: s.localTime, x: s.p.x, y: s.p.y, vx: s.p.vx, vy: s.p.vy, dead: s.p.dead, dashing: s.p.dashing, shots: s.shots.length, projectedX: 960 + (s.p.x - s.cam.x) * s.cam.zoom, projectedY: 570 + (s.p.y - s.cam.y) * s.cam.zoom});
    }
    const events = demo.events();
    check('All six direct-cut worlds visited', new Set(film.map(s => s.scene)).size === 6, {scenes: [...new Set(film.map(s => s.scene))]});
    const offscreen = film.filter(s => !s.dead && (s.projectedX < 50 || s.projectedX > 1870 || s.projectedY < 40 || s.projectedY > 1130));
    check('Alive heroine kept in film frame', offscreen.length === 0, {offscreen});
    return {checks, samples, film, events, summary: {passed: checks.every(c => c.passed), checks: checks.length, failures: checks.filter(c => !c.passed), deaths: events.filter(e => e.kind === 'death').length, respawns: events.filter(e => e.kind === 'respawn').length, dodges: events.filter(e => e.kind === 'dodge').length}};
  });
  report.pageErrors = errors;
  report.summary.passed &&= errors.length === 0;
  report.generatedAt = new Date().toISOString();
  report.scope = 'Private Chromium read-only manual controls and deterministic six-world film; music-video difficulty accepted.';
  await fs.writeFile(path.join(folder, 'control-qa-v2.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({summary: report.summary, pageErrors: errors}));
} finally { await browser.close(); await new Promise(resolve => server.close(resolve)); }
