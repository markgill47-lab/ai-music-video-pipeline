"""Slice the instrumental, stage inputs and queue Grounded shots in H3 ref2va.

Every shot pins the instrumental stem (nobody sings). Slots are beat indices into
audio/beats_full.json; renders run min(slot, 15.08 s). Each spec: (first beat, last beat,
refs in <Picture> order, guide image at frame 0, optional guide at the last frame).
  python queue_shots.py              # queue all
  python queue_shots.py s10_mirror   # queue just these
  python queue_shots.py --seed-offset 50 s10_mirror   # re-roll with a new seed
  python queue_shots.py --front ...                   # jump the queue
"""
import json, os, shutil, subprocess, sys, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools"))
from build_beat_test import build, queue, frames_for

INST = r"audio\stems\htdemucs\grounded\no_vocals.wav"
COMFY_IN = r"D:\Projects_26\Comfyu\ComfyUI\input"
BEATS = json.load(open("audio/beats_full.json"))["beats"]
SONG_END = 311.48
MAX_S = 362 / 24

HOME, OUT, CAPT, ALEC = "steve_home_combo.png", "steve_out_combo.png", "steve_captain_combo.png", "alec_street_combo.png"
CAST = {"a": "g_cast.png", "b": "g_cast_b.png", "c": "g_cast_c.png"}
CAB = {"a": "g_cabin_a.png", "b": "g_cabin_b.png", "c": "g_cabin_c.png"}

# name: (first beat, last beat, refs, guide at frame 0, guide at last frame)
SPECS = {
    "s01_airport":   (0, 18, ["g_airport_dawn.png"], "g_airport_dawn.png", None),
    "s01b_house":    (18, 36, ["g_house_dawn.png"], "g_house_dawn.png", None),
    "s02_bed":       (36, 68, [HOME, "g_bedroom_morning.png"], "fr_f02_bed.png", None),
    "s03_badge":     (68, 84, [HOME, "g_badge.png", "g_bedroom_morning.png"], "fr_f03_badge.png", None),
    "s04_dresser":   (84, 100, ["g_dresser_top.png"], "g_dresser_top.png", None),
    "s05_cockpit":   (100, 116, [CAPT, "g_cockpit_day.png"], "fr_f05_cockpit.png", None),
    "s06_bededge":   (116, 132, [HOME, "g_bedroom_morning.png"], "fr_f06_bededge.png", None),
    "s07_briefing":  (132, 148, [CAST["c"], "g_briefing_room.png"], "g_briefing_room.png", None),
    "s08_emptyseat": (148, 164, ["g_cockpit_2045.png"], "g_cockpit_2045.png", None),
    "s09_gate":      (164, 180, [OUT, "g_gate_window.png"], "fr_f09_gate.png", None),
    "s10_mirror":    (180, 208, [HOME, CAPT, "g_bathroom_mirror.png"], "fr_f10_mirror.png", None),
    "s11_planeA":    (208, 240, [CAB["a"]], "fr_pa_start.png", "fr_pa_end.png"),
    "s12_hall":      (240, 252, [OUT, "g_hallway.png"], "fr_f12_hall.png", None),
    "s13_tower":     (252, 284, ["g_tower.png"], "g_tower.png", None),
    "s14_apron":     (284, 300, ["g_apron_scan.png"], "g_apron_scan.png", None),
    "s15_fencewalk": (300, 316, [OUT, "g_fence.png"], "fr_f15_fence_walk.png", None),
    "s16_storm":     (316, 348, [CAPT, "g_cockpit_storm.png"], "fr_f16_storm.png", None),
    "s17_fence":     (348, 368, [OUT, "g_fence.png"], "fr_f17_fence_grip.png", None),
    "s18_face":      (368, 380, [OUT, "g_fence.png"], "fr_f18_fence_face.png", None),
    "s19_wide":      (380, 396, [OUT, "g_fence.png"], "fr_f19_fence_wide.png", None),
    "s20_planeB":    (396, 428, [CAB["b"]], "fr_pb_start.png", "fr_pb_end.png"),
    "s21_concourse": (428, 460, [OUT, "g_concourse_dusk.png"], "fr_f21_concourse.png", None),
    "s22_departure": (460, 476, [OUT, "g_departure_hall.png"], "g_departure_hall.png", "fr_f22_hall.png"),
    "s23a_flyby":    (476, 492, ["g_storm_plane2.png"], "g_storm_plane2.png", None),
    "s23b_cockpit":  (492, 504, ["g_cockpit_storm2045.png"], "g_cockpit_storm2045.png", None),
    "s23c_window":   (504, 520, [OUT, "g_window_night.png"], "fr_f23c_window.png", None),
    "s24_cafe":      (520, 552, [OUT, "g_cafe_evening.png"], "fr_f24_cafe.png", None),
    "s25_alec":      (552, 580, [OUT, ALEC, "g_cafe_evening.png"], "fr_f25_noplane.png", None),
    "s26_two":       (580, 600, [OUT, ALEC, "g_cafe_evening.png"], "fr_f26_noplane.png", None),
    "s26b_takeoff":  (600, 614, ["g_takeoff_night.png"], "g_takeoff_night.png", None),
    "s27_planeC":    (614, 648, [CAB["c"]], "fr_pc_start.png", "fr_pc_end.png"),
    "s28_night":     (648, None, [HOME, "g_badge.png", "g_bedroom_night.png"], "fr_f28_badge.png", None),
}
SEED0 = 4500
PLANE_SEED = 4545      # all three planes share one seed so the camera move matches


def slot(name):
    a, b = SPECS[name][:2]
    start = BEATS[a]
    end = BEATS[b] if b is not None else SONG_END
    return start, end


def submit(g, front=False):
    body = {"prompt": g, "front": True} if front else {"prompt": g}
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


def run(names, seed_offset=0, front=False):
    os.makedirs("audio/shots", exist_ok=True)
    ids = json.load(open("audio/shots/queued.json")) if os.path.exists("audio/shots/queued.json") else {}
    for name in names:
        a, b, refs, guide, guide_end = SPECS[name]
        start, end = slot(name)
        secs = min(end - start, MAX_S)
        secs = max(secs, 5.0)
        render_s = frames_for(secs) / 24
        wav = f"audio/shots/{name}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{render_s + 0.4:.3f}",
                        "-i", INST, "-ac", "2", "-ar", "44100", wav], check=True)
        shutil.copy(wav, os.path.join(COMFY_IN, os.path.basename(wav)))
        text = open(f"prompts/shots/{name}.txt", encoding="utf-8").read().strip()
        seed = (PLANE_SEED if "plane" in name else SEED0 + list(SPECS).index(name)) + seed_offset
        tag = name if not seed_offset else f"{name}_r{seed_offset}"
        g = build(text, tag, 1120, 640, secs, seed, 20, "beta", audio=os.path.basename(wav),
                  refs=refs, guide_image=guide, guide_end=guide_end)
        ids[tag] = submit(g, front).get("prompt_id")
        print(f"{tag:22s} {start:7.2f}-{end:7.2f}  {frames_for(secs)} f  refs={len(refs)}  seed={seed}")
    json.dump(ids, open("audio/shots/queued.json", "w"), indent=1)


if __name__ == "__main__":
    args = sys.argv[1:]
    off, front = 0, False
    if args[:1] == ["--front"]:
        front, args = True, args[1:]
    if args[:1] == ["--seed-offset"]:
        off, args = int(args[1]), args[2:]
    run(args or list(SPECS), off, front)
