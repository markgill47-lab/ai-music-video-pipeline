"""Score how well a video's motion locks to a beat grid.

Motion energy = mean absolute difference between consecutive downscaled grey frames
(so the camera must be static for this to mean anything). Motion-energy peaks are
compared with the beat times from a beats.py slice json:

  vector strength  |mean(w * exp(i*phase))| of peaks against the beat period;
                   0 = no phase preference, 1 = every hit on the same beat phase
  mean phase       where in the beat the hits land (0 = on the beat), in frames
  p                share of 2000 circularly-shifted motion traces scoring as high,
                   i.e. the chance a beat-agnostic motion pattern does this well

Also writes a PNG of motion energy with the beat grid overlaid.
"""
import argparse, json, subprocess
import numpy as np
from scipy.signal import find_peaks
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

W, H, FPS = 160, 90, 24


def motion(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    return np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))      # e[k] = change from frame k to k+1


def peaks_of(e):
    idx, _ = find_peaks(e, distance=4, prominence=np.std(e) * 0.5)
    return idx


def vector_strength(times, weights, beats):
    period = np.median(np.diff(beats))
    nearest = beats[np.clip(np.searchsorted(beats, times), 1, len(beats) - 1)]
    prev = beats[np.clip(np.searchsorted(beats, times) - 1, 0, len(beats) - 1)]
    ref = np.where(np.abs(times - prev) < np.abs(times - nearest), prev, nearest)
    ph = 2 * np.pi * (times - ref) / period
    z = (weights * np.exp(1j * ph)).sum() / weights.sum()
    return abs(z), np.angle(z) / (2 * np.pi) * period * FPS, period


def music_curve(wav, n):
    """Onset strength of the guide audio, max-pooled onto the 24 fps frame grid."""
    import librosa
    y, sr = librosa.load(wav, sr=44100)
    env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=441)       # 100 Hz
    t = np.arange(1, n + 1) / FPS
    k = np.clip((t * 100).astype(int), 0, len(env) - 1)
    return np.array([env[max(0, i - 2):i + 3].max() for i in k])


def best_lag(e, m, lags=range(-6, 13)):
    """Pearson r of motion vs music at each lag (motion trailing music is positive)."""
    def r(l):
        a, b = (e[l:], m[:len(m) - l]) if l >= 0 else (e[:l], m[-l:])
        return np.corrcoef(a, b)[0, 1]
    rs = {l: r(l) for l in lags}
    l = max(rs, key=rs.get)
    return l, rs[l]


def score(e, beats):
    pk = peaks_of(e)
    t = (pk + 1) / FPS                         # the change lands on frame k+1
    return vector_strength(t, e[pk], beats), pk


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("beats_json")
    p.add_argument("videos", nargs="+")
    p.add_argument("--png", default="out/beat_sync.png")
    p.add_argument("--audio", help="guide wav; adds a motion-vs-music-onset correlation")
    a = p.parse_args()
    beats = np.array(json.load(open(a.beats_json))["beats"])
    rng = np.random.default_rng(0)

    fig, axes = plt.subplots(len(a.videos), 1, figsize=(14, 3 * len(a.videos)), squeeze=False)
    for ax, v in zip(axes[:, 0], a.videos):
        e = motion(v)
        (vs, ph, period), pk = score(e, beats)
        null = []
        for _ in range(2000):
            (n, _, _), _ = score(np.roll(e, rng.integers(3, len(e) - 3)), beats)
            null.append(n)
        pval = (np.sum(np.array(null) >= vs) + 1) / (len(null) + 1)
        print(f"{v}\n  {len(pk)} motion peaks, beat period {period * FPS:.1f} frames"
              f"\n  vector strength {vs:.3f}  mean phase {ph:+.1f} frames  p={pval:.3f}"
              f"  (null median {np.median(null):.3f})")
        if a.audio:
            m = music_curve(a.audio, len(e))
            lag, r = best_lag(e, m)
            rnull = [best_lag(np.roll(e, rng.integers(24, len(e) - 24)), m)[1] for _ in range(500)]
            rp = (np.sum(np.array(rnull) >= r) + 1) / (len(rnull) + 1)
            print(f"  motion vs music onsets: r={r:.3f} at lag {lag:+d} frames  p={rp:.3f}"
                  f"  (null median {np.median(rnull):.3f})")
        tt = np.arange(1, len(e) + 1) / FPS
        ax.plot(tt, e, lw=1)
        ax.plot(tt[pk], e[pk], "o", ms=4)
        for b in beats:
            ax.axvline(b, color="r", alpha=0.35, lw=1)
        ax.set_title(f"{v.split('/')[-1]}   VS={vs:.2f}  phase={ph:+.1f}f  p={pval:.3f}")
        ax.set_xlim(0, tt[-1])
    axes[-1, 0].set_xlabel("seconds (red = beats)")
    fig.tight_layout()
    fig.savefig(a.png, dpi=90)
    print("wrote", a.png)
