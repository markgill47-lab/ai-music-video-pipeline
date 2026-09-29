"""Write a turbo-enabled copy of the shipped MiniMax H3 i2v workflow.

The i2v template keeps its model chain inside a subgraph definition, not at the
top level, so the LoRA has to be spliced in there. This produces a NEW template
file and never touches video_minimax_h3_i2v.json, which build_i2v.py reads.

Usage:
  python make_i2v_turbo.py                 # 4-step 768p LoRA (matches 1.0 MP i2v)
  python make_i2v_turbo.py --lora 8step    # 8-step 544p LoRA, more flexible
"""
import argparse, json

WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"
SRC = rf"{WF_DIR}\video_minimax_h3_i2v.json"
DST = rf"{WF_DIR}\video_minimax_h3_i2v_turbo.json"

# fl2v turbo LoRAs — for the fl2va checkpoint that i2v and t2v both run on.
# NOT interchangeable with the ref2v turbo LoRA.
LORAS = {
    "768p":  ("minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors", 4),
    "8step": ("minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors", 8),
}
SHIFT_VIDEO, SHIFT_AUDIO = 12.0, 3.0

N_UNET, N_SCHED = 6, 9          # inside the subgraph


def patch(sg, lora_name, strength, steps, scheduler):
    n_lora = max(n["id"] for n in sg["nodes"]) + 1
    n_shift = n_lora + 1
    l_unet_lora = max(l["id"] for l in sg["links"]) + 1
    l_lora_shift = l_unet_lora + 1

    unet = next(n for n in sg["nodes"] if n["id"] == N_UNET)
    downstream = list(unet["outputs"][0]["links"])      # -> BasicScheduler, BasicGuider
    unet["outputs"][0]["links"] = [l_unet_lora]
    for link in sg["links"]:                            # re-source, keep link ids
        if link["id"] in downstream:
            link["origin_id"], link["origin_slot"] = n_shift, 0

    def model_input(link_id):
        return {"localized_name": "model", "name": "model", "type": "MODEL", "link": link_id}

    def widget_input(name, type_):
        return {"localized_name": name, "name": name, "type": type_,
                "widget": {"name": name}, "link": None}

    def model_output(links):
        return [{"localized_name": "MODEL", "name": "MODEL", "type": "MODEL", "links": links}]

    sg["nodes"].append({
        "id": n_lora, "type": "LoraLoaderModelOnly",
        "pos": [-2020, 4790], "size": [640, 90], "flags": {}, "order": 2, "mode": 0,
        "inputs": [model_input(l_unet_lora),
                   widget_input("lora_name", "COMBO"),
                   widget_input("strength_model", "FLOAT")],
        "outputs": model_output([l_lora_shift]),
        "properties": {"Node name for S&R": "LoraLoaderModelOnly"},
        "widgets_values": [lora_name, strength],
    })
    sg["nodes"].append({
        "id": n_shift, "type": "MiniMaxH3SigmaShift",
        "pos": [-2020, 4910], "size": [640, 90], "flags": {}, "order": 3, "mode": 0,
        "inputs": [model_input(l_lora_shift),
                   widget_input("shift_video", "FLOAT"),
                   widget_input("shift_audio", "FLOAT")],
        "outputs": model_output(downstream),
        "properties": {"Node name for S&R": "MiniMaxH3SigmaShift"},
        "widgets_values": [SHIFT_VIDEO, SHIFT_AUDIO],
    })
    sg["links"].append({"id": l_unet_lora, "origin_id": N_UNET, "origin_slot": 0,
                        "target_id": n_lora, "target_slot": 0, "type": "MODEL"})
    sg["links"].append({"id": l_lora_shift, "origin_id": n_lora, "origin_slot": 0,
                        "target_id": n_shift, "target_slot": 0, "type": "MODEL"})

    sched = next(n for n in sg["nodes"] if n["id"] == N_SCHED)
    sched["widgets_values"] = [scheduler, steps, 1]
    return n_lora, n_shift


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--lora", default="768p", choices=list(LORAS))
    p.add_argument("--strength", type=float, default=1.0)
    p.add_argument("--steps", type=int, default=None, help="defaults to the LoRA's distilled step count")
    p.add_argument("--scheduler", default="simple")
    a = p.parse_args()

    lora_name, default_steps = LORAS[a.lora]
    steps = a.steps if a.steps is not None else default_steps

    wf = json.load(open(SRC, encoding="utf-8"))
    sg = wf["definitions"]["subgraphs"][0]
    n_lora, n_shift = patch(sg, lora_name, a.strength, steps, a.scheduler)
    json.dump(wf, open(DST, "w", encoding="utf-8"), indent=2)

    print("wrote", DST)
    print(f"  lora={lora_name} @ {a.strength}  (subgraph node {n_lora})")
    print(f"  shift={SHIFT_VIDEO}/{SHIFT_AUDIO}  (subgraph node {n_shift})")
    print(f"  scheduler={a.scheduler}  steps={steps}")
