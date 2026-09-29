"""Build (and optionally queue) an API-format MiniMax H3 t2va workflow with an
optional soundtrack pinned to the target timeline by MiniMaxH3AddGuide.

With --audio the guide audio is re-injected every step and never denoised, so the
model generates picture against a fixed soundtrack. Without it the same prompt and
seed run unguided, which is the baseline for judging whether the audio drives timing.
"""
import argparse, json, os, random, urllib.request

WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"
URL = "http://127.0.0.1:8188"

UNET = "minimax_h3_fl2va_pruned_int8_convrot.safetensors"
UNET_REF = "minimax_h3_ref2va_pruned_int8_convrot.safetensors"
CLIP = "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"
VAE_V = "minimax_h3_video_vae_fp16.safetensors"
VAE_A = "minimax_h3_audio_vae_fp32.safetensors"


def frames_for(seconds):
    n = max(5, round(seconds * 24))
    return n + (5 - n % 17) % 17          # snap up to the 17k+5 grid, as the template does


def build(prompt, name, width, height, seconds, seed, steps, scheduler, audio=None, frame_idx=0,
          first_frame=None, refs=None, guide_image=None, guide_end=None):
    """refs switches to ref2va (MiniMaxH3ReferenceToVideo, refs as <Picture 1..n>).
    first_frame is i2v only; guide_image pins an image at frame_idx through AddGuide,
    which works in either mode."""
    g = {
        "unet":   {"class_type": "UNETLoader", "inputs": {"unet_name": UNET_REF if refs else UNET, "weight_dtype": "default"}},
        "clip":   {"class_type": "CLIPLoader", "inputs": {"clip_name": CLIP, "type": "minimax", "device": "default"}},
        "vae_v":  {"class_type": "VAELoader", "inputs": {"vae_name": VAE_V}},
        "vae_a":  {"class_type": "VAELoader", "inputs": {"vae_name": VAE_A}},
        "i2v":    {"class_type": "MiniMaxH3ImageToVideo", "inputs": {
                    "clip": ["clip", 0], "vae": ["vae_v", 0], "prompt": prompt,
                    "width": width, "height": height, "length": frames_for(seconds)}},
        "noise":  {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "sampler": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}},
        "sched":  {"class_type": "BasicScheduler", "inputs": {
                    "model": ["unet", 0], "scheduler": scheduler, "steps": steps, "denoise": 1.0}},
        "guider": {"class_type": "BasicGuider", "inputs": {"model": ["unet", 0], "conditioning": ["i2v", 0]}},
        "sample": {"class_type": "SamplerCustomAdvanced", "inputs": {
                    "noise": ["noise", 0], "guider": ["guider", 0], "sampler": ["sampler", 0],
                    "sigmas": ["sched", 0], "latent_image": ["i2v", 1]}},
        "dec_v":  {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae_v", 0]}},
        "dec_a":  {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["sample", 0], "vae": ["vae_a", 0]}},
        "video":  {"class_type": "CreateVideo", "inputs": {"images": ["dec_v", 0], "audio": ["dec_a", 0],
                    "fps": 24.0, "bit_depth": 8}},
        "save":   {"class_type": "SaveVideo", "inputs": {"video": ["video", 0],
                    "filename_prefix": f"video/H3_{name}", "format": "auto", "format.codec": "auto"}},
    }
    if refs:
        inp = {k: v for k, v in g["i2v"]["inputs"].items()}
        inp.update({"audio_vae": ["vae_a", 0], "ref_image_size": "max"})
        for i, r in enumerate(refs):
            g[f"ref{i}"] = {"class_type": "LoadImage", "inputs": {"image": r}}
            inp[f"ref_images.ref_image_{i}"] = [f"ref{i}", 0]
        g["i2v"] = {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": inp}
    if first_frame:
        g["ff"] = {"class_type": "LoadImage", "inputs": {"image": first_frame}}
        g["i2v"]["inputs"]["first_frame"] = ["ff", 0]
    if audio or guide_image:
        guide = {"positive": ["i2v", 0], "latent": ["i2v", 1], "frame_idx": frame_idx}
        if audio:
            g["music"] = {"class_type": "LoadAudio", "inputs": {"audio": audio}}
            guide.update({"audio_vae": ["vae_a", 0], "audio": ["music", 0]})
        if guide_image:
            g["gimg"] = {"class_type": "LoadImage", "inputs": {"image": guide_image}}
            guide.update({"vae": ["vae_v", 0], "image": ["gimg", 0]})
        g["guide"] = {"class_type": "MiniMaxH3AddGuide", "inputs": guide}
        g["guider"]["inputs"]["conditioning"] = ["guide", 0]
    if guide_end:
        # second keyframe on the last frame: the shot travels between two pinned compositions
        g["gend"] = {"class_type": "LoadImage", "inputs": {"image": guide_end}}
        pos = ["guide", 0] if "guide" in g else ["i2v", 0]
        g["guide_end"] = {"class_type": "MiniMaxH3AddGuide", "inputs": {
            "positive": pos, "latent": ["i2v", 1], "frame_idx": -1, "vae": ["vae_v", 0], "image": ["gend", 0]}}
        g["guider"]["inputs"]["conditioning"] = ["guide_end", 0]
    return g


def queue(g):
    req = urllib.request.Request(URL + "/prompt", data=json.dumps({"prompt": g}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        raise SystemExit(e.read().decode())


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--audio", help="filename already in ComfyUI/input; omit for the unguided baseline")
    p.add_argument("--frame-idx", type=int, default=0)
    p.add_argument("--first-frame", help="i2v start frame, filename in ComfyUI/input")
    p.add_argument("--refs", nargs="+", help="ref2va reference images in <Picture> order")
    p.add_argument("--guide-image", help="image pinned at --frame-idx via AddGuide")
    p.add_argument("--width", type=int, default=1120)
    p.add_argument("--height", type=int, default=640)
    p.add_argument("--seconds", type=float, default=10)
    p.add_argument("--steps", type=int, default=20)
    p.add_argument("--scheduler", default="beta")
    p.add_argument("--seed", type=int, default=-1)
    p.add_argument("--queue", action="store_true")
    a = p.parse_args()

    seed = random.randint(0, 2**48) if a.seed < 0 else a.seed
    text = open(a.prompt, encoding="utf-8").read().strip()
    g = build(text, a.name, a.width, a.height, a.seconds, seed, a.steps, a.scheduler, a.audio, a.frame_idx,
              a.first_frame, a.refs, a.guide_image)
    dst = os.path.join(WF_DIR, f"minimax_h3_beat_{a.name}_api.json")
    json.dump(g, open(dst, "w", encoding="utf-8"), indent=2)
    print("wrote", dst)
    print(f"  {a.width}x{a.height}  {frames_for(a.seconds)} frames  audio={a.audio}  seed={seed}")
    print(f"  mode={'ref2va' if a.refs else 'fl2va'}  first_frame={a.first_frame}  refs={a.refs}  guide_image={a.guide_image}")
    if a.queue:
        print("  queued", queue(g).get("prompt_id"))
