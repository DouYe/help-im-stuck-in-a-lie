// SHOT — 'flap' (split-flap board). One idea: it's official — the board flips to REAL.
// A mechanical departures-style board: black flaps, white characters, a hinge across every tile. On the
// cut the whole board riffles to blank; each sung word then cascades onto its row, every tile clacking
// through a few wrong letters before it lands. The last word lands on orange flaps.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { rgba } from '../engine/palette';
import { F, font } from '../engine/type';
import { clamp, hash, ease } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { wordText } from '../danmaku/kinetic';
import { CLEAN } from './poster';

const COLS = 11, ROWS = 3, TW = 140, TH = 196, GAP = 10;
const X0 = (W - (COLS * (TW + GAP) - GAP)) / 2, Y0 = (H - (ROWS * (TH + GAP) - GAP)) / 2 + 20;
const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
const STEP = 0.042;

interface Plan { t0: number; seq: string[] } // a tile's flips: at t0 + i*STEP it becomes seq[i]

export default class Flap extends Mode {
  bg = new FSPass(/* glsl */ `
    void main() {
      vec2 p = FRAG_PX; p.y = ${H.toFixed(1)} - p.y;
      vec3 col = C_INK * (1.0 + 0.4 * snoise(p * 0.004));
      fragColor = vec4(col, 1.0);
    }`);
  L = new Layer2D();
  plans: Plan[][] = [];          // per tile, a list of flip runs in time order
  hot: boolean[] = [];

  init() {
    const beat = 60 / this.ctx.audio.bpm;
    const start = this.cutTime;
    const ws = this.wordsIn();
    const rows: string[] = ['', '', ''];
    ws.slice(0, ROWS).forEach((w, i) => (rows[i] = wordText(w.w)));
    for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
      const i = r * COLS + c;
      const runs: Plan[] = [];
      // on the cut: riffle to blank
      const n0 = 3 + Math.floor(hash(i, 1) * 5);
      runs.push({ t0: start + (r * COLS + c) * 0.011, seq: [...Array.from({ length: n0 }, (_, k) => CHARS[Math.floor(hash(i, k, 2) * CHARS.length)]!), ' '] });
      // each word cascades onto its row
      const w = ws[r];
      if (w) {
        const word = rows[r]!;
        const lead = Math.floor((COLS - word.length) / 2);
        const ch = c >= lead && c < lead + word.length ? word[c - lead]! : ' ';
        const n = 2 + Math.floor(hash(i, 3) * 5);
        runs.push({ t0: w.start - 0.02 + c * (beat / 16), seq: [...Array.from({ length: n }, (_, k) => CHARS[Math.floor(hash(i, k, 4) * CHARS.length)]!), ch] });
      }
      this.plans.push(runs);
      this.hot.push(r === Math.min(ws.length, ROWS) - 1);
    }
  }

  /** The tile's character before and after the flip in progress, the flip phase 0..1 (1 = settled),
   *  and which run it's in (-1 before the first). */
  state(i: number, t: number): { from: string; to: string; ph: number; run: number } {
    let cur = CHARS[Math.floor(hash(i, 9) * CHARS.length)]!;
    let run = -1;
    const runs = this.plans[i]!;
    for (let r = 0; r < runs.length; r++) {
      const p = runs[r]!;
      if (t < p.t0) break;
      run = r;
      const k = Math.floor((t - p.t0) / STEP);
      if (k >= p.seq.length) { cur = p.seq[p.seq.length - 1]!; continue; }
      const from = k === 0 ? cur : p.seq[k - 1]!;
      return { from, to: p.seq[k]!, ph: ((t - p.t0) % STEP) / STEP, run };
    }
    return { from: cur, to: cur, ph: 1, run };
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp } = this.ctx;
    const t = f.t;
    this.bg.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const fam = F.archivo(112, 800), fs = 148;
    const half = (ch: string, x: number, y: number, top: boolean, hot: boolean, shade: number, sy = 1) => {
      // one half of a flap, optionally squashed toward the hinge (sy)
      const mid = y + TH / 2;
      c.save();
      c.beginPath(); c.rect(x, top ? y : mid, TW, TH / 2); c.clip();
      c.translate(0, mid); c.scale(1, sy); c.translate(0, -mid);
      c.fillStyle = hot ? rgba('signal', 1) : rgba('ink2', 1);
      c.beginPath(); c.roundRect(x, y, TW, TH, 10); c.fill();
      if (ch !== ' ') {
        c.font = font(fam, fs); c.textAlign = 'center'; c.textBaseline = 'middle';
        c.fillStyle = hot ? rgba('ink', 1) : rgba('bone', 1);
        c.fillText(ch, x + TW / 2, y + TH / 2 + fs * 0.05);
      }
      // light from above: the lower half a touch brighter, the moving flap darker
      c.fillStyle = `rgba(0,0,0,${(top ? 0.12 : 0) + shade})`;
      c.fillRect(x, y, TW, TH);
      c.restore();
    };
    for (let r = 0; r < ROWS; r++) for (let col = 0; col < COLS; col++) {
      const i = r * COLS + col;
      const x = X0 + col * (TW + GAP), y = Y0 + r * (TH + GAP);
      const { from, to, ph, run } = this.state(i, t);
      const wordRun = this.plans[i]!.length > 1 && run === this.plans[i]!.length - 1;
      const hot = this.hot[i]! && wordRun && to !== ' ' && ph >= 1;
      const hotTo = this.hot[i]! && wordRun && to !== ' ';
      if (ph >= 1) { half(to, x, y, true, hot, 0); half(to, x, y, false, hot, 0); }
      else if (ph < 0.5) {
        // the top flap (old character) falls toward the hinge, revealing the new top half behind it
        half(to, x, y, true, hotTo, 0); half(from, x, y, false, false, 0);
        half(from, x, y, true, false, 0.35 * ph * 2, 1 - ph * 2);
      } else {
        // the flap has passed the hinge: it shows the new bottom half, opening down over the old one
        half(to, x, y, true, hotTo, 0); half(from, x, y, false, false, 0);
        half(to, x, y, false, hotTo, 0.35 * (1 - (ph - 0.5) * 2), (ph - 0.5) * 2);
      }
      // the hinge
      c.fillStyle = rgba('ink', 1); c.fillRect(x, y + TH / 2 - 1.5, TW, 3);
      c.fillStyle = rgba('graphite', 1); c.fillRect(x - 3, y + TH / 2 - 5, 6, 10); c.fillRect(x + TW - 3, y + TH / 2 - 5, 6, 10);
    }
    // the board's own labels
    c.font = font(F.mono(500), 15); c.fillStyle = rgba('ash', 0.9); c.textAlign = 'left'; c.textBaseline = 'alphabetic';
    c.fillText('STATUS', X0, Y0 - 22);
    c.textAlign = 'right';
    c.fillText('CONFIRMED', X0 + COLS * (TW + GAP) - GAP, Y0 - 22);
    comp.draw(renderer, this.L.upload(), out);

    const ws = this.wordsIn();
    const hit = ws.reduce((m, w) => (t >= w.start ? Math.max(m, Math.exp(-(t - w.start) * 16)) : m), 0);
    const push = ease.inOutCubic(clamp((t - this.cutTime) / 2.4));
    return { ...CLEAN, zoom: 1 + 0.035 * push + 0.01 * hit, shake: [0, 2 * hit] };
  }
}
