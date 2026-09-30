// Renders HER glyph grid (figure.ts) with a LineBatch: every glyph is one or two short strokes.
// Animation is a pure function of t:
//  - assembly: every glyph is a bullet fired from the edge of the screen that spirals in and lands on
//    its cell on a 16th note (so she forms in rhythmic bursts), flashing as it lands;
//  - storm: bullets passing through her knock glyphs aside (they spring back when the bullet is gone);
//  - awake: her eyes open (the closed-lid glyphs turn to bright dots);
//  - heart: glyphs over her heart glow in the signal colour and beat.
import { LineBatch } from '../engine/lines';
import { LIN } from '../engine/palette';
import { clamp, ease, hash, frameIdx } from '../engine/util';
import { buildGlyphGrid, GLYPH, FIG_H, type GlyphGrid, type Glyph, type Region } from './figure';
import type { Bullet } from './symbols';

type RGB = [number, number, number];
const mul = (c: RGB, k: number): RGB => [c[0] * k, c[1] * k, c[2] * k];
const mix = (a: RGB, b: RGB, k: number): RGB => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k];

const REGION_COL: Record<Region, () => RGB> = {
  hair: () => mul(LIN.bone, 1.05),
  face: () => mul(LIN.bone, 1.35),
  feature: () => mul(LIN.bone, 2.2),
  body: () => mul(LIN.bone, 0.8),
  dress: () => mul(LIN.ash, 0.85),
  hand: () => mul(LIN.bone, 1.4),
  heart: () => mul(LIN.bone, 1.2),
};

export interface FigureState {
  /** Screen position of the figure's top-left and its scale (1 = built size). */
  x: number; y: number; scale?: number;
  alpha?: number;
  /** Assembly window: runs land between start and end (on 16ths via `snap`). Omit = already assembled. */
  assemble?: { start: number; end: number; snap?: (t: number) => number; fly?: number };
  /** Bullets that knock glyphs aside. */
  storm?: Bullet[];
  /** 0..1 eyes open. */
  awake?: number;
  /** 0..1 glow of the heart region (and a beat pulse 0..1). */
  heart?: number; pulse?: number;
  /** 0..1 flicker/dropout (the lie wearing her down). */
  glitch?: number;
  /** Extra per-glyph offset hook (cage bars etc.). */
  push?: (sx: number, sy: number, g: Glyph) => [number, number, number] | null; // dx, dy, alphaMul
}

/** A glyph in flight: a bright dash pointing where it goes, with a short trail. */
function lbGlyphBullet(lb: LineBatch, x: number, y: number, dir: number, lw: number, col: RGB, a: number) {
  const dx = Math.cos(dir), dy = Math.sin(dir);
  lb.seg2(x - dx * 9, y - dy * 9, x + dx * 5, y + dy * 5, lw, col, a);
  lb.seg2(x - dx * 26, y - dy * 26, x - dx * 9, y - dy * 9, lw * 0.6, mul(col, 0.4), a * 0.6);
}

export class GlyphFigure {
  grid: GlyphGrid;
  landCache: { key: string; v: number[] } | null = null;
  eye: Set<number> = new Set();
  constructor(public height = 1000, cellW = 9, cellH = 16) {
    this.grid = buildGlyphGrid(height, cellW, cellH);
    // eye cells: the lids, in figure space (the head tilt is small; boxes are generous)
    const s = height / FIG_H;
    this.grid.glyphs.forEach((g, i) => {
      const fx = g.x / s, fy = g.y / s;
      if (g.region === 'feature' && fy > 318 && fy < 368 && ((fx > 405 && fx < 492) || (fx > 508 && fx < 596))) this.eye.add(i);
    });
  }

  get width() { return this.grid.width; }

  /** Landing time of a glyph within the assembly window (her face first, then outward; snapped to 16ths). */
  landing(i: number, a: NonNullable<FigureState['assemble']>) {
    const g = this.grid.glyphs[i]!;
    const cx = this.grid.width * 0.5, cy = this.grid.height * 0.33;
    const d = Math.hypot(g.x - cx, (g.y - cy) * 0.8) / Math.hypot(this.grid.width, this.grid.height);
    const f = clamp(0.15 + 0.9 * d * 1.4, 0, 1) * 0.7 + 0.3 * hash(i, 17);
    const t = a.start + clamp(f) * (a.end - a.start);
    return a.snap ? a.snap(t) : t;
  }

  draw(lb: LineBatch, t: number, st: FigureState) {
    const G = this.grid, sc = st.scale ?? 1, A = st.alpha ?? 1;
    if (A <= 0.001) return;
    const cw = G.cellW * sc, ch = G.cellH * sc;
    const lw = 3.1 * Math.max(0.7, sc);
    const sig = LIN.signal, ember = LIN.ember;
    const fi = frameIdx(t);
    const fly = st.assemble?.fly ?? 0.75;
    const land = st.assemble ? (this.landCache && this.landCache.key === st.assemble.start + ':' + st.assemble.end ? this.landCache.v : (this.landCache = { key: st.assemble.start + ':' + st.assemble.end, v: G.glyphs.map((_, i) => this.landing(i, st.assemble!)) }).v) : null;
    const storm = st.storm ?? [];
    for (let i = 0; i < G.glyphs.length; i++) {
      const g = G.glyphs[i]!;
      let x = st.x + g.x * sc, y = st.y + g.y * sc;
      let a = A * g.ink;
      let col = REGION_COL[g.region]();
      // assembly: a bullet spirals in from beyond the screen edge, lands on its cell, flashes
      if (land) {
        const tl = land[i]!;
        if (t < tl - fly) continue;
        if (t < tl) {
          const u = (t - (tl - fly)) / fly;
          const k = ease.outCubic(u);
          const a0 = hash(i, 31) * Math.PI * 2, sw = (hash(i, 32) < 0.5 ? -1 : 1) * (1.2 + hash(i, 33));
          const R = (1250 + 300 * hash(i, 34)) * (1 - k);
          const ang = a0 + sw * (1 - k);
          const bx = x + Math.cos(ang) * R, by = y + Math.sin(ang) * R;
          // direction of travel (for the bullet's dash)
          const k2 = ease.outCubic(Math.min(1, u + 0.02)), R2 = (1250 + 300 * hash(i, 34)) * (1 - k2), ang2 = a0 + sw * (1 - k2);
          const dir = Math.atan2(y + Math.sin(ang2) * R2 - by, x + Math.cos(ang2) * R2 - bx);
          lbGlyphBullet(lb, bx, by, dir, lw, mix(mul(LIN.bone, 1.6), mul(LIN.signal, 2), hash(i, 35) < 0.12 ? 1 : 0), A * clamp(u * 4));
          continue;
        } else {
          const fl = Math.exp(-(t - tl) * 9);
          col = mix(col, mul(LIN.bone, 2.4), fl * 0.75);
        }
      }
      // storm: bullets shove glyphs out of their way
      let pushA = 1;
      for (const b of storm) {
        const dx = x - b.x, dy = y - b.y;
        if (Math.abs(dx) > 34 || Math.abs(dy) > 34) continue;
        const d = Math.hypot(dx, dy);
        if (d > 34) continue;
        const k = 1 - d / 34;
        x += (dx / (d + 1e-3)) * 18 * k + (b.vx / 600) * 10 * k; y += (dy / (d + 1e-3)) * 18 * k + (b.vy / 600) * 10 * k;
        pushA *= 1 - 0.6 * k;
      }
      if (st.push) {
        const r = st.push(x, y, g);
        if (r) { x += r[0]; y += r[1]; pushA *= r[2]; }
      }
      a *= pushA;
      // glitch: dropouts and flicker keyed per frame
      if (st.glitch) {
        const h = hash(i, fi, 3);
        if (h < st.glitch * 0.35) continue;
        if (h < st.glitch * 0.6) x += (hash(i, fi, 4) - 0.5) * 30 * st.glitch;
      }
      // heart: the region under her hand glows and beats
      if (st.heart && (g.region === 'heart' || g.region === 'hand')) {
        const k = g.region === 'heart' ? st.heart : st.heart * 0.35;
        col = mix(col, mul(sig, 1.6 + 1.2 * (st.pulse ?? 0)), k);
      }
      let kind: number = g.kind;
      // awake: lids become open eyes (bright dots)
      if (st.awake && this.eye.has(i)) {
        col = mix(col, mul(ember, 2.4), st.awake);
        if (st.awake > 0.5 && (g.kind === GLYPH.dash || g.kind === GLYPH.back || g.kind === GLYPH.slash)) kind = GLYPH.dot;
      }
      if (a <= 0.01) continue;
      this.glyph(lb, kind, x, y, cw, ch, kind === GLYPH.dot && this.eye.has(i) ? lw * 2.2 : lw, col, a);
    }
  }

  /** One glyph as strokes (x, y = cell centre). */
  glyph(lb: LineBatch, kind: number, x: number, y: number, cw: number, ch: number, lw: number, col: RGB, a: number) {
    switch (kind) {
      case GLYPH.dash: lb.seg2(x - cw * 0.4, y, x + cw * 0.4, y, lw, col, a); break;
      case GLYPH.bar: lb.seg2(x, y - ch * 0.34, x, y + ch * 0.34, lw, col, a); break;
      case GLYPH.slash: lb.seg2(x - cw * 0.34, y + ch * 0.32, x + cw * 0.34, y - ch * 0.32, lw, col, a); break;
      case GLYPH.back: lb.seg2(x - cw * 0.34, y - ch * 0.32, x + cw * 0.34, y + ch * 0.32, lw, col, a); break;
      case GLYPH.plus:
        lb.seg2(x - cw * 0.3, y, x + cw * 0.3, y, lw, col, a);
        lb.seg2(x, y - ch * 0.22, x, y + ch * 0.22, lw, col, a); break;
      default: lb.seg2(x, y, x + 0.01, y, lw * 1.25, col, a);
    }
  }
}
