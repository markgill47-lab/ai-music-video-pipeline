"""Assemble the cut against the song from shots.py.

Each shot fills its beat slot from the start of its render (renders start on the slot's first beat,
so lip sync stays aligned). TAKES (takes.py) picks a different render or source offset. The last
shot cuts to black on the last beat. Missing renders become grey slates so a partial cut still plays.
  python assemble.py [out.mp4]
"""
import os, subprocess, sys
from shots import spans, SONG_END, LAST_BEAT

SONG = r"audio\not_my_pig.mp3"
FPS, W, H = 24, 1120, 640
TAKES = {}
if os.path.exists("takes.py"):
    from takes import TAKES


def fr(sec):
    return round(sec * FPS)


def duration(clip):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", clip],
                                capture_output=True, text=True).stdout)


def pieces():
    for sid, (a, b) in spans().items():
        clip, off = TAKES.get(sid, (f"out/{sid}.mp4", 0.0))
        yield sid, clip, off, fr(b) - fr(a)
    yield "black", None, 0.0, fr(SONG_END) - fr(LAST_BEAT)


def render(out):
    os.makedirs("out/edit", exist_ok=True)
    files, missing = [], []
    for i, (sid, clip, off, n) in enumerate(pieces()):
        f = f"out/edit/p{i:03d}.mp4"
        if clip and os.path.exists(clip):
            off = max(0.0, min(off, duration(clip) - n / FPS))
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{off:.3f}", "-i", clip, "-frames:v", str(n), "-an", "-vf",
                   f"scale={W}:{H},fps={FPS},tpad=stop_mode=clone:stop_duration=2"]
        else:
            colour = "black" if clip is None else "0x303030"
            cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c={colour}:s={W}x{H}:r={FPS}", "-frames:v", str(n)]
            if clip:
                missing.append(sid)
        subprocess.run(cmd + ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", f], check=True)
        files.append(f)
    open("out/edit/list.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/edit/list.txt",
                    "-c", "copy", "out/edit/video.mp4"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "out/edit/video.mp4", "-i", SONG, "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", out], check=True)
    print("wrote", out, f"{len(files)} pieces", "missing: " + " ".join(sorted(set(missing))) if missing else "")


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else "out/rough_cut_v1.mp4")
