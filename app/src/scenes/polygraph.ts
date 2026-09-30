// MODE 'polygraph' — lie-detector chart paper (works on any lines: each word jolts the voice pen,
// held notes send it off the scale, the first held note gets a DECEPTION INDICATED stamp).
// Bone chart paper scrolls under four pens at exactly one major division per beat, so the grid itself
// keeps time. The pens are driven by the music analysis (breath = pad, pulse = kicks, GSR = bass),
// and the signal pen — the spark — by the vocal: it jolts on every sung word and goes off the scale on "LIE".
// Each lyric word is printed onto the paper under the pen at the moment it's sung, then scrolls away
// with the chart. Ends on a DECEPTION INDICATED stamp and a snare roll that speeds the paper up.
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { Mode } from '../danmaku/mode';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { LineBatch } from '../engine/lines';
import { LIN, rgba } from '../engine/palette';
import { F, font } from '../engine/type';
import type { Line, Word } from '../engine/lyrics';
import { clamp, ease, hash, lerp, noise1, prog, smoothstep, frameIdx, keys } from '../engine/util';
import { sparkHead, sparkParticles } from './_motifs';

const PEN_X = 1330;
const CH = [ // channel baselines (y px) and names
  { y: 370, name: 'PNEUMO', sub: 'breath' },
  { y: 515, name: 'CARDIO', sub: 'pulse / kick' },
  { y: 660, name: 'EDA', sub: 'skin conductance' },
  { y: 850, name: 'VOICE', sub: 'the answer' },
];

export default class Polygraph extends Mode {
  paper = new FSPass(/* glsl */ `
    uniform float scroll, speedPx, penX, lie;
    void main() {
      vec2 p = FRAG_PX; p.y = ${H.toFixed(1)} - p.y;          // logical px, y down
      float x = p.x + scroll;                                   // paper coordinate
      float minor = speedPx / 5.0;
      float dMin = abs(mod(x + minor * 0.5, minor) - minor * 0.5);
      float dMaj = abs(mod(x + speedPx * 0.5, speedPx) - speedPx * 0.5);
      float dBar = abs(mod(x + speedPx * 2.0, speedPx * 4.0) - speedPx * 2.0);
      float dY = abs(mod(p.y + 17.0, 34.0) - 17.0);
      vec3 col = C_BONE * 0.93;
      // paper tooth
      col *= 0.97 + 0.03 * snoise(p * 0.9);
      float ink = 0.0;
      ink = max(ink, pxLine(dMin, 0.3, 1.0) * 0.10);
      ink = max(ink, pxLine(dY, 0.3, 1.0) * 0.10);
      ink = max(ink, pxLine(dMaj, 0.5, 1.4) * 0.28);
      ink = max(ink, pxLine(dBar, 0.9, 2.0) * 0.45);
      col = mix(col, C_ASH * 0.55, ink);
      // pen carriage shadow line
      col = mix(col, C_GRAPHITE, pxLine(abs(p.x - penX), 0.4, 1.2) * 0.35);
      // paper edges (the chart strip)
      float edge = smoothstep(150.0, 148.0, p.y) + smoothstep(${(H - 110).toFixed(1)}, ${(H - 108).toFixed(1)}, p.y);
      col = mix(col, C_INK2, clamp(edge, 0.0, 1.0));
      // "LIE": the paper blushes orange around the pen
      float g = exp(-pow((p.x - penX) / 520.0, 2.0)) * lie;
      col = mix(col, C_SIGNAL * 0.9, g * 0.35);
      fragColor = vec4(col, 1.0);
    }`, { scroll: { value: 0 }, speedPx: { value: 240 }, penX: { value: PEN_X }, lie: { value: 0 } });

  ink = new LineBatch(40000, { blend: 'normal' });
  glow = new LineBatch(20000, { blend: 'add' });
  text = new Layer2D();
  words: Word[] = [];
  held: Word[] = [];
  beat = 0.46875;
  speedPx = 240; // px per beat

  init() {
    const ly = this.ctx.lyrics;
    this.beat = 60 / this.ctx.audio.bpm;
    this.words = this.wordsIn(this.ctx.start - 4, this.ctx.end);
    // held notes: the last word of each line when it is sung long
    this.held = this.linesIn(this.ctx.start - 4, this.ctx.end).map((l) => l.words[l.words.length - 1]!).filter((w) => w.end - w.start > 0.45);
    void ly;
  }

  /** Paper position (px) at time t: constant speed, then the snare roll into the cut accelerates it. */
  scrollAt(t: number) {
    const v = this.speedPx / this.beat;
    const t0 = this.ctx.end - 2 * this.beat;           // last two beats before the cut
    const base = t * v;
    if (t <= t0) return base;
    const u = t - t0;
    return base + v * 1.6 * u * u / (2 * this.beat);    // quadratic acceleration
  }

  /** The held note that sends the pen off the scale (the first one in the window, if any). */
  get lieWord(): Word | null { return this.held.find((w) => w.start >= this.ctx.start - 0.2) ?? this.held[0] ?? null; }

  /** Signal pen deflection (px, up = negative) at song time t. */
  voice(t: number) {
    const a = this.ctx.audio;
    let y = noise1(t * 7, 3) * 3;
    for (const w of this.words) {
      if (t < w.start || t > w.end + 0.6) continue;
      const k = t - w.start;
      const isLie = this.held.includes(w);
      if (isLie) {
        // off the scale: slams to the top stop, then scribbles there while the note is held
        const hold = clamp((t - w.start) / 0.08);
        const scrib = Math.sin(t * 90) * 30 + Math.sin(t * 57) * 40 + noise1(t * 40, 9) * 90;
        const rel = 1 - smoothstep(w.end, w.end + 0.35, t);
        y += (-330 * hold + scrib * hold) * rel;
      } else {
        // a jolt per word: a sharp attack and a damped ring
        const amp = w.index === 0 ? 170 : 70 + 40 * hash(w.gi, 2);
        y += -amp * Math.exp(-k * 7) * Math.cos(k * 38) * clamp(k / 0.02);
      }
    }
    return y + -a.env('vocal', t) * 20;
  }

  chan(i: number, t: number) {
    const a = this.ctx.audio;
    switch (i) {
      case 0: return Math.sin(t * 2.1) * 28 + a.env('other', t) * -30;           // breath
      case 1: return -a.hit('kick', t, 0.05) * 70 + a.hit('kick', t - 0.09, 0.04) * 25 + noise1(t * 30, 1) * 1.5; // pulse
      case 2: return -a.env('bass', t) * 60 + Math.sin(t * 0.7) * 12;            // EDA
      default: return this.voice(t);
    }
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    const scroll = this.scrollAt(t);
    const lieW = this.lieWord ?? { start: 1e9, end: 1e9 } as Word;
    const lie = smoothstep(lieW.start - 0.02, lieW.start + 0.1, t) * (1 - 0.6 * smoothstep(lieW.end, lieW.end + 0.5, t));

    this.paper.u.scroll!.value = scroll % (this.speedPx * 4);
    this.paper.u.speedPx!.value = this.speedPx;
    this.paper.u.lie!.value = lie;
    this.paper.render(renderer, out);

    // ---- traces: sample history under the paper (x = pen - (scroll(t) - scroll(t')))
    this.ink.clear(); this.glow.clear();
    const inkC = LIN.ink, sig = LIN.signal;
    const dt = 1 / 240;
    for (let ci = 0; ci < 4; ci++) {
      const y0 = CH[ci]!.y;
      let px = NaN, py = NaN;
      for (let tp = t; tp > t - 4.5; tp -= dt) {
        if (tp < -0.5) break;
        const x = PEN_X - (scroll - this.scrollAt(tp));
        if (x < -20) break;
        const y = y0 + this.chan(ci, tp);
        if (!isNaN(px)) {
          if (ci === 3) {
            this.ink.seg2(px, py, x, y, 2.6, sig, 1);
            this.glow.seg2(px, py, x, y, 1.2, [sig[0] * 0.5, sig[1] * 0.35, sig[2] * 0.25], 0.8 * lie + 0.25);
          }
          else this.ink.seg2(px, py, x, y, 1.6, inkC, 0.85);
        }
        px = x; py = y;
      }
      // pen arm: from the carriage to the nib
      const ny = y0 + this.chan(ci, t);
      this.ink.seg2(PEN_X + 180, y0, PEN_X + 6, ny, 2.2, LIN.graphite, 0.9);
      this.ink.seg2(PEN_X + 180, y0 - 5, PEN_X + 180, y0 + 5, 7, LIN.ink, 1);
    }
    // the spark is the voice pen's nib
    const head = (tt: number) => ({ x: PEN_X, y: CH[3]!.y + this.chan(3, tt) });
    const h = head(t);
    sparkParticles(this.glow, t, (tb) => (tb > t ? null : { x: PEN_X - (scroll - this.scrollAt(tb)), y: head(tb).y }),
      { rate: (tb) => 30 + 260 * (this.held.some((w) => tb > w.start && tb < w.end) ? 1 : audio.hit('vocal', tb, 0.15)), rateMax: 290, speed: 320, seed: 11 });
    sparkHead(this.glow, h.x, h.y, t, 1 + lie * 0.6, 1 + lie);

    this.ink.render(renderer, out);

    // ---- type layer: margin labels, header, lyric printed onto the paper, stamp
    const L = this.text; L.clear(); const c = L.ctx;
    // header strip (on the dark band)
    c.fillStyle = rgba('ash', 0.9); c.font = font(F.mono(500), 17); c.textBaseline = 'alphabetic';
    c.fillText('CHART 01 · EXAMINATION OF SUBJECT', 96, 92);
    c.textAlign = 'right';
    c.fillText(`${audio.bpm.toFixed(0)} BPM · PAPER ${(this.speedPx / this.beat / 100).toFixed(2)} m/s`, W - 96, 92);
    c.fillText(`T+${t.toFixed(2).padStart(5, '0')} s   BEAT ${Math.max(0, Math.floor(f.beat) + 1).toString().padStart(2, '0')}`, W - 96, 120);
    c.textAlign = 'left';
    c.fillStyle = rgba('bone', 0.9); c.font = font(F.archivo(125, 900), 26);
    c.fillText((this.linesIn()[0]?.text ?? 'HELP! I’M STUCK IN A LIE').toUpperCase(), 96, 124);
    // channel labels in the left margin
    for (const [i, ch] of CH.entries()) {
      c.fillStyle = rgba(i === 3 ? 'signal' : 'ink', 0.85); c.font = font(F.mono(600), 15);
      c.fillText(ch.name, 40, ch.y - 6);
      c.fillStyle = rgba('graphite', 0.9); c.font = font(F.mono(400, true), 13);
      c.fillText(ch.sub, 40, ch.y + 13);
    }
    // bottom band: examiner notes
    c.fillStyle = rgba('ash', 0.8); c.font = font(F.mono(400), 15);
    const qs = ['Q1. Is your name what you say it is?   · awaiting response', 'Q2. Are you where you want to be?', 'Q3. Are you telling the truth?', 'Q4. Is this your own voice?', 'Q5. Do you feel anything?'];
    const note = qs[Math.min(qs.length - 1, Math.max(0, Math.floor((t - this.ctx.start) / (4 * this.beat))))]!;
    c.fillText(note, 96, H - 62);

    // lyric: each word is stamped under the pen when sung, then rides the paper away
    for (const w of this.words) {
      if (t < w.start - 0.001) continue;
      const x = PEN_X - (scroll - this.scrollAt(w.start)) + 14;
      if (x > W + 50 || x < -900) continue;
      const k = t - w.start;
      const isLie = this.held.includes(w);
      const help = w.index === 0;
      const size = isLie ? 150 : help ? 120 : 64;
      const fam = isLie ? F.archivo(125, 900) : help ? F.archivo(112, 900) : F.archivo(87, 700);
      const pop = 1 + 0.25 * Math.exp(-k * 18);
      const y = isLie ? 275 : help ? 275 : 790;
      c.save();
      c.translate(x, y); c.scale(pop, pop);
      c.font = font(fam, size);
      c.fillStyle = isLie ? rgba('signal', 1) : rgba('ink', 0.92);
      c.fillText(w.w.toUpperCase(), 0, 0);
      // time-code tick under each word, like an examiner's mark
      c.fillStyle = rgba('graphite', 0.9); c.font = font(F.mono(400), 12);
      c.fillText(`${w.start.toFixed(2)}s`, 2, isLie ? 26 : 22);
      c.restore();
    }

    // stamp: DECEPTION INDICATED lands on the 3rd beat of the held note
    const tStamp = this.lieWord ? audio.timeOfBeat(Math.round(audio.beatAt(lieW.start)) + 3) : 1e9;
    let shake: [number, number] = [0, 0];
    if (t >= tStamp) {
      const k = t - tStamp;
      const s = 1 + 1.4 * Math.exp(-k * 22);
      c.save();
      c.translate(PEN_X - (scroll - this.scrollAt(tStamp)) - 260, 560);
      c.rotate(-0.12); c.scale(s, s);
      c.globalAlpha = clamp(k * 30);
      c.strokeStyle = rgba('signal', 0.95); c.lineWidth = 7;
      c.strokeRect(-330, -78, 660, 156);
      c.lineWidth = 2; c.strokeRect(-316, -64, 632, 128);
      c.fillStyle = rgba('signal', 0.95); c.textAlign = 'center';
      c.font = font(F.archivo(112, 900), 62); c.fillText('DECEPTION', 0, 8);
      c.font = font(F.mono(700), 26); c.fillText('I N D I C A T E D', 0, 46);
      c.restore();
      const sh = Math.exp(-k * 14) * 18;
      shake = [(hash(frameIdx(t), 1) - 0.5) * sh, (hash(frameIdx(t), 2) - 0.5) * sh];
    }
    comp.draw(renderer, L.upload(), out);
    this.glow.render(renderer, out);

    // camera: starts tight on the voice pen, opens on the first downbeat after "Help!", and punches on hits
    const helpW = this.words.find((w) => w.start >= this.ctx.start - 0.1) ?? { start: this.ctx.start + 1 } as Word;
    const z0 = this.ctx.start;
    const zk: [number, number, ((x: number) => number)?][] = [[z0, 2.4], [Math.max(z0 + 0.01, helpW.start - 0.05), 1.9, ease.inOutCubic], [Math.max(z0 + 0.02, helpW.start + 0.25), 1.0, ease.outExpo]];
    if (this.lieWord && lieW.start > helpW.start + 0.3) zk.push([lieW.start, 1.0], [lieW.start + 0.12, 1.08, ease.outExpo]);
    zk.push([Math.max(zk[zk.length - 1]![0] + 0.01, this.ctx.end - 0.9), 1.04], [this.ctx.end, 1.25, ease.inCubic]);
    const zoom = keys(t, zk as any);
    const lieShake = lie * (1 - smoothstep(lieW.end - 0.2, lieW.end + 0.3, t)) * 7;
    shake = [shake[0] + (hash(frameIdx(t), 5) - 0.5) * lieShake, shake[1] + (hash(frameIdx(t), 6) - 0.5) * lieShake];
    // the zoom centre is the frame centre: pan the tight open toward the pen by offsetting with shake
    // post maps uv = (vUv - .5) / zoom + .5 - shake / res (y up): to centre point P, shake = (W/2 - Px, Py - H/2)
    const pan = clamp((zoom - 1.1) / 1.3);
    shake = [shake[0] + (W / 2 - PEN_X) * pan, shake[1] + (CH[3]!.y - H / 2) * pan];
    return {
      paper: 1, bloom: 0.45, grain: 0.05, vignette: 0.3, zoom, shake,
      flash: 0.6 * smoothstep(this.ctx.end - 0.12, this.ctx.end, t),
    };
  }
}
