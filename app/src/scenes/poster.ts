// SHOT — 'poster' (screen print). One idea: a scream printed as a poster.
// A flat orange sheet, a black HELP pulled across the whole width (a second, slightly misregistered
// pass under it), and the rest of the line printed word by word on a strip below, the last word
// knocked out of a black bar. Printer's marks in the corners. After the line the camera leans into the
// stem of the letter at the frame centre: a 'through' cut falls into it.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { rgba } from '../engine/palette';
import { F, font, measure } from '../engine/type';
import { clamp, ease, hash, frameIdx, smoothstep } from '../engine/util';
import { Mode, EXIT_FOCUS } from '../danmaku/mode';
import { wordText } from '../danmaku/kinetic';

export const CLEAN = { bloom: 0, halation: 0, ca: 0, grain: 0.035, vignette: 0.18 };

export default class Poster extends Mode {
  bg = new FSPass(/* glsl */ `
    uniform float seed;
    void main() {
      vec2 p = FRAG_PX; p.y = ${H.toFixed(1)} - p.y;
      // screen-printed orange: flat ink, faint mottling where the squeegee ran light, paper fibres
      float mott = snoise(p * 0.004 + seed) * 0.5 + snoise(p * 0.02 + seed * 2.0) * 0.25;
      float fib = snoise(vec2(p.x * 0.9, p.y * 0.05) + seed * 3.0);
      vec3 col = C_SIGNAL * (0.96 + 0.035 * mott) + 0.012 * fib;
      fragColor = vec4(col, 1.0);
    }`, { seed: { value: 3.7 } });
  L = new Layer2D();
  word = 'HELP'; size = 400; cx = W / 2;

  focus: [number, number] = [W / 2, H / 2];
  /** Words of this shot only (not the next line, sung during the outgoing transition). */
  own() { return this.wordsIn(this.ctx.start, this.ctx.params.cutOut ?? this.ctx.end); }

  init() {
    const ws = this.own();
    this.word = wordText(ws[0]?.w ?? 'HELP');
    const fam = F.archivo(125, 900);
    this.size = Math.min(620, (1760 / measure(this.word, fam, 100)) * 100);
    // the next shot falls into this picture's black: aim the zoom at the fattest bit of ink near the
    // middle (the centre of the largest circle that fits inside a letter, by a distance transform)
    const total = measure(this.word, fam, this.size);
    const cw = Math.ceil(total) + 40, ch = Math.ceil(this.size * 1.3);
    const cv = document.createElement('canvas'); cv.width = cw; cv.height = ch;
    const m = cv.getContext('2d', { willReadFrequently: true })!;
    m.font = font(fam, this.size); m.textAlign = 'center'; m.textBaseline = 'middle'; m.fillStyle = '#000';
    m.fillText(this.word, cw / 2, ch / 2 + this.size * 0.04);
    const img = m.getImageData(0, 0, cw, ch).data;
    const G = 4, gw = Math.ceil(cw / G), gh = Math.ceil(ch / G);
    const dist = new Float32Array(gw * gh).fill(1e9);
    const queue: number[] = [];
    for (let gy = 0; gy < gh; gy++) for (let gx = 0; gx < gw; gx++) {
      const x = Math.min(cw - 1, gx * G + 2), y = Math.min(ch - 1, gy * G + 2);
      if (img[(y * cw + x) * 4 + 3]! < 128) { dist[gy * gw + gx] = 0; queue.push(gy * gw + gx); }
    }
    for (let qi = 0; qi < queue.length; qi++) {
      const i = queue[qi]!, gx = i % gw, gy = (i / gw) | 0, d = dist[i]! + 1;
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]] as const) {
        const nx = gx + dx, ny = gy + dy;
        if (nx < 0 || ny < 0 || nx >= gw || ny >= gh) continue;
        const j = ny * gw + nx;
        if (dist[j]! > d) { dist[j] = d; queue.push(j); }
      }
    }
    let bi = -1, bs = -1e9;
    for (let i = 0; i < dist.length; i++) {
      if (dist[i]! <= 0) continue;
      const gx = i % gw, gy = (i / gw) | 0;
      const score = dist[i]! * G - 0.12 * Math.hypot(gx * G - cw / 2, gy * G - ch / 2);
      if (score > bs) { bs = score; bi = i; }
    }
    this.focus = bi < 0 ? [W / 2, H / 2] : [W / 2 + (bi % gw) * G + 2 - cw / 2, H / 2 + ((bi / gw) | 0) * G + 2 - ch / 2];
    EXIT_FOCUS.set(this.ctx.params.entryIndex ?? 0, [this.focus[0] / W, this.focus[1] / H]);
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    this.bg.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const ws = this.own();
    const first = ws[0];
    const press = (t0: number) => (t >= t0 ? 1 + 0.05 * Math.exp(-(t - t0) * 22) : 0);
    const thump = ws.reduce((m, w) => (t >= w.start ? Math.max(m, Math.exp(-(t - w.start) * 30)) : m), 0);
    const jx = (hash(frameIdx(t), 1) - 0.5) * 3 * thump, jy = (hash(frameIdx(t), 2) - 0.5) * 3 * thump;
    // after the line the camera leans into the ink it will fall through (baked into the picture, so
    // the transition that follows starts from exactly this frame)
    const end = this.ctx.params.cutOut ?? this.ctx.end;
    const lastW = ws[ws.length - 1];
    const lean = lastW ? ease.inCubic(clamp((t - (lastW.end + 0.1)) / Math.max(0.2, end - lastW.end - 0.1))) : 0;
    const z = 1 + 0.35 * lean;
    c.save();
    c.translate(this.focus[0], this.focus[1]); c.scale(z, z); c.translate(-this.focus[0], -this.focus[1]);

    // ---- HELP: second pass (misregistered, dark orange) then the black pass
    const fam = F.archivo(125, 900);
    if (first && t >= first.start - 0.001) {
      const s = press(first.start);
      c.save(); c.translate(this.cx + jx, H / 2 + jy); c.scale(s, s);
      c.font = font(fam, this.size); c.textAlign = 'center'; c.textBaseline = 'middle';
      c.fillStyle = rgba('blood', 0.55); c.fillText(this.word, 7, this.size * 0.04 + 5);
      c.fillStyle = rgba('ink', 1); c.fillText(this.word, 0, this.size * 0.04);
      c.restore();
    }
    // ---- the rest of the line on a strip below, word by word; the last word knocked out of a black bar
    const rest = ws.slice(1);
    const fam2 = F.archivo(125, 900), s2 = 76;
    c.font = font(fam2, s2); c.textBaseline = 'middle';
    const sep = measure('  ', fam2, s2);
    const widths = rest.map((w) => measure(wordText(w.w), fam2, s2));
    const total = widths.reduce((a, b) => a + b, 0) + sep * Math.max(0, rest.length - 1) + 40;
    let x = W / 2 - total / 2;
    const y = H / 2 + this.size * 0.5 + 70;
    rest.forEach((w, i) => {
      const txt = wordText(w.w), ww = widths[i]!;
      const last = i === rest.length - 1;
      if (t >= w.start - 0.001) {
        const s = press(w.start);
        c.save(); c.translate(x + ww / 2 + (last ? 20 : 0) + jx, y + jy); c.scale(s, s);
        c.textAlign = 'center';
        if (last) {
          c.fillStyle = rgba('ink', 1); c.fillRect(-ww / 2 - 22, -s2 * 0.62, ww + 44, s2 * 1.24);
          c.fillStyle = rgba('bone', 1); c.fillText(txt, 0, s2 * 0.05);
        } else { c.fillStyle = rgba('ink', 1); c.fillText(txt, 0, s2 * 0.05); }
        c.restore();
      }
      x += ww + sep + (last ? 40 : 0);
    });

    // ---- printer's marks: registration targets in the corners, a colour bar, a job line
    c.strokeStyle = rgba('ink', 0.8); c.lineWidth = 1.2;
    for (const [mx, my] of [[70, 70], [W - 70, 70], [70, H - 70], [W - 70, H - 70]] as const) {
      c.beginPath(); c.arc(mx, my, 14, 0, Math.PI * 2); c.moveTo(mx - 24, my); c.lineTo(mx + 24, my); c.moveTo(mx, my - 24); c.lineTo(mx, my + 24); c.stroke();
    }
    const cb = ['ink', 'blood', 'signal', 'bone'] as const;
    cb.forEach((k, i) => { c.fillStyle = rgba(k, 1); c.fillRect(W / 2 - 80 + i * 40, H - 58, 34, 16); });
    c.font = font(F.mono(500), 13); c.fillStyle = rgba('ink', 0.85); c.textAlign = 'left';
    c.fillText('PULL 1 / 1   ·   2 SCREENS   ·   INK ON ORANGE', 110, H - 46);
    c.textAlign = 'right';
    c.fillText(`${audio.bpm.toFixed(0)} BPM   ·   BAR ${Math.floor(f.bar) + 1}`, W - 110, H - 46);
    c.restore();
    comp.draw(renderer, this.L.upload(), out);
    return { ...CLEAN, zoom: 1 + 0.012 * thump, shake: [0, 0] };
  }
}
void smoothstep;
