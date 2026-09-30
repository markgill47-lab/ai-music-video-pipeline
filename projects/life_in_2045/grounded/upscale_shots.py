"""Upscale the Grounded cut with SeedVR2 2x (wavelet colour), one shot at a time.

Works from the edit pieces assemble.py writes to out/edit/pNNN.mp4 (each is exactly one
shot's slot), so every seam is a cut. Finished pieces are cached under a name that includes
the take and a hash of the piece, so re-running after an edit only upscales shots that
changed. Pieces over 15.1 s are split in two (SeedVR2 memory).
  python assemble.py out/rough_cut_v2.mp4
  python upscale_shots.py out/rough_cut_v2.mp4 out/rough_cut_v2_2x.mp4
Log: out/upscale/log.txt
"""
import glob, hashlib, os, shutil, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools"))
from build_upscale import build
from queue_shots import SPECS

FPS = 24
MAX_SEG = 15.1
COMFY = r"D:\Projects_26\Comfyu\ComfyUI"
CLI = os.path.join(COMFY, r"venv\Scripts\comfy.exe")
WORK = "out/upscale"


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    open(os.path.join(WORK, "log.txt"), "a", encoding="utf-8").write(line + "\n")


def frames(path):
    return int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                               "stream=nb_read_packets", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)


def upscale(src, name):
    done = os.path.join(WORK, f"{name}.mp4")
    if os.path.exists(done):
        log(f"{name} cached"); return done
    shutil.copy(src, os.path.join(COMFY, "input", f"{name}_src.mp4"))
    wf = build(f"{name}_src.mp4", name, 2.0, FPS, 42, split=True, color="wavelet")
    for attempt in (1, 2):
        subprocess.run(["curl", "-s", "-X", "POST", "http://127.0.0.1:8188/free", "-H",
                        "Content-Type: application/json", "-d", '{"unload_models":true,"free_memory":true}'],
                       capture_output=True)
        t = time.time()
        r = subprocess.run([CLI, "run", "--workflow", wf, "--wait", "--timeout", "3600"], capture_output=True, text=True)
        outs = sorted(glob.glob(os.path.join(COMFY, "output", "video", f"SeedVR2_{name}_*.mp4")), key=os.path.getmtime)
        if r.returncode == 0 and outs:
            shutil.copy(outs[-1], done)
            log(f"{name} ({frames(src) / FPS:.1f}s) done in {time.time() - t:.0f}s")
            return done
        log(f"{name} attempt {attempt} failed: {(r.stdout + r.stderr)[-600:]}")
    raise SystemExit(f"{name} failed twice; re-run to resume")


def main(cut, dst):
    os.makedirs(WORK, exist_ok=True)
    parts = []
    for i, shot in enumerate(SPECS):
        piece = f"out/edit/p{i:03d}.mp4"
        tag = hashlib.md5(open(piece, "rb").read()).hexdigest()[:8]
        n = frames(piece)
        halves = [(0, n)] if n / FPS <= MAX_SEG else [(0, n // 2), (n // 2, n)]
        for k, (a, b) in enumerate(halves):
            name = f"{shot}_{tag}_{k}"
            src = piece
            if len(halves) > 1:
                src = os.path.join(WORK, f"{name}_src.mp4")
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", piece, "-vf",
                                f"select='between(n\\,{a}\\,{b - 1})',setpts=N/{FPS}/TB", "-an",
                                "-c:v", "libx264", "-crf", "10", "-pix_fmt", "yuv420p", src], check=True)
            out = upscale(src, name)
            if frames(out) != b - a:
                log(f"WARNING {out}: {frames(out)} frames, expected {b - a}")
            parts.append(out)
    lst = os.path.join(WORK, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", cut,
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "14", "-preset", "slow",
                    "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "copy", "-shortest", dst], check=True)
    log(f"wrote {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
