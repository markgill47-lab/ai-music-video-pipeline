"""Collect finished act 2 renders and make a frame grid of each for review.
  python review_act2.py shot8a_boss shot8b_nope ...   (or no args: every finished shot)
Copies ComfyUI's latest H3_<name>_NNNNN_.mp4 to out/act2/<name>.mp4 and writes
frames/act2/<name>.png (8 evenly spaced frames).
"""
import glob, os, subprocess, sys

OUT = r"D:\Projects_26\Comfyu\ComfyUI\output\video"


def latest(name):
    files = sorted(glob.glob(os.path.join(OUT, f"H3_{name}_*.mp4")))
    return files[-1] if files else None


def grid(name):
    src = latest(name)
    if not src:
        return False
    os.makedirs("out/act2", exist_ok=True); os.makedirs("frames/act2", exist_ok=True)
    dst = f"out/act2/{name}.mp4"
    subprocess.run(["cmd", "/c", "copy", "/y", src, dst.replace("/", "\\")], check=True, capture_output=True)
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_packets", "-of", "csv=p=0", dst], capture_output=True, text=True).stdout)
    step = max(1, n // 8)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst, "-vf",
                    f"select='not(mod(n\\,{step}))',scale=400:-1,tile=4x2", "-frames:v", "1",
                    f"frames/act2/{name}.png"], check=True)
    print(f"{name}: {n} frames -> frames/act2/{name}.png")
    return True


if __name__ == "__main__":
    import json
    names = sys.argv[1:] or list(json.load(open("audio/act2/queued.json")))
    for nm in names:
        if not grid(nm):
            print(f"{nm}: not rendered yet")
