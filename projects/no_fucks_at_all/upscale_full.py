"""Upscale a finished cut with SeedVR2 2x (wavelet colour), segment by segment.

Segments break only at the edit's own shot cuts (from assemble_full.edl()), so every
seam is already a cut and temporal consistency inside each shot is untouched. Each
segment is resumable: finished segments in out/upscale_full/ are skipped on re-run.
  python upscale_full.py out/rough_cut_v5.mp4 out/rough_cut_v5_2x.mp4
Log: out/upscale_full/log.txt
"""
import glob, os, shutil, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))

import assemble_full
from build_upscale import build

FPS = 24
MAX_SEG = 15.1          # seconds; longest single shot in the cut
COMFY = r"D:\Projects_26\Comfyu\ComfyUI"
CLI = os.path.join(COMFY, r"venv\Scripts\comfy.exe")
WORK = "out/upscale_full"


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    open(os.path.join(WORK, "log.txt"), "a", encoding="utf-8").write(line + "\n")


def segments(total_frames):
    """Group consecutive EDL pieces into segments <= MAX_SEG, cut only at piece boundaries."""
    cuts = sorted({round(p[1] * FPS) for p in assemble_full.edl()} | {total_frames})
    cuts = [c for c in cuts if 0 <= c <= total_frames]
    segs, start = [], 0
    for a, b in zip(cuts, cuts[1:]):
        if (b - start) / FPS > MAX_SEG and a > start:
            segs.append((start, a)); start = a
    segs.append((start, total_frames))
    return segs


def upscale_segment(src, i, f0, f1):
    name = f"full_seg{i:02d}"
    done = os.path.join(WORK, f"{name}.mp4")
    if os.path.exists(done):
        log(f"{name} already done, skipping"); return done
    clip = os.path.join(WORK, f"{name}_src.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf",
                    f"select='between(n\\,{f0}\\,{f1 - 1})',setpts=N/{FPS}/TB", "-an",
                    "-c:v", "libx264", "-crf", "10", "-pix_fmt", "yuv420p", clip], check=True)
    shutil.copy(clip, os.path.join(COMFY, "input", f"{name}_src.mp4"))
    wf = build(f"{name}_src.mp4", name, 2.0, FPS, 42, split=True, color="wavelet")
    for attempt in (1, 2):
        # free VRAM between segments; leftover models caused OOMs in testing
        subprocess.run(["curl", "-s", "-X", "POST", "http://127.0.0.1:8188/free", "-H",
                        "Content-Type: application/json", "-d", '{"unload_models":true,"free_memory":true}'],
                       capture_output=True)
        t = time.time()
        r = subprocess.run([CLI, "run", "--workflow", wf, "--wait", "--timeout", "3600"],
                           capture_output=True, text=True)
        outs = sorted(glob.glob(os.path.join(COMFY, "output", "video", f"SeedVR2_{name}_*.mp4")), key=os.path.getmtime)
        if r.returncode == 0 and outs:
            shutil.copy(outs[-1], done)
            log(f"{name} frames {f0}-{f1} ({(f1 - f0) / FPS:.1f}s) done in {time.time() - t:.0f}s")
            return done
        log(f"{name} attempt {attempt} failed: {(r.stdout + r.stderr)[-600:]}")
    raise SystemExit(f"{name} failed twice; re-run to resume")


def main(src, dst):
    os.makedirs(WORK, exist_ok=True)
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_packets", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    segs = segments(n)
    log(f"{src}: {n} frames in {len(segs)} segments")
    parts = [upscale_segment(src, i, a, b) for i, (a, b) in enumerate(segs)]
    # check frame counts before joining so the song stays in sync
    for p, (a, b) in zip(parts, segs):
        m = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                                "stream=nb_read_packets", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
        if m != b - a:
            log(f"WARNING {p}: {m} frames, expected {b - a}")
    lst = os.path.join(WORK, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", src,
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "14", "-preset", "slow",
                    "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "copy", "-shortest", dst], check=True)
    log(f"wrote {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
