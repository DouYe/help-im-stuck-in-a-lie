// Debug page for designing HER: left = line art + tone, right = the glyph grid as drawn in the video.
import { drawFigure, buildGlyphGrid, FIG_W, FIG_H } from './danmaku/figure';
import { loadFonts } from './engine/type';
const params = new URLSearchParams(location.search);
const H = +(params.get('h') ?? 1000), cw = +(params.get('cw') ?? 9), ch = +(params.get('ch') ?? 16);
(async () => {
  await loadFonts();
  const cv = document.getElementById('c') as HTMLCanvasElement;
  cv.width = 1920; cv.height = 1080;
  const c = cv.getContext('2d')!;
  c.fillStyle = '#06070a'; c.fillRect(0, 0, 1920, 1080);
  // left: raw layers
  c.save(); const s = 1040 / FIG_H; c.translate(20, 20); c.scale(s, s);
  c.globalAlpha = 1; drawFigure(c, 'fill'); drawFigure(c, 'line'); c.restore();
  // right: glyphs
  const g = buildGlyphGrid(H * 1040 / 1100 / (H / 1000) * (H / 1000), cw, ch);
  const k = 1040 / g.height;
  c.save(); c.translate(960, 20); c.scale(k, k);
  c.strokeStyle = '#eef1f7'; c.lineCap = 'round'; c.lineWidth = 2.3;
  for (const q of g.glyphs) {
    const x = q.x, y = q.y, w = g.cellW, h = g.cellH;
    c.globalAlpha = q.ink; c.strokeStyle = q.region === 'feature' ? '#ffffff' : q.region === 'hair' ? '#b8bfcc' : q.region === 'heart' ? '#ff3d6e' : '#9aa3b3';
    c.beginPath();
    if (q.kind === 0) { c.moveTo(x - w * .4, y); c.lineTo(x + w * .4, y); }
    else if (q.kind === 2) { c.moveTo(x, y - h * .34); c.lineTo(x, y + h * .34); }
    else if (q.kind === 1) { c.moveTo(x - w * .34, y + h * .32); c.lineTo(x + w * .34, y - h * .32); }
    else if (q.kind === 3) { c.moveTo(x - w * .34, y - h * .32); c.lineTo(x + w * .34, y + h * .32); }
    else if (q.kind === 5) { c.moveTo(x - w * .3, y); c.lineTo(x + w * .3, y); c.moveTo(x, y - h * .22); c.lineTo(x, y + h * .22); }
    else { c.arc(x, y, 1.6, 0, 7); }
    c.stroke();
  }
  c.restore();
  (window as any).__done = g.glyphs.length;
})();
