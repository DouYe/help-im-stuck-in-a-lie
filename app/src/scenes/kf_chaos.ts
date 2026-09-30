// KEYFRAME 5 — everything at once ("I still got a heart inside"). The frame is torn into three slanted
// strips — the platformer, the 3D corridor, the maze from above — each still running, rows of the picture
// slipping sideways on the beat. In the middle, bigger than anywhere else, she stands holding the heart;
// rings of symbols go out from it on every beat. At the edges, copies of her made of other things (dots,
// code) flicker in and out: what's underneath. HEART in big outlined letters.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { F, font } from '../engine/type';
import { clamp, hash, frameIdx } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { GlyphPen } from '../game/glyph';
import { drawGirl } from '../game/girl';
import { C, hud, outlineWord, symHeart, bigMaze, farField } from '../game/world';
import { wordText } from '../danmaku/kinetic';

export default class KfChaos extends Mode {
  bg = new FSPass(/* glsl */ `void main() { vec2 p = FRAG_PX; fragColor = vec4(C_INK * (1.0 + 0.35 * snoise(p * 0.002)), 1.0); }`);
  L = new Layer2D();
  beats: number[] = [];
  init() { this.beats = this.ctx.audio.beats.filter((b) => b > this.ctx.start - 2 && b < this.ctx.end + 2); }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    this.bg.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const pen = new GlyphPen(c);
    const lb = [...this.beats].reverse().find((b) => b <= t) ?? -9, since = t - lb;
    const lt = t - this.ctx.start;
    // three slanted strips
    const strip = (k: number) => { const x0 = k * 640 - 180, x1 = x0 + 640; c.beginPath(); c.moveTo(x0 + 180, 0); c.lineTo(x1 + 180, 0); c.lineTo(x1 - 180, H); c.lineTo(x0 - 180, H); c.closePath(); };
    // --- strip 1: the platformer
    c.save(); strip(0); c.clip();
    farField(pen, W, H, lt * 40, 3); pen.flush();
    for (let x = -40; x < 700; x += 36) { pen.glyph('=', x, 760, 18, 18, C.bone, 2.6); pen.glyph('=', x + 18, 760, 18, 18, C.bone, 2.6); for (let y = 800; y < H; y += 36) if (((x / 36) | 0) % 2 === ((y / 36) | 0) % 2) pen.glyph('/', x + 4, y, 28, 28, 'rgba(94,91,87,0.7)', 1.6); }
    for (let x = 60; x < 600; x += 130) { pen.glyph('(', x, 560, 20, 60, C.bone, 2.4); pen.glyph(')', x + 70, 560, 20, 60, C.bone, 2.4); pen.line(x + 10, 622, x + 80, 622, C.graphite, 2.4); }
    for (let x = 0; x < 700; x += 18) pen.glyph('v', x, 130, 18, 18, C.bone, 2);
    for (const b of this.beats) { const age = t - b; if (age < 0 || age > 1.2) continue; for (let k = 0; k < 14; k++) { const a = (k / 14) * Math.PI * 2 + b; pen.glyphAt('o', 300 + Math.cos(a) * (40 + age * 420), 330 + Math.sin(a) * (40 + age * 420), 16, a, `rgba(238,233,223,${(0.9 * (1 - age / 1.2)).toFixed(2)})`, 2); } }
    drawGirl(pen, 'walk', (t * 2) % 1, 230, 760 - 96 * 1.5, 96, {});
    pen.flush(); c.restore();
    // --- strip 2: the corridor, a tunnel of symbols rushing toward us
    c.save(); strip(1); c.clip();
    const vx = 960, vy = 470;
    for (let ring = 0; ring < 14; ring++) {
      const zz = ((ring - lt * 2.2) % 14 + 14) % 14 + 0.6;
      const s = 900 / zz, a = clamp(1.2 - zz / 12);
      const col = `rgba(238,233,223,${a.toFixed(2)})`;
      const x0 = vx - s * 0.9, x1 = vx + s * 0.9, y0 = vy - s * 0.6, y1 = vy + s * 0.6;
      const step = Math.max(10, s / 10);
      for (let x = x0; x < x1; x += step) { pen.glyph('-', x, y0 - step / 2, step, step, col, Math.max(1, 2.4 * a)); pen.glyph('-', x, y1 - step / 2, step, step, col, Math.max(1, 2.4 * a)); }
      for (let y = y0; y < y1; y += step) { pen.glyph('|', x0 - step / 2, y, step, step, col, Math.max(1, 2.4 * a)); pen.glyph('|', x1 - step / 2, y, step, step, col, Math.max(1, 2.4 * a)); }
    }
    for (let k = 0; k < 16; k++) { const a = (k / 16) * Math.PI * 2; for (let r = 60; r < 900; r *= 1.35) pen.glyphAt('.', vx + Math.cos(a) * r, vy + Math.sin(a) * r * 0.66, 14, 0, 'rgba(238,233,223,0.55)', 2.4); }
    pen.flush(); c.restore();
    // --- strip 3: the maze from above
    c.save(); strip(2); c.clip();
    const CELL = 40, off = (lt * 30) % CELL;
    for (let gy = 0; gy < 30; gy++) for (let gx = 28; gx < 50; gx++) {
      const x = gx * CELL - off, y = gy * CELL;
      const h = hash(gx, gy, 12);
      if (h < 0.45) pen.glyph('|', x - CELL / 2, y, CELL, CELL, 'rgba(238,233,223,0.8)', 2.4);
      else if (h < 0.85) pen.glyph('-', x, y - CELL / 2, CELL, CELL, 'rgba(238,233,223,0.8)', 2.4);
      if (hash(gx, gy, 13) < 0.3) pen.glyph('+', x - 8, y - 8, 16, 16, 'rgba(156,151,143,0.8)', 1.6);
    }
    drawGirl(pen, 'frontwalk', (t * 2) % 1, 1590, 500, 64, { view: 'above' });
    pen.flush(); c.restore();
    // strip seams
    for (let k = 1; k < 3; k++) { const x0 = k * 640 - 180; for (let y = 0; y < H; y += 18) { const x = x0 + 180 - (y / H) * 360; pen.glyph('/', x - 9, y, 18, 18, C.bone, 2.6); } }
    pen.flush();
    // --- the tear: rows slip sideways on the beat
    const glitch = Math.exp(-since * 7);
    if (glitch > 0.05) {
      for (let k = 0; k < 7; k++) {
        const y = Math.floor(hash(k, Math.floor(lb * 10), 1) * H), hgt = 12 + Math.floor(hash(k, 2) * 60), dx = (hash(k, lb, 3) - 0.5) * 160 * glitch;
        c.drawImage(this.L.canvas, 0, y * (this.L.canvas.width / W), this.L.canvas.width, hgt * (this.L.canvas.width / W), dx, y, W, hgt);
      }
    }
    // --- HEART in big outlined letters behind her
    c.fillStyle = 'rgba(10,10,11,0.55)'; c.fillRect(W / 2 - (29 * 30) / 2 - 30, 130, 29 * 30 + 60, 7 * 30 + 40);   // calm the tunnel behind the word
    outlineWord(pen, 'HEART', W / 2 - (29 * 30) / 2, 150, 30, C.ink, 11);      // ink under-stroke so it reads over the tunnel
    pen.flush();
    outlineWord(pen, 'HEART', W / 2 - (29 * 30) / 2, 150, 30, C.bone, 3.2);
    pen.flush();
    // --- her, in the middle, holding the heart; rings of symbols go out from it on every beat
    const s = 250, x = W / 2 - s / 2, y = 330;
    c.fillStyle = 'rgba(10,10,11,0.92)'; c.beginPath(); c.ellipse(W / 2, y + s * 0.8, s * 0.75, s * 0.95, 0, 0, Math.PI * 2); c.fill();
    const hxp = W / 2 + 0.03 * s, hyp = y + 0.68 * s;
    for (const b of this.beats) {
      const age = t - b;
      if (age < 0 || age > 1.0) continue;
      const r = 60 + age * 520, n = 36;
      for (let k = 0; k < n; k++) { const a = (k / n) * Math.PI * 2; pen.glyphAt('-', hxp + Math.cos(a) * r, hyp + Math.sin(a) * r, 18, a + Math.PI / 2, `rgba(255,83,20,${(0.9 * (1 - age)).toFixed(2)})`, 2.6); }
    }
    pen.flush();
    const beat = Math.exp(-since * 10);
    drawGirl(pen, 'heart', 0, x, y, s, { big: 1.3 + 0.25 * beat });
    pen.flush();
    // --- what's underneath: copies of her in dots and in code, flickering at the seams
    const fi = frameIdx(t);
    if (fi % 5 !== 0) drawGirl(pen, 'front', 0, 470, 420, 120, { col: 'rgba(238,233,223,0.8)', knock: false, sub: (g, k) => (hash(k, 3) < 0.9 ? '.' : g) });
    if (fi % 7 !== 3) drawGirl(pen, 'q_front', 0, 1330, 400, 120, { col: 'rgba(238,233,223,0.8)', flip: true, knock: false, sub: (_g, k) => (hash(k, fi >> 2) < 0.5 ? '0' : '1') });
    pen.flush();
    // --- HUD and the line
    hud(c, pen, W, { stage: 'ERROR  ·  WORLD 1-?-3D', t, bar: Math.floor(f.bar) + 1, beat: Math.floor(f.beatPhase * 4) + 1, lives: 1, plate: 'rgba(10,10,11,0.88)' });
    const line = this.linesIn(t - 4, t + 0.01).filter((l) => l.start <= t).pop();
    if (line) {
      c.font = font(F.mono(700), 40); c.textAlign = 'center'; c.textBaseline = 'middle';
      const s2 = line.words.filter((w) => t >= w.start).map((w) => wordText(w.w)).join(' ');
      const tw = c.measureText(s2).width;
      c.fillStyle = C.bone; c.fillRect(W / 2 - tw / 2 - 24, 950, tw + 48, 64);
      c.fillStyle = C.ink; c.fillText(s2, W / 2, 983);
    }
    comp.draw(renderer, this.L.upload(), out);
    const kick = audio.hit('kick', t, 0.1);
    void bigMaze; void symHeart;
    return { bloom: 0, halation: 0, ca: 0, grain: 0.035, vignette: 0.2, shake: [(hash(fi, 1) - 0.5) * 8 * kick, (hash(fi, 2) - 0.5) * 8 * kick] };
  }
}
