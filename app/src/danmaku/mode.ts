// Base class for pickable "art modes". A mode:
//  - draws whatever lyrics fall inside its window (it never assumes which line it gets), so the edit
//    (src/edit.ts) can put any mode on any stretch of the song;
//  - receives a list of CUES (the edit's consecutive cuts that picked this same mode, merged into one
//    entry): cue(t) tells it which variant is active and since when;
//  - connects to whatever mode came before through a universal transition (see transition.ts).
import * as THREE from 'three';
import { Scene, type Frame, type PostOverrides } from '../engine/scene';
import { makeRT } from '../engine/gl';
import type { Line, Word } from '../engine/lyrics';
import { Transitions, type TransitionKind } from './transition';

export interface Cue { t: number; params: Record<string, any>; index: number }

let SHARED: Transitions | null = null;
/** Where a mode wants the next transition to push in (e.g. the stem of a letter), by entry index. */
export const EXIT_FOCUS = new Map<number, [number, number]>();

export abstract class Mode extends Scene {
  override handlesTransition = true;
  private inner: THREE.WebGLRenderTarget | null = null;

  /** Cues of this entry, sorted by time (at least one, at the entry's own cut). */
  get cues(): Cue[] {
    const c = (this.ctx.params.cues as Cue[] | undefined) ?? [{ t: this.ctx.start, params: this.ctx.params, index: 0 }];
    return c;
  }
  /** The cue active at t and the time since it began. */
  cue(t: number): { cue: Cue; since: number; next: Cue | null } {
    const cs = this.cues;
    let i = 0;
    while (i + 1 < cs.length && cs[i + 1]!.t <= t) i++;
    return { cue: cs[i]!, since: t - cs[i]!.t, next: cs[i + 1] ?? null };
  }
  /** A param of the active cue (falls back to the entry params, then to `d`). */
  param<T>(t: number, k: string, d: T): T {
    const c = this.cue(t).cue.params;
    return (c[k] ?? this.ctx.params[k] ?? d) as T;
  }
  /** Time of the cut that started this entry (the middle of the incoming transition). */
  get cutTime(): number { return this.ctx.params.cutTime ?? this.ctx.start; }

  /** Lyric lines that start inside [t0, t1) (default: this entry's window). */
  linesIn(t0 = this.ctx.start, t1 = this.ctx.end): Line[] {
    return this.ctx.lyrics.lines.filter((l) => l.start >= t0 - 0.05 && l.start < t1);
  }
  /** Words sung inside [t0, t1). */
  wordsIn(t0 = this.ctx.start, t1 = this.ctx.end): Word[] {
    return this.ctx.lyrics.words.filter((w) => w.start >= t0 - 0.05 && w.start < t1);
  }

  /** Draw the mode's picture into `out` (must fully overwrite it). */
  abstract draw(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides | void;

  render(f: Frame, out: THREE.WebGLRenderTarget): PostOverrides | void {
    const kind = (this.ctx.params.transition ?? 'wave') as TransitionKind;
    if (!f.under || f.tin >= 1) return this.draw(f, out);
    this.inner ??= makeRT();
    const ov = this.draw(f, this.inner);
    SHARED ??= new Transitions();
    SHARED.render(this.ctx.renderer, f.under, this.inner.texture, out, f.tin, kind, f.t, {
      seed: this.ctx.params.seed ?? 1 + (this.ctx.params.entryIndex ?? 0),
      focus: this.ctx.params.focus ?? EXIT_FOCUS.get((this.ctx.params.entryIndex ?? 0) - 1),
    });
    // the outgoing mode's camera moves (zoom, shake) are not carried over: settle ours in
    if (!ov) return ov;
    const r: PostOverrides = { ...ov, zoom: 1 + ((ov.zoom ?? 1) - 1) * f.tin };
    if (ov.shake) r.shake = [ov.shake[0] * f.tin, ov.shake[1] * f.tin];
    return r;
  }
}
