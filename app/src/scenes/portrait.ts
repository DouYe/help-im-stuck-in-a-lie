// MODE 'portrait' — HER, made of symbols, on a screen of symbols.
// Cue params (combine freely):
//   assemble  her glyphs are fired in from beyond the edges and spiral into place, landing on 16ths
//   awake     her eyes open on the cue's last sung word
//   storm     bullet barrages (rings and spirals of symbols) tear through her; she glitches on the held note
//   cage      each sung word slams a bar of symbols across her; the last one reads LIE
//   heart     the heart under her hand glows and beats (a small symbol heart)
//   wide      pull back
//   fadeOut   fade to black at the end of the window
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { Layer2D, W, H } from '../engine/gl';
import { LineBatch } from '../engine/lines';
import { LIN, rgba } from '../engine/palette';
import { F, font, measure } from '../engine/type';
import { clamp, ease, hash, smoothstep, frameIdx, lerp, TAU } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { GlyphFigure } from '../danmaku/glyphs';
import { drawHeart } from '../danmaku/heart';
import { drawLyric } from '../danmaku/lyric';
import { BulletField, SymbolGrid, SYM, glyph, mul, kickRing, type Emission } from '../danmaku/symbols';

const FIG_HEIGHT = 1180;

export default class Portrait extends Mode {
  grid = new SymbolGrid();
  lb = new LineBatch(60000, { blend: 'max' });
  fx = new LineBatch(30000, { blend: 'add' });
  L = new Layer2D();
  fig!: GlyphFigure;
  storm = new BulletField();
  ambient = new BulletField();

  init() {
    this.fig = new GlyphFigure(FIG_HEIGHT);
    const au = this.ctx.audio;
    const beats = au.beats;
    // storm: a real barrage. Two emitters flank her and spin out 6-arm spirals every 8th note; a ring of
    // stars bursts from behind her on every beat; a fan of dashes rains on her face on the backbeat.
    const beat = 60 / au.bpm;
    for (const c of this.cues.filter((c) => c.params.storm)) {
      const end = this.cues.find((x) => x.t > c.t)?.t ?? this.ctx.end;
      for (let k = 0, tt = c.t; tt < end; k++, tt = c.t + k * beat / 2) {
        for (const side of [-1, 1]) {
          const ex = W / 2 + side * 640, ey = 330 + 60 * Math.sin(k * 0.7);
          this.storm.add({ t0: tt, x: ex, y: ey, n: 6, a0: side * k * 0.33, spread: TAU, speed: 430, curl: side * 0.25, kind: k % 4 === 0 ? SYM.star : SYM.dash, size: 9, hot: k % 8 === 0, life: 3.2 });
        }
      }
      beats.forEach((bt, i) => {
        if (bt < c.t - 0.05 || bt >= end) return;
        this.storm.add({ t0: bt, x: W / 2, y: 520, n: 36, a0: hash(i, 7) * TAU, spread: TAU, speed: 650, kind: i % 2 ? SYM.star : SYM.plus, size: 10, hot: i % 2 === 0, life: 2.6 });
        if (i % 2 === 1) this.storm.add({ t0: bt, x: W / 2 + 300 * (hash(i, 8) - 0.5), y: -60, n: 15, a0: Math.PI / 2, spread: 1.1, speed: 1000, kind: SYM.dash, size: 12, life: 2 });
      });
    }
    // ambient: slow rings of dots every other bar (the screen keeps breathing)
    beats.forEach((bt, i) => {
      if (bt < this.ctx.start - 6 || bt > this.ctx.end || i % 8) return;
      this.ambient.add({ t0: bt, x: W / 2, y: 470, n: 48, a0: hash(i, 2) * TAU, spread: TAU, speed: 170, kind: SYM.dot, size: 6, life: 6 });
    });
  }

  snap = (t: number) => { const a = this.ctx.audio; return a.timeOfBeat(Math.round(a.beatAt(t) * 4) / 4); };

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, comp, audio, lyrics } = this.ctx;
    const t = f.t;
    const { cue, since, next } = this.cue(t);
    const P = cue.params;
    const cueEnd = next ? next.t : this.ctx.end;
    const words = (t0: number, t1: number) => lyrics.words.filter((w) => w.start >= t0 - 0.05 && w.start < t1);

    // ---- placement
    const wideK = P.wide ? ease.inOutCubic(clamp(since / 1.2)) : 0;
    const sc = lerp(1, 0.8, wideK) * (1 + 0.012 * Math.sin(t * 1.3));
    const fx = W / 2 - (this.fig.width * sc) / 2, fy = lerp(8, 110, wideK) + 6 * Math.sin(t * 0.9);

    const assembleCue = this.cues.find((c) => c.params.assemble);
    const assemble = assembleCue ? { start: assembleCue.t - 0.1, end: (this.cues.find((c) => c.t > assembleCue.t)?.t ?? assembleCue.t + 3) + 0.2, snap: this.snap, fly: 0.9 } : undefined;

    let awake = 0;
    const awakeCue = this.cues.find((c) => c.params.awake);
    if (awakeCue && t >= awakeCue.t) {
      const ws = words(awakeCue.t, this.cues.find((c) => c.t > awakeCue.t)?.t ?? this.ctx.end);
      const last = ws[ws.length - 1];
      if (last) awake = smoothstep(last.start - 0.05, last.start + 0.15, t);
    }

    const stormOn = !!P.storm;
    const bullets = stormOn ? [...this.storm.live(t)] : [];
    let glitch = 0;
    if (stormOn) {
      const ws = words(cue.t, cueEnd);
      const held = ws[ws.length - 1];
      if (held) glitch = 0.12 + 0.45 * smoothstep(held.start, held.start + 0.2, t) * (1 - smoothstep(held.end, held.end + 0.4, t));
    }

    // ---- cage: a bar of symbols slams across her on each sung word; the last reads LIE
    const bars: { y: number; t0: number; hot: boolean }[] = [];
    const cageCue = this.cues.find((c) => c.params.cage);
    if (cageCue && t >= cageCue.t - 0.1) {
      const ws = words(cageCue.t, this.cues.find((c) => c.t > cageCue.t)?.t ?? this.ctx.end);
      const ys = [250, 610, 420, 800];
      ws.forEach((w, i) => bars.push({ y: fy + ys[i % ys.length]! * sc, t0: this.snap(w.start), hot: i === ws.length - 1 }));
    }
    const barOn = (b: (typeof bars)[number]) => t >= b.t0 - 0.12;
    const push = bars.length ? (_sx: number, sy: number) => {
      for (const b of bars) {
        if (!barOn(b)) continue;
        const d = Math.abs(sy - b.y);
        if (d < 26) return [0, 0, 0] as [number, number, number];
        if (d < 70) return [0, (sy < b.y ? -1 : 1) * (70 - d) * 0.35 * Math.exp(-(t - b.t0) * 3), 1] as [number, number, number];
      }
      return null;
    } : undefined;

    const heartCue = this.cues.find((c) => c.params.heart);
    const heartK = heartCue ? smoothstep(heartCue.t - 0.5, heartCue.t + 0.8, t) : 0;
    const pulse = audio.hit('kick', t, 0.13);

    // ================= draw
    const ring = kickRing(audio.onsets['kick'], t);
    this.grid.render(renderer, out, t, { level: 0.9 - 0.3 * heartK, ringR: ring.r, ringK: ring.k * 0.8, pulse: heartK, cx: W / 2, cy: fy + 470 * sc });

    this.fx.clear();
    this.ambient.draw(this.fx, t, { alpha: 0.35, color: mul(LIN.ash, 0.9) });
    if (stormOn) this.storm.draw(this.fx, t, { alpha: 1 });

    this.lb.clear();
    this.fig.draw(this.lb, t, { x: fx, y: fy, scale: sc, assemble, storm: bullets, awake, glitch, push, heart: heartK, pulse });
    // cage bars: rows of heavy symbols
    for (const b of bars) {
      if (!barOn(b)) continue;
      const k = t - b.t0;
      const slam = ease.outExpo(clamp((k + 0.12) / 0.2));
      const x0 = lerp(W + 100, -40, slam);
      const col = b.hot ? mul(LIN.signal, 2.2) : mul(LIN.bone, 1.3);
      const off = (t * 90) % 36;
      for (let x = x0 - off; x < W + 40; x += 18) {
        const i = Math.round((x - x0 + off) / 18);
        glyph(this.lb, i % 4 === 3 ? SYM.plus : SYM.dash, x, b.y - 9, 8, 0, col, 1, 3);
        glyph(this.lb, i % 2 ? SYM.slash : SYM.back, x + 9, b.y + 9, 8, 0, mul(col, 0.8), 1, 2.6);
      }
    }
    if (heartK > 0) {
      const s = FIG_HEIGHT / 1100;
      drawHeart(this.lb, { cx: fx + 600 * s * sc, cy: fy + 830 * s * sc, R: 95 * sc, rings: 6, t, build: heartK, pulse, size: 5, alpha: heartK });
    }
    this.fx.render(renderer, out);
    this.lb.render(renderer, out);

    // text: LIE on the last bar, and her line
    const c = this.L.ctx; this.L.clear();
    for (const b of bars) {
      if (!barOn(b) || !b.hot) continue;
      const k = t - b.t0;
      const slam = ease.outExpo(clamp((k + 0.12) / 0.2));
      const fam = F.archivo(125, 900), size = 64;
      c.font = font(fam, size); c.textBaseline = 'middle';
      const wd = measure('LIE', fam, size) + 90;
      for (let x = lerp(W + 100, 60, slam); x < W; x += wd * 2.2) {
        c.fillStyle = rgba('ink', 0.9); c.fillRect(x - 20, b.y - 38, wd - 50, 76);
        c.fillStyle = rgba('signal', 1); c.fillText('LIE', x, b.y + 3);
      }
    }
    drawLyric(c, lyrics, t, { y: H - 70, size: 58 });
    comp.draw(renderer, this.L.upload(), out);

    const hit = stormOn ? audio.hit('snare', t, 0.1) + audio.hit('kick', t, 0.1) : 0;
    const sh = 6 * hit + 14 * glitch * (hash(frameIdx(t), 1) - 0.5);
    const barHit = bars.reduce((m, b) => (t >= b.t0 ? Math.max(m, Math.exp(-(t - b.t0) * 10)) : m), 0);
    return {
      fade: P.fadeOut ? smoothstep(this.ctx.end - 0.45, this.ctx.end - 0.02, t) : 0,
      bloom: 0.55 + 0.4 * heartK, grain: 0.05, vignette: 0.45, ca: 1.2 + 3 * glitch,
      zoom: 1 + 0.025 * awake + 0.03 * barHit - 0.02 * wideK,
      shake: [sh + (hash(frameIdx(t), 2) - 0.5) * 16 * barHit, (hash(frameIdx(t), 3) - 0.5) * (sh + 10 * barHit)],
    };
  }
}
