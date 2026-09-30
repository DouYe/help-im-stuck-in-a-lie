// Kinetic type for the chaotic edit: words that SLAM (big Archivo, pop, shake, echoes, stretch) and
// words MADE OF SYMBOLS (hundreds of marks that fly in, assemble, jitter and shatter).
import { LineBatch } from '../engine/lines';
import { LIN, rgba } from '../engine/palette';
import { F, font, measure, textPoints } from '../engine/type';
import { clamp, ease, hash, frameIdx } from '../engine/util';
import { glyph, SYM, mul, mixc, type RGB } from './symbols';

/** A sung word as display text: upper case, punctuation dropped, apostrophes kept (I’M). */
export const wordText = (w: string) => w.replace(/[^\p{L}\p{N}'’]/gu, '').replace(/'/g, '’').toUpperCase();

export interface SlamOpts {
  size?: number; width?: number; weight?: number;
  color?: string; alpha?: number;
  /** Seconds since the slam (drives the pop and the echo rings). */
  age: number;
  /** 0..1 horizontal stretch (held notes), 0..1 per-letter jitter. */
  stretch?: number; jitter?: number;
  /** Ghost copies expanding outward behind the word. */
  echoes?: number; echoColor?: string;
  rotate?: number; t?: number;
}

/** A word slammed at (cx, cy): pops from 1.4x, settles, optionally stretches and trembles. */
export function slamWord(c: CanvasRenderingContext2D, word: string, cx: number, cy: number, o: SlamOpts) {
  const fam = F.archivo(o.width ?? 125, o.weight ?? 900);
  let size = o.size ?? 300;
  const w0 = measure(word, fam, size);
  if (w0 > 1780) size *= 1780 / w0;
  const pop = 1 + 0.4 * Math.exp(-Math.max(0, o.age) * 16);
  const sx = 1 + 0.6 * (o.stretch ?? 0);
  c.save();
  c.translate(cx, cy);
  if (o.rotate) c.rotate(o.rotate);
  c.font = font(fam, size);
  c.textAlign = 'center'; c.textBaseline = 'middle';
  // echoes: outlines expanding and fading
  const E = o.echoes ?? 0;
  for (let k = E; k >= 1; k--) {
    const a = Math.exp(-o.age * 3) * (0.5 / k);
    if (a < 0.02) continue;
    const s = pop * (1 + k * 0.12 + o.age * 0.6 * k);
    c.save(); c.scale(s * sx, s);
    c.globalAlpha = (o.alpha ?? 1) * a;
    c.lineWidth = 3 / s; c.strokeStyle = o.echoColor ?? rgba('bone', 1);
    c.strokeText(word, 0, size * 0.04);
    c.restore();
  }
  c.scale(pop * sx, pop);
  c.globalAlpha = o.alpha ?? 1;
  c.fillStyle = o.color ?? rgba('bone', 1);
  if (o.jitter) {
    // per letter tremble (keyed per frame so motion blur doesn't smear it)
    const letters = Array.from(word);
    const total = measure(word, fam, size);
    let x = -total / 2;
    c.textAlign = 'left';
    letters.forEach((ch, i) => {
      const fi = frameIdx(o.t ?? 0);
      const jx = (hash(i, fi, 1) - 0.5) * size * 0.06 * o.jitter!, jy = (hash(i, fi, 2) - 0.5) * size * 0.08 * o.jitter!;
      c.fillText(ch, x + jx, size * 0.04 + jy);
      x += measure(ch, fam, size);
    });
  } else c.fillText(word, 0, size * 0.04);
  c.restore();
}

// ------------------------------------------------------------------ words made of symbols
interface Pt { x: number; y: number; k: number; h: number }
const cache = new Map<string, { pts: Pt[]; w: number }>();

/** Points (relative to the word's centre) filling the word, each with a symbol kind. */
export function symbolWord(word: string, size = 320, step = 13): { pts: Pt[]; w: number } {
  const key = `${word}|${size}|${step}`;
  let v = cache.get(key);
  if (!v) {
    const fam = F.archivo(125, 900);
    const raw = textPoints(word, fam, size, step, 7);
    const w = measure(word, fam, size);
    const kinds = [SYM.dash, SYM.slash, SYM.bar, SYM.back, SYM.plus, SYM.dot, SYM.cross, SYM.star];
    v = { pts: raw.map((p, i) => ({ x: p.x - w / 2, y: p.y + size * 0.36, k: kinds[Math.floor(hash(i, 3) * kinds.length)]!, h: hash(i, 4) })), w };
    cache.set(key, v);
  }
  return v;
}

export interface SymbolWordState {
  cx: number; cy: number; t: number;
  /** When it assembles (points fly in from a burst) and when it shatters (flies apart). */
  in: number; out?: number;
  color?: RGB; hot?: RGB; hotFrac?: number;
  alpha?: number; scale?: number; stretch?: number;
  /** Per-frame flicker 0..1. */
  flicker?: number; lw?: number; size?: number;
}

export function drawSymbolWord(lb: LineBatch, word: string, st: SymbolWordState, size = 320) {
  const { pts } = symbolWord(word, size);
  const bone = st.color ?? mul(LIN.bone, 1.0), hot = st.hot ?? mul(LIN.signal, 2.0);
  const sc = st.scale ?? 1, sx = 1 + 0.6 * (st.stretch ?? 0);
  const fi = frameIdx(st.t);
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i]!;
    // assemble: from a random direction and distance, fast ease-out, staggered by a few ms
    const tin = st.in + p.h * 0.1;
    if (st.t < tin - 0.35) continue;
    const u = clamp((st.t - (tin - 0.35)) / 0.35);
    const k = ease.outExpo(u);
    const a0 = hash(i, 11) * Math.PI * 2, d0 = 500 + 900 * hash(i, 12);
    let x = st.cx + p.x * sc * sx + Math.cos(a0) * d0 * (1 - k);
    let y = st.cy + p.y * sc + Math.sin(a0) * d0 * (1 - k);
    let a = (st.alpha ?? 1) * clamp(u * 3);
    // shatter: fly outward from the word's centre
    if (st.out !== undefined && st.t > st.out) {
      const s = st.t - st.out;
      const dx = p.x * sc, dy = p.y * sc;
      const L = Math.hypot(dx, dy) + 1;
      const v = 900 + 1400 * hash(i, 13);
      x += (dx / L) * v * s + (hash(i, 14) - 0.5) * 300 * s;
      y += (dy / L) * v * s + (hash(i, 15) - 0.5) * 300 * s + 400 * s * s;
      a *= clamp(1 - s / 0.7);
    }
    if (a <= 0.01) continue;
    if (st.flicker && hash(i, fi, 5) < st.flicker * 0.3) continue;
    const col = hash(i, 16) < (st.hotFrac ?? 0) ? hot : mixc(bone, mul(bone, 1.6), hash(i, 17) * 0.4);
    glyph(lb, p.k, x, y, (st.size ?? 5.5) * sc, (hash(i, 18) - 0.5) * 0.6, col, a, st.lw ?? 2.2);
  }
}
