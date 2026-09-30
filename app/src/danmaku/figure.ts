// HER: the heroine, an original figure drawn once as line art (bezier paths) and then converted into a
// grid of danmaku glyphs — the — | / \ · + marks of a text screen. She is never drawn as a picture:
// on screen she only exists as glyphs that arrive like bullet comments.
//
// Figure space: 1000 x 1100, y down. A bust: long straight hair (the left side falls in front of the
// shoulder), closed eyes, lips parted as if singing, her right hand laid over her heart.
export const FIG_W = 1000, FIG_H = 1100;

type Pt = [number, number];
type Cubic = [Pt, Pt, Pt, Pt];

export type Region = 'hair' | 'face' | 'feature' | 'body' | 'dress' | 'hand' | 'heart';
export const REGION_ID: Record<Region, number> = { hair: 1, face: 2, feature: 3, body: 4, dress: 5, hand: 6, heart: 7 };

interface Stroke { d: string; w: number; region: Region; head?: boolean }
interface Fill { d: string; tone: number; region: Region; head?: boolean }

// ---- head (tilted a little; the tilt is applied around the neck)
const HEAD_TILT = -0.07, NECK: Pt = [500, 470];
const STROKES: Stroke[] = [
  // jaw and cheeks (open at the temples: the hair covers them)
  { d: 'M 398 300 C 396 352 406 404 436 437 C 456 458 478 470 500 471 C 522 470 544 458 564 437 C 594 404 604 352 602 300', w: 7, region: 'face', head: true },
  // closed eyes: lids curving down, three lashes each
  { d: 'M 412 332 Q 446 356 484 335', w: 9, region: 'feature', head: true },
  { d: 'M 516 335 Q 554 356 588 332', w: 9, region: 'feature', head: true },
  // brows
  { d: 'M 410 300 Q 444 285 482 297', w: 7, region: 'feature', head: true },
  { d: 'M 518 297 Q 556 285 590 300', w: 7, region: 'feature', head: true },
  // nose
  { d: 'M 503 330 C 506 356 510 378 499 393', w: 5, region: 'feature', head: true },
  { d: 'M 486 399 Q 497 406 511 399', w: 5, region: 'feature', head: true },
  // lips, parted (singing)
  { d: 'M 470 424 Q 486 417 500 421 Q 514 417 530 424', w: 7, region: 'feature', head: true },
  { d: 'M 476 432 Q 500 448 524 432', w: 7, region: 'feature', head: true },
  // neck
  { d: 'M 462 452 C 462 490 458 520 452 548', w: 6, region: 'body' },
  { d: 'M 540 452 C 540 490 544 520 550 548', w: 6, region: 'body' },
  // shoulders and arms
  { d: 'M 452 548 C 420 562 360 570 300 590 C 250 606 222 640 214 700 C 206 770 200 860 196 1100', w: 7, region: 'body' },
  { d: 'M 550 548 C 584 562 646 572 704 592 C 754 608 780 644 788 704 C 796 780 802 880 806 1100', w: 7, region: 'body' },
  // collarbones
  { d: 'M 472 594 C 442 585 402 581 362 587', w: 5, region: 'body' },
  { d: 'M 528 594 C 558 585 598 581 638 587', w: 5, region: 'body' },
  // neckline of the dress
  { d: 'M 300 650 C 360 698 430 722 500 724 C 570 722 640 698 704 650', w: 6, region: 'dress' },
  // forearm crossing from below, hand laid over her heart (viewer's right)
  { d: 'M 330 1100 C 380 1004 452 934 522 894', w: 7, region: 'hand' },
  { d: 'M 404 1100 C 446 1022 504 962 566 930', w: 7, region: 'hand' },
  { d: 'M 560 862 C 582 830 606 800 634 772', w: 12, region: 'hand' },   // index
  { d: 'M 575 875 C 600 843 627 812 657 787', w: 12, region: 'hand' },   // middle
  { d: 'M 589 889 C 613 861 638 835 664 814', w: 12, region: 'hand' },   // ring
  { d: 'M 601 903 C 621 884 642 866 662 851', w: 11, region: 'hand' },   // little
  { d: 'M 552 874 C 546 846 551 822 566 804', w: 11, region: 'hand' },   // thumb
  { d: 'M 522 894 C 552 912 588 916 612 902', w: 7, region: 'hand' },
];

// hair: outer silhouettes and face-framing inner lines (cubic segments, evaluated for the strands)
const HAIR_L_OUT: Cubic[] = [
  [[500, 160], [430, 160], [372, 196], [350, 262]],
  [[350, 262], [330, 326], [330, 400], [336, 470]],
  [[336, 470], [342, 540], [322, 610], [296, 680]],
  [[296, 680], [272, 750], [262, 840], [270, 930]],
  [[270, 930], [276, 990], [292, 1040], [304, 1100]],
];
const HAIR_L_IN: Cubic[] = [
  [[500, 178], [468, 196], [424, 222], [404, 262]],
  [[404, 262], [392, 290], [390, 318], [392, 350]],
  [[392, 350], [394, 400], [402, 440], [420, 470]],
  [[420, 470], [438, 500], [446, 532], [440, 566]],
  [[440, 566], [432, 620], [412, 680], [398, 760]],
];
const HAIR_R_OUT: Cubic[] = [
  [[500, 160], [570, 160], [628, 196], [650, 262]],
  [[650, 262], [670, 326], [672, 400], [666, 470]],
  [[666, 470], [662, 520], [672, 566], [690, 606]],
];
const HAIR_R_IN: Cubic[] = [
  [[500, 178], [532, 196], [576, 222], [596, 262]],
  [[596, 262], [608, 290], [610, 318], [608, 350]],
  [[608, 350], [606, 400], [598, 440], [580, 470]],
  [[580, 470], [566, 494], [566, 526], [584, 560]],
];

function evalCubic(c: Cubic, u: number): Pt {
  const v = 1 - u;
  const a = v * v * v, b = 3 * v * v * u, cc = 3 * v * u * u, d = u * u * u;
  return [a * c[0][0] + b * c[1][0] + cc * c[2][0] + d * c[3][0], a * c[0][1] + b * c[1][1] + cc * c[2][1] + d * c[3][1]];
}
function samplePath(segs: Cubic[], n: number): Pt[] {
  const pts: Pt[] = [];
  for (let i = 0; i <= n; i++) {
    const s = (i / n) * segs.length;
    const k = Math.min(segs.length - 1, Math.floor(s));
    pts.push(evalCubic(segs[k]!, s - k));
  }
  return pts;
}
const cubicD = (segs: Cubic[]) => `M ${segs[0]![0].join(' ')} ` + segs.map((c) => `C ${c[1].join(' ')} ${c[2].join(' ')} ${c[3].join(' ')}`).join(' ');

/** Hair strands between the inner and outer lines (the inner side of the left lock ends at y 760). */
function strands(inner: Cubic[], outer: Cubic[], n: number, seed: number): Pt[][] {
  const A = samplePath(inner, 60), B = samplePath(outer, 60);
  const out: Pt[][] = [];
  for (let i = 1; i < n; i++) {
    const u = i / n;
    const pts: Pt[] = [];
    for (let k = 0; k <= 60; k++) {
      const s = k / 60;
      const a = A[k]!, b = B[k]!;
      const wav = Math.sin(s * 7 + i * 1.9 + seed) * 11 * s + 14 * s * s * (u - 0.5);
      pts.push([a[0] + (b[0] - a[0]) * u + wav, a[1] + (b[1] - a[1]) * u]);
    }
    // strands start at the crown and fan out; stagger their ends
    const cut = Math.floor(60 * (0.82 + 0.18 * Math.abs(Math.sin(i * 12.9898 + seed) * 43758.5453 % 1)));
    out.push(pts.slice(i % 3 === 0 ? 2 : 0, cut));
  }
  return out;
}

/** Draw one layer of the figure into a context already scaled to figure space. */
export function drawFigure(c: CanvasRenderingContext2D, layer: 'line' | 'fill' | 'region') {
  const withHead = (head: boolean | undefined, fn: () => void) => {
    c.save();
    if (head) { c.translate(NECK[0], NECK[1]); c.rotate(HEAD_TILT); c.translate(-NECK[0], -NECK[1]); }
    fn();
    c.restore();
  };
  const regionColor = (r: Region) => `rgb(${REGION_ID[r] * 30},0,0)`;
  c.lineCap = 'round'; c.lineJoin = 'round';
  if (layer === 'fill' || layer === 'region') {
    const tone = (v: number, r: Region) => (layer === 'fill' ? `rgba(255,255,255,${v})` : regionColor(r));
    // body (skin) and dress
    const body = new Path2D('M 452 548 C 420 562 360 570 300 590 C 250 606 222 640 214 700 C 206 770 200 860 196 1100 L 806 1100 C 802 880 796 780 788 704 C 780 644 754 608 704 592 C 646 572 584 562 550 548 C 544 520 540 490 540 452 L 462 452 C 462 490 458 520 452 548 Z');
    c.fillStyle = tone(0.0, 'body'); c.fill(body);
    const dress = new Path2D('M 300 650 C 360 698 430 722 500 724 C 570 722 640 698 704 650 C 760 660 788 700 788 704 C 796 780 802 880 806 1100 L 196 1100 C 200 860 206 770 214 700 C 222 660 260 640 300 650 Z');
    c.fillStyle = tone(0.12, 'dress'); c.fill(dress);
    // face
    withHead(true, () => {
      const face = new Path2D('M 398 250 C 396 352 406 404 436 437 C 456 458 478 470 500 471 C 522 470 544 458 564 437 C 594 404 604 352 602 250 Z');
      c.fillStyle = tone(0.0, 'face'); c.fill(face);
      // hair masses
      c.fillStyle = tone(0.3, 'hair');
      c.beginPath();
      const LO = samplePath(HAIR_L_OUT, 80), LI = samplePath(HAIR_L_IN, 80);
      c.moveTo(...LO[0]!); for (const p of LO) c.lineTo(...p);
      c.lineTo(398, 1100); for (const p of [...LI].reverse()) c.lineTo(...p); c.closePath(); c.fill();
      c.beginPath();
      const RO = samplePath(HAIR_R_OUT, 60), RI = samplePath(HAIR_R_IN, 60);
      c.moveTo(...RO[0]!); for (const p of RO) c.lineTo(...p);
      for (const p of [...RI].reverse()) c.lineTo(...p); c.closePath(); c.fill();
      // top of the head (between the two inner lines)
      c.beginPath(); c.moveTo(...LO[0]!);
      for (const p of samplePath([HAIR_L_IN[0]!], 20)) c.lineTo(...p);
      c.lineTo(...RI[0]!); for (const p of samplePath([HAIR_R_IN[0]!], 20)) c.lineTo(...p);
      c.closePath(); c.fill();
    });
    // hand
    const hand = new Path2D('M 330 1100 C 380 1004 452 934 522 894 C 540 860 560 820 600 790 C 630 770 660 780 664 814 C 668 850 640 890 612 902 C 588 916 566 930 566 930 C 504 962 446 1022 404 1100 Z');
    c.fillStyle = tone(0.1, 'hand'); c.fill(hand);
    if (layer === 'region') {
      // the heart lives under her hand
      c.fillStyle = regionColor('heart');
      c.beginPath(); c.ellipse(600, 830, 70, 60, 0, 0, Math.PI * 2); c.fill();
    }
    return;
  }
  // line layer
  c.strokeStyle = '#fff';
  withHead(true, () => {
    for (const [segs, w] of [[HAIR_L_OUT, 7], [HAIR_L_IN, 7], [HAIR_R_OUT, 7], [HAIR_R_IN, 7]] as const) {
      c.lineWidth = w; c.stroke(new Path2D(cubicD(segs as Cubic[])));
    }
    c.lineWidth = 4;
    for (const s of [...strands(HAIR_L_IN, HAIR_L_OUT, 3, 1), ...strands(HAIR_R_IN, HAIR_R_OUT, 2, 2)]) {
      c.beginPath(); c.moveTo(...s[0]!); for (const p of s) c.lineTo(...p); c.stroke();
    }
  });
  for (const s of STROKES) withHead(s.head, () => { c.lineWidth = s.w; c.stroke(new Path2D(s.d)); });
}

// ------------------------------------------------------------------ glyph grid
export const GLYPH = { dash: 0, slash: 1, bar: 2, back: 3, dot: 4, plus: 5 } as const;
export type GlyphKind = (typeof GLYPH)[keyof typeof GLYPH];
export interface Glyph {
  x: number; y: number;          // cell centre, px relative to the figure's top-left (display scale)
  row: number; col: number;
  kind: GlyphKind;
  ink: number;                   // 0..1 strength
  region: Region;
  run: number;                   // index of the "comment" (horizontal run) it arrives with
}
export interface Run { id: number; row: number; c0: number; c1: number; glyphs: number[]; region: Region }
export interface GlyphGrid { glyphs: Glyph[]; runs: Run[]; cellW: number; cellH: number; cols: number; rows: number; width: number; height: number }

/**
 * Rasterise the figure at `height` px and convert it to glyph cells of cellW x cellH px.
 * Lines become oriented glyphs (structure tensor of the line layer), flat tone becomes dots.
 */
export function buildGlyphGrid(height: number, cellW = 9, cellH = 16): GlyphGrid {
  const s = height / FIG_H, width = Math.round(FIG_W * s);
  const cols = Math.ceil(width / cellW), rows = Math.ceil(height / cellH);
  const mk = () => { const cv = document.createElement('canvas'); cv.width = cols * cellW; cv.height = rows * cellH; const c = cv.getContext('2d', { willReadFrequently: true })!; c.scale(s, s); return { cv, c }; };
  const L = mk(), Fl = mk(), R = mk();
  drawFigure(L.c, 'line'); drawFigure(Fl.c, 'fill'); drawFigure(R.c, 'region');
  const Wd = L.cv.width, Hd = L.cv.height;
  const la = L.c.getImageData(0, 0, Wd, Hd).data, fa = Fl.c.getImageData(0, 0, Wd, Hd).data, ra = R.c.getImageData(0, 0, Wd, Hd).data;
  const A = (x: number, y: number) => (x < 0 || y < 0 || x >= Wd || y >= Hd ? 0 : la[(y * Wd + x) * 4 + 3]! / 255);
  const glyphs: Glyph[] = [];
  const grid: number[] = new Array(cols * rows).fill(-1);
  const regionOf = (id: number): Region => (Object.keys(REGION_ID) as Region[]).find((k) => REGION_ID[k] === id) ?? 'body';
  for (let r = 0; r < rows; r++) for (let q = 0; q < cols; q++) {
    let cov = 0, jxx = 0, jyy = 0, jxy = 0, tone = 0, n = 0;
    for (let y = r * cellH; y < (r + 1) * cellH; y++) for (let x = q * cellW; x < (q + 1) * cellW; x++) {
      const a = A(x, y); cov += a; n++;
      const gx = A(x + 1, y) - A(x - 1, y), gy = A(x, y + 1) - A(x, y - 1);
      jxx += gx * gx; jyy += gy * gy; jxy += gx * gy;
      tone += fa[(y * Wd + x) * 4 + 3]! / 255;
    }
    cov /= n; tone /= n;
    const cx = q * cellW + cellW / 2, cy = r * cellH + cellH / 2;
    const rid = Math.round(ra[(Math.min(Hd - 1, Math.round(cy)) * Wd + Math.min(Wd - 1, Math.round(cx))) * 4]! / 30);
    const region = regionOf(rid);
    let kind: GlyphKind | -1 = -1, ink = 0;
    if (cov > 0.07) {
      const coh = Math.sqrt((jxx - jyy) ** 2 + 4 * jxy * jxy) / (jxx + jyy + 1e-6);
      const th = 0.5 * Math.atan2(2 * jxy, jxx - jyy) + Math.PI / 2; // line direction (y down)
      const a = ((th % Math.PI) + Math.PI) % Math.PI;
      const k = Math.round(a / (Math.PI / 4)) % 4;                  // 0:— 1:\ (y down) 2:| 3:/
      kind = coh < 0.35 && cov > 0.2 ? GLYPH.plus : k === 0 ? GLYPH.dash : k === 1 ? GLYPH.back : k === 2 ? GLYPH.bar : GLYPH.slash;
      ink = Math.min(1, 0.45 + cov * 2);
    } else if (tone > 0.03) {
      // dither the tone: brighter areas get more dots (ordered by a hash so it looks like text, not noise)
      const h = Math.abs(Math.sin(q * 12.9898 + r * 78.233) * 43758.5453) % 1;
      if (h < tone * 1.25) { kind = GLYPH.dot; ink = 0.3 + tone; }
    }
    if (kind >= 0) {
      grid[r * cols + q] = glyphs.length;
      glyphs.push({ x: cx, y: cy, row: r, col: q, kind: kind as GlyphKind, ink, region, run: -1 });
    }
  }
  // runs: horizontal sequences in a row (gaps of one empty cell allowed) = the comments she's made of
  const runs: Run[] = [];
  for (let r = 0; r < rows; r++) {
    let cur: Run | null = null, gap = 0;
    for (let q = 0; q < cols; q++) {
      const gi = grid[r * cols + q]!;
      if (gi >= 0) {
        const g = glyphs[gi]!;
        const len = cur ? q - cur.c0 : 0;
        if (!cur || gap > 1 || len > 14) { cur = { id: runs.length, row: r, c0: q, c1: q, glyphs: [], region: g.region }; runs.push(cur); }
        cur.c1 = q; cur.glyphs.push(gi); g.run = cur.id; gap = 0;
      } else if (cur) { gap++; if (gap > 1) cur = null; }
    }
  }
  return { glyphs, runs, cellW, cellH, cols, rows, width, height };
}
