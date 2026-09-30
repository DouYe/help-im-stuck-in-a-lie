# First 15 seconds: how this music video is made

This sample is a local render of [mexicat/pdoom-video](https://github.com/mexicat/pdoom-video) at commit `bdbad53`, using the repository's bundled recording and lyric timings. It reproduces the linked video's opening rather than introducing a new song or visual concept.

## What happens in the opening

| Time | Scene | Visual idea |
| --- | --- | --- |
| 0–9.328 s | `open` | A glowing orange spark plots a unicorn on a dark technical grid. Word-timed type enlarges “AGI”; the drawing turns into circuit traces as the lyrics continue. |
| 9.328–15 s | `loss` | A training-loss graph falls sharply, then becomes a 3D contour landscape. The camera follows the orange path while “SERVANT” fills the frame. |

The palette is near-black, warm white, and orange. Large Archivo lyrics sit over fine grid lines, tiny IBM Plex Mono labels, bloom, and grain.

## Rendering pipeline

1. `data/lyrics.json` supplies word and syllable times. `data/audio.json` supplies the 132 BPM beat grid, onsets, and loudness data. The Python analysis programs created these files; they are already committed and are not needed for this render.
2. `app/src/timeline.ts` places scene changes on the beat grid. For this excerpt it selects `open` and `loss`.
3. The TypeScript scenes draw each frame as a deterministic function of song time with Three.js, WebGL, and shader effects. The same scene code drives browser preview and offline export.
4. `app/scripts/render.ts` runs the Vite app in headless Chrome, sends raw frames to FFmpeg, and combines them with `audio/pdoom.mp3`.

This MP4 uses 1920×1080, 60 fps, four subframes per frame for motion blur, H.264 video, and AAC audio. On this Windows machine, Three.js asynchronous render-target readback caused export failure; the local working copy uses synchronous `readRenderTargetPixels` in `app/src/engine/engine.ts`. The one-line change is saved as [windows-readback.patch](windows-readback.patch).

To repeat the excerpt, apply the patch from the repository root, then run these commands in its `app` directory:

```text
git apply <path-to-windows-readback.patch>
cd app
bun install
bun scripts/render.ts video --from 0 --to 15 --only open,loss --fps 60 --samples 4 --shutter 0.2 --preset fast --crf 18 --out first_15s.mp4
```

The renderer starts Vite by invoking `bunx`. The Bun 1.4.2 Windows release ZIP contains only `bun.exe`; for this local run I copied it to `bunx.exe` in a project tool folder and temporarily put that folder on `PATH`.

The repository licenses its code under MIT, but explicitly excludes its bundled song and lyrics from that license. This render is a private proof of concept; publishing it requires rights to the recording and lyrics.
