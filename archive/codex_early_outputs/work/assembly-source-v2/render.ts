#!/usr/bin/env bun
// Deterministic Canvas2D export: draw at song-relative time, send RGBA frames
// from headless Chrome over a local WebSocket, and mux the audio with FFmpeg.
import { chromium } from 'playwright-core';
import { existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = import.meta.dir;
const WIDTH = 1920, HEIGHT = 1080;
const argv = process.argv.slice(2);
const value = (key: string, fallback: string) => {
  const i = argv.indexOf(`--${key}`);
  return i >= 0 ? argv[i + 1] ?? fallback : fallback;
};
const FPS = +value('fps', '60');
const FROM = +value('from', '0');
const DURATION = +value('duration', '20');
const FRAMES = Math.round(FPS * DURATION);
const OUT = path.resolve(value('out', path.join(ROOT, 'assembly-line-heart-47-67.mp4')));
const AUDIO = path.resolve(value('audio', path.join(ROOT, 'audio_47_67.flac')));
const STILL = argv.includes('--still');
const STILLS = argv.includes('--stills');
const STILL_T = +value('t', '0');

const staticServer = Bun.serve({
  hostname: '127.0.0.1',
  port: 0,
  async fetch(req) {
    const url = new URL(req.url);
    const relative = decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname);
    const filePath = path.resolve(ROOT, `.${relative}`);
    if (!filePath.startsWith(ROOT + path.sep) || !existsSync(filePath)) return new Response('Not found', { status: 404 });
    return new Response(Bun.file(filePath));
  },
});

const browser = await chromium.launch({
  channel: 'chrome',
  headless: true,
  args: ['--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows'],
});
const page = await browser.newPage({ viewport: { width: WIDTH, height: HEIGHT }, deviceScaleFactor: 1 });
page.setDefaultTimeout(120000);
const logs: string[] = [];
page.on('console', (m) => { if (m.type() === 'error') logs.push(m.text()); });
page.on('pageerror', (e) => logs.push(e.message));

try {
  await page.goto(`http://127.0.0.1:${staticServer.port}/`, { waitUntil: 'load' });
  await page.waitForFunction(() => (window as any).ready === true, null, { timeout: 120000 });
  if (STILLS) {
    const times = value('times', '0').split(',').map(Number);
    mkdirSync(OUT, { recursive: true });
    for (const t of times) {
      await page.evaluate((time) => (window as any).drawAt(time), t);
      const file = path.join(OUT, `frame_${t.toFixed(3)}.png`);
      await page.locator('#stage').screenshot({ path: file });
      console.log(file);
    }
  } else if (STILL) {
    await page.evaluate((t) => (window as any).drawAt(t), STILL_T);
    mkdirSync(path.dirname(OUT), { recursive: true });
    await page.locator('#stage').screenshot({ path: OUT });
    console.log(`wrote still ${OUT} at t=${STILL_T}`);
  } else {
    if (!existsSync(AUDIO)) throw new Error(`Audio file missing: ${AUDIO}`);
    mkdirSync(path.dirname(OUT), { recursive: true });
    const ff = Bun.spawn([
      'ffmpeg', '-y', '-v', 'error',
      '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', `${WIDTH}x${HEIGHT}`, '-r', String(FPS), '-i', 'pipe:0',
      '-ss', String(FROM), '-t', String(DURATION), '-i', AUDIO,
      '-vf', 'scale=out_color_matrix=bt709,setparams=color_primaries=bt709:color_trc=bt709',
      '-c:v', 'libx264', '-preset', value('preset', 'fast'), '-crf', value('crf', '18'),
      '-pix_fmt', 'yuv420p', '-tune', 'grain',
      '-c:a', 'aac', '-b:a', '320k', '-t', String(DURATION), '-movflags', '+faststart', OUT,
    ], { stdin: 'pipe', stdout: 'inherit', stderr: 'inherit' });
    let received = 0;
    const started = performance.now();
    const frameServer = Bun.serve({
      hostname: '127.0.0.1',
      port: 0,
      fetch(req, srv) { return srv.upgrade(req) ? undefined : new Response('WebSocket only', { status: 400 }); },
      websocket: {
        maxPayloadLength: WIDTH * HEIGHT * 4 + 1024,
        async message(ws, message) {
          ff.stdin.write(message as Uint8Array);
          await ff.stdin.flush();
          received++;
          ws.send(String(received));
          if (received % 60 === 0 || received === FRAMES) {
            const elapsed = (performance.now() - started) / 1000;
            process.stdout.write(`\r${received}/${FRAMES} frames; ${(received / elapsed).toFixed(1)} fps; ETA ${((FRAMES - received) * elapsed / received).toFixed(0)}s  `);
          }
        },
      },
    });
    try {
      await page.evaluate(async ({ fps, frames, from, wsUrl }) => {
        const socket = new WebSocket(wsUrl);
        socket.binaryType = 'arraybuffer';
        let acked = 0;
        socket.onmessage = (e) => { acked = Math.max(acked, Number(e.data) || 0); };
        await new Promise<void>((resolve, reject) => {
          socket.onopen = () => resolve();
          socket.onerror = () => reject(new Error('Frame WebSocket failed'));
        });
        const canvas = document.getElementById('stage') as HTMLCanvasElement;
        const ctx = canvas.getContext('2d', { willReadFrequently: true })!;
        for (let n = 0; n < frames; n++) {
          (window as any).drawAt(from + n / fps);
          const rgba = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
          while (n - acked >= 3 || socket.bufferedAmount > 32 * 1024 * 1024) {
            await new Promise((resolve) => setTimeout(resolve, 2));
          }
          socket.send(rgba);
          if (n % 30 === 0) await new Promise((resolve) => setTimeout(resolve, 0));
        }
        while (socket.bufferedAmount) await new Promise((resolve) => setTimeout(resolve, 5));
        socket.close();
      }, { fps: FPS, frames: FRAMES, from: FROM, wsUrl: `ws://127.0.0.1:${frameServer.port}` });
      while (received < FRAMES) await Bun.sleep(20);
      ff.stdin.end();
      const code = await ff.exited;
      if (code !== 0) throw new Error(`FFmpeg exited ${code}`);
      console.log(`\nwrote ${OUT} (${FRAMES} frames in ${((performance.now() - started) / 1000).toFixed(1)}s)`);
    } finally {
      frameServer.stop();
      if (ff.exitCode === null) ff.kill();
    }
  }
  if (logs.length) console.error('Browser diagnostics:\n' + logs.slice(0, 20).join('\n'));
} finally {
  await browser.close();
  staticServer.stop();
}
