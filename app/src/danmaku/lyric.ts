// Her lyric, pinned at the bottom of the frame, karaoke-filled
// word by word in the signal colour. Shared by every mode so the words read the same everywhere.
import { F, font, measure } from '../engine/type';
import { rgba } from '../engine/palette';
import { Lyrics, type Line } from '../engine/lyrics';
import { clamp, ease } from '../engine/util';
import { W, H } from '../engine/gl';

export interface LyricStyle { y?: number; size?: number; x?: number; align?: 'center' | 'left'; alpha?: number; hold?: number; lead?: number }

/** The line to show at t: sung now, or the last one within `hold` s after its end, or the next within `lead` s. */
export function lineAt(ly: Lyrics, t: number, hold = 0.9, lead = 0.25): Line | null {
  let best: Line | null = null;
  for (const l of ly.lines) if (t >= l.start - lead && t < l.end + hold) best = l;
  return best;
}

export function drawLyric(c: CanvasRenderingContext2D, ly: Lyrics, t: number, st: LyricStyle = {}) {
  const line = lineAt(ly, t, st.hold ?? 0.9, st.lead ?? 0.25);
  if (!line) return;
  const size = st.size ?? 60, fam = F.archivo(100, 800);
  const y = st.y ?? H - 92;
  const words = line.words.map((w) => w.w);
  const space = measure(' ', fam, size) * 1.1;
  const widths = words.map((w) => measure(w, fam, size));
  const total = widths.reduce((a, b) => a + b, 0) + space * (words.length - 1);
  let x = st.align === 'left' ? st.x ?? 120 : (st.x ?? W / 2) - total / 2;
  const fadeIn = clamp((t - (line.start - (st.lead ?? 0.25))) / 0.18);
  const fadeOut = 1 - clamp((t - (line.end + (st.hold ?? 0.9) - 0.3)) / 0.3);
  const A = (st.alpha ?? 1) * fadeIn * fadeOut;
  if (A <= 0.01) return;
  c.save();
  c.font = font(fam, size);
  c.textBaseline = 'middle';
  c.lineJoin = 'round';
  line.words.forEach((w, i) => {
    const p = Lyrics.wordProgress(w, t);
    const k = t - w.start;
    const pop = k >= 0 ? 1 + 0.16 * Math.exp(-k * 14) : 1;
    const ww = widths[i]!;
    c.save();
    c.translate(x + ww / 2, y);
    c.scale(pop, pop);
    c.globalAlpha = A;
    c.lineWidth = size * 0.14; c.strokeStyle = 'rgba(0,0,0,0.7)';
    c.strokeText(w.w, -ww / 2, 0);
    c.fillStyle = rgba('bone', 0.42);
    c.fillText(w.w, -ww / 2, 0);
    if (p > 0) {
      // karaoke wipe: the sung part in the signal colour
      c.beginPath(); c.rect(-ww / 2 - 4, -size, (ww + 8) * ease.outQuad(p), size * 2); c.clip();
      c.fillStyle = rgba('signal', 1);
      c.fillText(w.w, -ww / 2, 0);
    }
    c.restore();
    x += ww + space;
  });
  c.restore();
}
