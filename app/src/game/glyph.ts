// The symbol alphabet the whole game world is drawn with: each glyph is a few strokes in a unit cell
// (x right, y down). A GlyphPen batches strokes per colour so a frame full of symbols costs a handful of
// Canvas2D stroke calls. Mirrors the sheet generator (analysis sprite/glyphs.py).
type P = [number, number];
const ring = (cx: number, cy: number, r: number, n = 12): P[] => Array.from({ length: n + 1 }, (_, i) => [cx + r * Math.cos((i / n) * Math.PI * 2), cy + r * Math.sin((i / n) * Math.PI * 2)]);
const heartPts = (n = 18): P[] => Array.from({ length: n + 1 }, (_, i) => {
  const th = (i / n) * Math.PI * 2, st = Math.sin(th);
  const u = (16 * st * st * st) / 17, v = -(13 * Math.cos(th) - 5 * Math.cos(2 * th) - 2 * Math.cos(3 * th) - Math.cos(4 * th)) / 17;
  return [0.5 + u * 0.42, 0.52 + v * 0.42];
});
export const GLYPHS: Record<string, P[][]> = {
  '|': [[[0.5, 0.08], [0.5, 0.92]]],
  '-': [[[0.14, 0.5], [0.86, 0.5]]],
  '=': [[[0.14, 0.34], [0.86, 0.34]], [[0.14, 0.66], [0.86, 0.66]]],
  '/': [[[0.18, 0.92], [0.82, 0.08]]],
  '\\': [[[0.18, 0.08], [0.82, 0.92]]],
  '_': [[[0.06, 0.92], [0.94, 0.92]]],
  '`': [[[0.06, 0.08], [0.94, 0.08]]],
  '.': [[[0.5, 0.78], [0.5, 0.79]]],
  ':': [[[0.5, 0.3], [0.5, 0.31]], [[0.5, 0.72], [0.5, 0.73]]],
  "'": [[[0.5, 0.08], [0.5, 0.42]]],
  ',': [[[0.5, 0.58], [0.5, 0.92]]],
  '+': [[[0.18, 0.5], [0.82, 0.5]], [[0.5, 0.18], [0.5, 0.82]]],
  'x': [[[0.2, 0.2], [0.8, 0.8]], [[0.2, 0.8], [0.8, 0.2]]],
  '^': [[[0.12, 0.88], [0.5, 0.16], [0.88, 0.88]]],
  'v': [[[0.12, 0.12], [0.5, 0.84], [0.88, 0.12]]],
  '<': [[[0.8, 0.14], [0.2, 0.5], [0.8, 0.86]]],
  '>': [[[0.2, 0.14], [0.8, 0.5], [0.2, 0.86]]],
  '[': [[[0.72, 0.08], [0.3, 0.08], [0.3, 0.92], [0.72, 0.92]]],
  ']': [[[0.28, 0.08], [0.7, 0.08], [0.7, 0.92], [0.28, 0.92]]],
  '(': [[[0.68, 0.08], [0.36, 0.3], [0.3, 0.5], [0.36, 0.7], [0.68, 0.92]]],
  ')': [[[0.32, 0.08], [0.64, 0.3], [0.7, 0.5], [0.64, 0.7], [0.32, 0.92]]],
  '#': [[[0.36, 0.1], [0.36, 0.9]], [[0.64, 0.1], [0.64, 0.9]], [[0.12, 0.36], [0.88, 0.36]], [[0.12, 0.64], [0.88, 0.64]]],
  'o': [ring(0.5, 0.5, 0.3)],
  '0': [[[0.3, 0.15], [0.7, 0.15], [0.7, 0.85], [0.3, 0.85], [0.3, 0.15]]],
  '1': [[[0.36, 0.25], [0.54, 0.12], [0.54, 0.88]]],
  '!': [[[0.5, 0.08], [0.5, 0.62]], [[0.5, 0.86], [0.5, 0.87]]],
  '?': [[[0.24, 0.3], [0.3, 0.14], [0.5, 0.08], [0.7, 0.14], [0.76, 0.3], [0.5, 0.5], [0.5, 0.64]], [[0.5, 0.86], [0.5, 0.87]]],
  'L': [[[0.2, 0.08], [0.2, 0.92], [0.9, 0.92]]],
  'J': [[[0.8, 0.08], [0.8, 0.92], [0.1, 0.92]]],
  'r': [[[0.9, 0.08], [0.2, 0.08], [0.2, 0.92]]],
  '7': [[[0.1, 0.08], [0.8, 0.08], [0.8, 0.92]]],
  'H': [[[0.22, 0.02], [0.22, 0.98]], [[0.78, 0.02], [0.78, 0.98]], [[0.22, 0.5], [0.78, 0.5]]],
  '*': [heartPts()],
};
/** Glyphs drawn in the signal colour wherever they appear. */
export const HOT = new Set(['*']);
export const MIRROR: Record<string, string> = { '/': '\\', '\\': '/', '(': ')', ')': '(', '<': '>', '>': '<', '[': ']', ']': '[', L: 'J', J: 'L', r: '7', '7': 'r' };

/** Batches glyph strokes by colour; call flush() to draw. Widths are in px. */
export class GlyphPen {
  private paths = new Map<string, { p: Path2D; w: number }>();
  constructor(public c: CanvasRenderingContext2D) {}
  private path(col: string, w: number) {
    const k = col + '|' + w.toFixed(2);
    let e = this.paths.get(k);
    if (!e) { e = { p: new Path2D(), w }; this.paths.set(k, e); }
    return e.p;
  }
  /** One glyph in the cell (x, y, w, h). */
  glyph(ch: string, x: number, y: number, w: number, h: number, col: string, lw: number, flip = false) {
    const g = GLYPHS[flip ? (MIRROR[ch] ?? ch) : ch];
    if (!g) return;
    const p = this.path(col, lw);
    for (const poly of g) {
      for (let i = 0; i < poly.length; i++) {
        const [u, v] = poly[i]!;
        const px = x + (flip ? 1 - u : u) * w, py = y + v * h;
        if (i === 0) p.moveTo(px, py); else p.lineTo(px, py);
      }
    }
  }
  /** A glyph at centre (cx, cy), size s, rotated by a (for flying symbols). */
  glyphAt(ch: string, cx: number, cy: number, s: number, a: number, col: string, lw: number) {
    const g = GLYPHS[ch];
    if (!g) return;
    const p = this.path(col, lw), ca = Math.cos(a), sa = Math.sin(a);
    for (const poly of g) poly.forEach(([u, v], i) => {
      const dx = (u - 0.5) * s, dy = (v - 0.5) * s;
      const px = cx + dx * ca - dy * sa, py = cy + dx * sa + dy * ca;
      if (i === 0) p.moveTo(px, py); else p.lineTo(px, py);
    });
  }
  line(x0: number, y0: number, x1: number, y1: number, col: string, lw: number) { const p = this.path(col, lw); p.moveTo(x0, y0); p.lineTo(x1, y1); }
  flush() {
    const c = this.c;
    c.lineCap = 'round'; c.lineJoin = 'round';
    for (const [k, e] of this.paths) { c.strokeStyle = k.split('|')[0]!; c.lineWidth = e.w; c.stroke(e.p); }
    this.paths.clear();
  }
}
