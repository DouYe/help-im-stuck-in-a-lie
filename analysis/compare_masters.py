"""Compare two masters of the song: where are they sample-identical, and how do later times map across?
usage:  python3 analysis/compare_masters.py audio/edit/song.mp3 audio/final/song.mp3
Decodes both with ffmpeg (mono 22.05 kHz), finds the first point where the waveforms stop matching, then
maps 2-s windows of A onto B by normalised cross-correlation of log band energies (50 fps), and refines the
steady offset to the sample with a waveform cross-correlation. numpy + ffmpeg only."""
import subprocess, sys
import numpy as np

SR, HOP = 22050, 441


def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def bands(x):
    n = 2048
    fr = np.lib.stride_tricks.sliding_window_view(np.pad(x, (n // 2, n // 2)), n)[::HOP] * np.hanning(n)
    S = np.abs(np.fft.rfft(fr, axis=1)) ** 2
    f = np.fft.rfftfreq(n, 1 / SR); e = np.geomspace(60, 8000, 25)
    B = np.log1p(np.stack([S[:, (f >= a) & (f < b)].sum(1) for a, b in zip(e[:-1], e[1:])], 1) * 1e3)
    return (B - B.mean(0)) / (B.std(0) + 1e-6)


def main(pa, pb):
    a, b = load(pa), load(pb)
    print(f'A {pa}: {len(a) / SR:.3f} s   B {pb}: {len(b) / SR:.3f} s')
    n = min(len(a), len(b)); blk = SR // 100
    d = np.abs(a[:n] - b[:n]).reshape(-1)[: n // blk * blk].reshape(-1, blk).mean(1)
    lv = np.abs(a[:n]).reshape(-1)[: n // blk * blk].reshape(-1, blk).mean(1) + 1e-6
    k = int(np.argmax(d / lv > 0.05)) if np.any(d / lv > 0.05) else None
    print('identical up to', 'the end' if k is None else f'{k * blk / SR:.3f} s')
    A, B = bands(a), bands(b); fps = SR / HOP; win = int(2 * fps)
    prev, offs = None, []
    for t0 in np.arange(0, len(a) / SR - 2.5, 0.5):
        s0 = int(t0 * fps); w = A[s0:s0 + win]
        if len(w) < win: break
        best = (-9, 0)
        for off in range(int(-2 * fps), int(15 * fps)):
            s = s0 + off
            if s < 0 or s + win > len(B): continue
            c = float((w * B[s:s + win]).mean())
            if c > best[0]: best = (c, off)
        o = best[1] / fps; offs.append((t0, o))
        if prev is None or abs(o - prev) > 0.05: print(f'  A {t0:7.2f} s -> offset {o:+7.3f} s   (corr {best[0]:.2f})')
        prev = o
    print('  (isolated jumps in quiet or repeated passages - intro, fades, the tail - are matching noise)')
    # the steady offset after the change: the most common window offset, then refined to the sample
    late = [o for t, o in offs if (k is not None and t > k * blk / SR + 5)]
    if late:
        vals, cnt = np.unique(np.round(late, 2), return_counts=True); m = float(vals[np.argmax(cnt)])
        t = (k * blk / SR) + 20; i0 = int(t * SR); seg = a[i0:i0 + SR * 5]
        lo, hi = i0 + int((m - 0.05) * SR), i0 + int((m + 0.05) * SR)
        cs = [float(np.dot(seg, b[j:j + len(seg)])) for j in range(lo, hi)]
        j = lo + int(np.argmax(cs)); print(f'steady offset after the change: {(j - i0) / SR:+.4f} s (sample-accurate, at A {t:.1f} s)')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
