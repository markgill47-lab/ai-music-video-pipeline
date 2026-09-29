# No Fucks at All — shot list (full song)

123 BPM, beat = 0.487 s. Every boundary below sits on a detected beat. H3 renders
5–15 s per clip (max 362 frames ≈ 15.08 s), so anything longer is split into renders
that can also be alternate angles cut together on the beat.

Studio layout (stage left to stage right, as seen from the audience):
**bedroom set | band set (never changes) | office set**. Bright curtains on the back
wall, vintage pedestal cameras, lighting grid, bleachers with a few audience members.

| # | Time | Dur | Lyric | Set | Picture |
|---|---|---|---|---|---|
| 1 | 0:00.00–0:14.68 | 14.7 s | intro (instrumental) | whole studio | Establishing. Wide on the studio: bedroom set, band set, office set side by side; curtains, cameras, lighting rigs, a few people in the bleachers. Camera trucks slowly across the studio toward the band as they start playing. |
| 2 | 0:14.68–0:28.82 | 14.1 s | "I used to worry about everything I'm not / Till I learned a secret trick that the universe forgot" (vox from 0:16.8) | band | Zoom from the band to a close-up of the singer by the first line. |
| 3a | 0:28.82–0:38.08 | 9.3 s | "A guy screaming at a parking cone / I saw a lady losing sleep over her phone" | bedroom | Hard wipe in. Drummer and guitarist side by side in bed, each on a phone, angrily scrolling and yelling at it. |
| 3b | 0:38.08–0:47.35 | 9.3 s | "And I thought, wow, what a magical curse / To hand your precious fucks out / To the whole damn universe" | bedroom | Same scene, second angle (e.g. closer two-shot, or over-the-shoulder onto the phones). |
| 4 | 0:47.35–1:02.44 | 15.1 s | "So I tightened up my focus / Locked it in a tiny box / Cause every fuck you give is one you'll never get back, friend / Use them like they cost" | office | Swipe to office. Singer at the desk **singing** (full mix pinned), feeding palm-sized gold words into the glowing chest; slams the lid on "cost". |
| 5a | 1:02.44–1:11.70 | 9.3 s | "DON'T GIVE A FUCK! / It's a powerful skill / Save them for the moments when the world stands still / Don't give a fuck!" | band | Cut back to the band on the shout. Medium shot, singer dancing, wild and animated. |
| 5b | 1:11.70–1:18.04 | 6.3 s | "It's a sacred art from the very bottom of your carefree heart" | band | Same performance, low side angle; clutches his heart and swoons on "heart". |
| 6 | 1:18.04–1:21.92 | 3.9 s | "The purer that you spend, the lighter you appear" | bleachers | Reverse angle on the audience clapping along (instrumental pinned; render 5 s, trim). Audience may vary a little clip to clip. Candidate spot for a guy in a gorilla suit. |
| 7 | 1:21.92–1:26.80 | 4.9 s | "I'm a certified professional, not giving a fuck engineer" | office | Singer flops into a chair holding a framed certificate, sings the line, holds a beat past "engineer" and tosses it over his shoulder (render 5 s, trim). |

Verse 2 starts 1:27.2 ("The boss was yelling nonsense…"): the office set again.

## Decisions (2026-09-27)

1. **Vignette audio: instrumental.** Pin `no_vocals.wav` slices for vignettes so nobody
   lip-syncs; the full mix goes back on in the edit. Band shots pin the full mix.
2. **Costumes: band costumes throughout,** vignettes included.
3. **The "fuck" object: gold extruded 3D word "FUCK",** built as a prop image and given
   to H3 as a reference picture. Fallback: glowing orbs / composite in post.
4. **Transitions in the edit** (wipes, swipes, whip-pans); renders stay clean.

## B-roll (no lip sync)

- **Audience:** six 80s regulars. Seated in the bleachers early; later they leave the
  bleachers and dance a choreographed routine during the longer instrumental stretches.
- **Spaceship exterior (later):** a cheap hand-made model hanging in a big black
  enclosure on an obvious string.

## Assets needed

- [x] Establishing wide `refs/set/studio_wide_final.png` (Krea layout → Flux sets+band → hue-fix headboard → Flux audience, composited)
- [x] Audience lineup `refs/audience/audience_lineup_master.png` (six people; the preppy teen is missing from the wide)
- [x] Bedroom set plate `refs/set/set_s4_bedroom_*` (office = `refs/set/set_s3_office_*`, band = `refs/set/set_s1_bandstage_00002_.png`)
- [x] Treasure chest `refs/props/prop_chest_*` + gold word `refs/props/prop_gold_word_*` (video-tested: `out/goldword_test.mp4`)
- [x] First frames: shot 3 `refs/frames/frame3_master.png` (bedroom; Flux read "phones" as corded handsets), shot 4 `refs/frames/frame4_master.png` (office, palm-sized gold words)

## Render status

- [x] Shot 1 `out/shot1_establish.mp4` (i2v from `studio_wide_final.png`, 362 f, intro pinned, seed 900)
- [x] Shot 2 `out/shot2_zoom.mp4` (ref2v, 4 sheets + band master + full mix pinned, 345 f, seed 901; lip sync r=0.33 p=0.001)
- [x] 3a `out/shot3a_bedroom.mp4` (ref2v + frame3 master + instrumental, 226 f, seed 902)
- [x] 3b `out/shot3b_bedroom.mp4` (ref2v, low two-shot, instrumental, 226 f, seed 903; brief two-handsets glitch)
- [x] 4 `out/shot4_office.mp4` (ref2v + frame4 master + full mix, 362 f, seed 904; lip sync r=0.54 p=0.001 on a face crop)
- [x] 5a `out/shot5a_band.mp4` (ref2v, 226 f, seed 905; r=0.46 p=0.001)
- [x] 5b `out/shot5b_band.mp4` (ref2v, side angle, 158 f, seed 906; r=0.41 p=0.001)
- [x] 6 `out/shot6_audience.mp4` (ref2v lineup + studio, instrumental, 124 f, seed 907; all six present)
- [x] 7 `out/shot7_certificate.mp4` (ref2v, 124 f, seed 908; lip sync unproven on 5 s, r=0.19 p=0.7; check by eye)

Rough cuts: `out/rough_cut_v2.mp4` (shots 1–7, 0:00–1:26.8); v1 (shots 1–3b trimmed to their beat slots, song laid over; built by the inline assembly in this session, `out/edit/`).

## Act 2 (1:26.8–4:01.7) — all rendered, assembled in `out/rough_cut_v3.mp4`

Specs, render lengths, pinned stems and refs live in `queue_act2.py`; prompts are generated by
`prompts/shots/make_prompts_act2.py`; the edit list is `assemble_full.py`. Review grids: `frames/act2/`.

| # | Time | Picture | Notes |
|---|---|---|---|
| 8a | 1:26.8–1:35.5 | Boss (guitarist in power suit) storms in, flings papers, singer catches | new ref `refs/act2/gsuit_combo.png` (Flux edit of his sheet) |
| 8b | 1:35.5–1:40.9 | "filed it away… nope, not now" papers into the wastebasket | |
| 8c | 1:40.9–1:50.1 | Singer dances from the office across the studio floor to the band stage by "love" | tracking shot |
| 9 | 1:50.1–2:05.6 | Drummer pelts the TV politician / guitarist pelts the grooms, intercut every 8 beats | instrumental; 9a skips 1.2 s where H3 opened on the chest ref |
| 10a/b | 2:05.6–2:19.7 | Band chorus, wide push-in then close-up | |
| 11 | 2:19.7–2:31.2 | Both, sad with empty boxes, intercut every 6 beats | instrumental |
| 12a | 2:31.2–2:36.0 | String-hung model ship drifts in, bobbing | |
| 12b | 2:36.0–2:44.2 | Cardboard bridge, camera arcs around the crew + robot | |
| 12c/d | 2:44.2–3:04.5 | Robot: apathy mode / load shedding / recalibrating / zero zero zero / yes captain | 12c re-rendered with a 12d frame pinned (v1 lost the set) |
| 12e | 3:04.5–3:07.1 | Captain: "No fucks at all" | |
| 13a | 3:07.1–3:21.0 | Band build-up and chorus, points out at the audience | |
| 13b | 3:21.0–3:25.3 | Audience leaps off the bleachers and rushes the stage; grooms and gorilla join | |
| 13c | 3:25.3–3:37.7 | Everyone in a line with the singer, dancing | v2 (kick line); still modest from a wide static angle |
| 14 | 3:37.7–3:49.2 | Finale: everyone on stage / ECU singer, alternating on "Save your fucks / They're rare / Spend with flair" | "all" pieces picked from two takes around sheet-montage stretches |
| end | 3:49.2–4:01.7 | Studio wide, crowd dancing, cardboard robot walks across the floor | from `refs/act2/end_frame_master.png` |

## Pickups (rough cut v4, `out/rough_cut_v4.mp4`)

- **Opening:** establishing truck split by three crew inserts (crew ref `refs/act2/crew_lineup_00002_.png`):
  0–3.9 establishing · 3.9–7.8 stagehand + electrician carry a zigzag flat · 7.8–9.8 electrician aims a fresnel
  from a ladder · 9.8–11.7 floor manager counts the band in · 11.7–14.7 back to the establishing push.
- **13c dance line:** replaced by two closer moving takes intercut every 6 beats, song-aligned for lip sync:
  A2 trucks right along the line (both ends pinned to crops of the wide take), B is a low angle trucking left.
