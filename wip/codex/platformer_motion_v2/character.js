/* Original symbol girl — articulated motion study, isolated from the locked rig.
 * Source silhouette: design/character/src/vgirl.py, side view; cell alphabet:
 * app/src/game/glyph.ts. All visible geometry is rastered to 17 x 27 symbols.
 * No bundler, assets, fonts, or random state. See character-notes-v2.md for API.
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
    const vy = Number.isFinite(state.vy) ? state.vy : (Number(state.moveY) || 0) * (state.swim ? 300 : 700);
    const ax = clamp((vx - hair.prevVx) / dt, -8000, 8000);
    const ay = clamp((vy - hair.prevVy) / dt, -16000, 16000);
    // Fast locomotion is not simulated by clamping the hair flat. Normalize to
    // the new speed range, reserve displacement for acceleration and landing.
    const maxSpeed = clamp(Number(state.maxSpeed) || 1320, 640, 2200);
    const water = !!state.swim, dash = clamp(Number(state.dashing) || 0, 0, 1);
    const tx = clamp(-vx / maxSpeed * (water ? .19 : .23) - ax / 160000
      - Math.sign(vx) * dash * .07, -.39, .39);
    const ty = state.topDown ? 0 : water
      ? clamp(vy / 2600 + ay / 160000, -.09, .22)
      : clamp(vy / 2400 + ay / 100000, -.11, .46);
    const n = Math.max(1, Math.ceil(dt / (1 / 120))), h = dt / n;
    for (let i = 0; i < n; i++) {
      hair.hxv += ((tx - hair.hx) * (water ? 36 : 58) - hair.hxv * (water ? 7.0 : 9.0)) * h;
      hair.liftv += ((ty - hair.lift) * (water ? 39 : 67) - hair.liftv * (water ? 7.0 : 8.4)) * h;
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
    const vy = Number.isFinite(state.vy) ? state.vy : (Number(state.moveY) || 0) * (state.swim ? 300 : 700);
    const swim = !!state.swim, dash = clamp(Number(state.dashing) || 0, 0, 1);
    const grounded = state.grounded !== false && !swim && dash < .05;
    const duck = clamp(Number(state.duck) || 0, 0, 1) * (1 - dash);
    const landing = clamp(Number(state.landing) || 0, 0, 1);
    const phase = Number.isFinite(state.runPhase) ? state.runPhase : time * TAU * Math.min(3.6, 1.1 + speed / 420);
    // Broad stylized sprint stride: 0.69 widths of floor travel in a stance.
    // At width 105 and vx 480 this gives ~130 px/cycle, ~3.7 Hz, not a tiny
    // rapid walk. Segment lengths change smoothly with speed, never by pose.
    const stride = .035 + .31 * moving;
    const bob = grounded ? -.015 * moving - .022 * moving * Math.cos(phase * 2) : -.025;
    const squash = .12 * landing;
    const headDy = bob + .36 * duck + squash;
    const hipDy = bob + .105 * duck + squash * .6;
    const lean = .055 * moving + .105 * duck;
    // Rotating a world-axis hair lag along with a 90-degree dash would send the
    // curtain upwards. Attenuate that local component; the long curtain itself
    // already trails behind the turned head along the dash direction.
    const hx = (state.hair ? state.hair.hx : clamp(-(state.vx || 0) / 1320 * .23, -.39, .39))
      * face * (1 - .9 * dash);
    const lift = state.hair ? state.hair.lift : clamp(vy / 2400, -.11, .46);
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
    if (dash > .05) {
      // Streamline: hands reach ahead after the body turns horizontal; feet tuck.
      farElbow = [shoulderX - .08, shoulderY - .06];
      farHand = [shoulderX - .065, shoulderY - .23];
      nearElbow = [shoulderX + .08, shoulderY - .04];
      nearHand = [shoulderX + .06, shoulderY - .25];
    } else if (swim) {
      const stroke = Math.sin(time * 5.2);
      farElbow = [shoulderX - .11, shoulderY + .10 + stroke * .05];
      farHand = [shoulderX - .14 - stroke * .025, shoulderY + .17 + stroke * .08];
      nearElbow = [shoulderX + .13, shoulderY + .07 - stroke * .06];
      nearHand = [shoulderX + .20, shoulderY - .01 - stroke * .06];
    } else if (grounded) {
      const swing = Math.sin(phase) * .12 * moving;
      farElbow = [shoulderX - .095 - swing, shoulderY + .16];
      farHand = [shoulderX + .005 - swing, shoulderY + .23 - moving * .065];
      nearElbow = [shoulderX + .07 + swing, shoulderY + .16];
      nearHand = [shoulderX + .155 + swing, shoulderY + .10];
    } else {
      const falling = smooth(clamp((vy + 70) / 650, 0, 1));
      farElbow = [shoulderX - .10, shoulderY + lerp(.10, -.055, falling)];
      farHand = [shoulderX - .16, shoulderY + lerp(.03, -.16, falling)];
      nearElbow = [shoulderX + .10, shoulderY + lerp(.04, -.09, falling)];
      nearHand = [shoulderX + .17, shoulderY + lerp(-.025, -.23, falling)];
    }
    add('far_arm', [shoulder, farElbow, farHand]);
    add('over', [shoulder, nearElbow, nearHand]);

    const leftHip = [hipX - .026, hemY - .015], rightHip = [hipX + .028, hemY - .005];
    let f0, f1;
    if (dash > .05) {
      f0 = [.44, 1.34]; f1 = [.67, 1.40];
    } else if (swim) {
      const kick = Math.sin(time * 6.0);
      f0 = [.47 - kick * .07, 1.39 - kick * .045];
      f1 = [.68 + kick * .065, 1.40 + kick * .04];
    } else if (grounded) {
      if (moving > .025) {
        f0 = footForPhase(phase, stride, duck, bob);
        f1 = footForPhase(phase + PI, stride, duck, bob);
      } else {
        f0 = [.53 - duck * .06, 1.47]; f1 = [.64 + duck * .05, 1.47];
      }
    } else {
      // Rise: trailing leg tucks high, lead leg forward. Fall: extend for landing.
      const falling = smooth(clamp((vy + 160) / 700, 0, 1));
      f0 = [lerp(.43, .50, falling), lerp(1.22, 1.43, falling)];
      f1 = [lerp(.74, .67, falling), lerp(1.27, 1.46, falling)];
    }
    const legReach = grounded ? moving : 0;
    const upper = .222 + .060 * legReach, lower = .225 + .060 * legReach;
    const k0 = knee(leftHip, f0, 1, upper, lower), k1 = knee(rightHip, f1, 1, upper, lower);
    add('far_leg', [leftHip, k0, f0]); add('far_leg', [f0, [f0[0] + .075, f0[1]]]);
    add('legs', [rightHip, k1, f1]); add('legs', [f1, [f1[0] + .075, f1[1]]]);
    let heart = [.58 + lean * .5, .68 + headDy * .65 + hipDy * .35];
    if (dash > .001 || swim) {
      // Keep the foot-based drawing contract. Dash rotates the intact symbol
      // silhouette to horizontal, rather than substituting a generic capsule.
      const turn = dash > .001 ? PI * .5 * smooth(dash)
        : .16 * Math.sin(time * 2.3) + clamp(vy / 650, -.20, .20);
      const pivot = [.575, 1.03], sn = Math.sin(turn), cs = Math.cos(turn);
      const transform = ([x, y]) => [pivot[0] + (x - pivot[0]) * cs - (y - pivot[1]) * sn,
        pivot[1] + (x - pivot[0]) * sn + (y - pivot[1]) * cs];
      for (const name of Object.keys(g)) g[name] = g[name].map(pl => pl.map(transform));
      heart = transform(heart);
    }
    return {g, heart, width, face, dashing: dash, swim};
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
    if (Number.isFinite(state.angle) && Math.abs(state.angle) > .0001) {
      ctx.translate(state.x || 0, state.y || 0);
      ctx.rotate(state.angle);
      ctx.translate(-(state.x || 0), -(state.y || 0));
    }
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

  // Original overhead view: a foreshortened version of the same crown, curtain,
  // closed eyes, dress and symbol heart. x/y is its centre, not a foot anchor.
  // Rotation follows movement; the two short eye strokes stay screen-horizontal
  // so the tiny character remains readable during turns through the maze.
  function drawTop(ctx, state, time = 0) {
    const width = state.width || 96;
    const vx = Number.isFinite(state.vx) ? state.vx : Number(state.moveX) || 0;
    const vy = Number.isFinite(state.vy) ? state.vy : Number(state.moveY) || 0;
    const moving = clamp(Math.hypot(vx, vy) / 240, 0, 1);
    const heading = Number.isFinite(state.angle) ? state.angle
      : Math.hypot(vx, vy) > 2 ? Math.atan2(vy, vx) + PI / 2
      : state.facing === -1 ? -PI / 2 : PI / 2;
    const phase = Number.isFinite(state.runPhase) ? state.runPhase : time * TAU * 3.2;
    const dash = clamp(Number(state.dashing) || 0, 0, 1);
    const swing = Math.sin(phase) * .045 * moving * (1 - dash);
    const hairLag = state.hair ? clamp(Math.hypot(state.hair.hx, state.hair.lift) * .30, 0, .13) : .06 * moving;
    const polys = [
      // The twin curtain edges and three pointed tips, not a generic round cap.
      [[.80, .25], [.78, .13], [.66, .07], [.49, .055], [.34, .08], [.23, .16], [.20, .30], [.20, .64 + hairLag], [.25, .87 + hairLag]],
      [[.25, .87 + hairLag], [.30, .92 + hairLag], [.35, .87 + hairLag], [.40, .91 + hairLag]],
      [[.40, .91 + hairLag], [.39, .69], [.35, .54], [.32, .37], [.36, .27], [.49, .23], [.64, .26], [.80, .25]],
      [[.80, .25], [.81, .52], [.79, .72 + hairLag], [.74, .90 + hairLag], [.69, .95 + hairLag], [.66, .88 + hairLag]],
      [[.66, .88 + hairLag], [.64, .68], [.66, .53]],
      // Face window and crown strands retain the accepted girl's landmarks.
      [[.36, .27], [.33, .35], [.34, .48], [.41, .55], [.59, .55], [.67, .48], [.69, .34], [.64, .26]],
      [[.37, .15], [.41, .21]], [[.53, .13], [.56, .21]],
      // Foreshortened neck, dress, elbows and feet; glyph strokes only.
      [[.43, .55], [.43, .59]], [[.57, .55], [.57, .59]],
      [[.38, .61], [.43, .58], [.57, .58], [.62, .61], [.60, .73], [.66, .86], [.34, .86], [.40, .73], [.38, .61]],
      [[.40, .73], [.60, .73]],
      [[.38, .62], [.28 - swing, .69], [.32 - swing, .79]],
      [[.62, .62], [.72 + swing, .69], [.68 + swing, .79]],
      [[.43, .86], [.43 - swing, 1.01], [.37 - swing, 1.01]],
      [[.57, .86], [.57 + swing, 1.04], [.64 + swing, 1.04]]
    ];
    const sn = Math.sin(heading), cs = Math.cos(heading), pivot = [.5, .56];
    const rotate = ([x, y]) => [pivot[0] + (x - pivot[0]) * cs - (y - pivot[1]) * sn,
      pivot[1] + (x - pivot[0]) * sn + (y - pivot[1]) * cs];
    const cells = raster(polys.map(pl => pl.map(rotate)));
    const cw = width * CW, ch = width * CH;
    const ox = (state.x || 0) - pivot[0] * width, oy = (state.y || 0) - pivot[1] * width;
    const lw = Math.max(2.15, ch * .34);
    ctx.save();
    ctx.globalAlpha *= state.opacity === undefined ? 1 : state.opacity;
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    const knock = state.knock === undefined ? INK : state.knock;
    if (knock) {
      const rows = new Map();
      for (const v of cells.values()) {
        let row = rows.get(v.r);
        if (!row) rows.set(v.r, [v.c, v.c]);
        else { row[0] = Math.min(row[0], v.c); row[1] = Math.max(row[1], v.c); }
      }
      ctx.fillStyle = knock;
      for (const [r, [c0, c1]] of rows) ctx.fillRect(ox + c0 * cw - 3, oy + r * ch - 2,
        (c1 - c0 + 1) * cw + 6, ch + 4);
    }
    ctx.strokeStyle = state.bone || BONE; ctx.lineWidth = lw; ctx.beginPath();
    for (const v of cells.values()) addGlyph(ctx, v.glyph, ox + v.c * cw, oy + v.r * ch, cw, ch);
    ctx.stroke();
    // The eye plate is kept upright in screen space at the rotated head centre.
    const eye = rotate([.50, .40]);
    const ex = ox + eye[0] * width, ey = oy + eye[1] * width;
    if (knock) { ctx.fillStyle = knock; ctx.fillRect(ex - cw * 1.7, ey - ch * .50, cw * 3.4, ch); }
    ctx.beginPath();
    addGlyph(ctx, '-', ex - cw * 1.45, ey - ch * .50, cw * 1.1, ch);
    addGlyph(ctx, '-', ex + cw * .35, ey - ch * .50, cw * 1.1, ch);
    ctx.stroke();
    if (!state.noHeart) {
      const heart = rotate([.50, .67]), hw = cw * .69, hh = ch * .55;
      const x0 = ox + heart[0] * width - hw * 2, y0 = oy + heart[1] * width - hh * 1.5;
      ctx.strokeStyle = state.heartColor || ORANGE; ctx.lineWidth = Math.max(1.55, hw * .42); ctx.beginPath();
      ['/\\/\\', '\\  /', ' \\/ '].forEach((row, r) => Array.from(row).forEach((glyph, c) => {
        if (glyph !== ' ') addGlyph(ctx, glyph, x0 + c * hw, y0 + r * hh, hw, hh);
      }));
      ctx.stroke();
    }
    ctx.restore();
    return {width, heading, moving, cells};
  }

  global.PlatformerCharacter = Object.freeze({draw, drawTop, pose, raster, createHair, updateHair,
    palette: Object.freeze({ink: INK, bone: BONE, orange: ORANGE}), grid: Object.freeze({cols: COLS, rows: ROWS})});
})(typeof window !== 'undefined' ? window : globalThis);
