// SHOT — 'xray' (a chest radiograph). One idea: look inside — there's still a heart in there.
// A PA chest film builds up under a scan bar moving top to bottom: clavicles, ribs, spine, dark lung
// fields with their vessels. Where the heart should be sits a heart. On the word 'heart' it fills
// orange (the ribs still show through it, as they would on a film); through 'inside' it beats on the
// beat, lub-dub, and the view leans toward it. A radiographer's strip types the findings as sung.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { rgba } from '../engine/palette';
import { F, font } from '../engine/type';
import { clamp, ease } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { wordText } from '../danmaku/kinetic';
import type { Word } from '../engine/lyrics';
import { CLEAN } from './poster';

const S = 455;                               // px per chest unit
const HEART_TIP: [number, number] = [0.5, -0.8], HEART_SIZE = 0.64, HEART_ANG = 0.5;

function sdHeart(x: number, y: number) {
  x = Math.abs(x);
  if (y + x > 1) return Math.hypot(x - 0.25, y - 0.75) - Math.SQRT2 / 4;
  const a = (x) ** 2 + (y - 1) ** 2, m = 0.5 * Math.max(x + y, 0), b = (x - m) ** 2 + (y - m) ** 2;
  return Math.sqrt(Math.min(a, b)) * Math.sign(x - y);
}

export default class Xray extends Mode {
  film = new FSPass(/* glsl */ `
    uniform vec2 camC; uniform float camS; uniform float scanY; uniform float heartOn; uniform float beat;
    uniform vec2 hTip; uniform float hSize; uniform float hAng;
    float dot2(vec2 v) { return dot(v, v); }
    float sdHeart(vec2 p) {
      p.x = abs(p.x);
      if (p.y + p.x > 1.0) return sqrt(dot2(p - vec2(0.25, 0.75))) - sqrt(2.0) / 4.0;
      return sqrt(min(dot2(p - vec2(0.0, 1.0)), dot2(p - 0.5 * max(p.x + p.y, 0.0)))) * sign(p.x - p.y);
    }
    // a tubular bone seen side-on: faint marrow, bright cortex at both edges
    float bone(float d, float hw, float aa) {
      float inside = 1.0 - smoothstep(hw - aa, hw + aa, d);
      float cortex = smoothstep(hw - 0.022, hw - 0.004, d) * inside;
      return 0.5 * inside + 0.75 * cortex;
    }
    float curveDist(vec2 q, float yc, float slope) { return abs(q.y - yc) / sqrt(1.0 + slope * slope); }
    float ribs(vec2 q, float aa, out float ant) {
      float ax = abs(q.x), acc = 0.0; ant = 0.0;
      for (int i = 0; i < 10; i++) {
        float fi = float(i);
        float y0 = 0.93 - fi * 0.178;
        float L = 0.5 + 0.78 * smoothstep(0.0, 4.5, fi);         // the cage widens down to the 6th rib
        float hw = 0.03 + 0.004 * fi / 9.0;
        // posterior rib: out from the spine, a slight rise, then down round the side
        float u = (ax - 0.09) / L;
        if (u > -0.05 && u < 1.08) {
          float k = 3.1416 * 0.9;
          float yc = y0 + 0.07 * sin(k * u) - 0.26 * u * u * u;
          float sl = (0.07 * k * cos(k * u) - 0.78 * u * u) / L;
          float end = smoothstep(-0.03, 0.04, u) * (1.0 - smoothstep(0.98, 1.06, u));
          acc += bone(curveDist(q, yc, sl), hw, aa) * end;
        }
        // anterior rib: from the side back toward the sternum, sloping down, fainter
        float xe = 0.09 + L * 1.02, ye = y0 + 0.07 * sin(3.1416 * 0.9 * 1.02) - 0.26 * 1.06;
        float v = (xe - ax) / (xe - 0.32);
        if (v > -0.05 && v < 1.0 && i < 8) {
          float yc = ye - 0.36 * pow(max(v, 0.0), 1.25) + 0.05 * sin(3.1416 * v);
          float sl = (0.36 * 1.25 * pow(max(v, 0.001), 0.25) - 0.05 * 3.1416 * cos(3.1416 * v)) / (xe - 0.32);
          float end = smoothstep(-0.05, 0.05, v) * (1.0 - smoothstep(0.75, 1.0, v));
          ant += bone(curveDist(q, yc, sl), hw * 0.9, aa) * end;
        }
      }
      return acc;
    }
    float spine(vec2 q, float aa) {
      float h = 0.158;
      float yy = mod(q.y + 2.0, h) - h * 0.5;
      float body = sdBox(vec2(q.x, yy), vec2(0.085 + 0.012 * (1.0 - q.y), 0.058)) - 0.012;
      float b = (1.0 - smoothstep(-aa, aa, body)) * 0.45 + (1.0 - smoothstep(0.0, 0.012, abs(body))) * 0.5;
      // pedicles: little rings either side
      vec2 pp = vec2(abs(q.x) - 0.062, yy + 0.01);
      float ped = 1.0 - smoothstep(0.0, 0.008, abs(length(pp / vec2(0.022, 0.03)) - 1.0) * 0.022);
      // spinous process: a teardrop on the midline
      float sp = 1.0 - smoothstep(-aa, aa, length(vec2(q.x * 1.8, yy + 0.02)) - 0.028);
      return b + 0.28 * ped + 0.25 * sp;
    }
    float clav(vec2 q, float aa) {
      float ax = abs(q.x);
      float u = (ax - 0.13) / 0.98;
      if (u < -0.05 || u > 1.05) return 0.0;
      float yc = 0.8 + 0.2 * u + 0.045 * sin(6.2832 * u);
      float sl = (0.2 + 0.045 * 6.2832 * cos(6.2832 * u)) / 0.98;
      float end = smoothstep(-0.04, 0.03, u) * (1.0 - smoothstep(0.95, 1.05, u));
      return bone(curveDist(q, yc, sl), 0.034, aa) * end;
    }
    float lung(vec2 q, float side) {
      float ax = abs(q.x);
      // an egg, narrower at the apex, cut by the dome of the diaphragm; the heart side is smaller
      vec2 c = vec2(0.76, 0.02);
      vec2 r = vec2(0.5 + 0.06 * smoothstep(0.8, -0.4, q.y), 0.92);
      float e = length((vec2(ax, q.y) - c) / r) - 1.0;
      float dd = (ax - 0.78) / 0.56;
      float dome = -0.6 - 0.34 * dd * dd + (side > 0.0 ? -0.05 : 0.0);
      float m = (1.0 - smoothstep(-0.05, 0.03, e)) * smoothstep(dome - 0.02, dome + 0.04, q.y);
      m *= smoothstep(0.14, 0.26, ax);
      return m;
    }
    void main() {
      vec2 p = FRAG_PX; p.y = ${H.toFixed(1)} - p.y;              // px, y down
      vec2 q = (p - vec2(${(W / 2).toFixed(1)}, 540.0)) / (${S.toFixed(1)} * camS);
      q.y = -q.y; q += camC;                                       // chest units, y up
      float aa = 1.5 / (${S.toFixed(1)} * camS);
      float ax = abs(q.x);
      // torso: soft tissue thicker toward the middle; shoulders flare at the top
      float bw = 1.5 + 0.42 * smoothstep(0.45, 1.1, q.y);
      float body = 1.0 - smoothstep(-0.02, 0.02, ax - bw);
      float soft = 0.3 * body * (0.55 + 0.45 * smoothstep(0.0, 0.5, bw - ax));
      float lu = lung(q, sign(q.x));
      // the heart (drawn where the real one sits, tilted toward the left of the patient)
      float ca = cos(hAng), sa = sin(hAng);
      vec2 hq = q - hTip; hq = vec2(ca * hq.x + sa * hq.y, -sa * hq.x + ca * hq.y);
      float hs = hSize * (1.0 + 0.07 * beat);
      float hd = sdHeart(hq / hs + vec2(0.0, 0.0)) * hs;
      float heart = 1.0 - smoothstep(-aa, aa, hd);
      float heartBody = smoothstep(0.02, -0.14, hd);
      lu *= 1.0 - heart;
      // lung markings: vessels branching out of each hilum, fading to the periphery
      vec2 hil = vec2(0.34, 0.06);
      vec2 hp = vec2(ax, q.y) - hil;
      float rr = length(hp), th = atan(hp.y, hp.x);
      float ves = abs(snoise(vec2(th * 7.0 + 0.8 * snoise(q * 4.0), rr * 2.2 - 0.5 * snoise(q * 9.0))));
      ves = (1.0 - smoothstep(0.0, 0.16, ves)) * exp(-rr * 1.6) * lu;
      float D = soft - 0.2 * lu + 0.1 * ves;
      float ant;
      float rb = ribs(q, aa, ant) * body;
      float sp = spine(q, aa);
      D += 0.32 * rb + 0.07 * ant * body + 0.17 * sp * (1.0 - 0.4 * lu) + 0.42 * clav(q, aa);
      D += 0.2 * heart * heartBody + 0.06 * heart;
      // below the diaphragm: dense abdomen, and the stomach's air bubble under the left dome
      float abd = body * (1.0 - lu) * smoothstep(-0.55, -0.85, q.y) * (1.0 - heart);
      D += 0.08 * abd;
      D -= 0.1 * (1.0 - smoothstep(-0.01, 0.02, length((q - vec2(0.72, -1.02)) / vec2(0.22, 0.1)) - 1.0));
      // film response: grey scale from ink to bone
      float I = 1.0 - exp(-2.6 * max(D, 0.0));
      I *= 1.0 - 0.28 * smoothstep(0.7, 1.5, length(q / vec2(1.9, 1.15)));   // beam falls off at the edges
      float grain = (hash12(floor(p)) - 0.5) * 0.05 + 0.03 * snoise(p * 0.9);
      I = clamp(I + grain * (0.4 + I), 0.0, 1.0);
      vec3 col = mix(C_INK * 0.7, C_BONE, pow(I, 1.15));
      // the heart in orange: flat, a touch deeper at the middle, the ribs and spine still showing through
      float over = clamp(0.8 * rb + 0.35 * sp, 0.0, 1.0);
      vec3 hc = C_SIGNAL * (0.86 + 0.18 * heartBody) + (C_EMBER - C_SIGNAL) * over * 0.9;
      col = mix(col, hc, heart * heartOn);
      // the scan: exposed above the bar, dark below; the bar itself a thin white line
      float below = smoothstep(scanY - 1.0, scanY + 1.0, p.y);
      float wake = exp(-max(scanY - p.y, 0.0) / 60.0) * (1.0 - below);
      col = mix(col + wake * 0.18 * C_BONE, C_INK * 0.55, below);
      col += C_BONE * (1.0 - smoothstep(0.0, 1.6, abs(p.y - scanY))) * step(scanY, ${H.toFixed(1)} + 10.0);
      fragColor = vec4(col, 1.0);
    }`, {
    camC: { value: new THREE.Vector2(0, 0) }, camS: { value: 1 }, scanY: { value: 0 }, heartOn: { value: 0 }, beat: { value: 0 },
    hTip: { value: new THREE.Vector2(...HEART_TIP) }, hSize: { value: HEART_SIZE }, hAng: { value: HEART_ANG },
  });
  L = new Layer2D();
  words: Word[] = [];
  tHeart = 1e9; tEnd = 1e9;
  heartSpan: [number, number, number] = [0, 0, 0];   // chest-units: y, x0, x1 of the widest cut

  init() {
    this.words = this.wordsIn();
    const hw = this.words.find((w) => /heart/i.test(w.w));
    this.tHeart = hw?.start ?? this.cutTime + 1.2;
    this.tEnd = this.ctx.params.cutOut ?? this.ctx.end;
    // the widest horizontal chord through the heart, for the measurement line
    let best: [number, number, number] = [0, 0, 0];
    for (let y = -0.9; y < 0.2; y += 0.01) {
      let x0 = 9, x1 = -9;
      for (let x = -0.8; x < 1.4; x += 0.005) {
        const ca = Math.cos(HEART_ANG), sa = Math.sin(HEART_ANG);
        const dx = x - HEART_TIP[0], dy = y - HEART_TIP[1];
        const hx = ca * dx + sa * dy, hy = -sa * dx + ca * dy;
        if (sdHeart(hx / HEART_SIZE, hy / HEART_SIZE) < 0) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); }
      }
      if (x1 - x0 > best[2] - best[1]) best = [y, x0, x1];
    }
    this.heartSpan = best;
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    const beatLen = 60 / audio.bpm;
    // the scan bar reaches the bottom of the heart just as 'heart' is sung
    const t0 = this.cutTime, t1 = this.tHeart + 0.22;
    const scanY = 330 + (H + 30 - 330) * ease.outQuad(clamp((t - t0) / (t1 - t0)));   // the cut lands on a film already part-exposed
    const on = clamp((t - this.tHeart) / 0.06);
    // lub-dub on every beat after 'heart'
    let bt = 0;
    if (t >= this.tHeart) {
      const bi = audio.beatAt(t), b0 = Math.floor(bi), tb = audio.timeOfBeat(b0);
      const since = t - tb;
      bt = Math.exp(-since * 16) + 0.6 * (since > beatLen * 0.25 ? Math.exp(-(since - beatLen * 0.25) * 16) : 0);
      if (tb < this.tHeart - 0.02) bt = Math.exp(-(t - this.tHeart) * 16);
    }
    // camera: still while scanning, then leans toward the heart
    const lean = ease.inOutCubic(clamp((t - this.tHeart) / Math.max(0.3, this.tEnd - this.tHeart)));
    const camS = 1 + 0.16 * lean, camC: [number, number] = [0.22 * lean, -0.3 * lean];
    const u = this.film.u;
    (u.camC!.value as THREE.Vector2).set(camC[0], camC[1]); u.camS!.value = camS; u.scanY!.value = scanY;
    u.heartOn!.value = on; u.beat!.value = bt;
    this.film.render(renderer, out);

    const c = this.L.ctx; this.L.clear();
    const toPx = (x: number, y: number): [number, number] => [W / 2 + (x - camC[0]) * S * camS, 540 - (y - camC[1]) * S * camS];
    // the lead 'L' marker, on the film (shows white: lead stops the rays)
    const [lx, ly] = toPx(1.55, 0.98);
    if (ly < scanY) {
      c.save(); c.translate(lx, ly); c.scale(camS, camS);
      c.strokeStyle = rgba('bone', 0.95); c.lineWidth = 3; c.strokeRect(-34, -40, 68, 80);
      c.font = font(F.archivo(100, 900), 64); c.fillStyle = rgba('bone', 0.95); c.textAlign = 'center'; c.textBaseline = 'middle';
      c.fillText('L', 0, 3);
      c.restore();
    }
    // the measurement across the heart, once it's lit
    if (on > 0) {
      const [yy, x0, x1] = this.heartSpan;
      const [ax, ay] = toPx(x0, yy), [bx] = toPx(x1, yy);
      const k = ease.outExpo(clamp((t - this.tHeart - 0.12) / 0.25));
      const mx = ax + (bx - ax) * k;
      c.strokeStyle = rgba('bone', 1); c.lineWidth = 2; c.setLineDash([10, 7]);
      c.beginPath(); c.moveTo(ax, ay); c.lineTo(mx, ay); c.stroke(); c.setLineDash([]);
      c.beginPath(); c.moveTo(ax, ay - 14); c.lineTo(ax, ay + 14); c.stroke();
      if (k > 0.98) { c.beginPath(); c.moveTo(bx, ay - 14); c.lineTo(bx, ay + 14); c.stroke(); }
      if (k > 0.5) {
        c.font = font(F.mono(700), 22); c.fillStyle = rgba('bone', 1); c.textAlign = 'left'; c.textBaseline = 'bottom';
        c.fillText(`${((x1 - x0) * 11.6).toFixed(1)} CM`, bx + 16, ay - 8);
      }
    }
    // the plate's own labels (screen-fixed)
    c.font = font(F.mono(500), 18); c.fillStyle = rgba('bone', 0.8); c.textAlign = 'left'; c.textBaseline = 'alphabetic';
    c.fillText('PA CHEST  ·  ERECT', 70, 74);
    c.fillText('120 kVp  ·  2.0 mAs', 70, 100);
    c.textAlign = 'right';
    c.fillText(`${(t - t0 + 0.004).toFixed(2)} S`, W - 70, 74);
    // a ruler down the left edge
    c.strokeStyle = rgba('bone', 0.55); c.lineWidth = 1.5;
    for (let i = 0; i <= 40; i++) { const y = 180 + i * 18; if (y > scanY) break; c.beginPath(); c.moveTo(40, y); c.lineTo(i % 5 ? 52 : 64, y); c.stroke(); }
    // findings, typed as sung
    const typed = this.words.filter((w) => t >= w.start).map((w) => wordText(w.w)).join(' ');
    c.fillStyle = rgba('ink', 0.85); c.fillRect(0, H - 96, W, 96);
    c.font = font(F.mono(700), 30); c.textAlign = 'left'; c.textBaseline = 'middle';
    c.fillStyle = rgba('ash', 1); c.fillText('FINDINGS', 70, H - 48);
    c.fillStyle = rgba('bone', 1); c.fillText(typed + (Math.floor(t * 4) % 2 ? '_' : ''), 270, H - 48);
    if (t >= this.tHeart) {
      const hw = this.words.find((w) => /heart/i.test(w.w));
      if (hw) {
        // the word 'heart' in the findings, in orange
        const pre = this.words.slice(0, this.words.indexOf(hw)).map((w) => wordText(w.w)).join(' ');
        c.font = font(F.mono(700), 30);
        const x = 270 + c.measureText(pre + (pre ? ' ' : '')).width;
        c.fillStyle = rgba('ink', 1); c.fillRect(x - 2, H - 70, c.measureText(wordText(hw.w)).width + 4, 44);
        c.fillStyle = rgba('signal', 1); c.fillText(wordText(hw.w), x, H - 48);
      }
    }
    comp.draw(renderer, this.L.upload(), out);
    return { ...CLEAN, zoom: 1 + 0.01 * bt };
  }
}
