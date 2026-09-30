// MODE 'swarm' — a vortex of symbols. Default: thousands of marks spiral in toward the centre, faster
// and faster, the sung words flashing in the middle; `collapse` sucks everything into the centre at the
// end of the window (a flash hands over to the next mode). `tail`: the aftermath — hearts and dots
// drift outward, one big heart beats in the middle, fading out.
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { Layer2D, W, H } from '../engine/gl';
import { LineBatch } from '../engine/lines';
import { LIN, rgba } from '../engine/palette';
import { clamp, ease, hash, smoothstep, frameIdx, TAU } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { SymbolGrid, SYM, glyph, mul, mixc, kickRing } from '../danmaku/symbols';
import { slamWord, wordText } from '../danmaku/kinetic';

const N = 1500;
const KINDS = [SYM.dash, SYM.dash, SYM.dot, SYM.star, SYM.plus, SYM.slash, SYM.back, SYM.chevron];

export default class Swarm extends Mode {
  grid = new SymbolGrid();
  lb = new LineBatch(40000, { blend: 'add' });
  L = new Layer2D();

  /** Accelerating phase: how far the vortex has turned by t. */
  phase(t: number) {
    const d = Math.max(0, t - this.ctx.start), D = Math.max(1, this.ctx.end - this.ctx.start);
    return d + 1.6 * d * d / D;
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    const tail = this.param(t, 'tail', false);
    const end = this.ctx.params.cutOut ?? this.ctx.end;
    const collapse = this.param(t, 'collapse', false) ? ease.inCubic(clamp((t - (end - 0.45)) / 0.45)) : 0;
    const pulse = audio.hit('kick', t, 0.12);
    const ring = kickRing(audio.onsets['kick'], t);
    this.grid.render(renderer, out, t, { level: tail ? 0.5 : 0.8 + collapse, ringR: ring.r, ringK: ring.k, cx: W / 2, cy: H / 2 });

    this.lb.clear();
    const cx = W / 2, cy = H / 2;
    const bone = mul(LIN.bone, 1.3), sig = mul(LIN.signal, 2.2);
    const ph = this.phase(t);
    for (let i = 0; i < N; i++) {
      const h1 = hash(i, 1), h2 = hash(i, 2), h3 = hash(i, 3);
      let x: number, y: number, dir: number, a: number;
      if (!tail) {
        // inward spiral: u runs 0 -> 1 (outer -> centre) and wraps
        const rate = 0.18 + 0.35 * h2;
        const u = (h1 + ph * rate) % 1;
        const r = (1250 * (1 - u) ** 1.6 + 8) * (1 - collapse);
        const th = h3 * TAU + (1 - u) * 4.2 * (h2 < 0.5 ? 1 : -1) * 0.6 + ph * 0.5;
        x = cx + Math.cos(th) * r; y = cy + Math.sin(th) * r * 0.9;
        dir = th + Math.PI * 0.62 * (h2 < 0.5 ? 1 : -1);
        a = clamp(u * 6) * clamp((1 - u) * 8);
      } else {
        // drift outward, slowly turning
        const since = t - this.ctx.start;
        const r = 60 + (h1 * 900 + since * (40 + 80 * h2));
        const th = h3 * TAU + since * 0.12 * (h2 < 0.5 ? 1 : -1);
        x = cx + Math.cos(th) * r; y = cy + Math.sin(th) * r * 0.85;
        dir = th; a = 0.6 * clamp(1 - r / 1300);
      }
      if (x < -40 || x > W + 40 || y < -40 || y > H + 40 || a <= 0.01) continue;
      const kind = tail ? (i % 3 === 0 ? SYM.heart : SYM.dot) : KINDS[i % KINDS.length]!;
      const col = h1 < (tail ? 0.35 : 0.1) ? sig : mixc(bone, mul(LIN.ash, 0.9), h2 * 0.6);
      glyph(this.lb, kind, x, y, tail ? 6 + 5 * h3 : 7 + 4 * h3, kind === SYM.heart || kind === SYM.dot ? 0 : dir, col, a, 2.2);
    }
    if (tail) {
      // the heart that is left: one big outline, beating
      const k = 1 + 0.12 * pulse;
      for (let j = 0; j < 4; j++) glyph(this.lb, SYM.heart, cx, cy - 10, (150 - j * 18) * k, 0, mul(LIN.signal, 2.4 - j * 0.4), 1 - j * 0.15, 3.2 - j * 0.4);
    }
    this.lb.render(renderer, out);

    // the sung words flash in the vortex
    const c = this.L.ctx; this.L.clear();
    const ws = this.wordsIn(this.ctx.start - 0.5, this.ctx.end);
    const cur = ws.filter((w) => t >= w.start - 0.02 && t < w.end + 0.12).pop();
    if (cur && !tail) {
      const i = ws.indexOf(cur);
      slamWord(c, wordText(cur.w), cx + (i % 2 ? 1 : -1) * 120 * (i % 3), cy + ((i * 37) % 3 - 1) * 90, { size: 190, age: t - cur.start, color: rgba('bone', 1), echoes: 2, jitter: 0.3, t });
    }
    comp.draw(renderer, this.L.upload(), out);

    const sh = 4 * pulse + 20 * collapse;
    return {
      bloom: 0.6 + collapse, grain: 0.05, vignette: 0.5,
      zoom: 1 + 0.05 * collapse + (tail ? -0.02 * clamp((t - this.ctx.start) / 2) : 0.02 * pulse),
      shake: [(hash(frameIdx(t), 1) - 0.5) * sh, (hash(frameIdx(t), 2) - 0.5) * sh],
      flash: 1.3 * smoothstep(end - 0.08, end, t) * (this.param(t, 'collapse', false) ? 1 : 0),
      fade: this.param(t, 'fadeOut', false) ? smoothstep(this.ctx.end - 0.6, this.ctx.end - 0.02, t) : 0,
    };
  }
}
