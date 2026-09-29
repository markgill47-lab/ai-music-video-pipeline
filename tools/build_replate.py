"""Build a Krea2 reference-guided t2i workflow: new camera angle of an existing location.

Derives from kea2_t2I_ref_Lora.json, which conditions generation on a reference
image via TextEncodeQwenImageEdit rather than editing it in place.
"""
import argparse, json, os, random

TEMPLATE = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows\kea2_t2I_ref_Lora.json"
WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"


def build(prompt_text, name, ref, aspect, megapixels, seed, batch, expand, steps):
    wf = json.load(open(TEMPLATE, encoding="utf-8"))

    for n in wf["nodes"]:
        if str(n["id"]) == "29":
            n["widgets_values"][0] = f"plates/{name}"
        if str(n["id"]) == "49":
            n["widgets_values"][0] = aspect
            n["widgets_values"][1] = megapixels
        # orphaned top-level LoadImage: feeds nothing, but a stale filename fails validation
        if str(n["id"]) == "59":
            n["widgets_values"][0] = ref

    sg = wf["definitions"]["subgraphs"][0]
    inner = {str(n["id"]): n for n in sg["nodes"]}

    inner["19"]["widgets_values"][0] = prompt_text   # user prompt
    inner["54"]["widgets_values"][0] = ref           # reference image in ComfyUI/input
    inner["24"]["widgets_values"][0] = bool(expand)  # LLM expander
    inner["23"]["widgets_values"][0] = False         # model-LoRA branch + style suffix off
    inner["3"]["widgets_values"][0] = seed
    inner["3"]["widgets_values"][2] = steps
    inner["5"]["widgets_values"][2] = batch

    # node 52 always feeds CLIP to the encoder, so the switch cannot bypass it.
    # Its entry points at a LoRA that is not installed -> disable it explicitly.
    for w in inner["52"]["widgets_values"]:
        if isinstance(w, dict) and "lora" in w:
            w["on"] = False

    dst = os.path.join(WF_DIR, f"plate_{name}.json")
    json.dump(wf, open(dst, "w", encoding="utf-8"), indent=2)
    return dst


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--ref", required=True, help="filename already in ComfyUI/input")
    p.add_argument("--aspect", default="16:9 (Widescreen)")
    p.add_argument("--megapixels", type=float, default=1.0)
    p.add_argument("--batch", type=int, default=4)
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("--expand", action="store_true")
    p.add_argument("--seed", type=int, default=-1)
    a = p.parse_args()

    seed = random.randint(0, 2**48) if a.seed < 0 else a.seed
    text = open(a.prompt, encoding="utf-8").read().strip()
    dst = build(text, a.name, a.ref, a.aspect, a.megapixels, seed, a.batch, a.expand, a.steps)
    print("wrote", dst)
    print(f"  ref={a.ref}  {a.aspect}  {a.megapixels}MP  batch={a.batch}  steps={a.steps}")
    print(f"  expander={'ON' if a.expand else 'OFF'}  lora=OFF  seed={seed}")
    print(f"  prompt chars={len(text)}")
