import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import os from 'node:os';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

export const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const sourceRoot = path.join(projectRoot, 'wip', 'codex', 'platformer_motion_v2');
export const width = 1920, height = 1080, duration = 20;

export function parseArgs(argv) {
  const options = {};
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (!key.startsWith('--')) throw new Error(`Unexpected argument: ${key}`);
    if (['--help', '--silent'].includes(key)) options[key.slice(2)] = true;
    else {
      if (!argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error(`Missing value for ${key}`);
      options[key.slice(2)] = argv[++i];
    }
  }
  return options;
}

export function checkOptions(options, allowed) {
  for (const key of Object.keys(options)) if (!allowed.includes(key)) throw new Error(`Unknown option: --${key}`);
}

export function numeric(value, fallback, name, min = 0, max = Infinity) {
  const number = value === undefined ? fallback : Number(value);
  if (!Number.isFinite(number) || number < min || number > max) throw new Error(`--${name} must be between ${min} and ${max}`);
  return number;
}

export function audioPath(options) {
  return path.resolve(projectRoot, options.audio || 'audio/current/song.mp3');
}

export async function runCommand(command, args) {
  const child = spawn(command, args, { windowsHide: true, stdio: ['ignore', 'ignore', 'pipe'] });
  let stderr = '';
  child.stderr.on('data', chunk => { stderr = (stderr + chunk).slice(-6000); });
  await new Promise((resolve, reject) => {
    child.once('error', reject);
    child.once('close', code => code === 0 ? resolve() : reject(new Error(`${command} exited ${code}: ${stderr}`)));
  });
}

export async function previewAudio(options) {
  const source = audioPath(options);
  if (options.silent || !fs.existsSync(source)) {
    if (!options.silent && options.audio) throw new Error(`Audio not found: ${source}`);
    return { path: null, cleanup: async () => {} };
  }
  const start = numeric(options['audio-start'], 0, 'audio-start');
  if (!start) return { path: source, cleanup: async () => {} };
  const temp = await fsp.mkdtemp(path.join(os.tmpdir(), 'heart-preview-'));
  const output = path.join(temp, 'preview.mp3');
  try {
    await runCommand(options.ffmpeg || process.env.FFMPEG_PATH || 'ffmpeg', [
      '-hide_banner', '-loglevel', 'error', '-ss', String(start), '-i', source,
      '-map', '0:a:0', '-t', String(duration), '-vn', '-c:a', 'libmp3lame', '-q:a', '2', output,
    ]);
  } catch (error) {
    await fsp.rm(temp, { recursive: true, force: true });
    throw error;
  }
  return { path: output, cleanup: () => fsp.rm(temp, { recursive: true, force: true }) };
}

const contentTypes = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json', '.mp3': 'audio/mpeg', '.wav': 'audio/wav',
  '.flac': 'audio/flac', '.png': 'image/png', '.jpg': 'image/jpeg',
};

async function serveFile(req, res, target) {
  const stat = await fsp.stat(target);
  if (!stat.isFile()) { res.writeHead(404).end('File not found'); return; }
  let start = 0, end = stat.size - 1, status = 200;
  if (req.headers.range) {
    const match = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
    if (!match || (!match[1] && !match[2])) { res.writeHead(416).end(); return; }
    if (!match[1]) start = Math.max(0, stat.size - Number(match[2]));
    else start = Number(match[1]);
    if (match[1] && match[2]) end = Math.min(end, Number(match[2]));
    if (start > end || start >= stat.size) {
      res.writeHead(416, { 'Content-Range': `bytes */${stat.size}` }).end(); return;
    }
    status = 206;
    res.setHeader('Content-Range', `bytes ${start}-${end}/${stat.size}`);
  }
  res.writeHead(status, {
    'Content-Type': contentTypes[path.extname(target).toLowerCase()] || 'application/octet-stream',
    'Content-Length': end - start + 1,
    'Accept-Ranges': 'bytes',
    'Cache-Control': 'no-store',
  });
  if (req.method === 'HEAD') { res.end(); return; }
  const stream = fs.createReadStream(target, { start, end });
  stream.on('error', () => res.destroy());
  stream.pipe(res);
}

export async function startServer({ port = 0, audio = null, onFrame = null, onProgress = null } = {}) {
  const server = http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url, 'http://localhost');
      if (url.pathname === '/__frame' && req.method === 'POST' && onFrame) {
        const expected = width * height * 4;
        const chunks = []; let size = 0;
        for await (const chunk of req) {
          size += chunk.length;
          if (size > expected) throw new Error('RGBA frame exceeds expected size');
          chunks.push(chunk);
        }
        if (size !== expected) throw new Error(`Wrong RGBA size: ${size}`);
        await onFrame(Buffer.concat(chunks, size));
        res.end('ok'); return;
      }
      if (url.pathname === '/__progress' && onProgress) { onProgress(); res.end('ok'); return; }
      if (!['GET', 'HEAD'].includes(req.method)) { res.writeHead(405).end(); return; }
      const pathname = decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname);
      if (pathname === '/preview_audio.mp3') {
        if (!audio) { res.writeHead(404).end('Replacement audio pending; preview is silent.'); return; }
        await serveFile(req, res, audio); return;
      }
      const target = path.resolve(sourceRoot, '.' + pathname);
      const relative = path.relative(sourceRoot, target);
      if (relative.startsWith('..') || path.isAbsolute(relative)) { res.writeHead(403).end(); return; }
      await serveFile(req, res, target);
    } catch (error) {
      if (!res.headersSent) res.writeHead(error.code === 'ENOENT' ? 404 : 500);
      res.end(String(error.message));
    }
  });
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(port, '127.0.0.1', resolve);
  });
  return { server, url: `http://127.0.0.1:${server.address().port}/`, close: () => new Promise(resolve => server.close(resolve)) };
}

function existingExecutable(candidate) {
  try { return fs.statSync(candidate).isFile(); } catch { return false; }
}

function onPath(name) {
  const probe = spawnSync(process.platform === 'win32' ? 'where.exe' : 'which', [name], { encoding: 'utf8', windowsHide: true });
  if (probe.status !== 0) return null;
  return probe.stdout.split(/\r?\n/).find(existingExecutable) || null;
}

export function browserLaunchOptions(options) {
  const selected = options.chrome || process.env.CHROME_PATH || process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
  if (selected) {
    const executablePath = path.resolve(selected);
    if (!existingExecutable(executablePath)) throw new Error(`Browser executable not found: ${executablePath}`);
    return { executablePath };
  }
  if (options.channel) return { channel: options.channel };
  let candidates;
  if (process.platform === 'win32') {
    candidates = [process.env.PROGRAMFILES, process.env['PROGRAMFILES(X86)'], process.env.LOCALAPPDATA]
      .filter(Boolean).flatMap(base => [path.join(base, 'Google/Chrome/Application/chrome.exe'), path.join(base, 'Microsoft/Edge/Application/msedge.exe')]);
  } else if (process.platform === 'darwin') {
    candidates = [
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
      path.join(os.homedir(), 'Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
    ];
  } else candidates = ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/opt/google/chrome/chrome'];
  const executablePath = candidates.find(existingExecutable) || ['google-chrome', 'chromium', 'chromium-browser', 'chrome', 'msedge'].map(onPath).find(Boolean);
  return executablePath ? { executablePath } : {}; // Falls back to an explicitly installed Playwright Chromium.
}
