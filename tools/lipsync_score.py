"""Score lip sync: mouth aperture (from mouth_track.py) against the isolated vocal.

The vocal's RMS envelope is sampled onto the 24 fps grid and Pearson r is taken at
lags -6..+12 frames (positive = mouth trailing voice). p is the share of 1000
circularly shifted aperture traces that correlate as well at their best lag.
Also plots aperture over the vocal envelope with the word timings.
"""
import argparse, json
import numpy as np
import librosa
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FPS = 24


def vocal_env(wav, n):
    y, sr = librosa.load(wav, sr=24000)
    hop = sr // FPS
    rms = librosa.feature.rms(y=y, frame_length=hop * 2, hop_length=hop, center=True)[0]
    rms = np.pad(rms, (0, max(0, n - len(rms))))[:n]
    return rms


def fill(a):
    a = np.array([np.nan if x is None else x for x in a], float)
    ok = ~np.isnan(a)
    a[~ok] = np.interp(np.flatnonzero(~ok), np.flatnonzero(ok), a[ok])
    return a, ok.mean()


def best_lag(x, y, lags=range(-6, 13)):
    def r(l):
        a, b = (x[l:], y[:len(y) - l]) if l >= 0 else (x[:l], y[-l:])
        return np.corrcoef(a, b)[0, 1]
    rs = {l: r(l) for l in lags}
    l = max(rs, key=rs.get)
    return l, rs[l]


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("vocals")
    p.add_argument("mouths", nargs="+", help="*.mouth.json from mouth_track.py")
    p.add_argument("--words", help="json list of [word, start_s, end_s] relative to the clip")
    p.add_argument("--png", default="out/lipsync.png")
    p.add_argument("--start", type=float, default=0, help="score from this second on (skip a wide opening shot)")
    a = p.parse_args()
    rng = np.random.default_rng(0)
    words = json.load(open(a.words)) if a.words else []

    fig, axes = plt.subplots(len(a.mouths), 1, figsize=(14, 3.2 * len(a.mouths)), squeeze=False)
    for ax, m in zip(axes[:, 0], a.mouths):
        raw = json.load(open(m))
        env = vocal_env(a.vocals, len(raw))
        k0 = int(round(a.start * FPS))
        ap, cover = fill(raw[k0:])
        env = env[k0:]
        lag, r = best_lag(ap, env)
        null = [best_lag(np.roll(ap, rng.integers(24, len(ap) - 24)), env)[1] for _ in range(1000)]
        pv = (np.sum(np.array(null) >= r) + 1) / 1001
        r0 = np.corrcoef(ap, env)[0, 1]
        print(f"{m}\n  face {cover:.0%} of frames   r={r:.3f} at lag {lag:+d} frames"
              f"   r(lag 0)={r0:.3f}   p={pv:.3f}  (null median {np.median(null):.3f})")
        t = (np.arange(len(ap)) + k0) / FPS
        ax.fill_between(t, 0, env / env.max(), color="tab:orange", alpha=0.3, label="vocal RMS")
        ax.plot(t, (ap - ap.min()) / (np.ptp(ap) + 1e-9), lw=1.2, label="mouth aperture")
        for w, s, e in words:
            ax.text(s, 1.02, w, fontsize=7, rotation=45)
        ax.set_xlim(t[0], t[-1]); ax.set_ylim(0, 1.25)
        ax.set_title(f"{m.split('/')[-1]}   r={r:.2f} @ {lag:+d}f   p={pv:.3f}", loc="left")
        ax.legend(loc="upper right", fontsize=8)
    axes[-1, 0].set_xlabel("seconds")
    fig.tight_layout(); fig.savefig(a.png, dpi=90)
    print("wrote", a.png)
