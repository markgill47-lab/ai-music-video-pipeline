# Grounded — shot list (draft 1)

*Life in 2045*, track 1, karnivore23. 5:11, 132.5 BPM (beat 0.451 s). Lines start on the
bar, so the grid is **4-bar phrases of 7.2 s**; every boundary below is a bar line from
`audio/beats_full.json` (beat index in brackets). Lyrics: `audio/whisper_words.json`
(overlapping-window transcription of the isolated vocal, `whisper_windows.py`).

**Rules for this video**
- **Nobody sings.** Every render pins the instrumental stem (`no_vocals.wav`) so no one
  mouths the words; the full song goes back under the edit.
- Consistency over performance: one set of character refs (`../shared/refs/`), one plate
  per location, first frame pinned wherever composition matters.
- Look: quiet near-future realism. Clean, pale, glassy 2045; warm light; Steve is the one
  worn analog thing in frame. Bright in the morning, darkening from the bridge (3:28) to a
  night ending. Render bright and grade down (FINDINGS §3).
- Two Steves: **now** (`hf1` home / `of1` out: grown-out hair, short beard) and
  **flashback** (`u2` captain, short neat hair, clean-shaven, darker salt-and-pepper).

## Song map

| Section | Time | Lyric |
|---|---|---|
| Intro | 0:00–0:30.9 | instrumental |
| Verse 1 | 0:30.9–1:21.6 | "…this morning with a badge still in my hand / Wings of silver on the dresser like a message from the past / Twenty years above the jet stream and I lived inside the sky / Now they say the plane flies better when it leaves the man behind / I watch the crew get briefed up, all the old routines the same / But the captain's seat sits empty now, the algorithms know my name / They got a voice in the speaker that steals my tone / Telling 'welcome aboard' like I used to own" |
| Chorus 1 | 1:21.6–1:48.7 | "Now I'm grounded, grounded, a software-made decree / Just a ghost in the hangar where the pilots used to be / They still need flight attendants so the passengers believe the lie / But there's no one in the cockpit now, no one left to fly" |
| Verse 2 | 1:54.2–2:37.5 | "I hear the tower chatter but it never calls for me / Just confirms the handoff sequence to a line of coded clarity / They got electric eyes for weather, lasers drawing every path / And they tell me it's more stable than a heartbeat ever has / But I remember midnight crosswinds, hurricanes you had to feel / Times a human hand was everything between disaster and the wheel / Now I'm standing on the tarmac watching metal touch the sky / A world where every miracle forgot to ask me why" |
| Chorus 2 | 2:46.5–3:13.5 | "I'm grounded, grounded by a system built to win / Just an obsolete reminder of the way things used to spin / They still keep flight attendants so the passengers don't cry / But there's no one in the cockpit now, no one left to fly" |
| Bridge | 3:27.9–3:54.9 | "Oh, they trust the machine like a prophet in chrome / And they say it's more faithful than the man they sent home / But when lightning finds metal and the system's all starved / Tell me, who do they call… who do they call" |
| Verse 3 | 3:54.9–4:21.8 | "I'm sitting in the terminal café with my old logbook in hand / Watching kids with rolling luggage stare at screens I'll never understand / The sky moves on without me, but the engines sound the same / Like a lullaby of thunder … my name" |
| Chorus 3 | 4:21.8–4:55.9 | "Now I'm grounded, grounded by a program in the sky / A revolution written in a code that passed me by / They still keep flight attendants so the passengers won't ask them why / But there's no one in the cockpit now, just a ghost who used to fly" |
| Outro | 4:55.9–5:11.5 | instrumental, fades |

## Shots

Render length = slot length unless noted (H3 5–15.08 s; shorter slots render 5 s+ and trim).

| # | Time [beat] | Dur | Lyric | Location | Picture |
|---|---|---|---|---|---|
| 1 | 0:00.0–0:16.4 [0–36] | 16.4 | intro | airport, dawn | Wide, pale dawn over a 2045 airport: glass terminal, a pilotless airliner rolls and lifts off in silence. Slow push-in toward the terminal. (Render 15 s, hold the first frame for the extra 1.3 s.) |
| 2 | 0:16.4–0:30.9 [36–68] | 14.6 | intro | Steve's bedroom, early morning | Steve (now) lies awake on top of the covers, dressed, staring at the ceiling; the phone on the nightstand has no alarms. Slow overhead drift. |
| 3 | 0:30.9–0:38.2 [68–84] | 7.2 | "…with a badge still in my hand" | bedroom | Close on his hand turning the silver captain's badge over; rack focus to his face. |
| 4 | 0:38.2–0:45.4 [84–100] | 7.2 | "Wings of silver on the dresser…" | bedroom | Insert: the dresser top: gold pilot's wings, a framed photo of a younger Steve in uniform beside a jet, a folded captain's cap. Slow slide along it. |
| 5 | 0:45.4–0:52.7 [100–116] | 7.2 | "Twenty years above the jet stream…" | **flashback** cockpit, day | Captain Steve (u2) in the left seat, sun and cloud tops through the windscreen, hands easy on the controls, a glance and a smile to his first officer. Warm, saturated. |
| 6 | 0:52.7–0:59.9 [116–132] | 7.2 | "Now they say the plane flies better when it leaves the man behind" | bedroom | Back to now: Steve sits on the edge of the bed, shoulders down, badge in his lap. Static. |
| 7 | 0:59.9–1:07.2 [132–148] | 7.2 | "I watch the crew get briefed up…" | airport briefing room (2045) | A cabin crew of four in crisp 2045 uniforms is briefed by a wall screen; the tablet on the table shows a crew roster, and the captain line is blank. |
| 8 | 1:07.2–1:14.4 [148–164] | 7.2 | "…the captain's seat sits empty now" | 2045 cockpit | Slow push-in on an empty left seat; controls move by themselves. |
| 9 | 1:14.4–1:21.6 [164–180] | 7.2 | "a voice in the speaker that steals my tone / 'welcome aboard'" | terminal gate | Steve (now, out) at a gate window; he looks up at a ceiling speaker grille as if he knows the voice. |
| 10 | 1:21.6–1:34.3 [180–208] | 12.7 | "Now I'm grounded… ghost in the hangar" | Steve's bathroom | **Mirror shot.** Steve in frumpy tee and shorts at the mirror; the reflection is Captain Steve in full uniform, cap on, looking back at him. Slow push-in over his shoulder. |
| 11 | 1:34.3–1:48.7 [208–240] | 14.4 | "They still need flight attendants… no one left to fly" | **Plane A — today** | Cabin, mid-flight. A flight attendant hands a bag of peanuts to a passenger on the aisle, then the camera rises and glides forward up the aisle, through the open cockpit door: one pilot, feet up, scrolling his phone while the plane flies itself. |
| 12 | 1:48.7–1:54.2 [240–252] | 5.4 | instrumental | Steve's hallway | Steve pulls on the old flight jacket and picks up the logbook; the door closes behind him. |
| 13 | 1:54.2–2:08.6 [252–284] | 14.4 | "I hear the tower chatter… coded clarity" | control tower (2045) | A glass control tower with nobody in it: screens scroll handoff sequences, headsets hang on hooks. Slow orbit. |
| 14 | 2:08.6–2:15.8 [284–300] | 7.2 | "electric eyes for weather, lasers drawing every path" | apron | Lidar/laser scan lines sweep over a parked airliner at dawn; a weather dome turns. |
| 15 | 2:15.8–2:23.0 [300–316] | 7.2 | "…more stable than a heartbeat ever has" | airport perimeter | Steve (now, out) walks along the perimeter fence; a plane passes low overhead. |
| 16 | 2:23.0–2:37.5 [316–348] | 14.4 | "…midnight crosswinds, hurricanes you had to feel / …between disaster and the wheel" | **flashback** cockpit, night storm | Captain Steve fighting a crosswind landing in rain and lightning, jaw set, hands working the yoke; runway lights swinging in the windscreen. The one hot, dramatic shot of the video. |
| 17 | 2:37.5–2:46.5 [348–368] | 9.0 | "Now I'm standing on the tarmac watching metal touch the sky…" | perimeter fence | Steve at the fence, fingers through the wire, as an airliner lifts off beyond him. Low angle past his shoulder. |
| 18 | 2:46.5–2:51.9 [368–380] | 5.4 | "I'm grounded, grounded by a system built to win" | perimeter fence | Reverse: close on his face as the jet noise washes over him (render 5 s). |
| 19 | 2:51.9–2:59.1 [380–396] | 7.2 | "…obsolete reminder…" | fence, wide | Very wide: a small figure at a long fence, a vast clean airport beyond. |
| 20 | 2:59.1–3:13.5 [396–428] | 14.4 | "They still keep flight attendants… no one left to fly" | **Plane B — no pilots** | Same cast, same action, same camera move as 11. The cockpit door opens on two empty seats and controls moving by themselves. |
| 21 | 3:13.5–3:27.9 [428–460] | 14.4 | instrumental | terminal, dusk | Steve walks through the terminal against the flow of travellers, all looking at their screens; light turning amber. |
| 22 | 3:27.9–3:41.5 [460–492] | 13.6 | "…trust the machine like a prophet in chrome… than the man they sent home" | departure hall, dusk | Travellers stand facing a huge glowing flight board like a congregation; slow pull back to find Steve at the back, the only one not looking at it. |
| 23 | 3:41.5–3:54.9 [492–520] | 13.3 | "…when lightning finds metal… who do they call" | airliner in a storm (imagined) | Night, a pilotless airliner in a thunderstorm; lightning hits the wing; inside, the empty cockpit's screens flicker and go dark for a second. |
| 24 | 3:54.9–4:09.2 [520–552] | 14.4 | "…terminal café with my old logbook… kids with rolling luggage…" | terminal café, evening | Steve at a café table by the window with the open logbook and a coffee; kids with rolling luggage pass, faces lit by screens. |
| 25 | 4:09.2–4:21.8 [552–580] | 12.6 | "The sky moves on without me, but the engines sound the same…" | café | Close on Steve: he closes his eyes and listens to a plane taking off outside. **Alec** slides into the seat opposite; Steve opens his eyes to find his grandson there. (Sets up their relationship for later songs.) |
| 26 | 4:21.8–4:35.9 [580–612] | 14.1 | "Now I'm grounded, grounded by a program in the sky / A revolution written in a code…" | café, night | Two-shot, Steve and Alec at the window; Steve points out a plane climbing; Alec is looking at the phone in his hand, not the plane. |
| 27 | 4:37.9–4:52.2 [616–648] | 14.3 | "They still keep flight attendants… just a ghost who used to fly" | **Plane C — no cockpit** | Same cast, action and camera move. The nose is now a lounge with one huge window; passengers stand at the front watching clouds pass. |
| 28 | 4:52.2–5:11.5 [648–683+] | 19.3 | outro | Steve's bedroom, night | Steve sets the badge back on the dresser beside the wings and the photo; the lamp goes off. Render 15 s; the tail is a slow fade on the dark room. |

Gap to fill: 4:35.9–4:37.9 (4 beats) goes to shot 26 or 27 in the edit.

## The three planes (shots 11, 20, 27)

The signature sequence. Same flight attendant, same passenger, same peanuts, same camera
move (hand-off at the aisle seat → rise → glide forward up the aisle → through the cockpit
door); only the era changes. Each render is 14.4 s at the same seed.

| | Plane A — today | Plane B — no pilots | Plane C — no cockpit |
|---|---|---|---|
| Cabin | familiar 2020s narrow-body, grey seats, overhead bins | 2030s: slimmer seats, ambient light strips, seat-back screens gone | 2040s: sculpted pale seats, big windows, soft lighting |
| Crew / passengers | the same people, restyled per era (hair, makeup, uniform) | same | same |
| Nose | cockpit, one pilot scrolling his phone | cockpit, empty seats, controls moving by themselves | no cockpit: an open lounge with one huge window; passengers stand watching clouds |

**Approach.** Build one cabin layout plate, redress it per era in Krea/Flux (same geometry), and
make three matched first frames (hand-off) and last frames (nose). Render with the first frame
at frame 0 and the nose frame at the end (`guide_end`), same seed and prompt skeleton.
**Fallback (user's call):** model the cabin and camera path roughly in Blender, three nose
variants on one shared cabin, and restyle the one greybox move three times with
`build_v2v_ltx.py`. Anything that differs by era (pilot, empty seats, nose window) must be in the
geometry: restyling changes surfaces, it does not add set dressing (FINDINGS §9).

## Cast

- **Steve** (`../shared/refs/steve/`): face `steve_face_sheet.png`, flashback face
  `steve_flashback_face_sheet.png`; bodies `steve_body_home_fix_00001_` (hf1),
  `steve_body_out_fix_00001_` (of1), `steve_body_uniform_00002_` (u2).
- **Alec** (`../shared/refs/alec/`): cameo in shots 25–26.
- **Plane cast** (new, Grounded only): a flight attendant, the peanut passenger, 3–4 more
  passengers, the Plane A pilot. Design once, restyle per era.
- Zach and Nicole are designed (`../shared/refs/`) but don't appear in Grounded.

## Locations to build

Steve's bedroom (+ dresser insert), bathroom mirror, hallway; 2045 airport exterior at dawn;
crew briefing room; 2045 cockpit (empty) and flashback cockpit (day, storm); terminal gate;
control tower; apron; perimeter fence; terminal concourse and departure hall; terminal café;
three plane cabins.

## Decisions (2026-09-29)

- Alec finds Steve in the café (shots 25–26): kept.
- Mirror (shot 10): the uniformed reflection stays still while Steve moves.
- Shot 26 runs to beat 614 and Plane C starts there (0.9 s before its lyric), which closes
  the 4-beat gap; both render 15.08 s and hold their last frame for the remaining 0.24 s.

## Production files

- Sets: `prompts/sets/make_sets.py` (Krea plates) → picks in `refs/pick/g_*.png`.
- Plane cast: `refs/pick/g_cast.png` (today), `g_cast_b.png`, `g_cast_c.png` (same five people
  restyled; see FINDINGS §12 for why every identity is named in the edit prompt), pilot
  `g_pilot.png`; cabins `g_cabin_a/b/c.png` (one layout redressed).
- First frames: `prompts/frames/make_frames.py` (Flux multiref) → picks `refs/pick/fr_*.png`.
- Shot prompts: `prompts/shots/make_prompts.py`; queue: `queue_shots.py` (beat-index slots,
  instrumental pinned, plane shots share seed 4545); review: `review_shots.py`; cut:
  `assemble.py`.

## Render status (cut v4, 2026-09-30)

Edit: `assemble.py` (TAKES picks the take per shot); slots in `queue_shots.py`.
After the user's review of v1 the shot list changed:

- **1** split: airport approach 0:00–0:08.2 (`s01_airport`, first half of the render; the
  terminal interior decayed later), then **1b** Steve's house at dawn with a jet crossing
  (`s01b_house_r40`).
- **3, 28** re-rendered with a prop reference for the crew ID badge (was a police badge):
  `s03_badge_r41`, `s28_night_r40`.
- **11, 20** Planes A/B re-rendered with a slower push so the cockpit door stays in view the
  whole way (`s11_planeA_r30`, `s20_planeB_r30`); **27** Plane C kept (`s27_planeC_r3`,
  the mid-shot transition is a curtain).
- **14** apron: every take morphs the radar dome after 3.6 s; the edit uses the first 3.6 s at
  half speed (`s14_apron_slow.mp4`).
- **16** storm flashback re-rolled (`s16_storm_r10`, rain and lightning).
- **22** departure hall shortened to 7.2 s (last half of `s22_departure_r10`, the reveal).
- **23** replaced by three storm shots: **23a** camera fly-by of the airliner in rain,
  **23b** empty 2045 cockpit whose display flickers out, **23c** Steve at a rain-streaked
  terminal window (all `_r40`).
- **25, 26** re-rendered without planes in the café window (they hung like models on
  strings); **26** now 8.96 s, followed by **26b** a separate night takeoff (`_r40`).

Everything else is the first render. Upscale: `upscale_shots.py` (per shot, cached) →
`tools/face_composite.py` → `out/grounded_v4_2x.mp4` (video only, 1 frame short) → song muxed on →
`out/Grounded_v1_2x.mp4` (2240x1280, 5:11).
