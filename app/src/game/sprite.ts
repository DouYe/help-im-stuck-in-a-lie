// The girl: a sprite whose every pixel is a symbol (frames in girl.txt -> girl_frames.ts).
import { GIRL } from './girl_frames';
import { GLYPHS, HOT, GlyphPen } from './glyph';
import { hash } from '../engine/util';

export const SPRITE_W = 10, SPRITE_H = 14;
export interface SpriteOpts {
  flip?: boolean;           // face left
  col?: string;             // stroke colour (the heart stays orange)
  hot?: string;             // heart colour
  lw?: number;              // line width as a fraction of the cell height (default 0.13)
  glitch?: number;          // 0..1: cells swap to code digits / slip sideways
  seed?: number;
  dissolve?: number;        // 0..1: cells fall apart into dots from the bottom
}
/** Width in cells of a frame. */
export const frameW = (name: string) => GIRL[name]?.[0]?.length ?? SPRITE_W;

/**
 * Draw a frame with its top-left at (x, y), cells cw x ch px. Big-heart blocks ('@') draw one heart over
 * their bounding box.
 */
export function drawGirl(pen: GlyphPen, name: string, x: number, y: number, cw: number, ch: number, o: SpriteOpts = {}) {
  const rows = GIRL[name] ?? GIRL.side!;
  const col = o.col ?? '#EEE9DF', hot = o.hot ?? '#FF5314';
  const lw = Math.max(0.6, (o.lw ?? 0.13) * ch);
  const w = rows[0]!.length;
  let big = null as [number, number, number, number] | null;
  rows.forEach((row, r) => {
    const slip = o.glitch && hash(r, o.seed ?? 0, 7) < o.glitch * 0.5 ? Math.round((hash(r, o.seed ?? 0, 8) - 0.5) * 4) : 0;
    for (let c = 0; c < row.length; c++) {
      let chr = row[c]!;
      if (chr === ' ') continue;
      const cc = o.flip ? w - 1 - c : c;
      if (chr === '@') { big = big ? [Math.min(big[0], cc), Math.min(big[1], r), Math.max(big[2], cc), Math.max(big[3], r)] : [cc, r, cc, r]; continue; }
      if (o.glitch && hash(r, c, o.seed ?? 0) < o.glitch * 0.35) chr = hash(r, c, (o.seed ?? 0) + 1) < 0.5 ? '0' : '1';
      if (o.dissolve && (rows.length - r) / rows.length < o.dissolve * 1.2 && hash(r, c, 3) < o.dissolve * 1.4) chr = hash(r, c, 4) < 0.5 ? '.' : ':';
      pen.glyph(chr, x + (cc + slip) * cw, y + r * ch, cw, ch, HOT.has(chr) ? hot : col, lw, !!o.flip);
    }
  });
  if (big) {
    const [c0, r0, c1, r1] = big as [number, number, number, number];
    pen.glyph('*', x + c0 * cw, y + r0 * ch, (c1 - c0 + 1) * cw, (r1 - r0 + 1) * ch, hot, lw * 1.2);
  }
}
void GLYPHS;
