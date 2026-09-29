"""Build a SeedVR2 3B int8 video-upscale workflow from the ComfyUI template.

  python build_upscale.py --video clip.mp4 --name test --scale 3.4286   # 1120 -> 3840 wide
The clip must already be in ComfyUI/input. Output lands in output/video/SeedVR2_<name>.
"""
import argparse, json, os

TEMPLATE = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows\utility_seedvr2_3b_int8_upscale_video.json"
WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"


def build(video, name, scale, fps, seed, split=False, color="none", denoise=1.0):
    wf = json.load(open(TEMPLATE, encoding="utf-8"))
    for n in wf["nodes"]:
        if n["id"] == 73:
            n["widgets_values"][0] = video
        if n["id"] == 76:
            n["widgets_values"][0] = f"video/SeedVR2_{name}"
    inner = {n["id"]: n for n in wf["definitions"]["subgraphs"][0]["nodes"]}
    inner[57]["widgets_values"][1] = scale          # ResizeImageMaskNode multiplier
    inner[75]["widgets_values"][0] = fps            # CreateVideo fps (template default 30)
    inner[54]["widgets_values"][0] = seed
    inner[54]["widgets_values"][6] = denoise       # KSampler denoise: <1 restores less, invents less
    inner[59]["widgets_values"][0] = color          # colour match to the source: lab | wavelet | adain | none
    inner[105]["widgets_values"][0] = split        # "Split Latent": sample in temporal chunks (needed at 4K)
    dst = os.path.join(WF_DIR, f"seedvr2_{name}.json")
    json.dump(wf, open(dst, "w", encoding="utf-8"), indent=2)
    return dst


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--scale", type=float, default=2.0)
    p.add_argument("--fps", type=float, default=24)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--color", default="none", choices=["lab", "wavelet", "adain", "none"])
    p.add_argument("--denoise", type=float, default=1.0)
    p.add_argument("--split", action="store_true", help="temporal chunking to fit 4K in VRAM")
    a = p.parse_args()
    print("wrote", build(a.video, a.name, a.scale, a.fps, a.seed, a.split, a.color, a.denoise))
