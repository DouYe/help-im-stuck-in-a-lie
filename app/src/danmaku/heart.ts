// A heart made of symbols: concentric heart-shaped lanes, each a stream of marks (— · + ♥ * ◇ >)
// flowing along the curve. Rings type themselves in (outer first), beat with the kick, and can burst.
import { LineBatch } from '../engine/lines';
import { LIN } from '../engine/palette';
import { clamp, hash } from '../engine/util';
import { glyph, SYM, mul, mixc, type RGB } from './symbols';

const N_SAMPLES = 480;
/** Unit heart outline (y down), centred on the heart's visual centre, about 2 units wide. */
function heartPt(th: number): [number, number] {
  const s = Math.sin(th);
  const x = 16 * s * s * s;
  const y = -(13 * Math.cos(th) - 5 * Math.cos(2 * th) - 2 * Math.cos(3 * th) - Math.cos(4 * th));
  return [x / 17, (y + 2.5) / 17];
}
const BASE: [number, number][] = [];
const CUM: number[] = [];
{
  let acc = 0;
  for (let i = 0; i <= N_SAMPLES; i++) {
    const p = heartPt((i / N_SAMPLES) * Math.PI * 2);
    if (i > 0) { const q = BASE[i - 1]!; acc += Math.hypot(p[0] - q[0], p[1] - q[1]); }
    BASE.push(p); CUM.push(acc);
  }
}
const TOTAL = CUM[N_SAMPLES]!;
/** Point and tangent angle at arc-length fraction u (0..1) of the unit heart. */
export function heartAt(u: number): [number, number, number] {
  const s = (((u % 1) + 1) % 1) * TOTAL;
  let lo = 0, hi = N_SAMPLES;
  while (hi - lo > 1) { const m = (lo + hi) >> 1; if (CUM[m]! <= s) lo = m; else hi = m; }
  const a = BASE[lo]!, b = BASE[hi]!, f = (s - CUM[lo]!) / Math.max(1e-9, CUM[hi]! - CUM[lo]!);
  return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, Math.atan2(b[1] - a[1], b[0] - a[0])];
}

export interface HeartState {
  cx: number; cy: number; R: number;          // centre and half-width in px
  rings?: number;
  /** 0..1 how much of each ring is typed in (outer rings first). */
  build?: number;
  /** Beat pulse 0..1 (scales the heart). */
  pulse?: number;
  /** 0..1 burst: rings fly outward, the core flares. */
  burst?: number;
  t: number; flow?: number;
  alpha?: number;
  /** Symbol size at the outer ring. */
  size?: number;
}

const RING_KINDS = [
  [SYM.heart, SYM.dot],
  [SYM.dash],
  [SYM.plus, SYM.dot, SYM.dot],
  [SYM.chevron],
  [SYM.star, SYM.dash],
  [SYM.dot],
  [SYM.diamond, SYM.dot],
  [SYM.dash, SYM.dash, SYM.dot],
  [SYM.heart],
  [SYM.cross, SYM.dot],
  [SYM.chevron, SYM.chevron, SYM.dot],
  [SYM.dash],
  [SYM.plus],
  [SYM.dot, SYM.dash],
];

export function drawHeart(lb: LineBatch, st: HeartState) {
  const N = st.rings ?? 12, A = st.alpha ?? 1;
  if (A <= 0.001) return;
  const scale = 1 + 0.07 * (st.pulse ?? 0);
  const burst = st.burst ?? 0;
  const sig = mul(LIN.signal, 2.0 + 1.2 * (st.pulse ?? 0)), ember = mul(LIN.ember, 1.5), bone = mul(LIN.bone, 1.1);
  for (let k = 0; k < N; k++) {
    const f = N === 1 ? 1 : k / (N - 1);                  // 0 inner .. 1 outer
    const r = st.R * scale * (0.16 + 0.84 * f) * (1 + burst * (0.4 + 1.6 * f));
    const size = Math.max(3, (st.size ?? 11) * (0.5 + 0.5 * f));
    const built = clamp((st.build ?? 1) * 1.6 - (1 - f) * 0.6);     // outer first
    if (built <= 0) continue;
    const dir = k % 2 === 0 ? 1 : -1;
    const speed = (st.flow ?? 1) * dir * (26 + 18 * hash(k, 9));      // px/s along the ring
    const L = TOTAL * r;
    const step = size * 2.3;
    const kinds = RING_KINDS[k % RING_KINDS.length]!;
    const col: RGB = f < 0.3 ? sig : f < 0.6 ? mixc(sig, ember, (f - 0.3) / 0.3) : mixc(ember, bone, clamp((f - 0.6) / 0.3));
    const alpha = A * (1 - burst * f * 0.8) * (0.6 + 0.4 * (1 - f * 0.5));
    const lw = Math.max(1.4, 2.4 * (0.6 + 0.4 * f));
    const off = ((st.t * speed) % step + step) % step;
    const limit = L * built;
    const count = Math.floor(L / step);
    for (let i = 0; i < count; i++) {
      const s = i * step + off;
      if (s > limit) break;
      const [x, y, ang] = heartAt(s / L);
      const kind = kinds[(i + Math.floor(st.t * speed / step) * 0) % kinds.length]!;
      const tail = s > limit - 40 ? clamp((limit - s) / 40 + 0.3) : 1;
      glyph(lb, kind, st.cx + x * r, st.cy + y * r, size, kind === SYM.heart || kind === SYM.dot ? 0 : ang + (dir < 0 ? Math.PI : 0), col, alpha * tail, lw);
    }
  }
  // the core: nested small hearts (reads as solid), glowing
  const core = st.R * scale * 0.12 * (1 + burst * 0.6);
  for (let j = 0; j < 5; j++) glyph(lb, SYM.heart, st.cx, st.cy - core * 0.05, core * (1 - j * 0.18) * 1.6, 0, mul(LIN.signal, 2.6 + 1.5 * (st.pulse ?? 0)), A, 3.2);
}

/** Outline points of the heart at radius r (for glyph hearts, collision, masks). */
export function heartOutline(cx: number, cy: number, r: number, n = 64): [number, number][] {
  const out: [number, number][] = [];
  for (let i = 0; i < n; i++) { const [x, y] = heartAt(i / n); out.push([cx + x * r, cy + y * r]); }
  return out;
}
