"""Build a depth-locked video-to-video restyle workflow on LTX 2.3 + IC-LoRA Union Control.

Derives from the gallery template `video_ltx2_3_ic_lora`, which ships unrunnable on
this install (7 validation errors). Three repairs, all applied here:

1. The template's `ltx-2.3-22b-distilled-fp8.safetensors` is not installed. We hold
   `ltx-2.3-22b-dev-fp8.safetensors` plus `ltx-2.3-22b-distilled-lora-384.safetensors`,
   which is how LTX23_i2v_official.json (known-good on this machine) is wired. So we
   swap the checkpoint and splice the distill LoRA in ahead of the IC-LoRA, keeping
   the template's 8-step schedule honest.

2. The depth branch wants `moge_2_vitl_normal_fp16.safetensors`, which we do not have.
   We do have `video_depth_anything_vits.pth`, which is *better* here: MoGe is per-frame
   and flickers, VDA is temporally consistent, and control flicker becomes output
   flicker. The whole MoGe subgraph is dropped and replaced with flat top-level nodes.
   The template's own note blesses this: "Users can swap in other preprocessors ...
   as long as they produce frame-aligned control_images."

3. The FLF subgraph's prompt-enhancer switch (inner node 211) takes `on_false` from the
   promoted `text` input, which has no inner widget to fall back on — hence
   `required_input_missing`. Fixed by feeding node 129.text from a real top-level
   PrimitiveStringMultiline instead of relying on promoted-widget serialisation.

Inner subgraph nodes are edited directly rather than through node 129's promoted
widgets, for the same reason build_r2v_multiref.py does it: the instance's
widgets_values do not reliably carry through, but an unset promoted input falls back
to the inner node's own widget.

Note the two link encodings: top-level links are arrays
[id, origin_id, origin_slot, target_id, target_slot, type]; subgraph links are dicts.

Frame count is NOT set here — the FLF subgraph derives it from the control image count
(GetImageSize -> EmptyLTXVLatentVideo.length), so the control clip's length is the
output length. Keep it on LTX's 8k+1 grid.
"""
import argparse, json, os, random

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "ltx23_ic_lora_union_control.json")
WF_DIR = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"

FLF_SUB = "f9f61b10-b689-4d67-b4fa-0acc1d9b5390"
MOGE_SUB = "ed545fa5-009c-4ccc-b318-4c00dd239751"

# top-level node ids in the template
N_SAVE, N_FLF, N_LOADVID, N_LOADIMG, N_SLICE, N_MOGE, N_PREVIEW = 68, 129, 199, 200, 692, 697, 693
# inner FLF node ids
I_CKPT, I_AUDIOVAE, I_TEXTENC = 127, 126, 103
I_W, I_H, I_KSAMPLER, I_ICLORA = 113, 98, 704, 195
I_NEG, I_FPS, I_AUDIOLATENT, I_VIDLATENT = 112, 114, 101, 108


def _mk(nid, ntype, pos, inputs, outputs, widgets):
    return {
        "id": nid, "type": ntype, "pos": pos, "size": [340, 120],
        "flags": {}, "order": 0, "mode": 0,
        "inputs": inputs, "outputs": outputs,
        "properties": {"Node name for S&R": ntype},
        "widgets_values": widgets,
    }


class Graph:
    """Top-level graph edits. Keeps wf['links'] and per-node link refs in sync."""

    def __init__(self, wf):
        self.wf = wf
        self.next_link = wf["last_link_id"] + 1
        self.next_node = wf["last_node_id"] + 1

    def node(self, nid):
        return next(n for n in self.wf["nodes"] if n["id"] == nid)

    def add_node(self, ntype, pos, inputs, outputs, widgets):
        nid = self.next_node
        self.next_node += 1
        self.wf["nodes"].append(_mk(nid, ntype, pos, inputs, outputs, widgets))
        return nid

    def drop_node(self, nid):
        self.wf["nodes"] = [n for n in self.wf["nodes"] if n["id"] != nid]
        for l in [l for l in self.wf["links"] if nid in (l[1], l[3])]:
            self._unlink(l)

    def _unlink(self, l):
        lid, oid, oslot, tid, tslot, _ = l
        self.wf["links"].remove(l)
        for n in self.wf["nodes"]:
            if n["id"] == oid:
                for o in n.get("outputs", []):
                    if o.get("links") and lid in o["links"]:
                        o["links"].remove(lid)
            if n["id"] == tid:
                for i in n.get("inputs", []):
                    if i.get("link") == lid:
                        i["link"] = None

    def unlink_into(self, tid, tslot):
        """Drop whatever currently feeds input `tslot` of node `tid`."""
        for l in [l for l in self.wf["links"] if l[3] == tid and l[4] == tslot]:
            self._unlink(l)

    def link(self, oid, oslot, tid, tslot, ltype):
        self.unlink_into(tid, tslot)
        lid = self.next_link
        self.next_link += 1
        self.wf["links"].append([lid, oid, oslot, tid, tslot, ltype])
        src = self.node(oid)["outputs"][oslot]
        src.setdefault("links", [])
        if src["links"] is None:
            src["links"] = []
        src["links"].append(lid)
        self.node(tid)["inputs"][tslot]["link"] = lid
        return lid

    def finish(self):
        self.wf["last_link_id"] = self.next_link - 1
        self.wf["last_node_id"] = self.next_node - 1


def rebuild_depth_branch(g, control_mode, vda_model, input_size, max_res, precision,
                         canny_low, canny_high, pose_resolution):
    """Replace LoadVideo -> VideoSlice -> MoGe-subgraph with the chosen control chain.

    control_mode "estimate" runs VideoDepthAnything over the clip, for ordinary
    footage. "canny" runs edge detection instead, which keeps the design lines depth
    discards -- panel seams, railings, dish arrays, lettering. Reach for it when the
    source's surface detail IS the content and the job is to re-render its materials
    and light, rather than to replace the scene. "pose" renders an OpenPose skeleton,
    which carries a performer's motion while deliberately discarding their silhouette
    -- the one control that lets a body of different proportions replace the one that
    was filmed, where depth or canny would lock the original outline. "passthrough"
    wires the clip's frames straight to control_images, for a control pass rendered
    elsewhere -- a Blender/Unity Z-depth render, or a clay/AO pass of untextured
    geometry. The IC-LoRA only asks for frame-aligned control_images and does not care
    how they were produced; the template's own note says as much.

    Pose discards the ENTIRE scene, not just the performer -- the skeleton frames carry
    no room, no wall, no props. Everything except the motion has to come from the first
    frame and the prompt, so expect the background to drift far more than it does under
    depth or canny.

    Canny is per-frame and has no temporal smoothing, unlike VideoDepthAnything, so
    edges can crawl on noisy sources. A clean engine render is about the best case
    for it.

    Authored geometry is the way out of the scale problem estimated depth has. Depth
    from real footage carries the real scene's scale relationships with it, so
    restyling desk-height boxes yields desk-height rocks no matter what the prompt
    says. Geometry built at canyon scale, with a camera move to match, does not.
    """
    g.drop_node(N_SLICE)
    g.drop_node(N_MOGE)
    g.wf["definitions"]["subgraphs"] = [
        s for s in g.wf["definitions"]["subgraphs"] if s["id"] != MOGE_SUB
    ]

    n_comp = g.add_node(
        "GetVideoComponents", [-100, 3030],
        [{"name": "video", "type": "VIDEO", "link": None}],
        [{"name": "images", "type": "IMAGE", "links": []},
         {"name": "audio", "type": "AUDIO", "links": []},
         {"name": "fps", "type": "FLOAT", "links": []},
         {"name": "bit_depth", "type": "INT", "links": []}],
        [])
    g.link(N_LOADVID, 0, n_comp, 0, "VIDEO")

    if control_mode == "passthrough":
        n_out, out_slot = n_comp, 0
    elif control_mode == "pose":
        n_out = g.add_node(
            "OpenposePreprocessor", [300, 3030],
            [{"name": "image", "type": "IMAGE", "link": None}],
            [{"name": "IMAGE", "type": "IMAGE", "links": []},
             {"name": "POSE_KEYPOINT", "type": "POSE_KEYPOINT", "links": []}],
            ["enable", "enable", "enable", pose_resolution, "disable"])
        g.link(n_comp, 0, n_out, 0, "IMAGE")
        out_slot = 0
    elif control_mode == "canny":
        n_out = g.add_node(
            "Canny", [300, 3030],
            [{"name": "image", "type": "IMAGE", "link": None}],
            [{"name": "IMAGE", "type": "IMAGE", "links": []}],
            [canny_low, canny_high])
        g.link(n_comp, 0, n_out, 0, "IMAGE")
        out_slot = 0
    else:
        n_vda = g.add_node(
            "LoadVideoDepthAnythingModel", [-100, 3260], [],
            [{"name": "vda_model", "type": "VDAMODEL", "links": []}],
            [vda_model])
        n_proc = g.add_node(
            "VideoDepthAnythingProcess", [300, 3030],
            [{"name": "vda_model", "type": "VDAMODEL", "link": None},
             {"name": "images", "type": "IMAGE", "link": None}],
            [{"name": "depths", "type": "DEPTHS", "links": []}],
            [input_size, max_res, precision])
        n_out = g.add_node(
            "VideoDepthAnythingOutput", [700, 3030],
            [{"name": "depths", "type": "DEPTHS", "link": None}],
            [{"name": "images", "type": "IMAGE", "links": []}],
            ["gray"])
        g.link(n_vda, 0, n_proc, 0, "VDAMODEL")
        g.link(n_comp, 0, n_proc, 1, "IMAGE")
        g.link(n_proc, 0, n_out, 0, "DEPTHS")
        out_slot = 0

    g.link(n_out, out_slot, N_FLF, 1, "IMAGE")       # -> control_images
    g.link(n_out, out_slot, N_PREVIEW, 0, "IMAGE")   # -> PreviewImage
    return n_out


def splice_distill_lora(sg, lora_name, strength):
    """Insert LoraLoaderModelOnly between the checkpoint and the IC-LoRA loader."""
    nid = max(n["id"] for n in sg["nodes"]) + 1
    lid = max((l["id"] for l in sg["links"]), default=0) + 1

    sg["nodes"].append(_mk(
        nid, "LoraLoaderModelOnly", [400, 3020],
        [{"name": "model", "type": "MODEL", "link": None}],
        [{"name": "MODEL", "type": "MODEL", "links": []}],
        [lora_name, strength]))

    # the checkpoint's MODEL currently lands on the IC-LoRA loader; divert it
    feed = next(l for l in sg["links"] if l["target_id"] == I_ICLORA and l["target_slot"] == 0)
    feed["target_id"] = nid
    inner = {n["id"]: n for n in sg["nodes"]}
    inner[nid]["inputs"][0]["link"] = feed["id"]

    sg["links"].append({"id": lid, "origin_id": nid, "origin_slot": 0,
                        "target_id": I_ICLORA, "target_slot": 0, "type": "MODEL"})
    inner[nid]["outputs"][0]["links"] = [lid]
    inner[I_ICLORA]["inputs"][0]["link"] = lid
    return nid


def pin_latent_shapes(sg, width, height, frames, fps):
    """Set the two Empty*Latent nodes from explicit widgets instead of links.

    LTXVEmptyLatentAudio declares `frame_rate` as an io.MultiType (Float accepting
    Int). comfy-cli's UI->API conversion does not consume a widgets_values entry for
    a MultiType input: it leaves frame_rate at the schema default and passes the
    value that was meant for it on to the NEXT widget. So widgets_values[1] lands on
    `batch_size`. Verified against the submitted prompt in ComfyUI's /history:

        "frames_number": 121, "frame_rate": 25.0, "batch_size": 24

    The audio latent is shaped (batch_size, z_channels, num_audio_latents,
    audio_freq) (comfy_extras/nodes_lt_audio.py), so a wrong batch_size makes dim 0
    disagree with the video latent and comfy.utils.pack_latents fails concatenating
    them. The symptom is remote from the cause -- the run dies inside KSampler with
    "Sizes of tensors must match except in dimension 2. Expected size 1 but got size
    25", naming neither the node nor the widget responsible. The failing number
    tracks widgets_values[1] exactly: editing the frame rate walked it 25 -> 24, and
    padding the list walked it to 121.

    So frame_rate has to arrive by LINK (links convert correctly), and
    widgets_values carries just [frames_number, batch_size]. The template also omits
    the trailing `batch_size` socket on both latent nodes, which
    LTX23_i2v_official.json -- known good on this machine -- has; it is restored here
    so the graph reopens cleanly in the UI.

    EmptyLTXVLatentVideo has no MultiType input and pairs correctly, so its values
    are simply written out. That does mean `frames` must match the control clip by
    hand.
    """
    inner = {n["id"]: n for n in sg["nodes"]}

    def unlink(nid, slot):
        node = inner[nid]
        lid = node["inputs"][slot].get("link")
        if lid is None:
            return
        node["inputs"][slot]["link"] = None
        for l in [l for l in sg["links"] if l["id"] == lid]:
            sg["links"].remove(l)
            src = inner[l["origin_id"]]["outputs"][l["origin_slot"]]
            if src.get("links") and lid in src["links"]:
                src["links"].remove(lid)

    def restore_batch_size(nid):
        node = inner[nid]
        if any(i["name"] == "batch_size" for i in node["inputs"]):
            return
        node["inputs"].append({"localized_name": "batch_size", "name": "batch_size",
                               "type": "INT", "widget": {"name": "batch_size"},
                               "link": None})

    unlink(I_AUDIOLATENT, 1)                 # frames_number; frame_rate stays LINKED
    restore_batch_size(I_AUDIOLATENT)
    inner[I_AUDIOLATENT]["widgets_values"] = [frames, 1]

    for slot in range(len(inner[I_VIDLATENT]["inputs"])):
        unlink(I_VIDLATENT, slot)            # width, height, length
    restore_batch_size(I_VIDLATENT)
    inner[I_VIDLATENT]["widgets_values"] = [width, height, frames, 1]


def build(prompt_text, name, video, plate, width, height, frames, ckpt, audio_vae, fps,
          distill_lora, distill_strength, ic_strength, steps, cfg, seed, control_mode,
          vda_model, input_size, max_res, precision, canny_low, canny_high,
          pose_resolution, negative):
    # The IC-LoRA carries reference_downscale_factor 2, and LTXVAddGuide demands the
    # latent (w/32, h/32) divide by it -- so /32 is not enough, it has to be /64.
    # 1120x640 validates clean and then dies at runtime with "Latent spatial size
    # 35x20 must be divisible by reference_downscale_factor 2".
    for label, v in (("width", width), ("height", height)):
        if v % 64:
            raise SystemExit(f"{label}={v} must be a multiple of 64 for the IC-LoRA "
                             f"(latent {v // 32} would be odd); try {v // 64 * 64}")

    wf = json.load(open(TEMPLATE, encoding="utf-8"))
    g = Graph(wf)

    rebuild_depth_branch(g, control_mode, vda_model, input_size, max_res, precision,
                         canny_low, canny_high, pose_resolution)

    # the promoted `text` input has no inner widget fallback - drive it for real
    n_txt = g.add_node("PrimitiveStringMultiline", [-660, 2700], [],
                       [{"name": "STRING", "type": "STRING", "links": []}],
                       [prompt_text])
    g.link(n_txt, 0, N_FLF, 2, "STRING")

    g.node(N_LOADVID)["widgets_values"][0] = video
    g.node(N_LOADIMG)["widgets_values"][0] = plate
    g.node(N_SAVE)["widgets_values"][0] = f"video/V2V_{name}"
    g.finish()

    sg = {s["id"]: s for s in wf["definitions"]["subgraphs"]}[FLF_SUB]
    splice_distill_lora(sg, distill_lora, distill_strength)
    inner = {n["id"]: n for n in sg["nodes"]}

    inner[I_CKPT]["widgets_values"][0] = ckpt
    # The template pulls the audio VAE out of its monolithic distilled checkpoint. The
    # dev checkpoint we substitute does not carry an equivalent one, and the mismatch
    # only shows up at the very end, as a pack_latents concat failure in KSampler
    # ("Expected size 1 but got size 25") when the audio latent comes back the wrong
    # rank. This install ships a standalone audio VAE; point at that instead.
    inner[I_AUDIOVAE]["widgets_values"][0] = audio_vae
    inner[I_TEXTENC]["widgets_values"][1] = ckpt
    # drives LTXVConditioning.frame_rate, the audio latent's frame_rate and CreateVideo
    # fps; the template ships 25 and our control clips are 24
    inner[I_FPS]["widgets_values"][0] = fps
    inner[I_W]["widgets_values"][0] = width
    inner[I_H]["widgets_values"][0] = height
    pin_latent_shapes(sg, width, height, frames, fps)
    inner[I_ICLORA]["widgets_values"][1] = ic_strength
    inner[I_NEG]["widgets_values"][0] = negative
    ks = inner[I_KSAMPLER]["widgets_values"]      # [seed, after_gen, steps, cfg, sampler, sched, denoise]
    ks[0], ks[1], ks[2], ks[3] = seed, "fixed", steps, cfg

    dst = os.path.join(WF_DIR, f"v2v_ltx_{name}.json")
    json.dump(wf, open(dst, "w", encoding="utf-8"), indent=2)
    return dst


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--video", required=True, help="filename in ComfyUI/input - drives the depth control")
    p.add_argument("--plate", required=True, help="filename in ComfyUI/input - becomes first_frame")
    p.add_argument("--width", type=int, default=1088)
    p.add_argument("--height", type=int, default=640)
    p.add_argument("--frames", type=int, default=121,
                   help="MUST equal the control clip's frame count; LTX wants 8k+1")
    p.add_argument("--ckpt", default="ltx-2.3-22b-dev-fp8.safetensors")
    p.add_argument("--audio-vae", default="LTXV2\\LTX23_audio_vae_bf16.safetensors")
    p.add_argument("--fps", type=int, default=24)
    p.add_argument("--distill-lora", default="ltx-2.3-22b-distilled-lora-384.safetensors")
    p.add_argument("--distill-strength", type=float, default=0.5)
    p.add_argument("--ic-strength", type=float, default=1.0,
                   help="IC-LoRA guide adherence; higher tracks the depth harder")
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("--cfg", type=float, default=1.0)
    p.add_argument("--seed", type=int, default=-1)
    p.add_argument("--control-mode", default="estimate",
                   choices=["estimate", "canny", "pose", "passthrough"],
                   help="estimate: run VideoDepthAnything over --video (ordinary footage). "
                        "canny: edge-detect it instead, keeping design lines depth loses. "
                        "pose: OpenPose skeleton only - motion without silhouette, for "
                        "replacing a performer with a body of different proportions. "
                        "passthrough: --video IS the control pass already (a Blender/Unity "
                        "depth render, or untextured/clay geometry)")
    p.add_argument("--canny-low", type=float, default=0.4)
    p.add_argument("--canny-high", type=float, default=0.8)
    p.add_argument("--pose-resolution", type=int, default=1024)
    p.add_argument("--vda-model", default="video_depth_anything_vits.pth")
    p.add_argument("--input-size", type=int, default=518)
    p.add_argument("--max-res", type=int, default=1280)
    p.add_argument("--precision", default="fp16", choices=["fp16", "fp32"])
    p.add_argument("--negative", default="blurry, out of focus, overexposed, underexposed, "
                                         "low contrast, washed out colors, excessive noise")
    a = p.parse_args()

    seed = random.randint(0, 2**48) if a.seed < 0 else a.seed
    text = open(a.prompt, encoding="utf-8").read().strip()
    if (a.frames - 1) % 8:
        raise SystemExit(f"--frames {a.frames} is off LTX's 8k+1 grid; try {(a.frames - 1) // 8 * 8 + 1}")

    dst = build(text, a.name, a.video, a.plate, a.width, a.height, a.frames, a.ckpt,
                a.audio_vae, a.fps, a.distill_lora, a.distill_strength, a.ic_strength,
                a.steps, a.cfg, seed, a.control_mode, a.vda_model, a.input_size,
                a.max_res, a.precision, a.canny_low, a.canny_high,
                a.pose_resolution, a.negative)
    print("wrote", dst)
    print(f"  control video = {a.video}  (its frame count sets the output length)")
    print(f"  first_frame   = {a.plate}")
    print(f"  {a.width}x{a.height}  {a.frames}f  steps={a.steps}  cfg={a.cfg}  seed={seed}")
    print(f"  ckpt={a.ckpt}  audio_vae={a.audio_vae}  fps={a.fps}")
    print(f"  distill_lora={a.distill_lora} @{a.distill_strength}  ic_lora @{a.ic_strength}")
    if a.control_mode == "passthrough":
        print("  control=passthrough (video used AS control_images, no depth estimation)")
    elif a.control_mode == "canny":
        print(f"  control=canny  low={a.canny_low} high={a.canny_high}")
    elif a.control_mode == "pose":
        print(f"  control=pose (OpenPose skeleton)  resolution={a.pose_resolution}")
    else:
        print(f"  control=estimate  depth={a.vda_model} input_size={a.input_size} "
              f"max_res={a.max_res} {a.precision}")
    print(f"  prompt chars={len(text)}")
