"""The shot list as data: one row per shot, boundaries snapped to the beat grid.

  python shots.py          # print the table and check every shot fits a 5 s render
  python shots.py --md     # rewrite the "## Shots" section of SHOTLIST.md

Each row: (id, start in seconds, sound, set, lyric, picture). A shot runs from its start to the
next shot's start; starts are snapped to the nearest detected beat (0 and the song end stay put).
Sound: "mix" pins the full song (she sings on screen), "inst" pins the instrumental stem
(nobody's mouth moves).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = json.load(open(os.path.join(HERE, "audio", "beats_full.json")))["beats"]
# librosa finds the first beat at 7.85 s; the whispered intro has the same pulse, so extend the grid back
STEP = 0.4875
BEATS = [round(RAW[0] - STEP * k, 3) for k in range(16, 0, -1)] + RAW
SONG_END = 241.28
LAST_BEAT = 239.166

SECTIONS = [
    ("Intro — sunrise, her building (trench)", [
        ("i01", 0.0, "inst", "skyline", "", "Sunrise behind the apartment block, the whole city lit orange. Slow push."),
        ("i02", 4.4, "inst", "window", "Chaos on the rise", "A window: a man in pyjamas smashes his ringing alarm clock with a shoe."),
        ("i03", 8.3, "inst", "window", "But it's not mine", "Another window: a woman flaps a tea towel at a smoking toaster and a shrieking smoke alarm."),
        ("i04", 11.7, "mix", "hallway", "Never was. Never will be.", "Her purple door opens; she steps out in the trench, coffee cup in hand, and whispers to the lens."),
        ("i05", 16.6, "inst", "hallway", "", "Low at floor level: the pig in its red harness trots past her purple boots, leash trailing."),
        ("i06", 21.0, "inst", "hallway", "", "The green door bursts open: the owner in his striped bathrobe charges past her after the pig, shouting."),
        ("i07", 24.9, "inst", "stoop", "", "She comes out onto the stoop into the sun; the garbage truck pulls away and a man in a bath towel chases it, hauling a huge bag of garbage."),
        ("i08", 28.8, "inst", "stoop", "", "Close: she slides the purple sunglasses down off her curls onto her nose, on the beat."),
    ]),
    ("Verse 1 — the morning sidewalk", [
        ("v1a", 33.6, "mix", "sidewalk", "There's a man on the sidewalk wrestling with a cone", "Walk-and-sing toward the lens, camera backing away; behind her a man fights an umbrella blown inside out."),
        ("v1b", 37.5, "inst", "sidewalk", "", "The umbrella man, closer: it flips inside out again and wraps over his head."),
        ("v1c", 39.4, "mix", "sidewalk", "Someone arguing with shadows on a megaphone", "She sings past a man in a suit screaming into his phone on speaker, red in the face."),
        ("v1d", 43.3, "inst", "sidewalk", "Drowning in a thimble of stress", "A commuter's coffee lid pops; the whole cup goes down his white shirt. He freezes, mouth open."),
        ("v1e", 45.2, "mix", "sidewalk", "Strolling through the madness like it's none of my mess", "She strolls, sips her coffee, sings, untouched by all of it."),
    ]),
    ("Pre-chorus — the coffee shop", [
        ("p1a", 48.2, "inst", "coffee", "Drama's got teeth, it'll bite if you stare", "A customer jabs a finger at the barista over a wrong order, demanding the manager."),
        ("p1b", 51.1, "mix", "coffee", "It'll brand your heart with somebody else's care", "The customer turns to her for backup; she sings to the lens with a sweet, blank smile."),
        ("p1c", 55.0, "mix", "coffee", "But I learned a magic phrase", "She picks up her cup from the pickup counter and sings as she turns to leave."),
        ("p1d", 59.4, "mix", "sidewalk", "Not my circus… not my monkey. Tattooed on my calm.", "A canvasser shoves a clipboard at her; she smiles, sings, and side-steps without breaking stride."),
    ]),
    ("Chorus 1 — rush hour", [
        ("c1a", 63.5, "mix", "gridlock", "Not my circus, not my monkey", "She walks between the gridlocked cars singing, every driver leaning on the horn."),
        ("c1b", 67.4, "inst", "gridlock", "Spin your wheels", "A car's back wheel spins in a slush puddle, spraying a wall of dirty water."),
        ("c1c", 69.0, "mix", "stoop", "Not my fire, not my barn — burn it down, I'll still be calm", "A fire alarm has emptied a building: residents in robes and curlers on the pavement; she sings through them."),
        ("c1d", 72.9, "inst", "stoop", "Your chaos isn't mine to wrangle", "The culprit in a robe holds up a blackened, smoking toaster to the crowd."),
        ("c1e", 74.8, "inst", "sidewalk", "Your knots aren't mine to untangle", "A dog walker spins in place, trussed up in six leashes and six dogs."),
        ("c1f", 76.7, "mix", "sidewalk", "Not my storm… not my sky. Not my reason why.", "A sudden downpour, everyone scattering; she pops open a purple umbrella and sings."),
    ]),
    ("Instrumental — to the office", [
        ("k1", 80.4, "inst", "sidewalk", "", "Under the purple umbrella she walks on; the pig trots out from a doorway and follows at her heels."),
        ("k2", 84.3, "inst", "sidewalk", "", "The owner, soaked, robe flapping, runs after the pig, slips and goes down in a puddle."),
        ("k3", 88.2, "inst", "tower", "", "She steps into the revolving door of the office tower in her trench."),
        ("k4", 92.1, "inst", "office", "", "She steps out into the office in the purple power suit and cat-eye glasses, as if nothing happened."),
    ]),
    ("Verse 2 — the office (power suit)", [
        ("v2a", 95.2, "mix", "desk", "Someone knocks on my door with a crisis bouquet", "At her desk; a coworker leans over the cubicle wall clutching a fistful of sticky notes. She sings."),
        ("v2b", 99.1, "inst", "office", "Dropping wilted little problems", "Down the corridor: the coworker walks off dropping sticky notes like petals, a trail behind him."),
        ("v2c", 101.0, "mix", "desk", "I nod politely, then return their concern", "A queue at her desk: a jammed printer tray, a broken stapler. She nods, sings, slides each one back."),
        ("v2d", 104.9, "mix", "office", "Wrong department, sorry friend", "She points down the corridor with a pen and sings; the queue turns to look."),
        ("v2e", 108.8, "inst", "office", "Not my candle to burn", "The hanging sign over the far doorway: WRONG DEPARTMENT, with an arrow."),
    ]),
    ("Pre-chorus 2 — hooked", [
        ("q1", 110.1, "inst", "office", "Life's full of hooks", "Every coworker hunched over a phone, faces lit, thumbs scrolling, mouths open."),
        ("q2", 112.0, "mix", "office", "Trying hard to snag your mind — you bite once, you're stuck", "She walks down the corridor through the scrolling zombies, singing."),
        ("q3", 115.9, "inst", "office", "You get reeled in blind", "The pig tears down the corridor; coworkers leap onto their chairs screaming; the owner chases it through."),
        ("q4", 117.8, "mix", "desk", "But I sharpened up my boundaries", "Back at her desk she sings while the chaos runs past behind her."),
        ("q5", 121.7, "mix", "desk", "Not my pony… not my derby. That's my lucky farm.", "The wall clock hits five; she shuts her laptop on the beat, stands, sings."),
    ]),
    ("Chorus 2 — the supermarket (tracksuit)", [
        ("c2a", 125.0, "mix", "market", "Not my plan, not my plot", "Pushing a trolley down the aisle in the purple tracksuit, singing."),
        ("c2b", 128.9, "inst", "checkout", "Twist it, turn it, I care not", "A man pounds a self-checkout screen flashing UNEXPECTED ITEM IN BAGGING AREA."),
        ("c2c", 130.8, "mix", "checkout", "Not my hive, not my bees — buzz away", "Shoppers swarm the 50% OFF bin like bees; she strolls past singing."),
        ("c2d", 134.7, "inst", "market", "Your panic isn't mine to carry", "A panic-buyer behind a teetering tower of toilet roll holds a pack out to her; she pushes on."),
        ("c2e", 136.6, "inst", "market", "Your ghosts aren't mine to marry", "The pig sits in a trolley's child seat munching a lettuce, the owner sprinting up the aisle."),
        ("c2f", 138.5, "mix", "carpark", "Not my bridge… not my troll. Not my weary soul.", "The car park exit: a grumpy booth attendant won't lift the barrier; she ducks under it singing."),
    ]),
    ("Instrumental — evening", [
        ("k5", 142.2, "inst", "carpark", "", "Wipe: a delivery van crosses in front of her in the car park; when it clears she's in the sequin dress."),
        ("k6", 146.1, "inst", "suburb", "", "Golden hour: she walks up a suburban street to a party gate with balloons, a gift in her hand."),
        ("k7", 150.0, "inst", "party", "", "The party: the host flips burgers on a grill throwing flames, kids running, a balloon popping."),
        ("k8", 154.0, "inst", "party", "", "The pig has its face in the birthday cake; the owner dives across the table after it, plates flying."),
    ]),
    ("Bridge (spoken) — the party", [
        ("b1", 158.1, "mix", "party", "Look — people juggle flaming bowling pins", "She stands with a cup of punch and speaks to the lens; behind her the host juggles grill, baby and cake."),
        ("b2", 162.0, "inst", "party", "And hand you one like it's a compliment", "The host hands her a screaming baby with a huge proud smile."),
        ("b3", 165.9, "mix", "party", "But I've got better places to stand", "She holds the baby at arm's length, hands it straight back, speaking."),
        ("b4", 169.8, "mix", "party", "Far from their hands", "She walks away across the lawn toward the gate, speaking over her shoulder."),
        ("b5", 173.7, "inst", "party", "Far from their lands", "Wide: the party in uproar, and her small, walking out through the gate."),
        ("b6", 177.6, "mix", "suburb", "My mantra keeps me warm", "On the sidewalk outside, close, she says it to the lens, calm."),
        ("b7", 181.5, "inst", "party", "Not my parade… not my rainstorm", "The lawn sprinklers burst on; guests shriek and run, the cake gets soaked."),
        ("b8", 184.5, "inst", "suburb", "", "Outside the fence she clicks the gate shut, perfectly dry, as the spray spatters the other side."),
    ]),
    ("Breakdown — the walk home (jacket)", [
        ("d1", 186.9, "mix", "night", "Not my —", "Night. She walks home under the streetlights in the leather jacket over the dress, singing softly."),
        ("d2", 191.2, "inst", "night", "(Not my headache…)", "A car alarm wails; a man in a vest leans out of a window shaking his fist at it."),
        ("d3", 195.1, "inst", "night", "(Not my fallout… not my sandcastle)", "A lit window: a couple argue, a pot plant flies past the glass."),
        ("d4", 199.0, "inst", "night", "(Not my tide.)", "A fire hydrant bursts into a geyser; she steps neatly around the flood without looking."),
    ]),
    ("Final chorus — the finale on her street (jacket)", [
        ("f1", 203.2, "mix", "night (chaos)", "Not my quest, not my dragon — slay it, chase it", "Her street falls apart (geyser, steam, sparks) and everyone she passed today dances in a line behind her as she struts toward the lens."),
        ("f2", 207.1, "inst", "night (chaos)", "Not my cliff, not my leap", "Low and close: the line drops into a deep knee bend, arms flung up, the geyser erupting behind."),
        ("f3", 209.0, "mix", "night (chaos)", "Fall or fly, that's yours to keep — your circus isn't mine to enter", "Medium on her singing, the dancers popping their shoulders over her shoulder."),
        ("f4", 212.9, "inst", "night (chaos)", "Your whirlwind isn't my adventure", "The end of the line: the owner hopelessly out of step, the pig perfectly in step."),
        ("f5", 214.8, "mix", "night (chaos)", "Nope. Not my maze… not my rat.", "She throws up a palm like a traffic cop; the whole line freezes mid-move."),
        ("f6", 216.8, "mix", "night (chaos)", "And that's the end of that.", "Final pose, hand on hip, the line in a V behind her, a huge burst of sparks across the sky."),
    ]),
    ("Outro — home (robe)", [
        # o1 (pig asleep on the mat) dropped in v2: f6 runs on so its final pose and sparks land on the outro downbeat
        ("o2", 220.6, "mix", "hallway", "Take your metaphors home", "She sings it to the sleeping pig with a small shrug."),
        ("o3", 224.5, "inst", "hallway", "I've got none to tame", "She steps inside and closes her purple door on the pig, still asleep on the mat."),
        ("o4", 228.4, "mix", "living", "But my own.", "In the silk robe and headwrap she sinks into the purple sofa with tea and sings the last line."),
        ("o5", 232.3, "inst", "living", "", "She draws the curtains on the city's flashing lights and sirens."),
        ("o6", 236.2, "inst", "living", "", "She reaches over and clicks off the lamp. Black on the last beat."),
    ]),
]


def snap(s):
    return s if s == 0.0 else min(BEATS, key=lambda b: abs(b - s))


def rows():
    for title, shots in SECTIONS:
        for s in shots:
            yield title, s


def spans():
    """id -> (start, end) in seconds, snapped; the last shot ends on the last beat."""
    flat = [s for _, s in rows()]
    out = {}
    for i, s in enumerate(flat):
        end = snap(flat[i + 1][1]) if i + 1 < len(flat) else LAST_BEAT
        out[s[0]] = (snap(s[1]), end)
    return out


def clock(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def markdown():
    sp, out = spans(), []
    for title, shots in SECTIONS:
        out += [f"### {title}", "", "| Shot | Time | Len | Sound | Set | Lyric | Picture |", "|---|---|---|---|---|---|---|"]
        for sid, _a, snd, place, lyric, pic in shots:
            a, b = sp[sid]
            out.append(f"| {sid} | {clock(a)} | {b - a:.1f} | {snd} | {place} | {lyric} | {pic} |")
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    sp = spans()
    for sid, (a, b) in sp.items():
        assert 0.8 < b - a <= 5.0, f"{sid}: {b - a:.2f} s"
    print(f"{len(sp)} shots, {sum(s[2] == 'mix' for _, s in rows())} sung, longest {max(b - a for a, b in sp.values()):.2f} s")
    if "--md" in sys.argv:
        path = os.path.join(HERE, "SHOTLIST.md")
        text = open(path, encoding="utf-8").read()
        head = text[:text.index("## Shots")]
        intro = ("## Shots\n\nGenerated from `shots.py` (`python shots.py --md`). Len is seconds on screen; every "
                 "shot is a 5 s render trimmed to its slot.\n\n")
        open(path, "w", encoding="utf-8").write(head + intro + markdown())
        print("rewrote the Shots section of SHOTLIST.md")
    else:
        print(markdown())
