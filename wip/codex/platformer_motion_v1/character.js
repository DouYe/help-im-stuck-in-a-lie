/* Original symbol girl — articulated motion study, isolated from the locked rig.
 * Source silhouette: design/character/src/vgirl.py, side view; cell alphabet:
 * app/src/game/glyph.ts. All visible geometry is rastered to 17 x 27 symbols.
 * No bundler, assets, fonts, or random state. See character-notes.md for API.
 */
(function (global) {
  'use strict';
  const PI = Math.PI, TAU = PI * 2;
  const INK = '#0A0A0B', BONE = '#EEE9DF', ORANGE = '#FF5314';
  const COLS = 17, ROWS = 27, CW = 1 / COLS, CH = 1.6 / ROWS;
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, u) => a + (b - a) * u;
  const smooth = u => u * u * (3 - 2 * u);
  const mod = (x, n) => ((x % n) + n) % n;
  const GLYPHS = {
    '|': [[[.5, .08], [.5, .92]]],
    '-': [[[.14, .5], [.86, .5]]],
    '_': [[[.06, .92], [.94, .92]]],
    '`': [[[.06, .08], [.94, .08]]],
    '/': [[[.18, .92], [.82, .08]]],
    '\\': [[[.18, .08], [.82, .92]]],
    '+': [[[.18, .5], [.82, .5]], [[.5, .18], [.5, .82]]],
    '>': [[[.2, .14], [.8, .5], [.2, .86]]],
    '<': [[[.8, .14], [.2, .5], [.8, .86]]],
    'o': [Array.from({length: 13}, (_, i) => [.5 + .3 * Math.cos(i * TAU / 12), .5 + .3 * Math.sin(i * TAU / 12)])]
  };

  function createHair(state = {}) {
    return {hx: 0, lift: 0, hxv: 0, liftv: 0,
      prevVx: state.vx || 0, prevVy: state.vy || 0, initialized: true};
  }

  // Call exactly once per fixed simulation step, including during jump/fall/land.
  // hx is a world-axis horizontal displacement in figure-width units.
  // Positive lift curls the curtain upward while falling. No teleport delta used.
  function updateHair(hair, state, dt) {
    if (!hair) return createHair(state);
    if (!(dt > 0)) return hair;
    dt = Math.min(dt, .05);
    const vx = Number.isFinite(state.vx) ? state.vx : 0;
    const vy = Number.isFinite(state.vy) ? state.vy : 0;
    const ax = clamp((vx - hair.prevVx) / dt, -8000, 8000);
    const ay = clamp((vy - hair.prevVy) / dt, -16000, 16000);
    const tx = clamp(-vx / 1400 - ax / 65000, -.36, .36);
    const ty = clamp(vy / 2400 + ay / 100000, -.11, .46);
    const n = Math.max(1, Math.ceil(dt / (1 / 120))), h = dt / n;
    for (let i = 0; i < n; i++) {
      hair.hxv += ((tx - hair.hx) * 58 - hair.hxv * 9.0) * h;
      hair.liftv += ((ty - hair.lift) * 67 - hair.liftv * 8.4) * h;
      hair.hx += hair.hxv * h;
      hair.lift += hair.liftv * h;
      hair.hx = clamp(hair.hx, -.48, .48);
      hair.lift = clamp(hair.lift, -.16, .58);
    }
    hair.prevVx = vx; hair.prevVy = vy;
    return hair;
  }

  // Two-bone IK. bend = 1 makes the knee fold forward in the right-facing rig.
  function knee(hip, foot, bend = 1, upper = .222, lower = .225) {
    let dx = foot[0] - hip[0], dy = foot[1] - hip[1];
    const raw = Math.hypot(dx, dy), d = clamp(raw, .025, upper + lower - .001);
    if (raw < 1e-8) { dx = 0; dy = 1; }
    const nx = dx / (raw || 1), ny = dy / (raw || 1);
    const along = (upper * upper - lower * lower + d * d) / (2 * d);
    const perp = Math.sqrt(Math.max(0, upper * upper - along * along));
    return [hip[0] + nx * along + ny * perp * bend, hip[1] + ny * along - nx * perp * bend];
  }

  function footForPhase(phase, stride, duck, bob) {
    const u = mod(phase / TAU, 1), contact = .56;
    let x, y;
    if (u < contact) {
      x = lerp(stride, -stride, u / contact);
      y = 1.47;
    } else {
      const v = (u - contact) / (1 - contact);
      x = lerp(-stride, stride, smooth(v));
      // Keep the ankle safely below the hip during recovery: a very high foot
      // pickup rotates two-bone IK sharply around the hip even with slow cadence.
      y = 1.47 - (.11 + stride * .32) * Math.sin(PI * v) * (1 - .55 * duck);
    }
    // Stance remains exactly on the floor; bob affects hip, never foot anchor.
    return [.575 + x, y];
  }

  function pose(state, time = 0) {
    const width = state.width || 116;
    const face = state.facing === -1 ? -1 : 1;
    const speed = Math.abs(state.vx || 0), moving = clamp(speed / 250, 0, 1);
    const grounded = state.grounded !== false;
    const duck = clamp(Number(state.duck) || 0, 0, 1);
    const landing = clamp(Number(state.landing) || 0, 0, 1);
    const phase = Number.isFinite(state.runPhase) ? state.runPhase : time * (4 + speed / 70);
    // Broad stylized sprint stride: 0.69 widths of floor travel in a stance.
    // At width 105 and vx 480 this gives ~130 px/cycle, ~3.7 Hz, not a tiny
    // rapid walk. Segment lengths change smoothly with speed, never by pose.
    const stride = .035 + .31 * moving;
    const bob = grounded ? -.015 * moving - .022 * moving * Math.cos(phase * 2) : -.025;
    const squash = .12 * landing;
    const headDy = bob + .36 * duck + squash;
    const hipDy = bob + .105 * duck + squash * .6;
    const lean = .055 * moving + .105 * duck;
    const hx = (state.hair ? state.hair.hx : clamp(-(state.vx || 0) / 1400, -.36, .36)) * face;
    const lift = state.hair ? state.hair.lift : clamp((state.vy || 0) / 2400, -.11, .46);
    const g = {}, add = (name, line) => (g[name] || (g[name] = [])).push(line);
    const H = ([x, y]) => [x + lean, y + headDy];
    // The crown, face, two closed-eye dashes, and dress proportions match side rig.
    // Only the hanging portion deforms; its roots stay attached to the scalp.
    const hairPoint = ([x, y]) => {
      const u = clamp((y - .25) / .58, 0, 1), w = u * u * (3 - 2 * u);
      return H([x + hx * w, y - lift * w]);
    };
    add('hair_out', [[.68, .24], [.66, .12], [.6, .05], [.5, .02], [.38, .04], [.28, .12], [.23, .26], [.22, .5], [.21, .8]].map(hairPoint));
    add('hair_out', [[.21, .8], [.26, .84], [.31, .8], [.36, .83]].map(hairPoint));
    add('hair_in', [[.36, .83], [.39, .6], [.43, .44], [.46, .3], [.52, .25], [.68, .24]].map(hairPoint));
    add('strands', [[.56, .12], [.54, .2]].map(H));
    add('strands', [[.44, .1], [.4, .2]].map(H));
    if (lift > .18) {
      const flutter = clamp(lift - .18, 0, .32);
      add('strands', [[.31, .085], [.27 + hx * .13, .055 - flutter * .25]].map(H));
    }
    add('face', [[.68, .24], [.69, .29], [.73, .34], [.69, .36], [.7, .4], [.67, .45], [.58, .47], [.5, .46]].map(H));
    add('eyes', [[.59, .31], [.64, .31]].map(H));
    add('neck', [H([.52, .47]), [.52 + lean * .65, .55 + headDy]]);
    add('neck', [H([.6, .47]), [.6 + lean * .65, .55 + headDy]]);
    const shoulderY = .56 + headDy, waistY = .8 + hipDy;
    const shoulderX = .57 + lean * .65, hipX = .575;
    add('body', [[.48, waistY], [.47 + lean * .65, shoulderY + .04], [.50 + lean * .65, shoulderY], [.62 + lean * .65, shoulderY], [.65 + lean * .65, shoulderY + .04], [.64, waistY]]);
    const hemY = 1.1 + hipDy;
    const hemSway = clamp(hx * -.045 + Math.sin(phase) * .014 * moving, -.03, .03);
    add('body', [[.48, waistY], [.4 + hemSway - duck * .045, hemY], [.75 + hemSway + duck * .045, hemY], [.64, waistY]]);
    add('body', [[.48, waistY], [.64, waistY]]);

    // Arms oppose the leg cycle, elbows bent; falling arms gradually recover up.
    let farElbow, farHand, nearElbow, nearHand;
    const shoulder = [shoulderX, shoulderY + .035];
    if (grounded) {
      const swing = Math.sin(phase) * .12 * moving;
      farElbow = [shoulderX - .095 - swing, shoulderY + .16];
      farHand = [shoulderX + .005 - swing, shoulderY + .23 - moving * .065];
      nearElbow = [shoulderX + .07 + swing, shoulderY + .16];
      nearHand = [shoulderX + .155 + swing, shoulderY + .10];
    } else {
      const falling = smooth(clamp(((state.vy || 0) + 70) / 650, 0, 1));
      farElbow = [shoulderX - .10, shoulderY + lerp(.10, -.055, falling)];
      farHand = [shoulderX - .16, shoulderY + lerp(.03, -.16, falling)];
      nearElbow = [shoulderX + .10, shoulderY + lerp(.04, -.09, falling)];
      nearHand = [shoulderX + .17, shoulderY + lerp(-.025, -.23, falling)];
    }
    add('far_arm', [shoulder, farElbow, farHand]);
    add('over', [shoulder, nearElbow, nearHand]);

    const leftHip = [hipX - .026, hemY - .015], rightHip = [hipX + .028, hemY - .005];
    let f0, f1;
    if (grounded) {
      if (moving > .025) {
        f0 = footForPhase(phase, stride, duck, bob);
        f1 = footForPhase(phase + PI, stride, duck, bob);
      } else {
        f0 = [.53 - duck * .06, 1.47]; f1 = [.64 + duck * .05, 1.47];
      }
    } else {
      // Rise: trailing leg tucks high, lead leg forward. Fall: extend for landing.
      const falling = smooth(clamp(((state.vy || 0) + 160) / 700, 0, 1));
      f0 = [lerp(.43, .50, falling), lerp(1.22, 1.43, falling)];
      f1 = [lerp(.74, .67, falling), lerp(1.27, 1.46, falling)];
    }
    const legReach = grounded ? moving : 0;
    const upper = .222 + .060 * legReach, lower = .225 + .060 * legReach;
    const k0 = knee(leftHip, f0, 1, upper, lower), k1 = knee(rightHip, f1, 1, upper, lower);
    add('far_leg', [leftHip, k0, f0]); add('far_leg', [f0, [f0[0] + .075, f0[1]]]);
    add('legs', [rightHip, k1, f1]); add('legs', [f1, [f1[0] + .075, f1[1]]]);
    return {g, heart: [.58 + lean * .5, .68 + headDy * .65 + hipDy * .35], width, face};
  }

  // Matches the original directional raster; negative hair/stride cells allowed.
  function raster(polys) {
    const acc = new Map();
    for (const pl of polys) for (let i = 1; i < pl.length; i++) {
      const [x0, y0] = pl[i - 1], [x1, y1] = pl[i];
      const n = Math.max(1, Math.floor(Math.hypot((x1 - x0) / CW, (y1 - y0) / CH) / .18));
      const angle = Math.atan2((y1 - y0) / CH, (x1 - x0) / CW);
      for (let j = 0; j <= n; j++) {
        const u = j / n, x = lerp(x0, x1, u), y = lerp(y0, y1, u);
        const c = Math.floor(x / CW), r = Math.floor(y / CH), key = r + ',' + c;
        let a = acc.get(key);
        if (!a) { a = [0, 0, 0, 0, r, c]; acc.set(key, a); }
        a[0] += Math.cos(2 * angle); a[1] += Math.sin(2 * angle);
        a[2] += y / CH - r; a[3]++;
      }
    }
    const out = new Map();
    for (const [key, a] of acc) {
      const coh = Math.hypot(a[0], a[1]) / a[3];
      const th = mod(Math.atan2(a[1], a[0]) * 90 / PI, 180), fy = a[2] / a[3];
      let glyph;
      if (coh < .12) glyph = '+';
      else if (th < 22 || th > 158) glyph = fy > .72 ? '_' : fy < .28 ? '`' : '-';
      else if (th > 68 && th < 112) glyph = '|';
      else glyph = th < 90 ? '\\' : '/';
      out.set(key, {r: a[4], c: a[5], glyph});
    }
    return out;
  }

  function addGlyph(ctx, glyph, x, y, cw, ch) {
    for (const poly of GLYPHS[glyph] || []) {
      poly.forEach(([u, v], i) => {
        if (i) ctx.lineTo(x + u * cw, y + v * ch);
        else ctx.moveTo(x + u * cw, y + v * ch);
      });
    }
  }

  function draw(ctx, state, time = 0) {
    const rig = pose(state, time), width = rig.width;
    const face = rig.face;
    const F = pl => pl.map(([x, y]) => [face === -1 ? 1 - x : x, y]);
    const lines = [];
    for (const [name, pls] of Object.entries(rig.g)) {
      if (name !== 'eyes' && name !== 'over') for (const pl of pls) lines.push(F(pl));
    }
    const cells = raster(lines);
    for (const [k, val] of raster((rig.g.over || []).map(F))) cells.set(k, val);
    const eyes = [];
    for (const line of rig.g.eyes || []) {
      const p = F(line), r = Math.floor(p[0][1] / CH), c = Math.floor((p[0][0] + p[1][0]) / 2 / CW);
      cells.delete(r + ',' + c); eyes.push({r, c, glyph: '-'});
    }
    const cw = width * CW, ch = width * CH;
    const anchorX = face === -1 ? .425 : .575;
    const ox = (state.x || 0) - anchorX * width, oy = (state.y || 0) - 1.47 * width;
    const lw = Math.max(2.4, ch * .32);
    ctx.save();
    ctx.globalAlpha *= state.opacity === undefined ? 1 : state.opacity;
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    const knock = state.knock === undefined ? INK : state.knock;
    if (knock) {
      const rows = new Map();
      for (const v of [...cells.values(), ...eyes]) {
        let row = rows.get(v.r);
        if (!row) rows.set(v.r, [v.c, v.c]);
        else { row[0] = Math.min(row[0], v.c); row[1] = Math.max(row[1], v.c); }
      }
      ctx.fillStyle = knock;
      const pad = Math.max(lw * .9, cw * .45);
      for (const [r, [c0, c1]] of rows) ctx.fillRect(ox + c0 * cw - pad, oy + r * ch - pad * .6, (c1 - c0 + 1) * cw + pad * 2, ch + pad * 1.2);
    }
    ctx.beginPath(); ctx.strokeStyle = state.bone || BONE; ctx.lineWidth = lw;
    for (const v of cells.values()) addGlyph(ctx, v.glyph, ox + v.c * cw, oy + v.r * ch, cw, ch);
    ctx.stroke();
    // Eyes last, above all hair/body strokes.
    ctx.beginPath();
    for (const e of eyes) addGlyph(ctx, e.glyph, ox + e.c * cw, oy + e.r * ch, cw, ch);
    ctx.stroke();
    if (!state.noHeart) {
      const hw = cw * .72, hh = ch * .58;
      const hx = face === -1 ? 1 - rig.heart[0] : rig.heart[0];
      const x0 = ox + hx * width - 2 * hw, y0 = oy + rig.heart[1] * width - 1.5 * hh;
      ctx.strokeStyle = state.heartColor || ORANGE;
      ctx.lineWidth = Math.max(1.6, Math.min(lw * .95, hw * .42));
      ctx.beginPath();
      const rows = ['/\\/\\', '\\  /', ' \\/ '];
      rows.forEach((row, r) => Array.from(row).forEach((glyph, c) => {
        if (glyph !== ' ') addGlyph(ctx, glyph, x0 + c * hw, y0 + r * hh, hw, hh);
      }));
      ctx.stroke();
    }
    ctx.restore();
    return rig;
  }

  global.PlatformerCharacter = Object.freeze({draw, pose, raster, createHair, updateHair,
    palette: Object.freeze({ink: INK, bone: BONE, orange: ORANGE}), grid: Object.freeze({cols: COLS, rows: ROWS})});
})(typeof window !== 'undefined' ? window : globalThis);
