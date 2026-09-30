// KEYFRAME 3 — the maze from above ("Stuck in a lie"). A labyrinth of symbol walls ( | - + ) whose
// shape, seen from this high, is the word LIE; she's tiny, at a dead end inside the I, the dotted trail of
// where she's been behind her; the light of her lamp is the only part of the maze that's clear, the rest
// sinks into dim symbols. A minimap in the corner, the HUD, the dialog box.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { F, font } from '../engine/type';
import { hash, mulberry32, clamp } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { GlyphPen } from '../game/glyph';
import { drawGirl } from '../game/girl';
import { PIX } from '../game/pixfont';
import { C, hud, dialog, symBox, symHeart } from '../game/world';

const CELL = 34;                         // maze cell px
const K = 3;                             // maze cells per font pixel

export default class KfMaze extends Mode {
  bg = new FSPass(/* glsl */ `void main() { vec2 p = FRAG_PX; fragColor = vec4(C_INK * (1.0 + 0.3 * snoise(p * 0.003)), 1.0); }`);
  L = new Layer2D();
  cols = 0; rows = 0; ox = 0; oy = 0;
  inside: boolean[] = [];
  open = new Set<string>();        // passages "a|b"
  path: number[] = [];             // entrance -> her dead end
  her = 0;

  init() {
    const word = 'LIE';
    const glyphs = [...word].map((ch) => PIX[ch]!);
    const fw = glyphs.length * 5 + (glyphs.length - 1) * 1;
    this.cols = fw * K; this.rows = 7 * K;
    this.ox = Math.round((W - this.cols * CELL) / 2); this.oy = 150;
    this.inside = new Array(this.cols * this.rows).fill(false);
    glyphs.forEach((g, li) => g.forEach((row, r) => { for (let c = 0; c < 5; c++) if (row[c] === '#') for (let a = 0; a < K; a++) for (let b = 0; b < K; b++) this.inside[(r * K + a) * this.cols + (li * 6 + c) * K + b] = true; }));
    // a maze through every cell of the letters (DFS), each letter its own region
    const rnd = mulberry32(7);
    const seen = new Array(this.cols * this.rows).fill(false);
    const nb = (i: number) => {
      const x = i % this.cols, y = (i / this.cols) | 0, out: number[] = [];
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]] as const) {
        const nx = x + dx, ny = y + dy;
        if (nx >= 0 && ny >= 0 && nx < this.cols && ny < this.rows && this.inside[ny * this.cols + nx]) out.push(ny * this.cols + nx);
      }
      return out;
    };
    const parent = new Map<number, number>();
    for (let s = 0; s < this.inside.length; s++) {
      if (!this.inside[s] || seen[s]) continue;
      const st = [s]; seen[s] = true;
      while (st.length) {
        const cur = st[st.length - 1]!;
        const cand = nb(cur).filter((n) => !seen[n]);
        if (!cand.length) { st.pop(); continue; }
        const n = cand[Math.floor(rnd() * cand.length)]!;
        seen[n] = true; parent.set(n, cur);
        this.open.add(cur < n ? `${cur}|${n}` : `${n}|${cur}`);
        st.push(n);
      }
    }
    // her: the dead end in the I farthest (in the tree) from the I's bottom-left cell
    const iCol0 = 6 * K, iCells = this.inside.map((v, i) => v && (i % this.cols) >= iCol0 && (i % this.cols) < iCol0 + 5 * K);
    const root = (this.rows - 1) * this.cols + iCol0 + 1 * K;
    const depth = new Map<number, number>([[root, 0]]); const q = [root]; const from = new Map<number, number>();
    while (q.length) {
      const cur = q.shift()!;
      for (const n of nb(cur)) {
        const key = cur < n ? `${cur}|${n}` : `${n}|${cur}`;
        if (!this.open.has(key) || depth.has(n)) continue;
        depth.set(n, depth.get(cur)! + 1); from.set(n, cur); q.push(n);
      }
    }
    let best = root;
    for (const [i, d] of depth) if (iCells[i] && d > (depth.get(best) ?? 0) && nb(i).filter((n) => this.open.has(i < n ? `${i}|${n}` : `${n}|${i}`)).length === 1) best = i;
    this.her = best;
    const path = [best];
    while (from.has(path[path.length - 1]!)) path.push(from.get(path[path.length - 1]!)!);
    this.path = path.reverse();
    void parent;
  }

  cx(i: number) { return this.ox + ((i % this.cols) + 0.5) * CELL; }
  cy(i: number) { return this.oy + (((i / this.cols) | 0) + 0.5) * CELL; }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    this.bg.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const pen = new GlyphPen(c);
    const hx = this.cx(this.her), hy = this.cy(this.her);
    const lamp = (x: number, y: number) => clamp(1 - Math.hypot(x - hx, y - hy) / 460) ** 0.7;
    // rock outside the letters: dim hatching
    for (let y = this.oy - 3 * CELL; y < H; y += CELL) for (let x = this.ox - 6 * CELL; x < W + CELL; x += CELL) {
      const gx = Math.floor((x - this.ox) / CELL), gy = Math.floor((y - this.oy) / CELL);
      if (gx >= 0 && gy >= 0 && gx < this.cols && gy < this.rows && this.inside[gy * this.cols + gx]) continue;
      if (hash(gx, gy, 3) < 0.55) pen.glyph(hash(gx, gy, 4) < 0.5 ? '/' : '.', x + 7, y + 7, CELL - 14, CELL - 14, `rgba(94,91,87,${(0.25 + 0.3 * lamp(x, y)).toFixed(2)})`, 1.4);
    }
    pen.flush();
    // walls: every cell edge without a passage; the letters' own outline heavier
    const wallCol = (x: number, y: number, outer: boolean) => {
      const k = lamp(x, y);
      return outer ? `rgba(238,233,223,${(0.32 + 0.68 * k).toFixed(2)})` : `rgba(238,233,223,${(0.08 + 0.92 * k).toFixed(2)})`;
    };
    for (let i = 0; i < this.inside.length; i++) {
      if (!this.inside[i]) continue;
      const x = this.ox + (i % this.cols) * CELL, y = this.oy + ((i / this.cols) | 0) * CELL;
      const xx = i % this.cols, yy = (i / this.cols) | 0;
      const edge = (n: number, ok: boolean) => ok && this.inside[n] ? !this.open.has(i < n ? `${i}|${n}` : `${n}|${i}`) : true;
      const outerR = !(xx + 1 < this.cols && this.inside[i + 1]), outerD = !(yy + 1 < this.rows && this.inside[i + this.cols]);
      const outerL = !(xx > 0 && this.inside[i - 1]), outerU = !(yy > 0 && this.inside[i - this.cols]);
      if (edge(i + 1, xx + 1 < this.cols)) pen.glyph('|', x + CELL - CELL / 2, y, CELL, CELL, wallCol(x + CELL, y, outerR), outerR ? 3.2 : 2.2);
      if (edge(i + this.cols, yy + 1 < this.rows)) pen.glyph('-', x, y + CELL / 2, CELL, CELL, wallCol(x, y + CELL, outerD), outerD ? 3.2 : 2.2);
      if (outerL) pen.glyph('|', x - CELL / 2, y, CELL, CELL, wallCol(x, y, true), 3.2);
      if (outerU) pen.glyph('-', x, y - CELL / 2, CELL, CELL, wallCol(x, y, true), 3.2);
      // corners
      if (hash(i, 9) < 0.5) pen.glyph('+', x + CELL - 7, y + CELL - 7, 14, 14, wallCol(x, y, false), 1.6);
    }
    pen.flush();
    // the trail: dots along her path from the entrance, the newest brightest
    const n = this.path.length;
    this.path.forEach((i, k) => {
      if (k === n - 1) return;
      const a = 0.25 + 0.75 * (k / n);
      pen.glyph('.', this.cx(i) - 8, this.cy(i) - 12, 16, 16, `rgba(238,233,223,${a.toFixed(2)})`, 3.2);
    });
    pen.flush();
    // her, seen from above, facing down the corridor she came from (bold, knocked out over the walls)
    const s = 52, bob = Math.sin(t * 6) * 1.5;
    drawGirl(pen, 'front', 0, hx - s / 2, hy - s * 0.9 + bob, s, { view: 'above' });
    pen.flush();
    const beat = Math.exp(-(t - (audio.beats.filter((b) => b <= t).pop() ?? -9)) * 6);
    // a zoom callout in the empty bay of the L, a dotted leader line from her to it: so you can see her
    const bx = 290, by = 320, bw = 310, bh = 400;
    for (let k = 1; k < 16; k++) { const u = k / 16; pen.glyph('.', hx - s * 0.3 + (bx + bw - 20 - (hx - s * 0.3)) * u - 8, hy + 8 + (by + 20 - hy - 8) * u - 12, 16, 16, C.bone, 3.4); }
    pen.flush();
    c.fillStyle = C.ink; c.fillRect(bx, by, bw, bh);
    symBox(pen, bx, by, bw, bh, C.bone, 18, 2.6);
    pen.flush();
    const zs = 176;
    drawGirl(pen, 'front', 0, bx + bw / 2 - zs / 2, by + 62, zs, {});
    pen.glyph('?', bx + bw / 2 - 16, by + 12 - beat * 5, 32, 46, C.bone, 4);
    pen.flush();
    c.font = font(F.mono(700), 20); c.fillStyle = C.bone; c.textAlign = 'center'; c.textBaseline = 'alphabetic';
    c.fillText('P1  ·  DEAD END', bx + bw / 2, by + bh - 22);
    // minimap (top right): the whole LIE maze, her blinking
    const mm = 4, mx = W - 44 - this.cols * mm, my = H - 178;
    c.fillStyle = C.ink; c.fillRect(mx - 14, my - 14, this.cols * mm + 28, this.rows * mm + 28);
    symBox(pen, mx - 14, my - 14, this.cols * mm + 28, this.rows * mm + 28, C.ash, 12, 1.6);
    for (let i = 0; i < this.inside.length; i++) if (this.inside[i]) { c.fillStyle = 'rgba(156,151,143,0.35)'; c.fillRect(mx + (i % this.cols) * mm, my + ((i / this.cols) | 0) * mm, mm - 1, mm - 1); }
    for (const i of this.path) { c.fillStyle = 'rgba(238,233,223,0.8)'; c.fillRect(mx + (i % this.cols) * mm + 1, my + ((i / this.cols) | 0) * mm + 1, mm - 3, mm - 3); }
    if (Math.floor(t * 4) % 2) symHeart(pen, mx + (this.her % this.cols) * mm + 2, my + ((this.her / this.cols) | 0) * mm + 2, 3.4);
    pen.flush();
    c.font = font(F.mono(500), 13); c.fillStyle = C.ash; c.textAlign = 'left'; c.textBaseline = 'alphabetic';
    c.fillText('YOU ARE HERE  ·  EXITS 0', mx - 14, my - 22);
    hud(c, pen, W, { stage: 'FLOOR 2  ·  STUCK IN A LIE', t, bar: Math.floor(f.bar) + 1, beat: Math.floor(f.beatPhase * 4) + 1, lives: 2 });
    const line = this.linesIn(t - 4, t + 0.01).filter((l) => l.start <= t).pop();
    dialog(c, pen, line, t, { x: 170, y: H - 196, w: W - 520, h: 136 });
    comp.draw(renderer, this.L.upload(), out);
    return { bloom: 0, halation: 0, ca: 0, grain: 0.03, vignette: 0.2 };
  }
}
