// SHOT — 'engrave' (copperplate engraving). One idea: stuck inside the lie.
// The key word (default: the last word of the line, LIE) is a labyrinth: every letter is filled with a
// maze, drawn as an engraving (ink walls, hatched shadows, a field of engraved rules around the
// letters). One orange mark sits at a dead end, with the orange hairline of the way it came. The shot
// opens tight on the mark and snaps back on every sung word until the whole word is in view.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { LineBatch } from '../engine/lines';
import { LIN, rgba } from '../engine/palette';
import { F, font, measure, textPath2D } from '../engine/type';
import { clamp, ease, hash, lerp, mulberry32 } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { wordText } from '../danmaku/kinetic';
import { CLEAN } from './poster';

const CELL = 26;
type Seg = [number, number, number, number];

export default class Engrave extends Mode {
  bg = new FSPass(/* glsl */ `
    uniform sampler2D mask; uniform vec2 maskSize, cam; uniform float zoom;
    void main() {
      vec2 p = FRAG_PX; p.y = ${H.toFixed(1)} - p.y;
      vec2 w = (p - vec2(${(W / 2).toFixed(1)}, ${(H / 2).toFixed(1)})) / zoom + cam;     // world px
      vec2 mu = w / maskSize;
      float inside = (mu.x > 0.0 && mu.y > 0.0 && mu.x < 1.0 && mu.y < 1.0) ? texture(mask, vec2(mu.x, 1.0 - mu.y)).a : 0.0;
      // engraved rules around the letters: horizontal lines whose weight swells with a slow tone field
      float spacing = 5.0;
      float tone = 0.45 + 0.35 * snoise(w * 0.0025) + 0.15 * snoise(w * 0.011);
      float wv = sin(w.x * 0.013 + snoise(w * 0.004) * 2.0) * 1.2;
      float d = abs(fract((w.y + wv) / spacing) - 0.5) * spacing * zoom;      // distance to the rule, screen px
      float halfw = clamp(tone, 0.12, 0.9) * 0.5 * spacing * zoom * 0.5;
      float rule = 1.0 - smoothstep(halfw - 0.6, halfw + 0.6, d);
      vec3 paper = C_BONE * (0.97 + 0.02 * snoise(p * 0.8));
      vec3 col = mix(paper, C_INK * 1.5, rule * (1.0 - inside) * 0.92);
      fragColor = vec4(col, 1.0);
    }`, { mask: { value: null }, maskSize: { value: new THREE.Vector2(1, 1) }, cam: { value: new THREE.Vector2() }, zoom: { value: 1 } });
  lb = new LineBatch(90000, { blend: 'normal' });
  L = new Layer2D();
  word = 'LIE';
  walls: Seg[] = [];
  hatch: Seg[] = [];
  trail: [number, number][] = [];
  dot: [number, number] = [0, 0];
  size = 800; ox = 0; oy = 0; mw = 0; mh = 0;
  outline!: Path2D;

  init() {
    const lines = this.linesIn();
    const l0 = lines[0];
    this.word = wordText(this.ctx.params.word ?? l0?.words[l0.words.length - 1]?.w ?? 'LIE');
    const fam = F.archivo(125, 900);
    this.size = Math.min(900, (1640 / measure(this.word, fam, 100)) * 100);
    const tw = measure(this.word, fam, this.size);
    this.mw = Math.ceil(tw + 120); this.mh = Math.ceil(this.size * 1.05);
    const base = this.size * 0.86;
    this.ox = 60; this.oy = base;
    const cv = document.createElement('canvas'); cv.width = this.mw; cv.height = this.mh;
    const m = cv.getContext('2d', { willReadFrequently: true })!;
    m.font = font(fam, this.size); m.fillStyle = '#fff'; m.textBaseline = 'alphabetic';
    m.fillText(this.word, this.ox, this.oy);
    const img = m.getImageData(0, 0, this.mw, this.mh).data;
    const tex = new THREE.CanvasTexture(cv); tex.flipY = true; tex.needsUpdate = true;
    this.bg.u.mask!.value = tex; (this.bg.u.maskSize!.value as THREE.Vector2).set(this.mw, this.mh);
    this.outline = textPath2D(this.word, fam, this.size, this.ox, this.oy);

    // ---- maze on the cells inside the letters
    const cols = Math.floor(this.mw / CELL), rows = Math.floor(this.mh / CELL);
    const inside = (cx: number, cy: number) => {
      let n = 0;
      for (const [dx, dy] of [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75], [0.5, 0.5]]) {
        const x = Math.floor((cx + dx!) * CELL), y = Math.floor((cy + dy!) * CELL);
        if (img[(y * this.mw + x) * 4 + 3]! > 128) n++;
      }
      return n >= 4;
    };
    const IN = new Array(cols * rows).fill(false);
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) IN[r * cols + c] = inside(c, r);
    const open = new Set<string>();
    const seen = new Array(cols * rows).fill(false);
    const rnd = mulberry32(11);
    const comps: number[][] = [];
    for (let s = 0; s < cols * rows; s++) {
      if (!IN[s] || seen[s]) continue;
      const comp: number[] = [];
      const stack = [s]; seen[s] = true;
      while (stack.length) {
        const cur = stack[stack.length - 1]!; comp.push(cur);
        const c = cur % cols, r = Math.floor(cur / cols);
        const nb = [[c + 1, r], [c - 1, r], [c, r + 1], [c, r - 1]].filter(([x, y]) => x! >= 0 && y! >= 0 && x! < cols && y! < rows && IN[y! * cols + x!] && !seen[y! * cols + x!]);
        if (!nb.length) { stack.pop(); continue; }
        const [x, y] = nb[Math.floor(rnd() * nb.length)]!;
        const n = y! * cols + x!;
        open.add(`${Math.min(cur, n)}-${Math.max(cur, n)}`);
        seen[n] = true; stack.push(n);
      }
      comps.push(comp);
    }
    const isOpen = (a: number, b: number) => open.has(`${Math.min(a, b)}-${Math.max(a, b)}`);
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      const i = r * cols + c;
      if (!IN[i]) continue;
      const x0 = c * CELL, y0 = r * CELL, x1 = x0 + CELL, y1 = y0 + CELL;
      // right and bottom walls (left/top come from the neighbour, or the outline if it's outside)
      const R = c + 1 < cols ? i + 1 : -1, B = r + 1 < rows ? i + cols : -1, Lf = c > 0 ? i - 1 : -1, T = r > 0 ? i - cols : -1;
      if (R < 0 || !IN[R] || !isOpen(i, R)) this.walls.push([x1, y0, x1, y1]);
      if (B < 0 || !IN[B] || !isOpen(i, B)) this.walls.push([x0, y1, x1, y1]);
      if (Lf < 0 || !IN[Lf]) this.walls.push([x0, y0, x0, y1]);
      if (T < 0 || !IN[T]) this.walls.push([x0, y0, x1, y0]);
    }
    // hatched shadow under/right of every wall (the engraver's relief)
    for (const [x0, y0, x1, y1] of this.walls) {
      const horiz = y0 === y1;
      for (let k = 1; k <= 4; k++) {
        if (horiz) { const x = x0 + (k / 5) * (x1 - x0); this.hatch.push([x, y0 + 2, x + 6, y0 + 8]); }
        else { const y = y0 + (k / 5) * (y1 - y0); this.hatch.push([x0 + 2, y, x0 + 8, y + 6]); }
      }
    }
    // ---- the orange mark: a dead end in the middle letter, and the way it came
    const comp = comps.length ? comps.sort((a, b) => b.length - a.length).find((cmp) => { const c0 = cmp[0]! % cols; return c0 > cols * 0.3 && c0 < cols * 0.7; }) ?? comps[0]! : [];
    if (comp.length) {
      const adj = (i: number) => [i + 1, i - 1, i + cols, i - cols].filter((n) => n >= 0 && n < cols * rows && IN[n] && isOpen(i, n));
      const bfs = (s: number) => { const prev = new Map<number, number>([[s, -1]]); const q = [s]; let last = s; while (q.length) { const u = q.shift()!; last = u; for (const v of adj(u)) if (!prev.has(v)) { prev.set(v, u); q.push(v); } } return { prev, last }; };
      const a = bfs(comp[0]!).last, { prev, last } = bfs(a);
      const path: number[] = []; for (let u = last; u >= 0; u = prev.get(u)!) path.push(u);
      this.trail = path.map((i) => [(i % cols + 0.5) * CELL, (Math.floor(i / cols) + 0.5) * CELL]);
      this.dot = this.trail[0]!;
    }
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp } = this.ctx;
    const t = f.t;
    const ws = this.wordsIn();
    // camera: tight on the mark, one snap back per sung word
    const zs = [7, 4.3, 2.7, 1.75, 1.0];
    let zi = 0;
    ws.forEach((w, i) => { if (t >= w.start - 0.02) zi = Math.min(zs.length - 1, i + 1); });
    if (ws.length && ws.length < zs.length - 1 && t >= ws[ws.length - 1]!.start - 0.02) zi = zs.length - 1;
    const tw = ws[zi - 1]?.start ?? this.ctx.start;
    const k = ease.outExpo(clamp((t - tw) / 0.28));
    const zFrom = zs[Math.max(0, zi - 1)]!, zTo = zs[zi]!;
    let z = zi === 0 ? zs[0]! : lerp(zFrom, zTo, k);
    const lastW = ws[ws.length - 1];
    if (lastW && t > lastW.end) z *= 1 - 0.07 * ease.outCubic(clamp((t - lastW.end) / 1.2));
    const u = clamp((z - 1) / (zs[0]! - 1));
    const mc: [number, number] = [this.mw / 2, this.mh / 2 + 40];
    const cx = lerp(mc[0], this.dot[0], u), cy = lerp(mc[1], this.dot[1], u);
    this.bg.u.zoom!.value = z; (this.bg.u.cam!.value as THREE.Vector2).set(cx, cy);
    this.bg.render(renderer, out);

    const X = (x: number) => W / 2 + (x - cx) * z, Y = (y: number) => H / 2 + (y - cy) * z;
    const lwWall = 2.4 * Math.pow(z, 0.55), lwH = 0.9 * Math.pow(z, 0.5);
    const ink = LIN.ink, sig: [number, number, number] = [LIN.signal[0] * 1.05, LIN.signal[1] * 1.05, LIN.signal[2] * 1.05];
    this.lb.clear();
    const vis = (x0: number, y0: number, x1: number, y1: number) => !(Math.max(X(x0), X(x1)) < -20 || Math.min(X(x0), X(x1)) > W + 20 || Math.max(Y(y0), Y(y1)) < -20 || Math.min(Y(y0), Y(y1)) > H + 20);
    for (const [x0, y0, x1, y1] of this.hatch) if (vis(x0, y0, x1, y1)) this.lb.seg2(X(x0), Y(y0), X(x1), Y(y1), lwH, ink, 0.55);
    for (const [x0, y0, x1, y1] of this.walls) if (vis(x0, y0, x1, y1)) this.lb.seg2(X(x0), Y(y0), X(x1), Y(y1), lwWall, ink, 1);
    // the orange way it came, and the mark at its dead end
    for (let i = 1; i < this.trail.length; i++) {
      const a = this.trail[i - 1]!, b = this.trail[i]!;
      this.lb.seg2(X(a[0]), Y(a[1]), X(b[0]), Y(b[1]), 1.6 * Math.pow(z, 0.5), sig, 0.95);
    }
    const r = 6 * Math.pow(z, 0.6);
    this.lb.seg2(X(this.dot[0]), Y(this.dot[1]), X(this.dot[0]) + 0.01, Y(this.dot[1]), r * 2, sig, 1);
    this.lb.render(renderer, out);

    // letter outlines (double engraved rule) and, once the whole word is in view, the cartouche
    const c = this.L.ctx; this.L.clear();
    c.save(); c.setTransform(z, 0, 0, z, W / 2 - cx * z, H / 2 - cy * z);
    c.lineWidth = 3.2 / Math.pow(z, 0.5); c.strokeStyle = rgba('ink', 1); c.stroke(this.outline);
    c.restore();
    const reveal = clamp((1.35 - z) / 0.3);
    if (reveal > 0 && this.linesIn()[0]) {
      const text = this.linesIn()[0]!.text.toUpperCase().replace(/[.,]/g, '');
      const y = Y(this.mh + 50);
      c.globalAlpha = reveal;
      c.font = font(F.serif(600, true), 46); c.textAlign = 'center'; c.textBaseline = 'middle';
      c.fillStyle = rgba('ink', 1);
      const tw2 = measure(text, F.serif(600, true), 46);
      c.fillText(text, W / 2, y);
      c.lineWidth = 1; c.strokeStyle = rgba('ink', 1);
      c.beginPath(); c.moveTo(W / 2 - tw2 / 2 - 60, y - 34); c.lineTo(W / 2 + tw2 / 2 + 60, y - 34); c.moveTo(W / 2 - tw2 / 2 - 60, y + 32); c.lineTo(W / 2 + tw2 / 2 + 60, y + 32); c.stroke();
      c.font = font(F.mono(500), 13); c.fillStyle = rgba('ink', 0.7);
      c.fillText('A MAP OF THE INSIDE OF A LIE   ·   ONE WAY IN   ·   NO WAY OUT', W / 2, y + 56);
      c.globalAlpha = 1;
    }
    comp.draw(renderer, this.L.upload(), out);

    return { ...CLEAN, paper: 1, vignette: 0.12, grain: 0.03 };
  }
}
void hash;
