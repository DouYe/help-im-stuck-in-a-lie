// MODE 'bars' — every sung word slams a bar of symbols across the screen (alternating sides), the
// word itself caught between them; the last bar reads the key word in red (default: LIE). Meanwhile
// the top and bottom close in until the whole picture is a slit.
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { Layer2D, W, H } from '../engine/gl';
import { LineBatch } from '../engine/lines';
import { LIN, rgba } from '../engine/palette';
import { F, font, measure } from '../engine/type';
import { clamp, ease, hash, lerp, frameIdx } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { SymbolGrid, SYM, glyph, mul, kickRing } from '../danmaku/symbols';
import { slamWord, wordText } from '../danmaku/kinetic';

const YS = [300, 780, 460, 620, 220, 860];

export default class Bars extends Mode {
  grid = new SymbolGrid();
  lb = new LineBatch(40000, { blend: 'max' });
  L = new Layer2D();

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    const ring = kickRing(audio.onsets['kick'], t);
    this.grid.render(renderer, out, t, { level: 0.8, ringR: ring.r, ringK: ring.k });
    const ws = this.wordsIn();
    const key = String(this.ctx.params.word ?? 'LIE').toUpperCase();
    const snap = (x: number) => audio.timeOfBeat(Math.round(audio.beatAt(x) * 4) / 4);

    // the word, big, behind the bars
    const c = this.L.ctx; this.L.clear();
    const cur = ws.filter((w) => t >= w.start - 0.02).pop();
    if (cur) {
      const word = wordText(cur.w);
      const hot = word === key;
      slamWord(c, word, W / 2, H / 2, { size: 280, width: 62, age: t - cur.start, color: hot ? rgba('signal', 1) : rgba('bone', 1), echoes: 2, jitter: hot ? 0.8 : 0.1, t });
    }

    this.lb.clear();
    ws.forEach((w, i) => {
      const t0 = snap(w.start);
      if (t < t0 - 0.12) return;
      const last = i === ws.length - 1;
      const k = ease.outExpo(clamp((t - t0 + 0.12) / 0.2));
      const side = i % 2 ? -1 : 1;
      const y = YS[i % YS.length]!;
      const x0 = side > 0 ? lerp(W + 60, -40, k) : lerp(-W - 60, -40, k);
      const col = last ? mul(LIN.signal, 2.3) : mul(LIN.bone, 1.3);
      const off = ((t * 120 * side) % 36 + 36) % 36;
      for (let x = x0 - 36 + off; x < x0 + W + 100; x += 18) {
        const j = Math.round((x - x0) / 18);
        glyph(this.lb, j % 4 === 3 ? SYM.plus : SYM.dash, x, y - 11, 8, 0, col, 1, 3.2);
        glyph(this.lb, j % 2 ? SYM.slash : SYM.back, x + 9, y + 11, 8, 0, mul(col, 0.8), 1, 2.8);
      }
      if (last) {
        const fam = F.archivo(125, 900), size = 60;
        c.font = font(fam, size); c.textBaseline = 'middle';
        const wd = measure(key, fam, size) + 120;
        for (let x = x0 + 40; x < W; x += wd * 1.8) {
          c.fillStyle = rgba('ink', 0.92); c.fillRect(x - 20, y - 36, wd - 70, 72);
          c.fillStyle = rgba('signal', 1); c.fillText(key, x, y + 3);
        }
      }
    });
    this.lb.render(renderer, out);
    // the slit: top and bottom close in over the window
    const close = ease.inCubic(clamp((t - this.ctx.start) / Math.max(0.5, (this.ctx.params.cutOut ?? this.ctx.end) - this.ctx.start)));
    const hgt = lerp(0, H / 2 - 40, close);
    c.fillStyle = rgba('ink', 1);
    c.fillRect(0, 0, W, hgt); c.fillRect(0, H - hgt, W, hgt);
    c.fillStyle = rgba('signal', 0.9);
    if (hgt > 2) { c.fillRect(0, hgt - 2, W, 2); c.fillRect(0, H - hgt, W, 2); }
    comp.draw(renderer, this.L.upload(), out);

    const bh = ws.reduce((m, w) => (t >= snap(w.start) ? Math.max(m, Math.exp(-(t - snap(w.start)) * 10)) : m), 0);
    const sh = 18 * bh;
    return {
      bloom: 0.6, grain: 0.05, vignette: 0.45, ca: 2,
      zoom: 1 + 0.04 * bh,
      shake: [(hash(frameIdx(t), 1) - 0.5) * sh, (hash(frameIdx(t), 2) - 0.5) * sh],
    };
  }
}
