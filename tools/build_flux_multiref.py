"""Build a Flux.2 Klein multi-reference composite from Flux2-Klein_3Images.json.

reference_image1 sets the output resolution, so pass the environment plate there.
Node 75 / SaveImage 9 are an unrelated single-image edit branch; SaveImage 9 is
muted so that branch never executes.
"""
import argparse, json, os, random

TEMPLATE = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows\Flux2-Klein_3Images.json"
WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"

# top-level LoadImage id -> subgraph reference slot
REF_SLOTS = {"76": "reference_image1", "81": "reference_image2",
             "99": "reference_image3", "100": "reference_image4"}
MULTIREF_SG = "65c22b29"


def build(prompt_text, name, refs, seed, batch, steps):
    wf = json.load(open(TEMPLATE, encoding="utf-8"))

    for n in wf["nodes"]:
        nid = str(n["id"])
        if nid in REF_SLOTS:
            n["widgets_values"][0] = refs[REF_SLOTS[nid]]
        if nid == "9":          # unrelated edit branch output
            n["mode"] = 2       # never
        if nid == "94":
            n["widgets_values"][0] = f"plates/{name}"

    sg = [s for s in wf["definitions"]["subgraphs"] if s["id"].startswith(MULTIREF_SG)][0]
    inner = {str(n["id"]): n for n in sg["nodes"]}
    inner["109"]["widgets_values"][0] = prompt_text        # CLIPTextEncode
    inner["106"]["widgets_values"][0] = seed               # RandomNoise
    inner["106"]["widgets_values"][1] = "fixed"
    inner["112"]["widgets_values"][2] = batch              # EmptyFlux2LatentImage
    inner["113"]["widgets_values"][0] = steps              # Flux2Scheduler

    dst = os.path.join(WF_DIR, f"flux_{name}.json")
    json.dump(wf, open(dst, "w", encoding="utf-8"), indent=2)
    return dst


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--ref1", required=True, help="environment; also sets output resolution")
    p.add_argument("--ref2", required=True)
    p.add_argument("--ref3", required=True)
    p.add_argument("--ref4", default=None, help="defaults to ref1")
    p.add_argument("--batch", type=int, default=4)
    p.add_argument("--steps", type=int, default=20)
    p.add_argument("--seed", type=int, default=-1)
    a = p.parse_args()

    seed = random.randint(0, 2**48) if a.seed < 0 else a.seed
    refs = {"reference_image1": a.ref1, "reference_image2": a.ref2,
            "reference_image3": a.ref3, "reference_image4": a.ref4 or a.ref1}
    text = open(a.prompt, encoding="utf-8").read().strip()
    dst = build(text, a.name, refs, seed, a.batch, a.steps)

    print("wrote", dst)
    for k, v in refs.items():
        print(f"  {k}: {v}")
    print(f"  batch={a.batch} steps={a.steps} seed={seed} prompt chars={len(text)}")
