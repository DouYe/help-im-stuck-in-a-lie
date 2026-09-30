// MODE 'cage' — "The cell" (works on any lines). The first word slams full-frame and squashes into a box
// whose walls are a marquee of the KEY WORD (param \`word\`, default: the first held note). Every sung
// word snaps the box smaller; the held note lights the walls; repeats of the key word invert the frame.
// Hard cut on the drop: HELP! slams full-frame, squashes to a hairline, and the hairline becomes a box.
// The walls of the box are made of the word LIE (a marquee running clockwise), with engineering
// dimension lines that tick down as the box shrinks on every sung word. The spark is trapped inside,
// bouncing wall to wall. On the held "LIE" the walls light up orange clockwise; on the four stuttered
// LIEs the frame inverts per beat and the box slams smaller each time, then collapses to the spark.
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { Mode } from '../danmaku/mode';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { LineBatch } from '../engine/lines';
import { LIN, rgba } from '../engine/palette';
import { F, font, measure } from '../engine/type';
import { Lyrics, type Word } from '../engine/lyrics';
import { clamp, ease, hash, keys, lerp, smoothstep, frameIdx, type Key } from '../engine/util';
import { sparkHead, sparkParticles } from './_motifs';

const CX = W / 2, CY = H / 2 + 10;
const tri = (x: number) => 1 - 4 * Math.abs(x - Math.floor(x + 0.5)); // triangle wave in [-1, 1]

export default class Cage extends Mode {
  bg = new FSPass(/* glsl */ `
    uniform float t, glow, hw, hh, inv;
    void main() {
      vec2 p = FRAG_PX; p.y = ${H.toFixed(1)} - p.y;
      vec2 d = abs(p - vec2(${CX.toFixed(1)}, ${CY.toFixed(1)})) - vec2(hw, hh);
      float outside = step(0.0, max(d.x, d.y));
      // engraved hatching outside the cell (the world it can't reach), plain ink inside
      float dark = 0.55 + 0.25 * snoise(p * 0.004 + t * 0.05);
      float e = engrave(p, dark, 0.16, 0.785);
      vec3 col = C_INK;
      col = mix(col, C_INK2 * 1.6, e * 0.55 * outside);
      col += C_SIGNAL * glow * 0.08 * (1.0 - outside);
      // inverted beats: bone paper with ink hatching (orange stays orange)
      vec3 paper = mix(C_BONE * 0.92, C_ASH * 0.7, e * 0.35 * outside);
      col = mix(col, paper, inv);
      fragColor = vec4(col, 1.0);
    }`, { t: { value: 0 }, glow: { value: 0 }, hw: { value: 0 }, hh: { value: 0 }, inv: { value: 0 } });

  lb = new LineBatch(20000, { blend: 'add' });
  L = new Layer2D();
  slam!: Word; slamText = 'HELP!'; key = 'LIE';
  steps: Word[] = []; held!: Word; stut: Word[] = [];
  sizeW: Key[] = []; sizeH: Key[] = [];

  init() {
    const au = this.ctx.audio;
    const ws = this.wordsIn();
    const fallback = { w: 'HELP!', start: this.ctx.start + 0.2, end: this.ctx.start + 0.6, line: 0, index: 0, gi: 0 } as Word;
    this.slam = ws[0] ?? fallback;
    this.slamText = this.slam.w.toUpperCase();
    const tIn = au.timeOfBeat(Math.round(au.beatAt(this.slam.start)) + 2); // walls slam in two beats later
    const after = ws.filter((w) => w.start >= tIn - 0.05);
    this.held = after.find((w) => w.end - w.start > 0.45) ?? after[after.length - 1] ?? this.slam;
    this.key = String(this.ctx.params.word ?? this.held.w).replace(/[^\p{L}\p{N}']/gu, '').toUpperCase() || 'LIE';
    const norm = (x: string) => x.replace(/[^\p{L}\p{N}']/gu, '').toUpperCase();
    this.stut = after.filter((w) => w.start > this.held.start + 0.05 && norm(w.w) === this.key);
    this.steps = after.filter((w) => w !== this.held && !this.stut.includes(w));
    const W0: Key[] = [[0, 1500], [tIn - 0.001, 1500], [tIn + 0.12, 800, ease.outExpo]];
    const H0: Key[] = [[0, 900], [tIn - 0.001, 900], [tIn + 0.12, 400, ease.outExpo]];
    const ordered = [...after].sort((a, b) => a.start - b.start);
    let cw = 800, ch = 400;
    for (const w of ordered) {
      const shrink = w === this.held ? 0.97 : this.stut.includes(w) ? 0.86 : 0.94;
      cw = Math.max(300, cw * shrink); ch = Math.max(170, ch * shrink);
      W0.push([w.start, W0[W0.length - 1]![1]], [w.start + 0.1, cw, ease.outExpo]);
      H0.push([w.start, H0[H0.length - 1]![1]], [w.start + 0.1, ch, ease.outExpo]);
      if (w === this.held) { // the held note squeezes continuously
        cw *= 0.86; ch *= 0.86;
        W0.push([w.end, cw, ease.inOutCubic]); H0.push([w.end, ch, ease.inOutCubic]);
      }
    }
    const tEnd = Math.max(tIn + 0.5, this.ctx.end - 0.55);
    W0.push([Math.max(tEnd, W0[W0.length - 1]![0] + 0.01), cw], [Math.max(tEnd, W0[W0.length - 1]![0] + 0.01) + 0.2, 0, ease.inExpo]);
    H0.push([Math.max(tEnd, H0[H0.length - 1]![0] + 0.01), ch], [Math.max(tEnd, H0[H0.length - 1]![0] + 0.01) + 0.2, 0, ease.inExpo]);
    this.sizeW = W0; this.sizeH = H0;
    this.tIn = tIn; this.tEnd = tEnd;
  }
  tIn = 0; tEnd = 0;

  box(t: number) { return { hw: keys(t, this.sizeW), hh: keys(t, this.sizeH) }; }

  spark(t: number) {
    const { hw, hh } = this.box(t);
    const m = 34;
    return { x: CX + Math.max(0, hw - m) * tri(t * 0.83 + 0.17), y: CY + Math.max(0, hh - m) * tri(t * 1.31 + 0.61) };
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    const { hw, hh } = this.box(t);
    const lw = this.stut, held = this.held;
    const heldP = clamp((t - held.start) / (held.end - held.start));
    const inHeld = t >= held.start && t < held.end + 0.1;
    // which LIE stutter are we on (for the per-beat invert)
    let stut = -1;
    for (let i = 0; i < lw.length; i++) if (t >= lw[i]!.start) stut = i;
    const invert = stut >= 0 && t < this.tEnd ? (stut % 2 === 0 ? 1 : 0) : 0;

    this.bg.u.t!.value = t; this.bg.u.hw!.value = hw; this.bg.u.hh!.value = hh;
    this.bg.u.glow!.value = inHeld ? heldP : 0;
    this.bg.u.inv!.value = invert;
    this.bg.render(renderer, out);

    const c = this.L.ctx; this.L.clear();
    const boxOn = t >= this.tIn;

    // ---- HELP! slam (before the walls arrive)
    if (t < this.tIn + 0.05) {
      const k = t - this.slam.start;
      const s = 1 + 0.12 * Math.exp(-k * 14);
      const squash = keys(t, [[this.tIn - 0.28, 1], [this.tIn - 0.02, 0.012, ease.inExpo]]);
      const stretch = keys(t, [[this.tIn - 0.28, 1], [this.tIn, 1.35, ease.inExpo]]);
      const fam = F.archivo(125, 900);
      const size = Math.min(1480 / (measure(this.slamText, fam, 100) / 100), 900);
      c.save(); c.translate(CX, CY); c.scale(s * stretch, s * squash);
      c.font = font(fam, size); c.textAlign = 'center'; c.textBaseline = 'middle';
      c.fillStyle = rgba('bone', 1); c.fillText(this.slamText, 0, size * 0.04);
      c.restore();
    }

    if (boxOn) {
      // ---- walls: marquee of LIE, clockwise, lit orange clockwise during the held note
      const band = 58, fs = 50, fam = F.archivo(62, 900);
      c.font = font(fam, fs); c.textBaseline = 'middle'; c.textAlign = 'left';
      const unit = `${this.key}  ·  `;
      const uw = measure(unit, fam, fs);
      const marq = (t - this.tIn) * 140;
      const lit = inHeld ? heldP * 4 : t > held.end ? 4 : 0;
      const walls = [ // [centre x, centre y, length, angle]
        [CX, CY - hh - band / 2, 2 * hw + 2 * band, 0],
        [CX + hw + band / 2, CY, 2 * hh + 2 * band, Math.PI / 2],
        [CX, CY + hh + band / 2, 2 * hw + 2 * band, 0], // bottom stays upright (runs right-to-left)
        [CX - hw - band / 2, CY, 2 * hh + 2 * band, -Math.PI / 2],
      ] as const;
      walls.forEach(([x, y, len, ang], i) => {
        if (len < 4) return;
        c.save(); c.translate(x, y); c.rotate(ang);
        c.beginPath(); c.rect(-len / 2, -band / 2, len, band); c.clip();
        c.fillStyle = rgba(invert ? 'bone' : 'ink2', 1); c.fillRect(-len / 2, -band / 2, len, band);
        const wl = clamp(lit - i); // this wall's lit fraction (the wipe travels along it)
        const n = Math.ceil(len / uw) + 2;
        for (let j = -1; j < n; j++) {
          const gx = -len / 2 + j * uw + (i === 2 ? uw - (marq % uw) : marq % uw);
          const along = (gx + len / 2) / len, on = (i === 2 ? 1 - along - uw / len : along) < wl;
          c.fillStyle = on ? rgba('signal', 1) : rgba(invert ? 'ash' : 'graphite', 1);
          c.fillText(unit, gx, 2);
        }
        c.restore();
      });

      // ---- dimension lines (engineering drawing): width above, height at the right
      c.strokeStyle = rgba(invert ? 'graphite' : 'ash', 0.7); c.fillStyle = rgba(invert ? 'ink' : 'ash', 0.9); c.lineWidth = 1;
      c.font = font(F.mono(500), 15); c.textAlign = 'center'; c.textBaseline = 'alphabetic';
      const yd = CY - hh - band - 34, xd = CX + hw + band + 40;
      if (yd > 20 && hw > 20) {
        c.beginPath(); c.moveTo(CX - hw - band, yd); c.lineTo(CX + hw + band, yd);
        c.moveTo(CX - hw - band, yd - 8); c.lineTo(CX - hw - band, yd + 8); c.moveTo(CX + hw + band, yd - 8); c.lineTo(CX + hw + band, yd + 8); c.stroke();
        c.fillText(`W ${Math.round(2 * hw)} px`, CX, yd - 10);
      }
      if (xd < W - 30 && hh > 20) {
        c.beginPath(); c.moveTo(xd, CY - hh - band); c.lineTo(xd, CY + hh + band);
        c.moveTo(xd - 8, CY - hh - band); c.lineTo(xd + 8, CY - hh - band); c.moveTo(xd - 8, CY + hh + band); c.lineTo(xd + 8, CY + hh + band); c.stroke();
        c.save(); c.translate(xd + 22, CY); c.rotate(Math.PI / 2); c.fillText(`H ${Math.round(2 * hh)} px`, 0, 0); c.restore();
      }
      c.textAlign = 'left'; c.font = font(F.mono(400), 14); c.fillStyle = rgba('graphite', 1);
      const area = (4 * hw * hh) / (W * H);
      if (hw > 40) c.fillText(`CELL 01 · ${(area * 100).toFixed(1)}% OF FRAME · EXITS: 0`, CX - hw - band, CY + hh + band + 30);

      // ---- lyric inside the cell
      c.save(); c.beginPath(); c.rect(CX - hw, CY - hh, 2 * hw, 2 * hh); c.clip();
      if (t < held.start) {
        // "I'M STUCK IN A", one word per beat, stacked left, pushed by the walls
        const fam2 = F.archivo(100, 800), size = 96;
        c.font = font(fam2, size); c.textBaseline = 'alphabetic';
        let y = CY - hh + 40 + size;
        let x = CX - hw + 48;
        for (const w of this.steps) {
          if (t < w.start - 0.001) break;
          const k = t - w.start, s = 1 + 0.3 * Math.exp(-k * 20);
          c.save(); c.translate(x, y); c.scale(s, s);
          c.fillStyle = rgba('bone', 1); c.fillText(w.w.toUpperCase(), 0, 0); c.restore();
          x += measure(w.w.toUpperCase() + ' ', fam2, size);
          if (x > CX + hw - 300) { x = CX - hw + 48; y += size * 1.02; }
        }
      }
      // the held LIE / the stuttered LIEs: one giant word that fills the cell as it shrinks
      const lieOn = t >= held.start && t < this.tEnd + 0.2;
      if (lieOn) {
        const cur = stut >= 0 ? lw[stut]! : held;
        const k = t - cur.start;
        const fam3 = F.archivo(stut >= 2 ? 62 : stut >= 0 ? 87 : 125, 900);
        const target = 2 * hw - 60;
        const size = Math.min((target / (measure(this.key, fam3, 100) / 100)), 2 * hh * 1.25);
        const s = 1 + 0.18 * Math.exp(-k * 16);
        c.save(); c.translate(CX, CY); c.scale(s, s);
        c.font = font(fam3, size); c.textAlign = 'center'; c.textBaseline = 'middle';
        // karaoke: the held note fills orange left to right as it's sung
        const p = Lyrics.wordProgress(cur, t);
        const wWord = measure(this.key, fam3, size);
        c.fillStyle = rgba(invert ? 'ink' : 'graphite', 1); c.fillText(this.key, 0, size * 0.05);
        c.beginPath(); c.rect(-wWord / 2, -size, wWord * (stut >= 0 ? 1 : p), size * 2); c.clip();
        c.fillStyle = rgba('signal', 1); c.fillText(this.key, 0, size * 0.05);
        c.restore();
      }
      c.restore();
    }
    comp.draw(renderer, this.L.upload(), out);

    // ---- the spark, trapped: a trail of its recent path plus sputter, all additive
    this.lb.clear();
    if (boxOn) {
      const sig = LIN.signal;
      let prev = this.spark(t - 0.6);
      for (let i = 1; i <= 90; i++) {
        const tt = t - 0.6 + (0.6 * i) / 90;
        if (tt < this.tIn) { prev = this.spark(tt); continue; }
        const p = this.spark(tt), a = i / 90;
        this.lb.seg2(prev.x, prev.y, p.x, p.y, 1.5 + 2 * a, [sig[0] * 2 * a, sig[1] * 2 * a, sig[2] * 2 * a], a);
        prev = p;
      }
      const h = this.spark(t);
      sparkParticles(this.lb, t, (tb) => (tb < this.tIn || tb > t ? null : this.spark(tb)), { rate: (tb) => 60 + 200 * audio.hit('kick', tb, 0.1), rateMax: 260, speed: 300, seed: 5 });
      const collapse = smoothstep(this.tEnd, this.tEnd + 0.2, t);
      sparkHead(this.lb, h.x, h.y, t, 1 + collapse * 2.5, 1 + collapse * 3);
    }
    this.lb.render(renderer, out);

    // ---- camera: punch-ins on the stutters and the slam, shake on hits, flash on the cut in
    const kIn = t - this.tIn;
    let zoom = 1 + (kIn >= 0 ? 0.06 * Math.exp(-kIn * 10) : 0);
    if (stut >= 0) zoom += 0.1 * Math.exp(-(t - lw[stut]!.start) * 12);
    const hitK = audio.hit('kick', t, 0.08);
    const sh = 10 * Math.exp(-Math.max(0, t - this.slam.start) * 9) + 6 * hitK + (stut >= 0 ? 8 * Math.exp(-(t - lw[stut]!.start) * 14) : 0);
    const collapse = smoothstep(this.tEnd, this.tEnd + 0.2, t);
    return {
      bloom: 0.6 + collapse, grain: 0.06, vignette: 0.4, paper: invert, zoom,
      shake: [(hash(frameIdx(t), 7) - 0.5) * sh, (hash(frameIdx(t), 8) - 0.5) * sh],
      flash: (t >= this.slam.start ? 0.35 * Math.exp(-(t - this.slam.start) * 16) : 0) + 1.2 * smoothstep(this.tEnd + 0.12, this.tEnd + 0.2, t) * (1 - smoothstep(this.tEnd + 0.2, this.tEnd + 0.3, t)),
      fade: smoothstep(this.tEnd + 0.18, this.tEnd + 0.3, t),
    };
  }
}
