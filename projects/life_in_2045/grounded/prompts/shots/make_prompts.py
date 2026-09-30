"""ref2v prompts for every Grounded shot, built from shared subject blocks so each character,
set and plane cast is described with identical wording in every shot. Nobody sings: the
instrumental is pinned on every render, so no <d> dialogue appears anywhere.
Run: python prompts/shots/make_prompts.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SHEET = ("<Picture {n}> is a character sheet showing <Subject {n}> full-length from several angles above close-ups "
         "of his face, the same single person throughout.")
FACE_NOW = ("a white man of about sixty with a broad square face, heavy brows, grey-blue eyes, a slightly crooked "
            "nose, shaggy salt-and-pepper hair grown out over his ears and a short grey beard")
STEVE_HOME = ("<Subject {n}> is Steve in <Picture {n}>: " + FACE_NOW + ", in a faded navy henley t-shirt, baggy "
              "washed-out navy shorts and worn brown slippers. " + SHEET)
STEVE_OUT = ("<Subject {n}> is Steve in <Picture {n}>: " + FACE_NOW + ", in a worn brown leather flight jacket with a "
             "sheepskin collar over a navy henley, faded jeans and scuffed brown boots. " + SHEET)
CAPTAIN = ("<Subject {n}> is Steve years earlier in <Picture {n}>: an airline captain of about fifty-five with a broad "
           "square face, heavy brows, grey-blue eyes, short neat dark salt-and-pepper hair and a clean shave, in a navy "
           "captain's uniform jacket with four gold sleeve stripes and gold wings, a white shirt, a black tie and a "
           "black peaked cap with a gold badge. " + SHEET)
ALEC = ("<Subject {n}> is Alec, Steve's teenage grandson, in <Picture {n}>: a thin boy of seventeen with a long angular "
        "face, grey-blue eyes, heavy brows and messy dark brown hair falling over his forehead, in a faded black hoodie "
        "under a worn olive field jacket, black cargo trousers and grey high-top sneakers. " + SHEET)
PILOT = ("<Subject {n}> is the first officer in <Picture {n}>: a man of about forty with a lean tanned face, styled "
         "dark blond hair and a trim moustache, in a white short-sleeved airline pilot's shirt with three-stripe "
         "epaulettes and a loosened navy tie, holding a smartphone. " + SHEET)
CAST_PEOPLE = ("a tall Black flight attendant of about thirty-five with a neat low bun, an elderly white man with a "
               "shock of white hair and round tortoiseshell glasses, a young East Asian woman with a sleek black bob, "
               "a heavyset bald man with a ginger beard, and a freckled girl of about nine with two red braids "
               "holding a stuffed rabbit")
CAST_CLOTHES = {
    "a": "the attendant in a classic navy airline uniform with a red silk neck scarf",
    "b": "the attendant in a pale grey high-collared tunic uniform with a teal sash and a small glowing badge",
    "c": "the attendant in an elegant cream wrap uniform with a soft gold collar",
}
def CAST(era):
    return (f"<Subject {{n}}> is the cabin crew and passengers in <Picture {{n}}>: {CAST_PEOPLE}; "
            f"{CAST_CLOTHES[era]}. <Picture {{n}}> is a lineup of these five people, the same individuals throughout.")

R_PERSON = ("<Subject {n}> (appears in [Shot 1]): fully_preserved - his face, hair, beard and clothes are retained "
            "exactly as in <Picture {n}>.")
R_CAST = ("<Subject {n}> (appears in [Shot 1]): fully_preserved - each person's face, hair, skin and clothes are "
          "retained exactly as in <Picture {n}>.")

def SET(desc):
    return f"<Subject {{n}}> is {desc} in <Picture {{n}}>."
R_SET = ("<Subject {n}> (appears in [Shot 1]): attribute_transfer - the layout, surfaces, colours and light of the "
         "location are carried into the target video.")

AIRPORT = SET("a vast, spotless airport of the year 2045 at dawn, a curved glass terminal and white airliners")
BEDROOM = SET("Steve's modest bedroom: an unmade bed with a faded patchwork quilt, a wooden dresser with a mirror, "
              "a framed aerial photograph of clouds, half-open blinds")
BEDROOM_N = SET("Steve's modest bedroom at night: an unmade bed with a faded patchwork quilt, a wooden dresser with a "
                "mirror, one warm bedside lamp on, dark blue blinds")
DRESSER = SET("the top of Steve's wooden dresser: gold pilot's wings, a silver captain's badge, a black captain's cap, a "
              "framed photograph of a pilot in front of a jet, a leather logbook")
COCKPIT_DAY = SET("an airliner cockpit in flight around 2015, glass displays and side-sticks, sunlit cloud tops ahead")
COCKPIT_STORM = SET("an airliner cockpit at night in a storm around 2015, rain on the windscreen, runway lights ahead")
COCKPIT_2045 = SET("the cockpit of a pilotless airliner of 2045: two empty pale seats and one seamless glowing display")
BRIEFING = SET("an airline crew briefing room of 2045: a pale oval table, white chairs, a wall screen, glass wall onto "
               "the apron")
GATE = SET("a departure gate of 2045: a tall glass wall onto a white airliner at the jet bridge, pale seats, a slim "
           "ceiling speaker grille")
BATHROOM = SET("Steve's small, tired bathroom: a white sink, a mirror over it, a frosted window")
HALLWAY = SET("Steve's narrow front hallway: a wooden front door, a coat hook, a small table with keys, framed photos of "
              "airliners")
TOWER = SET("an empty airport control tower cab of 2045: slanted glass windows, pale consoles, unused headsets on hooks")
APRON = SET("a white airliner on a clean apron at dawn, green laser scan lines, a white weather radar dome")
FENCE = SET("a long chain-link perimeter fence beside a grassy verge and footpath at the edge of a vast airport")
CONCOURSE = SET("a huge airport concourse of 2045 at dusk: a curved glass roof, a polished floor, travellers with "
                "rolling luggage")
DEPARTURE = SET("a vast departure hall of 2045 at dusk with an enormous glowing wall of flight information")
STORM_PLANE = SET("a white airliner flying through a towering night thunderstorm lit by lightning")
CAFE = SET("a small airport café of 2045: pale wooden tables by a tall window onto the runway, warm pendant lights")
CABIN = {"a": SET("the cabin of a present-day single-aisle airliner: grey seats, closed overhead bins, an open cockpit "
                  "door at the far end of the aisle"),
         "b": SET("the cabin of a late-2030s airliner: white shell seats with teal upholstery, white bins with a cyan "
                  "light line, an open cockpit door at the far end of the aisle"),
         "c": SET("the cabin of a 2040s airliner: sculpted cream seats, warm light lines, and at the far end, where the "
                  "cockpit used to be, a lounge behind one enormous curved nose window")}

BADGE = ("<Subject {n}> is Steve's airline crew ID badge in <Picture {n}>: a white plastic photo identity card with a "
         'navy stripe, small gold wings, the word "CAPTAIN" and a black clip, the size of a credit card.')
R_BADGE = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - the white ID card, its navy stripe, gold wings, the word '
           '"CAPTAIN" and the black clip are retained exactly as in <Picture {n}>.')
HOUSE = SET("Steve's modest single-storey suburban house at dawn, a porch light on, a jet crossing the sky above")
STORM_PLANE2 = SET("a white airliner flying level through a night thunderstorm in heavy rain, seen from behind its wing")
COCKPIT_STORM2045 = SET("the empty cockpit of a pilotless airliner of 2045 at night in a storm, rain on the windscreen")
WINDOW_NIGHT = SET("a tall rain-streaked terminal window at night, the lit runway and parked airliners beyond, lightning")
TAKEOFF_NIGHT = SET("an airport runway at night in 2045, rows of runway lights, the glowing glass terminal behind")

LOOK = ("Live-action, a quiet, naturalistic drama set in the near future of 2045, soft warm natural light, clean pale "
        "surfaces, 35mm film grain, nobody speaks.")
LOOK_PAST = ("Live-action, a memory from years earlier, warm and golden, saturated colour, 35mm film grain, nobody "
             "speaks.")
MUSIC = "A slow, aching rock instrumental with a steady drum beat."


def build(name, subs, summary, shot, sound, look=LOOK):
    defs = "\n".join(s.format(n=i + 1) for i, (s, _) in enumerate(subs))
    ret = "\n".join(r.format(n=i + 1) for i, (_, r) in enumerate(subs))
    txt = (f"subject_definitions\n{defs}\n\nsummary\n[reference generation] {summary}\n\n"
           f"retention_analysis\n{ret}\n\ndetailed_description\n{look}\n\n[Shot 1] {shot}\n\n"
           f"overall_soundscape\n{sound}\n\nnon_diegetic_music\n{MUSIC}\n")
    open(os.path.join(HERE, f"{name}.txt"), "w", encoding="utf-8").write(txt)


def plane(era, ending):
    # Cabin plate only: the lineup sheets made H3 open on the grey lineup for 2.5 s (v1 of Plane A).
    # The people come from the pinned start frame and are described in prose.
    subs = [(CABIN[era], R_SET)]
    build(f"s{ {'a': '11', 'b': '20', 'c': '27'}[era]}_plane{era.upper()}", subs,
          "The target video shows an ordinary moment mid-flight in <Subject 1>: a flight attendant hands a passenger a "
          "bag of peanuts, then the camera glides forward up the aisle to the front of the plane.",
          f"Mid-flight in <Subject 1>, bright daylight through the windows. The camera looks forward toward the cockpit, and "
          f"every passenger in every row sits facing the front of the plane, so the camera sees the backs of their heads "
          f"above the seat backs all the way up the aisle. A tall Black "
          f"flight attendant with a neat low bun, {CAST_CLOTHES[era][len('the attendant '):]}, stands in the aisle a few "
          f"rows ahead of the camera and leans down to hand a small bag of peanuts to an elderly white man with white hair "
          f"and round tortoiseshell glasses in the left aisle seat; he takes it and smiles up at her, and she smiles back "
          f"and straightens. A young East Asian woman with a black bob, a bald man with a ginger beard and a freckled girl "
          f"with red braids sit further up the aisle, and the open cockpit door is visible at the far end of the one "
          f"continuous cabin. At 00:03.000 the camera rises slightly and glides slowly forward up the aisle past the "
          f"attendant, the backs of the seats and the backs of the passengers' heads sliding by on both sides as it "
          f"overtakes each row from behind, Push with medium amplitude at slow speed, the same cockpit door growing "
          f"steadily larger straight ahead the whole way. At 00:12.500 the camera reaches the door "
          f"and moves through it: {ending} The camera holds there to the end.",
          "The steady roar of the engines, the hiss of the air vents, a soft cabin chime.")


def main():
    H, O, C, A = (STEVE_HOME, R_PERSON), (STEVE_OUT, R_PERSON), (CAPTAIN, R_PERSON), (ALEC, R_PERSON)
    S = lambda block: (block, R_SET)

    build("s01_airport", [S(AIRPORT)],
          "The target video shows a vast, silent airport of 2045 at dawn as a pilotless airliner takes off.",
          "A wide view across <Subject 1> at dawn, pale pink and gold sky, mist over the grass. A single white airliner "
          "rolls along the distant runway, gathers speed and lifts smoothly into the sky, its lights blinking. Nothing "
          "else moves; no people anywhere on the apron. The camera pushes in with small amplitude at slow speed toward "
          "the glowing glass terminal.",
          "Distant jet engines rising to a roar and fading, birdsong, a faint wind.")
    build("s02_bed", [H, S(BEDROOM)],
          "The target video shows Steve lying awake on his bed in the early morning, staring at the ceiling.",
          "In <Subject 2> in pale early morning light, <Subject 1> lies on his back on top of the unmade bed, fully "
          "awake, one arm behind his head, staring at the ceiling. He blinks slowly, breathes out, and turns his head "
          "a little toward the window as a faint jet passes far overhead, then looks back at the ceiling. The light "
          "through the blinds brightens very slightly. The camera pushes in with small amplitude at slow speed.",
          "Morning quiet, a far-off jet, a clock ticking, birds outside.")
    build("s03_badge", [H, (BADGE, R_BADGE), S(BEDROOM)],
          "The target video shows Steve holding his old airline crew ID badge in his palm.",
          "A close-up in <Subject 3>: <Subject 1> sits on the edge of the bed in the morning light, <Subject 2> lying flat "
          "in his open palm in the foreground, sharp. He tilts the card slowly with his thumb so it catches the light, "
          "and looks at it for a long moment, his face soft and heavy behind it. The camera is Static with a slow rack "
          "of focus from the badge to his face.",
          "Morning quiet, birds outside.")
    build("s01b_house", [S(HOUSE)],
          "The target video shows Steve's quiet suburban house at dawn as an airliner crosses the sky above it.",
          "<Subject 1> at dawn, pale pink and gold sky, the porch light still on and one window glowing. High above the "
          "roof a white airliner crosses the sky steadily from left to right, trailing a thin contrail. A light breeze "
          "stirs the lawn. The camera pushes in with small amplitude at slow speed toward the lit window.",
          "Dawn quiet, birds, the far-off rumble of a jet.")
    build("s04_dresser", [S(DRESSER)],
          "The target video shows the top of Steve's dresser: his pilot's wings, cap, badge and an old photograph.",
          "A close view along the top of <Subject 1> in soft morning window light: the gold pilot's wings, the silver "
          "captain's badge, the black captain's cap with its gold badge, the framed photograph of a pilot in front of a "
          "jet, the leather logbook, dust drifting in the sunbeam. The camera trucks right with small amplitude at slow "
          "speed along the dresser top.",
          "Morning quiet, a clock ticking, birds outside.")
    build("s05_cockpit", [C, S(COCKPIT_DAY)],
          "The target video shows Captain Steve, years earlier, flying an airliner above sunlit clouds, content.",
          "In <Subject 2>, high above brilliant sunlit cloud tops, <Subject 1> sits in the left pilot seat in his "
          "captain's uniform and cap, one hand resting easily on the side-stick. He glances at the instruments, then "
          "turns toward the right seat with a broad, easy smile and a small nod, completely at home. Warm sunlight "
          "moves across the controls. The camera pushes in with small amplitude at slow speed.",
          "The deep hum of the cockpit, the rush of air past the windscreen, a soft chime.", look=LOOK_PAST)
    build("s06_bededge", [H, S(BEDROOM)],
          "The target video shows Steve sitting slumped on the edge of his bed, the badge in his hand.",
          "In <Subject 2> in morning light, <Subject 1> sits on the edge of the unmade bed facing the camera, forearms "
          "on his knees, the small silver badge loose in one hand. He stares at the floor, lets out a long breath, "
          "rubs his face with his free hand and stays there, shoulders down. The camera is Static.",
          "Morning quiet, a clock ticking, a far-off jet.")
    build("s07_briefing", [(CAST("c"), R_CAST), S(BRIEFING)],
          "The target video shows a cabin crew being briefed by a wall screen in 2045; the captain's line on the "
          "roster is blank.",
          "In <Subject 2> in morning light, the tall Black flight attendant from <Subject 1> in her cream uniform and "
          "three other flight attendants in identical cream uniforms walk in and sit around the pale oval table, "
          "facing the wall screen, which shows a flight plan and a crew roster where the captain's line is empty. They "
          "nod along, relaxed and routine. An airliner waits at the gate through the glass wall. The camera trucks "
          "left with small amplitude at slow speed.",
          "A quiet room, the soft tone of the screen, muffled jet engines outside.")
    build("s08_emptyseat", [S(COCKPIT_2045)],
          "The target video shows the empty cockpit of a pilotless airliner of 2045, flying itself.",
          "In <Subject 1>, high above bright clouds, the two pale pilot seats are empty. The seamless display glows "
          "and scrolls softly, small controls move by themselves, the view tilts gently as the plane banks. The camera "
          "pushes in with medium amplitude at slow speed toward the empty left seat.",
          "The deep hum of the cockpit, a soft automated tone, air rushing past.")
    build("s09_gate", [O, S(GATE)],
          "The target video shows Steve at a departure gate, looking up at a ceiling speaker as a synthetic voice "
          "welcomes passengers aboard.",
          "In <Subject 2> in morning light, <Subject 1> stands at the tall window beside the white airliner at the jet "
          "bridge. He turns his head and looks up at the slim ceiling speaker grille, frowning, as if he recognises the "
          "voice coming from it, then his face falls and he looks back out at the plane. Travellers sit in the "
          "background looking at screens. The camera pushes in with small amplitude at slow speed.",
          "A calm, warm synthetic announcement voice through the ceiling speaker, the murmur of a gate, jet engines "
          "outside.")
    build("s10_mirror", [H, C, S(BATHROOM)],
          "The target video shows Steve looking into his bathroom mirror; his reflection is himself years earlier in "
          "full captain's uniform.",
          "In <Subject 3> in pale morning light, <Subject 1> stands at the sink seen from behind his shoulder, looking "
          "into the mirror. The reflection in the mirror is <Subject 2>, the captain in his navy uniform and peaked cap, "
          "standing tall and perfectly still, looking straight back at him. <Subject 1> slowly lifts a hand to his own "
          "beard, then lowers it and leans on the sink, shoulders dropping, while the reflection does not move at all, "
          "calm and upright. The camera pushes in over his shoulder toward the mirror with small amplitude at slow "
          "speed.",
          "A dripping tap, the hum of a fan, morning quiet.")
    plane("a", "through the open cockpit door, where a first officer in a white short-sleeved shirt with a trim moustache lounges in the left seat with one "
               "foot up on the panel, scrolling his phone with a bored smirk while the controls move by themselves and "
               "clouds stream past the windscreen.")
    build("s12_hall", [O, S(HALLWAY)],
          "The target video shows Steve pulling on his old flight jacket in the hallway and heading out.",
          "In <Subject 2>, <Subject 1> stands in the middle of the hallway facing the camera and shrugs the brown "
          "leather flight jacket onto his shoulders, settles the collar, picks the leather logbook up from the table, "
          "turns and walks to the front door and opens it onto bright daylight. The camera is Static.",
          "Footsteps on a wooden floor, the creak of leather, a door opening onto birdsong.")
    build("s13_tower", [S(TOWER)],
          "The target video shows an empty airport control tower of 2045 running itself.",
          "Inside <Subject 1> in morning light, not a single person: the pale consoles scroll with handoff sequences and "
          "flight tags, empty chairs sit pushed in, a row of old headsets hangs unused on hooks, and through the slanted "
          "windows an airliner lands on the runway far below. The camera arcs slowly around the room with medium "
          "amplitude at slow speed.",
          "Soft automated radio chatter, synthetic handoff tones, the hum of equipment.")
    build("s14_apron", [S(APRON)],
          "The target video shows a parked airliner being scanned by lasers at dawn.",
          "On <Subject 1> at dawn, thin green laser scan lines sweep slowly along the white fuselage from the small "
          "autonomous inspection vehicle, and the smooth white radar dome sits motionless on top of its mast in the background. No "
          "people. The camera trucks left with small amplitude at slow speed.",
          "A soft electronic whir, distant engines, wind.")
    build("s15_fencewalk", [O, S(FENCE)],
          "The target video shows Steve walking along the airport perimeter fence as a plane climbs overhead.",
          "On the footpath beside <Subject 2> in bright late-morning light, <Subject 1> walks slowly toward the camera, "
          "hands in his jacket pockets, and tips his head back to watch an airliner climb low overhead, following it "
          "with his eyes. The camera tracks backward in front of him with small amplitude at slow speed.",
          "A jet roaring low overhead and fading, wind in the grass, footsteps.")
    build("s16_storm", [C, S(COCKPIT_STORM)],
          "The target video shows Captain Steve, years earlier, fighting a crosswind landing at night in a storm.",
          "In <Subject 2> at night in a violent thunderstorm: heavy rain streams and splatters across the windscreen the "
          "whole time, the wipers sweep, and bright white lightning flashes every few seconds, lighting the clouds and "
          "the whole cockpit. Ahead through the rain the runway approach lights swing left and right as the plane is "
          "thrown by the crosswind. <Subject 1> in his captain's uniform, without his cap, seen from behind and to the "
          "right, grips the side-stick and works the throttles, jaw set, eyes locked on the runway, correcting hard as "
          "the cockpit rocks and yaws in the gusts. A lightning flash lights his face. The camera Shakes with medium "
          "amplitude.",
          "Rain hammering the windscreen, thunder, the roar of engines, warning chimes.", look=LOOK_PAST)
    build("s17_fence", [O, S(FENCE)],
          "The target video shows Steve at the airport fence, fingers in the wire, watching a plane take off.",
          "At <Subject 2> in bright light, <Subject 1> stands close to the fence with the fingers of one hand hooked "
          "through the wire, seen from behind and to the left, his face in profile. Beyond the fence a white airliner "
          "lifts off the runway and climbs away; he watches it all the way up. The camera pushes in with small amplitude "
          "at slow speed.",
          "A jet taking off, a rising roar, wind in the grass, the wire rattling.")
    build("s18_face", [O, S(FENCE)],
          "The target video shows a close-up of Steve's face at the airport fence as a jet's roar washes over him.",
          "A close-up of <Subject 1> behind the wire of <Subject 2>, looking up past the camera at the sky. The noise of "
          "a jet washes over him; his eyes are wet, his jaw tight, and he swallows and keeps looking up. The camera is "
          "Static.",
          "A jet roaring close overhead, wind.")
    build("s19_wide", [O, S(FENCE)],
          "The target video shows a very wide view of Steve alone at the fence of a vast airport.",
          "A very wide view of <Subject 2>: the long fence line crossing a vast airport, the runway and the distant "
          "glass terminal, and <Subject 1> a small solitary figure standing still at the fence in the middle distance "
          "as an airliner climbs away into the sky. The camera pulls back with small amplitude at slow speed.",
          "Distant jet engines, wind.")
    plane("b", "through the open cockpit door into the cockpit, where both pilot seats are empty and the controls move "
               "by themselves, bright clouds streaming past the windscreen.")
    build("s21_concourse", [O, S(CONCOURSE)],
          "The target video shows Steve walking against the flow of travellers through a vast concourse at dusk.",
          "In <Subject 2> in warm amber dusk light, <Subject 1> walks toward the camera through the centre of the "
          "concourse against a steady stream of travellers who all walk the other way, heads down over glowing screens, "
          "pulling rolling luggage. He looks up and around at the glass roof as they part around him without looking "
          "up. The camera tracks backward in front of him with small amplitude at slow speed.",
          "Rolling luggage wheels, footsteps, soft synthetic announcements, a hushed crowd.")
    build("s22_departure", [O, S(DEPARTURE)],
          "The target video shows travellers facing a giant glowing flight board like a congregation, and Steve at the "
          "back turned away.",
          "In <Subject 2> at dusk, rows of travellers stand still facing the enormous glowing flight board high above "
          "them, faces lit, like a congregation. The camera starts wide on the crowd and the board and slowly pulls "
          "back and pans right, Pull with medium amplitude at slow speed, until at 00:09.000 <Subject 1> in his brown "
          "leather flight jacket comes into the right foreground at the back of the crowd, the only one turned away from "
          "the board, looking out through the glass at the darkening sky. The camera holds on him to the end.",
          "A hushed hall, a soft synthetic chime, distant engines.")
    build("s23a_flyby", [S(STORM_PLANE2)],
          "The target video shows the camera flying past a pilotless airliner in a night thunderstorm in heavy rain.",
          "<Subject 1>: the white airliner holds a steady, level course through the storm while the camera flies "
          "alongside and slowly overtakes it from behind the wing toward the nose, Truck left with medium amplitude at "
          "medium speed. Heavy rain streaks diagonally past the camera the whole time, water sheets off the wing, and "
          "lightning flashes in different places among the clouds every few seconds, each flash lighting the wet "
          "fuselage and then fading.",
          "Rain roaring, thunder, the drone of engines.")
    build("s23b_cockpit", [S(COCKPIT_STORM2045)],
          "The target video shows the empty cockpit of a pilotless airliner in a storm as its screens flicker.",
          "In <Subject 1> at night, rain streams down the outside of the windscreen and lightning flashes in the clouds "
          "ahead. The two pilot seats are empty. A close lightning flash whites out the view, and the glowing display "
          "flickers and goes dark for a moment, leaving the empty seats lit only by the storm, then blinks back on. "
          "The camera is Static.",
          "Thunder, rain drumming on the glass, an electronic tone cutting out and returning.")
    build("s23c_window", [O, S(WINDOW_NIGHT)],
          "The target video shows Steve at a rain-streaked terminal window at night, watching the storm.",
          "At <Subject 2> at night, <Subject 1> stands close to the rain-streaked glass in the right foreground in "
          "three-quarter view, looking out at the storm over the lit runway. Rain runs down the window, lightning "
          "flashes in the distant clouds and lights his face each time; he does not move, only watches. The camera "
          "pushes in with small amplitude at slow speed.",
          "Rain on the glass, distant thunder, a hushed terminal.")
    build("s24_cafe", [O, S(CAFE)],
          "The target video shows Steve alone at a café table in the terminal with his old logbook, watching planes.",
          "In <Subject 2> in the warm evening light, <Subject 1> sits alone at the window table with an old leather "
          "logbook open in front of him and a cup of coffee, turning a page slowly, then looking out of the window at an "
          "airliner taking off. Behind him, kids with rolling luggage pass by, their faces lit by glowing screens. The "
          "camera pushes in with small amplitude at slow speed.",
          "Café murmur, a coffee machine, rolling luggage, a plane taking off outside.")
    build("s25_alec", [O, A, S(CAFE)],
          "The target video shows Steve with his eyes closed, listening to a plane take off, when his grandson Alec "
          "sits down across from him.",
          "At the window table in <Subject 3> in the evening, the window showing the lit runway under an open dusk "
          "sky, <Subject 1> sits with the open logbook, eyes closed, head tilted toward the window, listening to "
          "the sound of engines outside. At 00:05.000 <Subject 2> walks in from "
          "the left and drops into the empty chair across the table. <Subject 1> opens his eyes, sees his grandson, and "
          "a slow, surprised smile spreads across his face; <Subject 2> gives a small half-smile back. The camera is "
          "Static.",
          "Café murmur, a plane climbing outside, a chair scraping.")
    build("s26_two", [O, A, S(CAFE)],
          "The target video shows Steve telling his grandson Alec about the planes outside, while Alec looks at his "
          "phone.",
          "At the window table in <Subject 3> at dusk, the last light fading above the rows of runway lights, "
          "<Subject 1> on the left turns and points out through the glass toward the runway, his face lit up as he "
          "talks with his hands. Across the table <Subject 2> glances out of the window for a moment, then back down to "
          "the glowing phone in his hand. <Subject 1> keeps looking out, his hand slowly lowering. The camera pushes in "
          "with small amplitude at slow speed.",
          "Café murmur, engines outside, the clink of a cup.")
    build("s26b_takeoff", [S(TAKEOFF_NIGHT)],
          "The target video shows an airliner taking off at night.",
          "On <Subject 1> at night, a white airliner races along the runway from left to right, its landing lights "
          "blazing, the runway lights streaking past beneath it, then its nose lifts and it climbs away steeply into "
          "the dark sky, its lights growing smaller. The camera pans right with medium amplitude at medium speed to "
          "follow it.",
          "A roaring takeoff, the engines rising to a scream and fading into the night.")
    plane("c", "the aisle opens into the bright lounge in the nose of the plane, where there is no cockpit at all, only "
               "one enormous curved window filled with passing clouds, and the young woman, the bald man and the girl "
               "from the cabin stand at the glass looking out, the girl pressing her hand to the window.")
    build("s28_night", [H, (BADGE, R_BADGE), S(BEDROOM_N)],
          "The target video shows Steve at night laying his airline crew ID badge down on the dresser and switching "
          "off the lamp.",
          "In <Subject 3> at night by the warm lamp, <Subject 1> stands at the dresser and lays <Subject 2> face up on "
          "the dresser top beside the gold pilot's wings, very gently, and rests his fingers on it for a moment. Then he "
          "turns, reaches over and switches off the bedside lamp; the room falls into soft blue darkness lit only by "
          "the window. The camera is Static.",
          "Night quiet, the click of a lamp switch, a far-off jet.")
    print("wrote", len([f for f in os.listdir(HERE) if f.endswith(".txt")]), "prompts")


if __name__ == "__main__":
    main()
