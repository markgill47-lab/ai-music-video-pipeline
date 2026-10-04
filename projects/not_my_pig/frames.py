"""First (and a few last) frames for every shot, built in Flux 2 Klein and staged for H3.

  python frames.py build [ids...]            # queue Flux jobs for these frames (default: all missing), wait, collect
  python frames.py build --seed 7 i04 v1a    # re-roll with a seed offset
  python frames.py collect                   # copy finished frames to frames/ and ComfyUI/input
  python frames.py sheet NAME id id ...      # contact sheet frames/contact_NAME.jpg

Kinds:  plate  use a reference plate as it is
        edit   single-image Flux edit of `src` (keeps the camera)
        multi  Flux multi-reference: image 1 the set (or a master frame), images 2-4 the characters
`src`/`refs` are ComfyUI input names without the nmp_ prefix; a `src` starting with f_ is another
frame from this file. The user's rule for this video: once a master frame of her in a place is
good, every other angle there is made FROM that master (src f_<master>), not from the empty plate.
Run `build` repeatedly: frames whose master is not built yet are skipped until the next pass.
"""
import glob, json, os, subprocess, sys, time, urllib.request
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import build_flux_multiref, build_flux_batch

COMFY = r"D:\Projects_26\Comfyu\ComfyUI"
COMFY_EXE = COMFY + r"\venv\Scripts\comfy.exe"
INP, OUT = COMFY + r"\input", COMFY + r"\output\plates"
SEED0 = 41000

LOOK = ("Glossy late-1990s R&B music video look: vivid saturated colour, crisp bright light, wide-angle lens, 35mm film, "
        "fine grain. Photorealistic. She is the only person wearing purple.")
HER = "the woman from image 2, with deep brown skin, big voluminous brunette curls, purple eyeshadow, plum lipstick and gold hoop earrings"
TRENCH = f"{HER}, in her long belted violet trench coat over a lavender turtleneck, purple trousers and glossy purple ankle boots, purple sunglasses pushed up into her curls"
SUIT = f"{HER}, in her violet double-breasted power suit, lilac silk blouse and purple cat-eye glasses"
TRACK = f"{HER}, in her purple velour tracksuit with white side stripes and white sneakers"
DRESS = f"{HER}, in her knee-length sparkling purple sequin dress and purple strappy heels"
JACKET = f"{HER}, in her cropped dark purple leather biker jacket over a sparkling purple sequin dress and purple heels"
ROBE = f"{HER}, in her long lavender silk robe over purple satin pyjamas, her curls wrapped in a purple satin headwrap"
COFFEE = "She holds a giant white paper coffee cup"
OWNER = "a skinny frantic grey-haired man with a moustache, in a green-and-orange striped terry bathrobe and one slipper"
PIG = "a small pale pink pet piglet with grey freckles, in a red harness with a red leash trailing"
CALM = "Her face is calm and amused, mouth closed."
SING = "She looks into the lens with a sly, unbothered half-smile, mouth closed."
KEEP = "Keep the exact same place, camera position and lighting as image 1."
SAME = ("The same place as image 1, with the same lighting and the same woman in the same clothes as image 1; her face and "
        "hair as in image 2.")

F = {}


def plate(sid, src):
    F[sid] = dict(kind="plate", src=src)


def edit(sid, src, text, keep=KEEP):
    F[sid] = dict(kind="edit", src=src, text=f"{keep} {text} {LOOK}".strip())


def multi(sid, set_, refs, text):
    F[sid] = dict(kind="multi", src=set_, refs=refs, text=f"{text} {LOOK}")


def again(sid, master, combo, text, extra=()):
    """Another angle in a place that already has a master frame of her."""
    multi(sid, f"f_{master}", [combo, *extra], f"{SAME} {text}")


# ---- intro: sunrise, her building (trench) ------------------------------------------------------
edit("i01", "skyline", "Nothing else changes: the same sunrise view of the apartment block and skyline.")
edit("i02", "window", "Inside the open window, framed from the waist up, a bleary man in blue striped pyjamas and wild bed-head "
     "raises a slipper high over a ringing red alarm clock on the sill, about to smash it, face scrunched in fury.")
edit("i03", "window", "Inside the open window a frazzled woman in a yellow dressing gown and pink hair curlers flaps a tea towel "
     "at a white smoke alarm on the ceiling while black smoke pours from a toaster on the counter.")
multi("i04", "hallway", ["singer_trench_combo"], f"In the hallway of image 1, the purple door 4B stands open and {TRENCH} has just "
      f"stepped out of it, seen from the waist up close to the camera, facing the lens. {COFFEE}. Her purple sunglasses are on her "
      f"nose. {SING}")
again("i05", "i04", "pig_sheet", f"The camera is at floor level on the carpet runner looking along the hallway: her glossy purple "
      f"ankle boots and the hem of the violet trench coat stand on the right, and {PIG}, as in image 2, trots past them toward the "
      "camera, filling the lower left of the frame.")
multi("i06", "f_i04", ["owner_combo", "singer_trench_combo"], "The same hallway as image 1, seen from further back so both doors "
      f"are in frame. The green door opposite has burst open and {OWNER}, the man from image 2, charges out of it mid-stride, arms "
      "flailing, mouth wide open shouting, holding an empty red leash. The woman from image 3 in her violet trench coat stands calmly "
      f"by her purple door sipping from her giant coffee cup, watching him go. {LOOK}")
multi("i07", "stoop", ["singer_trench_combo"], f"On the stoop of image 1, {TRENCH}, has just stepped out of the front door at the top "
      f"of the steps, seen full length, purple sunglasses on her nose. {COFFEE}. {CALM} On the sidewalk below, a dripping wet man "
      "wearing only a white bath towel sprints past after a green garbage truck pulling away down the street.")
again("i08", "i07", "singer_trench_combo", "A close-up of her face and shoulders on the stoop, the sunny street soft behind her. One "
      "finger is on the bridge of her purple sunglasses, about to push them up onto her curls, and she looks over them at the lens. "
      "Mouth closed, a knowing smile.")

# ---- verse 1 / pre-chorus: the morning sidewalk, the coffee shop -------------------------------------
multi("v1a", "sidewalk", ["singer_trench_combo"], f"On the sidewalk of image 1, {TRENCH}, walks straight toward the camera, seen "
      f"from the knees up in the centre of the frame, large and close, the sidewalk stretching behind her. {COFFEE}. {SING} Behind "
      "her on the pavement a man in a grey suit fights a black umbrella that the wind has blown inside out.")
edit("v1b", "f_v1a", "Change the camera: a medium shot of the man in the grey suit on the sidewalk, wrestling with the black "
     "umbrella that has blown inside out and wrapped itself over his head and shoulders, his briefcase dropped at his feet. The "
     "woman in purple is no longer in the frame.", keep="Keep the same sidewalk, morning sun and look as image 1.")
again("v1c", "v1a", "singer_trench_combo", f"She walks toward the camera seen from the waist up. {COFFEE}. {SING} Just behind her, "
      "a man in a blue business suit stands on the pavement screaming into his phone held out flat on speaker in front of his "
      "face, red in the face, veins on his neck.")
edit("v1d", "f_v1a", "Change the camera: a medium close-up of a young commuter in a crisp white shirt and tie on the sidewalk, his "
     "paper coffee cup crushed in his hand and brown coffee splashed all down the front of his white shirt, frozen with his mouth "
     "and eyes wide open in horror. The woman in purple is no longer in the frame.",
     keep="Keep the same sidewalk, morning sun and look as image 1.")
again("v1e", "v1a", "singer_trench_combo", f"A medium close-up from the chest up as she strolls toward the camera, lifting the "
      f"giant coffee cup toward her lips. {SING}")
multi("p1a", "coffee", ["singer_trench_combo"], "At the counter of the coffee shop in image 1, a red-faced middle-aged man in a "
      "tan golf jacket leans over the counter jabbing his finger at a terrified young barista in a green apron who holds up a wrong "
      "paper cup. Behind him in the queue, slightly out of focus, stands the woman from image 2 in her violet trench coat, calm.")
again("p1b", "p1a", "singer_trench_combo", "A medium shot of her in the queue facing the camera, seen from the waist up, with the "
      "red-faced man in the tan golf jacket beside her turned toward her, palms up, pleading for her to back him up. She looks into "
      "the lens with a sweet, blank smile, mouth closed.")
again("p1c", "p1a", "singer_trench_combo", f"At the pickup counter she lifts a fresh giant white paper coffee cup off the counter, "
      f"seen from the waist up, turning toward the camera to leave. {SING}")
again("p1d", "v1a", "singer_trench_combo", f"A medium shot on the sidewalk: an eager young canvasser in a bright orange charity "
      f"vest thrusts a clipboard and pen right at her from the side, and she walks on past it toward the camera. {COFFEE}. {SING}")

# ---- chorus 1: rush hour ----------------------------------------------------------------------------
multi("c1a", "gridlock", ["singer_trench_combo"], f"In the gridlocked intersection of image 1, {TRENCH}, walks toward the camera "
      f"down the narrow gap between two lanes of jammed yellow taxis, seen from the knees up. {COFFEE}. {SING} The drivers on both "
      "sides lean out of their windows yelling, one pressing his horn with his whole palm.")
edit("c1b", "gridlock", "Change the camera: a low close view of the back wheel of a red car stuck in a deep grey slush puddle "
     "beside the kerb, the tyre spinning and throwing up a huge fan of dirty water across the frame.",
     keep="Keep the same morning street, sun and look as image 1.")
multi("c1c", "f_i07", ["singer_trench_combo"], f"{SAME} The sidewalk below the stoop of image 1 is crowded with startled residents "
      "who have fled a fire alarm: people in bathrobes, towels, pyjamas and hair curlers, an old man holding a cat, a little grey "
      "smoke drifting from an upstairs window. She walks along the sidewalk through the middle of them toward the camera, seen from "
      f"the waist up. {COFFEE}. {SING}")
edit("c1d", "f_c1c", "Change the camera: a medium close-up of one embarrassed bald man in a maroon bathrobe in the crowd holding up "
     "a blackened, smoking toaster in both hands, wincing. The woman in purple is no longer in the frame.",
     keep="Keep the same street, crowd, sun and look as image 1.")
edit("c1e", "f_v1a", "Change the camera: a medium shot of a young dog walker in the middle of the sidewalk trussed up from knees to "
     "chest in six tangled leashes, six different dogs pulling in six directions around her. The woman in purple is no longer in "
     "the frame.", keep="Keep the same sidewalk, morning light and look as image 1.")
again("c1f", "v1a", "singer_trench_combo", "It is suddenly pouring with rain: heavy rain streaks across the frame, the pavement is "
      "shining wet and people in the background run for cover holding newspapers over their heads. She stands dry under an open "
      f"purple umbrella held over her shoulder, seen from the waist up, facing the camera. {SING}")

# ---- instrumental: to the office ---------------------------------------------------------------------
edit("k1", "f_c1f", f"Change the camera: a wider shot from behind her as she walks away down the wet sidewalk under her purple "
     f"umbrella, the rain lighter now, and close behind her heels trots {PIG}, following her.",
     keep="Keep the same wet sidewalk, light and look as image 1.")
multi("k2", "f_k1", ["owner_combo", "pig_sheet"], f"The same wet sidewalk as image 1. In the middle of the frame {OWNER}, the man "
      "from image 2, soaked to the skin, has slipped mid-run and is falling flat on his back into a big puddle, legs in the air, a "
      "splash going up, the empty red leash flying from his hand. In the distance a little pink piglet trots away.")
multi("k3", "tower", ["singer_trench_combo"], f"At the office tower of image 1, {TRENCH}, steps into the brass revolving door, seen "
      f"from behind and from the knees up, one hand on the glass. {COFFEE}.")
multi("k4", "office", ["singer_suit_combo"], f"In the office of image 1, {SUIT}, walks out of the far end of the corridor toward "
      f"the camera, seen full length, a slim purple folder under her arm. {CALM} Office workers in grey and beige at the cubicles.")

# ---- verse 2: the office (power suit) -----------------------------------------------------------------
multi("v2a", "desk", ["singer_suit_combo"], f"At the desk of image 1, {SUIT}, sits at the laptop facing the camera, seen from the "
      "waist up. Leaning over the cubicle wall beside her is a sweaty young coworker in a short-sleeved shirt and tie, clutching a "
      f"big crumpled bouquet of yellow sticky notes out toward her like flowers. {SING}")
edit("v2b", "f_k4", "Change the camera: the office corridor seen from behind a sweaty young man in a short-sleeved shirt and tie "
     "as he walks away down it, yellow sticky notes fluttering down from his hands and lying in a long trail behind him on the "
     "carpet. The woman in purple is no longer in the frame.", keep="Keep the same office, light and look as image 1.")
again("v2c", "v2a", "singer_suit_combo", "She sits at the desk, seen from the waist up, and a queue of three anxious coworkers "
      "stands beside the cubicle: the first holds a jammed printer paper tray out to her, the second a broken stapler, the third a "
      f"tangled phone cord. She slides the printer tray back toward him across the desk with two fingers. {SING}")
again("v2d", "k4", "singer_suit_combo", f"She stands in the office corridor seen from the waist up, facing the camera, pointing "
      "off down the corridor with a purple pen, and three coworkers holding a printer tray, a stapler and a phone cord crowd beside "
      f"her, turning to look where she points. {SING}")
edit("v2e", "office", "Change the camera: a close view of the hanging sign over the doorway at the far end of the corridor. The "
     "sign reads WRONG DEPARTMENT in bold black capital letters with a big black arrow pointing to the right, on a white sign.",
     keep="Keep the same office, light and look as image 1.")

# ---- pre-chorus 2: hooked -----------------------------------------------------------------------------
edit("q1", "office", "Every cubicle is occupied: office workers in grey, beige and blue sit hunched over their phones, every face lit "
     "by its screen, mouths hanging open, thumbs on the glass, nobody looking up.")
multi("q2", "f_q1", ["singer_suit_combo"], "The same office as image 1, with the same lighting and the same hunched phone-scrolling workers. "
      f"{SUIT[0].upper() + SUIT[1:]}, walks down the corridor between them toward the camera, seen from the waist up, a slim "
      f"purple folder under her arm. {SING}")
multi("q3", "f_q1", ["pig_sheet", "owner_combo"], f"The same office as image 1. {PIG}, as in image 2, races down the corridor toward "
      "the camera; the office workers on either side shriek and leap up onto their desk chairs, papers flying, and behind it "
      f"{OWNER}, the man from image 3, sprints after it with his arms out.")
again("q4", "v2a", "singer_suit_combo", f"She sits at the desk facing the camera, seen from the chest up, perfectly composed, while "
      f"behind her over the cubicle walls flying papers and a toppled water cooler show chaos running past. {SING}")
again("q5", "v2a", "singer_suit_combo", "She sits at the desk, seen from the waist up, both hands on the open laptop lid about to "
      f"close it; on the cubicle wall behind her a round clock reads exactly five o'clock. {SING}")

# ---- chorus 2: the supermarket (tracksuit) ------------------------------------------------------------
multi("c2a", "market", ["singer_track_combo"], f"In the supermarket aisle of image 1, {TRACK}, pushes a shopping trolley toward "
      f"the camera, seen from the waist up, a few groceries in the trolley. {SING}")
edit("c2b", "checkout", "A furious middle-aged man in a red polo shirt pounds both fists on the screen of the nearest "
     "self-checkout machine, its screen glowing red with the words UNEXPECTED ITEM, a single banana in the bagging area.")
multi("c2c", "checkout", ["singer_track_combo"], f"In the checkout area of image 1, a crowd of frantic shoppers swarm and elbow "
      f"around the 50% OFF bin, grabbing with both hands. In front of them {TRACK}, strolls past toward the camera carrying one "
      f"shopping bag, seen from the waist up. {SING}")
again("c2d", "c2a", "singer_track_combo", "A medium shot in the aisle: a wild-eyed man stands behind a shopping trolley piled "
      "impossibly high with a teetering tower of toilet roll packs, holding one pack out to her at arm's length. She pushes her "
      "trolley past him with a polite smile, mouth closed.")
multi("c2e", "market", ["pig_sheet", "owner_combo"], f"In the supermarket aisle of image 1, {PIG}, as in image 2, sits in the "
      "child seat of a shopping trolley munching a whole head of lettuce, and further up the aisle "
      f"{OWNER}, the man from image 3, sprints toward it with his arms outstretched.")
multi("c2f", "carpark", ["singer_track_combo"], f"At the car park exit of image 1, {TRACK}, carrying a shopping bag, ducks under "
      "the red-and-white barrier arm, seen from the waist up close to the camera, while in the booth behind her a grumpy bald "
      f"attendant with a big moustache scowls out of the sliding window. {SING}")

# ---- instrumental: evening (the wipe to the sequin dress) ------------------------------------------------
again("k5", "c2f", "singer_track_combo", "She walks across the car park toward the camera seen full length, carrying her shopping "
      "bag, and a white delivery van is driving across the frame just in front of her from the left, its front already covering "
      "the left third of the picture.")
multi("k5_end", "carpark", ["singer_dress_combo"], f"At the car park of image 1 in warm sunset light, {DRESS}, stands seen full "
      "length, one hand on her hip, a small wrapped gift with a gold bow in the other hand, as the back of a white delivery van "
      "leaves the right edge of the frame.")
multi("k6", "suburb", ["singer_dress_combo"], f"On the sidewalk of image 1, {DRESS}, walks toward the camera seen from the knees "
      f"up, carrying a small wrapped gift with a gold bow, the balloon-tied party gate behind her. {CALM}")
edit("k7", "party", "Change the camera: a medium shot of the party host, a harried man in a Hawaiian shirt and an apron, at the "
     "barbecue grill as a huge burst of flame leaps up from it, a spatula in one hand and a crying baby on his hip, kids running "
     "past behind him.", keep="Keep the same backyard, sunset light and look as image 1.")
multi("k8", "party", ["pig_sheet", "owner_combo"], f"At the party of image 1, {PIG}, as in image 2, stands on the long table with its "
      f"face buried in the big frosted birthday cake, and {OWNER}, the man from image 3, dives full length across the table toward "
      "it, paper plates and cups flying, guests jumping back.")

# ---- bridge: the party ------------------------------------------------------------------------------------
multi("b1", "party", ["singer_dress_combo"], f"At the party of image 1, {DRESS}, stands in the foreground seen from the waist up, "
      "holding a red plastic cup of punch, facing the camera. Behind her the harried host in a Hawaiian shirt and apron juggles "
      f"a flaming spatula, a crying baby and a wobbling cake. {SING}")
again("b2", "b1", "singer_dress_combo", "A medium two-shot: the harried host in the Hawaiian shirt holds a red-faced screaming baby "
      "out to her at arm's length with a huge proud smile, and she looks down at the baby, eyebrows raised, mouth closed.")
again("b3", "b1", "singer_dress_combo", f"She holds the screaming baby out at arm's length in both hands, handing it back toward "
      f"the host at the edge of the frame, and looks into the lens, seen from the waist up. {SING}")
again("b4", "b1", "singer_dress_combo", f"She walks away across the lawn toward the camera and the gate, seen from the knees up, "
      f"glancing back over her shoulder, the party behind her. {SING}")
edit("b5", "f_b1", "Change the camera: a high wide view of the whole backyard party in uproar, smoke from the grill, the cake "
     "smashed, people shouting, and at the far end the small figure of the woman in the purple sequin dress walking out through "
     "the gate.", keep="Keep the same backyard, sunset light and look as image 1.")
multi("b6", "suburb", ["singer_dress_combo"], f"On the sidewalk of image 1 at dusk, a close-up of {DRESS}, her face and shoulders "
      f"filling the frame, the warm streetlights and fence soft behind her. {SING}")
edit("b7", "party", "The lawn sprinklers have burst on all over the backyard, jets of water spraying everywhere; guests shriek "
     "and run with their arms over their heads, the cake on the table being soaked.",
     keep="Keep the same backyard, camera and look as image 1.")
again("b8", "k6", "singer_dress_combo", "She stands on the sidewalk outside the wooden fence, seen from the waist up, closing the "
      "gate behind her with one hand, perfectly dry, while water from the sprinklers sprays and spatters over the top of the "
      "fence behind her. Mouth closed, a small satisfied smile.")

# ---- breakdown: the walk home (jacket) ---------------------------------------------------------------------
multi("d1", "night", ["singer_jacket_combo"], f"On the night street of image 1, {JACKET}, walks toward the camera under the "
      f"streetlights, seen from the waist up. {SING}")
edit("d2", "night", "Change the camera: looking up at a lit second-floor window where a man in a white vest leans out shaking "
     "his fist at the street, while below at the kerb a parked car's hazard lights flash orange.",
     keep="Keep the same night street, light and look as image 1.")
edit("d3", "night", "Change the camera: a close view of one lit apartment window at night: behind the glass the silhouettes of a "
     "man and a woman arguing, arms waving, and a pot plant flying through the air between them.",
     keep="Keep the same night street, light and look as image 1.")
again("d4", "d1", "singer_jacket_combo", "The fire hydrant at the kerb has burst and shoots a tall white geyser of water into the "
      "air, the street flooding. She steps neatly around the spreading water toward the camera, seen full length, not looking at it, "
      "mouth closed.")

# ---- final chorus: the subway ----------------------------------------------------------------------------
multi("f1", "subway", ["singer_jacket_combo"], f"On the subway platform of image 1, {JACKET}, stands in the foreground facing the "
      "camera, seen from the waist up. Behind her a big man in a hi-vis work jacket is kicking and punching the glowing vending "
      f"machine against the wall. {SING}")
edit("f2", "nightclub", "Change the camera: on the wet street outside the nightclub, a young man in a baseball cap is mid-leap over "
     "a huge black puddle, arms windmilling, clearly about to land in it, while three friends behind him cheer with their arms up.",
     keep="Keep the same night street, neon light and look as image 1.")
multi("f3", "nightclub", ["singer_jacket_combo"], f"On the street outside the nightclub of image 1, {JACKET}, walks past the long "
      f"queue and the velvet rope toward the camera, seen from the waist up, the big bouncer behind her. {SING}")
edit("f4", "nightclub", "A sudden gust whips a whirlwind of litter, paper cups and flyers spinning around the nightclub queue; "
     "people flail, shield their faces and grab at their hair.", keep="Keep the same night street, camera, neon and look as image 1.")
edit("f5", "subway", "Change the camera: low at floor level on the platform, a big brown rat drags a whole slice of pepperoni pizza "
     "across the yellow safety line toward the camera, and behind it passengers' legs leap away.",
     keep="Keep the same subway platform, light and look as image 1.")
again("f6", "f1", "singer_jacket_combo", "A close-up of her face and shoulders filling the frame on the platform, the vending "
      f"machine soft behind her. {SING}")

# ---- outro: home (robe) --------------------------------------------------------------------------------
again("o1", "i04", "singer_jacket_combo", f"Night now, the hallway lit by its warm ceiling lights. She stands in the hallway in her "
      f"cropped purple leather jacket and purple sequin dress, seen from the waist up, looking down at {PIG}, curled up fast asleep "
      "on her doormat in front of the purple door 4B. Mouth closed, eyebrows raised.", extra=["pig_sheet"])
again("o2", "o1", "singer_jacket_combo", f"A medium close-up of her in the hallway, looking into the lens, one hand lifted in a "
      f"small shrug. {SING}")
edit("o3", "f_o1", "Change the camera: low on the carpet in front of the purple door 4B, which is now closed. The little pink "
     "piglet in its red harness is curled up asleep on the doormat, filling the foreground, the woman gone inside.",
     keep="Keep the same hallway, night light and look as image 1.")
multi("o4", "living", ["singer_robe_combo"], f"In the living room of image 1 at night, {ROBE}, sits curled up on the purple velvet "
      f"sofa holding a mug of tea in both hands, seen from the waist up, facing the camera. {SING}")
again("o5", "o4", "singer_robe_combo", "She stands at the window, seen from behind and from the waist up, drawing the curtains "
      "closed with both hands; outside the window the city flashes with red and blue emergency lights.")
again("o6", "o4", "singer_robe_combo", "She sits on the purple sofa, seen from the waist up, reaching over to the warm table lamp "
      "with one hand on its switch, about to turn it off. Mouth closed, eyes half-lidded, content.")


# ---- second pass: fixes after reviewing the first set ----------------------------------------------
# The "only purple" line leaked: with her out of the frame, Flux dressed a stranger in purple instead.
LOOK_NOHER = ("Glossy late-1990s R&B music video look: vivid saturated colour, crisp bright light, wide-angle lens, 35mm film, "
              "fine grain. Photorealistic. Everyone wears ordinary everyday colours: grey, navy, brown, denim, red and green.")
NO_HER = ["i01", "i02", "i03", "v1b", "v1d", "p1a", "c1b", "c1d", "c1e", "k2", "v2b", "v2e", "q1", "q3", "c2b", "c2e", "k7", "k8",
          "b5", "b7", "d2", "d3", "f2", "f4", "f5", "o3"]
for _sid in NO_HER:
    F[_sid]["text"] = F[_sid]["text"].replace(LOOK, LOOK_NOHER)
F["p1a"]["text"] = F["p1a"]["text"].replace(LOOK_NOHER, LOOK)          # she is in the queue in this one
F["b5"]["text"] = F["b5"]["text"].replace(LOOK_NOHER, LOOK)
# Flux misspelled the sign: spell it out letter by letter.
edit("v2e", "office", "Change the camera: a close view of a white sign hanging over the doorway at the far end of the corridor, "
     "with two words on two lines in bold black capital letters, \"WRONG\" on the first line and \"DEPARTMENT\" (D-E-P-A-R-T-M-E-N-T) "
     "on the second, and a big black arrow pointing right. Nobody else in frame but office workers at their desks.",
     keep="Keep the same office, light and look as image 1.")
F["v2e"]["text"] = F["v2e"]["text"].replace(LOOK, LOOK_NOHER)
# She became the tangled dog walker when this was an edit of her master; start from the empty sidewalk.
edit("c1e", "sidewalk", "In the middle of the sidewalk a young dog walker with a blonde ponytail, in a grey hoodie and jeans, is "
     "trussed up from knees to chest in six tangled leashes, six different dogs pulling in six directions around her.",
     keep="Keep the same sidewalk, camera, morning light and look as image 1.")
F["c1e"]["text"] = F["c1e"]["text"].replace(LOOK, LOOK_NOHER)
again("c2d", "c2a", "singer_track_combo", "A medium shot in the aisle. On the left a wild-eyed bald man in a brown cardigan stands "
      "behind his own shopping trolley piled impossibly high with a teetering tower of toilet roll packs, holding one pack out at "
      "arm's length toward her. On the right she pushes her own trolley past him, both her hands on its handle, with a polite "
      "smile, mouth closed.")
# Flux could not spell the sign in an edit; Krea spelled it right in 4/4 plates.
plate("v2e", "sign")

# c1c from the i07 master kept her on the stairs AND added her on the sidewalk: two of her. Start from the plate.
multi("c1c", "stoop", ["singer_trench_combo"], "On the sidewalk in front of the stoop of image 1, a crowd of startled residents "
      "who have fled a fire alarm: people in bathrobes, towels, pyjamas and hair curlers, an old man holding a cat, a little grey "
      f"smoke drifting from an upstairs window. The stoop steps are empty. Through the middle of the crowd {TRENCH}, walks toward "
      f"the camera, seen from the waist up, the only woman in purple. {COFFEE}. {SING}")

# ...and the crowd came back in lavender robes: name their colours, drop "the only purple" for this one.
F["c1c"]["text"] = (F["c1c"]["text"].replace(" the only woman in purple.", ".")
                    .replace("She is the only person wearing purple.", "The residents' robes and pyjamas are white, grey, "
                             "navy, yellow, red-and-white striped and green tartan; she alone wears violet."))

# ---- third pass: the user's notes on rough cut v1 ---------------------------------------------------
# One cup, the same cup: a trench sheet with the cup in her right hand (Flux edit of the sheet).
CUP = ("She holds one ordinary takeaway coffee cup in her right hand, a white paper cup with a brown cardboard sleeve and a "
       "white lid, normal size, as in image 2")
for _sid in ("i04", "i07", "v1a", "v1c", "v1e", "p1b", "p1c", "p1d", "c1a", "c1c", "k3"):
    _f = F[_sid]
    _f["text"] = (_f["text"].replace(COFFEE, CUP)
                  .replace("a fresh giant white paper coffee cup", "one white takeaway coffee cup with a brown sleeve")
                  .replace("giant white paper coffee cup", "white takeaway coffee cup"))
    _f["refs"] = ["singer_trenchcup_combo" if r == "singer_trench_combo" else r for r in _f["refs"]]
# 0:21 the hallway shrank: same camera as the i04 master, the owner bursts out of a door on the left.
multi("i06", "f_i04", ["owner_combo", "singer_trenchcup_combo"], "Keep the exact same camera position, lens, hallway length, "
      "doors and lighting as image 1. One of the doors on the left side of the hallway has burst open and "
      f"{OWNER}, the man from image 2, charges out of it into the hallway toward the camera, arms flailing, mouth wide open "
      "shouting, an empty red leash in one hand. The woman from image 3 still stands by her open purple door on the right "
      "in her violet trench coat, calmly sipping from one white takeaway coffee cup with a brown sleeve, watching him.")
# 0:26 he ran backward: seen from behind, chasing the truck away from us with a huge bag of garbage.
multi("i07", "stoop", ["singer_trenchcup_combo"], f"On the stoop of image 1, {TRENCH}, has just stepped out of the front door "
      f"at the top of the steps, seen full length, purple sunglasses on her nose. {CUP}. {CALM} Down on the street a green "
      "garbage truck is driving away from the camera, and a dripping wet man wearing only a white bath towel runs after it, "
      "seen from behind, away from the camera, hauling a huge overstuffed black garbage bag over his shoulder.")
# 1:22 the umbrella floated: put the handle in her hand.
edit("k1", "f_c1f", "Change the camera: a wider shot from behind her as she walks away down the wet sidewalk, holding the "
     "purple umbrella up by its curved handle in her right hand, the canopy over her head and shoulder, the rain lighter "
     f"now, and close behind her heels trots {PIG}, following her.", keep="Keep the same wet sidewalk, light and look as image 1.")
# The babies changed every shot: one host and one baby, from references.
HOSTB = ("the sunburned man from image 3 in his teal Hawaiian shirt with yellow flowers and grey apron, with the chubby blond "
         "baby boy in a light blue onesie from image 4")
multi("k7", "party", ["host_combo", "baby_sheet"], "In the backyard of image 1, a medium shot of the party host, the sunburned "
      "man from image 2 in his teal Hawaiian shirt with yellow flowers and grey apron, at the barbecue grill as a huge burst of "
      "flame leaps up from it, a spatula in one hand and the chubby blond baby boy in a light blue onesie from image 3 crying "
      "on his hip, kids running past behind him.")
F["k7"]["text"] = F["k7"]["text"].replace(LOOK, LOOK_NOHER)
multi("b1", "party", ["singer_dress_combo", "host_combo", "baby_sheet"], f"At the party of image 1, {DRESS}, stands in the "
      f"foreground seen from the waist up, holding a red plastic cup of punch, facing the camera. Behind her {HOSTB} wailing on "
      f"his hip, juggles a flaming spatula and a wobbling cake. {SING}")
multi("b2", "f_b1", ["singer_dress_combo", "host_combo", "baby_sheet"], f"{SAME} A medium two-shot: {HOSTB}, holds the "
      "screaming baby out to her at arm's length with a huge proud smile, and she looks down at the baby, eyebrows raised, "
      "mouth closed.")
multi("b3", "f_b1", ["singer_dress_combo", "host_combo", "baby_sheet"], f"{SAME} She holds the chubby blond baby boy in the "
      "light blue onesie from image 4 out at arm's length in both hands, handing him back toward the sunburned host from "
      f"image 3 at the edge of the frame, and looks into the lens, seen from the waist up. {SING}")
multi("b5", "f_b1", ["host_combo", "baby_sheet"], "The same backyard party as image 1, now a high wide view of the whole party "
      "in uproar, smoke from the grill, the cake smashed, people shouting, the sunburned host from image 2 in his teal Hawaiian "
      "shirt in the middle holding the chubby blond baby from image 3, and at the far end the small figure of a woman in a "
      "purple sequin dress walking out through the gate.")
# 3:54 the curtains hung in the middle of the room: hang them on a rod over the window.
multi("o5", "living", ["singer_robe_combo"], f"In the living room of image 1 at night, {ROBE}, stands right at the window, "
      "seen from behind and from the waist up. Two long curtain panels hang from a rod fixed across the top of the window frame, "
      "one on each side of the glass, and she holds one panel in each hand, pulling them together across the window; outside "
      "the glass the city flashes with red and blue emergency lights.")
# Signs: Krea plates with the words spelled right.
for _sid in ("c2b", "c2c", "c2f", "k5_end", "d1", "d2", "d3"):
    F[_sid]["src"] = {"checkout": "checkout2", "carpark": "carpark2", "night": "night2"}[F[_sid]["src"]]

# ---- the finale: her street falls apart and everyone she passed today dances behind her -------------
LINE = ("a young barista in a green apron, a young office worker in a short-sleeved shirt and tie, a blonde dog walker in a grey "
        "hoodie, a young commuter in a coffee-stained white shirt, a sunburned dad in a teal Hawaiian shirt and grey apron, and at "
        "the end the skinny grey-haired man from image 3 in his green-and-orange striped bathrobe, with the little pink piglet in "
        "a red harness from image 4 at his feet")
FIN = ["singer_jacket_combo", "owner_combo", "pig_sheet"]
multi("f1", "night_chaos", FIN, f"In the middle of the wet street of image 1 at night, {JACKET}, struts toward the camera, "
      f"seen from the knees up, leading a dance line. Behind her in two staggered rows, all caught in the same dance move with "
      f"one hip popped and both arms snapped out to the side: {LINE}. Behind them the street falls apart: the hydrant geyser, "
      f"the steam from the manholes, the sparks and flying flyers of image 1. {SING}")
multi("f2", "f_f1", FIN, f"{SAME} A low, closer angle on the dance line behind her: the dancers all drop into the same deep "
      "knee bend with both arms flung up over their heads, the hydrant geyser and the shower of sparks erupting behind them. "
      "She is at the front, seen from the waist up, mouth closed.")
multi("f3", "f_f1", FIN, f"{SAME} A medium shot of her from the waist up, close to the camera, the dance line behind her over "
      f"her shoulder all popping their shoulders in time, steam and flyers swirling. {SING}")
multi("f4", "f_f1", FIN, "The same street and dance line as image 1. A medium shot of the end of the dance line: the skinny "
      "grey-haired man from image 2 in his striped bathrobe, hopelessly out of step, arms flailing the wrong way, and at his feet "
      "the little pink piglet from image 3 in its red harness trotting perfectly in step with the dancers beside him. Steam and "
      "sparks behind them.")
F["f4"]["text"] = F["f4"]["text"].replace(LOOK, LOOK_NOHER)
multi("f5", "f_f1", FIN, f"{SAME} She stands at the front, seen from the knees up, one hand raised straight out toward the "
      "camera, palm out, like a traffic cop saying stop; behind her the whole dance line has frozen mid-move. Steam, sparks "
      f"and the hydrant geyser behind them. {SING}")
multi("f6", "f_f1", FIN, f"{SAME} The final pose: she stands at the front, seen from the knees up, one hand on her hip and her "
      "chin up, and the whole dance line behind her strikes the same pose, arms thrown up in a V. Behind them a huge burst of "
      f"orange sparks fans out across the night sky. {SING}")

# two pigs in k1; a second Hawaiian-shirt host in b1/b3; the FOOD MART sign repainted as "A ART"
F["k1"]["text"] = F["k1"]["text"].replace(f"close behind her heels trots {PIG}, following her.",
    f"close behind her heels trots one single {PIG[2:]}, following her: one pig in the whole picture.")
GUESTS = " The other guests wear plain T-shirts, polo shirts and sundresses; he is the only man in a Hawaiian shirt and apron."
for _sid in ("b1", "b3"):
    F[_sid]["text"] = F[_sid]["text"].replace(f" {SING}", GUESTS + f" {SING}")
SIGN = (' Behind, the supermarket\'s big red sign reads "FOOD MART", its letters exactly as in image 1.')
for _sid in ("c2f", "k5_end"):
    F[_sid]["text"] = F[_sid]["text"].replace(LOOK, SIGN.strip() + " " + LOOK)
multi("k5", "carpark2", ["singer_track_combo"], f"At the car park exit of image 1, {TRACK}, walks across the car park toward the "
      "camera seen full length, carrying a shopping bag, and a white delivery van is driving across the frame just in front of "
      f"her from the left, its front already covering the left third of the picture.{SIGN}")
# k1: "one pig" still gave two; edit the original one-pig frame instead and just put the umbrella in her hand.
edit("k1", "k1_v1", "Her right arm is raised and her right hand grips the curved handle of the purple umbrella, holding the "
     "umbrella up over her head; the umbrella's shaft runs down into her hand.",
     keep="Keep image 1 exactly as it is: the same street, the same woman seen from behind, the same single piglet, the same light.")
# b3: the baby went back to a stranger; edit the b2 frame so the host in it takes him back.
edit("b3", "f_b2", "Now she holds the chubby blond baby out at arm's length in both hands, handing him back to the sunburned man "
     "in the teal Hawaiian shirt and apron, whose hands reach out to take him, and she looks into the lens with a sly half-smile, "
     "mouth closed.", keep="Keep the same backyard, the same woman, the same sunburned host, the same baby and light as image 1.")

# ---- fourth pass: the user's notes on rough cut v2 ---------------------------------------------------
# 0:48 she read as a shocked barista: edit the p1b frame (the look the user liked) into the argument.
edit("p1a", "f_p1b", "The red-faced man in the tan golf jacket now leans over the counter jabbing his finger at the young "
     "barista in the green apron behind it. The woman in the violet trench coat stands calmly in the customers' queue beside "
     "him, on the customers' side of the counter, holding her coffee cup, watching him with a small amused half-smile, mouth "
     "closed.", keep="Keep the same coffee shop, camera, light and the same three people as image 1.")
F["p1a"]["text"] = F["p1a"]["text"].replace(LOOK, LOOK.replace(" She is the only person wearing purple.", ""))
# 1:17 a hand went missing and a passer-by grew a newspaper umbrella: both her hands in frame, newspapers folded flat.
again("c1f", "v1a", "singer_trenchcup_combo", "It is suddenly pouring with rain: heavy rain streaks across the frame, the "
      "pavement is shining wet and people in the background run for cover holding folded flat newspapers over their heads. "
      "She stands dry under an open purple umbrella, seen from the waist up, facing the camera, both hands in view: her right "
      "hand holds the umbrella's handle at her shoulder and her left hand holds her white takeaway coffee cup. " + SING)
# 1:50 the same angle twice, empty then with her: a different angle for the scrolling workers.
edit("q1", "office", "Change the camera: a close side view looking along one row of desks: five office workers in grey, beige "
     "and blue sit side by side in profile, each hunched over a phone held close to the face, every face lit blue-white by its "
     "screen, mouths hanging open.", keep="Keep the same office colours, light and look as image 1.")
F["q1"]["text"] = F["q1"]["text"].replace(LOOK, LOOK_NOHER)
# 1:59 the water jug behind her melted: put a filing cabinet there.
edit("q4", "f_q4", "Replace the water cooler and its big plastic bottle behind her with a tall grey metal filing cabinet with a "
     "potted plant on top.", keep="Keep image 1 exactly as it is: the same woman, desk, laptop, cubicle walls, flying papers and light.")
# 2:10 the angry man and then her from the same angle: shoot him close and from the side.
edit("c2b", "checkout2", "Change the camera: a close side view of one self-checkout machine: a furious middle-aged man in a red "
     "polo shirt, seen from the side from the waist up, pounds both fists on its screen, which glows red with the words "
     "\"UNEXPECTED ITEM\"; a single banana sits in the bagging area. The sale signs are soft in the background.",
     keep="Keep the same supermarket, light and look as image 1.")
F["c2b"]["text"] = F["c2b"]["text"].replace(LOOK, LOOK_NOHER)
# 2:43 the baby held out sideways and screaming was nightmare fuel: from the b3 frame, held upright, fussing.
edit("b2", "f_b3", "Now the sunburned host in the teal Hawaiian shirt holds the chubby blond baby upright in both hands under "
     "the arms, holding him out toward her with a big proud grin; the baby's face is calm and pouting, his legs dangling. She "
     "looks at the baby with her eyebrows raised, her hands at her sides, mouth closed.",
     keep="Keep the same backyard, the same woman, the same host, the same baby and light as image 1.")

# c1f: newspapers held overhead still read as newspaper umbrellas; c2b: Flux misspelled the screen. No props, no words.
F["c1f"]["text"] = F["c1f"]["text"].replace("holding folded flat newspapers over their heads",
    "hunched over with their jackets pulled up over their heads").replace("her right hand holds the umbrella's handle at her shoulder and her left hand holds her white takeaway coffee cup",
    "her left hand grips the umbrella's handle, the shaft running up from her fist to the canopy, and her right hand holds her white takeaway coffee cup")
F["c2b"]["text"] = F["c2b"]["text"].replace('which glows red with the words "UNEXPECTED ITEM"', "which glows solid red with one big white warning triangle")

# ---- fifth pass: the user's notes on the 2x cut ----------------------------------------------------
# 0:06 his arm passed through the sash: a different, wide-open window (also unlike i03's), and he stays inside the room.
edit("i02", "window_b", "Inside, a step back from the open window in the middle of the small kitchen, framed from the waist "
     "up, a bleary man in blue striped pyjamas and wild bed-head raises a slipper high over a ringing red alarm clock on the "
     "kitchen table in front of him, about to smash it, face scrunched in fury. His arms and the clock are well inside the room.")
F["i02"]["text"] = F["i02"]["text"].replace(LOOK, LOOK_NOHER)
# 0:59 the canvasser came back as a second her, with a warping clipboard: a different person, one flat flyer.
again("p1d", "v1a", "singer_trenchcup_combo", "A medium shot on the sidewalk: a lanky young white man with messy red hair and "
      "freckles, in a bright orange charity vest, leans in from the side holding one paper flyer out at her; she walks on past "
      f"it toward the camera. {CUP}. {SING}")
# 1:05 heads came up through the taxi roofs: a fender bender, the two drivers out of their cars.
multi("c1a", "gridlock", ["singer_trenchcup_combo"], "In the intersection of image 1, a fender bender: a yellow taxi has "
      "crumpled into the back of a red sedan in the middle of the road, steam rising from the taxi's bonnet, the traffic stopped "
      "behind them. The two drivers stand outside their cars yelling at each other, arms waving: a heavyset man in a blue "
      "tracksuit on the left and a woman in a yellow raincoat on the right. Between the two of them "
      f"{TRENCH}, walks toward the camera, seen from the knees up. {CUP}. {SING}")
# 2:59 her skin went waxy and creased in the close-up: smooth it on the frame the user loves.
edit("b6", "f_b6", "Give her smooth, even, glowing skin on her face and neck, youthful and soft, the same age and face as in a "
     "beauty portrait, with a warm dusk glow on her cheeks.", keep="Keep image 1 exactly as it is: the same framing, woman, "
     "expression, hair, makeup, earrings, dress, street and light.")
# 3:56 the curtains she had just closed were open again.
edit("o6", "f_o6", "The curtains are now drawn closed across the whole window, two long panels meeting in the middle, the "
     "city lights only a faint glow through the fabric.", keep="Keep image 1 exactly as it is: the same room, woman, sofa, "
     "lamp and light.")

edit("o6", "o6_v3", "Cover the whole window behind her with two long closed lavender curtains hanging from a rod above it, "
     "meeting in the middle, so no glass and no city lights show at all; only a faint red and blue glow through the fabric.",
     keep="Keep image 1 exactly as it is: the same room, the same woman in her pale lavender silk robe and headwrap, the same "
     "sofa, lamp, records and light.")

edit("o6", "o6_v4b", "The dark window glass between the two lavender curtains is gone: the window is now completely hidden behind "
     "one continuous wall of drawn lavender curtain fabric hanging straight down from the rod to the radiator, soft vertical "
     "folds across its entire width, with no gap and no glass visible anywhere.",
     keep="Keep image 1 exactly as it is: the same room, woman, robe, headwrap, sofa, lamp, records and light.")

# ---- runner -----------------------------------------------------------------------------------
def inp(name):
    return os.path.join(INP, f"nmp_{name}.png")


def ready(sid):
    s = F[sid]
    return all(os.path.exists(inp(r)) for r in [s["src"]] + s.get("refs", []))


def done(sid):
    return os.path.exists(os.path.join(HERE, "frames", f"{sid}.png"))


def stage(sid, path):
    """Keep the full frame in frames/, and a 1120x640 copy in ComfyUI/input for H3 and for later edits."""
    os.makedirs(os.path.join(HERE, "frames"), exist_ok=True)
    im = Image.open(path).convert("RGB")
    im.save(os.path.join(HERE, "frames", f"{sid}.png"))
    ImageOps.fit(im, (1120, 640), Image.LANCZOS).save(inp(f"f_{sid}"))


def build(ids, seed_off=0):
    wfs = []
    for sid in ids:
        s = F[sid]
        if not ready(sid):
            print("  not ready yet:", sid); continue
        if s["kind"] == "plate":
            stage(sid, inp(s["src"])); continue
        seed = SEED0 + list(F).index(sid) + 1000 * seed_off
        name = f"nmp_f_{sid}"
        for old in glob.glob(os.path.join(OUT, f"{name}_[0-9][0-9][0-9][0-9][0-9]_.png")):
            os.remove(old)
        if s["kind"] == "edit":
            wfs.append(build_flux_batch.build(name, f"nmp_{s['src']}.png", "", [s["text"]], "", seed, 8))
        else:
            r = [f"nmp_{x}.png" for x in s["refs"]]
            refs = {"reference_image1": f"nmp_{s['src']}.png", "reference_image2": r[0],
                    "reference_image3": r[1] if len(r) > 1 else r[0], "reference_image4": r[2] if len(r) > 2 else r[0]}
            wfs.append(build_flux_multiref.build(s["text"], name, refs, seed, 1, 8))
    for w in wfs:
        r = subprocess.run([COMFY_EXE, "run", "--workflow", w], capture_output=True, text=True, creationflags=0x08000000)
        if r.returncode:
            print("  FAILED", os.path.basename(w), (r.stdout + r.stderr)[-300:])
    print(f"queued {len(wfs)} Flux jobs")


def wait(limit=3000):
    t0 = time.time()
    while time.time() - t0 < limit:
        q = json.load(urllib.request.urlopen("http://127.0.0.1:8188/queue"))
        if not q["queue_running"] and not q["queue_pending"]:
            break
        time.sleep(5)


def collect(ids):
    n = 0
    for sid in ids:
        got = sorted(glob.glob(os.path.join(OUT, f"nmp_f_{sid}_[0-9][0-9][0-9][0-9][0-9]_.png")), key=os.path.getmtime)
        if got:
            stage(sid, got[-1]); os.remove(got[-1]); n += 1
    print(f"collected {n} frames")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "build":
        off = 0
        if args[:1] == ["--seed"]:
            off, args = int(args[1]), args[2:]
        ids = args or [s for s in F if not done(s)]
        build(ids, off); wait(); collect(ids)
        left = [s for s in F if not done(s)]
        print("still missing:", " ".join(left) if left else "none")
    elif cmd == "collect":
        collect(args or list(F))
    elif cmd == "sheet":
        items = [f"{s}=frames/{s}.png" for s in args[1:] if done(s)]
        subprocess.run([sys.executable, os.path.join(HERE, "contact.py"), os.path.join(HERE, "frames", f"contact_{args[0]}.jpg"),
                        "--cols", "4", "--width", "560"] + items, cwd=HERE)
