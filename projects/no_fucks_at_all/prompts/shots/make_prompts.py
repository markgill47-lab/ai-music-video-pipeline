"""Generate ref2v prompts for the music-video shots from shared subject blocks, so every
shot describes each character, set and prop with identical wording."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SINGER = ('<Subject {n}> is the singer in <Picture {n}>: a gangly older man with a long bony face, beaky hooked nose, '
          'jug ears, pale blue eyes, highly arched eyebrows, fire-engine red spiked hair and small round red-lensed wire '
          'glasses, in a boxy oversized purple suit with padded shoulders, a black-and-white checkerboard shirt buttoned '
          'to the neck, a hot pink and turquoise daisy-print tie and an office ID badge. <Picture {n}> is a character '
          'sheet showing <Subject {n}> full-length from several angles above close-ups of his face, the same single '
          'person throughout.')
GUIT = ('<Subject {n}> is the guitarist in <Picture {n}>: a tall thin man with long straight black hair and a curled '
        'waxed moustache, in a battered crimson top hat, a crimson tailcoat with gold braid, a black silk scarf and '
        'striped trousers. <Picture {n}> is a character sheet of <Subject {n}>, the same single person throughout.')
DRUM = ('<Subject {n}> is the drummer in <Picture {n}>: a punk woman with huge crimped 1980s hair split down the '
        'middle, jet black on her right side and bright red on her left, hot pink eyeshadow, silver hoops and a studded '
        'collar, in a leopard-print crop top and a red tartan vest. <Picture {n}> is a character sheet of '
        '<Subject {n}>, the same single person throughout.')
BAND = ('<Subject {n}> is the television studio band set in <Picture {n}>: a hand-painted cartoon city skyline '
        'backdrop in turquoise, hot pink and lemon yellow with a jagged lightning bolt and painted stars, a '
        'black-and-white checkerboard riser with a red drum kit and two small amplifiers, a fresnel lighting grid '
        'overhead, black drapes, and a studio camera on a pedestal.')
OFFICE = ('<Subject {n}> is the television studio office set in <Picture {n}>: canary yellow plywood walls with '
          'painted-on windows showing a turquoise sky and cartoon skyline, a fire-engine red desk, an oversized beige '
          'desk telephone, a stack of paper, a blue filing cabinet, a painted wall calendar and a potted plastic palm.')
WORD = ('<Subject {n}> is the gold word in <Picture {n}>: the word "FUCK" as a solid object, chunky rounded 1980s '
        'capital letters extruded in polished gold metal with bevelled edges, softly glowing, small enough to fit in '
        'the palm of a hand.')
CHEST = ('<Subject {n}> is the treasure chest in <Picture {n}>: a shoebox-sized wooden chest with dark varnished wood '
         'and polished brass bands, corners and hasp, warm golden light pouring up from inside when its curved lid is '
         'open.')
CERT = ('<Subject {n}> is the framed certificate in <Picture {n}>: cream parchment reading "CERTIFIED PROFESSIONAL" '
        'in large black lettering, with a red foil seal and ribbons, in an ornate gold frame behind glass.')
AUD = ('<Subject {n}> is the studio audience in <Picture {n}>: six ordinary people in bright everyday 1980s fashion, '
       'a woman with a big blonde perm in a neon pink sweatshirt, a moustached man in a red trucker cap and tan '
       'windbreaker, a young man with a hi-top fade in a purple colour-block windbreaker, an older woman with a silver '
       'bouffant in a lavender skirt suit, a teenage boy in a salmon polo with a sweater over his shoulders, and a '
       'woman with a black bob in an electric-blue blazer.')
STUDIO = ('<Subject {n}> is the television studio in <Picture {n}>: walls hung with huge hot pink, tangerine orange and '
          'turquoise curtains, a fresnel lighting grid, wooden audience bleachers and vintage pedestal cameras.')

R_SINGER = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - his face, red spiked hair, red-lensed glasses, '
            'purple suit, checkerboard shirt and daisy tie are retained exactly as in <Picture {n}>.')
R_GUIT = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - his face, black hair, moustache, crimson top hat and '
          'tailcoat are retained exactly as in <Picture {n}>.')
R_DRUM = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - her face, split black and red crimped hair, makeup '
          'and punk outfit are retained exactly as in <Picture {n}>.')
R_BAND = ('<Subject {n}> (appears in [Shot 1]): attribute_transfer - the painted skyline backdrop, checkerboard riser, '
          'red drum kit, amplifiers and lighting grid are carried into the target video.')
R_OFFICE = ('<Subject {n}> (appears in [Shot 1]): attribute_transfer - the yellow walls, painted windows, red desk, '
            'beige telephone and blue filing cabinet are carried into the target video.')
R_WORD = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - the gold letters spelling "FUCK", their chunky '
          'rounded shape and polished gold finish are retained exactly as in <Picture {n}>.')
R_CHEST = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - the wooden chest with brass bands and the golden '
           'light inside are retained exactly as in <Picture {n}>.')
R_CERT = ('<Subject {n}> (appears in [Shot 1]): fully_preserved - the gold frame, the lettering "CERTIFIED '
          'PROFESSIONAL" and the red seal are retained exactly as in <Picture {n}>.')
R_AUD = ("<Subject {n}> (appears in [Shot 1]): fully_preserved - each person's hair and bright 1980s outfit are "
         "retained as in <Picture {n}>.")
R_STUDIO = ('<Subject {n}> (appears in [Shot 1]): attribute_transfer - the bright curtains, lighting grid and wooden '
            'bleachers are carried into the target video.')

LOOK = ("Live-action, a 1980s public-access television music video, flat bright studio light, hugely saturated candy "
        "colours, 35mm film grain.")
SING_SND = ("The band plays loud in a small television studio, the singer's voice through the PA, the room's hard walls "
            "ringing slightly.")
INST = "A bouncy new-wave rock instrumental with a driving beat."


def build(name, subs, summary, shot, sound, music="N/A"):
    defs = "\n".join(s.format(n=i + 1) for i, (s, _) in enumerate(subs))
    ret = "\n".join(r.format(n=i + 1) for i, (_, r) in enumerate(subs))
    txt = (f"subject_definitions\n{defs}\n\nsummary\n[reference generation] {summary}\n\n"
           f"retention_analysis\n{ret}\n\ndetailed_description\n{LOOK}\n\n[Shot 1] {shot}\n\n"
           f"overall_soundscape\n{sound}\n\nnon_diegetic_music\n{music}\n")
    open(os.path.join(HERE, f"{name}.txt"), "w", encoding="utf-8").write(txt)
    print("wrote", name)



if __name__ == "__main__":
    build("shot4_office", [(SINGER, R_SINGER), (WORD, R_WORD), (CHEST, R_CHEST), (OFFICE, R_OFFICE)],
          "The target video shows <Subject 1> behind the red desk on <Subject 4>, singing to camera as he feeds gold "
          "words like <Subject 2> one by one into <Subject 3> and finally shuts the lid.",
          "A medium shot of <Subject 1> (S1) standing behind the red desk on <Subject 4>, framed from the waist up, "
          "<Subject 3> open on the desk in front of him with golden light pouring up out of it and lighting his face from "
          "below, several palm-sized gold words like <Subject 2> lying beside it. He sings to the camera throughout while "
          "he works, lips shaping every word, eyebrows lifting on the long notes. He (S1) sings <d>[English] So</d> "
          "At 00:01.900 he (S1) sings <d>[English] I tightened up my focus</d> and picks up one gold word, holding it up "
          "so the letters \"FUCK\" face the camera. At 00:03.800 he (S1) sings <d>[English] Locked it in a tiny box</d> "
          "and lowers it reverently into <Subject 3>, the glow flaring brighter. He picks up a second gold word, turns it "
          "admiringly in the light, and drops it in too. At 00:09.300 he (S1) sings <d>[English] Cause every fuck you give "
          "is one you'll never get back, friend</d> wagging a finger at the camera, then placing a third gold word inside. "
          "At 00:13.500 he (S1) sings <d>[English] Use them like they cost</d> and on the final word slams the lid of "
          "<Subject 3> shut, the golden light cut off, and gives the camera a smug, satisfied look. The camera is Static.",
          SING_SND)

    build("shot5a_band", [(SINGER, R_SINGER), (GUIT, R_GUIT), (DRUM, R_DRUM), (BAND, R_BAND)],
          "The target video shows <Subject 1> dancing wildly at the microphone on <Subject 4> as he belts the chorus, "
          "with <Subject 2> and <Subject 3> playing behind him.",
          "A medium shot of <Subject 1> (S1) at the chrome microphone stand on <Subject 4>, framed from the knees up, "
          "<Subject 2> strumming a white electric guitar behind him to the left and <Subject 3> pounding the red drum kit "
          "on the checkerboard riser behind him to the right. <Subject 1> dances in wild, rubbery, animated jerks to the "
          "beat, knees pumping, elbows flapping, shoulders snapping, grabbing the mic stand and swinging it, his red "
          "spikes bouncing. He (S1) sings <d>[English] Don't give a fuck!</d> thrusting a fist in the air. At 00:01.200 "
          "he (S1) sings <d>[English] It's a powerful skill</d> At 00:04.200 he (S1) sings <d>[English] Save them for the "
          "moments when the world stands still</d> freezing in a comic pose on \"still\". At 00:07.900 he (S1) sings "
          "<d>[English] Don't give a fuck!</d> and spins on his heel. The camera is Static.",
          SING_SND)

    build("shot5b_band", [(SINGER, R_SINGER), (GUIT, R_GUIT), (DRUM, R_DRUM), (BAND, R_BAND)],
          "The target video shows <Subject 1> dancing and singing at the microphone on <Subject 4> from a low side "
          "angle, <Subject 2> and <Subject 3> playing around him.",
          "A low-angle medium shot from the left side of the stage on <Subject 4>, looking up at <Subject 1> (S1) at the "
          "chrome microphone, framed from the waist up, <Subject 2> at the edge of frame in the foreground strumming his "
          "white guitar, <Subject 3> behind on the riser pounding the drums, the fresnel grid blazing above. <Subject 1> "
          "dances in jerky, rubbery moves, hips wagging, eyes rolled heavenward. At 00:00.400 he (S1) sings "
          "<d>[English] It's a sacred art from the very bottom of your carefree heart</d> clutching his chest with both "
          "hands on \"heart\" and swooning backwards. The camera is Static.",
          SING_SND)

    build("shot6_audience", [(AUD, R_AUD), (STUDIO, R_STUDIO)],
          "The target video shows the studio audience from <Subject 1> sitting on the wooden bleachers of <Subject 2>, "
          "clapping along to the band.",
          "A reverse angle from the stage looking back at the wooden bleachers of <Subject 2>, a medium-wide shot of the "
          "people from <Subject 1> sitting scattered across the benches in their bright 1980s outfits, facing the camera, "
          "the bright curtains and a pedestal camera behind them. They clap along on the beat with big grins, heads "
          "bobbing, the blonde perm woman bouncing in her seat, the man in the red cap clapping over his head, the older "
          "woman clapping primly with her handbag on her knees. The camera Pans slowly to the right across the bleachers.",
          "The audience clapping in time, a few whoops, the band playing loud in the room.", INST)

    build("shot7_certificate", [(SINGER, R_SINGER), (CERT, R_CERT), (OFFICE, R_OFFICE)],
          "The target video shows <Subject 1> on <Subject 3> dropping into an office chair with <Subject 2>, singing "
          "about it, then tossing it away.",
          "A medium shot on <Subject 3>. <Subject 1> (S1) flops down into a swivel office chair behind the red desk, "
          "holding <Subject 2> up proudly beside his face with both hands so the lettering \"CERTIFIED PROFESSIONAL\" "
          "faces the camera. At 00:00.100 he (S1) sings <d>[English] I'm a certified professional, not giving a fuck "
          "engineer</d> with a smug, heavy-lidded look over the top of his red glasses. On the final word he tosses the "
          "framed certificate nonchalantly over his shoulder without looking, and it clatters away out of frame behind him "
          "while he leans back in the chair and puts his feet up on the desk. The camera is Static.",
          SING_SND)
