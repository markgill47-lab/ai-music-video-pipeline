"""Build a 3-reference MiniMax H3 ref2v workflow, using hey_claude.json as the base.

That template already wires three LoadImage nodes into ref_image_0/1/2, which the
tokenizer emits as <Picture 1>/<Picture 2>/<Picture 3> in socket order.
"""
import argparse, json, os, random

TEMPLATE = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows\hey_claude.json"
WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"

N_SAVE, N_RES, N_SCHED, N_SEED = "92", "115", "124", "129"
N_REF2V, N_PROMPT, N_DUR = "136", "138", "132"
# LoadImage id -> the <Picture N> tag it becomes (socket order on node 136)
PIC = {"137": 1, "139": 2, "141": 3}


def build(prompt_text, name, pics, megapixels, seconds, ref_size, scheduler, steps, seed):
    wf = json.load(open(TEMPLATE, encoding="utf-8"))
    nodes = {str(n["id"]): n for n in wf["nodes"]}

    for nid, idx in PIC.items():
        nodes[nid]["widgets_values"][0] = pics[idx]

    nodes[N_PROMPT]["widgets_values"][0] = prompt_text
    nodes[N_REF2V]["widgets_values"][4] = ref_size      # [prompt, w, h, length, ref_image_size]
    nodes[N_RES]["widgets_values"][1] = megapixels
    nodes[N_DUR]["widgets_values"][0] = seconds
    nodes[N_SCHED]["widgets_values"][0] = scheduler
    nodes[N_SCHED]["widgets_values"][1] = steps
    nodes[N_SEED]["widgets_values"][0] = seed
    nodes[N_SEED]["widgets_values"][1] = "fixed"
    nodes[N_SAVE]["widgets_values"][0] = f"video/H3_{name}"

    dst = os.path.join(WF_DIR, f"minimax_h3_r2v3_{name}.json")
    json.dump(wf, open(dst, "w", encoding="utf-8"), indent=2)
    return dst


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--pic1", required=True, help="becomes <Picture 1>")
    p.add_argument("--pic2", required=True, help="becomes <Picture 2>")
    p.add_argument("--pic3", required=True, help="becomes <Picture 3>")
    p.add_argument("--megapixels", type=float, default=0.7)
    p.add_argument("--seconds", type=float, default=10)
    p.add_argument("--ref-size", default="max", choices=["match", "max"])
    p.add_argument("--scheduler", default="beta")
    p.add_argument("--steps", type=int, default=20)
    p.add_argument("--seed", type=int, default=-1)
    a = p.parse_args()

    seed = random.randint(0, 2**48) if a.seed < 0 else a.seed
    text = open(a.prompt, encoding="utf-8").read().strip()
    dst = build(text, a.name, {1: a.pic1, 2: a.pic2, 3: a.pic3},
                a.megapixels, a.seconds, a.ref_size, a.scheduler, a.steps, seed)
    print("wrote", dst)
    print(f"  <Picture 1> = {a.pic1}")
    print(f"  <Picture 2> = {a.pic2}")
    print(f"  <Picture 3> = {a.pic3}")
    print(f"  {a.megapixels}MP  {a.seconds}s  ref_size={a.ref_size}  "
          f"scheduler={a.scheduler}  steps={a.steps}  seed={seed}")
    print(f"  prompt chars={len(text)}")
