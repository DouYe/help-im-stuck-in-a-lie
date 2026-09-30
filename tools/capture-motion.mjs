import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { projectRoot, width, height, duration, parseArgs, checkOptions, numeric, audioPath, browserLaunchOptions, startServer } from './motion-common.mjs';

const mode = process.argv[2] || 'audit';
const options = parseArgs(process.argv.slice(mode.startsWith('--') ? 2 : 3));
checkOptions(options, ['help', 'silent', 'out', 'audio', 'audio-start', 'chrome', 'channel', 'ffmpeg', 'ffprobe', 'fps', 'duration']);
if (options.help || mode === '--help') {
  console.log(`node tools/capture-motion.mjs audit --out wip/YOUR_MODEL/audit_v1 [--chrome PATH | --channel chrome]
node tools/capture-motion.mjs render --out renders/NEW_NAME.mp4 [--audio audio/current/song.mp3 --audio-start 0 | --silent]
Optional: --ffmpeg PATH --ffprobe PATH --fps 60 --duration 20. Duration may be shorter for a smoke capture; the motion timeline remains 20s.
Install root dependencies with npm ci. Chrome/Edge is discovered on Windows, macOS and Linux; CHROME_PATH is supported.`);
} else {
  if (!['audit', 'render'].includes(mode)) throw new Error('Mode must be audit or render');
  const fps = numeric(options.fps, 60, 'fps', 1, 120);
  const seconds = numeric(options.duration, duration, 'duration', 1 / fps, duration);
  const total = Math.round(seconds * fps);
  const output = path.resolve(projectRoot, options.out || (mode === 'audit' ? 'wip/codex/portable_motion_audit_v1' : 'renders/portable_six_worlds_v1.mp4'));
  if (fs.existsSync(output)) throw new Error(`Output already exists; choose a new versioned name: ${output}`);
  if (mode === 'render' && path.extname(output).toLowerCase() !== '.mp4') throw new Error('--out must name an .mp4 file');
  const report = mode === 'audit' ? path.join(output, 'motion_audit.json') : output + '.audit.json';
  if (fs.existsSync(report)) throw new Error(`Audit already exists; choose a new versioned name: ${report}`);
  const audio = audioPath(options), audioStart = numeric(options['audio-start'], 0, 'audio-start');
  if (mode === 'render' && !options.silent && !fs.existsSync(audio)) throw new Error(`Replacement audio missing: ${audio}. Supply --audio PATH or explicitly use --silent.`);
  if (mode === 'render' && !options.silent) {
    const ffmpeg = options.ffmpeg || process.env.FFMPEG_PATH;
    const ffprobe = options.ffprobe || process.env.FFPROBE_PATH || (ffmpeg && path.dirname(ffmpeg) !== '.' ? path.join(path.dirname(ffmpeg), process.platform === 'win32' ? 'ffprobe.exe' : 'ffprobe') : 'ffprobe');
    const probe = spawnSync(ffprobe, ['-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=duration:format=duration', '-of', 'json', audio], { encoding: 'utf8', windowsHide: true });
    if (probe.error || probe.status !== 0) throw new Error(`Audio probe failed; install FFprobe or pass --ffprobe PATH. ${probe.error?.message || probe.stderr}`);
    const metadata = JSON.parse(probe.stdout);
    const audioLength = Number(metadata.streams?.[0]?.duration || metadata.format?.duration);
    if (!metadata.streams?.length || !Number.isFinite(audioLength) || audioLength + .025 < audioStart + total / fps) throw new Error(`Selected audio does not contain the complete ${total / fps}s excerpt at ${audioStart}s (length ${audioLength}s).`);
  }
  const require = createRequire(import.meta.url);
  let chromium;
  try { ({ chromium } = require('playwright-core')); }
  catch { throw new Error('Install capture dependency at repository root: npm ci'); }
  let encoder = null, encoderDone, stderr = '', frameCount = 0, browser = null;
  const service = await startServer({
    onFrame: async bytes => {
      if (!encoder || encoder.stdin.destroyed) throw new Error('Encoder is not accepting frames');
      await new Promise((resolve, reject) => encoder.stdin.write(bytes, error => error ? reject(error) : resolve()));
      frameCount++;
    },
    onProgress: () => console.log(`Rendered ${frameCount}/${total} frames`),
  });
  try {
    try {
      browser = await chromium.launch({ ...browserLaunchOptions(options), headless: true, args: ['--disable-lcd-text', '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows'] });
    } catch (error) { throw new Error(`Browser launch failed. Install Chrome/Edge, pass --chrome PATH, or run npx playwright-core install chromium. ${error.message}`); }
    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
    const errors = []; page.on('pageerror', error => errors.push(String(error)));
    await page.goto(service.url + '?render=1');
    await page.evaluate(() => document.fonts.ready);
    await page.waitForFunction(() => window.demo?.ready);
    const audit = await page.evaluate(() => {
      demo.reset('auto'); const samples = [];
      for (let f = 0; f <= 1200; f++) {
        demo.renderAt(f / 60);
        if (f % 6 === 0) { const state = demo.state(); samples.push({ t: state.time, scene: state.scene, x: state.p.x, y: state.p.y, shots: state.shots.length, dead: state.p.dead }); }
      }
      return { events: demo.events(), samples, state: demo.state(), physicsHz: demo.physicsHz, layers: demo.layerDepths, hazardsPerSecond: demo.hazardsPerSecond };
    });
    audit.capture = { source: 'wip/codex/platformer_motion_v2', width, height, fps, frames: total, duration: total / fps, audio: mode === 'render' && !options.silent ? path.relative(projectRoot, audio).replaceAll(path.sep, '/') : null, audioStart: options.silent ? null : audioStart, browserVersion: browser.version(), nodeVersion: process.version };
    await fsp.mkdir(mode === 'audit' ? output : path.dirname(output), { recursive: true });
    if (mode === 'audit') {
      await page.evaluate(() => demo.reset('auto'));
      for (const t of [1.5, 2.8, 4.8, 5.9, 8, 9.1, 11.5, 13.1, 15.2, 16.1, 18.5, 19.5]) {
        const png = await page.evaluate(t => { demo.renderAt(t); return document.getElementById('screen').toDataURL('image/png').split(',')[1]; }, t);
        await fsp.writeFile(path.join(output, `frame_${t.toFixed(1)}.png`), Buffer.from(png, 'base64'), { flag: 'wx' });
      }
    } else {
      const args = ['-hide_banner', '-loglevel', 'warning', '-n', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', `${width}x${height}`, '-r', String(fps), '-i', 'pipe:0'];
      if (!options.silent) args.push('-ss', String(audioStart), '-i', audio, '-map', '0:v:0', '-map', '1:a:0');
      else args.push('-map', '0:v:0', '-an');
      args.push('-vf', 'scale=out_color_matrix=bt709,setparams=color_primaries=bt709:color_trc=bt709', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p');
      if (!options.silent) args.push('-c:a', 'aac', '-b:a', '320k');
      args.push('-t', String(total / fps), '-movflags', '+faststart', output);
      encoder = spawn(options.ffmpeg || process.env.FFMPEG_PATH || 'ffmpeg', args, { windowsHide: true, stdio: ['pipe', 'ignore', 'pipe'] });
      encoder.stdin.on('error', error => { stderr = (stderr + '\n' + error.message).slice(-6000); });
      encoder.stderr.on('data', chunk => { stderr = (stderr + chunk).slice(-6000); });
      encoderDone = new Promise((resolve, reject) => {
        encoder.once('error', reject);
        encoder.once('close', code => code === 0 ? resolve() : reject(new Error(`FFmpeg exited ${code}: ${stderr}`)));
      });
      encoderDone.catch(() => {}); // Preserve failure for await; avoid an unhandled rejection while frames are in flight.
      await page.evaluate(async ({ fps, total, width, height }) => {
        demo.reset('auto'); const context = document.getElementById('screen').getContext('2d');
        for (let frame = 0; frame < total; frame++) {
          demo.renderAt(frame / fps);
          const rgba = context.getImageData(0, 0, width, height).data;
          const response = await fetch('/__frame', { method: 'POST', body: rgba });
          if (!response.ok) throw new Error(await response.text());
          if (frame % 180 === 179) await fetch('/__progress');
        }
      }, { fps, total, width, height });
      encoder.stdin.end(); await encoderDone;
    }
    if (errors.length) throw new Error(`Browser errors: ${errors.join('\n')}`);
    await fsp.writeFile(report, JSON.stringify(audit, null, 2) + '\n', { flag: 'wx' });
    const counts = {}; for (const event of audit.events) counts[event.kind] = (counts[event.kind] || 0) + 1;
    console.log(JSON.stringify({ output, report, counts, layers: audit.layers, peakShots: Math.max(...audit.samples.map(sample => sample.shots)) }, null, 2));
  } finally {
    if (encoder && encoder.exitCode === null) encoder.kill();
    if (browser) await browser.close();
    await service.close();
  }
}
