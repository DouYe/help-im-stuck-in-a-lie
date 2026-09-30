import { hexToLinear } from './util';

// The whole video lives in a restrained palette: ink, bone, and one signal colour.
// One rare accent (acid, the shrooms moment) — see docs/TREATMENT.md.
export const HEX = {
  // Ink, paper and one colour: orange. Nothing else.
  ink: '#0A0A0B', // background black (slightly warm)
  ink2: '#161618', // raised black
  graphite: '#5E5B57', // pencil grey, dim lines
  ash: '#9C978F', // mid grey
  bone: '#EEE9DF', // paper, type
  signal: '#FF5314', // the one colour: orange
  ember: '#FF9A5C', // light orange
  blood: '#B8370C', // dark orange (shadow of the orange)
  acid: '#FF5314', // (unused: kept as orange so nothing else can sneak in)
} as const;

export type PaletteKey = keyof typeof HEX;

/** Linear RGB triplets for GL uniforms. */
export const LIN: Record<PaletteKey, [number, number, number]> = Object.fromEntries(
  Object.entries(HEX).map(([k, v]) => [k, hexToLinear(v)]),
) as Record<PaletteKey, [number, number, number]>;

/** CSS rgba() for Canvas2D. */
export function rgba(key: PaletteKey | string, a = 1): string {
  const hex = (HEX as Record<string, string>)[key] ?? key;
  const n = parseInt(hex.replace('#', ''), 16);
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
}
