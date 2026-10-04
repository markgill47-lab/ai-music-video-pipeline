# Not my Pig, Not my Farm — shot list

Song by karnivore23, 4:01, 126 BPM (lyrics in `audio/lyrics.txt`, word timings in `audio/whisper_words.json`).

## Treatment (approved 2026-10-02)

*One bad day — for everyone else.* One day in her life, sunrise to bedtime. The whole city has the worst day of
its life over ordinary annoyances, and she strolls through all of it singing, completely unbothered. Every lyric
is a metaphor for daily stress, so the pictures are everyday irritations, not the literal images. She is the only
purple thing in every frame; her costume changes with the time of day.

**The pig:** a neighbour's escaped pet mini-pig turns up all day (hallway, street, office, supermarket, party) with
its frantic owner in a striped bathrobe always one step behind. It ends asleep on her doormat as she closes the door.

**Look:** glossy late-1990s R&B/hip-hop video: saturated colour, crisp light, wide lenses, walk-toward-camera.

## Cast and references (`refs/`)

| | Source | H3/Flux reference |
|---|---|---|
| Singer face | Krea `a3` (picked from 16 candidates) → Flux hair to brunette (`k1`) → 8 Flux views | `cast/singer_face_sheet.png` |
| Costumes | Krea trench sheet from the face; suit, tracksuit, sequin dress, dress + leather jacket, robe as Flux edits of the trench sheet | `cast/singer_<look>_combo.png` |
| The pig | Krea 3-view sheet | `cast/pig_sheet.png` |
| The owner | Krea face → Flux views; Krea bathrobe sheet | `cast/owner_combo.png` |
| Sets | 19 Krea plates (`make_sets.py`), kept free of purple; the sign is its own Krea plate | `sets/<name>.png` |

## Tooling

`shots.py` (data) → `frames.py build` (Flux first frames; each place has a master frame of her, and every other
angle there is made from that master) → `queue_shots.py` (H3 fl2va, 5 s, mix/instrumental pinned) →
`review_shots.py` → `assemble.py` (+ `takes.py`).

## Status (2026-10-04): finished, released as `not-my-pig-v1.0`

- Final: `out/not_my_pig_v4_2x.mp4` (2240x1280, SeedVR2 2x + small-face fix). Edit: `out/rough_cut_v4.mp4`.
  Videos are gitignored and published as release assets.
- Four cuts: v1 first pass (70/71 renders kept); v2 the user's notes (props from reference sheets, the street finale
  with the dance line, Krea signs); v3 transitions; v4 contact errors spotted on the 2x cut. The takes used are in
  `takes.py`; every frame's history is in the passes at the end of `frames.py`.
- Lessons: `docs/FINDINGS.md` §15. To change a shot: edit its spec at the end of `frames.py`, `python frames.py build
  --seed N id` (delete `frames/id.png` and ComfyUI `input/nmp_f_id.png` first), `python queue_shots.py --seed N id`,
  point `takes.py` at the new take, `python assemble.py out/rough_cut_vN.mp4`, then `sh upscale_run.sh` after renaming
  the cut in it (only changed shots re-upscale).

## Shots

Generated from `shots.py` (`python shots.py --md`). Len is seconds on screen; every shot is a 5 s render trimmed to its slot.

### Intro — sunrise, her building (trench)

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| i01 | 0:00.0 | 4.4 | inst | skyline |  | Sunrise behind the apartment block, the whole city lit orange. Slow push. |
| i02 | 0:04.4 | 3.9 | inst | window | Chaos on the rise | A window: a man in pyjamas smashes his ringing alarm clock with a shoe. |
| i03 | 0:08.3 | 3.4 | inst | window | But it's not mine | Another window: a woman flaps a tea towel at a smoking toaster and a shrieking smoke alarm. |
| i04 | 0:11.7 | 4.8 | mix | hallway | Never was. Never will be. | Her purple door opens; she steps out in the trench, coffee cup in hand, and whispers to the lens. |
| i05 | 0:16.5 | 4.3 | inst | hallway |  | Low at floor level: the pig in its red harness trots past her purple boots, leash trailing. |
| i06 | 0:20.8 | 4.3 | inst | hallway |  | The green door bursts open: the owner in his striped bathrobe charges past her after the pig, shouting. |
| i07 | 0:25.1 | 3.8 | inst | stoop |  | She comes out onto the stoop into the sun; the garbage truck pulls away and a man in a bath towel chases it, hauling a huge bag of garbage. |
| i08 | 0:29.0 | 4.8 | inst | stoop |  | Close: she slides the purple sunglasses down off her curls onto her nose, on the beat. |

### Verse 1 — the morning sidewalk

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| v1a | 0:33.8 | 3.8 | mix | sidewalk | There's a man on the sidewalk wrestling with a cone | Walk-and-sing toward the lens, camera backing away; behind her a man fights an umbrella blown inside out. |
| v1b | 0:37.6 | 1.9 | inst | sidewalk |  | The umbrella man, closer: it flips inside out again and wraps over his head. |
| v1c | 0:39.5 | 3.8 | mix | sidewalk | Someone arguing with shadows on a megaphone | She sings past a man in a suit screaming into his phone on speaker, red in the face. |
| v1d | 0:43.4 | 1.9 | inst | sidewalk | Drowning in a thimble of stress | A commuter's coffee lid pops; the whole cup goes down his white shirt. He freezes, mouth open. |
| v1e | 0:45.3 | 2.9 | mix | sidewalk | Strolling through the madness like it's none of my mess | She strolls, sips her coffee, sings, untouched by all of it. |

### Pre-chorus — the coffee shop

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| p1a | 0:48.2 | 2.8 | inst | coffee | Drama's got teeth, it'll bite if you stare | A customer jabs a finger at the barista over a wrong order, demanding the manager. |
| p1b | 0:51.0 | 3.9 | mix | coffee | It'll brand your heart with somebody else's care | The customer turns to her for backup; she sings to the lens with a sweet, blank smile. |
| p1c | 0:54.9 | 4.3 | mix | coffee | But I learned a magic phrase | She picks up her cup from the pickup counter and sings as she turns to leave. |
| p1d | 0:59.2 | 4.3 | mix | sidewalk | Not my circus… not my monkey. Tattooed on my calm. | A canvasser shoves a clipboard at her; she smiles, sings, and side-steps without breaking stride. |

### Chorus 1 — rush hour

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| c1a | 1:03.5 | 3.9 | mix | gridlock | Not my circus, not my monkey | She walks between the gridlocked cars singing, every driver leaning on the horn. |
| c1b | 1:07.4 | 1.5 | inst | gridlock | Spin your wheels | A car's back wheel spins in a slush puddle, spraying a wall of dirty water. |
| c1c | 1:08.8 | 4.3 | mix | stoop | Not my fire, not my barn — burn it down, I'll still be calm | A fire alarm has emptied a building: residents in robes and curlers on the pavement; she sings through them. |
| c1d | 1:13.1 | 1.4 | inst | stoop | Your chaos isn't mine to wrangle | The culprit in a robe holds up a blackened, smoking toaster to the crowd. |
| c1e | 1:14.6 | 1.9 | inst | sidewalk | Your knots aren't mine to untangle | A dog walker spins in place, trussed up in six leashes and six dogs. |
| c1f | 1:16.5 | 3.9 | mix | sidewalk | Not my storm… not my sky. Not my reason why. | A sudden downpour, everyone scattering; she pops open a purple umbrella and sings. |

### Instrumental — to the office

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| k1 | 1:20.4 | 3.8 | inst | sidewalk |  | Under the purple umbrella she walks on; the pig trots out from a doorway and follows at her heels. |
| k2 | 1:24.2 | 3.9 | inst | sidewalk |  | The owner, soaked, robe flapping, runs after the pig, slips and goes down in a puddle. |
| k3 | 1:28.0 | 4.3 | inst | tower |  | She steps into the revolving door of the office tower in her trench. |
| k4 | 1:32.3 | 2.9 | inst | office |  | She steps out into the office in the purple power suit and cat-eye glasses, as if nothing happened. |

### Verse 2 — the office (power suit)

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| v2a | 1:35.2 | 3.8 | mix | desk | Someone knocks on my door with a crisis bouquet | At her desk; a coworker leans over the cubicle wall clutching a fistful of sticky notes. She sings. |
| v2b | 1:39.0 | 1.9 | inst | office | Dropping wilted little problems | Down the corridor: the coworker walks off dropping sticky notes like petals, a trail behind him. |
| v2c | 1:40.9 | 3.9 | mix | desk | I nod politely, then return their concern | A queue at her desk: a jammed printer tray, a broken stapler. She nods, sings, slides each one back. |
| v2d | 1:44.8 | 3.8 | mix | office | Wrong department, sorry friend | She points down the corridor with a pen and sings; the queue turns to look. |
| v2e | 1:48.6 | 1.5 | inst | office | Not my candle to burn | The hanging sign over the far doorway: WRONG DEPARTMENT, with an arrow. |

### Pre-chorus 2 — hooked

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| q1 | 1:50.1 | 1.9 | inst | office | Life's full of hooks | Every coworker hunched over a phone, faces lit, thumbs scrolling, mouths open. |
| q2 | 1:52.0 | 3.8 | mix | office | Trying hard to snag your mind — you bite once, you're stuck | She walks down the corridor through the scrolling zombies, singing. |
| q3 | 1:55.8 | 1.9 | inst | office | You get reeled in blind | The pig tears down the corridor; coworkers leap onto their chairs screaming; the owner chases it through. |
| q4 | 1:57.7 | 3.8 | mix | desk | But I sharpened up my boundaries | Back at her desk she sings while the chaos runs past behind her. |
| q5 | 2:01.6 | 3.4 | mix | desk | Not my pony… not my derby. That's my lucky farm. | The wall clock hits five; she shuts her laptop on the beat, stands, sings. |

### Chorus 2 — the supermarket (tracksuit)

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| c2a | 2:05.0 | 3.8 | mix | market | Not my plan, not my plot | Pushing a trolley down the aisle in the purple tracksuit, singing. |
| c2b | 2:08.8 | 1.9 | inst | checkout | Twist it, turn it, I care not | A man pounds a self-checkout screen flashing UNEXPECTED ITEM IN BAGGING AREA. |
| c2c | 2:10.7 | 3.9 | mix | checkout | Not my hive, not my bees — buzz away | Shoppers swarm the 50% OFF bin like bees; she strolls past singing. |
| c2d | 2:14.6 | 1.9 | inst | market | Your panic isn't mine to carry | A panic-buyer behind a teetering tower of toilet roll holds a pack out to her; she pushes on. |
| c2e | 2:16.5 | 1.9 | inst | market | Your ghosts aren't mine to marry | The pig sits in a trolley's child seat munching a lettuce, the owner sprinting up the aisle. |
| c2f | 2:18.4 | 3.8 | mix | carpark | Not my bridge… not my troll. Not my weary soul. | The car park exit: a grumpy booth attendant won't lift the barrier; she ducks under it singing. |

### Instrumental — evening

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| k5 | 2:22.2 | 3.9 | inst | carpark |  | Wipe: a delivery van crosses in front of her in the car park; when it clears she's in the sequin dress. |
| k6 | 2:26.1 | 3.8 | inst | suburb |  | Golden hour: she walks up a suburban street to a party gate with balloons, a gift in her hand. |
| k7 | 2:29.9 | 4.3 | inst | party |  | The party: the host flips burgers on a grill throwing flames, kids running, a balloon popping. |
| k8 | 2:34.2 | 3.8 | inst | party |  | The pig has its face in the birthday cake; the owner dives across the table after it, plates flying. |

### Bridge (spoken) — the party

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| b1 | 2:38.1 | 3.8 | mix | party | Look — people juggle flaming bowling pins | She stands with a cup of punch and speaks to the lens; behind her the host juggles grill, baby and cake. |
| b2 | 2:41.9 | 3.9 | inst | party | And hand you one like it's a compliment | The host hands her a screaming baby with a huge proud smile. |
| b3 | 2:45.8 | 3.8 | mix | party | But I've got better places to stand | She holds the baby at arm's length, hands it straight back, speaking. |
| b4 | 2:49.6 | 4.3 | mix | party | Far from their hands | She walks away across the lawn toward the gate, speaking over her shoulder. |
| b5 | 2:53.9 | 3.9 | inst | party | Far from their lands | Wide: the party in uproar, and her small, walking out through the gate. |
| b6 | 2:57.8 | 3.8 | mix | suburb | My mantra keeps me warm | On the sidewalk outside, close, she says it to the lens, calm. |
| b7 | 3:01.6 | 2.9 | inst | party | Not my parade… not my rainstorm | The lawn sprinklers burst on; guests shriek and run, the cake gets soaked. |
| b8 | 3:04.5 | 2.4 | inst | suburb |  | Outside the fence she clicks the gate shut, perfectly dry, as the spray spatters the other side. |

### Breakdown — the walk home (jacket)

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| d1 | 3:06.9 | 4.3 | mix | night | Not my — | Night. She walks home under the streetlights in the leather jacket over the dress, singing softly. |
| d2 | 3:11.2 | 3.8 | inst | night | (Not my headache…) | A car alarm wails; a man in a vest leans out of a window shaking his fist at it. |
| d3 | 3:15.0 | 3.9 | inst | night | (Not my fallout… not my sandcastle) | A lit window: a couple argue, a pot plant flies past the glass. |
| d4 | 3:18.9 | 4.3 | inst | night | (Not my tide.) | A fire hydrant bursts into a geyser; she steps neatly around the flood without looking. |

### Final chorus — the finale on her street (jacket)

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| f1 | 3:23.2 | 3.9 | mix | night (chaos) | Not my quest, not my dragon — slay it, chase it | Her street falls apart (geyser, steam, sparks) and everyone she passed today dances in a line behind her as she struts toward the lens. |
| f2 | 3:27.0 | 1.9 | inst | night (chaos) | Not my cliff, not my leap | Low and close: the line drops into a deep knee bend, arms flung up, the geyser erupting behind. |
| f3 | 3:28.9 | 3.9 | mix | night (chaos) | Fall or fly, that's yours to keep — your circus isn't mine to enter | Medium on her singing, the dancers popping their shoulders over her shoulder. |
| f4 | 3:32.8 | 1.9 | inst | night (chaos) | Your whirlwind isn't my adventure | The end of the line: the owner hopelessly out of step, the pig perfectly in step. |
| f5 | 3:34.7 | 1.9 | mix | night (chaos) | Nope. Not my maze… not my rat. | She throws up a palm like a traffic cop; the whole line freezes mid-move. |
| f6 | 3:36.6 | 3.9 | mix | night (chaos) | And that's the end of that. | Final pose, hand on hip, the line in a V behind her, a huge burst of sparks across the sky. |

### Outro — home (robe)

| Shot | Time | Len | Sound | Set | Lyric | Picture |
|---|---|---|---|---|---|---|
| o2 | 3:40.5 | 3.8 | mix | hallway | Take your metaphors home | She sings it to the sleeping pig with a small shrug. |
| o3 | 3:44.3 | 4.3 | inst | hallway | I've got none to tame | She steps inside and closes her purple door on the pig, still asleep on the mat. |
| o4 | 3:48.6 | 3.8 | mix | living | But my own. | In the silk robe and headwrap she sinks into the purple sofa with tea and sings the last line. |
| o5 | 3:52.5 | 3.8 | inst | living |  | She draws the curtains on the city's flashing lights and sirens. |
| o6 | 3:56.3 | 2.9 | inst | living |  | She reaches over and clicks off the lamp. Black on the last beat. |
