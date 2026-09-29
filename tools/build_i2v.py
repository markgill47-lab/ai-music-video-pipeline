"""Build a MiniMax H3 image-to-video workflow from video_minimax_h3_i2v.json.

The first_frame is emitted to the text encoder as <Picture 1>, so prompts should
follow the official I2VA format (image-alignment line, then the three core fields).
"""
import argparse, json, os, random

TEMPLATE = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows\video_minimax_h3_i2v.json"
WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"

N_SAVE, N_IMG, N_RES = "92", "114", "115"          # top level
N_I2V, N_DUR, N_SEED, N_SCHED, N_VIDEO = "104", "111", "15", "9", "91"   # inside subgraph


def build(prompt_text, name, first_frame, aspect, megapixels, seconds,
          seed, scheduler, steps, fps, bit_depth):
    wf = json.load(open(TEMPLATE, encoding="utf-8"))

    for n in wf["nodes"]:
        nid = str(n["id"])
        if nid == N_SAVE:
            n["widgets_values"][0] = f"video/H3_{name}"
        if nid == N_IMG:
            n["widgets_values"][0] = first_frame
        if nid == N_RES:
            n["widgets_values"][0] = aspect
            n["widgets_values"][1] = megapixels

    sg = wf["definitions"]["subgraphs"][0]
    inner = {str(n["id"]): n for n in sg["nodes"]}
    inner[N_I2V]["widgets_values"][0] = prompt_text
    inner[N_DUR]["widgets_values"][0] = seconds
    inner[N_SEED]["widgets_values"][0] = seed
    inner[N_SEED]["widgets_values"][1] = "fixed"
    inner[N_SCHED]["widgets_values"][0] = scheduler
    inner[N_SCHED]["widgets_values"][1] = steps
    inner[N_VIDEO]["widgets_values"][0] = fps
    inner[N_VIDEO]["widgets_values"][1] = bit_depth

    dst = os.path.join(WF_DIR, f"minimax_h3_i2v_{name}.json")
    json.dump(wf, open(dst, "w", encoding="utf-8"), indent=2)
    return dst


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--first-frame", required=True, help="filename already in ComfyUI/input")
    p.add_argument("--aspect", default="16:9 (Widescreen)")
    p.add_argument("--megapixels", type=float, default=1.0)
    p.add_argument("--seconds", type=float, default=5)
    p.add_argument("--scheduler", default="beta")
    p.add_argument("--steps", type=int, default=20)
    p.add_argument("--fps", type=float, default=24)
    p.add_argument("--bit-depth", type=int, default=8)
    p.add_argument("--seed", type=int, default=-1)
    a = p.parse_args()

    seed = random.randint(0, 2**48) if a.seed < 0 else a.seed
    text = open(a.prompt, encoding="utf-8").read().strip()
    dst = build(text, a.name, a.first_frame, a.aspect, a.megapixels, a.seconds,
                seed, a.scheduler, a.steps, a.fps, a.bit_depth)
    print("wrote", dst)
    print(f"  first_frame={a.first_frame}  {a.aspect}  {a.megapixels}MP  {a.seconds}s")
    print(f"  scheduler={a.scheduler} steps={a.steps} fps={a.fps} bit_depth={a.bit_depth} seed={seed}")
    print(f"  prompt chars={len(text)}")
