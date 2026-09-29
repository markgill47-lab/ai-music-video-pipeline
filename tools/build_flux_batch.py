"""Build a Flux 2 Klein 9B single-reference edit batch from the user's
Flux2_K8B_Batch_Prompt.json: one reference image, one output per prompt line.

SimplePromptBatcher joins prepend + line + append for every line of --lines, so a
whole expression/angle set runs from one file. Camera moves read best phrased as
instructions ("Rotate the camera 90 degrees to the right, show the man in profile").
"""
import argparse, json, os, random

TEMPLATE = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows\Flux2_K8B_Batch_Prompt.json"
WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"

N_SAVE, N_LOAD, N_BATCH, N_EDIT = 9, 76, 101, 75


def build(name, ref, prepend, lines, append, seed, steps):
    wf = json.load(open(TEMPLATE, encoding="utf-8"))
    for n in wf["nodes"]:
        if n["id"] == N_SAVE:
            n["widgets_values"][0] = f"plates/{name}"
        if n["id"] == N_LOAD:
            n["widgets_values"][0] = ref
        if n["id"] == N_BATCH:
            n["widgets_values"][:3] = [prepend, "\n".join(lines), append]
        if n["id"] == N_EDIT:
            n["widgets_values"][0] = seed
            n["widgets_values"][7] = steps
    dst = os.path.join(WF_DIR, f"flux9b_{name}.json")
    json.dump(wf, open(dst, "w", encoding="utf-8"), indent=2)
    return dst


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--ref", required=True, help="filename already in ComfyUI/input")
    p.add_argument("--lines", required=True, help="text file, one prompt per line")
    p.add_argument("--prepend", default="")
    p.add_argument("--append", default="")
    p.add_argument("--steps", type=int, default=4)
    p.add_argument("--seed", type=int, default=-1)
    a = p.parse_args()

    seed = random.randint(0, 2**48) if a.seed < 0 else a.seed
    lines = [l.strip() for l in open(a.lines, encoding="utf-8") if l.strip()]
    dst = build(a.name, a.ref, a.prepend, lines, a.append, seed, a.steps)
    print("wrote", dst)
    print(f"  ref={a.ref}  {len(lines)} prompts  steps={a.steps}  seed={seed}")
