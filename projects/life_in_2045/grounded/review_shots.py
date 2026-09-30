"""Collect finished Grounded renders and make an 8-frame grid of each for review.
  python review_shots.py [names...]     (no args: every queued shot)
Copies ComfyUI's latest H3_<name>_NNNNN_.mp4 to out/<name>.mp4, writes frames/<name>.png."""
import glob, json, os, shutil, subprocess, sys

OUT = r"D:\Projects_26\Comfyu\ComfyUI\output\video"


def latest(name):
    files = sorted(glob.glob(os.path.join(OUT, f"H3_{name}_0*.mp4")))
    return files[-1] if files else None


def grid(name):
    src = latest(name)
    if not src:
        return False
    os.makedirs("out", exist_ok=True); os.makedirs("frames", exist_ok=True)
    dst = f"out/{name}.mp4"
    shutil.copy(src, dst)
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_packets", "-of", "csv=p=0", dst], capture_output=True, text=True).stdout)
    step = max(1, n // 8)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dst, "-vf",
                    f"select='not(mod(n\,{step}))',scale=400:-1,tile=4x2", "-frames:v", "1",
                    f"frames/{name}.png"], check=True)
    print(f"{name}: {n} frames")
    return True


if __name__ == "__main__":
    names = sys.argv[1:] or list(json.load(open("audio/shots/queued.json")))
    for nm in names:
        if not grid(nm):
            print(f"{nm}: not rendered yet")
