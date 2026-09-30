// SHOT — 'stitch' (cross-stitch sampler). One idea: the heart is still there, made by hand.
// Close on Aida cloth. A needle racing through the holes cross-stitches a pixel heart in orange thread:
// the outline while 'Heart' is sung, the fill row by row (half-stitches out, crossing stitches back)
// through the held 'inside', two white stitches for a shine. Then the line is backstitched under it in
// black thread, a knot, the needle leaves, and the finished sampler holds.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { rgba } from '../engine/palette';
import { clamp, ease, lerp } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { wordText } from '../danmaku/kinetic';
import { CLEAN } from './poster';

const HEART = [
  '..XXX...XXX..',
  '.XXXXX.XXXXX.',
  'XXXXXXXXXXXXX',
  'XXXXXXXXXXXXX',
  'XXXXXXXXXXXXX',
  '.XXXXXXXXXXX.',
  '..XXXXXXXXX..',
  '...XXXXXXX...',
  '....XXXXX....',
  '.....XXX.....',
  '......X......',
];
const SHINE = new Set(['1,2', '1,3', '2,1']);
const C = 40, COLS = 13, ROWS = 11;
const GX = W / 2 - (COLS * C) / 2, GY = 220;           // top-left hole of the heart's grid
const U = C / 2, TEXT_Y = GY + ROWS * C + 2 * C;         // backstitch letters: 4x6 units of half a cell
// pixel letters as backstitch skeletons (polylines on a 4x6 grid)
const LET: Record<string, number[][]> = {
  A: [[0, 6, 0, 2, 2, 0, 4, 2, 4, 6], [0, 4, 4, 4]], B: [[0, 0, 0, 6, 3, 6, 4, 5, 4, 4, 3, 3, 0, 3], [0, 0, 3, 0, 4, 1, 4, 2, 3, 3]],
  C: [[4, 1, 3, 0, 1, 0, 0, 1, 0, 5, 1, 6, 3, 6, 4, 5]], D: [[0, 0, 0, 6, 3, 6, 4, 5, 4, 1, 3, 0, 0, 0]],
  E: [[4, 0, 0, 0, 0, 6, 4, 6], [0, 3, 3, 3]], F: [[4, 0, 0, 0, 0, 6], [0, 3, 3, 3]],
  G: [[4, 1, 3, 0, 1, 0, 0, 1, 0, 5, 1, 6, 3, 6, 4, 5, 4, 3, 2, 3]], H: [[0, 0, 0, 6], [4, 0, 4, 6], [0, 3, 4, 3]],
  I: [[1, 0, 3, 0], [2, 0, 2, 6], [1, 6, 3, 6]], J: [[4, 0, 4, 5, 3, 6, 1, 6, 0, 5]],
  K: [[0, 0, 0, 6], [4, 0, 0, 4], [1, 3, 4, 6]], L: [[0, 0, 0, 6, 4, 6]], M: [[0, 6, 0, 0, 2, 3, 4, 0, 4, 6]],
  N: [[0, 6, 0, 0, 4, 6, 4, 0]], O: [[1, 0, 3, 0, 4, 1, 4, 5, 3, 6, 1, 6, 0, 5, 0, 1, 1, 0]],
  P: [[0, 6, 0, 0, 3, 0, 4, 1, 4, 2, 3, 3, 0, 3]], Q: [[1, 0, 3, 0, 4, 1, 4, 5, 3, 6, 1, 6, 0, 5, 0, 1, 1, 0], [2, 4, 4, 6]],
  R: [[0, 6, 0, 0, 3, 0, 4, 1, 4, 2, 3, 3, 0, 3], [2, 3, 4, 5, 4, 6]], S: [[4, 0, 1, 0, 0, 1, 0, 2, 1, 3, 3, 3, 4, 4, 4, 5, 3, 6, 0, 6]],
  T: [[0, 0, 4, 0], [2, 0, 2, 6]], U: [[0, 0, 0, 5, 1, 6, 3, 6, 4, 5, 4, 0]], V: [[0, 0, 0, 3, 2, 6, 4, 3, 4, 0]],
  W: [[0, 0, 0, 6, 2, 3, 4, 6, 4, 0]], X: [[0, 0, 4, 6], [4, 0, 0, 6]], Y: [[0, 0, 2, 3, 4, 0], [2, 3, 2, 6]],
  Z: [[0, 0, 4, 0, 0, 6, 4, 6]], '’': [[2, 0, 2, 1]],
};

type Thread = 'signal' | 'bone' | 'ink';
interface Leg { ax: number; ay: number; bx: number; by: number; t: number; th: Thread; top: boolean; back: boolean }

export default class Stitch extends Mode {
  cloth = new FSPass(/* glsl */ `
    uniform vec2 origin;
    void main() {
      vec2 p = FRAG_PX; p.y = ${H.toFixed(1)} - p.y;
      vec2 q = p - origin;
      // Aida cloth: blocks of 4x4 woven threads, a hole at every block corner
      float pitch = ${(C / 4).toFixed(2)};
      vec2 w = q / pitch;
      vec2 id = floor(w), f = fract(w);
      float slubX = 0.1 * snoise(vec2(id.x * 0.9, q.y * 0.02)), slubY = 0.1 * snoise(vec2(q.x * 0.02, id.y * 0.9));
      float tx = 0.36 + 0.08 * hash11(id.x * 1.7) + slubX, ty = 0.36 + 0.08 * hash11(id.y * 3.1 + 5.0) + slubY;
      float onX = 1.0 - smoothstep(tx - 0.1, tx + 0.06, abs(f.x - 0.5));
      float onY = 1.0 - smoothstep(ty - 0.1, ty + 0.06, abs(f.y - 0.5));
      bool warpTop = mod(id.x + id.y, 2.0) < 1.0;
      float rx = 0.72 + 0.28 * cos((f.x - 0.5) * 3.0), ry = 0.72 + 0.28 * cos((f.y - 0.5) * 3.0);
      float lum = warpTop ? max(onX * rx * (0.82 + 0.18 * sin(f.y * 3.1416)), onY * ry * 0.78)
                          : max(onY * ry * (0.82 + 0.18 * sin(f.x * 3.1416)), onX * rx * 0.78);
      vec3 col = C_BONE * (0.5 + 0.5 * lum);
      col = mix(col, C_BONE * 0.3, (1.0 - max(onX, onY)) * 0.55);
      // the holes at block corners
      vec2 hc = fract(q / ${C.toFixed(1)} + 0.5) - 0.5;
      float hole = 1.0 - smoothstep(2.2, 4.8, length(hc * ${C.toFixed(1)}));
      col = mix(col, C_BONE * 0.16, hole * 0.85);
      col *= 0.95 + 0.05 * snoise(p * 0.003);
      fragColor = vec4(col, 1.0);
    }`, { origin: { value: new THREE.Vector2(GX, GY) } });
  L = new Layer2D();
  legs: Leg[] = [];
  knotT = 1e9; leaveT = 1e9;
  tFillEnd = 0;

  init() {
    const ws = this.wordsIn();
    const cut = this.cutTime;
    const w0 = ws[0], w1 = ws[1];
    const tOutlineEnd = w0 ? w0.end : cut + 0.9;
    const tFill0 = w1 ? w1.start : tOutlineEnd + 0.03, tFill1 = w1 ? w1.end : tFill0 + 1;
    this.tFillEnd = tFill1;
    const on = (r: number, c: number) => r >= 0 && r < ROWS && c >= 0 && c < COLS && HEART[r]![c] === 'X';
    const cells: { r: number; c: number; edge: boolean }[] = [];
    for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) if (on(r, c)) cells.push({ r, c, edge: !on(r - 1, c) || !on(r + 1, c) || !on(r, c - 1) || !on(r, c + 1) });
    const X = (c: number) => GX + c * C, Y = (r: number) => GY + r * C;
    const thread = (r: number, c: number): Thread => (SHINE.has(`${r},${c}`) ? 'bone' : 'signal');
    // the outline, in one sweep round the heart from its tip
    const cx = (COLS * C) / 2, cy = (ROWS * C) / 2;
    const edge = cells.filter((q) => q.edge).map((q) => ({ ...q, a: (Math.atan2(-((q.c + 0.5) * C - cx), (q.r + 0.5) * C - cy) + Math.PI * 2) % (Math.PI * 2) }));
    edge.sort((a, b) => a.a - b.a);
    const t0 = cut + 0.04, dt = (tOutlineEnd - t0) / edge.length;
    edge.forEach((q, i) => {
      const t = t0 + i * dt;
      this.legs.push({ ax: X(q.c), ay: Y(q.r + 1), bx: X(q.c + 1), by: Y(q.r), t, th: 'signal', top: false, back: false });
      this.legs.push({ ax: X(q.c + 1), ay: Y(q.r + 1), bx: X(q.c), by: Y(q.r), t: t + dt * 0.5, th: 'signal', top: true, back: false });
    });
    // the fill, row by row: half-stitches along the row, then crossed coming back
    const rows = new Map<number, { r: number; c: number }[]>();
    for (const q of cells) if (!q.edge) (rows.get(q.r) ?? rows.set(q.r, []).get(q.r)!).push(q);
    const nLegs = [...rows.values()].reduce((a, v) => a + v.length * 2, 0);
    let k = 0;
    const tf = (i: number) => tFill0 + ((tFill1 - 0.08 - tFill0) * i) / Math.max(1, nLegs - 1);
    for (const r of [...rows.keys()].sort((a, b) => a - b)) {
      const row = rows.get(r)!.sort((a, b) => a.c - b.c);
      for (const q of row) this.legs.push({ ax: X(q.c), ay: Y(q.r + 1), bx: X(q.c + 1), by: Y(q.r), t: tf(k++), th: thread(q.r, q.c), top: false, back: false });
      for (const q of [...row].reverse()) this.legs.push({ ax: X(q.c + 1), ay: Y(q.r + 1), bx: X(q.c), by: Y(q.r), t: tf(k++), th: thread(q.r, q.c), top: true, back: false });
    }
    // the words, backstitched in black under the heart
    const text = ws.map((w) => wordText(w.w)).join(' ');
    const adv = (ch: string) => (ch === ' ' ? 4 : 6);
    const width = Array.from(text).reduce((a, ch) => a + adv(ch), 0) - 2;
    let ox = Math.round((W / 2 - (width * U) / 2) / U) * U;
    const segs: [number, number, number, number][] = [];
    for (const ch of Array.from(text)) {
      for (const pl of LET[ch] ?? []) {
        for (let i = 2; i < pl.length; i += 2) {
          const ax = ox + pl[i - 2]! * U, ay = TEXT_Y + pl[i - 1]! * U, bx = ox + pl[i]! * U, by = TEXT_Y + pl[i + 1]! * U;
          const n = Math.max(1, Math.round(Math.hypot(bx - ax, by - ay) / (U * 1.05)));
          for (let j = 0; j < n; j++) segs.push([lerp(ax, bx, j / n), lerp(ay, by, j / n), lerp(ax, bx, (j + 1) / n), lerp(ay, by, (j + 1) / n)]);
        }
      }
      ox += adv(ch) * U;
    }
    const beat = 60 / this.ctx.audio.bpm;
    const s0 = tFill1 + 0.1, s1 = Math.min(this.ctx.end - beat * 1.3, s0 + beat * 3.4);
    segs.forEach(([ax, ay, bx, by], i) => this.legs.push({ ax, ay, bx, by, t: s0 + ((s1 - s0) * i) / Math.max(1, segs.length - 1), th: 'ink', top: true, back: true }));
    this.knotT = s1 + 0.12; this.leaveT = s1 + 0.3;
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp } = this.ctx;
    const t = f.t;
    this.cloth.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const DUR = 0.03;
    const shown = this.legs.filter((l) => t >= l.t);
    const prog = (l: Leg) => ease.outCubic(clamp((t - l.t) / DUR));
    const end = (l: Leg) => { const p = prog(l); return [lerp(l.ax, l.bx, p), lerp(l.ay, l.by, p)] as const; };
    const inset = (l: Leg) => { const dx = l.bx - l.ax, dy = l.by - l.ay, d = Math.hypot(dx, dy); const k = (l.back ? 2.2 : 4) / d; return [l.ax + dx * k, l.ay + dy * k] as const; };
    c.lineCap = 'round'; c.lineJoin = 'round';
    // shadows on the cloth
    c.strokeStyle = rgba('ink', 0.26);
    for (const l of shown) {
      const [ax, ay] = inset(l), [bx, by] = end(l);
      c.lineWidth = l.back ? 9 : 13;
      c.beginPath(); c.moveTo(ax + 2, ay + 3); c.lineTo(bx + 2, by + 3); c.stroke();
    }
    // bottom legs first, then the crossing legs and the backstitch
    for (const pass of [false, true]) for (const l of shown) {
      if (l.top !== pass) continue;
      const [ax0, ay0] = inset(l), [bx1, by1] = end(l);
      const dx = bx1 - ax0, dy = by1 - ay0, d = Math.hypot(dx, dy) || 1;
      const k = (l.back ? 2.2 : 4) / d;
      const ax = ax0, ay = ay0, bx = bx1 - (prog(l) >= 1 ? dx * k : 0), by = by1 - (prog(l) >= 1 ? dy * k : 0);
      const nx = -dy / d, ny = dx / d;
      const wBody = l.back ? 8.5 : 10.5;
      const dark = l.th === 'ink' ? rgba('ink', 1) : l.th === 'bone' ? rgba('ash', 1) : rgba('blood', 1);
      const mid = l.th === 'ink' ? rgba('ink2', 1) : l.th === 'bone' ? rgba('bone', 1) : rgba('signal', 1);
      const hi = l.th === 'ink' ? rgba('graphite', 0.9) : l.th === 'bone' ? rgba('bone', 1) : rgba('ember', 0.9);
      c.strokeStyle = dark; c.lineWidth = wBody + 1.5; c.beginPath(); c.moveTo(ax, ay); c.lineTo(bx, by); c.stroke();
      c.strokeStyle = mid; c.lineWidth = wBody - 1.5; c.beginPath(); c.moveTo(ax, ay); c.lineTo(bx, by); c.stroke();
      // the twist of the floss: short slanted ticks along the thread
      c.strokeStyle = l.th === 'bone' ? rgba('ash', 0.55) : l.th === 'ink' ? rgba('graphite', 0.5) : rgba('blood', 0.5);
      c.lineWidth = 1.3;
      const step = 5.5, n = Math.floor(Math.hypot(bx - ax, by - ay) / step);
      c.beginPath();
      for (let i = 1; i < n; i++) {
        const px = ax + ((bx - ax) * i) / n, py = ay + ((by - ay) * i) / n, h = wBody * 0.42;
        c.moveTo(px - nx * h - (dx / d) * 2.2, py - ny * h - (dy / d) * 2.2); c.lineTo(px + nx * h + (dx / d) * 2.2, py + ny * h + (dy / d) * 2.2);
      }
      c.stroke();
      c.strokeStyle = hi; c.lineWidth = l.back ? 1.4 : 2;
      c.beginPath(); c.moveTo(ax - nx * wBody * 0.2, ay - ny * wBody * 0.2); c.lineTo(bx - nx * wBody * 0.2, by - ny * wBody * 0.2); c.stroke();
    }
    // the knot at the end of the line
    if (t >= this.knotT) {
      const l = this.legs[this.legs.length - 1]!;
      const s = ease.outBack(clamp((t - this.knotT) / 0.12));
      c.fillStyle = rgba('ink', 0.3); c.beginPath(); c.arc(l.bx + 2, l.by + 3, 8 * s, 0, Math.PI * 2); c.fill();
      c.fillStyle = rgba('ink2', 1); c.beginPath(); c.arc(l.bx, l.by, 7.5 * s, 0, Math.PI * 2); c.fill();
      c.fillStyle = rgba('graphite', 0.9); c.beginPath(); c.arc(l.bx - 2, l.by - 2, 2.5 * s, 0, Math.PI * 2); c.fill();
    }
    // the needle: its point at the hole being worked, the working thread trailing from its eye
    const cur = [...this.legs].reverse().find((l) => t >= l.t) ?? this.legs[0]!;
    const nxt = this.legs[this.legs.indexOf(cur) + 1];
    let tip: [number, number] = [cur.bx, cur.by];
    if (t < cur.t) tip = [cur.ax, cur.ay];
    else if (nxt && prog(cur) >= 1) {
      const u = clamp((t - cur.t - DUR) / Math.max(1e-3, nxt.t - cur.t - DUR));
      tip = [lerp(cur.bx, nxt.ax, u), lerp(cur.by, nxt.ay, u)];
    } else { const e = end(cur); tip = [e[0], e[1]]; }
    const gone = t >= this.leaveT ? ease.inCubic(clamp((t - this.leaveT) / 0.5)) : 0;
    const lift = Math.abs(Math.sin(t * 40)) * 10 * (1 - gone) + 900 * gone;
    const ang = -0.95, Lg = 330;
    const tx = tip[0] + Math.cos(ang) * lift * 0.2 + 700 * gone, ty = tip[1] + Math.sin(ang) * lift;
    const ex = tx + Math.cos(ang) * (Lg - 36), ey = ty + Math.sin(ang) * (Lg - 36);
    const th = t < this.tFillEnd ? 'signal' : 'ink';
    if (gone < 1) {
      // working thread from the eye down to the last stitch
      const last = shown.length ? shown[shown.length - 1]! : null;
      if (last) {
        const [lx, ly] = end(last);
        c.strokeStyle = rgba('ink', 0.22); c.lineWidth = 9;
        c.beginPath(); c.moveTo(ex + 3, ey + 4); c.quadraticCurveTo((ex + lx) / 2 + 80, Math.max(ey, ly) + 60, lx + 3, ly + 4); c.stroke();
        c.strokeStyle = th === 'ink' ? rgba('ink2', 1) : rgba('signal', 1); c.lineWidth = 7;
        c.beginPath(); c.moveTo(ex, ey); c.quadraticCurveTo((ex + lx) / 2 + 80, Math.max(ey, ly) + 60, lx, ly); c.stroke();
      }
      c.save(); c.translate(tx, ty); c.rotate(ang);
      // shadow, then steel: a long taper to the point, the eye near the head
      const body = (dx: number, dy: number) => { c.beginPath(); c.moveTo(dx, dy); c.lineTo(60 + dx, -4.5 + dy); c.lineTo(Lg - 8 + dx, -4.5 + dy); c.quadraticCurveTo(Lg + 4 + dx, dy, Lg - 8 + dx, 4.5 + dy); c.lineTo(60 + dx, 4.5 + dy); c.closePath(); };
      body(10, 16); c.fillStyle = rgba('ink', 0.22); c.fill();
      body(0, 0); c.fillStyle = rgba('ash', 1); c.fill(); c.strokeStyle = rgba('graphite', 1); c.lineWidth = 1.5; c.stroke();
      c.strokeStyle = rgba('bone', 1); c.lineWidth = 1.6; c.beginPath(); c.moveTo(40, -1.5); c.lineTo(Lg - 14, -2.4); c.stroke();
      c.fillStyle = rgba('ink2', 1); c.beginPath(); c.ellipse(Lg - 36, 0, 12, 1.8, 0, 0, Math.PI * 2); c.fill();
      c.restore();
    }
    comp.draw(renderer, this.L.upload(), out);

    // camera: close on the heart while it's stitched, easing back to show the words
    const back = ease.inOutCubic(clamp((t - this.tFillEnd) / 0.9));
    const endT = this.ctx.params.cutOut ?? this.ctx.end;
    const fade = 1 - Math.pow(1 - ease.inOutQuad(clamp((t - (endT - 0.7)) / 0.68)), 2.2);   // perceptually even, black on the last frame
    return { ...CLEAN, zoom: lerp(1.2, 1.0, back) + 0.004 * Math.sin(t * 1.7), fade };
  }
}
