"""Slice audio, stage inputs and queue every act 2 shot (verse 2 to the end) in ref2va.

Each spec: slot start in the song, render length, which stem to pin (full mix for
anyone singing, instrumental where nobody should lip-sync), refs in <Picture> order,
and an optional AddGuide image pinned at frame 0.
  python queue_act2.py            # queue all
  python queue_act2.py shot9a_tv  # queue just these
"""
import json, os, shutil, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from build_beat_test import build, queue, frames_for

SONG = r"audio\No Fucks at All.mp3"
INST = r"audio\stems\htdemucs\No Fucks at All\no_vocals.wav"
COMFY_IN = r"D:\Projects_26\Comfyu\ComfyUI\input"

S, G, D = "singer_ref_combo.png", "guitarist_ref_combo.png", "drummer_ref_combo.png"
GS = "gsuit_combo.png"
BAND, OFFICE = "set_s1_bandstage_00002_.png", "set_s3_office_00001_.png"
LIVING, CHAPEL, BRIDGE = "set_livingroom_00002_.png", "set_chapel_00001_.png", "set_bridge_00002_.png"
SHIP, GROOMS, ROBOT, GORILLA = ("spaceship_model_00002_.png", "grooms_00002_.png", "robot_sheet_00002_.png",
                                "gorilla_sheet_00001_.png")
CHEST, WORD = "prop_chest_00001_.png", "prop_gold_word_00001_.png"
AUD, STUDIO = "audience_lineup_master.png", "studio_wide_final.png"
CREW = "crew_lineup_00002_.png"

# name: (slot start, render seconds, stem, refs, guide image)
SPECS = {
    "shot8a_boss":        (86.796, 8.731, "mix", [S, GS, OFFICE], None),
    "shot8b_nope":        (95.527, 5.340, "mix", [S, GS, OFFICE], None),
    "shot8c_dance":       (100.867, 9.242, "mix", [S, OFFICE, BAND, D], None),
    "shot9a_tv":          (110.109, 9.30, "inst", [D, CHEST, WORD, LIVING], None),
    "shot9b_chapel":      (110.109, 9.30, "inst", [G, GROOMS, CHEST, WORD, CHAPEL], None),
    "shot10a_chorus":     (125.643, 7.756, "mix", [S, G, D, BAND], None),
    "shot10b_chorus":     (133.399, 6.269, "mix", [S, G, D, BAND], None),
    "shot11a_tv_sad":     (139.668, 6.30, "inst", [D, CHEST, WORD, LIVING], None),
    "shot11b_chapel_sad": (139.668, 6.30, "inst", [G, GROOMS, CHEST, WORD, CHAPEL], None),
    "shot12a_ship":       (151.208, 5.0, "inst", [SHIP], None),
    "shot12b_bridge":     (156.038, 8.150, "mix", [S, D, G, ROBOT, BRIDGE], None),
    "shot12c_robot":      (164.188, 11.494, "mix", [ROBOT, S, BRIDGE], "robot_bridge_frame.png"),
    "shot12d_robot":      (175.682, 8.847, "mix", [ROBOT, S, BRIDGE], None),
    "shot12e_captain":    (184.529, 5.0, "mix", [S, BRIDGE], None),
    "shot13a_chorus":     (187.130, 13.839, "mix", [S, G, D, BAND], None),
    "shot13b_rush":       (200.969, 5.0, "inst", [AUD, GROOMS, GORILLA, STUDIO, BAND], None),
    "shot13c_line":       (205.264, 12.423, "mix", [S, AUD, GROOMS, GORILLA, G, D, BAND], None),
    "shot13c_line_v2":    (205.264, 12.423, "mix", [S, AUD, GROOMS, GORILLA, G, D, BAND], None),
    "shot14_all":         (217.687, 11.540, "mix", [S, G, D, AUD, GROOMS, GORILLA, ROBOT, BAND], None),
    "shot14_all_v2":      (217.687, 11.540, "mix", [S, G, D, AUD, GROOMS, GORILLA, ROBOT, BAND], "finale_stage_frame.png"),
    "shot14_ecu":         (217.687, 11.540, "mix", [S, BAND], None),
    "shot14_end":         (229.227, 12.453, "inst", [ROBOT, STUDIO], "end_frame_master.png"),
    # pickups: closer moving dance line (pinned to crops of the wide take) and opening crew inserts
    "shot13c_line_A":     (205.264, 12.423, "mix", [S, AUD, GROOMS, GORILLA, BAND], "line_close_left.png"),
    "shot13c_line_B":     (205.264, 12.423, "mix", [S, AUD, GROOMS, GORILLA, BAND], "line_close_right.png"),
    # v2: both ends pinned so the stage never leaves frame; grey-backed sheets dropped
    "shot13c_line_A2":    (205.264, 12.423, "mix", [S, BAND], "line_close_left.png", "line_close_right.png"),
    "shot13c_line_B2":    (205.264, 12.423, "mix", [S, BAND], "line_close_right.png", "line_close_left.png"),
    "shot12b_bridge_v2":  (156.038, 8.150, "mix", [S, D, G, ROBOT, BRIDGE], None),
    "crew_flat":          (3.924, 5.0, "mix", [CREW, STUDIO], None),
    "crew_light":         (7.848, 5.0, "mix", [CREW, STUDIO], None),
    "crew_countdown":     (9.799, 5.0, "mix", [CREW, STUDIO], None),
}


def stage(path):
    shutil.copy(path, os.path.join(COMFY_IN, os.path.basename(path)))


def run(names):
    os.makedirs("audio/act2", exist_ok=True)
    stage("refs/act2/end_frame_master.png")
    ids = {}
    for i, name in enumerate(names):
        start, secs, stem, refs, guide, *rest = SPECS[name]
        guide_end = rest[0] if rest else None
        render_s = frames_for(secs) / 24
        wav = f"audio/act2/{name}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", f"{render_s + 0.4:.3f}",
                        "-i", SONG if stem == "mix" else INST, "-ac", "2", "-ar", "44100", wav], check=True)
        stage(wav)
        text = open(f"prompts/shots/{name}.txt", encoding="utf-8").read().strip()
        seed = 1100 + list(SPECS).index(name)
        g = build(text, name, 1120, 640, secs, seed, 20, "beta", audio=os.path.basename(wav),
                  refs=refs, guide_image=guide, guide_end=guide_end)
        ids[name] = queue(g).get("prompt_id")
        print(f"{name:20s} {frames_for(secs)} f  {stem}  refs={len(refs)}  seed={seed}  {ids[name]}")
    json.dump(ids, open("audio/act2/queued.json", "w"), indent=1)


if __name__ == "__main__":
    run(sys.argv[1:] or list(SPECS))
