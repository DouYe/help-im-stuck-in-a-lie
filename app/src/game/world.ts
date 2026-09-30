// Shared pieces of the game world: the HUD, the RPG dialog box that types the sung line, big words built
// from the pixel font (as bricks or as outlined blocks), the far field of faint symbols and the giant maze
// that stands behind every level. Everything is symbols; the only orange is a heart.
import { GlyphPen } from './glyph';
import { drawGirl } from './girl';
import { PIX } from './pixfont';
import { F, font } from '../engine/type';
import { hash } from '../engine/util';
import { wordText } from '../danmaku/kinetic';
import type { Line } from '../engine/lyrics';

export const C = { ink: '#0A0A0B', ink2: '#161618', graphite: '#5E5B57', ash: '#9C978F', bone: '#EEE9DF', sig: '#FF5314' };
export const HEART = ['/\\/\\', '\\  /', ' \\/ '];

/** A symbol heart ( /\/\ over \/ ) centred at (x, y), `s` px per small cell. */
export function symHeart(pen: GlyphPen, x: number, y: number, s: number, col = C.sig, lw = Math.max(1, s * 0.22)) {
  const hw = s, hh = s * 1.25;
  HEART.forEach((row, r) => { for (let c = 0; c < row.length; c++) if (row[c] !== ' ') pen.glyph(row[c]!, x - 2 * hw + c * hw, y - 1.5 * hh + r * hh, hw, hh, col, lw); });
}

/** Faint far field of dots and dashes; `par` is the parallax offset in px. */
export function farField(pen: GlyphPen, W: number, H: number, par: number, seed = 1, alpha = 0.5, step = 36) {
  const cols = Math.ceil(W / step) + 2, rows = Math.ceil(H / step) + 1, base = Math.floor(par / step);
  for (let gy = 0; gy < rows; gy++) for (let gx = -1; gx < cols; gx++) {
    const wx = gx + base, h = hash(wx, gy, seed);
    if (h > 0.3) continue;
    pen.glyph(h < 0.2 ? '.' : '-', wx * step - par + step / 4, gy * step + step / 4, step / 2, step / 2, `rgba(94,91,87,${alpha})`, 1.3);
  }
}

/** The giant maze behind the level: corridors of stacked bars, `par` px of parallax. */
export function bigMaze(pen: GlyphPen, W: number, H: number, par: number, cell = 216, alpha = 0.28, seed = 21, y0 = -40) {
  const base = Math.floor(par / cell);
  for (let my = 0; my < Math.ceil(H / cell) + 1; my++) for (let mx = -1; mx < Math.ceil(W / cell) + 1; mx++) {
    const wx = mx + base, x = wx * cell - par, y = my * cell + y0, a = `rgba(94,91,87,${alpha})`, n = Math.round(cell / 18);
    if (hash(wx, my, seed) < 0.5) for (let k = 0; k < n; k++) pen.glyph('-', x + k * 18, y, 18, 18, a, 3);
    else for (let k = 0; k < n; k++) pen.glyph('|', x, y + k * 18, 18, 18, a, 3);
  }
}

/** A box outlined with symbols: - along the top/bottom, | down the sides, + at the corners. */
export function symBox(pen: GlyphPen, x: number, y: number, w: number, h: number, col = C.bone, s = 18, lw = 2.2) {
  for (let px = x + s / 2; px < x + w - s / 2; px += s) { pen.glyph('-', px, y - s / 2, s, s, col, lw); pen.glyph('-', px, y + h - s / 2, s, s, col, lw); }
  for (let py = y + s / 2; py < y + h - s / 2; py += s) { pen.glyph('|', x - s / 2, py, s, s, col, lw); pen.glyph('|', x + w - s / 2, py, s, s, col, lw); }
  for (const [px, py] of [[x, y], [x + w, y], [x, y + h], [x + w, y + h]] as const) pen.glyph('+', px - s / 2, py - s / 2, s, s, col, lw * 1.1);
}

/** Top HUD: lives as symbol hearts, stage name, time, bar/beat. */
export function hud(c: CanvasRenderingContext2D, pen: GlyphPen, W: number, o: { stage: string; t: number; bar: number; beat: number; lives?: number; col?: string; dim?: string; plate?: string }) {
  const col = o.col ?? C.bone, dim = o.dim ?? C.ash;
  if (o.plate) {                       // dark plates behind the readouts, for busy frames
    c.font = font(F.mono(700), 22);
    const sw = c.measureText(o.stage).width;
    c.fillStyle = o.plate;
    c.fillRect(56, 26, 90 + (o.lives ?? 3) * 52, 58); c.fillRect(W / 2 - sw / 2 - 18, 36, sw + 36, 44); c.fillRect(W - 290, 30, 250, 74);
  }
  for (let k = 0; k < (o.lives ?? 3); k++) symHeart(pen, 80 + k * 52, 56, 9);
  pen.flush();
  c.textBaseline = 'alphabetic';
  c.font = font(F.mono(700), 22); c.fillStyle = col; c.textAlign = 'left';
  c.fillText(`x ${String(o.lives ?? 3).padStart(2, '0')}`, 80 + (o.lives ?? 3) * 52, 66);
  c.textAlign = 'center'; c.fillText(o.stage, W / 2, 66);
  c.textAlign = 'right'; c.fillText(`TIME ${o.t.toFixed(2).padStart(6, '0')}`, W - 60, 66);
  c.font = font(F.mono(500), 15); c.fillStyle = dim;
  c.fillText(`BAR ${o.bar}  ·  BEAT ${o.beat}`, W - 60, 90);
}

/** RPG dialog box that types the current line as it's sung; the word being sung is inverted. */
export function dialog(c: CanvasRenderingContext2D, pen: GlyphPen, line: Line | undefined, t: number, box: { x: number; y: number; w: number; h: number }, o: { face?: boolean; col?: string; bg?: string } = {}) {
  const col = o.col ?? C.bone, bg = o.bg ?? C.ink;
  c.fillStyle = bg; c.fillRect(box.x, box.y, box.w, box.h);
  symBox(pen, box.x, box.y, box.w, box.h, col);
  if (o.face !== false) drawGirl(pen, 'front', 0, box.x + 22, box.y + 14, 64, { col, knock: bg, minPx: 1.8 });
  pen.flush();
  if (!line) return;
  c.font = font(F.mono(700), 44); c.textAlign = 'left'; c.textBaseline = 'middle';
  let x = box.x + (o.face !== false ? 130 : 40);
  const cy = box.y + box.h / 2 + 2;
  for (const w of line.words) {
    if (t < w.start) break;
    const s = wordText(w.w), ww = c.measureText(s + ' ').width;
    if (t < w.end + 0.05) { c.fillStyle = col; c.fillRect(x - 8, cy - 30, c.measureText(s).width + 16, 60); c.fillStyle = bg; } else c.fillStyle = col;
    c.fillText(s, x, cy);
    x += ww;
  }
  if (Math.floor(t * 3) % 2) { pen.glyph('v', box.x + box.w - 60, box.y + box.h - 50, 24, 24, col, 2.6); pen.flush(); }
}

/** A word in the 5x7 pixel font, every pixel a pair of brackets [ ] (a brick). Returns its size. */
export function brickWord(pen: GlyphPen, word: string, x: number, y: number, px: number, col: string, lw = 2.4, gap = 1) {
  let cx = x;
  for (const ch of word.toUpperCase()) {
    const g = PIX[ch] ?? PIX[' ']!;
    g.forEach((row, r) => { for (let k = 0; k < row.length; k++) if (row[k] === '#') { pen.glyph('[', cx + k * px, y + r * px + 1, px / 2, px - 2, col, lw); pen.glyph(']', cx + k * px + px / 2, y + r * px + 1, px / 2, px - 2, col, lw); } });
    cx += ((ch === ' ' ? 3 : 5) + gap) * px;
  }
  return { w: cx - x - gap * px, h: 7 * px };
}

/** A word in the 5x7 pixel font drawn as outlines only: each pixel's exposed edges are symbols. */
export function outlineWord(pen: GlyphPen, word: string, x: number, y: number, px: number, col: string, lw = 2.4, gap = 1) {
  let cx = x;
  for (const ch of word.toUpperCase()) {
    const g = PIX[ch] ?? PIX[' ']!;
    const on = (r: number, k: number) => r >= 0 && r < 7 && k >= 0 && k < 5 && g[r]![k] === '#';
    for (let r = 0; r < 7; r++) for (let k = 0; k < 5; k++) {
      if (!on(r, k)) continue;
      const X = cx + k * px, Y = y + r * px;
      if (!on(r - 1, k)) pen.glyph('`', X, Y, px, px, col, lw);
      if (!on(r + 1, k)) pen.glyph('_', X, Y, px, px, col, lw);
      if (!on(r, k - 1)) pen.glyph('|', X - px / 2, Y, px, px, col, lw);
      if (!on(r, k + 1)) pen.glyph('|', X + px / 2, Y, px, px, col, lw);
    }
    cx += ((ch === ' ' ? 3 : 5) + gap) * px;
  }
  return { w: cx - x - gap * px, h: 7 * px };
}
