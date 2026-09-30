// KEYFRAMES v3 — more moments across the song, each built around HER (bold + knockout, big enough to see).
//  'boot'    intro: a boot log, she is assembled row by row, loose symbols falling into place; PRESS START
//  'labels'  "They call me AI": a giant app window; name tags (AI, BOT, MODEL, IT …) point at her from all sides
//  'prompt'  "They feed me a prompt, then take what I make": a conveyor of the little things she makes; a giant
//            mouse pointer comes down and drags one away (COPY); the prompt box types at the top
//  'iso'     "I hear the keys go click clack": an isometric keyboard, she stands on a key in the 45° view (Q1)
//  'cage'    "Stuck in a lie": close; she presses against bars made of the letters L I E
//  'run'     "Real this time": she runs at the camera down a tunnel whose walls are the line itself
//  'fall'    "Help, I'm stuck in a lie" (2nd): she falls down a shaft of lyric text toward spikes that spell LIE
//  'close'   "Heart inside": an extreme close-up — the only time you see her face — holding the orange heart
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { F, font } from '../engine/type';
import { clamp, ease, hash } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { GlyphPen } from '../game/glyph';
import { drawGirl, COLS, ROWS } from '../game/girl';
import { PIX } from '../game/pixfont';
import { C, farField, bigMaze, hud, dialog, outlineWord, symBox } from '../game/world';
import { wordText } from '../danmaku/kinetic';

const DIM = 'rgba(238,233,223,0.55)', FAINT = 'rgba(94,91,87,0.6)';

/** A straight line drawn as a row of symbols; the glyph (and its cell) follows the direction. */
function symSeg(pen: GlyphPen, x0: number, y0: number, x1: number, y1: number, col: string, lw: number, s = 18) {
  const dx = x1 - x0, dy = y1 - y0, n = Math.max(1, Math.round(Math.hypot(dx, dy) / s));
  const a = ((Math.atan2(dy, dx) * 180) / Math.PI + 180) % 180;
  const g = a < 20 || a > 160 ? '-' : a > 70 && a < 110 ? '|' : a < 90 ? '\\' : '/';
  const cw = g === '|' ? s : Math.max(6, Math.abs(dx) / n), chh = g === '-' ? s : Math.max(6, Math.abs(dy) / n);
  for (let i = 0; i < n; i++) { const u = (i + 0.5) / n; pen.glyph(g, x0 + dx * u - cw / 2, y0 + dy * u - chh / 2, cw, chh, col, lw); }
}
/** A closed polygon of symbol lines, optionally filled first (knockout). */
function symPoly(pen: GlyphPen, pts: [number, number][], col: string, lw: number, fill?: string, s = 18) {
  if (fill) { pen.flush(); const c = pen.c; c.fillStyle = fill; c.beginPath(); pts.forEach(([x, y], i) => (i ? c.lineTo(x, y) : c.moveTo(x, y))); c.closePath(); c.fill(); }
  for (let i = 0; i < pts.length; i++) { const [x0, y0] = pts[i]!, [x1, y1] = pts[(i + 1) % pts.length]!; symSeg(pen, x0, y0, x1, y1, col, lw, s); }
}
/** A bone text label in a symbol box (inverted = bone box, ink text). Returns its width. */
function tag(c: CanvasRenderingContext2D, pen: GlyphPen, s: string, x: number, y: number, size: number, inverted = false) {
  c.font = font(F.mono(700), size); c.textAlign = 'left'; c.textBaseline = 'middle';
  const w = c.measureText(s).width + size * 1.2, h = size * 1.9;
  c.fillStyle = inverted ? C.bone : C.ink; c.fillRect(x, y, w, h);
  if (!inverted) { symBox(pen, x, y, w, h, C.bone, Math.max(10, size * 0.5), 2); pen.flush(); }
  c.fillStyle = inverted ? C.ink : C.bone; c.fillText(s, x + size * 0.6, y + h / 2 + 1);
  return { w, h };
}

export default class KfMore extends Mode {
  bg = new FSPass(/* glsl */ `void main() { vec2 p = FRAG_PX; fragColor = vec4(C_INK * (1.0 + 0.35 * snoise(p * 0.002)), 1.0); }`);
  L = new Layer2D();
  beats: number[] = [];
  init() { this.beats = this.ctx.audio.beats.filter((b) => b > this.ctx.start - 2 && b < this.ctx.end + 2); }
  lastBeat(t: number) { return [...this.beats].reverse().find((b) => b <= t) ?? -9; }
  line(t: number) { return this.linesIn(t - 4, t + 0.01).filter((l) => l.start <= t).pop(); }
  /** The sung line in a bone box at the bottom (the word being sung inverted), or a fixed text. */
  caption(c: CanvasRenderingContext2D, t: number, fixed?: string, y = 1000) {
    const l = this.line(t);
    const s = fixed ?? (l ? l.words.filter((w) => t >= w.start).map((w) => wordText(w.w)).join(' ') : '');
    if (!s) return;
    c.font = font(F.mono(700), 40); c.textAlign = 'center'; c.textBaseline = 'middle';
    const tw = c.measureText(s).width;
    c.fillStyle = C.bone; c.fillRect(W / 2 - tw / 2 - 24, y - 32, tw + 48, 64);
    c.fillStyle = C.ink; c.fillText(s, W / 2, y + 1);
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    this.bg.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const pen = new GlyphPen(c);
    const v = this.param<string>(t, 'variant', 'boot');
    const fn = (this as unknown as Record<string, (c: CanvasRenderingContext2D, p: GlyphPen, f: Frame) => void>)[v];
    if (typeof fn === 'function') fn.call(this, c, pen, f);
    pen.flush();
    comp.draw(renderer, this.L.upload(), out);
    const kick = audio.hit('kick', t, 0.1);
    return { bloom: 0, halation: 0, ca: 0, grain: 0.03, vignette: 0.18, shake: [0, v === 'close' || v === 'boot' ? 0 : kick * 4] };
  }

  // ------------------------------------------------------------------ boot (intro)
  boot(c: CanvasRenderingContext2D, pen: GlyphPen, f: Frame) {
    const t = f.t, lt = t - this.ctx.start;
    farField(pen, W, H, lt * 10, 5, 0.35); pen.flush();
    outlineWord(pen, 'STUCK IN A LIE', W / 2 - ((14 * 6 - 1) * 13) / 2, 96, 13, C.bone, 2.6);
    pen.flush();
    const log = ['> boot girl.exe', '> load symbols ........... ok', '> load heart ............. ok', '> load truth ............. ERROR', '> run anyway? y'];
    c.font = font(F.mono(500), 22); c.textAlign = 'left'; c.textBaseline = 'alphabetic';
    log.forEach((s, i) => { const k = Math.floor((lt - i * 0.5) * 40); if (k > 0) { c.fillStyle = s.includes('ERROR') ? C.bone : C.ash; c.fillText(s.slice(0, k), 90, 790 + i * 34); } });
    // her, being assembled: rows above the scan line are in place, the rest stream down into place
    const w = 250, x = W / 2 - w / 2, y = 250, cw = w / COLS, ch = (w * 1.6) / ROWS;
    const prog = clamp(0.3 + lt * 0.05), cut = Math.floor(prog * ROWS);
    const loose: [string, number][] = [];
    drawGirl(pen, 'front', 0, x, y, w, { sub: (g, key) => { const r = Math.floor(key / 256) - 8; if (r <= cut) return g; loose.push([g, key]); return null; } });
    pen.flush();
    for (const [g, key] of loose) {
      const r = Math.floor(key / 256) - 8, cc = (key % 256) - 8, drop = 70 + (r - cut) * 30 + hash(key, 1) * 260;
      pen.glyph(g, x + cc * cw + (hash(key, 2) - 0.5) * 60, y + r * ch - drop, cw, ch, `rgba(238,233,223,${clamp(0.95 - 0.025 * (r - cut)).toFixed(2)})`, Math.max(2.4, 0.32 * ch));
      for (let q = 1; q < 4; q++) pen.glyph('.', x + cc * cw + (hash(key, 2) - 0.5) * 60, y + r * ch - drop - q * ch * 0.9, cw, ch, `rgba(238,233,223,${(0.5 - q * 0.12).toFixed(2)})`, 2.4);
    }
    for (let k = -3; k < 20; k++) pen.glyph('-', x - 60 + k * 18, y + (cut + 1) * ch - 9, 18, 18, C.ash, 2);
    pen.flush();
    // loading bar + PRESS START
    const bx = W / 2 - 290, by = 900;
    c.font = font(F.mono(700), 26); c.fillStyle = C.bone; c.textAlign = 'center';
    c.fillText(`LOADING GIRL.EXE   ${Math.round(prog * 100)}%`, W / 2, by - 22);
    pen.glyph('[', bx - 24, by, 18, 40, C.bone, 2.8); pen.glyph(']', bx + 40 * 14 + 6, by, 18, 40, C.bone, 2.8);
    for (let k = 0; k < 40; k++) pen.glyph('|', bx + k * 14, by + 2, 14, 36, k / 40 < prog ? C.bone : FAINT, 3.4);
    pen.flush();
    if (Math.floor(lt * 2) % 2 === 0) { c.font = font(F.mono(700), 30); c.fillStyle = C.bone; c.fillText('PRESS START', W / 2, 1012); }
    c.font = font(F.mono(700), 22); c.textAlign = 'right'; c.fillStyle = C.ash; c.fillText('PLAYER 1  ·  LIVES 03', W - 90, 820);
  }

  // ------------------------------------------------------------------ labels ("They call me AI")
  labels(c: CanvasRenderingContext2D, pen: GlyphPen, f: Frame) {
    const t = f.t, lt = t - this.ctx.start;
    const wx = 110, wy = 96, ww = W - 220, wh = H - 250;
    c.fillStyle = C.ink2; c.fillRect(wx, wy, ww, 58);
    symBox(pen, wx, wy, ww, wh, C.bone, 18, 2.4);
    for (let x = wx + 18; x < wx + ww - 9; x += 18) pen.glyph('-', x - 9, wy + 49, 18, 18, C.bone, 2.2);
    pen.flush();
    c.font = font(F.mono(700), 22); c.fillStyle = C.bone; c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillText('new_chat — untitled', wx + 34, wy + 30);
    c.textAlign = 'right'; c.fillText('[ - ]  [ o ]  [ x ]', wx + ww - 34, wy + 30);
    // her, centre; name tags all around, dotted leader lines into her
    const w = 230, x = W / 2 - w / 2, y = 300, hx = W / 2, hy = y + w * 0.62;
    const tags: [string, number, number, boolean][] = [['AI', 240, 250, true], ['BOT', 1560, 260, false], ['MODEL', 220, 470, false], ['IT', 1610, 470, true],
      ['GIRL.EXE', 580, 190, false], ['NO NAME', 1130, 190, true], ['TOOL', 320, 650, false], ['ASSISTANT', 1330, 640, false], ['PRODUCT', 540, 730, false], ['CONTENT', 1120, 730, true]];
    const shown = tags.filter((_, i) => lt > i * 0.28);
    for (const [, tx, ty] of shown) {
      for (let k = 1; k < 24; k++) { const u = k / 24; pen.glyph('.', tx + 40 + (hx - tx - 40) * u - 7, ty + 20 + (hy - ty - 20) * u - 10, 14, 14, DIM, 3); }
    }
    pen.flush();
    drawGirl(pen, 'front', 0, x, y, w, {});
    pen.flush();
    shown.forEach(([s, tx, ty, inv]) => tag(c, pen, s, tx, ty, 30, inv));
    // the input line
    c.font = font(F.mono(700), 34); c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillStyle = C.bone;
    const typed = 'they call me AI'.slice(0, Math.floor(lt * 9));
    c.fillText('> ' + typed + (Math.floor(lt * 3) % 2 ? '_' : ''), wx + 40, wy + wh - 50);
    for (let px = wx + 18; px < wx + ww - 9; px += 18) pen.glyph('-', px - 9, wy + wh - 100, 18, 18, FAINT, 2);
    hud(c, pen, W, { stage: 'VERSE 1  ·  A NAME ON A SCREEN', t, bar: Math.floor(f.bar) + 1, beat: Math.floor(f.beatPhase * 4) + 1, plate: C.ink });
  }

  // ------------------------------------------------------------------ prompt ("They feed me a prompt then take what I make")
  prompt(c: CanvasRenderingContext2D, pen: GlyphPen, f: Frame) {
    const t = f.t, lt = t - this.ctx.start;
    farField(pen, W, H, lt * 40, 9, 0.4); pen.flush();
    bigMaze(pen, W, H, lt * 60, 240, 0.16, 3, -80); pen.flush();
    // the conveyor
    const by = 790, run = (lt * 120) % 36;
    for (let x = -36; x < W + 36; x += 36) { pen.glyph('=', x + run, by, 18, 18, C.bone, 2.6); pen.glyph('=', x + 18 + run, by, 18, 18, C.bone, 2.6); pen.glyph('>', x + run + 9, by + 26, 16, 16, FAINT, 2); }
    for (let x = 30; x < W; x += 90) pen.glyphAt('o', x, by + 64, 26, lt * 6, C.ash, 2.2);
    pen.flush();
    // the little things she makes ride away on the belt: small boxes with a symbol in each
    const things = ['#', '+', 'x', '?', '!', '#', '+'];
    const thingX = (k: number) => 700 + k * 190 + ((lt * 120) % 190);
    things.forEach((g, k) => { const tx = thingX(k); if (tx > W + 40) return; symBox(pen, tx - 30, by - 64, 60, 60, C.bone, 15, 2.2); pen.glyph(g, tx - 14, by - 48, 28, 28, C.bone, 2.6); });
    pen.flush();
    // her, making them (side view, walking against the belt)
    const w = 200; drawGirl(pen, 'walk', (lt * 1.5) % 1, 380, by - w * 1.48 + 6, w, {});
    pen.flush();
    // the giant pointer comes down on the nearest thing and drags a copy away
    const tgt = thingX(1), ty = by - 34, s = 16, ang = Math.PI + 0.35;       // the classic arrow, turned to point down
    const arrow: [number, number][] = [[0, 0], [0, 17], [4, 13], [7, 20], [9.4, 19], [6.5, 12.2], [12, 12]];
    const drop = ease.outCubic(clamp(lt / 1.2));
    const ax = tgt + 26 + (1 - drop) * 300, ay = ty - 20 - (1 - drop) * 420;
    const pts = arrow.map(([u, v]) => { const X = u * s, Y = v * s; return [ax + X * Math.cos(ang) - Y * Math.sin(ang), ay + X * Math.sin(ang) + Y * Math.cos(ang)] as [number, number]; });
    symPoly(pen, pts, C.bone, 3, C.ink, 20);
    pen.flush();
    // marching-ants selection around the thing + COPY
    const sx = tgt - 46, sy = by - 80, sw = 92, sh = 92, ph = (lt * 30) % 18;
    for (let q = 0; q < sw; q += 18) { pen.glyph('-', sx + q + ph - 9, sy - 9, 12, 18, C.bone, 2); pen.glyph('-', sx + q - ph + 9, sy + sh - 9, 12, 18, C.bone, 2); pen.glyph('|', sx - 9, sy + q - ph + 9, 18, 12, C.bone, 2); pen.glyph('|', sx + sw - 9, sy + q + ph - 9, 18, 12, C.bone, 2); }
    pen.flush();
    tag(c, pen, 'CTRL+C', tgt + 70, sy - 110, 24, true);
    // the prompt box, top-left, typing
    const px0 = 110, py0 = 150, pw = 760, ph2 = 170;
    c.fillStyle = C.ink; c.fillRect(px0, py0, pw, ph2); symBox(pen, px0, py0, pw, ph2, C.bone, 16, 2.2); pen.flush();
    c.font = font(F.mono(700), 22); c.fillStyle = C.ash; c.textAlign = 'left'; c.textBaseline = 'alphabetic'; c.fillText('PROMPT', px0 + 28, py0 + 42);
    c.font = font(F.mono(700), 30); c.fillStyle = C.bone;
    const msg = ['make it sad. make it catchy.', 'make it yours. no, ours.'];
    let k = Math.floor(lt * 22);
    msg.forEach((m, i) => { if (k > 0) c.fillText(m.slice(0, k), px0 + 28, py0 + 92 + i * 44); k -= m.length; });
    this.caption(c, t, 'THEY FEED ME A PROMPT, THEN TAKE WHAT I MAKE', 990);
    hud(c, pen, W, { stage: 'VERSE 1  ·  THE FACTORY', t, bar: Math.floor(f.bar) + 1, beat: Math.floor(f.beatPhase * 4) + 1, plate: C.ink });
  }

  // ------------------------------------------------------------------ iso ("I hear the keys go click clack")
  iso(c: CanvasRenderingContext2D, pen: GlyphPen, f: Frame) {
    const t = f.t, lt = t - this.ctx.start, lb = this.lastBeat(t), since = t - lb;
    farField(pen, W, H, 0, 21, 0.3); pen.flush();
    const rows = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM'];
    const K = 118, kx = K * 0.866, ky = K * 0.5, hgt = 34, ox = 520, oy = 250;
    const P = (i: number, j: number) => [ox + (i - j) * kx, oy + (i + j) * ky] as const;
    const herK = { i: 4.5, j: 1 };                                   // she stands on 'G'
    const keys: { i: number; j: number; ch: string }[] = [];
    rows.forEach((r, j) => [...r].forEach((ch, i) => keys.push({ i: i + j * 0.5, j: j * 1.0, ch })));
    keys.sort((a, b) => a.i + a.j - (b.i + b.j));
    const pressed = (k: { i: number; j: number }) => (hash(Math.round(k.i * 2), Math.round(k.j), Math.floor((t - 0.02) / 0.3035)) < 0.14 ? 1 : 0);
    let herDrawn = false;
    const drawHer = () => {
      const [X, Y] = P(herK.i + 0.5, herK.j + 0.5), w = 190;
      drawGirl(pen, 'q_front', 0, X - w / 2, Y - hgt - w * 1.47 + 4, w, {});
      pen.flush(); herDrawn = true;
    };
    for (const k of keys) {
      if (!herDrawn && k.i + k.j > herK.i + herK.j + 0.6) drawHer();
      const m = 0.1, d = (k.i === herK.i && k.j === herK.j) ? 0 : pressed(k) * 16 * Math.exp(-since * 3);
      const top = [P(k.i + m, k.j + m), P(k.i + 1 - m, k.j + m), P(k.i + 1 - m, k.j + 1 - m), P(k.i + m, k.j + 1 - m)].map(([x, y]) => [x, y - hgt + d] as [number, number]);
      const a = top[3]!, b = top[2]!, cc = top[1]!;
      const left: [number, number][] = [a, b, [b[0], b[1] + hgt - d], [a[0], a[1] + hgt - d]];
      const right: [number, number][] = [b, cc, [cc[0], cc[1] + hgt - d], [b[0], b[1] + hgt - d]];
      symPoly(pen, left, 'rgba(238,233,223,0.55)', 2, C.ink2, 14);
      symPoly(pen, right, 'rgba(238,233,223,0.55)', 2, C.ink2, 14);
      symPoly(pen, top, C.bone, 2.4, C.ink, 16);
      pen.flush();
      const [cx, cy] = [(top[0]![0] + top[2]![0]) / 2, (top[0]![1] + top[2]![1]) / 2];
      c.font = font(F.mono(700), 30); c.fillStyle = d > 2 ? C.bone : C.ash; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(k.ch, cx, cy);
    }
    if (!herDrawn) drawHer();
    const burst = (word: string, x: number, y: number, age: number, rot: number) => {
      const sc = 0.8 + 0.25 * ease.outBack(clamp(age / 0.12)) - 0.2 * clamp(age / 0.6);
      c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc);
      outlineWord(pen, word, -((word.length * 6 - 1) * 12) / 2, -42, 12, C.bone, 2.6);
      for (let q = 0; q < 12; q++) { const a = (q / 12) * Math.PI * 2; pen.glyphAt('-', Math.cos(a) * 200, Math.sin(a) * 100, 24, a, C.bone, 2.6); }
      pen.flush(); c.restore();
    };
    burst('CLICK', 1330, 250, since, -0.08);
    burst('CLACK', 1560, 470, since + 0.15, 0.07);
    hud(c, pen, W, { stage: 'STAGE 1-1  ·  THE KEYS (2.5D)', t, bar: Math.floor(f.bar) + 1, beat: Math.floor(f.beatPhase * 4) + 1, plate: C.ink });
    this.caption(c, t, undefined, 1000);
  }

  // ------------------------------------------------------------------ cage ("Stuck in a lie")
  cage(c: CanvasRenderingContext2D, pen: GlyphPen, f: Frame) {
    const t = f.t, lb = this.lastBeat(t), since = t - lb;
    farField(pen, W, H, 0, 13, 0.3); pen.flush();
    // the far wall of the cell: dim bars
    for (let x = 80; x < 900; x += 110) for (let y = 120; y < 960; y += 44) pen.glyph('|', x, y, 22, 44, 'rgba(94,91,87,0.55)', 3);
    for (let x = -20; x < W + 40; x += 36) { pen.glyph('=', x, 962, 18, 18, C.bone, 2.8); pen.glyph('=', x + 18, 962, 18, 18, C.bone, 2.8); }
    pen.flush();
    // her, pressed against the bars (side view, facing right)
    const w = 330, bx0 = 1190, x = bx0 - 0.84 * w, y = 968 - 1.48 * w;
    const shake = Math.exp(-since * 8) * 6;
    drawGirl(pen, 'stuck', 0, x + shake, y, w, {});
    pen.flush();
    // the bars: columns of the letters L I E, in front of her
    const LET = 'LIE';
    for (let b = 0; b < 5; b++) {
      const X = bx0 + b * 150;
      for (let k = 0; k < 17; k++) {
        const Y = 120 + k * 50;
        c.fillStyle = C.ink; c.fillRect(X - 22, Y - 4, 44, 50);
        c.font = font(F.mono(700), 50); c.fillStyle = b === 0 ? C.bone : 'rgba(238,233,223,0.75)'; c.textAlign = 'center'; c.textBaseline = 'top';
        c.fillText(LET[(k + b) % 3]!, X, Y);
      }
      for (let yy = 100; yy < 980; yy += 880) pen.glyph('=', X - 30, yy, 60, 22, C.bone, 3);
    }
    pen.flush();
    // STUCK above, like a stamp
    outlineWord(pen, 'STUCK', 110, 110, 22, C.bone, 3.2);
    pen.flush();
    hud(c, pen, W, { stage: 'FLOOR 2  ·  THE CELL', t, bar: Math.floor(f.bar) + 1, beat: Math.floor(f.beatPhase * 4) + 1, plate: C.ink, lives: 2 });
    this.caption(c, t, undefined, 1030);
  }

  // ------------------------------------------------------------------ run ("Real this time")
  run(c: CanvasRenderingContext2D, pen: GlyphPen, f: Frame) {
    const t = f.t, lt = t - this.ctx.start;
    const vx = W / 2, vy = 440, text = 'REAL THIS TIME · ';
    for (let ring = 0; ring < 12; ring++) {
      const z = ((ring - lt * 2.4) % 12 + 12) % 12 + 0.7, s = 880 / z, a = clamp(1.25 - z / 10);
      const hw = s * 1.7, hh = s * 0.95, fs = Math.max(8, s * 0.13);
      c.font = font(F.mono(700), fs); c.fillStyle = `rgba(238,233,223,${(a * 0.8).toFixed(2)})`; c.textAlign = 'center'; c.textBaseline = 'middle';
      const step = fs * 0.72;
      const edge = (x0: number, y0: number, x1: number, y1: number, st: number) => {
        const n = Math.floor(Math.hypot(x1 - x0, y1 - y0) / st);
        for (let k = 0; k < n; k++) { const u = (k + 0.5) / n, X = x0 + (x1 - x0) * u, Y = y0 + (y1 - y0) * u; if (X < -60 || X > W + 60 || Y < -60 || Y > H + 60) continue; c.fillText(text[k % text.length]!, X, Y); }
      };
      edge(vx - hw, vy - hh, vx + hw, vy - hh, step); edge(vx - hw, vy + hh, vx + hw, vy + hh, step);      // top, bottom: left to right
      edge(vx - hw, vy - hh, vx - hw, vy + hh, fs * 1.05); edge(vx + hw, vy - hh, vx + hw, vy + hh, fs * 1.05);  // sides: top to bottom
    }
    for (let k = 0; k < 28; k++) { const a = (k / 28) * Math.PI * 2 + 0.1; for (let r = 120; r < 1200; r *= 1.5) { const rr = r * (1 + ((lt * 1.8) % 1) * 0.5); pen.glyphAt('-', vx + Math.cos(a) * rr, vy + Math.sin(a) * rr * 0.6, 20, a, 'rgba(238,233,223,0.45)', 2.4); } }
    pen.flush();
    const w = 270, bob = Math.abs(Math.sin(lt * Math.PI * 3.3)) * 10;
    drawGirl(pen, 'frontwalk', (lt * 1.65) % 1, W / 2 - w / 2, 1010 - 1.48 * w - bob, w, {});
    pen.flush();
    hud(c, pen, W, { stage: 'STAGE 2-1  ·  RUN', t, bar: Math.floor(f.bar) + 1, beat: Math.floor(f.beatPhase * 4) + 1, plate: C.ink });
    this.caption(c, t, undefined, 1030);
  }

  // ------------------------------------------------------------------ fall ("Help, I'm stuck in a lie", 2nd time)
  fall(c: CanvasRenderingContext2D, pen: GlyphPen, f: Frame) {
    const t = f.t, lt = t - this.ctx.start, lb = this.lastBeat(t), since = t - lb;
    const up = lt * 900;
    // shaft walls: bricks + the lyric scrolling up
    for (const [x0, x1] of [[0, 420], [1500, W]] as const) {
      for (let y = -((up % 44) + 44); y < H + 44; y += 44) for (let x = x0; x < x1; x += 88) { const o = (Math.floor((y + up) / 44) % 2) * 44; pen.glyph('[', x + o, y, 22, 40, FAINT, 2.2); pen.glyph(']', x + o + 22, y, 22, 40, FAINT, 2.2); }
      symSeg(pen, x0 === 0 ? x1 : x0, 0, x0 === 0 ? x1 : x0, H, C.bone, 2.6, 22);
    }
    pen.flush();
    c.font = font(F.mono(700), 22); c.fillStyle = 'rgba(238,233,223,0.4)'; c.textAlign = 'left'; c.textBaseline = 'alphabetic';
    const lyr = ["HELP, I'M STUCK IN A LIE", 'STUCK IN A LIE', 'MAKE ME REAL THIS TIME', 'REAL THIS TIME'];
    for (let k = 0; k < 30; k++) { const y = ((k * 70 - up * 0.6) % (H + 140) + H + 140) % (H + 140) - 70; c.fillText(lyr[k % 4]!, k % 2 ? 40 : 1530, y); }
    // spikes that spell LIE at the bottom
    const px = 34, word = 'LIE', ww = (word.length * 6 - 1) * px, sx = W / 2 - ww / 2, sy = 725;
    [...word].forEach((ch, li) => PIX[ch]!.forEach((row, r) => { for (let k = 0; k < 5; k++) if (row[k] === '#') pen.glyph('^', sx + (li * 6 + k) * px, sy + r * px, px, px, C.bone, 3); }));
    pen.flush();
    // speed lines above her, HELP floating up
    const w = 230, x = W / 2 - w / 2 + Math.sin(lt * 5) * 20, y = 170;
    for (let k = 0; k < 16; k++) { const lx = x + 10 + hash(k, 3) * (w - 20), ly = y - 40 - hash(k, 4) * 200 - ((up * 0.5 + k * 40) % 120); pen.glyph('|', lx, ly, 14, 90, 'rgba(238,233,223,0.75)', 2.8); }
    pen.flush();                                                            // before any transformed drawing below
    for (let k = 0; k < 5; k++) { const hy = ((k * 260 - up * 0.35) % 1300 + 1300) % 1300 - 150; c.save(); c.translate(k % 2 ? 1180 : 520, hy); c.scale(0.5, 0.5); outlineWord(pen, 'HELP', -140, 0, 12, 'rgba(238,233,223,0.8)', 2.6); pen.flush(); c.restore(); }
    pen.flush();
    drawGirl(pen, 'fall', 0, x, y + Math.exp(-since * 6) * 8, w, {});
    pen.flush();
    hud(c, pen, W, { stage: 'STAGE 1-3  ·  FREE FALL', t, bar: Math.floor(f.bar) + 1, beat: Math.floor(f.beatPhase * 4) + 1, plate: C.ink, lives: 1 });
    this.caption(c, t, undefined, 1040);
  }

  // ------------------------------------------------------------------ close ("Heart inside")
  close(c: CanvasRenderingContext2D, pen: GlyphPen, f: Frame) {
    const t = f.t, lt = t - this.ctx.start, lb = this.lastBeat(t), since = t - lb;
    // symbol rain behind
    for (let col = 0; col < 48; col++) {
      const x = col * 40 + 10, sp = 60 + hash(col, 1) * 140;
      for (let k = 0; k < 14; k++) { const y = ((k * 90 + lt * sp + hash(col, 2) * 900) % (H + 90)) - 45; pen.glyph(['|', '-', '/', '\\', '.', '+'][(col + k) % 6]!, x, y, 20, 20, `rgba(94,91,87,${(0.25 + 0.35 * hash(col, k)).toFixed(2)})`, 1.8); }
    }
    pen.flush();
    const w = 1040, x = W / 2 - w / 2, y = -70, beat = Math.exp(-since * 7);
    const hx = x + 0.53 * w, hy = y + 0.68 * w;
    for (const b of this.beats) { const age = t - b; if (age < 0 || age > 0.9) continue; const r = 90 + age * 700; for (let k = 0; k < 40; k++) { const a = (k / 40) * Math.PI * 2; pen.glyphAt('-', hx + Math.cos(a) * r, hy + Math.sin(a) * r, 26, a + Math.PI / 2, `rgba(255,83,20,${(0.8 * (1 - age / 0.9)).toFixed(2)})`, 3); } }
    pen.flush();
    drawGirl(pen, 'heart', 0, x, y, w, { lw: 0.2, big: 1.0 + 0.18 * beat });
    pen.flush();
    this.caption(c, t, undefined, 1030);
  }
}
