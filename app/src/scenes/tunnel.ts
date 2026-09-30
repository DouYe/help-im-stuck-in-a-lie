// MODE 'tunnel' — rings of symbols rush at the camera out of a vanishing point, spinning; speed lines
// streak outward. Every sung word SLAMS in the middle; hot words (lie, real, heart…) are red, a held
// word stretches and trembles, then shatters into symbols when the note ends.
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { Layer2D, W, H } from '../engine/gl';
import { LineBatch } from '../engine/lines';
import { LIN, rgba } from '../engine/palette';
import { clamp, hash, smoothstep, frameIdx, TAU } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { SYM, glyph, mul } from '../danmaku/symbols';
import { slamWord, drawSymbolWord, wordText } from '../danmaku/kinetic';

const RINGS = 26;
const HOT = /lie|real|heart|help/i;
const KINDS = [SYM.dash, SYM.plus, SYM.dot, SYM.chevron, SYM.star, SYM.cross, SYM.diamond, SYM.heart];

export default class Tunnel extends Mode {
  lb = new LineBatch(50000, { blend: 'add' });
  txt = new LineBatch(30000, { blend: 'max' });
  L = new Layer2D();

  /** Distance travelled down the tunnel: accelerates on every word. */
  travel(t: number) {
    let d = (t - this.ctx.start) * 2.2;
    for (const w of this.wordsIn()) if (t > w.start) d += 1.2 * (1 - Math.exp(-(t - w.start) * 6));
    return d;
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    renderer.setRenderTarget(out);
    renderer.setClearColor(new THREE.Color().setRGB(LIN.ink[0], LIN.ink[1], LIN.ink[2], THREE.LinearSRGBColorSpace), 1);
    renderer.clear(true, true, true);

    const cx = W / 2 + 40 * Math.sin(t * 1.3), cy = H / 2 + 30 * Math.cos(t * 1.1);
    const d = this.travel(t);
    const spin = t * 0.6 + 0.3 * Math.sin(t * 2.1);
    const kick = audio.hit('kick', t, 0.1);
    this.lb.clear();
    const bone = mul(LIN.bone, 0.95), sig = mul(LIN.signal, 2.0);
    for (let j = 0; j < RINGS; j++) {
      const idx = Math.floor(d) + j;                   // ring identity (stable as it approaches)
      const z = RINGS - j - (d % 1);                   // depth: RINGS (far) .. 0 (at the camera)
      if (z <= 0.15) continue;
      const s = 1 / (z * 0.16 + 0.04);
      const R = 150 * s * (1 + 0.08 * kick);
      if (R > 2400) continue;
      const n = 28 + (idx % 3) * 8;
      const kind = KINDS[((idx % KINDS.length) + KINDS.length) % KINDS.length]!;
      const hot = idx % 5 === 0;
      const a = clamp((RINGS - z) / 6) * clamp(z / 0.8);
      const rot = spin * (idx % 2 ? 1 : -1) + idx * 0.37;
      for (let i = 0; i < n; i++) {
        const th = rot + (i / n) * TAU;
        const x = cx + Math.cos(th) * R, y = cy + Math.sin(th) * R * 0.92;
        if (x < -60 || x > W + 60 || y < -60 || y > H + 60) continue;
        glyph(this.lb, kind, x, y, Math.min(60, 4 + s * 3.2), th + Math.PI / 2, hot ? sig : bone, a, Math.min(6, 1.2 + s * 0.35));
      }
    }
    // speed lines
    for (let i = 0; i < 90; i++) {
      const th = hash(i, 1) * TAU;
      const u = (hash(i, 2) + d * (0.3 + 0.5 * hash(i, 3))) % 1;
      const r0 = 60 + 1400 * u * u, r1 = r0 + 30 + 260 * u * u;
      this.lb.seg2(cx + Math.cos(th) * r0, cy + Math.sin(th) * r0, cx + Math.cos(th) * r1, cy + Math.sin(th) * r1, 1.2 + 2 * u, i % 7 === 0 ? sig : mul(LIN.bone, 0.8), u);
    }
    this.lb.render(renderer, out);

    // words
    const c = this.L.ctx; this.L.clear();
    this.txt.clear();
    const ws = this.wordsIn();
    const cur = ws.filter((w) => t >= w.start - 0.02).pop();
    if (cur) {
      const word = wordText(cur.w);
      const held = cur.end - cur.start > 0.45 && cur === ws[ws.length - 1];
      const hot = HOT.test(word);
      if (held && t > cur.end) {
        // the held word breaks into symbols and blows past the camera
        drawSymbolWord(this.txt, word, { cx: W / 2, cy: H / 2, t, in: cur.start - 1, out: cur.end, hotFrac: hot ? 0.85 : 0.05, scale: 1.1, stretch: 1 }, 300);
      } else {
        const stretch = held ? clamp((t - cur.start) / Math.max(0.2, cur.end - cur.start)) : 0;
        slamWord(c, word, W / 2, H / 2, { size: word.length <= 2 ? 330 : 300, age: t - cur.start, color: hot ? rgba('signal', 1) : rgba('bone', 1), echoes: 3, echoColor: hot ? rgba('signal', 1) : rgba('bone', 1), jitter: held ? 0.4 + 0.6 * stretch : 0.15, stretch: stretch * 0.9, t });
      }
    }
    this.txt.render(renderer, out);
    comp.draw(renderer, this.L.upload(), out);

    const wk = cur ? Math.exp(-(t - cur.start) * 9) : 0;
    const sh = 8 * wk + 5 * kick;
    return {
      bloom: 0.45, bloomThreshold: 1.0, grain: 0.05, vignette: 0.55, ca: 2.5,
      zoom: 1 + 0.08 * wk,
      shake: [(hash(frameIdx(t), 1) - 0.5) * sh, (hash(frameIdx(t), 2) - 0.5) * sh],
      flash: cur ? 0.35 * Math.exp(-Math.max(0, t - cur.start) * 40) : 0,
    };
  }
}
void smoothstep;
