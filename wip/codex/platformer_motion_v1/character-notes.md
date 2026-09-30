# Articulated symbol girl — motion study

This isolated module starts from the approved side-view silhouette in `design/character/src/vgirl.py` and the directional glyph raster in `app/src/game/girl.ts`. It preserves the 17×27 cell dimensions, bone lines, long outer/inner hair curtain, face window and one closed side-view eye dash, original dress, and symbol-only orange heart. It does not change either locked rig source.

## Canvas API

Load `character.js` as an ordinary script. It creates `window.PlatformerCharacter` (also `globalThis.PlatformerCharacter` in Node).

```js
const hair = PlatformerCharacter.createHair({vx: 0, vy: 0});
const girl = {x: 400, y: 720, width: 116, vx: 320, vy: 0,
  grounded: true, facing: 1, duck: 0, landing: 0, runPhase: 0, hair};

// In each FIXED physics step, once:
girl.runPhase += Math.abs(girl.vx) * dt / (girl.width * 1.232) * Math.PI * 2;
PlatformerCharacter.updateHair(hair, girl, dt);

// In each draw; does not mutate motion state:
PlatformerCharacter.draw(ctx, girl, simulationTime);
```

- `x,y`: world-space **foot anchor**, pixels; y points downward. Position the camera with the Canvas transform.
- `width`: figure coordinate box width; default 116. Box height is 1.6×width, original head is near y−1.45×width. Visible silhouette width is narrower than the box.
- `vx,vy`: world velocity in pixels/second. Positive `vy` means falling.
- `grounded`: default true; set false for all airborne frames.
- `facing`: +1 right or −1 left. Default +1. Rig, heart and hair mirror together.
- `runPhase`: radians, default derived from time/velocity. Advance from travelled distance for stable contact timing. `1.232×width` per cycle matches the full-speed sprint stance travel: ≈129.4 px at width 105, giving ≈3.7 Hz at 480 px/s. At slower speeds, use `stride = .035 + .31 * min(abs(vx)/250, 1)` and `cycleDistance = width * 2 * stride / .56`; this keeps the stance foot approximately fixed in world coordinates. Root integration may use a constant 130 px for the full-speed pass.
- `duck`: continuous 0..1; moves head/chest down, compresses legs and widens skirt. Ease state rather than toggling.
- `landing`: continuous 0..1 impact squash. Simulator can set on contact (`min(1, abs(preContactVy)/900)`) and decay over ≈0.15 seconds. Reset it on jump.
- `hair`: mutable spring object from `createHair`; update every fixed step. `hx` is world-axis offset in width units, `lift` is upward curl in width units. Do not negate `hx` on facing changes; renderer handles mirroring.
- Optional `opacity` (default 1), `knock` (default ink; false for ghosts, paper colour for light stages), `bone`, `heartColor`, `noHeart` for identical factory clones.

Other exports: `pose(state,time)` returns rig polyline groups in 1×1.6 coordinates; `raster(polys)` converts polylines to directional symbol cells. Palette and grid objects are read-only.

## Motion choices

The run is articulated: each leg uses two-bone inverse kinematics, a 56% stance phase with foot on the floor, a broad 0.345×width half-stride at sprint speed, a bent-knee swing phase, opposing elbow swing, modest head bob and forward lean. Thigh/calf lengths interpolate continuously from `.222/.225` to `.282/.285` figure-width units as running speed rises, allowing the broad stride without changing standing silhouette height. Jumping uses its own shorter limb reach, tucks the trailing leg; falling gradually extends legs for landing and lifts the arms. Landing compresses head/torso/hips while feet remain on their baseline.

Hair springs depend on velocity **and acceleration**, independently on horizontal trail and vertical lift. The hanging curtain bends from fixed scalp roots, visibly curls upward in a fall, and overshoots after landing. Spring integration subdivides to at most 1/120 seconds. Rendering is deterministic and has no random particle layer, bloom or glow.

Collision should be a separate gameplay capsule/box: start with half-width 0.22×width, height 1.30×width standing, ≈0.95×width crouching, foot anchor at `y`. Hair and skirt tips are visual and should not collide. Exact game tuning belongs to the simulator.

This is a proposed motion rig, not a replacement for the approved turnaround. Run/jump/duck choreography and hair dynamics require viewing in the final motion preview.

## Module validation

2026-09-30: Node syntax check passed. A synthetic 960-frame sequence exercised left/right facing, run, jump, fall, crouch and impact states at 120 Hz, with finite Canvas coordinates and finite springs throughout. At 300 px/s horizontal and 700 px/s downward speed after one second, the hair settled at `hx≈−0.212`, `lift≈0.288` figure-width units. This validates the numerical module; final visual QA belongs to the rendered preview.

Sprint revision: 2,401 phases spanning a complete 480 px/s ground cycle had thigh/calf length error below `4e−16`, consistently forward knees, and continuous limb coordinates. Swing pickup was reduced to `.11 + .32×stride` widths to keep the foot below the hip and halve the largest midpoint knee rotation. At width 105, cycle distance is 129.375 px and cadence 3.710 Hz. Airborne poses and physics remain independent of this sprint cadence.
