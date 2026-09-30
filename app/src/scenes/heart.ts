// MODE 'heart' — inside her chest: a heart made of symbols (concentric heart-shaped lanes of marks
// flowing along the curve). Behind it, her hand's glyphs, enormous. The heart types itself in as the
// line is sung and beats with the kick; cue param `burst` makes it blow outward on the held note,
// firing rings of symbols (hearts, dots, stars) across the screen.
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { Layer2D, W, H } from '../engine/gl';
import { LineBatch } from '../engine/lines';
import { LIN } from '../engine/palette';
import { clamp, ease, hash, frameIdx, TAU } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { GlyphFigure } from '../danmaku/glyphs';
import { drawHeart } from '../danmaku/heart';
import { drawLyric } from '../danmaku/lyric';
import { BulletField, SymbolGrid, SYM, mul, glyph, kickRing } from '../danmaku/symbols';
import { slamWord, wordText } from '../danmaku/kinetic';
import { rgba } from '../engine/palette';

export default class Heart extends Mode {
  grid = new SymbolGrid();
  lb = new LineBatch(60000, { blend: 'max' });
  fx = new LineBatch(30000, { blend: 'add' });
  L = new Layer2D();
  fig!: GlyphFigure;
  bursts = new BulletField();

  init() {
    this.fig = new GlyphFigure(1000);
    const au = this.ctx.audio;
    // every beat inside the window: a ring of symbols from the heart; the burst cue fires denser, hotter rings
    const burstCue = this.cues.find((c) => c.params.burst);
    au.beats.forEach((bt, i) => {
      if (bt < this.ctx.start || bt >= this.ctx.end) return;
      const hot = !!burstCue && bt >= burstCue.t - 0.05;
      const kinds = [SYM.heart, SYM.dot, SYM.star, SYM.plus];
      this.bursts.add({ t0: bt, x: W / 2, y: 540, n: hot ? 40 : 20, a0: hash(i, 3) * TAU, spread: TAU, speed: hot ? 520 : 300, curl: hot ? (i % 2 ? 0.35 : -0.35) : 0, kind: kinds[i % kinds.length]!, size: hot ? 12 : 8, hot: hot || i % 2 === 0, life: 3.5 });
      // explode: on the burst cue, a storm of hearts on every 16th
      if (hot && this.cues.some((c) => c.params.explode)) {
        for (let q = 1; q < 4; q++) this.bursts.add({ t0: bt + q * (60 / au.bpm) / 4, x: W / 2, y: 540, n: 24, a0: hash(i, q, 5) * TAU, spread: TAU, speed: 700 + 200 * q, curl: q % 2 ? 0.5 : -0.5, kind: SYM.heart, size: 14 + 4 * q, hot: q !== 2, life: 2.4 });
      }
    });
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, comp, audio, lyrics } = this.ctx;
    const t = f.t;
    const ws = this.wordsIn();
    const first = ws[0];
    const firstLineEnd = first ? lyrics.lines[first.line]!.end : this.ctx.start + 2;
    const build = first ? ease.outCubic(clamp((t - (first.start - 0.3)) / Math.max(0.5, firstLineEnd - first.start))) : 1;
    const burstCue = this.cues.find((c) => c.params.burst);
    let burst = 0, flare = 0;
    if (burstCue && t >= burstCue.t - 0.2) {
      const bws = ws.filter((w) => w.start >= burstCue.t - 0.05);
      const b0 = bws[0], held = bws[bws.length - 1];
      if (b0 && t >= b0.start) flare = Math.exp(-(t - b0.start) * 5);
      if (held) burst = 0.3 * ease.outCubic(clamp((t - held.start) / Math.max(0.3, held.end - held.start)));
    }
    const pulse = Math.max(audio.hit('kick', t, 0.12), flare);

    const ring = kickRing(audio.onsets['kick'], t);
    this.grid.render(renderer, out, t, { level: 0.7, ringR: ring.r, ringK: ring.k, pulse: 1, cx: W / 2, cy: 540 });

    const chaos = !!this.ctx.params.chaos;
    this.fx.clear();
    this.bursts.draw(this.fx, t, { alpha: 0.85 * build });
    this.lb.clear();
    if (!chaos) {
      // her hand, enormous, behind the heart (we are inside her chest)
      const S = 3.1, s = 1000 / 1100;
      this.fig.draw(this.lb, t, { x: W / 2 - 600 * s * S, y: 560 - 830 * s * S, scale: S, alpha: 0.22 + 0.08 * pulse, heart: 0.6 * build, pulse });
    } else {
      // comets of symbols orbiting the heart on tilted ellipses
      for (let k = 0; k < 7; k++) for (let j = 0; j < 14; j++) {
        const ph = t * (0.9 + 0.25 * k) * (k % 2 ? 1 : -1) + k * 1.3 - j * 0.045;
        const rx = 560 + 70 * k, ry = 190 + 35 * k, tilt = k * 0.45;
        const ex = Math.cos(ph) * rx, ey = Math.sin(ph) * ry;
        const x = W / 2 + ex * Math.cos(tilt) - ey * Math.sin(tilt), y = 540 + ex * Math.sin(tilt) + ey * Math.cos(tilt);
        glyph(this.fx, j === 0 ? SYM.star : SYM.dot, x, y, j === 0 ? 11 : 6 - j * 0.3, 0, j === 0 ? mul(LIN.signal, 2.6) : mul(LIN.bone, 1.2 - j * 0.07), (1 - j / 14) * build, 2.4);
      }
    }
    drawHeart(this.lb, { cx: W / 2, cy: 540, R: 440, rings: 13, t, build, pulse, burst, flow: (chaos ? 2 : 1) + 2 * burst, size: 12 });
    this.fx.render(renderer, out);
    this.lb.render(renderer, out);

    const c = this.L.ctx; this.L.clear();
    if (chaos) {
      const cur = ws.filter((w) => t >= w.start - 0.02).pop();
      if (cur) {
        const word = wordText(cur.w);
        const hot = /heart/i.test(word);
        const held = cur.end - cur.start > 0.45;
        const st = held ? clamp((t - cur.start) / Math.max(0.2, cur.end - cur.start)) : 0;
        slamWord(c, word, W / 2, 545, { size: word.length > 5 ? 190 : 230, age: t - cur.start, color: hot ? rgba('bone', 1) : rgba('bone', 0.95), echoes: 2, echoColor: rgba('signal', 1), jitter: 0.2 + 0.5 * st, stretch: st * 0.6, t });
      }
    } else drawLyric(c, lyrics, t, { y: H - 70, size: 58 });
    comp.draw(renderer, this.L.upload(), out);

    // explode: on the last held note, the camera falls into the core
    let dive = 0;
    if (this.cues.some((c) => c.params.explode) && burstCue) {
      const bws = ws.filter((w) => w.start >= burstCue.t - 0.05);
      const held = bws[bws.length - 1];
      if (held) dive = Math.pow(clamp((t - (held.start + (held.end - held.start) * 0.35)) / ((held.end - held.start) * 0.9)), 2.2);
    }
    const sh = 5 * pulse + 10 * flare;
    return {
      bloom: 0.75 + 0.5 * flare + dive, bloomThreshold: 0.7, grain: 0.05, vignette: 0.5,
      zoom: (1 + 0.035 * pulse + 0.1 * burst) * (1 + 5 * dive),
      shake: [(hash(frameIdx(t), 1) - 0.5) * sh, (hash(frameIdx(t), 2) - 0.5) * sh],
      flash: 0.3 * flare * flare * flare * flare + 1.2 * Math.max(0, dive - 0.85) * 6,
    };
  }
}
void mul;
