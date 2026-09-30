// THE GIRL (style 1, final — see design/character/GIRL_SPEC.md). A vector rig of polylines per part,
// rasterized every frame into a 17 x 27 grid of symbols: each cell a stroke passes through takes the
// symbol that matches the stroke's direction; the eyes (and the nose in a turned view) are placed last, on
// top of everything, one symbol each. The heart is symbols too ( /\/\ over \/ ), the only orange.
// Port of design/character/src/vgirl.py — keep the two in step.
import { GlyphPen } from './glyph';

type Pt = [number, number];
export interface Rig { g: Record<string, Pt[][]>; heart?: [number, number, number] }
export const COLS = 17, ROWS = 27;

const arc = (cx: number, cy: number, rx: number, ry: number, a0: number, a1: number, n = 12): Pt[] =>
  Array.from({ length: n + 1 }, (_, i) => [cx + rx * Math.cos(a0 + ((a1 - a0) * i) / n), cy + ry * Math.sin(a0 + ((a1 - a0) * i) / n)]);
const PI = Math.PI;

/** front (f = 0) to three-quarter (f = 1, ~45 degrees to her left) as one continuous rig (Q1). */
export function turn(f: number, t = 0, walk = false): Rig {
  const L = (a: number, b: number) => a + (b - a) * f;
  const P = (pa: Pt[], pb: Pt[]): Pt[] => pa.map((a, i) => [L(a[0], pb[i]![0]), L(a[1], pb[i]![1])]);
  const g: Record<string, Pt[][]> = {};
  const add = (k: string, pl: Pt[]) => (g[k] ??= []).push(pl);
  const cx = L(0.5, 0.53), rx = L(0.31, 0.29), lo = L(0.2, 0.21), ro = L(0.81, 0.79);
  add('hair_out', [[lo, 0.8], [lo - 0.01, 0.5], [cx - rx, 0.26], ...arc(cx, 0.26, rx, 0.25, PI, 2 * PI, 16), [ro, 0.5], [ro - 0.01, 0.8]]);
  const li = L(0.31, 0.385), ri = L(0.69, 0.765);
  add('hair_out', [[lo, 0.8], [lo + 0.04, 0.84], [lo + 0.07, 0.8], [li, 0.83]]);
  add('hair_out', [[ro - 0.01, 0.8], [ro - 0.04, 0.84], [L(ro - 0.07, ro - 0.03), 0.81], [ri, 0.83]]);
  const fc = (li + ri) / 2, frx = (ri - li) / 2;
  add('hair_in', [[li, 0.83], [li, 0.5], [li + 0.01, 0.3], ...arc(fc, 0.3, frx - 0.01, 0.08, PI, 2 * PI, 10), [ri - 0.01, 0.5], [ri, 0.83]]);
  const ne = L(0.42, 0.515), fe = L(0.58, 0.665), e1 = L(0.03, 0.035), e2 = L(0.03, 0.024);
  g.eyes = [[[ne - e1, 0.335], [ne + e1, 0.335]], [[fe - e2, 0.335], [fe + e2, 0.335]]];
  if (f > 0.3) { const k = (f - 0.3) / 0.7, nx = L(0.6, 0.715); add('nose', [[nx, 0.35], [nx + 0.022 * k, 0.385], [nx, 0.4]]); }
  add('face', P([[0.35, 0.4], [0.4, 0.46], [0.5, 0.49], [0.6, 0.46], [0.65, 0.4]], [[0.43, 0.41], [0.49, 0.47], [0.58, 0.49], [0.67, 0.46], [0.72, 0.41]]));
  const n1 = L(0.46, 0.53), n2 = L(0.54, 0.61);
  add('neck', [[n1, 0.49], [n1, 0.55]]); add('neck', [[n2, 0.49], [n2, 0.55]]);
  add('body', P([[0.38, 0.8], [0.37, 0.6], [0.4, 0.56], [0.6, 0.56], [0.63, 0.6], [0.62, 0.8]], [[0.45, 0.8], [0.43, 0.6], [0.47, 0.56], [0.66, 0.56], [0.7, 0.6], [0.68, 0.8]]));
  add('body', P([[0.38, 0.8], [0.27, 1.12], [0.73, 1.12], [0.62, 0.8]], [[0.45, 0.8], [0.34, 1.11], [0.77, 1.13], [0.68, 0.8]]));
  add('body', P([[0.38, 0.8], [0.62, 0.8]], [[0.45, 0.8], [0.68, 0.8]]));
  const st = walk ? 0.05 * Math.sin(t * 2 * PI) : 0, l1 = L(0.44, 0.51), l2 = L(0.56, 0.64);
  add('legs', [[l1, 1.12], [l1 - st * 0.6, 1.44 + st]]); add('legs', [[l2, 1.12], [l2 + st * 0.6, 1.45 - st]]);
  add('legs', [[l1 - 0.03 - st * 0.6, 1.47 + st], [l1 + 0.02 - st * 0.6, 1.47 + st]]); add('legs', [[l2 - 0.01 + st * 0.6, 1.48 - st], [l2 + 0.05 + st * 0.6, 1.48 - st]]);
  return { g, heart: [L(0.53, 0.6), 0.68, 0.09] };
}

/** Every pose on the sheet. t: 0..1 cycle phase for walks. */
export function pose(name: string, t = 0): Rig {
  if (name === 'q_front' || name === 'q_frontwalk') return turn(1, t, name === 'q_frontwalk');
  const g: Record<string, Pt[][]> = {};
  const add = (k: string, pl: Pt[]) => (g[k] ??= []).push(pl);
  const sway = 0.02 * Math.sin(t * 2 * PI);
  let heart: [number, number, number] | undefined;
  if (name === 'front' || name === 'heart' || name === 'help' || name === 'frontwalk') {
    const r = turn(0, t, name === 'frontwalk');
    Object.assign(g, r.g); heart = r.heart;
    if (name === 'help') g.eyes = [[[0.42, 0.335]], [[0.58, 0.335]]];   // wide open: one 'o' each
    add('strands', [[0.36, 0.22], [0.39, 0.28]]); add('strands', [[0.5, 0.2], [0.5, 0.26]]); add('strands', [[0.64, 0.22], [0.61, 0.28]]);
    if (name === 'heart') { add('arms', [[0.38, 0.6], [0.34, 0.72], [0.46, 0.7]]); add('arms', [[0.62, 0.6], [0.66, 0.72], [0.54, 0.7]]); heart = [0.53, 0.68, 0.15]; }
    // arms up like \o/ , in front of the hair (group 'over' is rasterized on top of the other lines)
    if (name === 'help') { add('over', [[0.39, 0.58], [0.2, 0.45], [0.1, 0.27]]); add('over', [[0.61, 0.58], [0.8, 0.45], [0.9, 0.27]]); }
  } else if (name === 'q_back') {
    add('hair_out', [[0.22, 0.86], [0.2, 0.5], [0.22, 0.26], ...arc(0.5, 0.26, 0.28, 0.25, PI, 2 * PI, 16), [0.78, 0.5], [0.77, 0.86]]);
    add('hair_out', [[0.22, 0.86], [0.31, 0.9], [0.4, 0.86], [0.5, 0.9], [0.6, 0.86], [0.69, 0.9], [0.77, 0.86]]);
    add('face', [[0.78, 0.3], [0.82, 0.36], [0.79, 0.43]]);
    add('strands', [[0.57, 0.02], [0.57, 0.19]]);
    for (const x of [0.32, 0.44, 0.66]) add('strands', [[x, 0.32], [x + (0.55 - x) * 0.1, 0.8]]);
    add('body', [[0.4, 0.9], [0.31, 1.12], [0.74, 1.13], [0.64, 0.9]]);
    add('legs', [[0.46, 1.12], [0.46, 1.44]]); add('legs', [[0.59, 1.13], [0.6, 1.45]]);
    add('legs', [[0.43, 1.47], [0.48, 1.47]]); add('legs', [[0.57, 1.48], [0.62, 1.48]]);
  } else if (name === 'back' || name === 'backwalk') {
    add('hair_out', [[0.2, 0.84], [0.18, 0.5], [0.19, 0.24], ...arc(0.5, 0.26, 0.31, 0.25, PI, 2 * PI, 16), [0.81, 0.5], [0.8, 0.84]]);
    add('hair_out', [[0.2, 0.84], [0.3, 0.88], [0.4, 0.84], [0.5, 0.88], [0.6, 0.84], [0.7, 0.88], [0.8, 0.84]]);
    add('strands', [[0.5, 0.02], [0.5, 0.2]]);
    for (const x of [0.3, 0.4, 0.6, 0.7]) add('strands', [[x, 0.3], [x + (0.5 - x) * 0.1, 0.78]]);
    add('body', [[0.38, 0.88], [0.27, 1.12], [0.73, 1.12], [0.62, 0.88]]);
    const st = name === 'backwalk' ? 0.04 * Math.sin(t * 2 * PI) : 0;
    add('legs', [[0.44, 1.12], [0.44, 1.44 + st]]); add('legs', [[0.56, 1.12], [0.56, 1.44 - st]]);
    add('legs', [[0.41, 1.47 + st], [0.46, 1.47 + st]]); add('legs', [[0.54, 1.47 - st], [0.59, 1.47 - st]]);
  } else {
    // side view facing right: side, walk, run, jump, fall, stuck
    const lift = name === 'jump' ? 0.1 : name === 'fall' ? 0.3 : 0;
    const bx = 0.21 - (name === 'jump' ? 0.04 : 0) - (name === 'run' ? 0.05 : 0) + sway;
    add('hair_out', [[0.68, 0.24], [0.66, 0.12], [0.6, 0.05], [0.5, 0.02], [0.38, 0.04], [0.28, 0.12], [0.23, 0.26], [bx + 0.01, 0.5], [bx, 0.8 - lift]]);
    add('hair_out', [[bx, 0.8 - lift], [bx + 0.05, 0.84 - lift], [bx + 0.1, 0.8 - lift], [0.36, 0.83 - lift]]);
    if (name === 'fall') [0.3, 0.38, 0.46].forEach((x, k) => add('strands', [[x, 0.06], [x - 0.06 + 0.02 * k, -0.08]]));
    add('hair_in', [[0.36, 0.83 - lift], [0.39, 0.6], [0.43, 0.44], [0.46, 0.3], [0.52, 0.25], [0.68, 0.24]]);
    add('strands', [[0.56, 0.12], [0.54, 0.2]]); add('strands', [[0.44, 0.1], [0.4, 0.2]]);
    add('face', [[0.68, 0.24], [0.69, 0.29], [0.73, 0.34], [0.69, 0.36], [0.7, 0.4], [0.67, 0.45], [0.58, 0.47], [0.5, 0.46]]);
    add('eyes', [[0.59, 0.31], [0.64, 0.31]]);
    add('neck', [[0.52, 0.47], [0.52, 0.55]]); add('neck', [[0.6, 0.47], [0.6, 0.55]]);
    add('body', [[0.48, 0.8], [0.47, 0.6], [0.5, 0.56], [0.62, 0.56], [0.65, 0.6], [0.64, 0.8]]);
    add('body', [[0.48, 0.8], [0.4, 1.1], [0.75, 1.1], [0.64, 0.8]]);
    add('body', [[0.48, 0.8], [0.64, 0.8]]);
    if (name === 'fall') { add('arms', [[0.52, 0.58], [0.4, 0.44], [0.36, 0.3]]); add('arms', [[0.62, 0.58], [0.74, 0.44], [0.8, 0.32]]); }
    else if (name === 'stuck') add('arms', [[0.62, 0.6], [0.74, 0.62], [0.82, 0.58]]);
    else if (name === 'run') add('arms', [[0.6, 0.6], [0.7, 0.7], [0.78, 0.64]]);
    else add('arms', [[0.6, 0.6], [0.62, 0.74], [0.66, 0.82]]);
    if (name === 'walk' || name === 'run') {
      const a = (name === 'run' ? 0.55 : 0.32) * Math.sin(t * 2 * PI);
      for (const s of [1, -1]) {
        const hip: Pt = [0.57, 1.1], Lg = 0.36, foot: Pt = [hip[0] + Lg * Math.sin(s * a), hip[1] + Lg * Math.cos(s * a)];
        add('legs', [hip, foot]); add('legs', [foot, [foot[0] + 0.06, foot[1]]]);
      }
    } else if (name === 'jump') {
      add('legs', [[0.53, 1.1], [0.45, 1.3], [0.4, 1.31]]); add('legs', [[0.62, 1.1], [0.56, 1.28], [0.51, 1.29]]);
    } else {
      add('legs', [[0.53, 1.1], [0.53, 1.44]]); add('legs', [[0.62, 1.1], [0.62, 1.44]]);
      add('legs', [[0.53, 1.47], [0.58, 1.47]]); add('legs', [[0.62, 1.47], [0.67, 1.47]]);
    }
    heart = [0.58, 0.68, 0.09];
  }
  return { g, heart };
}

/** Seen from ~45 degrees above: the body shortens under the head, the parting shows. */
export function above(r: Rig): Rig {
  const ny = 0.5, k = 0.66, lift = 1.48 - (ny + (1.48 - ny) * 0.62);
  const g: Record<string, Pt[][]> = {};
  for (const [name, pls] of Object.entries(r.g)) g[name] = pls.map((pl) => pl.map(([x, y]) => [x, (y <= ny ? y : ny + (y - ny) * k) + lift] as Pt));
  (g.strands ??= []).push([[0.5, lift], [0.5, 0.12 + lift]]);
  const h = r.heart ? ([r.heart[0], ny + (r.heart[1] - ny) * 0.62 + lift, r.heart[2]] as [number, number, number]) : undefined;
  return { g, heart: h };
}

/** Polylines -> symbol per cell (key r * 256 + c), by the dominant stroke direction in the cell. */
export function raster(polys: Pt[][], cols = COLS, rows = ROWS, step = 0.18): Map<number, string> {
  const cw = 1 / cols, ch = 1.6 / rows;
  const acc = new Map<number, number[]>();
  for (const pl of polys) for (let i = 1; i < pl.length; i++) {
    const [x0, y0] = pl[i - 1]!, [x1, y1] = pl[i]!;
    const n = Math.max(1, Math.floor(Math.hypot((x1 - x0) / cw, (y1 - y0) / ch) / step));
    const ang = Math.atan2((y1 - y0) / ch, (x1 - x0) / cw);
    for (let k = 0; k <= n; k++) {
      const u = k / n, x = x0 + (x1 - x0) * u, y = y0 + (y1 - y0) * u;
      const c = Math.floor(x / cw), r = Math.floor(y / ch);
      const key = (r + 8) * 256 + c + 8;
      let a = acc.get(key);
      if (!a) { a = [0, 0, 0, 0]; acc.set(key, a); }
      a[0] += Math.cos(2 * ang); a[1] += Math.sin(2 * ang); a[2] += y / ch - r; a[3]! += 1;
    }
  }
  const out = new Map<number, string>();
  for (const [key, [ca, sa, fyS, n]] of acc) {
    const coh = Math.hypot(ca!, sa!) / n!;
    const th = (((Math.atan2(sa!, ca!) / 2) * 180) / PI + 180) % 180;
    const fy = fyS! / n!;
    let gl: string;
    if (coh < 0.12) gl = '+';
    else if (th < 22 || th > 158) gl = fy > 0.72 ? '_' : fy < 0.28 ? '`' : '-';
    else if (th > 68 && th < 112) gl = '|';
    else gl = th < 90 ? '\\' : '/';
    out.set(key, gl);
  }
  return out;
}

const HEART = ['/\\/\\', '\\  /', ' \\/ '];
/** Stroke weight (× cell height) and minimum stroke in px — BOLD since 2026-09-29 (Hon: "她几乎都看不太到 … 可能加粗"). */
export const GIRL_LW = 0.32, GIRL_MIN_PX = 2.4;
export interface GirlOpts {
  flip?: boolean; view?: 'above'; col?: string; hot?: string;
  /** stroke weight as a fraction of the cell height (default GIRL_LW) and its floor in px (default GIRL_MIN_PX) */
  lw?: number; minPx?: number;
  /** knockout: fill her silhouette with this colour first so nothing behind shows through her (default ink;
   *  pass the paper colour on paper levels, false for ghosts / after-images) */
  knock?: string | false;
  big?: number; noHeart?: boolean; sub?: (g: string, key: number) => string | null;
}
/**
 * Draw pose `name` (phase t) with the figure box's top-left at (x, y), `w` px wide (height 1.6 w).
 * Strokes go into `pen`; the knockout (if any) is painted immediately, so everything queued in `pen` before
 * this call is flushed first and stays underneath her. Flush `pen` yourself afterwards.
 */
export function drawGirl(pen: GlyphPen, name: string, t: number, x: number, y: number, w: number, o: GirlOpts = {}) {
  let rig = pose(name, t);
  if (o.view === 'above') rig = above(rig);
  const cw = w / COLS, ch = (w * 1.6) / ROWS, lw = Math.max(o.minPx ?? GIRL_MIN_PX, (o.lw ?? GIRL_LW) * ch);
  const col = o.col ?? '#EEE9DF', hot = o.hot ?? '#FF5314';
  const F = o.flip ? (pl: Pt[]) => pl.map(([px, py]) => [1 - px, py] as Pt) : (pl: Pt[]) => pl;
  const lines: Pt[][] = [];
  for (const [k, pls] of Object.entries(rig.g)) if (k !== 'eyes' && k !== 'nose' && k !== 'over') for (const pl of pls) lines.push(F(pl));
  const cells = raster(lines);
  if (rig.g.over) for (const [k, gl] of raster(rig.g.over.map(F))) cells.set(k, gl);
  const top = new Map<number, string>();
  const one = (px: number, py: number) => (Math.floor(py / (1.6 / ROWS)) + 8) * 256 + Math.floor(px * COLS) + 8;
  for (const pl0 of rig.g.eyes ?? []) {
    const pl = F(pl0);
    if (pl.length === 1) top.set(one(pl[0]![0], pl[0]![1]), 'o');
    else if (pl.length === 2 && Math.abs(pl[0]![1] - pl[1]![1]) < 1e-6) top.set(one((pl[0]![0] + pl[1]![0]) / 2, pl[0]![1]), '-');
    else for (const k of raster([pl]).keys()) top.set(k, 'o');
  }
  for (const pl0 of rig.g.nose ?? []) { const pl = F(pl0); top.set(one(pl[1]![0], pl[1]![1]), o.flip ? '<' : '>'); }
  for (const k of top.keys()) cells.delete(k);
  const knock = o.knock === undefined ? '#0A0A0B' : o.knock;
  if (knock) {
    // a stepped silhouette, row by row from her leftmost to her rightmost symbol, a little larger than her
    const rows = new Map<number, [number, number]>();
    for (const k of [...cells.keys(), ...top.keys()]) {
      const r = Math.floor(k / 256) - 8, cc = (k % 256) - 8, m = rows.get(r);
      rows.set(r, m ? [Math.min(m[0], cc), Math.max(m[1], cc)] : [cc, cc]);
    }
    pen.flush();
    const c = pen.c; c.fillStyle = knock;
    const px = Math.max(lw * 0.9, cw * 0.45);
    for (const [r, [c0, c1]] of rows) c.fillRect(x + c0 * cw - px, y + r * ch - px * 0.6, (c1 - c0 + 1) * cw + 2 * px, ch + px * 1.2);
  }
  const put = (key: number, gl0: string) => {
    const gl = o.sub ? o.sub(gl0, key) : gl0;
    if (!gl) return;
    const r = Math.floor(key / 256) - 8, c = (key % 256) - 8;
    pen.glyph(gl, x + c * cw, y + r * ch, cw, ch, col, lw);
  };
  for (const [k, gl] of cells) put(k, gl);
  for (const [k, gl] of top) put(k, gl);
  if (rig.heart && !o.noHeart) {
    let [hx, hy] = rig.heart;
    if (o.flip) hx = 1 - hx;
    const big = (o.big ?? 1) * (name === 'heart' ? 1.35 : 1);
    const hw = cw * 0.72 * big, hh = ch * 0.58 * big, hlw = Math.max(1.6, Math.min(lw * 0.95, hw * 0.42));
    const x0 = x + hx * w - 2 * hw, y0 = y + hy * w - 1.5 * hh;
    HEART.forEach((row, r) => { for (let c = 0; c < row.length; c++) if (row[c] !== ' ') pen.glyph(row[c]!, x0 + c * hw, y0 + r * hh, hw, hh, hot, hlw); });
  }
}
