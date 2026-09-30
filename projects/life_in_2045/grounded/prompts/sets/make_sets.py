"""Location plates for Grounded (Krea 2 t2i via tools/build_plate.py). Writes one prompt file
per set and builds its workflow; queue with ../../comfyq.py run plate_<name>.json.
Run from the project folder: python prompts/sets/make_sets.py [names...]"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = r"D:\Projects_26\Comfyu\ComfyUI\venv\Scripts\python.exe"
BUILD = os.path.join(HERE, "..", "..", "..", "..", "..", "tools", "build_plate.py")

NOW = ("Photorealistic cinematic film still, the near future of 2045: clean, pale, quiet, glass and white "
       "surfaces, warm natural light, 35mm film, fine grain, natural muted colour.")
PAST = ("Photorealistic cinematic film still, 35mm film, fine grain, warm saturated colour.")
HOME = ("Photorealistic cinematic film still, 35mm film, fine grain, natural muted colour.")

SETS = {
    "airport_dawn": (
        "A wide view across a vast, spotless airport at dawn in the year 2045: a long, low terminal of curved glass "
        "and pale concrete glowing warm inside, sleek white airliners parked at the gates, a single airliner rolling "
        "along the runway in the middle distance, pale pink and gold sky, a thin mist over the grass between the "
        "runways. Nobody on the apron. Silent, clean, orderly. " + NOW),
    "bedroom_morning": (
        "The bedroom of a sixty-year-old man living alone in a modest suburban house: an unmade double bed with a "
        "faded quilt, a plain wooden nightstand with a lamp, a wooden dresser against the wall with a mirror above "
        "it, pale morning light through half-open blinds, clothes over a chair, a framed aerial photograph of clouds "
        "on the wall. Lived-in, slightly neglected, quiet. Wide shot from the doorway, nobody in the room. " + HOME),
    "dresser_top": (
        "Close-up of the top of a wooden dresser in soft morning window light: a pair of gold airline pilot's wings, "
        "a silver captain's name badge, a folded black airline captain's peaked cap with a gold badge, a framed "
        "photograph of an airline pilot in uniform standing in front of a jet, a leather-bound pilot's logbook, a "
        "few coins and a watch. Dust in the light. Shallow depth of field. " + HOME),
    "cockpit_day": (
        "Inside the cockpit of a modern airliner in flight around 2015, seen from behind and between the two pilot "
        "seats: the glass cockpit displays, the throttle quadrant, the overhead panel, the two side-stick seats, and "
        "through the wide windscreen a brilliant sunlit sea of cloud tops and deep blue sky. Warm sunlight across "
        "the controls. Nobody in the seats. " + PAST),
    "cockpit_storm": (
        "Inside the cockpit of a modern airliner at night in a violent storm around 2015, seen from behind and "
        "between the two pilot seats: rain streaming across the windscreen, runway approach lights swinging "
        "through the rain ahead, a flash of lightning lighting the clouds, the displays glowing amber and green, "
        "the controls lit by panel light. Nobody in the seats. Brightly lit by the panels and the lightning. " + PAST),
    "cockpit_2045": (
        "Inside the cockpit of a pilotless airliner in the year 2045, seen from behind the two seats: two empty "
        "pale grey pilot seats, a single seamless curved glass display glowing softly across the whole panel, no "
        "yokes, small controls moving by themselves, bright clouds and blue sky through the wide windscreen. "
        "Pristine, white, eerie. " + NOW),
    "briefing_room": (
        "A small airline crew briefing room in the year 2045: a pale oval table, white chairs, a large wall screen "
        "showing a flight plan map and a crew roster, glass wall looking out onto parked airliners at the gate, "
        "morning light. Nobody in the room. " + NOW),
    "gate_window": (
        "An airport departure gate in the year 2045 seen from inside: a tall wall of glass looking out at a white "
        "airliner parked at the jet bridge, rows of pale seats, a slim ceiling speaker grille above the window, soft "
        "morning light, a few travellers seated in the distance looking at glowing screens. " + NOW),
    "bathroom_mirror": (
        "A small, tired bathroom in a suburban house: a white sink with a chipped enamel edge, a large mirror above "
        "it with a medicine cabinet, a towel over the rail, a razor and a toothbrush in a glass, pale morning light "
        "from a small frosted window. Nobody in the room. Viewed from the doorway at a slight angle so the mirror "
        "is on the right. " + HOME),
    "hallway": (
        "The narrow front hallway of a modest suburban house in the morning: a wooden front door with a small "
        "window, a coat hook with an old brown leather flight jacket hanging on it, a small table with keys and a "
        "leather logbook, a worn runner rug, framed photographs of airliners on the wall. Nobody in it. " + HOME),
    "tower": (
        "Inside an airport control tower cab in the year 2045, completely empty of people: a ring of tall slanted "
        "glass windows looking out over the runways, pale consoles with softly scrolling displays, empty chairs "
        "pushed in, a row of old headsets hanging unused on hooks, morning light. " + NOW),
    "apron_scan": (
        "A white airliner parked on a clean airport apron at dawn in the year 2045, thin green laser scan lines "
        "sweeping across its fuselage from a small autonomous inspection vehicle, a white dome-shaped weather radar "
        "on a mast in the background, no people, pale gold light. " + NOW),
    "fence": (
        "A long chain-link perimeter fence at the edge of a vast airport in the year 2045, a grassy verge and a "
        "cracked footpath beside it, the runway beyond with a white airliner lifting off into a bright late-morning "
        "sky, the long glass terminal far away. Nobody on the path. " + NOW),
    "concourse_dusk": (
        "A huge airport concourse in the year 2045 at dusk: a curved glass roof, polished pale floor, warm amber "
        "evening light slanting in, a steady stream of travellers with rolling luggage all looking down at glowing "
        "screens, no staff anywhere. " + NOW),
    "departure_hall": (
        "A vast airport departure hall in the year 2045 at dusk: an enormous glowing wall of flight information "
        "high above the floor like an altar, travellers standing still in rows facing it and looking up, warm amber "
        "light through the glass walls, polished floor. " + NOW),
    "storm_plane": (
        "A white airliner flying through a towering thunderstorm at night in the year 2045, seen from the side at "
        "a little distance, its lights blinking, huge anvil clouds lit from inside by lightning, a bolt of "
        "lightning striking near the wing, rain. Dramatic and brightly lit by the lightning. " + NOW),
    "cafe_evening": (
        "A small café inside an airport terminal in the year 2045 in the evening: pale wooden tables by a tall "
        "window looking out on the lit runway and a white airliner taking off, warm pendant lights, a coffee "
        "machine, travellers passing behind with rolling luggage. One empty window table for two in the "
        "foreground. " + NOW),
    "house_dawn": (
        "A modest single-storey suburban house at dawn, seen from across a quiet street: a small front lawn, a "
        "mailbox, a porch light still on, one window glowing warm, pale pink and gold sky above, and a white airliner "
        "high in the sky above the roof climbing away, with a thin contrail. Nobody outside. " + HOME),
    "storm_plane2": (
        "A white airliner flying level through a night thunderstorm, seen from slightly behind and above its left wing "
        "at close range, heavy rain streaking diagonally across the frame, the fuselage wet and glistening, its "
        "navigation lights glowing, towering dark clouds glowing faintly from inside all around it. " + NOW),
    "takeoff_night": (
        "A white airliner lifting off a runway at night in the year 2045, seen from the side at a distance: its landing "
        "lights blazing, rows of blue and white runway lights streaking past below, the glowing glass terminal far "
        "behind, dark blue sky. " + NOW),
    "window_night": (
        "A tall glass window in an airport terminal at night in a storm, rain streaming down the glass, the lit runway "
        "and parked airliners blurred beyond it, lightning in the distant clouds, the dim terminal interior in the "
        "foreground. Nobody in it. " + NOW),
}


def main(names):
    for n in names:
        path = os.path.join(HERE, f"{n}.txt")
        open(path, "w", encoding="utf-8").write(SETS[n])
        subprocess.run([PY, BUILD, "--prompt", path, "--name", f"set_{n}", "--batch", "2", "--steps", "8"],
                       check=True, capture_output=True)
        print("built", n)


if __name__ == "__main__":
    main(sys.argv[1:] or list(SETS))
