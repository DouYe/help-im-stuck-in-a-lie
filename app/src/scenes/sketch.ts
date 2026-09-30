// SHOT — 'sketch' (graphite on paper, then ink). One idea: the sketch becomes real.
// The line's first words are roughed in with a pencil as they're sung — loose, overshooting, boiling
// strokes over construction guides. The key word (default: one that says REAL) is inked solid on its
// syllable. The words after it are written by hand in orange brush pen, stroke by stroke, as sung.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { rgba } from '../engine/palette';
import { F, font, measure, textPathCommands } from '../engine/type';
import { strokeText, drawStrokeText, writtenLength, type StrokeText } from '../engine/stroke';
import { clamp, ease, hash, noise1 } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { wordText } from '../danmaku/kinetic';
import type { Word } from '../engine/lyrics';
import { CLEAN } from './poster';

type Poly = { x: number; y: number }[];

/** Flatten opentype path commands into closed polylines. */
function contours(cmds: any[]): Poly[] {
  const out: Poly[] = []; let cur: Poly = []; let px = 0, py = 0, sx = 0, sy = 0;
  for (const c of cmds) {
    if (c.type === 'M') { if (cur.length) out.push(cur); cur = [{ x: c.x, y: c.y }]; px = sx = c.x; py = sy = c.y; }
    else if (c.type === 'L') { cur.push({ x: c.x, y: c.y }); px = c.x; py = c.y; }
    else if (c.type === 'Q') { for (let i = 1; i <= 8; i++) { const u = i / 8, v = 1 - u; cur.push({ x: v * v * px + 2 * v * u * c.x1 + u * u * c.x, y: v * v * py + 2 * v * u * c.y1 + u * u * c.y }); } px = c.x; py = c.y; }
    else if (c.type === 'C') { for (let i = 1; i <= 10; i++) { const u = i / 10, v = 1 - u; cur.push({ x: v * v * v * px + 3 * v * v * u * c.x1 + 3 * v * u * u * c.x2 + u * u * u * c.x, y: v * v * v * py + 3 * v * v * u * c.y1 + 3 * v * u * u * c.y2 + u * u * u * c.y }); } px = c.x; py = c.y; }
    else if (c.type === 'Z') { cur.push({ x: sx, y: sy }); out.push(cur); cur = []; }
  }
  if (cur.length) out.push(cur);
  return out;
}

export default class Sketch extends Mode {
  bg = new FSPass(/* glsl */ `
    void main() {
      vec2 p = FRAG_PX; p.y = ${H.toFixed(1)} - p.y;
      float tooth = snoise(p * 0.55) * 0.5 + snoise(p * 1.7) * 0.25;
      vec3 col = C_BONE * (0.965 + 0.022 * tooth);
      col *= 1.0 - 0.06 * smoothstep(0.55, 1.2, length((p - vec2(${(W / 2).toFixed(1)}, 540.0)) / vec2(1100.0, 700.0)));
      fragColor = vec4(col, 1.0);
    }`);
  L = new Layer2D();
  sketchWords: { w: Word; polys: Poly[]; path: Path2D; x: number; width: number; base: number; size: number }[] = [];
  ink: { w: Word; path: Path2D; x: number; width: number } | null = null;
  script: { st: StrokeText; x: number; y: number; times: [number, number][] } | null = null;
  guides: [number, number][] = [];   // [baseline, size] of each line

  init() {
    const ws = this.wordsIn();
    const fam = F.archivo(100, 900);
    const inkIdx = Math.max(0, ws.findIndex((w) => /real/i.test(w.w)));
    const head = ws.slice(0, inkIdx), key = ws[inkIdx], tail = ws.slice(inkIdx + 1);
    // two lines, flush left: the words before the key word, then the key word big (it gets inked)
    const t1 = head.map((w) => wordText(w.w)), kt = key ? wordText(key.w) : '';
    const w1 = (sz: number) => t1.reduce((a, s) => a + measure(s, fam, sz), 0) + sz * 0.28 * Math.max(0, t1.length - 1);
    const s1 = t1.length ? Math.min(230, (1250 / w1(100)) * 100) : 0;
    const s2 = kt ? Math.min(440, (1480 / measure(kt, fam, 100)) * 100) : 0;
    const cap1 = s1 * 0.72, cap2 = s2 * 0.72, gapY = t1.length ? 64 : 0;
    const blockW = Math.max(w1(s1), kt ? measure(kt, fam, s2) : 0);
    const x0 = W / 2 - blockW / 2;
    const top = (H - (cap1 + gapY + cap2 + 110)) / 2;
    const base1 = top + cap1, base2 = base1 + gapY + cap2;
    const add = (w: Word, txt: string, x: number, base: number, size: number, isKey: boolean) => {
      const polys = contours(textPathCommands(txt, fam, size, x, base));
      const path = new Path2D();
      for (const poly of polys) { path.moveTo(poly[0]!.x, poly[0]!.y); for (const q of poly) path.lineTo(q.x, q.y); path.closePath(); }
      const width = measure(txt, fam, size);
      if (isKey) this.ink = { w, path, x, width };
      this.sketchWords.push({ w, polys, path, x, width, base, size });
    };
    let x = x0;
    head.forEach((w, i) => { add(w, t1[i]!, x, base1, s1, false); x += measure(t1[i]!, fam, s1) + s1 * 0.28; });
    if (key) add(key, kt, x0 - s2 * 0.02, base2, s2, true);
    if (t1.length) this.guides.push([base1, s1]);
    if (key) this.guides.push([base2, s2]);
    if (tail.length) {
      const txt = tail.map((w) => w.w.replace(/[^\p{L}\p{N}'’ ]/gu, '')).join(' ').toLowerCase();
      const st = strokeText(txt, 'hscript', 210);
      // char times from word times (the space before a word belongs to it)
      const times: [number, number][] = [];
      tail.forEach((w, wi) => {
        const n = Array.from(w.w.replace(/[^\p{L}\p{N}'’]/gu, '')).length + (wi > 0 ? 1 : 0);
        for (let k = 0; k < n; k++) times.push([w.start + ((w.end - w.start) * k) / n, w.start + ((w.end - w.start) * (k + 1)) / n]);
      });
      // signed across the bottom right of the big word
      this.script = { st, x: x0 + blockW - st.width + 30, y: base2 + 72, times };
    }
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp } = this.ctx;
    const t = f.t;
    this.bg.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const boil = Math.floor(t * 12);                     // pencil lines re-drawn 12 times a second
    const J = (...k: number[]) => hash(...k, boil) - 0.5;
    // the sheet drifts a little under the pencil
    const lt = t - this.cutTime;
    c.save();
    c.translate(W / 2 + 14 - lt * 12, H / 2); c.rotate(-0.014); c.translate(-W / 2, -H / 2);

    // construction guides: baseline, x-height, cap line, a margin, tick marks
    c.lineCap = 'round'; c.lineJoin = 'round';
    c.strokeStyle = rgba('graphite', 0.42); c.lineWidth = 1.3;
    this.guides.forEach(([base, size], gi) => {
      for (const [y, k] of [[base, 1], [base - size * 0.72, 2], [base - size * 0.53, 5]] as const) {
        c.globalAlpha = k === 5 ? 0.5 : 1;
        c.beginPath(); c.moveTo(60 + J(gi, k, 1) * 20, y + J(gi, k, 2) * 2); c.lineTo(W - 60 + J(gi, k, 3) * 20, y + J(gi, k, 4) * 2); c.stroke();
      }
    });
    c.globalAlpha = 1;
    c.beginPath(); c.moveTo(150, 70); c.lineTo(152 + J(9, 1) * 3, H - 70); c.stroke();
    for (const [base] of this.guides) for (let i = 0; i < 26; i++) { const x = 170 + i * 66; c.beginPath(); c.moveTo(x, base + 8); c.lineTo(x + J(i, 7) * 2, base + 24); c.stroke(); }

    // the pencil: each word roughed in as it's sung — a light first pass, two firm passes that
    // overshoot the corners, then loose hatching inside
    this.sketchWords.forEach(({ w, polys, path, x, width, base, size }, wi) => {
      const p = clamp((t - (w.start - 0.08)) / 0.3);
      if (p <= 0) return;
      const n = (poly: Poly) => Math.max(2, Math.floor(poly.length * ease.outCubic(p)));
      for (let pass = 0; pass < 3; pass++) {
        const dx = (hash(wi, pass, 1) - 0.5) * 6 + J(wi, pass) * 2, dy = (hash(wi, pass, 2) - 0.5) * 6 + J(wi, pass + 9) * 2;
        c.strokeStyle = rgba('graphite', pass === 0 ? 0.35 : pass === 1 ? 0.9 : 0.6);
        c.lineWidth = pass === 0 ? 1.2 : pass === 1 ? 2.6 : 1.7;
        polys.forEach((poly, ci) => {
          const m = pass === 0 ? poly.length : n(poly);
          c.beginPath();
          for (let i = 0; i < m; i++) {
            const q = poly[i]!;
            const wob = noise1(i * 0.35 + pass * 7 + ci * 3, boil) * 1.6;
            if (i === 0) c.moveTo(q.x + dx, q.y + dy); else c.lineTo(q.x + dx + wob, q.y + dy + wob);
          }
          c.stroke();
          // overshoot: long straight runs carry on past their corners
          if (pass === 1 && p >= 1) {
            c.beginPath();
            for (let i = 1; i < poly.length; i++) {
              const a = poly[i - 1]!, b = poly[i]!;
              const L = Math.hypot(b.x - a.x, b.y - a.y);
              if (L < 28) continue;
              const ux = (b.x - a.x) / L, uy = (b.y - a.y) / L;
              const o1 = 6 + 14 * hash(wi, ci, i, 3), o2 = 6 + 14 * hash(wi, ci, i, 4);
              c.moveTo(b.x + dx, b.y + dy); c.lineTo(b.x + dx + ux * o1, b.y + dy + uy * o1);
              c.moveTo(a.x + dx, a.y + dy); c.lineTo(a.x + dx - ux * o2, a.y + dy - uy * o2);
            }
            c.stroke();
          }
        });
      }
      // hatching, swept in left to right
      const h = clamp((t - (w.start + 0.08)) / 0.3);
      if (h > 0) {
        c.save(); c.clip(path);
        c.strokeStyle = rgba('graphite', 0.4); c.lineWidth = 1.4;
        c.beginPath();
        const top = base - size * 0.72 - 30, bot = base + 30, sl = (bot - top) * 0.55;
        for (let k = 0, hx = x - sl; hx < x + width + 20; k++, hx += 9) {
          if (hx > x - sl + (width + sl + 20) * h) break;
          const j = J(wi, k, 5) * 3;
          c.moveTo(hx + j, bot); c.lineTo(hx + sl + j, top);
        }
        c.stroke();
        c.restore();
      }
    });

    // the ink lands on the key word
    if (this.ink && t >= this.ink.w.start) {
      const k = ease.outExpo(clamp((t - this.ink.w.start) / 0.12));
      c.save();
      c.beginPath(); c.rect(this.ink.x - 20, 0, (this.ink.width + 40) * k, H); c.clip();
      c.fillStyle = rgba('ink', 1); c.fill(this.ink.path);
      c.restore();
    }

    // the rest written by hand in orange brush pen
    if (this.script) {
      const s = this.script;
      const len = writtenLength(s.st, s.times, t);
      if (len > 0) {
        c.save(); c.translate(s.x, s.y);
        c.strokeStyle = rgba('signal', 1); c.lineWidth = 12; c.lineCap = 'round'; c.lineJoin = 'round';
        drawStrokeText(c, s.st, len);
        c.restore();
      }
    }
    // the draughtsman's note in the margin
    c.font = font(F.mono(400), 15); c.fillStyle = rgba('graphite', 0.85); c.textAlign = 'left';
    c.fillText('SKETCH  →  INK', 170, 100);
    c.restore();
    comp.draw(renderer, this.L.upload(), out);

    const kick = this.ink && t >= this.ink.w.start ? Math.exp(-(t - this.ink.w.start) * 14) : 0;
    return { ...CLEAN, paper: 1, zoom: 1.0 + 0.02 * kick + 0.02 * clamp(lt / 1.8), shake: [0, 3 * kick] };
  }
}
