// MODE 'slam' — words MADE OF SYMBOLS. Each sung word is hundreds of marks that fire in from every
// direction and lock into the letters on the word's first syllable, then blow apart when the next word
// arrives. Hot words (real, lie, heart…) burn red; held notes stretch. Behind: concentric rings of
// symbols turning against each other, and — whenever a word says TIME — a clock face of dashes whose
// hand sweeps once per bar and ticks on the 16ths.
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { W, H } from '../engine/gl';
import { LineBatch } from '../engine/lines';
import { LIN } from '../engine/palette';
import { clamp, ease, hash, frameIdx, TAU } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { SymbolGrid, SYM, glyph, mul, kickRing } from '../danmaku/symbols';
import { drawSymbolWord, wordText } from '../danmaku/kinetic';

const HOT = /real|lie|heart|help|alive|life/i;

export default class Slam extends Mode {
  grid = new SymbolGrid();
  bg = new LineBatch(30000, { blend: 'add' });
  lb = new LineBatch(60000, { blend: 'max' });

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, audio } = this.ctx;
    const t = f.t;
    const kick = audio.hit('kick', t, 0.12);
    const ring = kickRing(audio.onsets['kick'], t);
    this.grid.render(renderer, out, t, { level: 0.8, ringR: ring.r, ringK: ring.k });
    const cx = W / 2, cy = H / 2;
    const beat = 60 / audio.bpm;

    // ---- concentric rings of symbols, counter-rotating
    this.bg.clear();
    for (let k = 0; k < 9; k++) {
      const R = 150 + k * 120 + 12 * kick * (k + 1);
      const n = Math.round(R / 14);
      const rot = t * (0.25 + 0.06 * k) * (k % 2 ? 1 : -1);
      const kind = [SYM.dash, SYM.dot, SYM.plus, SYM.chevron, SYM.dot, SYM.dash, SYM.cross, SYM.dot, SYM.star][k]!;
      const col = k === 2 || k === 6 ? mul(LIN.signal, 1.2) : mul(LIN.bone, 0.45);
      for (let i = 0; i < n; i++) {
        const th = rot + (i / n) * TAU;
        const x = cx + Math.cos(th) * R, y = cy + Math.sin(th) * R;
        if (x < -30 || x > W + 30 || y < -30 || y > H + 30) continue;
        glyph(this.bg, kind, x, y, 6, th + Math.PI / 2, col, 0.8, 2);
      }
    }
    // ---- the clock, while a TIME word is up
    const ws = this.wordsIn();
    const timeW = ws.filter((w) => /time/i.test(w.w) && t >= w.start - 0.1 && t < w.end + 0.6).pop();
    if (timeW) {
      const a = clamp((t - timeW.start + 0.1) / 0.15) * clamp((timeW.end + 0.6 - t) / 0.3);
      const R = 470, n = 60;
      const hand = ((t - timeW.start) / (4 * beat)) * TAU - Math.PI / 2;
      const tick16 = Math.floor((t - timeW.start) / (beat / 4));
      for (let i = 0; i < n; i++) {
        const th = (i / n) * TAU - Math.PI / 2;
        const big = i % 5 === 0;
        const lit = i === ((tick16 % n) + n) % n;
        const r0 = R - (big ? 34 : 18), r1 = R;
        this.bg.seg2(cx + Math.cos(th) * r0, cy + Math.sin(th) * r0, cx + Math.cos(th) * r1, cy + Math.sin(th) * r1, big ? 4 : 2.2, lit ? mul(LIN.signal, 3) : mul(LIN.bone, 1.1), a);
      }
      for (let k = 0; k < 16; k++) { // the hand, a line of dots
        const r = 40 + k * 26;
        glyph(this.bg, SYM.dot, cx + Math.cos(hand) * r, cy + Math.sin(hand) * r, 6, 0, mul(LIN.signal, 2.4), a, 5);
      }
    }
    this.bg.render(renderer, out);

    // ---- the words, made of symbols
    this.lb.clear();
    for (let i = 0; i < ws.length; i++) {
      const w = ws[i]!, nx = ws[i + 1];
      const outT = nx ? nx.start : w.end + 0.25;
      if (t < w.start - 0.4 || t > outT + 0.75) continue;
      const word = wordText(w.w);
      const hot = HOT.test(word);
      const held = w.end - w.start > 0.45;
      const stretch = held ? ease.inOutCubic(clamp((t - w.start) / Math.max(0.2, w.end - w.start))) * 0.8 : 0;
      const size = word.length <= 2 ? 360 : word.length <= 4 ? 320 : 260;
      drawSymbolWord(this.lb, word, { cx, cy, t, in: w.start, out: outT, hotFrac: hot ? 0.9 : 0.06, stretch, flicker: held ? 0.3 : 0.05, scale: 1 + 0.05 * kick }, size);
    }
    this.lb.render(renderer, out);

    const cur = ws.filter((w) => t >= w.start).pop();
    const wk = cur ? Math.exp(-(t - cur.start) * 8) : 0;
    const sh = 7 * wk + 4 * kick;
    const roll = cur ? 0.02 * Math.sin(ws.indexOf(cur) * 2.1) : 0;
    return {
      bloom: 0.45, bloomThreshold: 1.0, grain: 0.05, vignette: 0.5, ca: 1.8,
      zoom: 1 + 0.06 * wk,
      shake: [(hash(frameIdx(t), 1) - 0.5) * sh + roll * 300, (hash(frameIdx(t), 2) - 0.5) * sh],
      flash: cur ? 0.25 * Math.exp(-Math.max(0, t - cur.start) * 40) : 0,
    };
  }
}
