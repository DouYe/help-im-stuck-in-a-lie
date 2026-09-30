// MODE 'maze' — the symbol maze: a 3D labyrinth whose walls are lanes of flowing symbols. Her voice is a
// glowing caret that runs the corridors while the line is sung; each word hangs in the air where it
// was sung. The path ends in a dead end whose walls read LIE.
// Cue params: camera: 'overview' (the maze rises out of the floor) | 'run' (chase the caret) | 'rise'
// (crane up while the walls grow on every sung word).
import * as THREE from 'three';
import type { Frame } from '../engine/scene';
import { Layer2D, W, H } from '../engine/gl';
import { LIN, rgba } from '../engine/palette';
import { F, font, measure } from '../engine/type';
import { clamp, ease, hash, lerp, mulberry32, smoothstep, frameIdx, keys, type Key } from '../engine/util';
import { Mode } from '../danmaku/mode';
import { drawLyric } from '../danmaku/lyric';
import { slamWord, wordText } from '../danmaku/kinetic';
import type { Word } from '../engine/lyrics';

const COLS = 15, ROWS = 11, CELL = 4, WALL_H = 3.2;
const OX = -(COLS * CELL) / 2, OZ = -(ROWS * CELL) / 2;
const ATLAS_ROWS = 16, ATLAS_W = 2048, ROW_PX = 64;
type V3 = THREE.Vector3;

// ------------------------------------------------------------------ maze
interface Maze { walls: { a: [number, number]; b: [number, number]; cells: number[] }[]; adj: number[][] }
function makeMaze(seed: number): Maze {
  const rnd = mulberry32(seed);
  const id = (c: number, r: number) => r * COLS + c;
  const open = new Set<string>();                // "a-b" for cells with no wall between
  const seen = new Array(COLS * ROWS).fill(false);
  const stack = [id(Math.floor(COLS / 2), Math.floor(ROWS / 2))];
  seen[stack[0]!] = true;
  while (stack.length) {
    const cur = stack[stack.length - 1]!;
    const c = cur % COLS, r = Math.floor(cur / COLS);
    const nb = [[c + 1, r], [c - 1, r], [c, r + 1], [c, r - 1]].filter(([x, y]) => x! >= 0 && y! >= 0 && x! < COLS && y! < ROWS && !seen[id(x!, y!)]);
    if (!nb.length) { stack.pop(); continue; }
    const [x, y] = nb[Math.floor(rnd() * nb.length)]!;
    const n = id(x!, y!);
    open.add(`${Math.min(cur, n)}-${Math.max(cur, n)}`);
    seen[n] = true; stack.push(n);
  }
  const adj: number[][] = Array.from({ length: COLS * ROWS }, () => []);
  for (const k of open) { const [a, b] = k.split('-').map(Number); adj[a!]!.push(b!); adj[b!]!.push(a!); }
  // wall segments (unit), then merged into runs along each line
  const walls: Maze['walls'] = [];
  const isOpen = (a: number, b: number) => open.has(`${Math.min(a, b)}-${Math.max(a, b)}`);
  // horizontal lines z = OZ + r*CELL, r = 0..ROWS
  for (let r = 0; r <= ROWS; r++) {
    let start = -1; let cells: number[] = [];
    for (let c = 0; c <= COLS; c++) {
      const wall = c < COLS && (r === 0 || r === ROWS || !isOpen(id(c, r - 1), id(c, r)));
      if (wall && start < 0) { start = c; cells = []; }
      if (wall) { if (r > 0) cells.push(id(c, r - 1)); if (r < ROWS) cells.push(id(c, r)); }
      if (!wall && start >= 0) { walls.push({ a: [OX + start * CELL, OZ + r * CELL], b: [OX + c * CELL, OZ + r * CELL], cells }); start = -1; }
    }
  }
  for (let c = 0; c <= COLS; c++) {
    let start = -1; let cells: number[] = [];
    for (let r = 0; r <= ROWS; r++) {
      const wall = r < ROWS && (c === 0 || c === COLS || !isOpen(id(c - 1, r), id(c, r)));
      if (wall && start < 0) { start = r; cells = []; }
      if (wall) { if (c > 0) cells.push(id(c - 1, r)); if (c < COLS) cells.push(id(c, r)); }
      if (!wall && start >= 0) { walls.push({ a: [OX + c * CELL, OZ + start * CELL], b: [OX + c * CELL, OZ + r * CELL], cells }); start = -1; }
    }
  }
  return { walls, adj };
}
const cellCenter = (i: number): [number, number] => [OX + (i % COLS + 0.5) * CELL, OZ + (Math.floor(i / COLS) + 0.5) * CELL];

/** From the centre, the path to a dead end about `want` cells away. */
function pickPath(m: Maze, want: number): number[] {
  const start = Math.floor(ROWS / 2) * COLS + Math.floor(COLS / 2);
  const prev = new Array(COLS * ROWS).fill(-1), dist = new Array(COLS * ROWS).fill(-1);
  dist[start] = 0; const q = [start];
  while (q.length) { const u = q.shift()!; for (const v of m.adj[u]!) if (dist[v] < 0) { dist[v] = dist[u] + 1; prev[v] = u; q.push(v); } }
  const ends = dist.map((d, i) => ({ d, i })).filter((x) => m.adj[x.i]!.length === 1 && x.i !== start);
  ends.sort((a, b) => Math.abs(a.d - want) - Math.abs(b.d - want));
  const path: number[] = [];
  for (let u = ends[0]!.i; u >= 0; u = prev[u]) path.push(u);
  return path.reverse();
}

// ------------------------------------------------------------------ text atlas for the walls
const PATTERNS = ['/\\/\\/\\/\\', '||·||·||·', '—·—·—·—·', '+-+-+-+-', '*·*·*·*·', '>>>>>>>>', '<<<<<<<<', '========', '::::::::',
  '////////', '\\\\\\\\', 'o·o·o·o·', '#·#·#·#·', 'x-x-x-x-', '|/-\\|/-\\', '<>·<>·<>'];
function makeAtlas(): THREE.CanvasTexture {
  const cv = document.createElement('canvas');
  cv.width = ATLAS_W; cv.height = ATLAS_ROWS * ROW_PX;
  const c = cv.getContext('2d')!;
  c.textBaseline = 'middle';
  for (let r = 0; r < ATLAS_ROWS; r++) {
    const special = r === ATLAS_ROWS - 1;
    let x = 10, k = 0;
    while (x < ATLAS_W - 40) {
      // runs of one pattern, broken by gaps: a lane of symbols
      const pat = special ? 'LIE' : PATTERNS[Math.floor(hash(r, k, 5) * PATTERNS.length)]!;
      const reps = special ? 1 : 1 + Math.floor(hash(r, k, 6) * 3);
      const txt = special ? pat : pat.repeat(reps);
      const fam = special ? F.archivo(125, 900) : F.mono(hash(r, k, 7) < 0.4 ? 700 : 500);
      const size = special ? 54 : 40;
      c.font = font(fam, size);
      const w = measure(txt, fam, size);
      if (x + w > ATLAS_W - 10) break;
      c.fillStyle = `rgba(255,255,255,${special ? 1 : 0.6 + 0.4 * hash(r, k, 8)})`;
      c.fillText(txt, x, r * ROW_PX + ROW_PX / 2 + 2);
      x += w + (special ? 60 : 24 + 60 * hash(r, k, 9));
      k++;
    }
  }
  const tex = new THREE.CanvasTexture(cv);
  tex.wrapS = THREE.RepeatWrapping; tex.minFilter = THREE.LinearMipmapLinearFilter; tex.anisotropy = 8;
  return tex;
}

const WALL_VS = /* glsl */ `
attribute float aS; attribute float aY; attribute float aLen; attribute float aRow; attribute float aSpeed; attribute float aSpecial; attribute float aDist;
uniform float hScale, rise, t;
varying float vS, vY, vLen, vRow, vSpeed, vSpecial, vDepth, vShow;
void main() {
  // the maze rises out of the floor, nearest the centre first
  float show = clamp((rise * 1.6 - aDist / 34.0) * 2.0, 0.0, 1.0);
  vec3 p = position;
  p.y *= hScale * show;
  vS = aS; vY = aY; vLen = aLen; vRow = aRow; vSpeed = aSpeed; vSpecial = aSpecial; vShow = show;
  vec4 mv = modelViewMatrix * vec4(p, 1.0);
  vDepth = -mv.z;
  gl_Position = projectionMatrix * mv;
}`;
const WALL_FS = /* glsl */ `
uniform sampler2D atlas; uniform float t, fogNear, fogFar, lie, fill, hScale;
uniform vec3 cInk, cWall, cText, cSig;
varying float vS, vY, vLen, vRow, vSpeed, vSpecial, vDepth, vShow;
void main() {
  float s = gl_FrontFacing ? vS : vLen - vS;
  float h = vY * ${WALL_H.toFixed(2)} * hScale;           // height in world units
  float laneH = 0.64;
  float lane = floor(h / laneH);
  float fy = fract(h / laneH);
  float row = vSpecial > 0.5 ? ${(ATLAS_ROWS - 1).toFixed(1)} : mod(vRow + lane * 5.0, ${(ATLAS_ROWS - 1).toFixed(1)});
  float dir = mod(lane, 2.0) < 0.5 ? 1.0 : -1.0;
  float stripLen = ${(ATLAS_W / ROW_PX).toFixed(1)} * laneH;
  float u = (s + t * vSpeed * dir) / stripLen;
  float v = 1.0 - (row + 0.92 - fy * 0.84) / ${ATLAS_ROWS.toFixed(1)};
  float a = texture2D(atlas, vec2(u, v)).a;
  // lanes of symbols fill in over the overview
  float filled = step(fract(sin(vRow * 12.9898 + lane * 78.233) * 43758.5453), fill);
  vec3 col = cWall;
  vec3 txt = vSpecial > 0.5 ? cSig * (1.2 + 2.5 * lie) : cText;
  col = mix(col, txt, a * filled);
  // lane gaps and the top rim
  col += cText * 0.25 * smoothstep(0.985, 1.0, vY) ;
  col *= 0.35 + 0.65 * vShow;
  float fog = smoothstep(fogNear, fogFar, vDepth);
  gl_FragColor = vec4(mix(col, cInk, fog), 1.0);
}`;
const FLOOR_FS = /* glsl */ `
uniform float headS, fogNear, fogFar, glow;
uniform vec3 cInk, cGrid, cSig;
uniform vec2 pts[40]; uniform int nPts;
varying vec3 vW; varying float vDepth;
float segD(vec2 p, vec2 a, vec2 b) { vec2 pa = p - a, ba = b - a; float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0); return length(pa - ba * h); }
void main() {
  vec2 p = vW.xz;
  vec2 q = fract((p - vec2(${OX.toFixed(1)}, ${OZ.toFixed(1)})) / 0.8) - 0.5;
  float dotm = 1.0 - smoothstep(0.06, 0.1, length(q));
  vec3 col = cInk + cGrid * 0.16 * dotm;
  // the caret's trail along the path, up to the head
  float d = 1e9;
  for (int i = 0; i < 39; i++) {
    if (i + 1 >= nPts) break;
    float s0 = float(i), s1 = float(i + 1);
    if (s0 > headS) break;
    vec2 a = pts[i], b = pts[i + 1];
    if (s1 > headS) b = mix(a, b, headS - s0);
    d = min(d, segD(p, a, b));
  }
  col += cSig * glow * (0.9 * exp(-d * 3.0) + 0.25 * exp(-d * 0.8));
  float fog = smoothstep(fogNear, fogFar, vDepth);
  gl_FragColor = vec4(mix(col, cInk, fog), 1.0);
}`;
const FLOOR_VS = /* glsl */ `
varying vec3 vW; varying float vDepth;
void main() { vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; vec4 mv = viewMatrix * w; vDepth = -mv.z; gl_Position = projectionMatrix * mv; }`;

export default class Maze3D extends Mode {
  scene3 = new THREE.Scene();
  cam = new THREE.PerspectiveCamera(52, W / H, 0.1, 400);
  wallMat!: THREE.ShaderMaterial;
  floorMat!: THREE.ShaderMaterial;
  maze!: Maze;
  path: number[] = [];
  pts: [number, number][] = [];
  head = new THREE.Mesh(new THREE.BoxGeometry(0.22, 2.4, 0.22), new THREE.MeshBasicMaterial({ color: new THREE.Color(4, 0.9, 1.6) }));
  headGlow = new THREE.Mesh(new THREE.BoxGeometry(0.6, 2.8, 0.6), new THREE.MeshBasicMaterial({ color: new THREE.Color(1.2, 0.18, 0.4), transparent: true, opacity: 0.35, depthWrite: false }));
  words: { w: Word; mesh: THREE.Mesh; s: number }[] = [];
  L = new Layer2D();
  sKeys: Key[] = [];
  deadEndT = 0;

  init() {
    this.maze = makeMaze(7);
    this.path = pickPath(this.maze, 11);
    this.pts = this.path.map(cellCenter);
    const deadEnd = this.path[this.path.length - 1]!;
    // ---- walls
    const pos: number[] = [], aS: number[] = [], aY: number[] = [], aLen: number[] = [], aRow: number[] = [], aSp: number[] = [], aSpec: number[] = [], aDist: number[] = [], idx: number[] = [];
    this.maze.walls.forEach((w, i) => {
      const [x0, z0] = w.a, [x1, z1] = w.b;
      const len = Math.hypot(x1 - x0, z1 - z0);
      const special = w.cells.includes(deadEnd) && len <= CELL * 1.01 ? 1 : 0;
      const row = Math.floor(hash(i, 3) * (ATLAS_ROWS - 1));
      const sp = (0.9 + 1.6 * hash(i, 4)) * (hash(i, 5) < 0.5 ? 1 : -1);
      const dist = Math.hypot((x0 + x1) / 2, (z0 + z1) / 2);
      const b = pos.length / 3;
      for (const [x, z, s, y] of [[x0, z0, 0, 0], [x1, z1, len, 0], [x1, z1, len, 1], [x0, z0, 0, 1]] as const) {
        pos.push(x, y * WALL_H, z); aS.push(s); aY.push(y); aLen.push(len); aRow.push(row); aSp.push(sp); aSpec.push(special); aDist.push(dist);
      }
      idx.push(b, b + 1, b + 2, b, b + 2, b + 3);
    });
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    for (const [n, a] of [['aS', aS], ['aY', aY], ['aLen', aLen], ['aRow', aRow], ['aSpeed', aSp], ['aSpecial', aSpec], ['aDist', aDist]] as const) g.setAttribute(n, new THREE.Float32BufferAttribute(a, 1));
    g.setIndex(idx);
    const v3 = (c: [number, number, number], k = 1) => new THREE.Vector3(c[0] * k, c[1] * k, c[2] * k);
    this.wallMat = new THREE.ShaderMaterial({
      vertexShader: WALL_VS, fragmentShader: WALL_FS, side: THREE.DoubleSide,
      uniforms: {
        atlas: { value: makeAtlas() }, t: { value: 0 }, hScale: { value: 1 }, rise: { value: 1 }, fill: { value: 1 }, lie: { value: 0 },
        fogNear: { value: 20 }, fogFar: { value: 90 },
        cInk: { value: v3(LIN.ink) }, cWall: { value: v3(LIN.ink2, 1.3) }, cText: { value: v3(LIN.bone, 1.05) }, cSig: { value: v3(LIN.signal) },
      },
    });
    this.scene3.add(new THREE.Mesh(g, this.wallMat));
    // ---- floor
    this.floorMat = new THREE.ShaderMaterial({
      vertexShader: FLOOR_VS, fragmentShader: FLOOR_FS,
      uniforms: {
        headS: { value: 0 }, glow: { value: 1 }, fogNear: { value: 20 }, fogFar: { value: 90 },
        cInk: { value: v3(LIN.ink) }, cGrid: { value: v3(LIN.ash) }, cSig: { value: v3(LIN.signal, 1.4) },
        pts: { value: Array.from({ length: 40 }, (_, i) => new THREE.Vector2(...(this.pts[Math.min(i, this.pts.length - 1)]!))) }, nPts: { value: this.pts.length },
      },
    });
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), this.floorMat);
    floor.rotation.x = -Math.PI / 2;
    this.scene3.add(floor, this.head, this.headGlow);

    // ---- head timing: slow during the lead-in, then the run; it reaches the dead end on the line's last word
    const runCue = this.cues.find((c) => c.params.camera === 'run' || c.params.camera === 'plunge');
    const lineWords = runCue ? this.wordsIn(runCue.t, this.cues.find((c) => c.t > runCue.t)?.t ?? this.ctx.end) : [];
    const lastW = lineWords[lineWords.length - 1];
    const N = this.path.length - 1;
    const tRun = runCue?.t ?? this.ctx.start + 1;
    this.deadEndT = lastW ? lastW.start : tRun + 1.5;
    this.sKeys = [[this.ctx.start, 0], [tRun, 1.6, ease.inOutCubic], [this.deadEndT, N, ease.inOutQuad]];

    // ---- sung words hang where the caret was when they were sung
    for (const w of this.wordsIn()) {
      const cv = document.createElement('canvas');
      const fam = F.archivo(100, 900), size = 110;
      const c = cv.getContext('2d')!;
      c.font = font(fam, size);
      const tw = Math.ceil(measure(w.w, fam, size)) + 40;
      cv.width = tw; cv.height = 160;
      c.font = font(fam, size); c.textBaseline = 'middle'; c.lineJoin = 'round';
      c.lineWidth = 16; c.strokeStyle = 'rgba(0,0,0,0.8)'; c.strokeText(w.w, 20, 84);
      c.fillStyle = rgba('signal', 1); c.fillText(w.w, 20, 84);
      const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
      const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, color: new THREE.Color(1.8, 1.8, 1.8) });
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(tw / 100, 1.6), mat);
      mesh.visible = false;
      this.scene3.add(mesh);
      this.words.push({ w, mesh, s: keys(w.start, this.sKeys) });
    }
  }

  /** Point along the path at s (in cells) and the smoothed direction. */
  at(s: number): { p: V3; d: V3 } {
    const N = this.pts.length - 1;
    const f = (x: number) => { const k = clamp(x, 0, N); const i = Math.min(N - 1, Math.floor(k)); const u = k - i; const a = this.pts[i]!, b = this.pts[i + 1]!; return new THREE.Vector3(lerp(a[0], b[0], u), 0, lerp(a[1], b[1], u)); };
    const p = f(s);
    const d = f(s + 0.9).sub(f(s - 0.6));
    if (d.lengthSq() < 1e-6) d.set(0, 0, 1);
    return { p, d: d.normalize() };
  }

  camFor(t: number, mode: string, since: number): { pos: V3; tgt: V3; up?: V3 } {
    const s = keys(t, this.sKeys);
    const { p, d } = this.at(s);
    const up = new THREE.Vector3(0, 1, 0);
    if (mode === 'overview') {
      const a = 0.6 + since * 0.12;
      const k = ease.inOutCubic(clamp(since / 2.6));
      // oblique orbit that closes in on the caret's start, ready for the run
      return { pos: new THREE.Vector3(Math.sin(a) * lerp(46, 24, k), lerp(34, 16, k), Math.cos(a) * lerp(46, 24, k)).add(new THREE.Vector3(p.x * k, 0, p.z * k)), tgt: new THREE.Vector3(p.x * (0.3 + 0.7 * k), 0, p.z * (0.3 + 0.7 * k)) };
    }
    if (mode === 'run') {
      if (t < this.deadEndT) return { pos: p.clone().addScaledVector(d, -9).add(new THREE.Vector3(0, 7.5, 0)), tgt: p.clone().addScaledVector(d, 5).add(new THREE.Vector3(0, 0.5, 0)) };
      // at the dead end: face the wall
      const k = ease.outCubic(clamp((t - this.deadEndT) / 0.5));
      const run = { pos: p.clone().addScaledVector(d, -9).add(new THREE.Vector3(0, 7.5, 0)), tgt: p.clone().addScaledVector(d, 5).add(new THREE.Vector3(0, 0.5, 0)) };
      const face = { pos: p.clone().addScaledVector(d, -5.5).add(new THREE.Vector3(0, 1.9, 0)), tgt: p.clone().addScaledVector(d, 3).add(new THREE.Vector3(0, 1.7, 0)) };
      return { pos: run.pos.lerp(face.pos, k), tgt: run.tgt.lerp(face.tgt, k) };
    }
    if (mode === 'plunge') {
      // fall out of the sky, spinning, while the caret runs below; land facing the dead end on the last word
      const runCue = this.cues.find((c) => c.params.camera === 'plunge')!;
      const k = ease.inOutCubic(clamp(since / Math.max(0.5, this.deadEndT - runCue.t)));
      const end = this.at(this.pts.length - 1);
      const face = { pos: end.p.clone().addScaledVector(end.d, -5.5).add(new THREE.Vector3(0, 1.9, 0)), tgt: end.p.clone().addScaledVector(end.d, 3).add(new THREE.Vector3(0, 1.7, 0)) };
      const push = t > this.deadEndT + 0.3 ? ease.inCubic(clamp((t - this.deadEndT - 0.3) / 1.2)) : 0;
      face.pos.addScaledVector(end.d, 4.2 * push);
      const topPos = new THREE.Vector3(p.x * 0.3, 82, p.z * 0.3);
      const pos = topPos.lerp(face.pos, k);
      const tgt = new THREE.Vector3(p.x, 0, p.z).lerp(face.tgt, k);
      const ang = since * 1.4;
      const u = new THREE.Vector3(Math.sin(ang) * (1 - k), k, Math.cos(ang) * (1 - k)).normalize();
      return { pos, tgt, up: u };
    }
    // rise: crane straight up from the dead end, spinning, until the maze is a pattern
    const k = ease.inOutCubic(clamp(since / 2.2));
    const pos = p.clone().addScaledVector(d, lerp(-5.5, -2, k)).add(new THREE.Vector3(0, lerp(1.9, 78, k), 0));
    const tgt = p.clone().addScaledVector(d, lerp(3, 0, k)).add(new THREE.Vector3(0, lerp(1.7, 0, k), 0));
    const ang = since * 0.5;
    up.set(Math.sin(ang) * k, 1 - k * 0.999, Math.cos(ang) * k).normalize();
    return { pos, tgt, up };
  }

  draw(f: Frame, out: THREE.WebGLRenderTarget) {
    const { renderer, comp, audio, lyrics } = this.ctx;
    const t = f.t;
    const { cue, since } = this.cue(t);
    const mode = this.param<string>(t, 'camera', 'overview');
    // camera: blend from the previous cue's framing over half a second
    let cam = this.camFor(t, mode, since);
    const prevCue = this.cues[this.cues.indexOf(cue) - 1];
    if (prevCue && since < 0.55) {
      const pc = this.camFor(t, prevCue.params.camera ?? 'overview', t - prevCue.t);
      const k = ease.inOutCubic(since / 0.55);
      cam = { pos: pc.pos.lerp(cam.pos, k), tgt: pc.tgt.lerp(cam.tgt, k), up: cam.up ? (pc.up ?? new THREE.Vector3(0, 1, 0)).lerp(cam.up, k).normalize() : pc.up };
    }
    this.cam.position.copy(cam.pos);
    this.cam.up.copy(cam.up ?? new THREE.Vector3(0, 1, 0));
    this.cam.lookAt(cam.tgt);
    const kick = audio.hit('kick', t, 0.1);
    this.cam.fov = 52 + 3 * kick; this.cam.updateProjectionMatrix();

    // walls: rise at the start, grow on every word of the 'rise' cue
    const riseCue = this.cues.find((c) => c.params.camera === 'rise');
    let hs = 1;
    if (riseCue) for (const [i, w] of this.wordsIn(riseCue.t, this.ctx.end).entries()) hs += 1.1 * ease.outExpo(clamp((t - w.start) / 0.25)) * (i === 3 ? 1.6 : 1);
    this.wallMat.uniforms.hScale!.value = hs;
    this.wallMat.uniforms.rise!.value = ease.outCubic(clamp((t - this.ctx.start + 0.3) / 2.0));
    this.wallMat.uniforms.fill!.value = clamp((t - this.ctx.start) / 1.8);
    this.wallMat.uniforms.t!.value = t;
    const lieW = this.wordsIn().filter((w) => w.start <= t + 0.02).pop();
    this.wallMat.uniforms.lie!.value = lieW && /lie/i.test(lieW.w) ? Math.exp(-(t - lieW.start) * 3) + 0.4 : 0.15;
    this.wallMat.uniforms.fogFar!.value = mode === 'rise' ? 160 : 90;
    this.floorMat.uniforms.fogFar!.value = mode === 'rise' ? 160 : 90;
    const s = keys(t, this.sKeys);
    this.floorMat.uniforms.headS!.value = s;
    const { p, d } = this.at(s);
    this.head.position.set(p.x, 1.25, p.z); this.headGlow.position.copy(this.head.position);
    const blink = t > this.deadEndT ? 0.55 + 0.45 * Math.round(0.5 + 0.5 * Math.sin(t * 9)) : 1;
    (this.head.material as THREE.MeshBasicMaterial).color.setRGB(4 * blink, 0.9 * blink, 1.6 * blink);
    for (const w of this.words) {
      const on = t >= w.w.start - 0.03;
      w.mesh.visible = on;
      if (!on) continue;
      const q = this.at(w.s);
      const k = t - w.w.start;
      const pop = 1 + 0.35 * Math.exp(-k * 12);
      w.mesh.position.set(q.p.x, 3.1 + 0.25 * Math.sin(k * 2 + w.s), q.p.z);
      w.mesh.quaternion.copy(this.cam.quaternion);
      w.mesh.scale.setScalar(pop * (mode === 'rise' ? 1 + 3 * ease.inCubic(clamp((since - 0.6) / 1.6)) : 1));
    }
    void d;
    renderer.setRenderTarget(out);
    renderer.setClearColor(new THREE.Color().setRGB(LIN.ink[0], LIN.ink[1], LIN.ink[2], THREE.LinearSRGBColorSpace), 1);
    renderer.clear(true, true, true);
    renderer.render(this.scene3, this.cam);

    // screen layer: her line pinned at the bottom
    const c = this.L.ctx; this.L.clear();
    if (this.param(t, 'slam', false)) {
      const cur = this.wordsIn().filter((w) => t >= w.start - 0.02).pop();
      if (cur) {
        const word = wordText(cur.w);
        const hot = /lie/i.test(word);
        const held = cur.end - cur.start > 0.45;
        const st = held ? clamp((t - cur.start) / Math.max(0.2, cur.end - cur.start)) : 0;
        slamWord(c, word, W / 2, H / 2, { size: 320, age: t - cur.start, color: hot ? rgba('signal', 1) : rgba('bone', 1), echoes: 3, echoColor: hot ? rgba('signal', 1) : rgba('bone', 1), jitter: hot ? 0.8 : 0.15, stretch: st * 0.6, alpha: held ? 1 : clamp((cur.end + 0.3 - t) / 0.2), t });
      }
    } else drawLyric(c, lyrics, t, { y: H - 70, size: 58 });
    comp.draw(renderer, this.L.upload(), out);

    const dead = t >= this.deadEndT && (mode === 'run' || mode === 'plunge') ? Math.exp(-(t - this.deadEndT) * 7) : 0;
    const sh = 18 * dead + 4 * kick;
    return {
      bloom: 0.6, grain: 0.05, vignette: 0.5,
      shake: [(hash(frameIdx(t), 1) - 0.5) * sh, (hash(frameIdx(t), 2) - 0.5) * sh],
      flash: 0.35 * dead,
    };
  }
}
void smoothstep;
