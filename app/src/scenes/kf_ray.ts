// KEYFRAME 4 — the maze in 3D ("Make me real this time"). A first-person raycast corridor like an old
// shooter, but every surface is symbols: walls of stacked bars with courses of dashes and a few [ ] bricks,
// a floor of dots, a ceiling of beams, fog to black. She walks away from us down the corridor toward a
// door at the end whose opening is pure light, REAL written over it. A status bar across the bottom:
// her hearts, a REALITY meter, her face, the floor, the keys; the line as a subtitle above it.
import * as THREE from 'three';
import type { Frame, PostOverrides } from '../engine/scene';
import { FSPass, Layer2D, W, H } from '../engine/gl';
import { F, font } from '../engine/type';
import { clamp, hash } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { wordText } from '../danmaku/kinetic';
import { GlyphPen } from '../game/glyph';
import { drawGirl } from '../game/girl';
import { C, symBox, symHeart, outlineWord } from '../game/world';

// the map: '#' wall, '.' floor, 'D' the door frame, 'R' the door's light
const MAP = [
  '################',
  '#######..#######',
  '#######..#######',
  '####.....#######',
  '####.##..#######',
  '#######..#######',
  '#######.....####',
  '#######..##.####',
  '#######..#######',
  '######DRRD######',
  '################',
];

export default class KfRay extends Mode {
  mapTex: THREE.DataTexture;
  ray: FSPass;
  L = new Layer2D();
  constructor(ctx: any) {
    super(ctx);
    const mw = 16, mh = MAP.length;
    const data = new Uint8Array(mw * mh * 4);
    MAP.forEach((row, z) => { for (let x = 0; x < mw; x++) { const ch = row[x] ?? '#'; data[(z * mw + x) * 4] = ch === '#' ? 1 : ch === 'D' ? 2 : ch === 'R' ? 3 : 0; data[(z * mw + x) * 4 + 3] = 255; } });
    this.mapTex = new THREE.DataTexture(data, mw, mh, THREE.RGBAFormat, THREE.UnsignedByteType);
    this.mapTex.magFilter = THREE.NearestFilter; this.mapTex.minFilter = THREE.NearestFilter; this.mapTex.needsUpdate = true;
    this.ray = new FSPass(/* glsl */ `
      uniform sampler2D mapT; uniform vec2 mapSize, camPos, camDir, camPlane; uniform float horizon, roll, time;
      float segd(vec2 p, vec2 a, vec2 b) { vec2 pa = p - a, ba = b - a; float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0); return length(pa - ba * h); }
      float glyphD(vec2 q, float k) {
        if (k < 0.5) return segd(q, vec2(0.5, 0.12), vec2(0.5, 0.88));
        if (k < 1.5) return segd(q, vec2(0.14, 0.5), vec2(0.86, 0.5));
        if (k < 2.5) return segd(q, vec2(0.2, 0.88), vec2(0.8, 0.12));
        if (k < 3.5) return segd(q, vec2(0.2, 0.12), vec2(0.8, 0.88));
        if (k < 4.5) return min(segd(q, vec2(0.18, 0.5), vec2(0.82, 0.5)), segd(q, vec2(0.5, 0.18), vec2(0.5, 0.82)));
        if (k < 5.5) return min(segd(q, vec2(0.14, 0.34), vec2(0.86, 0.34)), segd(q, vec2(0.14, 0.66), vec2(0.86, 0.66)));
        if (k < 6.5) return min(min(segd(q, vec2(0.72, 0.1), vec2(0.3, 0.1)), segd(q, vec2(0.3, 0.1), vec2(0.3, 0.9))), segd(q, vec2(0.3, 0.9), vec2(0.72, 0.9)));
        if (k < 7.5) return min(min(segd(q, vec2(0.28, 0.1), vec2(0.7, 0.1)), segd(q, vec2(0.7, 0.1), vec2(0.7, 0.9))), segd(q, vec2(0.7, 0.9), vec2(0.28, 0.9)));
        return length(q - vec2(0.5, 0.5));
      }
      float mapAt(ivec2 c) { if (c.x < 0 || c.y < 0 || float(c.x) >= mapSize.x || float(c.y) >= mapSize.y) return 1.0; return floor(texelFetch(mapT, c, 0).r * 255.0 + 0.5); }
      float ink(vec2 cellUv, float k, float wpx) {
        vec2 q = fract(cellUv);
        float d = glyphD(q, k);
        float px = max(fwidth(cellUv.x), fwidth(cellUv.y));
        return (1.0 - smoothstep(wpx * px * 0.5, wpx * px * 0.5 + px, d)) * sat(0.03 / max(px, 1e-4));
      }
      void main() {
        vec2 p = FRAG_PX;                                  // y up
        // roll the camera a little
        vec2 cc = vec2(${(W / 2).toFixed(1)}, ${(H / 2).toFixed(1)});
        vec2 pr = cc + mat2(cos(roll), -sin(roll), sin(roll), cos(roll)) * (p - cc);
        float sx = pr.x / ${W.toFixed(1)} * 2.0 - 1.0;
        vec2 rd = camDir + camPlane * sx;
        // DDA
        ivec2 m = ivec2(floor(camPos));
        vec2 dd = abs(1.0 / rd);
        ivec2 st = ivec2(sign(rd));
        vec2 sd = (sign(rd) * (vec2(m) - camPos) + sign(rd) * 0.5 + 0.5) * dd;
        float side = 0.0, hit = 0.0;
        for (int i = 0; i < 48; i++) {
          if (sd.x < sd.y) { sd.x += dd.x; m.x += st.x; side = 0.0; } else { sd.y += dd.y; m.y += st.y; side = 1.0; }
          hit = mapAt(m);
          if (hit > 0.5) break;
        }
        float dist = side < 0.5 ? sd.x - dd.x : sd.y - dd.y;
        float lineH = ${H.toFixed(1)} / dist;
        float y = pr.y - horizon;                           // px from the horizon, up positive
        vec3 col = C_INK;
        if (abs(y) < lineH * 0.5) {
          // wall
          float wx = side < 0.5 ? camPos.y + dist * rd.y : camPos.x + dist * rd.x;
          wx = fract(wx);
          float v = 0.5 - y / lineH;                        // 0 top .. 1 bottom
          vec2 uv = vec2(wx, v);
          float shade = side < 0.5 ? 1.0 : 0.72;
          if (hit < 1.5) {
            vec2 cu = uv * vec2(8.0, 10.0);
            vec2 id = floor(cu);
            float k = mod(id.y, 3.0) < 0.5 ? 1.0 : 0.0;
            float hh = hash12(id + vec2(float(m.x) * 7.0, float(m.y) * 13.0 + side * 3.0));
            if (hh < 0.08) k = mod(id.x, 2.0) < 0.5 ? 6.0 : 7.0;
            else if (hh < 0.11) k = 4.0;
            float a = ink(cu, k, 1.8);
            col = mix(C_INK2 * 1.4, C_BONE * shade, a);
          } else if (hit < 2.5) {
            vec2 cu = uv * vec2(6.0, 10.0);
            float k = mod(floor(cu.x), 2.0) < 0.5 ? 5.0 : 4.0;
            col = mix(C_INK2 * 1.6, C_BONE, ink(cu, k, 2.0));
          } else {
            // the door's opening: light, with a thin frame of symbols
            float edge = min(min(uv.x, 1.0 - uv.x), uv.y);
            col = C_BONE * (0.93 + 0.05 * snoise(uv * 6.0 + time * 0.3));
            vec2 cu = uv * vec2(6.0, 10.0);
            if (uv.y < 0.1) col = mix(col, C_INK, ink(cu, 1.0, 2.2));
          }
          col *= exp(-dist * 0.13);
        } else {
          // floor (below) and ceiling (above)
          float rowDist = 0.5 * ${H.toFixed(1)} / max(abs(y), 1.0);
          vec2 wp = camPos + rd * rowDist;
          if (y < 0.0) {
            vec2 cu = wp * 4.0;
            float a = ink(cu, 8.0, 3.0);
            vec2 cu2 = wp * 1.0;
            float a2 = ink(cu2, 4.0, 1.6);
            col = C_BONE * (a * 0.55 + a2 * 0.8);
          } else {
            vec2 cu = vec2(wp.x * 2.0, wp.y * 2.0);
            float a = ink(cu, 1.0, 1.6) * step(0.5, mod(floor(cu.y), 2.0));
            col = C_BONE * a * 0.45;
          }
          col *= exp(-rowDist * 0.2);
        }
        fragColor = vec4(col, 1.0);
      }`, {
      mapT: { value: this.mapTex }, mapSize: { value: new THREE.Vector2(16, MAP.length) },
      camPos: { value: new THREE.Vector2(8, 1.4) }, camDir: { value: new THREE.Vector2(0, 1) }, camPlane: { value: new THREE.Vector2(0.75, 0) },
      horizon: { value: H / 2 }, roll: { value: 0 }, time: { value: 0 },
    });
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides {
    const { renderer, comp, audio } = this.ctx;
    const t = f.t;
    const lt = t - this.ctx.start;
    // the camera creeps forward behind her, with a step bob and a slight roll on the kicks
    const kick = audio.hit('kick', t, 0.1);
    const z = 1.2 + lt * 0.35;
    const u = this.ray.u;
    (u.camPos!.value as THREE.Vector2).set(8, z);
    const hz = 470 + Math.sin(t * 8) * 4;
    u.horizon!.value = H - hz;
    u.roll!.value = -0.02 + 0.015 * Math.sin(t * 1.3) + 0.01 * kick;
    u.time!.value = t;
    this.ray.render(renderer, out);
    const c = this.L.ctx; this.L.clear();
    const pen = new GlyphPen(c);
    // the word over the door: its lintel at map z = 9
    const dz = 9 - z;
    const doorW = (2 / dz) / (2 * 0.75) * W, doorTop = hz - (H / dz) * 0.5;
    const pxs = Math.max(3, (doorW * 0.8) / 23);
    outlineWord(pen, 'REAL', W / 2 - (23 * pxs) / 2, doorTop - 9 * pxs, pxs, C.bone, Math.max(1.4, pxs * 0.22));
    pen.flush();
    // her: walking away down the corridor, 2.6 units ahead
    const d = 2.6, s = (H / d) * 0.56 / 1.6;
    const feet = hz + (H / d) * 0.5;
    drawGirl(pen, 'backwalk', t * 1.6, W / 2 - s / 2 - 20, feet - s * 1.5, s, {});
    pen.flush();
    // subtitle line
    const line = this.linesIn(t - 4, t + 0.01).filter((l) => l.start <= t).pop();
    if (line) {
      c.font = font(F.mono(700), 34); c.textAlign = 'center'; c.textBaseline = 'middle';
      const s2 = line.words.filter((w) => t >= w.start).map((w) => wordText(w.w)).join(' ');
      c.fillStyle = 'rgba(10,10,11,0.8)'; const tw = c.measureText(s2).width; c.fillRect(W / 2 - tw / 2 - 20, 860, tw + 40, 50);
      c.fillStyle = C.bone; c.fillText(s2, W / 2, 886);
    }
    // status bar
    const by = 930;
    c.fillStyle = C.ink2; c.fillRect(0, by, W, H - by);
    symBox(pen, 14, by + 10, W - 28, H - by - 24, C.ash, 16, 1.8);
    const sep = [420, 860, 1060, 1500];
    for (const x of sep) for (let yy = by + 26; yy < H - 26; yy += 16) pen.glyph('|', x - 8, yy, 16, 16, C.graphite, 1.6);
    pen.flush();
    c.font = font(F.mono(500), 15); c.fillStyle = C.ash; c.textAlign = 'left'; c.textBaseline = 'alphabetic';
    c.fillText('HEART', 50, by + 44); c.fillText('REALITY', 452, by + 44); c.fillText('FLOOR', 1092, by + 44); c.fillText('KEYS', 1532, by + 44);
    for (let k = 0; k < 3; k++) symHeart(pen, 80 + k * 64, by + 92, 11);
    pen.flush();
    c.font = font(F.mono(700), 40); c.fillStyle = C.bone; c.fillText('100%', 280, by + 108);
    // the reality meter: bars filling on the beat
    const fill = clamp(0.12 + 0.03 * Math.floor((t - this.ctx.start) * 1.65));
    for (let k = 0; k < 24; k++) pen.glyph('|', 452 + k * 15, by + 64, 15, 44, k / 24 < fill ? C.bone : 'rgba(94,91,87,0.6)', 3);
    pen.flush();
    c.font = font(F.mono(700), 26); c.fillText(`${Math.round(fill * 100)}%`, 820 - 60, by + 104);
    // her face in the middle, like the old shooters
    // (a bust: head, shoulders, the top of the heart; she glances left and right now and then)
    c.save(); c.beginPath(); c.rect(880, by + 22, 160, 124); c.clip();
    const glance = Math.floor(t / 1.2) % 4, pw = 150;            // 0 front, 1 turned one way, 2 front, 3 the other way
    drawGirl(pen, glance % 2 ? 'q_front' : 'front', 0, 960 - pw / 2, by + 21, pw, { flip: glance === 3, knock: C.ink2 });
    pen.flush(); c.restore();
    c.font = font(F.mono(700), 40); c.fillStyle = C.bone; c.fillText('03', 1092, by + 108);
    c.font = font(F.mono(500), 18); c.fillStyle = C.ash; c.fillText('STUCK IN A LIE', 1180, by + 104);
    c.font = font(F.mono(700), 26); c.fillStyle = C.bone; c.fillText('[C] [L] [I] [C] [K]', 1532, by + 104);
    comp.draw(renderer, this.L.upload(), out);
    void hash;
    return { bloom: 0, halation: 0, ca: 0, grain: 0.035, vignette: 0.25, shake: [0, kick * 3] };
  }
}
