"""Pickup shots: closer moving-camera dance line (13c) and studio-crew inserts for the
opening establishing shot. Dance takes are pinned to crops of the wide line take
(refs/act2/line_close_*.png) via AddGuide, so identities and stage come from there."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_prompts import build, SINGER, AUD, BAND, STUDIO, R_SINGER, R_AUD, R_BAND, R_STUDIO, SING_SND, INST
from make_prompts_act2 import GROOMS, GORILLA, R_GROOMS, R_GORILLA

CREW = ('<Subject {n}> is the studio crew in <Picture {n}>: a burly bearded stagehand in a red flannel shirt, a '
        'backwards grey cap, jeans and a leather tool belt; a wiry woman electrician with a curly brown perm and a '
        'yellow sweatband in blue denim overalls over a yellow T-shirt; and a skinny floor manager with a thin '
        'moustache and aviator glasses wearing a studio headset, a black STAFF T-shirt and khakis, carrying a clipboard.')
R_CREW = ("<Subject {n}> (appears in [Shot 1]): fully_preserved - each crew member's face, hair and work clothes are "
          "retained exactly as in <Picture {n}>.")

LINE = [(SINGER, R_SINGER), (AUD, R_AUD), (GROOMS, R_GROOMS), (GORILLA, R_GORILLA), (BAND, R_BAND)]
KICK = ("arms linked over each other's shoulders, doing an exuberant high-energy chorus-line kick routine in perfect "
        "unison: they kick a leg high on every beat, left, right, left, right, bouncing and swaying hard together, "
        "throwing their heads back laughing, hair flying, the older woman's handbag swinging")
LYRICS = ("<Subject 1> (S1) sings into a handheld microphone as he kicks. At 00:00.300 he (S1) sings <d>[English] Cause "
          "the world gets easier when there's nothing to spare</d> At 00:04.100 he (S1) sings <d>[English] Hold your "
          "precious fucks close</d> At 00:06.500 he (S1) sings <d>[English] Use them wisely, my friend</d> At 00:08.400 "
          "he (S1) sings <d>[English] Cause the ones you choose to give define you in the end</d> and everyone throws "
          "their arms up on \"end\".")

if __name__ == "__main__":
    build("shot13c_line_A", LINE,
          "The target video shows a moving medium shot travelling along the dancing line of <Subject 1>, the people of "
          "<Subject 2>, the grooms of <Subject 3> and <Subject 4> on <Subject 5>.",
          "A medium shot at waist height, close to the line of dancers at the front of <Subject 5>, starting on the "
          "woman with the blonde perm at the left end of the line. The dancers, " + KICK + ". The camera Tracks to the "
          "right along the line at medium speed, passing close by each dancer in turn: the moustached man in the red "
          "cap, the young man with the hi-top fade, the older woman in lavender, the teenage boy, then <Subject 1>, "
          "then the two grooms and finally <Subject 4> kicking wildly at the end. " + LYRICS,
          SING_SND)

    build("shot13c_line_B", LINE,
          "The target video shows a low moving shot of the kick line on <Subject 5>, from <Subject 4> at the right end "
          "back along the grooms and <Subject 1> to the people of <Subject 2>.",
          "A low-angle medium shot close to the front of <Subject 5>, looking up at the kick line, starting on the right "
          "end with <Subject 4> in his gorilla suit and party hat, the two grooms of <Subject 3> beside him and "
          "<Subject 1> beyond them. The dancers, " + KICK + ", legs kicking up toward the lens. The camera Tracks to "
          "the left along the line at medium speed with a slight upward tilt, the fresnel lights flaring behind their "
          "heads. " + LYRICS,
          SING_SND)

    crew = [(CREW, R_CREW), (STUDIO, R_STUDIO)]
    build("crew_flat", crew,
          "The target video shows the stagehand and the electrician from <Subject 1> carrying a painted set flat across "
          "the studio of <Subject 2> before the show.",
          "A medium-wide handheld shot on the concrete floor of the studio of <Subject 2>, the bright curtains and "
          "pedestal cameras behind. The burly stagehand and the woman electrician from <Subject 1> hurry across the "
          "frame from right to left carrying a tall plywood set flat between them, painted on the front with purple "
          "and yellow zigzags, raw plywood on the back, the stagehand walking backwards and waving her on, both "
          "hustling to beat the clock. The camera Pans to the left with them at medium speed.",
          "Footsteps, the scrape of plywood, a muffled shout of 'watch it', the band tuning up in the background.", INST)

    build("crew_light", crew,
          "The target video shows the electrician from <Subject 1> on a ladder aiming a studio light in <Subject 2>.",
          "A low-angle medium shot looking up at the woman electrician from <Subject 1> standing near the top of a "
          "wooden A-frame stepladder under the lighting grid of <Subject 2>, reaching up with gloved hands to swing a "
          "big fresnel lamp on its yoke and tighten the knob, the lamp's beam sweeping across the bright curtains "
          "behind her and flaring into the lens as it comes around. The camera Tilts up with small amplitude at slow "
          "speed.",
          "The squeak of a lamp yoke, a clank of metal, the band tuning up in the background.", INST)

    build("crew_countdown", crew,
          "The target video shows the floor manager from <Subject 1> counting the band in at the start of the show in "
          "<Subject 2>.",
          "A close shot of the floor manager from <Subject 1> in the foreground, facing the band stage with his back "
          "three-quarters to the camera, headset on, clipboard tucked under his arm, the band set blurred and glowing "
          "beyond him. He raises one hand high and counts down briskly on his fingers, three, two, one, then points "
          "sharply at the stage, and the stage lights blaze up behind him. The camera is Static.",
          "The floor manager whispering 'three, two, one', a burst of stage lights, the band kicking in.", INST)
