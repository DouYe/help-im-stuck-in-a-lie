// Universal transitions: connect ANY two art modes. The incoming mode renders into its own target,
// the outgoing one arrives as `under`; these passes blend them. They work on arbitrary pictures, so
// any pair of modes, in any order, gets a transition for free. No text: only symbols.
//
//  'wave' (default) — a ring of bright symbols expands from a focus point; ahead of it the old picture
//          breaks into symbols (— | / \ ·), behind it the new picture resolves out of symbols.
//  'sweep' — the same, with a ragged straight front travelling right→left, lane by lane.
//  'dive'  — push into a focus point: the old picture scales up toward it and breaks into symbols,
//          the new one resolves from the centre outward.
//  'fade'  — crossfade through symbols (both pictures symbolised at the midpoint).
//  'cut'   — hard cut at the midpoint.
//  'through' — zoom into the outgoing picture at the focus point; its DARK areas become windows onto
//          the incoming picture (zoom into a black letter on a red screen and come out the other side).
import * as THREE from 'three';
import { FSPass, W, H } from '../engine/gl';
import { hash, clamp, ease } from '../engine/util';

export type TransitionKind = 'wave' | 'sweep' | 'dive' | 'fade' | 'cut' | 'through';

export const LANE_H = 54;
const LANES = Math.ceil(H / LANE_H);
const DELAY = 0.35;

/** Front (left edge of the symbol band) of a sweep lane at progress p. */
export function sweepFront(lane: number, p: number, seed = 1) {
  const h1 = hash(lane, seed * 13 + 1), h2 = hash(lane, seed * 13 + 2);
  const q = ease.inOutCubic(clamp((p - h1 * DELAY) / (1 - DELAY)));
  const band = 220 + 520 * h2;
  const xf = W + 80 + (-(band + 160) - (W + 80)) * q;
  return { xf, band };
}

const GLYPH_GLSL = /* glsl */ `
float lum(vec3 c) { return dot(c, vec3(0.2126, 0.7152, 0.0722)); }
float segD(vec2 p, vec2 a, vec2 b) { vec2 pa = p - a, ba = b - a; float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0); return length(pa - ba * h); }
float hash2(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
// The picture in 'tex' redrawn as a grid of symbols (cells of 12 x 22 logical px): edges become
// strokes along their direction, flat light areas become dots; each symbol keeps the colour under it.
vec3 glyphify(sampler2D tex, vec2 px, float boost) {
  vec2 cell = vec2(12.0, 22.0);
  vec2 ci = floor(px / cell);
  vec2 c0 = (ci + 0.5) * cell;
  vec2 uv0 = vec2(c0.x / ${W.toFixed(1)}, 1.0 - c0.y / ${H.toFixed(1)});
  vec2 d = vec2(cell.x / ${W.toFixed(1)}, cell.y / ${H.toFixed(1)});
  vec3 cc = texture(tex, uv0).rgb;
  float l = lum(cc);
  float lx = lum(texture(tex, uv0 + vec2(d.x, 0.0)).rgb) - lum(texture(tex, uv0 - vec2(d.x, 0.0)).rgb);
  float ly = lum(texture(tex, uv0 - vec2(0.0, d.y)).rgb) - lum(texture(tex, uv0 + vec2(0.0, d.y)).rgb); // y down
  vec2 g = vec2(lx, ly);
  float gm = length(g);
  vec2 u = (px - c0) / cell.y;
  float aa = 1.5 / cell.y;
  float ink = 0.0;
  if (gm > 0.05 + 0.2 * l) {
    float ang = atan(g.y, g.x) + 1.5707963;
    float k = mod(floor(ang / 0.7853982 + 0.5), 4.0);
    vec2 dir = k < 0.5 ? vec2(1.0, 0.0) : k < 1.5 ? vec2(0.7071, 0.7071) : k < 2.5 ? vec2(0.0, 1.0) : vec2(-0.7071, 0.7071);
    dir *= vec2(0.27, 0.36);
    ink = 1.0 - smoothstep(0.045, 0.045 + aa, segD(u, -dir, dir));
  } else if (l > 0.035) {
    float r = mix(0.05, 0.11, clamp(l * 2.0, 0.0, 1.0));
    ink = 1.0 - smoothstep(r, r + aa, length(u));
  }
  float bright = max(l, 0.12);
  return (cc / max(l, 1e-3)) * bright * boost * ink;
}
// A band of bright symbols (the front itself): each cell a mark oriented along 'ang'.
vec3 symbolBand(vec2 px, float ang, float t, float k) {
  vec2 cell = vec2(12.0, 22.0);
  vec2 ci = floor(px / cell);
  vec2 c0 = (ci + 0.5) * cell;
  vec2 u = (px - c0) / cell.y;
  float h = hash2(ci + floor(t * 20.0));
  float aa = 1.5 / cell.y;
  float ink;
  vec2 dir = vec2(cos(ang), sin(ang)) * vec2(0.3, 0.36);
  if (h < 0.45) ink = 1.0 - smoothstep(0.05, 0.05 + aa, segD(u, -dir, dir));
  else if (h < 0.7) ink = max(1.0 - smoothstep(0.05, 0.05 + aa, segD(u, vec2(-0.2, 0.0), vec2(0.2, 0.0))), 1.0 - smoothstep(0.05, 0.05 + aa, segD(u, vec2(0.0, -0.26), vec2(0.0, 0.26))));
  else if (h < 0.9) ink = 1.0 - smoothstep(0.09, 0.09 + aa, length(u));
  else ink = 0.0;
  vec3 c = hash2(ci * 1.7) < 0.14 ? C_SIGNAL * 2.4 : C_BONE * 1.5;
  return c * ink * k;
}`;

export class Transitions {
  pass = new FSPass(/* glsl */ `
    uniform sampler2D A, B;
    uniform float p, kind, t;
    uniform vec2 focus;
    uniform vec2 fronts[${LANES}];
    ${GLYPH_GLSL}
    void main() {
      vec2 px = FRAG_PX; px.y = ${H.toFixed(1)} - px.y;      // logical px, y down
      vec2 uv = vUv;
      vec3 a = texture(A, uv).rgb, b = texture(B, uv).rgb;
      vec3 col;
      if (kind < 0.5) {                                       // wave: a ring of symbols from the focus
        vec2 f = vec2(focus.x * ${W.toFixed(1)}, (1.0 - focus.y) * ${H.toFixed(1)});
        float r = length(px - f);
        float R = mix(-120.0, 2300.0, p < 0.5 ? 2.0 * p * p : 1.0 - pow(-2.0 * p + 2.0, 2.0) / 2.0);
        float jag = 60.0 * (hash2(vec2(floor(atan(px.y - f.y, px.x - f.x) * 24.0), 3.0)) - 0.5);
        float d = r - (R + jag);                              // <0 inside (new), >0 outside (old)
        float preA = 1.0 - smoothstep(20.0, 380.0, d);
        float postB = smoothstep(-380.0, -20.0, d);
        vec3 outside = mix(a, glyphify(A, px, 1.4), preA);
        vec3 inside = mix(b, glyphify(B, px, 1.4), postB);
        float band = 1.0 - smoothstep(0.0, 70.0, abs(d));
        float ang = atan(px.y - f.y, px.x - f.x) + 1.5707963;
        col = (d > 0.0 ? outside : inside) * (1.0 - band * 0.7) + symbolBand(px, ang, t, band);
      } else if (kind < 1.5) {                                // sweep
        int lane = int(floor(px.y / ${LANE_H.toFixed(1)}));
        vec2 fr = fronts[clamp(lane, 0, ${LANES - 1})];
        float xf = fr.x, bandW = fr.y;
        float preA = smoothstep(xf - 420.0, xf - 20.0, px.x);
        float postB = 1.0 - smoothstep(xf + bandW + 20.0, xf + bandW + 420.0, px.x);
        vec3 left = mix(a, glyphify(A, px, 1.4), preA);
        vec3 right = mix(b, glyphify(B, px, 1.4), postB);
        vec3 mid = glyphify(B, px, 0.5) + symbolBand(px, 0.0, t, 1.0);
        col = px.x < xf ? left : (px.x > xf + bandW ? right : mid);
      } else if (kind < 2.5) {                                // dive
        vec2 f = focus;
        float z = 1.0 + 9.0 * pow(p, 2.2);
        vec2 ua = (uv - f) / z + f;
        vec3 az = texture(A, ua).rgb;
        vec2 pxa = vec2(ua.x * ${W.toFixed(1)}, (1.0 - ua.y) * ${H.toFixed(1)});
        az = mix(az, glyphify(A, pxa, 1.1), smoothstep(0.45, 0.8, p) * 0.8);
        float r = length((uv - f) * vec2(${(W / H).toFixed(4)}, 1.0));
        float reveal = smoothstep(0.35, 1.0, p) * 1.6;
        float m = 1.0 - smoothstep(reveal - 0.25, reveal, r);
        vec3 bb = mix(glyphify(B, px, 1.3), b, smoothstep(0.75, 1.0, p));
        col = mix(az * (1.0 - smoothstep(0.55, 0.95, p)), bb, m);
      } else if (kind < 3.5) {                                // fade through symbols
        float g = 1.0 - abs(p - 0.5) * 2.0;
        vec3 aa2 = mix(a, glyphify(A, px, 1.2), smoothstep(0.0, 1.0, g));
        vec3 bb2 = mix(b, glyphify(B, px, 1.2), smoothstep(0.0, 1.0, g));
        col = mix(aa2, bb2, smoothstep(0.35, 0.65, p));
      } else if (kind < 4.5) {                                // cut
        col = p < 0.5 ? a : b;
      } else {                                                // through: zoom into A, fall into its dark
        vec2 f = focus;
        float e = p * p * (3.0 - 2.0 * p);
        float z = exp(mix(0.0, 3.9, pow(e, 1.35)));           // up to ~50x
        vec2 ua = (uv - f) / z + f;
        vec3 az = texture(A, ua).rgb;
        float hole = 1.0 - smoothstep(0.04, 0.22, lum(az));   // ink = window
        float zb = mix(0.35, 1.0, smoothstep(0.2, 1.0, e));   // B grows out of the hole
        vec3 bz = texture(B, (uv - f) / zb + f).rgb;
        col = mix(az, bz, hole * smoothstep(0.3, 0.7, e));
        col = mix(col, b, smoothstep(0.85, 1.0, p));
      }
      fragColor = vec4(col, 1.0);
    }`, { A: { value: null }, B: { value: null }, p: { value: 0 }, kind: { value: 0 }, t: { value: 0 }, focus: { value: new THREE.Vector2(0.5, 0.5) }, fronts: { value: Array.from({ length: LANES }, () => new THREE.Vector2()) } });

  /** Blend `a` (outgoing) into `b` (incoming) at progress p (0..1) into `out`. */
  render(renderer: THREE.WebGLRenderer, a: THREE.Texture, b: THREE.Texture, out: THREE.WebGLRenderTarget, p: number, kind: TransitionKind, t: number, o: { seed?: number; focus?: [number, number] } = {}) {
    const seed = o.seed ?? 1;
    this.pass.u.A!.value = a; this.pass.u.B!.value = b;
    this.pass.u.p!.value = p; this.pass.u.t!.value = t;
    this.pass.u.kind!.value = kind === 'wave' ? 0 : kind === 'sweep' ? 1 : kind === 'dive' ? 2 : kind === 'fade' ? 3 : kind === 'cut' ? 4 : 5;
    const f = o.focus ?? [0.5, 0.5];
    (this.pass.u.focus!.value as THREE.Vector2).set(f[0], 1 - f[1]);
    const fr = this.pass.u.fronts!.value as THREE.Vector2[];
    for (let i = 0; i < LANES; i++) { const { xf, band } = sweepFront(i, p, seed); fr[i]!.set(xf, band); }
    this.pass.render(renderer, out);
  }
}
