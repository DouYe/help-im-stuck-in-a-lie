// Builds the engine timeline from the edit (src/edit.ts): resolves each cut's time from the lyrics
// and the beat grid, merges consecutive cuts of the same mode into one entry (with cues), and overlaps
// neighbouring entries by the transition length so the incoming mode can blend the outgoing one.
import type { TimelineEntry } from './engine/engine';
import type { SceneClass } from './engine/scene';
import type { Lyrics } from './engine/lyrics';
import type { AudioData } from './engine/audio';
import { EDIT, EDIT_RANGE as RANGE, type When, type Cut } from './edit';

const modules = import.meta.glob<{ default: SceneClass }>('./scenes/*.ts');
const scene = (name: string) => () => {
  const m = modules[`./scenes/${name}.ts`];
  return m ? m() : Promise.reject(new Error(`mode not found: scenes/${name}.ts`));
};

export function resolveWhen(w: When, ly: Lyrics, au: AudioData): number {
  if ('t' in w) return w.t;
  if ('bar' in w) {
    const d = au.downbeats[w.bar];
    const base = d ?? au.timeOfBeat(au.beatAt(au.downbeats[0]!) + 4 * w.bar);
    return base + (w.beat ?? 0) * (60 / au.bpm);
  }
  // whole-line match first ("Stuck in a lie" must not match "Help, I'm stuck in a lie"), then substring
  const key = (x: string) => x.toLowerCase().replace(/[‘’']/g, "'").replace(/[^a-z0-9'\u4e00-\u9fff]+/g, ' ').trim();
  const exact = ly.lines.filter((l) => key(l.text) === key(w.line));
  const line = exact.length > (w.nth ?? 0) ? exact[w.nth ?? 0]! : ly.get(w.line, w.nth ?? 0);
  const s = line.words[0]!.start;
  if (w.exact) return s + (w.shiftBeats ?? 0) * (60 / au.bpm);
  // the last beat at/before the first word (a cut never lands after the word it introduces)
  return au.timeOfBeat(Math.floor(au.beatAt(s + 0.02)) + (w.shiftBeats ?? 0));
}

export function makeTimeline(ly: Lyrics, au: AudioData): TimelineEntry[] {
  const beat = 60 / au.bpm;
  const t0 = resolveWhen(RANGE.from, ly, au), t1 = resolveWhen(RANGE.to, ly, au);
  const cuts = EDIT.map((c, i) => ({ ...c, at: resolveWhen(c.when, ly, au), i })).sort((a, b) => a.at - b.at);
  // group consecutive cuts that pick the same mode (and don't ask for a transition) into one entry
  const groups: (typeof cuts)[] = [];
  for (const c of cuts) {
    const g = groups[groups.length - 1];
    if (g && g[0]!.mode === c.mode && !c.transition) g.push(c);
    else groups.push([c]);
  }
  const entries: TimelineEntry[] = [];
  groups.forEach((g, gi) => {
    const first = g[0]!, next = groups[gi + 1]?.[0];
    const cutIn = gi === 0 ? Math.min(first.at, t0) : first.at;
    const cutOut = next ? next.at : t1;
    const inLen = gi === 0 || first.transition === 'cut' ? 0 : (first.beats ?? 1) * beat;
    const outLen = !next || next.transition === 'cut' ? 0 : (next.beats ?? 1) * beat;
    const start = cutIn - inLen / 2, end = cutOut + outLen / 2;
    const cues = g.map((c, k) => ({ t: c.at, params: c.params ?? {}, index: k }));
    entries.push({
      id: `${gi}-${first.mode}`,
      load: scene(first.mode),
      start, end,
      params: {
        ...(first.params ?? {}), cues, cutTime: cutIn, cutOut,
        transition: first.transition ?? 'wave', focus: first.focus, entryIndex: gi,
      },
    });
  });
  return entries;
}

/** The render range from the edit (used by the render script's defaults). */
export function renderRange(ly: Lyrics, au: AudioData) {
  return { from: resolveWhen(RANGE.from, ly, au), to: resolveWhen(RANGE.to, ly, au) };
}
export type { Cut };
