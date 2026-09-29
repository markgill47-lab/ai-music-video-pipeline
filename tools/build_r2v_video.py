"""Build a MiniMax H3 ref2v workflow that takes a REFERENCE VIDEO plus one plate.

Uses hey_claude.json as the base, same as build_r2v_multiref.py, but rewires the
reference side: one LoadImage on ref_image_0 (<Picture 1>) and a new
LoadVideo -> GetVideoComponents chain on ref_video_0 (<Video 1>).

Two things worth knowing about that socket, neither obvious from the UI:

- `ref_videos.ref_video_0` is typed IMAGE, not VIDEO. It wants a frame batch, so a
  video file has to go through GetVideoComponents first. The node tooltip
  (comfy_extras/nodes_minimax_h3.py:186) asks for "Reference video frames at 24 fps
  (2-15s)".
- The tokenizer pairs frames and encodes each pair as one video block
  (comfy/text_encoders/minimax.py:175, process_video_block with patch_size=16,
  temporal_patch_size=2, merge_size=2). That works out at (W/32)*(H/32) tokens per
  2-frame block, so reference cost scales with BOTH resolution and duration:
  121 frames at 896x512 is ~27k tokens, while the same clip at 1120x640 would be
  ~42k. FINDINGS.md measured 16k reference tokens as essentially free on render
  time; well past that is untested, so keep the reference small and let the plate
  carry the fine detail.

Socket names carry an underscore before the index (`ref_image_0`, `ref_video_0`),
not the `ref_image0` spelling the node schema's `wire_as` hint suggests.
"""
import argparse, json, os, random

TEMPLATE = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows\hey_claude.json"
WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"

N_SAVE, N_RES, N_SCHED, N_SEED = 92, 115, 124, 129
N_REF2V, N_PROMPT, N_DUR = 136, 138, 132
N_PLATE = 137                      # LoadImage already on ref_image_0
N_SPARE = (139, 141)               # LoadImage on ref_image_1 / ref_image_2, unused here

# input indices on node 136, in serialised order
IN_REF_IMAGE = {0: 3, 1: 4, 2: 5, 3: 6}
IN_REF_VIDEO_0 = 7


def build(prompt_text, name, plate, video, megapixels, seconds, ref_size,
          scheduler, steps, seed, keep_spares):
    wf = json.load(open(TEMPLATE, encoding="utf-8"))
    nodes = {n["id"]: n for n in wf["nodes"]}
    next_node = wf["last_node_id"] + 1
    next_link = wf["last_link_id"] + 1

    def drop_link(lid):
        for l in [l for l in wf["links"] if l[0] == lid]:
            wf["links"].remove(l)
            for o in nodes[l[1]].get("outputs", []):
                if o.get("links") and lid in o["links"]:
                    o["links"].remove(lid)
            for i in nodes[l[3]].get("inputs", []):
                if i.get("link") == lid:
                    i["link"] = None

    def add_node(ntype, pos, inputs, outputs, widgets):
        nonlocal next_node
        nid, next_node = next_node, next_node + 1
        n = {"id": nid, "type": ntype, "pos": pos, "size": [340, 120], "flags": {},
             "order": 0, "mode": 0, "inputs": inputs, "outputs": outputs,
             "properties": {"Node name for S&R": ntype}, "widgets_values": widgets}
        wf["nodes"].append(n)
        nodes[nid] = n
        return nid

    def link(oid, oslot, tid, tslot, ltype):
        nonlocal next_link
        for l in [l for l in wf["links"] if l[3] == tid and l[4] == tslot]:
            drop_link(l[0])
        lid, next_link = next_link, next_link + 1
        wf["links"].append([lid, oid, oslot, tid, tslot, ltype])
        out = nodes[oid]["outputs"][oslot]
        out.setdefault("links", [])
        if out["links"] is None:
            out["links"] = []
        out["links"].append(lid)
        nodes[tid]["inputs"][tslot]["link"] = lid
        return lid

    # one plate on <Picture 1>; free the other two reference-image sockets
    nodes[N_PLATE]["widgets_values"][0] = plate
    if not keep_spares:
        for slot in (IN_REF_IMAGE[1], IN_REF_IMAGE[2]):
            lid = nodes[N_REF2V]["inputs"][slot].get("link")
            if lid is not None:
                drop_link(lid)
        for nid in N_SPARE:
            wf["nodes"] = [n for n in wf["nodes"] if n["id"] != nid]
            nodes.pop(nid, None)

    # <Video 1>: LoadVideo -> GetVideoComponents.images -> ref_video_0 (typed IMAGE)
    n_lv = add_node("LoadVideo", [-700, 1200], [],
                    [{"name": "VIDEO", "type": "VIDEO", "links": []}],
                    [video, "image"])
    n_gc = add_node("GetVideoComponents", [-300, 1200],
                    [{"name": "video", "type": "VIDEO", "link": None}],
                    [{"name": "images", "type": "IMAGE", "links": []},
                     {"name": "audio", "type": "AUDIO", "links": []},
                     {"name": "fps", "type": "FLOAT", "links": []},
                     {"name": "bit_depth", "type": "INT", "links": []}],
                    [])
    link(n_lv, 0, n_gc, 0, "VIDEO")
    link(n_gc, 0, N_REF2V, IN_REF_VIDEO_0, "IMAGE")

    nodes[N_PROMPT]["widgets_values"][0] = prompt_text
    nodes[N_REF2V]["widgets_values"][4] = ref_size   # [prompt, w, h, length, ref_image_size]
    nodes[N_RES]["widgets_values"][1] = megapixels
    nodes[N_DUR]["widgets_values"][0] = seconds
    nodes[N_SCHED]["widgets_values"][0] = scheduler
    nodes[N_SCHED]["widgets_values"][1] = steps
    nodes[N_SEED]["widgets_values"][0] = seed
    nodes[N_SEED]["widgets_values"][1] = "fixed"
    nodes[N_SAVE]["widgets_values"][0] = f"video/H3V_{name}"

    wf["last_node_id"] = next_node - 1
    wf["last_link_id"] = next_link - 1

    dst = os.path.join(WF_DIR, f"r2v_video_{name}.json")
    json.dump(wf, open(dst, "w", encoding="utf-8"), indent=2)
    return dst


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--plate", required=True, help="becomes <Picture 1>")
    p.add_argument("--video", required=True, help="becomes <Video 1>; 24 fps, 2-15s")
    p.add_argument("--megapixels", type=float, default=0.7)
    p.add_argument("--seconds", type=float, default=5.0)
    p.add_argument("--ref-size", default="max", choices=["match", "max"])
    p.add_argument("--scheduler", default="beta")
    p.add_argument("--steps", type=int, default=20)
    p.add_argument("--seed", type=int, default=-1)
    p.add_argument("--keep-spares", action="store_true",
                   help="keep the template's other two LoadImage reference slots")
    a = p.parse_args()

    seed = random.randint(0, 2**48) if a.seed < 0 else a.seed
    text = open(a.prompt, encoding="utf-8").read().strip()
    dst = build(text, a.name, a.plate, a.video, a.megapixels, a.seconds, a.ref_size,
                a.scheduler, a.steps, seed, a.keep_spares)
    print("wrote", dst)
    print(f"  <Picture 1> = {a.plate}")
    print(f"  <Video 1>   = {a.video}")
    print(f"  {a.megapixels}MP  {a.seconds}s  ref_size={a.ref_size}  "
          f"scheduler={a.scheduler}  steps={a.steps}  seed={seed}")
    print(f"  prompt chars={len(text)}")
