# Assembly Line Heart — 47–67 s code-rendered sample

This is an original 20-second procedural lyric video for the user-supplied recording. It follows the broad construction method of [pdoom-video](https://github.com/mexicat/pdoom-video): timed words and beat data drive deterministic frames, which are drawn in a browser and encoded with FFmpeg. The factory, press, corridor, and mechanical-heart imagery is new for this song.

## Build and preview

Requirements: Bun, Google Chrome, FFmpeg (`ffmpeg` on `PATH`).

```text
bun install
bun render.ts --still --t 6.4 --out still.png
bun render.ts --out assembly-line-heart-47-67.mp4
```

`index.html` loads the local fonts and `scene.js`. `window.drawAt(t)` draws any frame from a clip-relative time in seconds. `timing.json` contains the eight supplied lyric lines, word times, a 98.7543 BPM beat grid, and 60 Hz loudness energy. `render.ts` opens the page in headless Chrome, streams 1920×1080 RGBA frames over a local WebSocket to FFmpeg, and muxes the exact 47–67 second audio excerpt in `audio_47_67.flac`.

The first “Help” begins about 20 ms before the cut. The 60 ms “I” before “still” is an estimate because the alignment returned zero duration for that syllable. The other word boundaries are automatic alignment estimates and can be refined by ear.

The Archivo and IBM Plex Mono font files were copied from the reference repository, which identifies them as SIL Open Font License fonts. The recording belongs to its rights holder; including a local excerpt here does not grant distribution rights.
