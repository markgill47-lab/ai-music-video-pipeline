"""Build a single-reference MiniMax H3 ref2v workflow from the shipped template.

Derives from ComfyUI's video_minimax_h3_r2v template, strips it to one reference
image socket, and applies prompt / resolution / duration / sampler overrides.

Usage:
  python build_r2v.py --ref Mara1.png --prompt prompts/mara_bar.txt --name mara_bar \
      --megapixels 0.7 --seconds 5 --ref-size max --scheduler beta

  # 4-step distilled ref2v (lightx2v turbo LoRA), ~5x fewer steps:
  python build_r2v.py --ref Mara1.png --prompt prompts/mara_bar.txt --name mara_bar \
      --turbo
"""
import argparse, json, os, random

TEMPLATE = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows\video_minimax_h3_r2v.json"
WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"

# node ids in the shipped template
N_SAVE, N_RES, N_SCHED, N_SEED = "92", "115", "124", "129"
N_REF2V, N_IMG_A, N_PROMPT, N_IMG_B, N_DUR = "136", "137", "138", "139", "132"
N_UNET = "127"

# ref2va turbo: distilled at 4 NFE, shift 12/3, 544p, ref_image_size=match.
# NOT interchangeable with the fl2v turbo LoRAs from the same repo.
TURBO_LORA = "minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors"
TURBO_STEPS, TURBO_SCHED = 4, "simple"
SHIFT_VIDEO, SHIFT_AUDIO = 12.0, 3.0


def widget_index(node, name):
    """Map a widget name to its positional index in widgets_values."""
    i = 0
    for inp in node.get("inputs", []):
        if inp.get("widget"):
            if inp["widget"].get("name") == name:
                return i
            i += 1
    raise KeyError(f"widget {name!r} not found on node {node['id']} ({node['type']})")


def set_widget(node, name, value):
    node["widgets_values"][widget_index(node, name)] = value


def insert_turbo(wf, nodes, strength):
    """Splice LoraLoaderModelOnly -> MiniMaxH3SigmaShift between UNETLoader and its consumers.

    The UNETLoader's two MODEL links (to BasicScheduler and BasicGuider) are
    re-sourced onto the shift node, so both the sigma schedule and the guider
    see the patched model.
    """
    n_lora = wf["last_node_id"] + 1
    n_shift = n_lora + 1
    l_unet_lora = wf["last_link_id"] + 1
    l_lora_shift = l_unet_lora + 1
    wf["last_node_id"], wf["last_link_id"] = n_shift, l_lora_shift

    unet = nodes[N_UNET]
    downstream = list(unet["outputs"][0]["links"])          # [252, 257]
    unet["outputs"][0]["links"] = [l_unet_lora]
    for link in wf["links"]:                                 # re-source, keep link ids
        if link[0] in downstream:
            link[1], link[2] = n_shift, 0

    def model_input(link_id):
        return {"localized_name": "model", "name": "model", "type": "MODEL", "link": link_id}

    def widget_input(name, type_):
        return {"localized_name": name, "name": name, "type": type_,
                "widget": {"name": name}, "link": None}

    wf["nodes"].append({
        "id": n_lora, "type": "LoraLoaderModelOnly",
        "pos": [-1490, 5080], "size": [640, 90], "flags": {}, "order": 7, "mode": 0,
        "inputs": [model_input(l_unet_lora),
                   widget_input("lora_name", "COMBO"),
                   widget_input("strength_model", "FLOAT")],
        "outputs": [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL",
                     "links": [l_lora_shift]}],
        "properties": {"Node name for S&R": "LoraLoaderModelOnly"},
        "widgets_values": [TURBO_LORA, strength],
    })
    wf["nodes"].append({
        "id": n_shift, "type": "MiniMaxH3SigmaShift",
        "pos": [-1490, 5220], "size": [640, 90], "flags": {}, "order": 8, "mode": 0,
        "inputs": [model_input(l_lora_shift),
                   widget_input("shift_video", "FLOAT"),
                   widget_input("shift_audio", "FLOAT")],
        "outputs": [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL",
                     "links": downstream}],
        "properties": {"Node name for S&R": "MiniMaxH3SigmaShift"},
        "widgets_values": [SHIFT_VIDEO, SHIFT_AUDIO],
    })
    wf["links"].append([l_unet_lora, int(N_UNET), 0, n_lora, 0, "MODEL"])
    wf["links"].append([l_lora_shift, n_lora, 0, n_shift, 0, "MODEL"])


def build(ref, prompt_text, name, megapixels, seconds, ref_size, scheduler, steps, seed,
          turbo, turbo_strength):
    wf = json.load(open(TEMPLATE, encoding="utf-8"))

    # one reference only: drop the second LoadImage and its link
    wf["nodes"] = [n for n in wf["nodes"] if str(n["id"]) != N_IMG_B]
    wf["links"] = [l for l in wf["links"] if str(l[1]) != N_IMG_B]
    nodes = {str(n["id"]): n for n in wf["nodes"]}
    for inp in nodes[N_REF2V].get("inputs", []):
        if inp.get("name") == "ref_images.ref_image_1":
            inp["link"] = None

    set_widget(nodes[N_IMG_A], "image", ref)
    set_widget(nodes[N_PROMPT], "value", prompt_text)
    set_widget(nodes[N_REF2V], "ref_image_size", ref_size)
    set_widget(nodes[N_RES], "megapixels", megapixels)
    set_widget(nodes[N_DUR], "value", seconds)
    set_widget(nodes[N_SCHED], "scheduler", scheduler)
    set_widget(nodes[N_SCHED], "steps", steps)
    set_widget(nodes[N_SEED], "noise_seed", seed)
    set_widget(nodes[N_SAVE], "filename_prefix", f"video/H3_{name}")

    if turbo:
        insert_turbo(wf, nodes, turbo_strength)

    dst = os.path.join(WF_DIR, f"minimax_h3_r2v_{name}.json")
    json.dump(wf, open(dst, "w", encoding="utf-8"), indent=2)
    return dst, nodes


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ref", required=True, help="filename already in ComfyUI/input")
    p.add_argument("--prompt", required=True, help="path to a prompt .txt")
    p.add_argument("--name", required=True)
    p.add_argument("--megapixels", type=float, default=0.7)
    p.add_argument("--seconds", type=float, default=5)
    p.add_argument("--ref-size", default="max", choices=["match", "max"])
    # steps/scheduler default per-mode: 20/beta base, 4/simple under --turbo
    p.add_argument("--scheduler", default=None)
    p.add_argument("--steps", type=int, default=None)
    p.add_argument("--seed", type=int, default=-1)
    p.add_argument("--turbo", action="store_true",
                   help="apply the 4-step ref2va turbo LoRA + 12/3 sigma shift")
    p.add_argument("--turbo-strength", type=float, default=1.0,
                   help="LoRA strength; raise toward 1.2 for ghosting, lower to ~0.9 if over-sharp")
    a = p.parse_args()

    steps = a.steps if a.steps is not None else (TURBO_STEPS if a.turbo else 20)
    scheduler = a.scheduler if a.scheduler is not None else (TURBO_SCHED if a.turbo else "beta")

    seed = random.randint(0, 2**48) if a.seed < 0 else a.seed
    text = open(a.prompt, encoding="utf-8").read().strip()
    dst, nodes = build(a.ref, text, a.name, a.megapixels, a.seconds,
                       a.ref_size, scheduler, steps, seed,
                       a.turbo, a.turbo_strength)

    print("wrote", dst)
    print(f"  ref={a.ref}  ref_size={a.ref_size}  {a.megapixels}MP  {a.seconds}s")
    print(f"  scheduler={scheduler}  steps={steps}  seed={seed}")
    if a.turbo:
        print(f"  turbo={TURBO_LORA} @ {a.turbo_strength}"
              f"  shift={SHIFT_VIDEO}/{SHIFT_AUDIO}")
    print(f"  prompt chars={len(text)}")
    print("  connected ref sockets:",
          [i["name"] for i in nodes[N_REF2V]["inputs"]
           if i["name"].startswith("ref_") and i.get("link") is not None])
