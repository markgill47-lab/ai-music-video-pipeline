"""Write the H3 prompt for every shot, slice its audio and queue it (fl2va, first frame from frames.py).

Every shot is a 5 s render that starts on its slot's first beat. "mix" shots pin the full song so her
mouth follows the vocal; "inst" shots pin the instrumental stem so nobody mouths anything.
Shots listed in END also pin a last frame.
  python queue_shots.py                 # queue every shot that has a frame and no render yet
  python queue_shots.py c1a c1b         # queue just these
  python queue_shots.py --seed 1 c1a    # re-roll: new seed, saved as out/c1a_r1.mp4
  python queue_shots.py --collect       # copy finished renders from ComfyUI/output to out/
"""
import glob, json, os, shutil, subprocess, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from build_beat_test import build, frames_for
from shots import rows, spans

COMFY = r"D:\Projects_26\Comfyu\ComfyUI"
MIX, INST = r"audio\not_my_pig.mp3", r"audio\stems\htdemucs\not_my_pig\no_vocals.wav"
SEED0 = 51000
END = {"k5": "k5_end"}

STYLE = ("Live-action, a glossy late-1990s R&B music video: vivid saturated colour, crisp bright light, wide-angle lens, "
         "35mm film.")
HER = "A woman with deep brown skin, big brunette curls and purple eyeshadow"
SINGS = "She (S1) sings {L} her lips shaping every word clearly, cool and unbothered."
SPEAKS = "She (S1) speaks in rhythm, cool and deadpan, {L}"
WALK = "The camera tracks backward in front of her as she walks toward it, Tracking with small amplitude at slow speed."
STATIC, PUSH = "The camera is Static.", "The camera pushes in with small amplitude at slow speed."
HAND = "The camera is handheld and follows the action."
CITY = "Busy city street: traffic, horns, footsteps, distant sirens."
OFFICE = "Open-plan office: keyboards, phones ringing, chatter."
MARKET = "Supermarket: trolley wheels, beeping checkouts, chatter."
PARTY = "Backyard party: chatter, laughter, sizzling grill, kids shrieking."
NIGHT = "Night city: distant traffic, a car alarm, footsteps."
HOME = "A quiet apartment at night, the city faint outside."
HALL = "An apartment hallway: a door, footsteps, muffled voices."

# id: (what happens, camera, soundscape). {L} becomes the sung line.
M = {
    "i01": ("The sun rises behind a red-brick apartment block and the city skyline, the orange light spreading across dozens of windows, steam drifting from rooftop vents.", PUSH, CITY),
    "i02": ("Through a wide-open window with green shutters, a bleary man in striped pyjamas standing inside the kitchen brings a slipper down hard on a ringing red alarm clock on the table in front of him, twice, then glares at it.", STATIC, CITY),
    "i03": ("Through an open apartment window, a frazzled woman in a yellow dressing gown and hair curlers flaps a tea towel wildly at a shrieking smoke alarm while black smoke billows from a toaster.", STATIC, CITY),
    "i04": (f"{HER}, in a violet trench coat and purple sunglasses, steps out of her purple apartment door holding a white takeaway coffee cup in her right hand. She tilts her head and (S1) whispers to the lens {{L}} her lips shaping every word, cool and detached.", PUSH, HALL),
    "i05": ("At floor level in a hallway, a small pink piglet in a red harness trots briskly past a woman's purple ankle boots toward the camera, its red leash trailing along the carpet. The boots stay still.", STATIC, HALL),
    "i06": ("A skinny grey-haired man in a striped bathrobe bursts out of a door on the left of a long hallway and charges down it toward the camera, arms flailing, shouting, waving an empty red leash. The woman in the violet trench coat by the purple door calmly sips from her coffee cup and watches him go.", STATIC, HALL),
    "i07": (f"{HER}, in a violet trench coat, steps out onto the stoop of her building into the morning sun with a coffee cup in her right hand. Down the street a green garbage truck drives away from the camera and a dripping man in a bath towel runs after it, away from the camera, hauling a huge black garbage bag over his shoulder and waving his free arm.", STATIC, CITY),
    "i08": (f"Close on {HER.lower()}, in purple sunglasses, on a sunny stoop. On the beat she pushes the sunglasses up into her curls with one finger and gives the lens a slow, knowing smile.", STATIC, CITY),
    "v1a": (f"{HER}, in a violet trench coat, strolls toward the camera down a busy morning sidewalk with a white takeaway coffee cup in her right hand, swaying a little with each step. Behind her a man in a grey suit fights an umbrella blown inside out. {SINGS}", WALK, CITY),
    "v1b": ("A man in a grey suit on a windy sidewalk wrestles an umbrella that flips inside out again and wraps itself over his head; he staggers in a circle, fighting it.", HAND, CITY),
    "v1c": (f"{HER}, in a violet trench coat, walks toward the camera with her coffee cup while behind her a man in a blue suit screams into his phone on speaker, red-faced. She never looks at him. {SINGS}", WALK, CITY),
    "v1d": ("A young commuter in a white shirt stands frozen on the sidewalk as brown coffee soaks down his shirt from a crushed cup; his mouth drops open and he slowly lifts his arms away from his sides in horror.", STATIC, CITY),
    "v1e": (f"{HER}, in a violet trench coat, strolls toward the camera, takes a leisurely sip from her white takeaway coffee cup, then sings. {SINGS}", WALK, CITY),
    "p1a": ("In a crowded coffee shop, a red-faced man in a tan golf jacket leans over the counter jabbing his finger at a terrified young barista who holds up the wrong cup. The woman in the violet trench coat waits behind him, calm.", HAND, "Coffee shop: espresso machine hissing, chatter, a man shouting."),
    "p1b": (f"In a coffee shop queue, the red-faced man turns to {HER.lower()} for backup, palms up, pleading. She gives the lens a sweet, blank smile and sings. {SINGS}", STATIC, "Coffee shop: espresso machine hissing, chatter."),
    "p1c": (f"{HER}, in a violet trench coat, lifts a white takeaway coffee cup in her right hand from the pickup counter and turns toward the camera to leave, singing. {SINGS}", STATIC, "Coffee shop: espresso machine hissing, chatter."),
    "p1d": (f"On a sunny sidewalk a lanky red-haired young man in an orange charity vest leans in and waves a single flyer at {HER.lower()}; she smiles, side-steps it without breaking stride and walks on toward the camera. {SINGS}", WALK, CITY),
    "c1a": (f"At a fender bender in a city intersection, a taxi crumpled into a red sedan with steam rising from its bonnet, the two drivers stand outside their cars yelling and waving their arms at each other, a big man in a blue tracksuit and a woman in a yellow raincoat. {HER}, in a violet trench coat, walks toward the camera right between them, coffee cup in her right hand, never looking at either. {SINGS}", WALK, "Horns, steam hissing, two people shouting."),
    "c1b": ("Low and close, the back wheel of a red car spins furiously in a deep slush puddle, throwing a huge fan of dirty water across the frame.", STATIC, "Engine revving, tyre whining, water spraying."),
    "c1c": (f"{HER}, in a violet trench coat, walks toward the camera through a crowd of residents in bathrobes and curlers milling on the pavement after a fire alarm, grey smoke drifting from a window above. {SINGS}", WALK, "A fire alarm ringing, people grumbling, a distant siren."),
    "c1d": ("A bald man in a maroon bathrobe holds up a blackened, smoking toaster to the crowd and winces sheepishly as smoke curls up into his face.", STATIC, "A fire alarm ringing, people grumbling."),
    "c1e": ("On a sidewalk a young dog walker spins in place, trussed up in six tangled leashes as six dogs pull in six directions; she topples sideways.", HAND, "Dogs barking, a woman yelping."),
    "c1f": (f"Sudden heavy rain pours down a city sidewalk and people run for cover hunched over with their jackets pulled up over their heads. {HER}, dry under an open purple umbrella whose handle she holds in her left hand, her coffee cup in her right hand, faces the camera and sings. {SINGS}", STATIC, "Heavy rain, people shrieking, splashing footsteps."),
    "k1": ("Seen from behind, a woman in a violet trench coat walks away down a wet sidewalk holding a purple umbrella up by its handle in her right hand, and a small pink piglet in a red harness trots happily at her heels, following her.", "The camera follows behind them, Tracking with small amplitude at slow speed.", "Light rain, trotting hooves, city traffic."),
    "k2": ("On a wet sidewalk a skinny grey-haired man in a soaked striped bathrobe slips mid-run and crashes flat on his back into a big puddle with a splash, legs in the air, the red leash flying from his hand.", STATIC, "A splash, a yelp, rain."),
    "k3": ("Seen from behind, a woman in a violet trench coat steps into a brass revolving door of an office tower and pushes it; the glass panels turn and carry her inside.", STATIC, CITY),
    "k4": (f"{HER}, in a violet power suit and purple cat-eye glasses, walks down an office corridor toward the camera with a slim purple folder under her arm, perfectly composed, as office workers glance up at her.", WALK, OFFICE),
    "v2a": (f"At her office desk {HER.lower()}, in a violet power suit and cat-eye glasses, looks at the lens while a sweaty coworker leans over the cubicle wall holding out a crumpled bouquet of sticky notes. {SINGS}", STATIC, OFFICE),
    "v2b": ("Seen from behind, a sweaty young man in a short-sleeved shirt walks away down an office corridor, yellow sticky notes fluttering from his hands and landing in a trail on the carpet.", "The camera follows behind him, Tracking with small amplitude at slow speed.", OFFICE),
    "v2c": (f"At her desk {HER.lower()}, in a violet power suit, nods politely to a queue of anxious coworkers and with two fingers slides a jammed printer tray back across the desk to the first one. {SINGS}", STATIC, OFFICE),
    "v2d": (f"In an office corridor {HER.lower()}, in a violet power suit, points off down the corridor with a purple pen; the coworkers holding a printer tray, a stapler and a phone cord all turn their heads to look. {SINGS}", STATIC, OFFICE),
    "v2e": ("A hanging office sign reading \"WRONG DEPARTMENT\" with a big arrow sways gently over a doorway under fluorescent lights.", PUSH, OFFICE),
    "q1": ("A row of office workers seen side-on, each hunched over a phone pressed close to the face, faces lit blue-white by the screens, mouths hanging open; nobody looks up.", "The camera glides slowly sideways along the row, Truck with small amplitude at slow speed.", "Office: notification pings, phones buzzing."),
    "q2": (f"{HER}, in a violet power suit, walks toward the camera down an office corridor between rows of workers hunched over their phones; none of them look up. {SINGS}", WALK, "Office: notification pings, phones buzzing."),
    "q3": ("A small pink piglet in a red harness races down an office corridor toward the camera; workers shriek and leap onto their chairs, papers flying, and a grey-haired man in a striped bathrobe sprints after it with his arms out.", HAND, "Screaming, squealing piglet, papers flying."),
    "q4": (f"At her desk {HER.lower()}, in a violet power suit, sits perfectly composed and sings to the lens while chaos runs past behind her cubicle wall, papers flying. {SINGS}", STATIC, "Office chaos: shrieks, a squealing piglet."),
    "q5": (f"At her desk {HER.lower()}, in a violet power suit, glances at the clock on the wall at five o'clock, snaps her laptop shut on the beat, and sings. {SINGS}", STATIC, OFFICE),
    "c2a": (f"{HER}, in a purple velour tracksuit, pushes a shopping trolley toward the camera down a bright supermarket aisle, bobbing her head to the beat. {SINGS}", WALK, MARKET),
    "c2b": ("Close and side-on, a furious man in a red polo shirt pounds both fists on a self-checkout screen glowing red with a warning triangle, shouting at it.", STATIC, "A self-checkout beeping, a man shouting."),
    "c2c": (f"Frantic shoppers swarm and elbow around a 50% OFF bin like bees. {HER}, in a purple velour tracksuit, strolls past them toward the camera with one shopping bag. {SINGS}", WALK, "A crowd jostling and shouting, beeping checkouts."),
    "c2d": ("In a supermarket aisle a wild-eyed man behind a teetering tower of toilet roll holds a pack out at arm's length; the woman in the purple tracksuit pushes her trolley past with a polite smile and the tower wobbles.", STATIC, MARKET),
    "c2e": ("A small pink piglet in a red harness sits in a shopping trolley's child seat munching a whole head of lettuce, while a grey-haired man in a striped bathrobe sprints up the aisle toward it with his arms out.", STATIC, MARKET),
    "c2f": (f"At a car park exit {HER.lower()}, in a purple velour tracksuit, ducks under the red-and-white barrier arm with her shopping bag and straightens up toward the camera, while a grumpy attendant scowls from the booth. {SINGS}", STATIC, "Car park: engines, a ticket machine beeping."),
    "k5": ("In a sunlit car park, a white delivery van drives across the frame from left to right just in front of the camera, filling the picture as it passes.", STATIC, "A van driving past."),
    "k6": (f"{HER}, in a sparkling purple sequin dress, walks toward the camera along a golden-hour suburban sidewalk carrying a small wrapped gift, the balloon-tied party gate behind her.", WALK, "Birdsong, party music in the distance."),
    "k7": ("At a backyard barbecue a sunburned man in a teal Hawaiian shirt and grey apron, a chubby blond baby in a light blue onesie on his hip, flips a burger and a huge burst of flame leaps up from the grill; he jerks back, kids running past behind him.", HAND, PARTY),
    "k8": ("A small pink piglet in a red harness has its face buried in a frosted birthday cake on a party table; a grey-haired man in a striped bathrobe dives full length across the table at it, plates and cups flying, guests jumping back.", HAND, PARTY),
    "b1": (f"At a backyard party {HER.lower()}, in a purple sequin dress, holds a cup of punch and speaks to the lens while behind her the sunburned host in a teal Hawaiian shirt, a chubby blond baby on his hip, juggles a flaming spatula and a wobbling cake. {SPEAKS}", STATIC, PARTY),
    "b2": ("The sunburned host in a teal Hawaiian shirt holds the chubby blond baby in a light blue onesie out to the woman in the purple sequin dress with a huge proud smile; the baby pouts and kicks his legs, and she looks at him, eyebrows raised.", STATIC, "A baby screaming, party chatter."),
    "b3": (f"{HER}, in a purple sequin dress, holds the chubby blond baby in a light blue onesie out at arm's length and hands him straight back to the host, then speaks to the lens. {SPEAKS}", STATIC, "A baby screaming, party chatter."),
    "b4": (f"{HER}, in a purple sequin dress, walks away from the party across the lawn toward the camera, glancing back over her shoulder as she speaks. {SPEAKS}", WALK, PARTY),
    "b5": ("A backyard party in uproar seen from above: smoke from the grill, a smashed cake, people shouting, and a small figure in a purple sequin dress walking out through the gate at the far end.", PUSH, PARTY),
    "b6": (f"Close on {HER.lower()}, in a purple sequin dress, on a dusky suburban sidewalk. She speaks to the lens, calm and warm. {SPEAKS}", PUSH, "Distant party noise, crickets."),
    "b7": ("Lawn sprinklers burst on all over a backyard party; guests shriek and run with their arms over their heads and the cake on the table gets soaked.", STATIC, "Sprinklers hissing, guests shrieking."),
    "b8": (f"Outside a wooden fence {HER.lower()}, in a purple sequin dress, clicks the gate shut behind her, perfectly dry, as sprinkler water spatters over the top of the fence. She smiles to herself.", STATIC, "Sprinklers hissing, muffled shrieks."),
    "d1": (f"At night {HER.lower()}, in a cropped purple leather jacket over a sequin dress, walks toward the camera under the streetlights, singing softly. {SINGS}", WALK, NIGHT),
    "d2": ("At night a man in a white vest leans out of a lit window shaking his fist and yelling at the street below, where a parked car's hazard lights flash orange.", STATIC, "A car alarm whooping, a man yelling."),
    "d3": ("A lit apartment window at night: behind the glass the silhouettes of a couple argue, arms waving, and a pot plant flies across between them.", STATIC, "Muffled shouting behind glass."),
    "d4": (f"At night a fire hydrant shoots a tall white geyser into the air and water floods across the street; {HER.lower()}, in a cropped purple leather jacket, steps neatly around the water toward the camera without looking at it.", STATIC, "Water gushing, splashing."),
    "f1": (f"At night in the middle of a wet street that is falling apart (a hydrant geyser, steam blasting from manholes, sparks raining from a broken streetlight, flyers whirling) {HER.lower()}, in a cropped purple leather jacket over a sequin dress, struts toward the camera leading a dance line of ordinary city people behind her. They all do the same sharp 1990s R&B routine in time with the beat: step-touch side to side on every beat, hips popping, arms snapping out and back. {SINGS}", WALK, "Hydrant gushing, steam hissing, sparks crackling, car alarms."),
    "f2": ("Low and close on a dance line of ordinary city people in a wet street at night: on the beat they all drop into a deep knee bend and fling both arms up over their heads, then spring back up, as a hydrant geyser and a shower of sparks erupt behind them.", "The camera rises from low to waist height, Crane up with small amplitude at medium speed.", "Hydrant gushing, sparks crackling, a crowd whooping."),
    "f3": (f"{HER}, in a cropped purple leather jacket, sings to the lens while over her shoulder the dance line behind her pops their shoulders on every beat, steam and flyers swirling through the street. The red neon sign above the shop always reads exactly DELI, four letters. {SINGS}", "The camera arcs slowly around her, Arc with small amplitude at slow speed.", "Steam hissing, sparks crackling."),
    "f4": ("At the end of a dance line in a wet street at night, a skinny grey-haired man in a striped bathrobe flails his arms the wrong way, hopelessly out of step, while the little pink piglet in a red harness at his feet trots side to side perfectly in time with the dancers.", HAND, "Steam hissing, a piglet squealing, the crowd laughing."),
    "f5": (f"{HER}, in a cropped purple leather jacket, throws one palm straight out toward the camera like a traffic cop on the beat, and the whole dance line behind her freezes mid-move. {SINGS}", STATIC, "Steam hissing, then a hush."),
    "f6": (f"{HER}, in a cropped purple leather jacket, strikes a final pose with one hand on her hip and her chin up, the whole dance line behind her snapping into a V with their arms thrown up at 00:02.800, and a huge burst of orange sparks fans out across the night sky behind them. {SINGS}", PUSH, "A burst of sparks, a cheer."),
    "o1": ("At night in an apartment hallway, a woman in a purple leather jacket looks down at a small pink piglet curled up fast asleep on her doormat in front of her purple door, and raises her eyebrows.", STATIC, "A quiet hallway, a piglet snoring softly."),
    "o2": (f"In a hallway at night {HER.lower()}, in a cropped purple leather jacket, looks into the lens and sings with a small shrug. {SINGS}", STATIC, "A quiet hallway, a piglet snoring softly."),
    "o3": ("Low on the hallway carpet, a small pink piglet in a red harness sleeps curled on a doormat in front of a closed purple door; its ear twitches and it snuggles deeper.", STATIC, "A piglet snoring softly, a door lock clicking."),
    "o4": (f"In a cozy living room at night {HER.lower()}, in a lavender silk robe and purple headwrap, curls up on a purple velvet sofa with a mug of tea and sings. {SINGS}", PUSH, HOME),
    "o5": ("A woman in a lavender silk robe stands at the window and pulls the two curtains hanging from the rod above it together with both hands, shutting out the red and blue flashing lights of the city outside.", STATIC, "Curtains swishing, a siren fading."),
    "o6": ("A woman in a lavender silk robe on a purple sofa reaches over and clicks off the table lamp at 00:02.500, and the room goes dark.", STATIC, "A lamp switch clicking."),
}


def prompt(sid, lyric):
    desc, cam, sound = M[sid]
    desc = desc.replace("{L}", f"<d>[English] {lyric}</d>")
    return ("For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\n"
            f"integrated_multimodal_description\n{STYLE} [Shot 1] {desc} {cam}\n\n"
            f"overall_soundscape\n{sound}\n\nnon_diegetic_music\nA confident, bouncy pop song with a female vocal.")


def submit(g):
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=json.dumps({"prompt": g}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{e.read().decode()[:600]}")


def take_path(sid, off):
    return f"out/{sid}.mp4" if not off else f"out/{sid}_r{off}.mp4"


def run(ids, off=0):
    os.makedirs("audio/shots", exist_ok=True); os.makedirs("prompts/shots", exist_ok=True)
    sp = spans()
    order = list(sp)
    for _, (sid, _a, snd, _set, lyric, _pic) in rows():
        if sid not in ids:
            continue
        if not os.path.exists(os.path.join(COMFY, "input", f"nmp_f_{sid}.png")):
            print("  no frame:", sid); continue
        secs = 5
        start = sp[sid][0]
        wav = f"audio/shots/{sid}.wav"
        n = frames_for(secs) / 24 + 0.4
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{n:.3f}",
                        "-i", MIX if snd == "mix" else INST, "-af", "apad", "-ac", "2", "-ar", "44100",
                        "-t", f"{n:.3f}", wav], check=True)
        shutil.copy(wav, os.path.join(COMFY, "input", f"nmp_{sid}.wav"))
        text = prompt(sid, lyric)
        open(f"prompts/shots/{sid}.txt", "w", encoding="utf-8").write(text + "\n")
        tag = f"nmp_{sid}" if not off else f"nmp_{sid}_r{off}"
        end = f"nmp_f_{END[sid]}.png" if sid in END else None
        g = build(text, tag, 1120, 640, secs, SEED0 + order.index(sid) + 1000 * off, 20, "beta",
                  audio=f"nmp_{sid}.wav", first_frame=f"nmp_f_{sid}.png", guide_end=end)
        submit(g)
        print(f"queued {tag:10s} {start:7.2f}s  {snd}  {frames_for(secs)} f" + (f"  end={END[sid]}" if end else ""))


def collect():
    n = 0
    for f in sorted(glob.glob(os.path.join(COMFY, "output", "video", "H3_nmp_*_0000?_.mp4")), key=os.path.getmtime):
        name = os.path.basename(f)[len("H3_nmp_"):-len("_00001_.mp4")]
        dst = os.path.join("out", name + ".mp4")
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(f):
            shutil.copy2(f, dst); n += 1
    print(f"collected {n} renders")


if __name__ == "__main__":
    args = sys.argv[1:]
    os.chdir(HERE)
    if args[:1] == ["--collect"]:
        collect(); sys.exit()
    off = 0
    if args[:1] == ["--seed"]:
        off, args = int(args[1]), args[2:]
    ids = args or [s[0] for _, s in rows() if not os.path.exists(take_path(s[0], 0))]
    run(ids, off)
