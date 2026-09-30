"""First frames for Grounded (Flux 2 Klein multi-reference via tools/build_flux_multiref.py).
Each frame: environment plate (sets resolution), up to three character refs, one prompt.
Run from the project folder: python prompts/frames/make_frames.py [names...]  then queue flux_fr_<name>.json"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = r"D:\Projects_26\Comfyu\ComfyUI\venv\Scripts\python.exe"
BUILD = os.path.join(HERE, "..", "..", "..", "..", "..", "tools", "build_flux_multiref.py")

HOME, OUT, CAPT = "steve_home_combo.png", "steve_out_combo.png", "steve_captain_combo.png"
FACE, FFACE = "steve_face_master.png", "steve_flashback_master.png"
ALEC, AFACE = "alec_street_combo.png", "alec_face_master.png"

S_NOW = ("the man from image 2: about sixty, broad square face, heavy brows, grey-blue eyes, shaggy salt-and-pepper "
         "hair over his ears and a short grey beard")
S_CAPT = ("the airline captain from image 2: about fifty-five, broad square face, heavy brows, grey-blue eyes, short "
          "neat dark salt-and-pepper hair, clean-shaven, in his navy captain's uniform")
SEED = {"pc_start": 777}
TAIL = " Photorealistic cinematic film still, 35mm film, fine grain, natural colour."
KEEP = "Keep the room, furniture, camera angle and light of image 1 exactly."

# name: (env, [refs...], prompt)
FRAMES = {
    "f02_bed": ("g_bedroom_morning.png", [HOME, FACE],
        f"Image 1 is the bedroom. Place {S_NOW}, in the same faded navy henley t-shirt and shorts, lying on his back "
        f"on top of the unmade bed, fully awake, staring at the ceiling, one arm behind his head. {KEEP}"),
    "f03_badge": ("g_bedroom_morning.png", [HOME, "g_badge.png", FACE],
        "Image 1 is the bedroom. A close-up of the man from image 2 (about sixty, broad square face, heavy brows, "
        "shaggy salt-and-pepper hair, short grey beard, faded navy henley), sitting on the edge of the bed in the "
        "morning light, looking down at the airline crew ID badge from image 3 held flat in his open palm in the "
        "foreground: a white plastic photo ID card with a navy stripe, gold wings and the word CAPTAIN, in sharp focus, "
        "his face soft behind it. The bedroom soft and out of focus behind him."),
    "f05_cockpit": ("g_cockpit_day.png", [CAPT, FFACE],
        f"Image 1 is the cockpit. Place {S_CAPT} and his black captain's cap, in the left pilot seat, seen from "
        "behind and to the right so his face is in three-quarter view, one hand resting easily on the side-stick, "
        "smiling toward the empty right seat, brilliant sun on the cloud tops ahead. Keep the cockpit and the "
        "view of image 1."),
    "f06_bededge": ("g_bedroom_morning.png", [HOME, FACE],
        f"Image 1 is the bedroom. Place {S_NOW}, in the same faded navy henley and shorts, sitting slumped on the "
        f"edge of the unmade bed facing the camera, shoulders down, forearms on his knees, the small silver badge "
        f"loose in one hand, staring at the floor. {KEEP}"),
    "f09_gate": ("g_gate_window.png", [OUT, FACE],
        f"Image 1 is the departure gate. Place {S_NOW}, in his worn brown leather flight jacket with a sheepskin "
        "collar over a navy henley, standing at the tall window in the foreground on the left in three-quarter view, "
        "looking up at the slim ceiling speaker grille with a puzzled, pained expression. Keep the gate, the "
        "airliner and the light of image 1."),
    "f10_mirror": ("g_bathroom_mirror.png", [HOME, CAPT, FACE],
        "Image 1 is the bathroom. The man from image 2, about sixty with shaggy salt-and-pepper hair and a short "
        "grey beard, in his faded navy henley and baggy shorts, stands at the sink facing the mirror, seen from "
        "behind his shoulder. In the mirror his reflection is not him as he is now: the reflection is the airline "
        "captain from image 3, the same man younger, clean-shaven, with short neat hair, in the navy captain's "
        "uniform and peaked cap, standing tall and looking straight back at him. The reflection is clearly "
        "visible and sharp. Keep the bathroom of image 1."),
    "f12_hall": ("g_hallway.png", [OUT, FACE],
        f"Image 1 is the hallway. Place {S_NOW}, in a navy henley and jeans, in the middle of the hallway facing the "
        "camera, pulling on the brown leather flight jacket with the sheepskin collar, the leather logbook on the "
        f"table beside him. {KEEP}"),
    "f15_fence_walk": ("g_fence.png", [OUT, FACE],
        f"Image 1 is the airport fence. Place {S_NOW}, in his worn brown leather flight jacket, jeans and boots, "
        "walking along the cracked footpath beside the fence toward the camera, hands in his jacket pockets, "
        "looking up at the airliner climbing overhead. Keep the fence, runway and sky of image 1."),
    "f16_storm": ("g_cockpit_storm.png", [CAPT, FFACE],
        f"Image 1 is the cockpit in a storm. Place {S_CAPT}, without his cap, in the left pilot seat, seen from "
        "behind and to the right so his face is in three-quarter view, lit by the amber panel light and a flash "
        "of lightning, jaw set, eyes locked on the runway lights ahead, one hand gripping the side-stick and the "
        "other on the throttles. Keep the storm, rain and cockpit of image 1."),
    "f17_fence_grip": ("g_fence.png", [OUT, FACE],
        f"Image 1 is the airport fence. A low angle from behind and to the left of {S_NOW}, in his worn brown "
        "leather flight jacket, standing close to the fence with the fingers of one hand hooked through the wire, "
        "watching the airliner lift off from the runway beyond. His face in profile. Keep the fence, runway and "
        "sky of image 1."),
    "f18_fence_face": ("g_fence.png", [OUT, FACE],
        f"Image 1 is the airport fence. A close-up of {S_NOW}, in his brown leather flight jacket with the "
        "sheepskin collar, behind the chain-link fence looking up and past the camera at the sky, the wire soft "
        "in the foreground, his eyes wet, jaw tight. The runway and sky soft behind him."),
    "f19_fence_wide": ("g_fence.png", [OUT, FACE],
        "Image 1 is the airport fence. Make the view much wider and higher: a very long fence line crossing a vast "
        "airport, the runway and the distant glass terminal, and one small solitary figure, the man from image 2 "
        "in his brown leather flight jacket, standing still at the fence far away in the middle distance. Keep "
        "the light and colour of image 1."),
    "f21_concourse": ("g_concourse_dusk.png", [OUT, FACE],
        f"Image 1 is the concourse. Place {S_NOW}, in his brown leather flight jacket, in the centre walking "
        "toward the camera against the stream of travellers who all walk the other way looking down at glowing "
        "screens; he looks up and around at the glass roof. Keep the concourse and the dusk light of image 1."),
    "f22_hall": ("g_departure_hall.png", [OUT, FACE],
        f"Image 1 is the departure hall. Place {S_NOW}, in his brown leather flight jacket, at the back of the "
        "crowd in the right foreground, the only person turned away from the glowing flight board, looking out "
        "through the glass at the dusk sky. Keep the hall, the crowd and the board of image 1."),
    "f24_cafe": ("g_cafe_evening.png", [OUT, FACE],
        f"Image 1 is the airport café. Place {S_NOW}, in his brown leather flight jacket, seated alone at the "
        "window table in the foreground, an old leather logbook open in front of him beside a cup of coffee, "
        "looking out of the window at the runway. Keep the café, the window and the evening light of image 1."),
    "f25_cafe_close": ("g_cafe_evening.png", [OUT, FACE],
        f"Image 1 is the airport café. A medium close-up of {S_NOW}, in his brown leather flight jacket, at the "
        "window table with the open logbook, eyes closed, head tilted slightly toward the window, listening; an "
        "airliner climbing outside the window behind him. The empty chair across the table in the foreground left. "
        "Evening light."),
    "f26_cafe_two": ("g_cafe_evening.png", [OUT, ALEC, FACE],
        "Image 1 is the airport café at night. A two-shot at the window table: on the left the man from image 2, "
        "about sixty with shaggy salt-and-pepper hair and a short grey beard, in his brown leather flight jacket, "
        "pointing out through the window at an airliner climbing into the night sky with its lights on; on the "
        "right his teenage grandson from image 3, messy dark hair, black hoodie and olive field jacket, sitting "
        "opposite and looking down at a glowing phone in his hand. The open logbook between them. The window dark "
        "blue outside with runway lights. Keep the café of image 1."),
    "f28_night": ("g_bedroom_night.png", [HOME, FACE],
        f"Image 1 is the bedroom at night. Place {S_NOW}, in his faded navy henley and shorts, standing at the "
        "dresser in the warm lamplight, seen from the side, setting the small silver badge down on the dresser top "
        f"beside a pair of gold pilot's wings, his head bowed. {KEEP}"),
    "f28_badge": ("g_bedroom_night.png", [HOME, "g_badge.png", FACE],
        "Image 1 is the bedroom at night. Place the man from image 2 (about sixty, broad square face, shaggy "
        "salt-and-pepper hair, short grey beard, faded navy henley and shorts), standing at the dresser in the warm "
        "lamplight, seen from the side, laying the airline crew ID badge from image 3, a white photo ID card with a navy "
        "stripe and a black clip, face up on the dresser top beside a pair of gold pilot's wings, his head bowed. Keep "
        "the room, furniture, camera angle and light of image 1 exactly."),
    "f23c_window": ("g_window_night.png", [OUT, FACE],
        f"Image 1 is the terminal window at night in a storm. Place {S_NOW}, in his brown leather flight jacket, "
        "standing close to the rain-streaked glass in the right foreground in three-quarter view, looking out at the "
        "storm and the runway lights, his face lit by a flash of lightning. Keep the window, rain and night of image 1."),
}

CAB = {"a": "g_cabin_a.png", "b": "g_cabin_b.png", "c": "g_cabin_c.png"}
CAST = {"a": "g_cast.png", "b": "g_cast_b.png", "c": "g_cast_c.png"}
HANDOFF = ("Image 1 is the airliner cabin in flight; keep its seats, bins, windows, aisle, camera position and light "
           "exactly. The camera looks forward toward the cockpit, so every passenger sits facing away from the camera "
           "toward the front of the plane: we see the backs of their heads above the seat backs. The people from image 2 "
           "are aboard, wearing exactly their clothes from image 2: the tall Black flight attendant with the low bun "
           "stands in the aisle about three rows ahead of the camera, facing the camera, leaning down to hand a small bag "
           "of peanuts to the elderly white man with white hair and round tortoiseshell glasses in the left aisle seat, "
           "who turns his head up toward her so his smiling face is seen in profile. Further forward, the back of the "
           "young East Asian woman's black bob, the bald head of the man with the ginger beard, and the freckled girl "
           "with red braids kneeling on her seat and peeking back over the seat top with her rabbit. The rest of the "
           "seats filled with ordinary passengers seen from behind. The aisle continues past them to the front.")
for era in "abc":
    FRAMES[f"p{era}_start"] = (CAB[era], [CAST[era], CAST[era]], HANDOFF + (" There is exactly one flight attendant, in her elegant cream wrap uniform with a soft gold collar, and at the far end of the aisle the huge curved nose window full of clouds." if era == "c" else ""))
FRAMES["pa_end"] = ("g_cabin_a.png", ["g_pilot.png", "g_cockpit_day.png"],
    "Image 1 is the airliner cabin; image 3 is the cockpit. The view from standing in the open cockpit doorway at the "
    "front of the cabin of image 1, looking into the cockpit of image 3: the first officer from image 2, in his white "
    "short-sleeved pilot's shirt, lounges in the left pilot seat with one foot up on the edge of the panel, scrolling "
    "a smartphone with a bored smirk, his back half turned to the controls; the right seat empty; the controls moving "
    "by themselves; bright cloud tops and blue sky through the windscreen.")
FRAMES["pb_end"] = ("g_cabin_b.png", ["g_cockpit_2045.png", "g_cabin_b.png"],
    "Image 1 is the airliner cabin; image 2 is the cockpit. The view from standing in the open cockpit doorway at the "
    "front of the cabin of image 1, looking into the cockpit of image 2: two empty pale pilot seats, a seamless "
    "glowing curved display, small controls moving by themselves, bright clouds and blue sky through the windscreen. "
    "Nobody in the cockpit. The door frame edges visible at the sides of the frame.")
FRAMES["pc_end"] = ("g_cabin_c.png", ["g_cast_c.png", "g_cabin_c.png"],
    "Image 1 is the airliner cabin; keep its cream seats, warm light and style. The view from the front row of seats "
    "looking forward into the nose of the plane, where there is no cockpit: an open lounge with a soft cream bench "
    "and one enormous curved wraparound window filling the whole nose, showing bright clouds passing below and deep "
    "blue sky. The young East Asian woman with the black bob, the bald man with the ginger beard and the freckled girl "
    "with red braids from image 2, in their clothes from image 2, stand at the window with their backs half turned, "
    "looking out at the clouds, the girl pressing one hand to the glass.")


def main(names):
    for n in names:
        env, refs, prompt = FRAMES[n]
        refs = refs + [env] * (3 - len(refs))
        path = os.path.join(HERE, f"{n}.txt")
        open(path, "w", encoding="utf-8").write(prompt + TAIL)
        cmd = [PY, BUILD, "--prompt", path, "--name", f"fr_{n}", "--ref1", env, "--ref2", refs[0], "--ref3", refs[1],
               "--batch", "2", "--steps", "8", "--seed", str(SEED.get(n, -1))]
        if len(FRAMES[n][1]) == 3:
            cmd += ["--ref4", refs[2]]
        subprocess.run(cmd, check=True, capture_output=True)
        print("built", n)


if __name__ == "__main__":
    main(sys.argv[1:] or list(FRAMES))
