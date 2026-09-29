"""Build a Krea2-turbo t2i workflow for an environment reference plate.

Derives from image_krea2_turbo_t2i_int8.json. Edits inner subgraph nodes directly
because comfy-cli reports a slot-pairing misalignment on this template.
"""
import argparse, json, os, random

TEMPLATE = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows\image_krea2_turbo_t2i_int8.json"
WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"


def build(prompt_text, name, aspect, megapixels, seed, batch, expand, steps,
          lora, lora_strength, use_lora, style_suffix):
    wf = json.load(open(TEMPLATE, encoding="utf-8"))

    # top level: output name + resolution
    for n in wf["nodes"]:
        if str(n["id"]) == "29":
            n["widgets_values"][0] = f"plates/{name}"
        if str(n["id"]) == "49":
            n["widgets_values"][0] = aspect
            n["widgets_values"][1] = megapixels

    sg = wf["definitions"]["subgraphs"][0]
    inner = {str(n["id"]): n for n in sg["nodes"]}

    inner["19"]["widgets_values"][0] = prompt_text      # user prompt
    inner["24"]["widgets_values"][0] = bool(expand)     # LLM prompt expander on/off
    # node 23 gates BOTH the LoRA branch (switch 22) and the style-suffix branch (switch 28)
    inner["23"]["widgets_values"][0] = bool(use_lora)
    inner["15"]["widgets_values"][0] = lora             # must exist even when bypassed
    inner["15"]["widgets_values"][1] = lora_strength
    inner["27"]["widgets_values"][1] = style_suffix
    inner["27"]["widgets_values"][2] = ", " if style_suffix else ""
    inner["3"]["widgets_values"][0] = seed              # KSampler seed
    inner["3"]["widgets_values"][2] = steps
    inner["5"]["widgets_values"][2] = batch             # batch size

    dst = os.path.join(WF_DIR, f"plate_{name}.json")
    json.dump(wf, open(dst, "w", encoding="utf-8"), indent=2)
    return dst


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--aspect", default="16:9 (Widescreen)")
    p.add_argument("--megapixels", type=float, default=1.0)
    p.add_argument("--batch", type=int, default=4)
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("--expand", action="store_true", help="route prompt through the LLM expander")
    p.add_argument("--seed", type=int, default=-1)
    p.add_argument("--lora", default="dramatic_dark_lighting.safetensors",
                   help="must name an installed LoRA even when --use-lora is off")
    p.add_argument("--lora-strength", type=float, default=0.8)
    p.add_argument("--use-lora", action="store_true")
    p.add_argument("--style-suffix", default="",
                   help="appended to the prompt; only active when --use-lora is set")
    a = p.parse_args()

    seed = random.randint(0, 2**48) if a.seed < 0 else a.seed
    text = open(a.prompt, encoding="utf-8").read().strip()
    dst = build(text, a.name, a.aspect, a.megapixels, seed, a.batch, a.expand, a.steps,
                a.lora, a.lora_strength, a.use_lora, a.style_suffix)
    print("wrote", dst)
    print(f"  {a.aspect}  {a.megapixels}MP  batch={a.batch}  steps={a.steps}")
    print(f"  expander={'ON' if a.expand else 'OFF'}  seed={seed}")
    print(f"  lora={'ON ' + a.lora + ' @' + str(a.lora_strength) if a.use_lora else 'OFF (' + a.lora + ' loaded but bypassed)'}")
    print(f"  style_suffix={a.style_suffix!r}")
    print(f"  prompt chars={len(text)}")
