// GAME MODE — 'plat': a side-scrolling platformer where everything is a symbol. The girl runs and jumps
// on the beat through a maze-like level (a ceiling of bricks with hanging spikes, pits of spikes, keys
// that click down on the beat, turrets firing rings of symbols). Each sung line puts its key word in her
// way as a building of [] bricks she runs across; it lights up when the word is sung. A HUD across the
// top and an RPG dialog box that types the line as it's sung.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { HEX } from '../engine/palette';
import { F, font } from '../engine/type';
import { hash, frameIdx } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { wordText } from '../danmaku/kinetic';
import { GlyphPen } from '../game/glyph';
import { drawGirl } from '../game/sprite';
import { wordTiles3 } from '../game/pixfont';
import type { Line } from '../engine/lyrics';

const T = 36;                        // tile px
const GROUND = 22;                   // ground surface row (y = 792)
const CEIL = 5;                      // ceiling row
const CW = 4.6, CH = 6.9;            // girl cell px -> 46 x 97
const BONE = HEX.bone, ASH = HEX.ash, GRAPH = HEX.graphite, SIG = HEX.signal, INK = HEX.ink;

const enum Tl { None, Ground, Word, Spike, Ladder, Bang, Key, Ceil, Hang }
interface Jump { t0: number; t1: number; h: number }
interface Build { line: Line; key: string; keyStart: number; x: number; w: number }

/** The word a line is about: HELP if it's there, else its longest word. */
export function keyWord(l: Line): { w: string; start: number } {
  const h = l.words.find((w) => /help/i.test(w.w));
  const best = h ?? [...l.words].sort((a, b) => wordText(b.w).length - wordText(a.w).length)[0]!;
  return { w: wordText(best.w), start: best.start };
}

export default class Plat extends Mode {
  bg = new FSPass(/* glsl */ `
    void main() { vec2 p = FRAG_PX; fragColor = vec4(C_INK * (1.0 + 0.35 * snoise(p * 0.002)), 1.0); }`);
  L = new Layer2D();
  map = new Map<number, Tl>();
  builds: Build[] = [];
  jumps: Jump[] = [];
  x0 = 4 * T; speed = 300;
  turrets: { x: number; y: number }[] = [];
  beats: number[] = [];

  k(c: number, r: number) { return c * 64 + r; }
  at(c: number, r: number): Tl { return this.map.get(this.k(c, r)) ?? Tl.None; }
  set(c: number, r: number, v: Tl) { this.map.set(this.k(c, r), v); }
  solid(v: Tl) { return v === Tl.Ground || v === Tl.Word || v === Tl.Bang || v === Tl.Key || v === Tl.Ceil; }

  init() {
    const { audio } = this.ctx;
    this.beats = audio.beats.filter((b) => b >= this.ctx.start - 1 && b <= this.ctx.end + 1);
    const colAt = (t: number) => Math.floor(this.herX(t) / T);
    const span = colAt(this.ctx.end) + 60;
    // each line's key word as a building on the ground, a few tiles ahead of her when the line starts
    for (const l of this.linesIn(this.ctx.start, this.ctx.end)) {
      const kw = keyWord(l);
      const { tiles, w } = wordTiles3(kw.w);
      const x = colAt(l.start) + 5;
      for (const [tc, tr] of tiles) this.set(x + tc, GROUND - 5 + tr, Tl.Word);
      this.builds.push({ line: l, key: kw.w, keyStart: kw.start, x, w });
    }
    const inBuild = (c: number) => this.builds.some((b) => c >= b.x - 3 && c < b.x + b.w + 3);
    // ground with pits between the buildings; spikes in every pit
    for (let c = -30; c < span; c++) {
      const pit = !inBuild(c) && hash(Math.floor(c / 9), 3) < 0.55 && c % 9 >= 6;
      if (pit) { this.set(c, GROUND + 3, Tl.Spike); continue; }
      for (let r = GROUND; r < GROUND + 9; r++) this.set(c, r, Tl.Ground);
    }
    // a ceiling of bricks with gaps and hanging spikes: she runs through a maze, not a field
    for (let c = -30; c < span; c++) {
      if (hash(Math.floor(c / 7), 5) < 0.2) continue;
      for (let r = 0; r <= CEIL; r++) this.set(c, r, Tl.Ceil);
      if (hash(c, 6) < 0.18) this.set(c, CEIL + 1, Tl.Hang);
    }
    // keys (click clack) as floating platforms, !-blocks, ladders
    for (let c = 8; c < span; c += 26) for (let j = 0; j < 5; j++) this.set(c + j * 2, GROUND - 9, Tl.Key);
    for (let c = 20; c < span; c += 17) this.set(c, GROUND - 4, Tl.Bang);
    for (let c = 30; c < span; c += 41) for (let r = CEIL + 1; r < GROUND; r++) this.set(c, r, Tl.Ladder);
    for (let c = 14; c < span; c += 29) this.turrets.push({ x: c * T + T / 2, y: (CEIL + 1.5) * T });
    // jumps: every two beats she leaps, higher on the downbeats
    for (let i = 0; i + 1 < this.beats.length; i += 2) {
      const t0 = this.beats[i]!, t1 = this.beats[i + 1]! + (this.beats[i + 1]! - t0) * 0.35;
      this.jumps.push({ t0, t1, h: i % 4 === 0 ? 4 * T : 2.6 * T });
    }
  }

  herX(t: number) { return this.x0 + (t - this.ctx.start) * this.speed; }
  /** Top of the solid ground under her (px), highest over her width. */
  floorAt(x: number) {
    let top = (GROUND + 3) * T;
    for (const dx of [-14, 0, 14]) {
      const c = Math.floor((x + dx) / T);
      for (let r = CEIL + 2; r < GROUND + 4; r++) if (this.solid(this.at(c, r))) { top = Math.min(top, r * T); break; }
    }
    return top;
  }
  herY(t: number) {
    const x = this.herX(t);
    let y = this.floorAt(x);
    for (const j of this.jumps) if (t >= j.t0 && t <= j.t1) {
      const u = (t - j.t0) / (j.t1 - j.t0);
      const from = this.floorAt(this.herX(j.t0)), to = this.floorAt(this.herX(j.t1));
      y = Math.min(from + (to - from) * u - j.h * 4 * u * (1 - u), y);
    }
    return y;
  }
  airborne(t: number) { return this.jumps.find((j) => t >= j.t0 && t <= j.t1); }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    this.bg.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const pen = new GlyphPen(c);
    const hx = this.herX(t), hy = this.herY(t);
    const camX = hx - W * 0.38;
    const kick = audio.hit('kick', t, 0.1);
    const lastBeat = [...this.beats].reverse().find((b) => b <= t) ?? -9;

    // ---- far field: faint dots and dashes, slow parallax
    for (let gy = 0; gy < 30; gy++) for (let gx = -1; gx < 56; gx++) {
      const wx = gx + Math.floor((camX * 0.25) / 36);
      const hsh = hash(wx, gy, 11);
      if (hsh > 0.3) continue;
      pen.glyph(hsh < 0.2 ? '.' : '-', wx * 36 - camX * 0.25 + 9, gy * 36 + 9, 18, 18, 'rgba(94,91,87,0.5)', 1.3);
    }
    pen.flush();
    // ---- a giant maze behind the level (half parallax): corridors of stacked bars
    const M = 216;
    for (let my = 0; my < 6; my++) for (let mx = -1; mx < 12; mx++) {
      const wx = mx + Math.floor((camX * 0.5) / M);
      const x = wx * M - camX * 0.5, y = my * M - 40;
      const a = 'rgba(94,91,87,0.28)';
      if (hash(wx, my, 21) < 0.5) for (let k = 0; k < 12; k++) pen.glyph('-', x + k * 18, y, 18, 18, a, 3);
      else for (let k = 0; k < 12; k++) pen.glyph('|', x, y + k * 18, 18, 18, a, 3);
    }
    pen.flush();

    // ---- level tiles (2 x 2 glyph cells each)
    const c0 = Math.floor(camX / T) - 1, c1 = c0 + Math.ceil(W / T) + 2, h2 = T / 2;
    for (let r = 0; r < GROUND + 9; r++) for (let cc = c0; cc <= c1; cc++) {
      const v = this.at(cc, r);
      if (!v) continue;
      const x = cc * T - camX, y = r * T;
      if (v === Tl.Ground) {
        const top = this.at(cc, r - 1) !== Tl.Ground;
        if (top) { pen.glyph('=', x, y - 5, h2, h2, BONE, 2.6); pen.glyph('=', x + h2, y - 5, h2, h2, BONE, 2.6); }
        else if ((cc + r) % 2 === 0) pen.glyph('/', x + 4, y + 4, T - 8, T - 8, 'rgba(94,91,87,0.7)', 1.6);
        if (top && this.at(cc - 1, r) === Tl.None) pen.glyph('|', x - h2 / 2, y, h2, T * 1.5, BONE, 2.2);
        if (top && this.at(cc + 1, r) === Tl.None) pen.glyph('|', x + T - h2 / 2, y, h2, T * 1.5, BONE, 2.2);
      } else if (v === Tl.Ceil) {
        const bottom = this.at(cc, r + 1) !== Tl.Ceil;
        if (bottom) { pen.glyph('=', x, y + h2 + 4, h2, h2, ASH, 2.4); pen.glyph('=', x + h2, y + h2 + 4, h2, h2, ASH, 2.4); }
        else if ((cc + r) % 3 === 0) pen.glyph('#', x + 6, y + 6, T - 12, T - 12, 'rgba(94,91,87,0.55)', 1.4);
      } else if (v === Tl.Hang) {
        pen.glyph('v', x, y, h2, h2, BONE, 2); pen.glyph('v', x + h2, y, h2, h2, BONE, 2);
      } else if (v === Tl.Word) {
        const b = this.builds.find((q) => cc >= q.x && cc < q.x + q.w);
        const lit = b && t >= b.keyStart - 0.02;
        const pop = lit ? Math.exp(-(t - b!.keyStart) * 7) : 0;
        const col = lit ? BONE : GRAPH;
        const yy = y - pop * 10;
        pen.glyph('[', x + 1, yy + 2, h2, T - 4, col, lit ? 2.8 : 2);
        pen.glyph(']', x + h2 - 1, yy + 2, h2, T - 4, col, lit ? 2.8 : 2);
      } else if (v === Tl.Spike) {
        pen.glyph('^', x, y, h2, h2, BONE, 2.2); pen.glyph('^', x + h2, y, h2, h2, BONE, 2.2);
      } else if (v === Tl.Ladder) {
        pen.glyph('H', x + 5, y, T - 10, T, 'rgba(156,151,143,0.8)', 2);
      } else if (v === Tl.Bang) {
        const bump = Math.exp(-((t - lastBeat) * 12)) * ((cc % 2) ? 8 : 0);
        pen.glyph('[', x, y - bump, h2, T, BONE, 2.4); pen.glyph(']', x + h2, y - bump, h2, T, BONE, 2.4);
        pen.glyph('!', x + h2 / 2, y + 5 - bump, h2, T - 10, BONE, 2.8);
      } else if (v === Tl.Key) {
        const down = Math.exp(-((t - lastBeat) * 10)) * (((cc / 2) | 0) % 2 === Math.round(lastBeat * 10) % 2 ? 7 : 0);
        pen.glyph('(', x - 2, y + down, h2 + 2, T - 6, BONE, 2.2); pen.glyph(')', x + h2, y + down, h2 + 2, T - 6, BONE, 2.2);
        pen.line(x + 6, y + T - 2 + down, x + T - 6, y + T - 2 + down, GRAPH, 2.4);
      }
    }
    pen.flush();
    c.font = font(F.mono(700), 15); c.fillStyle = BONE; c.textAlign = 'center'; c.textBaseline = 'middle';
    for (let cc = c0; cc <= c1; cc++) if (this.at(cc, GROUND - 9) === Tl.Key) {
      const down = Math.exp(-((t - lastBeat) * 10)) * (((cc / 2) | 0) % 2 === Math.round(lastBeat * 10) % 2 ? 7 : 0);
      c.fillText('QWERTYUIOPASDFGHJKL'[((cc % 19) + 19) % 19]!, cc * T - camX + T / 2, (GROUND - 9) * T + T / 2 - 2 + down);
    }

    // ---- turrets hanging from the ceiling, firing rings of symbols on the beat
    for (const tu of this.turrets) {
      const x = tu.x - camX, y = tu.y;
      if (x < -500 || x > W + 500) continue;
      pen.glyph('[', x - 20, y - 20, 20, 40, BONE, 2.6); pen.glyph(']', x, y - 20, 20, 40, BONE, 2.6); pen.glyph('o', x - 13, y - 13, 26, 26, BONE, 2.2);
      for (const b of this.beats) {
        const age = t - b;
        if (age < 0 || age > 1.4) continue;
        const n = 16, r = 34 + age * 480;
        for (let k = 0; k < n; k++) {
          const a = (k / n) * Math.PI * 2 + b * 3.1;
          pen.glyphAt(k % 2 ? 'o' : '+', x + Math.cos(a) * r, y + Math.sin(a) * r, 16, a, `rgba(238,233,223,${(0.9 * (1 - age / 1.4)).toFixed(2)})`, 2);
        }
      }
    }
    pen.flush();

    // ---- the heart to collect, bobbing over the next pit
    const hc = Math.ceil((hx + W * 0.35) / (9 * T)) * 9 * T + 7 * T - camX, hr = (GROUND - 3) * T + Math.sin(t * 5) * 8;
    pen.glyph('*', hc - 24, hr - 24, 48, 48, SIG, 4.2);
    pen.flush();

    // ---- the girl: after-images along her path, an ink outline, then her
    const air = this.airborne(t);
    const frame = air ? (t - air.t0 < (air.t1 - air.t0) * 0.5 ? 'jump' : 'fall') : ['run1', 'run2'][Math.floor(t * 8) % 2]!;
    for (let k = 3; k >= 1; k--) {
      const tt = t - k * 0.05;
      drawGirl(pen, frame, this.herX(tt) - camX - 23, this.herY(tt) - 14 * CH, CW, CH, { col: `rgba(238,233,223,${(0.1 * (4 - k)).toFixed(2)})`, hot: `rgba(255,83,20,${(0.18 * (4 - k)).toFixed(2)})` });
    }
    pen.flush();
    drawGirl(pen, frame, hx - camX - 23, hy - 14 * CH, CW, CH, { col: INK, hot: INK, lw: 0.42 });
    pen.flush();
    drawGirl(pen, frame, hx - camX - 23, hy - 14 * CH, CW, CH, { glitch: kick > 0.7 ? 0.25 : 0, seed: frameIdx(t), lw: 0.15 });
    pen.flush();

    // ---- HUD
    for (let k = 0; k < 3; k++) pen.glyph('*', 56 + k * 42, 38, 34, 34, SIG, 3.2);
    pen.flush();
    c.textBaseline = 'alphabetic';
    c.font = font(F.mono(700), 22); c.fillStyle = BONE; c.textAlign = 'left';
    c.fillText('x 03', 190, 64);
    c.textAlign = 'center'; c.fillText('STAGE 1-1  ·  STUCK IN A LIE', W / 2, 64);
    c.textAlign = 'right'; c.fillText(`TIME ${t.toFixed(2).padStart(6, '0')}`, W - 60, 64);
    c.font = font(F.mono(500), 15); c.fillStyle = ASH;
    c.fillText(`BAR ${Math.floor(f.bar) + 1}  ·  BEAT ${Math.floor(f.beatPhase * 4) + 1}`, W - 60, 88);
    // ---- dialog box: types the line as it's sung, her face in the corner
    const line = this.linesIn(t - 4, t + 0.01).filter((l) => l.start <= t).pop();
    const bx = 250, by = H - 200, bw = W - 500, bh = 140;
    c.fillStyle = INK; c.fillRect(bx, by, bw, bh);
    for (let x = bx + 9; x < bx + bw - 9; x += 18) { pen.glyph('-', x, by - 9, 18, 18, BONE, 2.2); pen.glyph('-', x, by + bh - 9, 18, 18, BONE, 2.2); }
    for (let y = by + 9; y < by + bh - 9; y += 18) { pen.glyph('|', bx - 9, y, 18, 18, BONE, 2.2); pen.glyph('|', bx + bw - 9, y, 18, 18, BONE, 2.2); }
    for (const [x, y] of [[bx, by], [bx + bw, by], [bx, by + bh], [bx + bw, by + bh]] as const) pen.glyph('+', x - 10, y - 10, 20, 20, BONE, 2.6);
    drawGirl(pen, 'front', bx + 26, by + 22, 7.4, 7, {});
    pen.flush();
    if (line) {
      c.font = font(F.mono(700), 44); c.textAlign = 'left'; c.textBaseline = 'middle';
      let x = bx + 140;
      for (const w of line.words) {
        if (t < w.start) break;
        const s = wordText(w.w), ww = c.measureText(s + ' ').width;
        const cur = t < w.end + 0.05;
        if (cur) { c.fillStyle = BONE; c.fillRect(x - 8, by + bh / 2 - 30, c.measureText(s).width + 16, 60); c.fillStyle = INK; } else c.fillStyle = BONE;
        c.fillText(s, x, by + bh / 2 + 2);
        x += ww;
      }
      if (Math.floor(t * 3) % 2) pen.glyph('v', bx + bw - 60, by + bh - 50, 24, 24, BONE, 2.6);
      pen.flush();
    }
    comp.draw(renderer, this.L.upload(), out);
    return { bloom: 0, halation: 0, ca: 0, grain: 0.03, vignette: 0.15, shake: [0, kick * 3] };
  }
}
