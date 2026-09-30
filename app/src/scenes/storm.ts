// MODE 'storm' — full-screen bullet patterns of symbols: four emitters spin out spirals on the 8th
// notes, the centre fires a ring on every beat, fans rain from the top on the backbeat. The sung words
// slam through the middle of it; hot words are red and tremble.
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { Layer2D, W, H } from '../engine/gl';
import { LineBatch } from '../engine/lines';
import { rgba } from '../engine/palette';
import { clamp, hash, frameIdx, TAU } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { BulletField, SymbolGrid, SYM, kickRing } from '../danmaku/symbols';
import { slamWord, wordText } from '../danmaku/kinetic';

const HOT = /lie|real|heart|help/i;

export default class Storm extends Mode {
  grid = new SymbolGrid();
  lb = new LineBatch(60000, { blend: 'add' });
  L = new Layer2D();
  field = new BulletField();

  init() {
    const au = this.ctx.audio, beat = 60 / au.bpm;
    const t0 = this.ctx.start - 2, t1 = this.ctx.end;
    const em = [[W * 0.18, H * 0.22], [W * 0.82, H * 0.22], [W * 0.18, H * 0.8], [W * 0.82, H * 0.8]];
    for (let k = 0, tt = t0; tt < t1; k++, tt = t0 + k * beat / 2) {
      em.forEach(([x, y], e) => {
        this.field.add({ t0: tt, x: x!, y: y!, n: 7, a0: (e % 2 ? 1 : -1) * k * 0.29 + e, spread: TAU, speed: 360 + 40 * (k % 3), curl: (e % 2 ? 0.3 : -0.3), kind: k % 3 === 0 ? SYM.star : SYM.dash, size: 9, hot: (k + e) % 6 === 0, life: 3.4 });
      });
    }
    au.beats.forEach((bt, i) => {
      if (bt < t0 || bt >= t1) return;
      this.field.add({ t0: bt, x: W / 2, y: H / 2, n: 40, a0: hash(i, 3) * TAU, spread: TAU, speed: 620, kind: i % 2 ? SYM.plus : SYM.ring, size: 11, hot: i % 2 === 0, life: 2.6 });
      if (i % 2) this.field.add({ t0: bt, x: W * (0.2 + 0.6 * hash(i, 4)), y: -40, n: 19, a0: Math.PI / 2, spread: 1.3, speed: 980, kind: SYM.dash, size: 13, life: 2 });
    });
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    const kick = audio.hit('kick', t, 0.1);
    const ring = kickRing(audio.onsets['kick'], t);
    this.grid.render(renderer, out, t, { level: 0.9, ringR: ring.r, ringK: ring.k * 1.2, pulse: 1 });
    this.lb.clear();
    this.field.draw(this.lb, t, { alpha: clamp((t - this.ctx.start + 0.2) / 0.3) });
    this.lb.render(renderer, out);

    const c = this.L.ctx; this.L.clear();
    const ws = this.wordsIn();
    const cur = ws.filter((w) => t >= w.start - 0.02).pop();
    if (cur) {
      const word = wordText(cur.w);
      const hot = HOT.test(word);
      const held = cur.end - cur.start > 0.45;
      const stretch = held ? clamp((t - cur.start) / Math.max(0.2, cur.end - cur.start)) : 0;
      const fade = held ? 1 : clamp((cur.end + 0.35 - t) / 0.2);
      slamWord(c, word, W / 2, H / 2, { size: 300, age: t - cur.start, color: hot ? rgba('signal', 1) : rgba('bone', 1), echoes: 3, echoColor: hot ? rgba('signal', 1) : rgba('bone', 1), jitter: hot ? 1 : 0.2, stretch: stretch * 0.7, alpha: fade, t });
    }
    comp.draw(renderer, this.L.upload(), out);

    const wk = cur ? Math.exp(-(t - cur.start) * 9) : 0;
    const sh = 9 * wk + 7 * kick + 4 * audio.hit('snare', t, 0.1);
    return {
      bloom: 0.5, bloomThreshold: 1.0, grain: 0.05, vignette: 0.5, ca: 3,
      zoom: 1 + 0.07 * wk + 0.02 * kick,
      shake: [(hash(frameIdx(t), 1) - 0.5) * sh, (hash(frameIdx(t), 2) - 0.5) * sh],
      flash: cur ? 0.3 * Math.exp(-Math.max(0, t - cur.start) * 40) : 0,
    };
  }
}
