// KEYFRAMES 1 & 2 — the 2D platformer.
//  'keys' (pre-chorus, "I hear the keys go click clack"): she leaps across a row of giant keyboard keys
//         over a spike pit; each key clicks down when it's hit, CLICK / CLACK burst out of them in outlined
//         pixel letters; a ceiling maze with hanging spikes and a turret firing rings of symbols.
//  'help' (the chorus hit): the whole picture flips to paper: the word HELP stands across the level as a
//         building of [ ] bricks, she's on top of the P with her arms up, turrets on both sides fire.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { F, font } from '../engine/type';
import { clamp, ease, hash } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { GlyphPen } from '../game/glyph';
import { drawGirl } from '../game/girl';
import { C, farField, bigMaze, hud, dialog, brickWord, outlineWord, symBox } from '../game/world';

export default class KfPlat extends Mode {
  bg = new FSPass(/* glsl */ `void main() { vec2 p = FRAG_PX; fragColor = vec4(C_INK * (1.0 + 0.35 * snoise(p * 0.002)), 1.0); }`);
  L = new Layer2D();
  beats: number[] = [];

  init() { this.beats = this.ctx.audio.beats.filter((b) => b > this.ctx.start - 2 && b < this.ctx.end + 2); }
  lastBeat(t: number) { return [...this.beats].reverse().find((b) => b <= t) ?? -9; }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    this.bg.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const pen = new GlyphPen(c);
    const v = this.param<string>(t, 'variant', 'keys');
    if (v === 'help') this.help(c, pen, f); else this.keys(c, pen, f);
    comp.draw(renderer, this.L.upload(), out);
    const kick = audio.hit('kick', t, 0.1);
    return { bloom: 0, halation: 0, ca: 0, grain: 0.03, vignette: 0.15, shake: [0, kick * 4] };
  }

  // ------------------------------------------------------------------ 'keys'
  keys(c: CanvasRenderingContext2D, pen: GlyphPen, f: Frame) {
    const t = f.t, lb = this.lastBeat(t), since = t - lb;
    const scroll = (t - this.ctx.start) * 140;
    farField(pen, W, H, scroll * 0.25, 11);
    pen.flush();
    bigMaze(pen, W, H, scroll * 0.5);
    pen.flush();
    // ceiling: hatched bricks with hanging spikes
    for (let x = -20; x < W + 40; x += 36) {
      for (let y = 100; y < 190; y += 36) pen.glyph((((x / 36) | 0) + ((y / 36) | 0)) % 2 ? '#' : '/', x + 6, y + 6, 24, 24, 'rgba(94,91,87,0.6)', 1.4);
      pen.glyph('=', x, 186, 18, 18, C.ash, 2.4); pen.glyph('=', x + 18, 186, 18, 18, C.ash, 2.4);
      if (hash(Math.floor(x / 36), 4) < 0.35) { pen.glyph('v', x, 204, 18, 18, C.bone, 2.2); pen.glyph('v', x + 18, 204, 18, 18, C.bone, 2.2); }
    }
    // ground left and right, the pit between with spikes at the bottom
    const gy = 800;
    const ground = (x0: number, x1: number) => {
      for (let x = x0; x < x1; x += 36) {
        pen.glyph('=', x, gy - 5, 18, 18, C.bone, 2.6); pen.glyph('=', x + 18, gy - 5, 18, 18, C.bone, 2.6);
        for (let y = gy + 36; y < H + 36; y += 36) if (((x / 36) | 0) % 2 === ((y / 36) | 0) % 2) pen.glyph('/', x + 4, y - 30, 28, 28, 'rgba(94,91,87,0.7)', 1.6);
      }
      pen.glyph('|', x0 - 9, gy, 18, 54, C.bone, 2.2); pen.glyph('|', x1 - 9, gy, 18, 54, C.bone, 2.2);
    };
    ground(-40, 380); ground(1560, W + 40);
    for (let x = 380; x < 1560; x += 18) pen.glyph('^', x, 1032, 18, 18, C.bone, 2.2);
    // a ladder and a !-block on the right
    for (let y = 460; y < gy; y += 36) pen.glyph('H', 1700, y, 26, 36, 'rgba(156,151,143,0.85)', 2);
    pen.glyph('[', 1780, 600, 18, 36, C.bone, 2.4); pen.glyph(']', 1798, 600, 18, 36, C.bone, 2.4); pen.glyph('!', 1789, 604, 18, 28, C.bone, 2.8);
    pen.flush();
    // the keys: a row of big keycaps over the pit; the one she just left is down
    const letters = 'CLICKS';
    const kx0 = 440, kw = 150, kh = 104, ky = 650, gapK = 38;
    const herKey = 2;
    for (let i = 0; i < letters.length; i++) {
      const x = kx0 + i * (kw + gapK);
      const down = i === herKey ? 16 * Math.exp(-since * 5) + 6 : ((i + Math.floor(t * 4)) % 5 === 0 ? 8 : 0);
      const y = ky + down;
      // keycap: rounded box of symbols, a lip line under it
      for (let px = x + 18; px < x + kw - 18; px += 18) { pen.glyph('`', px, y, 18, 18, C.bone, 2.4); pen.glyph('_', px, y + kh - 18, 18, 18, C.bone, 2.4); }
      for (let py = y + 18; py < y + kh - 18; py += 18) { pen.glyph('|', x - 9, py, 18, 18, C.bone, 2.4); pen.glyph('|', x + kw - 9, py, 18, 18, C.bone, 2.4); }
      pen.glyph('/', x - 9, y, 18, 18, C.bone, 2.4); pen.glyph('\\', x + kw - 9, y, 18, 18, C.bone, 2.4);
      pen.glyph('\\', x - 9, y + kh - 18, 18, 18, C.bone, 2.4); pen.glyph('/', x + kw - 9, y + kh - 18, 18, 18, C.bone, 2.4);
      for (let px = x + 10; px < x + kw - 10; px += 18) pen.glyph('_', px, y + kh + 4 - down * 0.5, 18, 18, C.graphite, 2);
      outlineWord(pen, letters[i]!, x + kw / 2 - 25, y + 22, 10, C.bone, 1.8);
    }
    pen.flush();
    // CLICK / CLACK bursting out of the keys
    const burst = (word: string, x: number, y: number, age: number, rot: number) => {
      if (age < 0 || age > 0.5) return;
      const s = 0.62 + 0.25 * ease.outBack(clamp(age / 0.12));
      c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
      outlineWord(pen, word, -((word.length * 6 - 1) * 12) / 2, -42, 12, C.bone, 2.4);
      for (let k = 0; k < 10; k++) { const a = (k / 10) * Math.PI * 2; pen.glyphAt('-', Math.cos(a) * 170, Math.sin(a) * 90, 22, a, C.bone, 2.4); }
      pen.flush(); c.restore();
    };
    burst('CLICK', kx0 + 1 * (kw + gapK) + kw / 2 - 60, ky - 150, since + 0.08, -0.1);
    burst('CLACK', kx0 + 5 * (kw + gapK) + kw / 2 - 20, ky - 250, since + 0.2, 0.08);
    // the turret hanging from the ceiling, firing a ring of symbols on every beat
    const tx = 1250, ty = 250;
    pen.glyph('[', tx - 22, ty - 22, 22, 44, C.bone, 2.8); pen.glyph(']', tx, ty - 22, 22, 44, C.bone, 2.8); pen.glyph('o', tx - 14, ty - 14, 28, 28, C.bone, 2.4);
    for (const b of this.beats) {
      const age = t - b;
      if (age < 0 || age > 1.3) continue;
      const n = 18, r = 40 + age * 520;
      for (let k = 0; k < n; k++) {
        const a = (k / n) * Math.PI * 2 + b * 2.3;
        pen.glyphAt(k % 3 === 0 ? '+' : 'o', tx + Math.cos(a) * r, ty + Math.sin(a) * r, 18, a, `rgba(238,233,223,${(0.95 * (1 - age / 1.3)).toFixed(2)})`, 2.2);
      }
    }
    pen.flush();
    // her: mid-leap from key 3 toward key 4, after-images behind
    const fx = kx0 + herKey * (kw + gapK) + kw * 0.5, tx2 = kx0 + (herKey + 1) * (kw + gapK) + kw * 0.5;
    const beatLen = 60 / this.ctx.audio.bpm;
    const u = clamp(since / beatLen);
    const pos = (uu: number) => [fx + (tx2 - fx) * uu, ky - 4 - 150 * 4 * uu * (1 - uu)] as const;
    const S = 132;                                             // her width (bold, knockout — see girl.ts)
    // after-images: the same figure in dots only, strung out along the arc behind her
    for (let k = 3; k >= 1; k--) {
      const uk = u - k * 0.13;
      if (uk < 0) continue;
      const [gx, gyy] = pos(uk);
      drawGirl(pen, 'jump', 0, gx - S / 2, gyy - S * 1.56, S, { col: `rgba(238,233,223,${(0.16 * (4 - k)).toFixed(2)})`, sub: () => '.', noHeart: true, knock: false });
    }
    pen.flush();
    const [hx, hy] = pos(u);
    drawGirl(pen, u < 0.5 ? 'jump' : 'fall', 0, hx - S / 2, hy - S * 1.56, S, {});
    pen.flush();
    // HUD + dialog
    hud(c, pen, W, { stage: 'STAGE 1-1  ·  THE KEYS', t, bar: Math.floor(f.bar) + 1, beat: Math.floor(f.beatPhase * 4) + 1 });
    const line = this.linesIn(t - 4, t + 0.01).filter((l) => l.start <= t).pop();
    dialog(c, pen, line, t, { x: 250, y: H - 196, w: W - 500, h: 136 });
    void symBox;
  }

  // ------------------------------------------------------------------ 'help'
  help(c: CanvasRenderingContext2D, pen: GlyphPen, f: Frame) {
    const t = f.t, lb = this.lastBeat(t), since = t - lb;
    const PAPER = C.bone, INKC = C.ink, DIM = 'rgba(94,91,87,0.5)';
    c.fillStyle = PAPER; c.fillRect(0, 0, W, H);
    const scroll = (t - this.ctx.start) * 60;
    for (let gy = 0; gy < 32; gy++) for (let gx = -1; gx < 56; gx++) { const h = hash(gx + Math.floor(scroll / 36), gy, 5); if (h < 0.22) pen.glyph(h < 0.15 ? '.' : '-', gx * 36 - (scroll % 36) + 9, gy * 36 + 9, 18, 18, DIM, 1.3); }
    pen.flush();
    bigMaze(pen, W, H, scroll * 0.5, 240, 0.22, 7, -60);
    pen.flush();
    // HELP, a building of bricks across the level; it shakes on the hit
    const px = 58, word = 'HELP';
    const ww = (word.length * 6 - 1) * px, x0 = W / 2 - ww / 2, y0 = 300;
    const hit = Math.exp(-since * 9);
    c.save(); c.translate((hash(Math.round(t * 60), 1) - 0.5) * 10 * hit, (hash(Math.round(t * 60), 2) - 0.5) * 10 * hit);
    brickWord(pen, word, x0, y0, px, INKC, 4.2);
    pen.flush();
    c.restore();
    // ground
    const gy = y0 + 7 * px;
    for (let x = -20; x < W + 40; x += 36) {
      pen.glyph('=', x, gy - 5, 18, 18, INKC, 2.8); pen.glyph('=', x + 18, gy - 5, 18, 18, INKC, 2.8);
      for (let y = gy + 30; y < H; y += 36) if (((x / 36) | 0) % 2 === ((y / 36) | 0) % 2) pen.glyph('/', x + 4, y, 28, 28, DIM, 1.6);
    }
    pen.flush();
    // turrets both sides, rings of symbols in ink
    for (const [tx, ty, ph] of [[150, 420, 0], [W - 150, 360, 1.3]] as const) {
      pen.glyph('[', tx - 24, ty - 24, 24, 48, INKC, 3); pen.glyph(']', tx, ty - 24, 24, 48, INKC, 3); pen.glyph('o', tx - 15, ty - 15, 30, 30, INKC, 2.6);
      for (const b of this.beats) {
        const age = t - b;
        if (age < 0 || age > 1.2) continue;
        const n = 20, r = 44 + age * 640;
        for (let k = 0; k < n; k++) { const a = (k / n) * Math.PI * 2 + b * 1.7 + ph; pen.glyphAt(k % 2 ? 'x' : 'o', tx + Math.cos(a) * r, ty + Math.sin(a) * r, 20, a, `rgba(10,10,11,${(0.9 * (1 - age / 1.2)).toFixed(2)})`, 2.4); }
      }
    }
    pen.flush();
    // her on top of the P, arms up; a burst of lines around her on the hit
    const pxX = x0 + 18 * px + 2.5 * px, pyY = y0;
    const s = 140;
    for (let k = 0; k < 12; k++) { const a = (k / 12) * Math.PI * 2; const r = 90 + 50 * (1 - hit); pen.glyphAt('|', pxX + Math.cos(a) * r, pyY - 80 + Math.sin(a) * r, 26, a + Math.PI / 2, `rgba(10,10,11,${(0.3 + 0.6 * hit).toFixed(2)})`, 2.6); }
    pen.flush();
    drawGirl(pen, 'help', 0, pxX - s / 2, pyY - s * 1.5, s, { col: INKC, knock: PAPER });
    pen.flush();
    hud(c, pen, W, { stage: 'STAGE 1-2  ·  HELP', t, bar: Math.floor(f.bar) + 1, beat: Math.floor(f.beatPhase * 4) + 1, col: INKC, dim: C.graphite });
    const line = this.linesIn(t - 4, t + 0.01).filter((l) => l.start <= t).pop();
    dialog(c, pen, line, t, { x: 250, y: H - 196, w: W - 500, h: 136 }, { col: INKC, bg: PAPER });
    c.font = font(F.mono(500), 15); c.fillStyle = C.graphite; c.textAlign = 'left';
    c.fillText('S.O.S.', x0, y0 - 24);
  }
}
