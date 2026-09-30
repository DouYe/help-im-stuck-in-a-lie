// MODE 'help' — the whole screen goes RED and one enormous word (the first word sung in the window,
// e.g. HELP) slams in, trembling, with echoes. The word is placed so the frame centre sits on the stem
// of its second letter: a 'through' transition into the next mode zooms into that stem and falls out
// of the letter into the next picture. `n: 2` escalates: rows of the word stream behind it and the
// screen strobes red/black on the 16ths.
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { rgba } from '../engine/palette';
import { F, font, measure } from '../engine/type';
import { clamp, hash, smoothstep, frameIdx } from '../engine/util';
import { Mode, EXIT_FOCUS } from '../danmaku/mode';
import { slamWord, wordText } from '../danmaku/kinetic';

export default class Help extends Mode {
  bg = new FSPass(/* glsl */ `
    uniform float t, strobe, shiver;
    float segD(vec2 p, vec2 a, vec2 b) { vec2 pa = p - a, ba = b - a; float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0); return length(pa - ba * h); }
    void main() {
      vec2 px = FRAG_PX; px.y = ${H.toFixed(1)} - px.y;
      // a red screen made of darker red symbols, streaming
      vec2 cell = vec2(16.0, 26.0);
      vec2 q = px + vec2(t * 260.0, 0.0) * (mod(floor(px.y / cell.y), 2.0) < 0.5 ? 1.0 : -1.0);
      vec2 ci = floor(q / cell), c0 = (ci + 0.5) * cell;
      vec2 u = (q - c0) / cell.y;
      float h = fract(sin(dot(ci, vec2(12.9898, 78.233))) * 43758.5453);
      float ink = h < 0.5 ? 1.0 - smoothstep(0.04, 0.08, segD(u, vec2(-0.25, 0.0), vec2(0.25, 0.0)))
                : h < 0.8 ? 1.0 - smoothstep(0.05, 0.09, length(u)) : 0.0;
      vec3 red = C_SIGNAL * (1.0 + 0.25 * shiver);
      vec3 col = mix(red, C_BLOOD * 0.8, ink * 0.55);
      col = mix(col, C_INK, strobe);
      fragColor = vec4(col, 1.0);
    }`, { t: { value: 0 }, strobe: { value: 0 }, shiver: { value: 0 } });
  L = new Layer2D();
  word = 'HELP';
  size = 400;
  cx = W / 2;

  init() {
    const ws = this.wordsIn();
    this.word = String(this.ctx.params.word ?? ws[0]?.w ?? 'HELP').replace(/[^\p{L}\p{N}']/gu, '').toUpperCase() || 'HELP';
    const fam = F.archivo(125, 900);
    this.size = Math.min(560, (1560 / measure(this.word, fam, 100)) * 100);
    // put the left stem of one letter (the one nearest the middle) on the frame centre: the zoom-through target
    const total = measure(this.word, fam, this.size);
    const chars = Array.from(this.word);
    let best = total / 2, pre = 0;
    for (const ch of chars) {
      const w = measure(ch, fam, this.size);
      const stem = pre + w * (ch === 'I' ? 0.5 : 0.2);
      if (/[BDEFHIKLMNPR]/.test(ch) && Math.abs(stem - total / 2) < Math.abs(best - total / 2)) best = stem;
      pre += w;
    }
    this.cx = W / 2 + (total / 2 - best);
    EXIT_FOCUS.set(this.ctx.params.entryIndex ?? 0, [0.5, 0.5]);
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    const n = this.param(t, 'n', 1);
    const ws = this.wordsIn();
    const first = ws[0];
    const t0 = first?.start ?? this.cutTime;
    const age = t - t0;
    // strobe (n >= 2): alternate on 16ths during the first beat
    const beat = 60 / audio.bpm;
    const q = Math.floor((t - t0) / (beat / 4));
    const strobe = n >= 2 && age >= 0 && age < beat ? (q % 2 ? 1 : 0) : 0;
    this.bg.u.t!.value = t; this.bg.u.strobe!.value = strobe; this.bg.u.shiver!.value = audio.hit('kick', t, 0.1);
    this.bg.render(renderer, out);

    const c = this.L.ctx; this.L.clear();
    if (n >= 2) {
      // rows of the word streaming behind, alternating directions
      const fam = F.archivo(125, 900), s = 150;
      c.font = font(fam, s); c.textBaseline = 'middle';
      const wd = measure(this.word + '  ', fam, s);
      for (let r = 0; r < 8; r++) {
        const y = 70 + r * 140, dir = r % 2 ? 1 : -1;
        const off = ((t * 700 * dir) % wd + wd) % wd;
        c.fillStyle = strobe ? rgba('signal', 0.5) : rgba('blood', 0.55);
        for (let x = -wd + off; x < W + wd; x += wd) c.fillText(this.word, x, y);
      }
    }
    const ink = strobe ? rgba('signal', 1) : rgba('ink', 1);
    slamWord(c, this.word, this.cx, H / 2, { size: this.size, age: Math.max(0, age), color: ink, echoes: n >= 2 ? 4 : 3, echoColor: strobe ? rgba('signal', 1) : rgba('ink', 1), jitter: n >= 2 ? 0.9 : 0.5, t });
    // the next word, small, under it (e.g. I'M)
    const next = ws[1];
    if (next && t >= next.start - 0.02) {
      c.save(); c.font = font(F.archivo(100, 800), 70); c.textAlign = 'center'; c.textBaseline = 'middle';
      c.fillStyle = strobe ? rgba('signal', 1) : rgba('bone', 1);
      c.fillText(wordText(next.w), W / 2, H / 2 + this.size * 0.55);
      c.restore();
    }
    comp.draw(renderer, this.L.upload(), out);

    const sh = (n >= 2 ? 26 : 16) * Math.exp(-Math.max(0, age) * 6) + 5;
    return {
      bloom: 0.25, bloomThreshold: 1.2, grain: 0.06, vignette: 0.25, ca: 2,
      zoom: 1 + 0.06 * Math.exp(-Math.max(0, age) * 8),
      shake: [(hash(frameIdx(t), 1) - 0.5) * sh, (hash(frameIdx(t), 2) - 0.5) * sh],
      flash: age >= 0 ? 0.8 * Math.exp(-age * 30) : 0,
    };
  }
}
void clamp; void smoothstep;
