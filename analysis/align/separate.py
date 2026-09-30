"""Vocal separation with UVR-MDX-NET-Voc_FT (ONNX, onnxruntime on CPU).
Writes audio/<SONG>/vocals.wav (44.1 kHz stereo) and vocals_16k.wav (mono 16 kHz, for ASR).
Model params (UVR model_data for Voc_FT): n_fft 7680, hop 1024, dim_f 3072, dim_t 2^8, compensate 1.021.
"""
import os, sys, time
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
import onnxruntime as ort

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SONG = os.environ.get('SONG', 'edit')
MODEL = os.environ.get('MDX', '/tmp/claude-0/models/UVR-MDX-NET-Voc_FT.onnx')
N_FFT, HOP, DIM_F, DIM_T, COMP = 7680, 1024, 3072, 256, 1.021
N_BINS = N_FFT // 2 + 1
CHUNK = HOP * (DIM_T - 1)
TRIM = N_FFT // 2
GEN = CHUNK - 2 * TRIM
WIN = (0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N_FFT) / N_FFT)).astype(np.float32)  # periodic hann

def stft(x):  # x [C, N] -> [C, F, T] complex (torch.stft center=True, reflect pad)
    p = N_FFT // 2
    xp = np.pad(x, ((0, 0), (p, p)), mode='reflect')
    n = 1 + (xp.shape[1] - N_FFT) // HOP
    idx = np.arange(N_FFT)[None, :] + HOP * np.arange(n)[:, None]
    fr = xp[:, idx] * WIN[None, None, :]
    return np.fft.rfft(fr, axis=-1).transpose(0, 2, 1)

def istft(S, length):  # S [C, F, T] -> [C, length]
    fr = np.fft.irfft(S.transpose(0, 2, 1), n=N_FFT, axis=-1) * WIN[None, None, :]
    C, T, _ = fr.shape
    total = N_FFT + HOP * (T - 1)
    out = np.zeros((C, total), np.float64); wsum = np.zeros(total, np.float64)
    for t in range(T):
        out[:, t * HOP:t * HOP + N_FFT] += fr[:, t]
        wsum[t * HOP:t * HOP + N_FFT] += WIN ** 2
    p = N_FFT // 2
    out = out[:, p:p + length] / np.maximum(wsum[p:p + length], 1e-8)
    return out

def main():
    sr, mix = wavfile.read(os.path.join(ROOT, 'audio', SONG, 'song_stereo.wav'))
    mix = mix.astype(np.float32)
    if mix.dtype != np.float32 or np.abs(mix).max() > 2: mix = mix / 32768.0
    mix = mix.T  # [2, N]
    assert sr == 44100, sr
    n = mix.shape[1]
    pad = GEN - (n % GEN)
    mp = np.concatenate([np.zeros((2, TRIM), np.float32), mix, np.zeros((2, pad + TRIM), np.float32)], 1)
    sess = ort.InferenceSession(MODEL, providers=['CPUExecutionProvider'])
    out = []
    t0 = time.time()
    steps = list(range(0, n + pad, GEN))
    for k, i in enumerate(steps):
        w = mp[:, i:i + CHUNK]
        S = stft(w)[:, :DIM_F]                       # [2, 3072, 256]
        x = np.stack([S[0].real, S[0].imag, S[1].real, S[1].imag])[None].astype(np.float32)
        y = sess.run(None, {'input': x})[0]
        y2 = sess.run(None, {'input': -x})[0]
        y = 0.5 * y - 0.5 * y2                        # UVR 'denoise': average of f(x) and -f(-x)
        Y = np.zeros((2, N_BINS, DIM_T), np.complex64)
        Y[0, :DIM_F] = y[0, 0] + 1j * y[0, 1]; Y[1, :DIM_F] = y[0, 2] + 1j * y[0, 3]
        wv = istft(Y, CHUNK)
        out.append(wv[:, TRIM:-TRIM])
        print(f'{k + 1}/{len(steps)}  {time.time() - t0:.0f}s', flush=True)
    voc = np.concatenate(out, 1)[:, :n] * COMP
    d = os.path.join(ROOT, 'audio', SONG)
    wavfile.write(os.path.join(d, 'vocals.wav'), sr, (np.clip(voc.T, -1, 1) * 32767).astype(np.int16))
    mono = voc.mean(0)
    m16 = resample_poly(mono, 160, 441).astype(np.float32)
    wavfile.write(os.path.join(d, 'vocals_16k.wav'), 16000, (np.clip(m16, -1, 1) * 32767).astype(np.int16))
    inst = mix[:, :n] - voc
    wavfile.write(os.path.join(d, 'instrumental.wav'), sr, (np.clip(inst.T, -1, 1) * 32767).astype(np.int16))
    print('done', voc.shape)

if __name__ == '__main__':
    main()
