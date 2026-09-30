// ============================================================================================
//  THE EDIT — pick an art mode for every stretch of the song.
//
//  Each cut says WHEN (a lyric line, a bar, or seconds) and WHICH MODE plays from there on.
//  Consecutive cuts that pick the same mode continue that mode (no transition) with new params;
//  a change of mode gets a transition automatically (any mode connects to any other).
//
//  when:  { line: "Make me real this time" }           first word of that line (snapped to the beat)
//         { line: "Stuck in a lie", nth: 1 }           the 2nd time that line is sung
//         { bar: 24 }  /  { bar: 24, beat: 2 }         a bar of the song, 0-based downbeat index (the HUD shows bar+1);
//                                                      chorus 1 starts at bar 17 = 42.01 s (see docs/LYRICS.md)
//         { t: 58.9 }                                  seconds
//  mode:  'maze'      a 3D labyrinth whose walls are lanes of flowing symbols; the lyric runs through it
//         'portrait'  the heroine, made of symbols  (params: assemble, awake, storm, cage, heart, wide, fadeOut)
//         'heart'     a heart made of rings of symbols, beating (params: burst)
//         'polygraph', 'cage'  (the first test's plates)
//         'help'      the whole screen red, one enormous word slams in (params: n: 1 | 2)
//         'tunnel'    rings of symbols rush at the camera, each sung word slams in the middle
//         'slam'      each sung word made of hundreds of symbols that assemble and blow apart
//         'storm'     full-screen bullet patterns of symbols, the words slam through them
//         'bars'      bars of symbols slam across on every word, the frame closes to a slit
//         'swarm'     a vortex of symbols (params: collapse, tail, fadeOut)
//  transition: 'wave' (default: a ring of symbols) | 'sweep' | 'dive' | 'fade' | 'cut'
//              | 'through' (zoom into the dark of the old picture, e.g. into a letter of HELP);  beats: length (default 1)
//
//  Several edits live here; pick one with ?edit=NAME in the preview URL or --edit NAME when rendering.
// ============================================================================================
export type When = { line: string; nth?: number; exact?: boolean; shiftBeats?: number } | { bar: number; beat?: number } | { t: number };
export interface Cut {
  when: When;
  mode: string;
  params?: Record<string, any>;
  transition?: 'wave' | 'sweep' | 'dive' | 'fade' | 'cut' | 'through';
  beats?: number;
  /** Where a 'dive' transition pushes in (0..1 of the frame). */
  focus?: [number, number];
}

/** The part of the song to render (the rest is not built). */
export const RANGE: { from: When; to: When } = { from: { bar: 15 }, to: { bar: 25 } };

const HEROINE: Cut[] = [
  // lead-in: the maze of symbols rises out of the floor while the pre-chorus ends
  { when: { bar: 15 }, mode: 'maze', params: { camera: 'overview' } },
  // "Help, I'm stuck in a lie": the lyric runs down the corridors and hits a dead end
  { when: { line: "Help, I'm stuck in a lie" }, mode: 'maze', params: { camera: 'run' } },
  // "Stuck in a lie": crane up — the walls rise, the maze is endless
  { when: { line: 'Stuck in a lie' }, mode: 'maze', params: { camera: 'rise' } },
  // "Make me real this time": symbols are fired in from everywhere and assemble HER
  { when: { line: 'Make me real this time' }, mode: 'portrait', params: { assemble: true } },
  { when: { line: 'Real this time' }, mode: 'portrait', params: { awake: true } },
  // second half: barrages of symbols tear through her, then bars of symbols lock her in
  { when: { line: "Help, I'm stuck in a lie", nth: 1 }, mode: 'portrait', params: { storm: true } },
  { when: { line: 'Stuck in a lie', nth: 1 }, mode: 'portrait', params: { cage: true } },
  // "I still got a heart inside": push into her chest — a heart made of symbols
  { when: { line: 'I still got a heart inside' }, mode: 'heart', transition: 'dive', focus: [0.56, 0.74] },
  { when: { line: 'Heart inside' }, mode: 'heart', params: { burst: true } },
  // the bar after the chorus: back out, the heart still glowing in her chest
  { when: { bar: 24 }, mode: 'portrait', params: { heart: true, wide: true, fadeOut: true }, transition: 'fade' },
];

// The chaotic cut: no heroine — everything moves; HELP turns the screen red and you fall into its letters.
const CHAOS: Cut[] = [
  { when: { bar: 15 }, mode: 'swarm', params: { collapse: true } },
  { when: { bar: 16 }, mode: 'help', params: { n: 1 }, transition: 'cut' },
  { when: { bar: 16, beat: 1 }, mode: 'tunnel', transition: 'through', beats: 0.5 },
  { when: { line: 'Stuck in a lie' }, mode: 'maze', params: { camera: 'plunge', slam: true }, transition: 'cut' },
  { when: { line: 'Make me real this time' }, mode: 'slam', transition: 'cut' },
  { when: { line: "Help, I'm stuck in a lie", nth: 1 }, mode: 'help', params: { n: 2 }, transition: 'cut' },
  { when: { bar: 20, beat: 1 }, mode: 'storm', transition: 'through', beats: 0.5 },
  { when: { line: 'Stuck in a lie', nth: 1 }, mode: 'bars', transition: 'cut' },
  { when: { line: 'I still got a heart inside' }, mode: 'heart', params: { chaos: true }, transition: 'cut' },
  { when: { line: 'Heart inside' }, mode: 'heart', params: { burst: true, explode: true } },
  { when: { bar: 24 }, mode: 'swarm', params: { tail: true, fadeOut: true }, transition: 'cut' },
];

// SEVEN: seven shots, seven art styles, one idea each, every cut on a beat. Ink, paper and orange only.
const SEVEN: Cut[] = [
  { when: { bar: 16 }, mode: 'poster' },                                                   // Help, I'm stuck in a lie
  { when: { line: 'Stuck in a lie' }, mode: 'engrave', transition: 'through', beats: 1 },   // Stuck in a lie
  { when: { line: 'Make me real this time' }, mode: 'sketch', transition: 'cut' },          // Make me real this time
  { when: { line: 'Real this time' }, mode: 'flap', transition: 'cut' },                    // Real this time
  { when: { line: "Help, I'm stuck in a lie", nth: 1 }, mode: 'tape', transition: 'cut' },  // Help… / Stuck in a lie
  { when: { line: 'I still got a heart inside' }, mode: 'xray', transition: 'cut' },        // I still got a heart inside
  { when: { line: 'Heart inside' }, mode: 'stitch', transition: 'cut' },                    // Heart inside (+ the bar after)
];

type Range = { from: When; to: When };
// GAME (work in progress): the girl made of symbols in a game world that keeps changing dimension.
const GAME: Cut[] = [
  { when: { bar: 15 }, mode: 'plat' },
];

// KEYS: the five keyframes of the game world (the girl, style 1).
const KEYS: Cut[] = [
  { when: { t: 35.5 }, mode: 'kf_plat', params: { variant: 'keys' } },
  { when: { line: "Help, I'm stuck in a lie" }, mode: 'kf_plat', params: { variant: 'help' } },
  { when: { line: 'Stuck in a lie' }, mode: 'kf_maze', transition: 'cut' },
  { when: { line: 'Make me real this time' }, mode: 'kf_ray', transition: 'cut' },
  { when: { line: 'I still got a heart inside' }, mode: 'kf_chaos', transition: 'cut' },
];

// MORE: keyframes v3 — more moments across the song (verse 1, pre-chorus, chorus 1), the girl bold and big.
// (Verse-1 lines are placeholders until the official lyrics are aligned; their text is typed in the scene.)
const MORE: Cut[] = [
  { when: { t: 0 }, mode: 'kf_more', params: { variant: 'boot' } },
  { when: { t: 16.4 }, mode: 'kf_more', params: { variant: 'labels' }, transition: 'cut' },
  { when: { t: 21.2 }, mode: 'kf_more', params: { variant: 'prompt' }, transition: 'cut' },
  { when: { t: 35.5 }, mode: 'kf_more', params: { variant: 'iso' }, transition: 'cut' },
  { when: { line: 'Stuck in a lie' }, mode: 'kf_more', params: { variant: 'cage' }, transition: 'cut' },
  { when: { line: 'Real this time' }, mode: 'kf_more', params: { variant: 'run' }, transition: 'cut' },
  { when: { line: "Help, I'm stuck in a lie", nth: 1 }, mode: 'kf_more', params: { variant: 'fall' }, transition: 'cut' },
  { when: { line: 'Heart inside' }, mode: 'kf_more', params: { variant: 'close' }, transition: 'cut' },
];

export const EDITS: Record<string, { cuts: Cut[]; range: Range }> = {
  heroine: { cuts: HEROINE, range: RANGE },
  chaos: { cuts: CHAOS, range: RANGE },
  seven: { cuts: SEVEN, range: { from: { bar: 16 }, to: { bar: 25 } } },
  game: { cuts: GAME, range: { from: { bar: 15 }, to: { bar: 26 } } },
  keys: { cuts: KEYS, range: { from: { t: 35.5 }, to: { bar: 26 } } },
  more: { cuts: MORE, range: { from: { t: 0 }, to: { bar: 26 } } },
};
const pick = typeof location !== 'undefined' ? new URLSearchParams(location.search).get('edit') : null;
export const EDIT_NAME = pick && EDITS[pick] ? pick : 'keys';   // default = the current work (keyframes v2)
export const EDIT: Cut[] = EDITS[EDIT_NAME]!.cuts;
export const EDIT_RANGE: Range = EDITS[EDIT_NAME]!.range;
