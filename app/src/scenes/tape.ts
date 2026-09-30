// SHOT — 'tape' (punched paper tape). One idea: a distress call that jams.
// Close on a paper tape running through a punch. The first sung word is punched in Morse, over and
// over (dots are round holes, dashes are slots, on the 16th-note grid), and the orange light of the
// reader shows through every hole; each Morse group has its letter printed above it, and a teleprinter
// stamps the sung words along the bottom edge. On the next line the tape jams: the punch hammers the
// same spot, the incoming tape crumples into pleats, the printer overprints in one place, and on the
// last word the tape tears.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { rgba } from '../engine/palette';
import { F, font } from '../engine/type';
import { clamp, ease, hash, frameIdx } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { wordText } from '../danmaku/kinetic';
import type { Word } from '../engine/lyrics';
import { CLEAN } from './poster';

const MORSE: Record<string, string> = { A: '.-', B: '-...', C: '-.-.', D: '-..', E: '.', F: '..-.', G: '--.', H: '....', I: '..', J: '.---', K: '-.-', L: '.-..', M: '--', N: '-.', O: '---', P: '.--.', Q: '--.-', R: '.-.', S: '...', T: '-', U: '..-', V: '...-', W: '.--', X: '-..-', Y: '-.--', Z: '--..' };
const HEAD_X = 1210, CY = 540, TAPE_H = 440, UNIT = 50;
const T_TOP = CY - TAPE_H / 2, T_BOT = CY + TAPE_H / 2;
const CH_LETTER = T_TOP + 62, CH_MORSE = CY - 58, CH_SPROCKET = CY + 26, CH_WORDS = T_BOT - 70;
const SP = UNIT;                   // sprocket pitch: one feed hole per Morse unit
const PRINT_OFF = 70, PS = 52, CW = PS * 0.6;   // printer sits just left of the punch; mono type
const PLEAT = 76, K0 = 0.36;       // material length of one pleat, and how much the crumple compresses it

interface Punch { t: number; dash: boolean; s: number }

export default class Tape extends Mode {
  bg = new FSPass(/* glsl */ `
    void main() {
      vec2 p = FRAG_PX; p.y = ${H.toFixed(1)} - p.y;
      fragColor = vec4(C_INK * (1.0 + 0.6 * snoise(p * 0.003)), 1.0);
    }`);
  L = new Layer2D();
  unit = 0.04; v = 600;
  punches: Punch[] = [];
  letters: { t: number; ch: string; s: number }[] = [];
  printed: { w: Word; s: number; over: boolean; k: number }[] = [];
  chars: { ch: string; t: number; s: number }[] = [];
  tJam = 1e9; tTear = 1e9; sJam = 0;

  init() {
    const beat = 60 / this.ctx.audio.bpm;
    this.unit = beat / 8;                                // a Morse unit is a 32nd: dots fall on 16ths
    this.v = UNIT / this.unit;
    const lines = this.linesIn();
    const l0 = lines[0], l1 = lines[1];
    const t0 = l0?.words[0]?.start ?? this.cutTime;
    if (l1) { this.tJam = l1.words[0]!.start; this.tTear = l1.words[l1.words.length - 1]!.start; }
    this.sJam = this.travel(this.tJam);
    const key = wordText(l0?.words[0]?.w ?? 'HELP').replace(/[^A-Z]/g, '') || 'HELP';
    // the call repeats until the machine jams
    let u = 0;
    outer: for (let rep = 0; rep < 8; rep++) {
      for (const ch of key) {
        const code = MORSE[ch] ?? '';
        const tl = t0 + u * this.unit;
        if (tl >= this.tJam - 1e-3) break outer;
        this.letters.push({ t: tl, ch, s: this.travel(tl) });
        for (const sym of code) {
          const tp = t0 + u * this.unit;
          if (tp >= this.tJam - 1e-3) break outer;
          this.punches.push({ t: tp, dash: sym === '-', s: this.travel(tp) });
          u += (sym === '-' ? 3 : 1) + 1;
        }
        u += 2;
      }
      u += 4;
    }
    // the teleprinter types each word as it's sung, a character per character-width of tape, never
    // over the previous word; once the tape is stuck it can only stamp words over each other
    const charT = CW / this.v;
    let free = -1e9;
    this.wordsIn().forEach((w, k) => {
      const over = w.start >= this.tJam - 1e-3;
      if (over) { this.printed.push({ w, over, k, s: this.sJam - PRINT_OFF }); return; }
      const txt = wordText(w.w);
      const t0 = Math.max(w.start, free);
      Array.from(txt).forEach((ch, i) => { const tc = t0 + i * charT; this.chars.push({ ch, t: tc, s: this.travel(tc) - PRINT_OFF }); });
      free = t0 + (txt.length + 1) * charT;
    });
  }

  /** Tape past the punch by t: it runs from the cut and stops dead when the jam starts. */
  travel(t: number) { return (Math.min(t, this.tJam) - this.cutTime) * this.v; }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    this.bg.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const beat = 60 / audio.bpm;
    const jam = t >= this.tJam, torn = t >= this.tTear;
    const tr = this.travel(t);
    const xL = (s: number) => HEAD_X - (tr - s);                 // a point of the punched (left) tape
    // after the jam the feed keeps pushing: e px of tape crumple into pleats right of the punch
    const e = jam ? this.v * (Math.min(t, this.tTear) - this.tJam) : 0;
    const k = K0 + (torn ? 0.34 * ease.outBack(clamp((t - this.tTear) / 0.45)) : 0);
    const P = k * e;
    const xR = (s: number) => {                                  // a point of the incoming (right) tape
      const m = s - (jam ? this.sJam : tr);
      return m < e ? HEAD_X + k * m : HEAD_X + P + (m - e);
    };
    // the tear: the punched tape whips away left and drops; the crumple springs open
    const tt = torn ? t - this.tTear : 0;
    const lDx = torn ? -230 * ease.outCubic(clamp(tt / 0.55)) : 0;
    const lDy = torn ? 70 * ease.inQuad(clamp(tt / 1.1)) : 0;
    const lRot = torn ? -0.035 * ease.outCubic(clamp(tt / 0.8)) : 0;
    const rDx = torn ? 26 * ease.outBack(clamp(tt / 0.4)) : 0;
    const jag = (side: number) => Array.from({ length: 12 }, (_, i) => [(hash(i, 5) - 0.5) * 26 + side * 4, T_TOP + (TAPE_H * i) / 11] as const);

    // ---------- the punched tape (left of the punch)
    c.save();
    c.translate(HEAD_X + lDx, CY + lDy); c.rotate(lRot); c.translate(-HEAD_X, -CY);
    const left = new Path2D();
    left.moveTo(-80, T_TOP); left.lineTo(HEAD_X + 1, T_TOP);
    if (torn) for (const [dx, y] of jag(-1)) left.lineTo(HEAD_X + dx, y); else left.lineTo(HEAD_X + 1, T_BOT);
    left.lineTo(HEAD_X + 1, T_BOT); left.lineTo(-80, T_BOT); left.closePath();
    c.fillStyle = rgba('bone', 1); c.fill(left);
    c.save(); c.clip(left);
    this.fibres(c, tr, xL, -80, HEAD_X + 30);
    // sprockets
    c.fillStyle = rgba('signal', 1);
    for (let n = Math.floor((tr - HEAD_X - 100) / SP); n * SP <= tr + 20; n++) { const x = xL(n * SP); this.hole(c, x, CH_SPROCKET, 7, 1); }
    // Morse holes and their letters
    for (const p of this.punches) {
      if (t < p.t) continue;
      const x = xL(p.s);
      if (x < -200) continue;
      if (p.dash) this.slot(c, x - 0.95 * UNIT, x + 0.95 * UNIT, CH_MORSE, 27); else this.hole(c, x, CH_MORSE, 27, 1);
    }
    c.font = font(F.mono(700), 40); c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillStyle = rgba('ink', 1);
    for (const l of this.letters) if (t >= l.t) { const x = xL(l.s); if (x > -60) c.fillText(l.ch, x, CH_LETTER); }
    // the jam: the punch keeps hammering one spot into a ragged wound
    if (jam) this.wound(c, t, beat);
    // the teleprinter: typed character by character; jammed, it stamps words over each other
    c.font = font(F.mono(700), PS); c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillStyle = rgba('ink', 1);
    for (const ch of this.chars) { if (t < ch.t) break; const x = xL(ch.s); if (x > -60) c.fillText(ch.ch, x, CH_WORDS); }
    c.textAlign = 'right';
    for (const pw of this.printed) {
      if (t < pw.w.start) continue;
      const x = xL(pw.s) + (pw.over ? (hash(pw.k, 3) - 0.5) * 16 : 0), y = CH_WORDS + (pw.over ? (hash(pw.k, 4) - 0.5) * 12 : 0);
      if (x < -40) continue;
      c.fillStyle = rgba('ink', 1); c.fillText(wordText(pw.w.w), x, y);
    }
    c.restore();
    c.restore();

    // ---------- the incoming tape (right of the punch): flat, then crumpled once jammed
    c.save(); c.translate(rDx, 0);
    const right = new Path2D();
    if (torn) { const j = jag(1); right.moveTo(HEAD_X + j[0]![0], T_TOP); for (const [dx, y] of j) right.lineTo(HEAD_X + dx, y); }
    else { right.moveTo(HEAD_X, T_TOP); right.lineTo(HEAD_X, T_BOT); }
    right.lineTo(HEAD_X + P, T_BOT); right.lineTo(W + 80, T_BOT); right.lineTo(W + 80, T_TOP); right.lineTo(HEAD_X + P, T_TOP); right.closePath();
    c.fillStyle = rgba('bone', 1); c.fill(right);
    c.save(); c.clip(right);
    const sHead = jam ? this.sJam : tr;
    this.fibres(c, tr, (s) => xR(s), HEAD_X + P, W + 80, sHead + e);
    c.fillStyle = rgba('signal', 1);
    for (let n = Math.ceil((sHead + e) / SP); xR(n * SP) < W + 40; n++) this.hole(c, xR(n * SP), CH_SPROCKET, 7, 1);
    if (jam && torn) this.wound(c, t, beat);
    c.restore();
    // the crumple: accordion pleats, lit and shadowed faces, the edges pushed out
    if (e > 0) {
      const half = PLEAT / 2, n = Math.ceil(e / half);
      for (let m = 0; m < n; m++) {
        const a = m * half, b = Math.min(e, (m + 1) * half);
        const xa = HEAD_X + k * a, xb = HEAD_X + k * b;
        const bump = (i: number) => (i % 2 ? 10 + 22 * hash(i, 11) : 3 + 4 * hash(i, 12));
        c.beginPath();
        c.moveTo(xa, T_TOP - bump(m)); c.lineTo(xb, T_TOP - bump(m + 1)); c.lineTo(xb, T_BOT + bump(m + 1) * 0.8); c.lineTo(xa, T_BOT + bump(m) * 0.8); c.closePath();
        c.fillStyle = m % 2 ? rgba('ash', 1) : rgba('bone', 1); c.fill();
        c.strokeStyle = rgba('graphite', 0.9); c.lineWidth = 1.2; c.stroke();
        // squashed sprocket holes on the crumpled faces
        c.fillStyle = rgba('signal', m % 2 ? 0.75 : 1);
        for (let q = Math.ceil((this.sJam + a) / SP); q * SP < this.sJam + b; q++) {
          const x = HEAD_X + k * (q * SP - this.sJam);
          c.beginPath(); c.ellipse(x, CH_SPROCKET, Math.max(1.5, 7 * k), 7, 0, 0, Math.PI * 2); c.fill();
        }
      }
    }
    c.restore();

    // ---------- pinch rollers riding the tape's edges, turning with it
    for (const [ry, dir] of [[T_TOP - 50, 1], [T_BOT + 50, -1]] as const) {
      const rx = HEAD_X - 330, r = 46, a = (dir * tr) / r;
      c.fillStyle = rgba('ink2', 1); c.strokeStyle = rgba('graphite', 1); c.lineWidth = 2;
      c.beginPath(); c.arc(rx, ry, r, 0, Math.PI * 2); c.fill(); c.stroke();
      c.beginPath(); c.arc(rx, ry, r - 9, 0, Math.PI * 2); c.stroke();
      c.lineWidth = 3;
      for (let k = 0; k < 3; k++) { const q = a + (k * Math.PI * 2) / 3; c.beginPath(); c.moveTo(rx + Math.cos(q) * 10, ry + Math.sin(q) * 10); c.lineTo(rx + Math.cos(q) * (r - 14), ry + Math.sin(q) * (r - 14)); c.stroke(); }
      c.fillStyle = rgba('graphite', 1); c.beginPath(); c.arc(rx, ry, 7, 0, Math.PI * 2); c.fill();
    }
    // ---------- the machine: punch above, die below, the pin dropping through the tape on every hit
    const hits = [...this.punches.map((p) => p.t), ...(jam ? Array.from({ length: 24 }, (_, i) => this.tJam + (i * beat) / 8).filter((x) => x <= this.tTear + 1e-3) : [])];
    const last = hits.filter((x) => x <= t).pop() ?? -9;
    const pin = Math.exp(-(t - last) * 38);
    const bx = HEAD_X - 86;
    c.fillStyle = rgba('ink2', 1); c.strokeStyle = rgba('graphite', 1); c.lineWidth = 2;
    c.fillRect(bx, -10, 172, T_TOP - 14 + 10); c.strokeRect(bx, -10, 172, T_TOP - 14 + 10);
    c.fillRect(bx, T_BOT + 14, 172, H - T_BOT); c.strokeRect(bx, T_BOT + 14, 172, H - T_BOT);
    for (const [sx, sy] of [[bx + 22, 40], [bx + 150, 40], [bx + 22, T_BOT + 44], [bx + 150, T_BOT + 44]] as const) {
      c.beginPath(); c.arc(sx, sy, 7, 0, Math.PI * 2); c.stroke(); c.beginPath(); c.moveTo(sx - 5, sy); c.lineTo(sx + 5, sy); c.stroke();
    }
    const pinY = T_TOP - 14 + (CH_MORSE + 30 - (T_TOP - 14)) * pin;
    c.fillStyle = rgba('graphite', 1); c.fillRect(HEAD_X - 14, T_TOP - 40, 28, pinY - (T_TOP - 40));
    c.fillStyle = rgba('ink', 1); c.fillRect(HEAD_X - 14, pinY - 4, 28, 4);
    c.font = font(F.mono(500), 17); c.fillStyle = rgba('ash', 1); c.textAlign = 'center'; c.textBaseline = 'middle';
    c.fillText('PUNCH', HEAD_X, 96);
    c.fillText(jam ? (torn ? 'TORN' : 'JAMMED') : 'MORSE  1/16', HEAD_X, T_BOT + 96);
    comp.draw(renderer, this.L.upload(), out);

    const sh = 4 * pin + (jam && !torn ? 3 : 0) + (torn ? 16 * Math.exp(-tt * 7) : 0);
    const jz = jam ? 0.05 * ease.outExpo(clamp((t - this.tJam) / 0.12)) : 0;
    return { ...CLEAN, shake: [(hash(frameIdx(t), 1) - 0.5) * sh, (hash(frameIdx(t), 2) - 0.5) * sh], zoom: 1 + 0.03 * clamp((t - this.cutTime) / 3) + jz };
  }

  hole(c: CanvasRenderingContext2D, x: number, y: number, r: number, a: number) {
    c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fillStyle = rgba('signal', a); c.fill();
    c.strokeStyle = rgba('blood', 0.55); c.lineWidth = 2; c.stroke();
  }
  slot(c: CanvasRenderingContext2D, x0: number, x1: number, y: number, r: number) {
    c.beginPath(); c.roundRect(x0, y - r, x1 - x0, 2 * r, r); c.fillStyle = rgba('signal', 1); c.fill();
    c.strokeStyle = rgba('blood', 0.55); c.lineWidth = 2; c.stroke();
  }
  /** Overlapping hits at the punch, piling into a torn hole (drawn in tape coordinates of the jam). */
  wound(c: CanvasRenderingContext2D, t: number, beat: number) {
    const n = Math.floor((Math.min(t, this.tTear) - this.tJam) / (beat / 8)) + 1;
    c.fillStyle = rgba('signal', 1);
    for (let i = 0; i < n; i++) {
      const x = HEAD_X - 4 + (hash(i, 1) - 0.5) * 34, y = CH_MORSE + (hash(i, 2) - 0.5) * 44, r = 22 + 14 * hash(i, 3);
      c.beginPath();
      for (let a = 0; a < 14; a++) { const ang = (a / 14) * Math.PI * 2, rr = r * (0.8 + 0.35 * hash(i, a, 4)); c.lineTo(x + Math.cos(ang) * rr, y + Math.sin(ang) * rr); }
      c.closePath(); c.fill();
    }
  }
  /** Paper fibres riding the tape (material coordinates). */
  fibres(c: CanvasRenderingContext2D, _tr: number, x: (s: number) => number, x0: number, x1: number, sMin = -1e9) {
    c.strokeStyle = rgba('ash', 0.35); c.lineWidth = 1;
    const s0 = Math.floor((_tr - HEAD_X - 200) / 23);
    for (let n = s0; n < s0 + 160; n++) {
      const s = n * 23 + hash(n, 1) * 20;
      if (s < sMin) continue;
      const px = x(s);
      if (px < x0 - 40 || px > x1 + 40) continue;
      const y = T_TOP + 14 + hash(n, 2) * (TAPE_H - 28), len = 10 + 26 * hash(n, 3), ang = (hash(n, 4) - 0.5) * 0.5;
      c.beginPath(); c.moveTo(px, y); c.lineTo(px + Math.cos(ang) * len, y + Math.sin(ang) * len); c.stroke();
    }
  }
}
