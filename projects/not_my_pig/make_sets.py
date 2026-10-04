"""Krea 2 plates for every location (empty sets, people added later in the Flux first frames).
  python make_sets.py [names...]      # build + queue, 2 takes each, output plates/nmp_set_<name>_*
Purple is kept out of the sets on purpose: the singer is the only purple thing in the picture."""
import os, subprocess, sys
sys.path.insert(0, os.path.join("..", "..", "tools"))
import build_plate

LOOK = ("Shot like a glossy late-1990s R&B music video: vivid saturated colour in warm reds, oranges, yellows and teal, "
        "crisp bright lighting, a wide-angle lens, 35mm film, fine grain. Photorealistic.")
SETS = {
    "skyline": "A wide view at sunrise of a tall old red-brick apartment block in a big American city, dozens of windows across its "
               "face with lights on in many of them, fire escapes zigzagging down the front, the orange sun just rising behind the "
               "skyline, steam rising from rooftop vents, a busy street at its foot.",
    "window": "Seen from outside, a close view of one apartment window in a red-brick building in the morning: a white-framed sash "
              "window with the lower half pushed open, a small cluttered yellow kitchen inside lit by morning sun, a fire escape "
              "railing across the bottom of the frame.",
    "hallway": "A long apartment building hallway in the morning: worn orange-and-brown patterned carpet runner, cream walls, a row "
               "of numbered apartment doors on the left, the nearest door painted glossy purple with a brass number 4B and a woven "
               "doormat in front of it, the door opposite painted green, warm ceiling lights, a window at the far end.",
    "stoop": "The front stoop of a red-brick apartment building on a city street in the morning: six stone steps down to the "
             "sidewalk, black iron railings, a heavy wooden front door with glass panes, trash cans at the curb, parked cars, "
             "bright low morning sun.",
    "sidewalk": "A busy downtown city sidewalk in the morning seen straight down its length, wide pavement, shop fronts with "
                "striped awnings, a hot-dog cart, a yellow taxi at the curb, street signs, pigeons, tall buildings either side, "
                "bright low morning sun raking across.",
    "coffee": "Inside a crowded, busy city coffee shop in the morning: a long counter with an espresso machine hissing steam, a "
              "chalkboard menu, a pastry case, orange and teal tiles, a pickup counter with paper cups lined up, morning sun "
              "through the front window.",
    "gridlock": "A city intersection in rush-hour gridlock in the morning, seen from the middle of the road at head height: lanes of "
                "stopped yellow taxis, cars, a delivery truck and a city bus jammed bumper to bumper, traffic lights, a crosswalk, "
                "tall buildings, exhaust haze glowing in the low sun.",
    "tower": "The street front of a glass office tower in the morning: a big brass-and-glass revolving door in the centre, a "
             "polished granite entrance, the tower's glass reflecting the sky, busy sidewalk in front.",
    "office": "A big open-plan office in the daytime: rows of grey cubicles, beige computers, piles of paper, fluorescent ceiling "
              "lights, a water cooler, a photocopier, a corridor running down the middle, a wall clock, a hanging sign over a "
              "doorway at the far end, tall windows with the city behind.",
    "desk": "Close view of one tidy office desk in an open-plan office in the daytime, seen from the front at seated height: a "
            "laptop, a small potted plant, a neat pen pot, an empty desk chair behind it, grey cubicle walls covered in other "
            "people's sticky notes around it, fluorescent light.",
    "market": "A long supermarket aisle in the late afternoon, bright fluorescent light, shelves packed with colourful boxes, "
              "cans and bottles, orange price signs hanging overhead, a polished white floor, shopping trolleys at the far end.",
    "checkout": "The self-checkout area of a big supermarket: a row of self-service checkout machines with screens and bagging "
                "areas, red and yellow sale signs, a big wire bin of discounted goods with a '50% OFF' sign, bright fluorescent light.",
    "carpark": "The exit of a supermarket car park in the late afternoon: a small ticket booth with a sliding window, a red-and-white "
               "striped barrier arm across the lane, rows of parked cars, the supermarket sign behind, warm low sun.",
    "suburb": "A leafy suburban street at golden-hour sunset, warm orange light, neat front lawns, white picket fences, parked "
              "cars, long shadows across the sidewalk, a backyard gate in a wooden fence with balloons tied to it.",
    "party": "A crowded suburban backyard party at sunset: string lights, a smoking barbecue grill, a long table with a big "
             "frosted birthday cake and paper plates, a kiddie pool, balloons, lawn chairs, a wooden fence and gate at the back, "
             "warm orange light.",
    "night": "A residential city street at night: warm streetlights, rows of apartment buildings with lit windows, parked cars, a "
             "fire hydrant at the curb, wet reflective pavement, a corner shop's neon sign glowing red.",
    "nightclub": "A city street at night outside a nightclub: a long queue of people behind a velvet rope, a big bouncer at the "
                 "door, a red and orange neon sign, a subway entrance with a lit green globe on the corner, puddles reflecting the neon.",
    "subway": "An underground subway platform late at night: white tiled walls, yellow safety line along the platform edge, a "
              "glowing vending machine against the wall, benches, fluorescent lights, a few late-night passengers.",
    "living": "A cozy small city apartment living room at night: a big plush purple velvet sofa, a warm table lamp beside it, "
              "plants, framed records on the wall, a window with the city's lights outside and curtains open, warm calm light.",
}

# rough cut v1: Flux/Krea garbled the signs ("BA ANC", "SALESNDE", "VUSSPEST"); the same sets with the words spelled out
SETS["night2"] = SETS["night"].replace("a corner shop's neon sign glowing red.", 'a corner deli with a red neon sign that reads "DELI" in big glowing letters, its window full of snacks.')
SETS["checkout2"] = SETS["checkout"].replace("red and yellow sale signs", 'red and yellow hanging signs that read "SALE"').replace("'50% OFF' sign", '"50% OFF" sign')
SETS["carpark2"] = SETS["carpark"].replace("the supermarket sign behind", 'the supermarket behind with a big red sign that reads "FOOD MART"')
SETS["window_b"] = ("Seen from outside, a close view of one wide-open apartment window in a pale blue-painted wooden wall in the "
                     "morning: tall green wooden shutters folded back on either side, no glass or frame bars in the opening at "
                     "all, a terracotta flower box on the sill, a small cluttered yellow kitchen with a table inside lit by "
                     "morning sun.")

if __name__ == "__main__":
    names = sys.argv[1:] or list(SETS)
    py = r"D:\Projects_26\Comfyu\ComfyUI\venv\Scripts\comfy.exe"
    for n in names:
        open(f"prompts/sets/{n}.txt", "w", encoding="utf-8").write(SETS[n] + " " + LOOK)
        w = build_plate.build(SETS[n] + " " + LOOK, f"nmp_set_{n}", "16:9 (Widescreen)", 1.0, 5000 + list(SETS).index(n),
                              2, False, 8, "dramatic_dark_lighting.safetensors", 0.8, False, "")
        r = subprocess.run([py, "run", "--workflow", w], capture_output=True, text=True)
        print(n, "ok" if r.returncode == 0 else r.stdout[-300:])
