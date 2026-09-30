# Overhead symbol maze — motion test v2

`topdown.js` exports `window.TopdownScene = { draw, drawForeground, walls, route, spawn, bounds }`.

Both draw functions accept `{ time, localTime, p, cam, width, height }`, own the camera transform (`translate(width/2, height*570/1080); scale(cam.zoom); translate(-cam.x, -cam.y)`), and restore the context. The root renderer draws the heroine between the two calls. This module does not draw or mutate the heroine or simulation state.

- Bounds: `{x:0, y:0, w:3400, h:2300}`.
- Spawn: `{x:480, y:1700}`.
- Route: `[[480,1700],[1400,1700],[1400,1020],[780,1020],[780,420],[1600,420],[1600,760],[1930,760]]`.
- Length: 4,310 px, about 3.92 s at 1,100 px/s. Its turns are right, up, left, up, right, down, right.
- Walls: ordinary `{x,y,w,h}` rectangles; grid slabs exclude the route's 280 px wide corridors and larger room openings. All route segments have at least 140 px nominal wall clearance before cell expansion of the opening.

Five visual planes: a slow distant code atlas, a pulsing floor of glyph dots and score notation, raised symbol walls with offset side shadows, the root's heroine, and two translucent overhead music conduits. The latter briefly fly past at a faster rate than the underlying map. Black, white and grey only; orange remains reserved for the heroine's heart.

Rooms show a reset/AI memory buffer, a five-line music score, an overhead piano keyboard, and a thick `REAL` doorway. Scene labels are English. The floor sequencer arrows are architecture and should not be treated as enemies or an actor trail.

The fast route is intended for film choreography; root owns manual collision, hazards and snap movement. Hard scene cuts remain root-owned. New files only; previous art and video packages are preserved.
