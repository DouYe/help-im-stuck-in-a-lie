// The video's only material: SYMBOLS. Everything on screen — her, the heart, the maze, the barrages —
// is made of the same few marks: — | / \ · + × * ○ ◇ > ♥, drawn as short strokes (LineBatch), so they
// stay crisp at any size and glow on the signal colour.
//
// "Danmaku" here means bullet patterns made of those marks: rings, spirals and fans of symbols fired on the
// beat, filling the screen (see BulletField). Everything is a pure function of t.
import { LineBatch } from '../engine/lines';
import { FSPass, W, H } from '../engine/gl';
import { LIN } from '../engine/palette';
import { hash, clamp, TAU } from '../engine/util';

export type RGB = [number, number, number];
export const mul = (c: RGB, k: number): RGB => [c[0] * k, c[1] * k, c[2] * k];
export const mixc = (a: RGB, b: RGB, k: number): RGB => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k];

export const SYM = { dash: 0, slash: 1, bar: 2, back: 3, dot: 4, plus: 5, cross: 6, star: 7, ring: 8, diamond: 9, chevron: 10, heart: 11 } as const;
export type SymKind = (typeof SYM)[keyof typeof SYM];

/**
 * One symbol at (x, y), `s` = its size (half-height in px), `a` = rotation (for dash/chevron: the
 * direction it points), line width `lw`.
 */
export function glyph(lb: LineBatch, kind: number, x: number, y: number, s: number, a: number, col: RGB, alpha: number, lw: number) {
  const ca = Math.cos(a), sa = Math.sin(a);
  const P = (u: number, v: number): [number, number] => [x + u * ca - v * sa, y + u * sa + v * ca];
  const seg = (u0: number, v0: number, u1: number, v1: number) => { const p = P(u0, v0), q = P(u1, v1); lb.seg2(p[0], p[1], q[0], q[1], lw, col, alpha); };
  switch (kind) {
    case SYM.dash: seg(-s * 0.85, 0, s * 0.85, 0); break;
    case SYM.bar: seg(0, -s * 0.8, 0, s * 0.8); break;
    case SYM.slash: seg(-s * 0.55, s * 0.75, s * 0.55, -s * 0.75); break;
    case SYM.back: seg(-s * 0.55, -s * 0.75, s * 0.55, s * 0.75); break;
    case SYM.plus: seg(-s * 0.6, 0, s * 0.6, 0); seg(0, -s * 0.6, 0, s * 0.6); break;
    case SYM.cross: seg(-s * 0.5, -s * 0.5, s * 0.5, s * 0.5); seg(-s * 0.5, s * 0.5, s * 0.5, -s * 0.5); break;
    case SYM.star: seg(-s * 0.6, 0, s * 0.6, 0); seg(-s * 0.3, -s * 0.52, s * 0.3, s * 0.52); seg(-s * 0.3, s * 0.52, s * 0.3, -s * 0.52); break;
    case SYM.ring: {
      const n = 8, r = s * 0.55;
      for (let i = 0; i < n; i++) { const a0 = (i / n) * TAU, a1 = ((i + 1) / n) * TAU; seg(Math.cos(a0) * r, Math.sin(a0) * r, Math.cos(a1) * r, Math.sin(a1) * r); }
      break;
    }
    case SYM.diamond: { const r = s * 0.6; seg(0, -r, r, 0); seg(r, 0, 0, r); seg(0, r, -r, 0); seg(-r, 0, 0, -r); break; }
    case SYM.chevron: seg(-s * 0.4, -s * 0.5, s * 0.4, 0); seg(s * 0.4, 0, -s * 0.4, s * 0.5); break;
    case SYM.heart: {
      const n = 14, r = s * 0.62;
      let prev: [number, number] | null = null;
      for (let i = 0; i <= n; i++) {
        const th = (i / n) * TAU, st = Math.sin(th);
        const u = (16 * st * st * st) / 17, v = -(13 * Math.cos(th) - 5 * Math.cos(2 * th) - 2 * Math.cos(3 * th) - Math.cos(4 * th)) / 17 + 0.1;
        if (prev) seg(prev[0] * r, prev[1] * r, u * r, v * r);
        prev = [u, v];
      }
      break;
    }
    default: lb.seg2(x, y, x + 0.01, y, lw * 1.35, col, alpha); // dot
  }
}

// ------------------------------------------------------------------ bullet patterns (danmaku)
export interface Emission {
  t0: number;                // fire time
  x: number; y: number;      // emitter
  n: number;                 // bullets in the volley
  a0: number;                // angle of the first bullet
  spread: number;            // total angle covered (TAU = full ring)
  speed: number;             // px/s
  curl?: number;             // rad/s the heading turns while flying (spirals)
  accel?: number;            // px/s^2
  kind: number;              // symbol
  size?: number;
  hot?: boolean;             // signal colour
  life?: number;             // s
}
export interface Bullet { x: number; y: number; vx: number; vy: number; e: Emission; age: number; i: number }

/** A set of volleys; draws every live bullet at t as a symbol pointing along its motion. */
export class BulletField {
  constructor(public volleys: Emission[] = []) {}
  add(...e: Emission[]) { this.volleys.push(...e); return this; }

  *live(t: number, margin = 60): Generator<Bullet> {
    for (const e of this.volleys) {
      const age = t - e.t0, life = e.life ?? 4;
      if (age < 0 || age > life) continue;
      for (let i = 0; i < e.n; i++) {
        const a = e.a0 + (e.n > 1 ? (e.spread >= TAU - 1e-6 ? (i / e.n) * TAU : (i / (e.n - 1) - 0.5) * e.spread) : 0);
        const c = e.curl ?? 0, acc = e.accel ?? 0;
        const d = e.speed * age + 0.5 * acc * age * age;
        let x: number, y: number, h: number;
        if (Math.abs(c) < 1e-4) { x = e.x + Math.cos(a) * d; y = e.y + Math.sin(a) * d; h = a; }
        else {
          // heading turns at constant rate: integrate analytically (constant speed part)
          h = a + c * age;
          const r = e.speed / c;
          x = e.x + r * (Math.sin(h) - Math.sin(a)) + Math.cos(h) * 0.5 * acc * age * age;
          y = e.y - r * (Math.cos(h) - Math.cos(a)) + Math.sin(h) * 0.5 * acc * age * age;
        }
        if (x < -margin || y < -margin || x > W + margin || y > H + margin) continue;
        const sp = e.speed + acc * age;
        yield { x, y, vx: Math.cos(h) * sp, vy: Math.sin(h) * sp, e, age, i };
      }
    }
  }

  draw(lb: LineBatch, t: number, o: { alpha?: number; scale?: number; color?: RGB; hot?: RGB } = {}) {
    const A = o.alpha ?? 1;
    if (A <= 0.001) return;
    const bone = o.color ?? mul(LIN.bone, 1.2), sig = o.hot ?? mul(LIN.signal, 2.2);
    for (const b of this.live(t)) {
      const life = b.e.life ?? 4;
      const fade = clamp(b.age / 0.08) * clamp((life - b.age) / 0.5);
      const s = (b.e.size ?? 9) * (o.scale ?? 1);
      const col = b.e.hot ? sig : bone;
      const ang = Math.atan2(b.vy, b.vx);
      glyph(lb, b.e.kind, b.x, b.y, s, b.e.kind === SYM.heart || b.e.kind === SYM.ring || b.e.kind === SYM.dot ? 0 : ang, col, A * fade, 2.4);
    }
  }
}

/** Volleys on the beat grid: a ring on every beat, a spiral every bar, from given emitters. */
export function beatVolleys(beats: number[], t0: number, t1: number, o: { x: number; y: number; seed?: number; every?: number; n?: number; speed?: number; kinds?: number[]; hotEvery?: number; spiral?: boolean }): Emission[] {
  const out: Emission[] = [];
  const seed = o.seed ?? 1;
  const kinds = o.kinds ?? [SYM.dash, SYM.dot, SYM.star, SYM.plus];
  beats.forEach((bt, i) => {
    if (bt < t0 || bt >= t1) return;
    if (i % (o.every ?? 1)) return;
    const kind = kinds[Math.floor(hash(i, seed) * kinds.length)]!;
    const n = o.n ?? 24;
    const hot = o.hotEvery ? i % o.hotEvery === 0 : false;
    out.push({ t0: bt, x: o.x, y: o.y, n, a0: hash(i, seed, 2) * TAU, spread: TAU, speed: o.speed ?? 380, curl: o.spiral ? (i % 2 ? 0.55 : -0.55) : 0, kind, size: 9, hot, life: 4.5 });
  });
  return out;
}

// ------------------------------------------------------------------ the screen: a grid of faint symbols
/** Full-screen grid of dim dots (a screen of characters), with rings of brighter symbols on the kick. */
export class SymbolGrid {
  pass = new FSPass(/* glsl */ `
    uniform float t, pulse, level, ringR, ringK;
    uniform vec2 center;
    float segD(vec2 p, vec2 a, vec2 b) { vec2 pa = p - a, ba = b - a; float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0); return length(pa - ba * h); }
    void main() {
      vec2 px = FRAG_PX; px.y = ${H.toFixed(1)} - px.y;
      vec2 cell = vec2(16.0, 26.0);
      vec2 ci = floor(px / cell), c0 = (ci + 0.5) * cell;
      vec2 u = (px - c0) / cell.y;
      float h = fract(sin(dot(ci, vec2(12.9898, 78.233))) * 43758.5453);
      // slow drifting field: some cells show a short stroke along a flow direction
      float n = snoise(ci * 0.06 + vec2(0.0, t * 0.12));
      float ang = n * 3.1416;
      vec2 dir = vec2(cos(ang), sin(ang)) * vec2(0.22, 0.3);
      float r = length(c0 - center);
      float ring = exp(-pow((r - ringR) / 70.0, 2.0)) * ringK;
      float lit = level * (0.5 + 0.9 * smoothstep(0.2, 0.9, n * 0.5 + 0.5)) + ring * 1.6;
      float aa = 1.2 / cell.y;
      float ink;
      if (h < 0.3 + 0.5 * ring) ink = 1.0 - smoothstep(0.04, 0.04 + aa, segD(u, -dir, dir));
      else ink = 1.0 - smoothstep(0.035, 0.035 + aa, length(u));
      vec3 col = C_INK + (C_ASH * 0.18 * lit + C_SIGNAL * 0.5 * ring * pulse) * ink;
      fragColor = vec4(col, 1.0);
    }`, { t: { value: 0 }, pulse: { value: 0 }, level: { value: 1 }, ringR: { value: 0 }, ringK: { value: 0 }, center: { value: [W / 2, H / 2] } });
  render(renderer: any, out: any, t: number, o: { level?: number; ringR?: number; ringK?: number; pulse?: number; cx?: number; cy?: number } = {}) {
    const u = this.pass.u;
    u.t!.value = t; u.level!.value = o.level ?? 1; u.ringR!.value = o.ringR ?? 0; u.ringK!.value = o.ringK ?? 0; u.pulse!.value = o.pulse ?? 0;
    u.center!.value = [o.cx ?? W / 2, o.cy ?? H / 2];
    this.pass.render(renderer, out);
  }
}

/** Kick rings: radius and strength of the ring that the last kick sent out from the centre. */
export function kickRing(onsets: [number, number][] | undefined, t: number, speed = 900): { r: number; k: number } {
  if (!onsets) return { r: 0, k: 0 };
  let last: [number, number] | null = null;
  for (const o of onsets) { if (o[0] <= t) last = o; else break; }
  if (!last) return { r: 0, k: 0 };
  const age = t - last[0];
  return { r: age * speed, k: Math.exp(-age * 2.2) * Math.min(1, last[1] * 1.3) };
}
