"""Act 2 shot prompts (verse 2 to the end), sharing subject wording with make_prompts.py.

Timing notes: every <d> timestamp is relative to the shot's start, taken from the
word-level Whisper pass over the isolated vocal (audio/whisper_86_242.json).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_prompts import (build, SINGER, GUIT, DRUM, BAND, OFFICE, WORD, CHEST, AUD, STUDIO,
                          R_SINGER, R_GUIT, R_DRUM, R_BAND, R_OFFICE, R_WORD, R_CHEST, R_AUD, R_STUDIO,
                          SING_SND, INST)

GSUIT = ('<Subject {n}> is the guitarist dressed as a corporate boss in <Picture {n}>: a tall thin man with long black '
         'hair slicked straight back and a curled waxed moustache, in a charcoal grey pinstripe double-breasted power '
         'suit with huge padded shoulders, a white shirt and a fat red power tie. <Picture {n}> is a character sheet of '
         '<Subject {n}>, the same single person throughout.')
R_GSUIT = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - his face, slicked-back black hair, moustache, '
           'pinstripe power suit and red tie are retained exactly as in <Picture {n}>.')
LIVING = ('<Subject {n}> is the television studio living room set in <Picture {n}>: plywood walls painted as fake wood '
          'panelling with a crooked sailboat picture, a lumpy orange floral sofa, a shaggy green rug, a fringed floor lamp, '
          'and a big vintage CRT television on a spindly stand with a bulging bulbous glass screen, a wood-grain cabinet '
          'and tall rabbit-ear antennae, a grey-haired politician in a dark suit and red tie speaking at a podium on its '
          'glowing screen.')
R_LIVING = ('<Subject {n}> (appears in [Shot 1]): attribute_transfer - the wood-panel walls, floral sofa, green rug and '
            'the rabbit-eared CRT television showing the politician are carried into the target video.')
CHAPEL = ('<Subject {n}> is the television studio wedding chapel set in <Picture {n}>: two wobbly white pillars made of '
          'painted cardboard tubes either side of a small plywood altar with a lace cloth and plastic flowers, a plywood '
          'flat painted as a stained-glass window in hot pink, turquoise and yellow, a white paper aisle runner, folding '
          'chairs with white bows and paper wedding bells overhead.')
R_CHAPEL = ('<Subject {n}> (appears in [Shot 1]): attribute_transfer - the cardboard pillars, altar, painted stained-glass '
            'window, aisle runner and paper bells are carried into the target video.')
GROOMS = ('<Subject {n}> is the two grooms in <Picture {n}>: a tall broad man with a thick dark beard in a white tuxedo '
          'with a ruffled shirt and pink bow tie, and a shorter slim man with a blond feathered mullet in a powder-blue '
          'tuxedo with velvet lapels and a navy bow tie.')
R_GROOMS = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - both grooms\' faces, hair and tuxedos are retained '
            'exactly as in <Picture {n}>.')
BRIDGE = ('<Subject {n}> is the television studio starship bridge set in <Picture {n}>, built from cardboard and '
          'aluminium foil: a horseshoe of foil-covered cardboard consoles with bottle-cap buttons and Christmas-tree '
          'lights, a gold spray-painted thrift-store swivel armchair as the captain\'s chair, two cardboard helm stations, '
          'orange, red and silver foil walls, and a big black viewscreen with glitter stars and a painted planet.')
R_BRIDGE = ('<Subject {n}> (appears in [Shot 1]): attribute_transfer - the foil consoles, gold captain\'s chair, foil walls '
            'and starry viewscreen are carried into the target video.')
SHIP = ('<Subject {n}> is the model spaceship in <Picture {n}>: a cheap hand-made model with a saucer of two paper plates '
        'spray-painted silver, a cardboard-tube neck, a toilet-roll hull and two foil-wrapped tube engines, hanging on an '
        'obvious white string inside a black-painted box with painted stars.')
R_SHIP = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - the paper-plate saucer, cardboard tubes, foil engines '
          'and the visible string are retained exactly as in <Picture {n}>.')
ROBOT = ('<Subject {n}> is the robot in <Picture {n}>: a man in a homemade cardboard-box robot costume, a square box '
         'helmet with a red cellophane eye slot, a grille mouth and pipe-cleaner antennae, a silver box torso covered in '
         'bottle-cap dials, a tin-can speaker and Christmas-tree lights, dryer-vent hose arms and legs and box boots.')
R_ROBOT = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - the box helmet, red eye slot, antennae, silver dial-covered '
           'torso, hose limbs and box boots are retained exactly as in <Picture {n}>.')
GORILLA = ('<Subject {n}> is the gorilla in <Picture {n}>: a man in a cheap shaggy black gorilla costume with a rubbery '
           'grey mask, a small red bow tie and a party hat.')
R_GORILLA = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - the shaggy black gorilla suit, mask, red bow tie and '
             'party hat are retained exactly as in <Picture {n}>.')

ROBOT_SND = ("A flat, crackly robotic voice over the band, the hum and beeps of the cardboard consoles.")

if __name__ == "__main__":
    build("shot8a_boss", [(SINGER, R_SINGER), (GSUIT, R_GSUIT), (OFFICE, R_OFFICE)],
          "The target video shows <Subject 2> storming across <Subject 3> with a sheaf of papers and hurling them at "
          "<Subject 1>, who is lounging in the office chair and catches them.",
          "A reverse angle across <Subject 3>: in the right foreground <Subject 1> (S1) lounges in the swivel office "
          "chair behind the red desk with his feet up on it, the plywood backs of the set flats, fresnel lamps and a "
          "pedestal camera visible at the far side. <Subject 2> in his pinstripe power suit stomps angrily across the set "
          "toward the desk from the left background, red-faced, a thick sheaf of papers clutched in his fist, shouting "
          "silently and jabbing a finger. He reaches the desk and flings the papers at <Subject 1>, who swings his feet "
          "down and catches the whole sheaf against his chest without looking. At 00:07.400 he (S1) sings "
          "<d>[English] The boss was yelling nonsense</d> with a bored, heavy-lidded look. The camera is Static.",
          SING_SND)

    build("shot8b_nope", [(SINGER, R_SINGER), (GSUIT, R_GSUIT), (OFFICE, R_OFFICE)],
          "The target video shows <Subject 1> in the office chair on <Subject 3> singing as he drops the boss's papers "
          "into a wastepaper basket while <Subject 2> fumes.",
          "A medium shot of <Subject 1> (S1) sitting in the swivel office chair behind the red desk on <Subject 3>, "
          "holding the sheaf of papers, <Subject 2> in his pinstripe suit standing at the edge of the desk, fists on "
          "hips, fuming. A small tin wastepaper basket sits on the floor beside the chair. At 00:00.200 he (S1) sings "
          "<d>[English] So I filed it away</d> dangling the papers over the wastepaper basket. At 00:01.700 he (S1) "
          "sings <d>[English] Under nope, not now, not ever today</d> and lets the papers drop into the basket with a "
          "flourish, dusting off his hands, while <Subject 2> gapes in outrage. The camera is Static.",
          SING_SND)

    build("shot8c_dance", [(SINGER, R_SINGER), (OFFICE, R_OFFICE), (BAND, R_BAND), (DRUM, R_DRUM)],
          "The target video shows <Subject 1> springing up from the office desk on <Subject 2> and dancing across the "
          "studio floor to the band stage <Subject 3>, singing all the way, arriving at the microphone on the last word.",
          "A tracking shot across the television studio floor. <Subject 1> (S1) springs up out of the office chair on "
          "<Subject 2> and dances away across the grey concrete studio floor past pedestal cameras and cables, "
          "high-stepping, spinning, snapping his fingers and kicking his heels, heading for <Subject 3> where <Subject 4> "
          "is pounding the red drum kit on the checkerboard riser. He sings the whole way. At 00:00.250 he (S1) sings "
          "<d>[English] Traffic was a circus, but I floated above</d> At 00:04.100 he (S1) sings <d>[English] Cause "
          "giving zero fucks is a whole new kind of love</d> and leaps up onto the band stage, grabbing the chrome "
          "microphone stand on the word \"love\". The camera Tracks to the right with him at medium speed.",
          SING_SND)

    build("shot9a_tv", [(DRUM, R_DRUM), (CHEST, R_CHEST), (WORD, R_WORD), (LIVING, R_LIVING)],
          "The target video shows <Subject 1> on <Subject 4> yelling at the politician on the television and pelting "
          "the screen with gold words like <Subject 3> pulled from <Subject 2>.",
          "A medium-wide shot on <Subject 4>. The grey-haired politician drones on at his podium on the bulging screen of "
          "the rabbit-eared television. <Subject 1> stands beside the floral sofa in her full punk outfit, <Subject 2> "
          "open in the crook of one arm with golden light spilling out of it. She yells furiously at the television in "
          "silent pantomime, then digs into the chest, pulls out a palm-sized gold word like <Subject 3> spelling "
          "\"FUCK\", and hurls it at the screen, where it bounces off the curved glass. She throws another, and another, "
          "in a furious rhythm, her split black and red hair whipping, gold words clattering onto the green rug around "
          "the television. The camera is Static.",
          "Gold words clanking off the television glass, a politician's muffled droning from the TV speaker.", INST)

    build("shot9b_chapel", [(GUIT, R_GUIT), (GROOMS, R_GROOMS), (CHEST, R_CHEST), (WORD, R_WORD), (CHAPEL, R_CHAPEL)],
          "The target video shows <Subject 2> getting married between the pillars of <Subject 5> while <Subject 1> "
          "pelts them with gold words like <Subject 4> pulled from <Subject 3>, and they dodge.",
          "A medium-wide shot on <Subject 5>. Between the two cardboard pillars in front of the altar, the two grooms of "
          "<Subject 2> stand face to face holding hands, beaming at each other in their white and powder-blue tuxedos. "
          "<Subject 1> in his crimson top hat and tailcoat stands at the side of the aisle holding <Subject 3> open, "
          "golden light spilling out, scowling. He pulls out a palm-sized gold word like <Subject 4> spelling \"FUCK\" "
          "and lobs it at the grooms; they duck and it sails past. He throws another and another; the grooms bob, weave "
          "and sway out of the way together, still holding hands, never looking at him, gold words bouncing off the "
          "pillars and scattering down the aisle. The camera is Static.",
          "Gold words thudding against cardboard and clattering on the floor, a few soft organ notes.", INST)

    build("shot10a_chorus", [(SINGER, R_SINGER), (GUIT, R_GUIT), (DRUM, R_DRUM), (BAND, R_BAND)],
          "The target video shows <Subject 1>, <Subject 2> and <Subject 3> together on <Subject 4>, <Subject 1> belting "
          "the chorus.",
          "A wide frontal shot of the whole band on <Subject 4>: <Subject 1> (S1) front and centre at the chrome "
          "microphone, <Subject 2> at the left windmilling his white electric guitar, <Subject 3> pounding the red drum "
          "kit on the checkerboard riser. <Subject 1> belts with his whole body, one arm flung wide. At 00:00.200 he (S1) "
          "sings <d>[English] It's a cosmic truth</d> At 00:02.700 he (S1) sings <d>[English] A universal cheat code for "
          "eternal youth</d> At 00:06.600 he (S1) sings <d>[English] Don't give a fuck</d> and all three band members "
          "jump in unison. The camera Pushes in with small amplitude at slow speed.",
          SING_SND)

    build("shot10b_chorus", [(SINGER, R_SINGER), (GUIT, R_GUIT), (DRUM, R_DRUM), (BAND, R_BAND)],
          "The target video shows a close-up of <Subject 1> belting the chorus on <Subject 4>, <Subject 2> and "
          "<Subject 3> behind him.",
          "A close-up of <Subject 1> (S1) at the chrome microphone on <Subject 4>, face and shoulders filling the frame, "
          "red spikes, red-lensed glasses and purple lapels, <Subject 2> and <Subject 3> playing out of focus behind him. "
          "He belts with his eyes squeezed shut and veins standing out on his neck, then opens them wide at the camera. "
          "At 00:00.200 he (S1) sings <d>[English] Yeah, the freedom shows</d> At 00:02.700 he (S1) sings <d>[English] "
          "Let the pointless problems fight among themselves</d> waving a dismissive hand. The camera is Static.",
          SING_SND)

    build("shot11a_tv_sad", [(DRUM, R_DRUM), (CHEST, R_CHEST), (WORD, R_WORD), (LIVING, R_LIVING)],
          "The target video shows <Subject 1> on <Subject 4>, deflated, holding <Subject 2> which is now empty, gold "
          "words scattered uselessly around the television.",
          "A medium shot on <Subject 4>. The politician is still talking on the rabbit-eared television, unbothered. "
          "<Subject 1> stands slumped beside the floral sofa holding <Subject 2>, its lid open and its inside dark and "
          "empty, no light coming out. Spent gold words like <Subject 3> lie scattered on the green rug around the "
          "television. She tips the chest toward the camera, peers into it, shakes it upside down, and nothing falls out. "
          "Her shoulders sag, her lower lip trembles, and she looks up at the camera with big sad eyes. The camera is "
          "Static.",
          "The politician's muffled droning from the TV speaker, a sad little sigh.", INST)

    build("shot11b_chapel_sad", [(GUIT, R_GUIT), (GROOMS, R_GROOMS), (CHEST, R_CHEST), (WORD, R_WORD),
                                 (CHAPEL, R_CHAPEL)],
          "The target video shows <Subject 1> on <Subject 5>, dejected, looking into <Subject 3> which is now empty, "
          "while <Subject 2> happily finish their wedding behind him.",
          "A medium shot on <Subject 5>. <Subject 1> in his crimson top hat and tailcoat stands in the foreground holding "
          "<Subject 3>, its lid open and its inside dark and empty. Spent gold words like <Subject 4> lie scattered down "
          "the aisle behind him. He peers into the box, turns it upside down and shakes it, and nothing comes out. His "
          "moustache droops and he gazes mournfully at the camera. Behind him, between the cardboard pillars, the two "
          "grooms of <Subject 2> kiss and throw their arms up in celebration, paying him no attention. The camera is "
          "Static.",
          "Soft organ music, a few cheers, a sad little sigh.", INST)

    build("shot12a_ship", [(SHIP, R_SHIP)],
          "The target video shows <Subject 1> drifting toward the camera through its painted starfield, bobbing on its "
          "string.",
          "A close shot of <Subject 1> hanging in the black painted starfield, lit by one hard desk lamp from the side. "
          "It drifts slowly toward the camera, swaying and bouncing up and down on its visible white string in time to "
          "the driving beat, turning slightly, its foil engines glinting, until the paper-plate saucer nearly fills the "
          "frame. The camera Pushes in with small amplitude at slow speed.",
          "A hollow whooshing sound effect over the music.", INST)

    build("shot12b_bridge", [(SINGER, R_SINGER), (DRUM, R_DRUM), (GUIT, R_GUIT), (ROBOT, R_ROBOT), (BRIDGE, R_BRIDGE)],
          "The target video shows the crew on <Subject 5>: <Subject 1> in the captain's chair, <Subject 2>, <Subject 3> "
          "and <Subject 4> at the cardboard consoles.",
          "A wide shot of <Subject 5> in bright flat studio light. <Subject 1> sits in the gold captain's chair in the "
          "centre, legs crossed, bouncing his hand on the armrest in time to the music and nodding along. <Subject 2> and "
          "<Subject 3> sit at the two cardboard helm stations in front of him, jabbing bottle-cap buttons with great "
          "seriousness. <Subject 4> stands stiffly at a foil-covered console to one side, its Christmas-tree lights "
          "blinking. The glitter stars on the viewscreen behind them. The camera Arcs slowly around the bridge from left "
          "to right at slow speed, showing the whole cardboard set.",
          "Beeps and boops from the consoles over the music.")

    # v2: the slow arc dragged in the cut; same action with a fast, wide swing
    build("shot12b_bridge_v2", [(SINGER, R_SINGER), (DRUM, R_DRUM), (GUIT, R_GUIT), (ROBOT, R_ROBOT), (BRIDGE, R_BRIDGE)],
          "The target video shows the crew on <Subject 5>: <Subject 1> in the captain's chair, <Subject 2>, <Subject 3> "
          "and <Subject 4> at the cardboard consoles, seen in a fast sweeping camera move.",
          "A wide shot of <Subject 5> in bright flat studio light. <Subject 1> sits in the gold captain's chair in the "
          "centre, legs crossed, bouncing his hand on the armrest in time to the music and nodding along. <Subject 2> and "
          "<Subject 3> sit at the two cardboard helm stations in front of him, jabbing bottle-cap buttons with great "
          "seriousness. <Subject 4> stands stiffly at a foil-covered console to one side, its Christmas-tree lights "
          "blinking. The camera Arcs around the bridge from left to right with large amplitude at fast speed, whipping "
          "past the foil consoles and the starry viewscreen, sweeping a full half-circle around the captain's chair and "
          "settling on a front view of <Subject 1> and the crew by the end of the shot.",
          "Beeps and boops from the consoles over the music.")

    build("shot12c_robot", [(ROBOT, R_ROBOT), (SINGER, R_SINGER), (BRIDGE, R_BRIDGE)],
          "The target video shows <Subject 1> at its console on <Subject 3> announcing its new programming in a robotic "
          "voice while <Subject 2> watches from the captain's chair.",
          "A medium shot of <Subject 1> (S2) standing at a foil-covered console on <Subject 3>, <Subject 2> in the gold "
          "captain's chair in the background. The robot jerks to attention, its antennae wobbling, the red eye slot "
          "flickering and the Christmas-tree lights on its chest blinking with every syllable, its box head turning in "
          "stiff mechanical ticks. At 00:00.100 it (S2) says <d>[English] Bleep, blorp</d> At 00:01.700 it (S2) says "
          "<d>[English] Activate apathy mode</d> and jabs a big bottle-cap button. At 00:04.800 it (S2) says "
          "<d>[English] Initiate emotional load shedding protocol</d> pulling a cardboard lever with a dramatic yank. The "
          "camera is Static.",
          ROBOT_SND)

    build("shot12d_robot", [(ROBOT, R_ROBOT), (SINGER, R_SINGER), (BRIDGE, R_BRIDGE)],
          "The target video shows a closer shot of <Subject 1> recalibrating at its console on <Subject 3>, then turning "
          "and saluting <Subject 2>.",
          "A close shot of <Subject 1> (S2) at its console on <Subject 3>, the box helmet and dial-covered chest filling "
          "much of the frame, <Subject 2> small in the gold captain's chair behind. Its red eye slot flickers, its "
          "antennae spin, and its head whirls in a jerky circle as it recalibrates. At 00:02.300 it (S2) says "
          "<d>[English] Recalibrating</d> At 00:05.200 it (S2) says <d>[English] Zero, zero, zero</d> its chest lights "
          "going dark one by one. At 00:07.000 it turns stiffly toward <Subject 2> and snaps a salute with its oven-mitt "
          "hand, and it (S2) says <d>[English] Yes, captain, we give</d> The camera is Static.",
          ROBOT_SND)

    build("shot12e_captain", [(SINGER, R_SINGER), (BRIDGE, R_BRIDGE)],
          "The target video shows <Subject 1> in the gold captain's chair on <Subject 2> delivering the punchline.",
          "A medium close-up of <Subject 1> (S1) lounging in the gold captain's chair on <Subject 2>, the foil walls and "
          "starry viewscreen behind him. He leans toward the camera, peers over the top of his red glasses and, with "
          "grand captainly authority, (S1) sings <d>[English] No fucks at all</d> then leans back with a satisfied smirk. "
          "The camera Pushes in with small amplitude at slow speed.",
          SING_SND)

    build("shot13a_chorus", [(SINGER, R_SINGER), (GUIT, R_GUIT), (DRUM, R_DRUM), (BAND, R_BAND)],
          "The target video shows the band on <Subject 4> building up to the final chorus and <Subject 1> belting it.",
          "A medium-wide shot of the band on <Subject 4>. For the first six seconds the band builds up the intro: "
          "<Subject 3> hammers a drum roll, <Subject 2> strums big chords with his guitar held high, and <Subject 1> "
          "(S1) bounces on the spot at the chrome microphone, pumping a fist, winding up. At 00:06.400 he (S1) sings "
          "<d>[English] Don't give a fuck</d> leaping into the air. At 00:08.600 he (S1) sings <d>[English] It's a "
          "joyful sin</d> At 00:10.800 he (S1) sings <d>[English] A rebellious revolution you can dance within</d> "
          "swinging his hips and pointing out past the camera. The camera Pushes in with small amplitude at slow speed.",
          SING_SND)

    build("shot13b_rush", [(AUD, R_AUD), (GROOMS, R_GROOMS), (GORILLA, R_GORILLA), (STUDIO, R_STUDIO), (BAND, R_BAND)],
          "The target video shows the studio audience of <Subject 1>, <Subject 2> and <Subject 3> leaping up from the "
          "bleachers of <Subject 4> and running onto <Subject 5>.",
          "A wide shot across the studio of <Subject 4>. The people of <Subject 1> leap up off the wooden bleachers, "
          "waving their arms, and run excitedly across the concrete floor toward <Subject 5>, joined by the two grooms "
          "of <Subject 2> in their tuxedos and by <Subject 3> in his gorilla suit and party hat, who bounds along "
          "scratching his head. They hop up onto the band stage in a happy rush. The camera Pans to the right with them "
          "at medium speed.",
          "Cheering, whooping and running footsteps over the music.", INST)

    build("shot13c_line", [(SINGER, R_SINGER), (AUD, R_AUD), (GROOMS, R_GROOMS), (GORILLA, R_GORILLA),
                           (GUIT, R_GUIT), (DRUM, R_DRUM), (BAND, R_BAND)],
          "The target video shows <Subject 1> leading a chorus line of the people of <Subject 2>, the two grooms of "
          "<Subject 3> and <Subject 4> across the front of <Subject 7>, all dancing in unison while <Subject 5> and "
          "<Subject 6> play behind.",
          "A wide frontal shot of <Subject 7>. <Subject 1> (S1) stands in the middle of a long line along the front of "
          "the stage with the people of <Subject 2>, the two grooms of <Subject 3> and <Subject 4> in his gorilla suit, "
          "arms linked, all dancing in perfect unison: a step to the left, a step to the right, a high kick, a shimmy "
          "and a spin, repeating on the beat, <Subject 5> and <Subject 6> playing on the riser behind them. <Subject 1> "
          "sings into a handheld microphone as he dances. At 00:00.300 he (S1) sings <d>[English] Cause the world gets "
          "easier when there's nothing to spare</d> At 00:04.100 he (S1) sings <d>[English] Hold your precious fucks "
          "close</d> At 00:06.500 he (S1) sings <d>[English] Use them wisely, my friend</d> At 00:08.400 he (S1) sings "
          "<d>[English] Cause the ones you choose to give define you in the end</d> and the whole line throws their "
          "arms up together on \"end\". The camera is Static.",
          SING_SND)

    build("shot13c_line_v2", [(SINGER, R_SINGER), (AUD, R_AUD), (GROOMS, R_GROOMS), (GORILLA, R_GORILLA),
                           (GUIT, R_GUIT), (DRUM, R_DRUM), (BAND, R_BAND)],
          "The target video shows <Subject 1> leading a chorus line of the people of <Subject 2>, the two grooms of "
          "<Subject 3> and <Subject 4> across the front of <Subject 7>, all dancing in unison while <Subject 5> and "
          "<Subject 6> play behind.",
          "A wide frontal shot of <Subject 7>. <Subject 1> (S1) stands in the middle of a long line along the front of "
          "the stage with the people of <Subject 2>, the two grooms of <Subject 3> and <Subject 4> in his gorilla suit, "
          "arms linked over each other's shoulders, doing an exuberant high-energy chorus-line kick routine in perfect "
          "unison: every one of them kicks a leg high into the air on every beat, left, right, left, right, the whole "
          "line bouncing, swaying hard side to side together and throwing their heads back laughing, the gorilla kicking "
          "highest of all, the older woman's handbag swinging wildly, <Subject 5> and <Subject 6> playing on the riser behind them. <Subject 1> "
          "sings into a handheld microphone as he dances. At 00:00.300 he (S1) sings <d>[English] Cause the world gets "
          "easier when there's nothing to spare</d> At 00:04.100 he (S1) sings <d>[English] Hold your precious fucks "
          "close</d> At 00:06.500 he (S1) sings <d>[English] Use them wisely, my friend</d> At 00:08.400 he (S1) sings "
          "<d>[English] Cause the ones you choose to give define you in the end</d> and the whole line throws their "
          "arms up together on \"end\". The camera is Static.",
          SING_SND)

    build("shot14_all", [(SINGER, R_SINGER), (GUIT, R_GUIT), (DRUM, R_DRUM), (AUD, R_AUD), (GROOMS, R_GROOMS),
                         (GORILLA, R_GORILLA), (ROBOT, R_ROBOT), (BAND, R_BAND)],
          "The target video shows everyone together on <Subject 8> for the finale: the band, the people of <Subject 4>, "
          "the grooms of <Subject 5>, <Subject 6> and <Subject 7>, with <Subject 1> singing at the microphone.",
          "A wide frontal shot of <Subject 8> packed with everyone for the finale. <Subject 1> (S1) stands front and "
          "centre at the chrome microphone, <Subject 2> playing his white guitar at the left, <Subject 3> pounding the "
          "drums on the riser. Crowded around them the people of <Subject 4>, the two grooms of <Subject 5>, <Subject 6> "
          "in his gorilla suit and <Subject 7> in its cardboard robot costume all dance and sway with their arms in the "
          "air. At 00:02.300 he (S1) sings <d>[English] Save your fucks</d> At 00:06.500 he (S1) sings <d>[English] "
          "They're rare</d> At 00:09.900 he (S1) sings <d>[English] Spend with flair</d> and everyone throws their arms "
          "up. The camera is Static.",
          SING_SND)

    build("shot14_ecu", [(SINGER, R_SINGER), (BAND, R_BAND)],
          "The target video shows an extreme close-up of <Subject 1> singing the final lines on <Subject 2>.",
          "An extreme close-up of <Subject 1> (S1): his face fills the frame from the red spikes to the chin, the red "
          "lenses of his glasses glowing, the painted skyline a blur of colour behind him. He waits, eyebrows twitching, "
          "then leans into the lens. At 00:02.300 he (S1) sings <d>[English] Save your fucks</d> wagging a finger. At "
          "00:06.500 he (S1) sings <d>[English] They're rare</d> in a conspiratorial whisper-shout, eyes wide over the "
          "top of his glasses. At 00:09.900 he (S1) sings <d>[English] Spend with flair</d> with a huge crooked grin and "
          "a wink. The camera is Static.",
          SING_SND)

    build("shot14_end", [(ROBOT, R_ROBOT), (STUDIO, R_STUDIO)],
          "The target video shows the whole studio of <Subject 2> after the show, a crowd dancing around the band stage "
          "while <Subject 1> walks slowly across the floor.",
          "A high wide shot of the whole studio of <Subject 2> a happy crowd "
          "dances around the band stage with their arms in the air while the band plays out the song, the bright "
          "curtains and fresnel lights blazing. In the foreground, between the empty wooden bleachers and the stage, "
          "<Subject 1> walks slowly and stiffly across the concrete floor from left to right in its cardboard robot "
          "costume, box head swivelling to look at the camera once, antennae wobbling, and keeps walking. The camera is "
          "Static.",
          "The band playing out the song, the crowd cheering, the clunk of cardboard boots.", INST)
