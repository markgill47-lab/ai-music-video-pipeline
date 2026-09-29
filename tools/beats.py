"""Beat analysis for music-driven H3 tests.

  analyse <track>                  tempo, beats, and a ranked list of 10 s windows
  slice <track> --start S --dur D  cut a window to audio/ as wav + beats json

Windows are ranked by how hard the beat hits (onset strength on the beat grid
relative to between beats) and how steady it is, so a test clip has a pulse the
model could plausibly lock onto.
"""
import argparse, json, os, subprocess
import numpy as np
import librosa

SR = 44100
HOP = 512


def load(path):
    y, sr = librosa.load(path, sr=SR, mono=True)
    return y, sr


def analyse(path, win, step):
    y, sr = load(path)
    env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=HOP)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=env, sr=sr, hop_length=HOP)
    beats = librosa.frames_to_time(beat_frames, sr=sr, hop_length=HOP)
    rms = librosa.feature.rms(y=y, hop_length=HOP)[0]
    t_env = librosa.frames_to_time(np.arange(len(env)), sr=sr, hop_length=HOP)
    dur = len(y) / sr

    rows = []
    for s in np.arange(0, dur - win, step):
        b = beats[(beats >= s) & (beats < s + win)]
        if len(b) < 8:
            continue
        m = (t_env >= s) & (t_env < s + win)
        on_beat = env[np.searchsorted(t_env, b)]
        mid = env[np.searchsorted(t_env, (b[:-1] + b[1:]) / 2)]
        contrast = float(on_beat.mean() / (mid.mean() + 1e-6))
        ibi = np.diff(b)
        steadiness = float(1 - ibi.std() / ibi.mean())
        loud = float(rms[m].mean())
        rows.append(dict(start=round(float(s), 2), beats=len(b), contrast=round(contrast, 2),
                         steadiness=round(steadiness, 3), rms=round(loud, 4),
                         score=round(contrast * steadiness * loud / rms.mean(), 3)))
    rows.sort(key=lambda r: -r["score"])
    return dict(duration=round(dur, 2), tempo=round(float(np.atleast_1d(tempo)[0]), 2),
                beats=[round(float(t), 3) for t in beats], windows=rows)


def slice_(path, start, dur, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    stem = f"{os.path.splitext(os.path.basename(path))[0].replace(' ', '_')}_{start:.2f}s_{dur:g}s"
    wav = os.path.join(out_dir, stem + ".wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-t", str(dur), "-i", path,
                    "-ac", "2", "-ar", str(SR), wav], check=True)
    # re-track beats on the slice itself so times are relative to the clip start
    y, sr = load(wav)
    env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=HOP)
    tempo, bf = librosa.beat.beat_track(onset_envelope=env, sr=sr, hop_length=HOP)
    beats = librosa.frames_to_time(bf, sr=sr, hop_length=HOP)
    onsets = librosa.onset.onset_detect(onset_envelope=env, sr=sr, hop_length=HOP, units="time")
    meta = dict(source=path, start=start, duration=dur, tempo=round(float(np.atleast_1d(tempo)[0]), 2),
                beats=[round(float(t), 3) for t in beats],
                beat_frames_24fps=[int(round(t * 24)) for t in beats],
                onsets=[round(float(t), 3) for t in onsets])
    json.dump(meta, open(os.path.join(out_dir, stem + ".json"), "w"), indent=1)
    return wav, meta


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyse"); a.add_argument("track")
    a.add_argument("--win", type=float, default=10); a.add_argument("--step", type=float, default=1)
    s = sub.add_parser("slice"); s.add_argument("track")
    s.add_argument("--start", type=float, required=True); s.add_argument("--dur", type=float, default=10)
    s.add_argument("--out", default="audio")
    args = p.parse_args()

    if args.cmd == "analyse":
        r = analyse(args.track, args.win, args.step)
        print(f"duration {r['duration']} s   tempo {r['tempo']} bpm   {len(r['beats'])} beats")
        print("top windows:")
        for w in r["windows"][:12]:
            print("  ", w)
    else:
        wav, m = slice_(args.track, args.start, args.dur, args.out)
        print("wrote", wav)
        print(f"  tempo {m['tempo']} bpm, {len(m['beats'])} beats at frames {m['beat_frames_24fps']}")
