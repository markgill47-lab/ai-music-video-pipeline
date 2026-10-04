# MiniMax H3 in ComfyUI — working notes

Findings from a hands-on session testing MiniMax H3 video generation locally, with
Krea 2 and Flux 2 Klein feeding it reference images and start frames. Everything
below was measured on this machine, not taken from documentation, unless a source
is named.

Hardware: RTX 5090 (32 GB), 64 GB RAM, ComfyUI v0.31.1 at `D:\Projects_26\Comfyu\ComfyUI`.

---

## 1. Prompt structure

MiniMax ships prompt-writing guides **inside the model repo** — most people miss these:

- [`VIDEO_PROMPT_WRITING_GUIDE_base_en.md`](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md) — text-to-video and image-to-video
- [`VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md) — reference-to-video

**ComfyUI passes your prompt to the text encoder raw.** No system prompt, no chat
template (`comfy/text_encoders/minimax.py:181`). The tokenizer prepends only
`<Picture N>: ` plus vision tokens per image. So the field scaffolding is entirely
your responsibility — the model was trained on it and nothing else supplies it.

### ref2v — six fields, in order

```
subject_definitions      <Subject N> is ... in <Picture N>: [description]
summary                  [reference generation] one paragraph
retention_analysis       <Subject N> (appears in [Shot 1], [Shot 3]): fully_preserved - ...
detailed_description     shot by shot, 350-500 words
overall_soundscape       1-4 sentences, ambient only
non_diegetic_music       1-3 sentences, or N/A
```

Retention markers: `fully_preserved` | `partially_preserved` | `attribute_transfer` |
`weak_reference`. Use `fully_preserved` for characters, `attribute_transfer` for an
environment whose *look* you want carried into new framing.

`<Subject N>` and `<Picture N>` are different things. `<Picture N>` is a reference
image; `<Subject N>` is a reusable entity that a picture defines. Define subjects,
then refer to subjects.

### i2v — image-alignment line, then three core fields

```
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description
overall_soundscape
non_diegetic_music
```

**Do not reuse an i2v prompt in ref2v.** In i2v `<Picture 1>` is the start frame; in
ref2v it is the first reference image. We hit this — an i2v prompt run in ref2v told
the model to open on an empty room *and* that `<Picture 1>` was a character. It
survived only because the surrounding description was unambiguous.

### Syntax that works

| Element | Form |
|---|---|
| Shot cut | `[Shot 2] At 00:02.600, the camera cuts to ...` |
| Camera | motion + amplitude + speed: `Push with small amplitude at slow speed` |
| Motion types | Zoom, Push, Pan, Truck, Tilt, Pedestal, Arc, Tracking, Static, Shake, POV, Roll |
| Speaker | assign `(S1)`, `(S2)` once, in playback order |
| Dialogue | `She (S1) says <d>[English] Thirty seconds.</d>` |

Verified: four shots and two speakers inside 10.1 seconds, each line landing in its
own shot with clean ambient between. Cuts occur near the stated timestamps.
Timestamps are absolute — rescale them if you change duration.

---

## 2. Never write negations

**Naming an unwanted thing makes it more likely to appear.** The noun outweighs the
"no" in front of it.

Across five versions of one shot, every instruction that failed was phrased as an
exclusion:

| Written | Read as |
|---|---|
| "It does not point at her booth" | *point at her booth* |
| "Her booth receives no direct light" | *direct light* |
| "the floor carries no light" | *light on the floor* |
| "No frontal key, no fill" | *frontal key, fill* |

Removing every negation while changing nothing else produced the largest single-step
improvement in the series (frame 1 mean luma 43.1 → 38.8, near-black 50.2% → 56.2%).

**Rewrite rule:** describe only what is present; express absence as a property of what
is there.

- ~~"no window or doorway behind the booth"~~ → "behind the booth, unbroken riveted plating runs floor to ceiling"
- ~~"the floor carries no light and reads as solid black"~~ → "the floor reads as solid black"
- ~~"no people"~~ → describe an empty room and never mention people

Many negations are pure deletions — the adjacent positive sentence was already doing
the work. This contradicts the "short local negatives" advice in the CINEDANCE /
Higgsfield prompt system; that system is tuned for Seedance, not H3.

---

## 3. Lighting: the subject will not go dark

Seven interventions, all measured, none put a referenced character's face in shadow:

grade vocabulary · physical-fact lighting · six-field format · dim source behind ·
negation removal · blown-out door behind · dark reference sheet

What *did* respond: the environment. Across five prompt revisions the frame darkened
monotonically (mean luma 48.3 → 32.4, near-black 47.1% → 66.8%) while the subject
stayed keyed throughout.

### The actual mechanism

Silhouette is a **contrast ratio**, not a darkness setting. The one shot that
silhouetted had a blown-out doorway directly behind the subject:

| | mean | near-black | **bright (>200)** |
|---|---|---|---|
| silhouetted frame | 39.5 | 74.2% | **8.8%** |
| best "dark" prompt | 38.8 | 56.2% | **0.7%** |

Nearly identical mean luminance; 12× the bright pixels. Five prompt revisions had
driven `bright%` from 4.2% down to 0.7% — optimising in exactly the wrong direction.
Asking for a dark room and a silhouette at once is self-contradictory.

Related: **bright elements expand.** An open door described as a light source becomes
the room's key light and floods the interior. You cannot have a dark room and a bright
opening in the same shot.

### The answer is post

Grading works completely, and the source matters:

| | mean | near-black | bright |
|---|---|---|---|
| dark render, graded | **4.5** | 96.9% | 0.0% |
| bright render, graded | **34.2** | 77.2% | 8.0% |
| *(target: the silhouetted frame)* | *39.5* | *74.2%* | *8.8%* |

Same filter chain. The already-dark render becomes a black rectangle; the bright one
lands on the target. **Shoot bright, grade down** — the standard film argument, and
it means prompting for darkness is actively harmful to the grade.

`grade.sh <in> <out> [medium|heavy]` implements a low-key chain (S-curve, contrast,
cool shadows / warm highlights, vignette). 8-bit H.264 survived a hard grade without
banding, but `CreateVideo.bit_depth` defaults to **8** — raise it for headroom on
aggressive grades.

---

## 4. What references do and don't carry

**Identity and wardrobe transfer strongly.** A single 3-view turnaround sheet held
face and full costume across sitting, standing, walking, running, different rooms and
different lighting — poses that appear in none of the reference views. No LoRA, no
fine-tune, one image.

**Lighting and grade do not transfer.** A reference regenerated at mean 0.119 with 71%
near-black (vs the original's 0.331 and 0%) changed the output by ~2 luma points.
Consequence: light your character sheets flat. It costs nothing and preserves detail.

**Reference conditioning anchors what the model will invent.** Asking for a part of a
room the reference never showed means fighting the reference — a prominent doorway in
the plate reappeared in every re-angle despite instructions to look away from it.

**A 3-view turnaround reads as one character**, not three people. (We always included a
hedge line saying so; whether the hedge is load-bearing is untested.)

**No identity bleed** with two characters in one frame, given distinct
`subject_definitions` and per-subject `retention_analysis`.

### ref_image_size

`match` scales each reference to the generation's *pixel area*. `max` caps the short
edge at 2048 and **never upscales** — so for any source under 2048 short edge, `max`
is a pass-through at native resolution.

The setting is **global** — one value for all references. Control per-reference
resolution by choosing export sizes instead: `max` leaves a 768-short-edge plate at
768 while a 1256-short-edge character sheet passes through whole.

At 0.4 MP output, `match` shrank a 1024² sheet to ~640² before encoding. Use `max`.

---

## 5. r2v vs i2v — two use cases

| | i2v (first frame) | r2v (references) |
|---|---|---|
| Opening composition | exact — it *is* your frame | invented by the model |
| Identity in close-ups | degrades as camera pushes in | strong, from full-res sheets |
| Location across cuts | drifts | holds |
| Identity source | whatever survived in frame 0 | dedicated sheets |
| Weights | `fl2va` | `ref2va` |

**Build the first frame in Flux when the opening composition is the point.** Use an
empty-set plate plus multi-pose character sheets when the action matters more than the
exact frame — you get better identity, better location continuity, and cheaper renders.

Switching modes swaps a 19.5 GiB checkpoint, so batch experiments by mode.

---

## 6. Cost model

Render time tracked **output pixels**, essentially linearly. Reference tokens were
close to free.

| | resolution | references | duration | render |
|---|---|---|---|---|
| i2v | 1.0 MP | start frame only | 10.1 s | 21m28s |
| ref2v | 0.7 MP | 3 sheets at `max` (~16k tokens) | 10.1 s | 15m02s |

0.7 / 1.0 × 21m28s = 15m02s — almost exact, despite 16,000 extra reference tokens
riding every sampling step. Two runs across different modes isn't proof, but it's
enough to stop economising on reference resolution.

Rough guide at these settings: **~2.1 min of render per second of footage at 1.0 MP,
~1.5 min at 0.7 MP.**

Other settings: `beta` scheduler (the template's own note prefers it over `simple` for
reference-heavy prompts), 20 steps, `res_multistep` sampler. Trained frame range is
~124–362 frames (5–15 s); length snaps to a 17k+5 grid at 24 fps.

---

## 7. Scene and environment

**Prose cannot produce science fiction here.** Five separate attempts at "backwater
desert world" and "space bar" all rendered as Earth roadhouses. One Krea 2 plate — one
image — produced riveted bulkheads, exposed conduit, stencilled alien lettering,
viewport, airlock and twin moons immediately.

Character conditioning is far stronger than scene conditioning in this model. Carry
locations with reference plates and spend the prompt budget on action and light.

Environment plates are reusable across shots, which is also how you get location
continuity through a sequence.

---

## 8. Gotchas

**LoRAs are architecture-specific.** A Flux LoRA on Krea 2 logs hundreds of
`lora key not loaded` and `0 patches attached` — it loads, applies nothing, and
produces byte-identical output. A Krea LoRA does nothing for H3 either; H3 has no
LoRA stage in these templates. Krea/Flux LoRAs reach H3 only by improving the
reference images and start frames you feed it.

**Partner nodes spend credits.** `MiniMaxH3*` under `model/conditioning/minimax` are
local. `MinimaxHailuo03*` and `MinimaxImageToVideoNode` under `partner/video/MiniMax`
call MiniMax's hosted API. The names and descriptions are confusingly similar — check
the category.

**Model list refreshes without a restart.** ComfyUI invalidates its model-list cache on
directory mtime, so newly downloaded checkpoints appear in enum validation immediately.

**`validate_workflow` blind spots.** `COMFY_MATCHTYPE_V3` polymorphic inputs produce
`edge_type_mismatch` warnings that are false positives. It also cannot see
`COMFY_AUTOGROW_V3` sub-inputs, so a clean validation does not prove reference wiring
is correct.

**Autogrow sockets always show one spare.** An empty `ref_image_2` below two connected
ones is capacity, not a missing input. Ceilings: 9 images, 3 videos, 3 paired video
soundtracks, 3 standalone audio clips.

**Reference tags are positional and 1-indexed in prose but 0-indexed in sockets.**
`ref_image_0` is `<Picture 1>`. A reference video's paired soundtrack also consumes an
`<Audio j>` ordinal, before any standalone audio.

---

## 9. Video references: style transfer from real footage

First test of driving generation from a **reference video** rather than stills. Source:
19 s of handheld phone footage of an office full of stacked cardboard boxes, trimmed to
a 5.04 s / 121-frame slice at 24 fps. Target look: a desert canyon on an alien planet.
Both paths got the same Krea 2 canyon plate as their style source and matched prompts.

### The two mechanisms are not interchangeable

| | LTX 2.3 + IC-LoRA (depth control) | H3 ref2v (`<Video 1>`) |
|---|---|---|
| Video acts as | frame-aligned **control** | **reference**, like a character sheet |
| Camera move | preserved exactly | invented |
| Scene geometry | every object restyled in place | rebuilt from the gist |
| **Scale** | **inherited from the source** | free, and it chooses well |
| Audio | none | native stereo |

**The finding that matters: depth control cannot change scale.** The restyle was
otherwise a success — every carton became a banded stone monolith in its exact place,
desks became rock ledges, a spherical speaker became a boulder, the window became sky
with the ringed planet's arcs across it. But the result reads as a *tabletop diorama*,
not a canyon, because the depth map carries the real scene's scale relationships with
it. Desk-height boxes give desk-height rocks whatever the prompt says, and the motion
gives it away most: parallax and camera speed stay at the scale they were shot.

H3 given the same footage as a reference had no such problem — it produced a monumental
canyon at wholly convincing scale — because it never tracked the footage at all. It
read a narrow space, two masses flanking, a forward-left drift and a bright gap high in
frame, then built its own.

So the mechanisms trade off exactly against each other, and neither gives structural
fidelity *and* free scale. The way to get both is to author the control geometry at the
intended scale (a Blender/Unity render of untextured geometry, or a Z-depth pass) rather
than estimating depth from footage shot at the wrong one. `build_v2v_ltx.py
--control-mode passthrough` wires a pre-rendered control pass straight to
`control_images`, skipping the estimator. The IC-LoRA only requires frame-aligned
control images and is indifferent to their provenance — the template's own note says so,
which also means Canny or normals are available.

### Describe a reference video by its geometry, never its contents

§2's rule extends: naming what is in the reference video summons it. Describing
`<Video 1>` as "an office with cardboard boxes" would put an office in the output. It
was described instead purely as abstract form and motion — "two tall rectangular masses,
one filling centre frame, one at the right edge, each built of blocky volumes stacked
one on another; a flat horizontal plane running away to the left; a bright opening high
beyond the central mass; a single unbroken handheld drift forward and to the left." That
is simultaneously a true description of the footage and of the canyon wanted, and H3
followed it closely.

### Wiring `ref_videos`

`ref_videos.ref_video_0` is typed **IMAGE**, not VIDEO — it takes a frame batch, so a
file needs `LoadVideo` → `GetVideoComponents`, or a single `VHS_LoadVideo` (which also
gives `frame_load_cap`). Socket names carry an underscore before the index
(`ref_video_0`), not the `ref_video0` spelling the node schema's `wire_as` hint gives.
The node tooltip asks for frames at 24 fps, 2–15 s.

Reference cost scales with resolution *and* duration. The tokenizer pairs frames and
encodes each pair as one block (`comfy/text_encoders/minimax.py:175`, `process_video_block`
with `patch_size=16, temporal_patch_size=2, merge_size=2`), which works out at
**(W/32) × (H/32) tokens per 2-frame block**. The 121-frame clip at 896×512 is ~27k
tokens; the same clip at 1120×640 would be ~42k. §6 measured 16k as essentially free, so
keep the reference small and let the plate carry fine detail.

### The first frame must agree with the control pass

In the canyon test the canyon plate was wired to `first_frame` and **both models threw
it away**, in different ways. LTX showed it for exactly frame 0 and snapped to the
depth-driven geometry by frame 1. H3 did the opposite — it reproduced the plate almost
exactly as its opening frame and then invented a continuation, taking very little from
`<Video 1>`.

The LTX half of that is a design error, not a model limit: the plate was a canyon and
the control depth at frame 0 was a stack of office boxes, so the guide and the control
described different scenes and one had to lose. **Derive `first_frame` from the actual
first frame of the control clip** and it holds — confirmed in the Unity test below,
where a Flux 2 Klein photoreal treatment of frame 0 propagated cleanly through all 121
frames instead of being discarded.

The H3 half revises §5's claim that r2v invents its opening composition: with a strong
environment plate on `ref_image_0` it does **not** — it reproduces the plate and builds
forward from there. A plate and a reference video compete, and at `attribute_transfer`
the plate won decisively.

### Restyling authored geometry (Unity capture)

The follow-up test, and the one that confirms the §9 scale argument. Source: 5 s of a
Unity capture of a sci-fi research base on an alien planet, recorded years ago for
social VR. Goal was the opposite of the canyon job — keep the environment, replace only
the rendering with photographic realism.

**It works, and the scale problem simply does not appear.** The base reads as a real
structure in a real landscape because the geometry was authored at that scale to begin
with; nothing had to be talked out of desk proportions. The restyle added weathering
and streaking on the panels, real terrain with rock and coarse grass, atmospheric haze
that separates the base from the ridgeline and shifts correctly as the camera moves,
and practical lights with real falloff — while keeping the tower, the tank cluster, the
deck layout on red columns, the yellow railings, the dish array and the solar field
where they were.

Depth vs Canny on the same clip, same seed, same prompt:

| | Canny | Depth (VideoDepthAnything) |
|---|---|---|
| Surface/design detail | slightly better — panel seams, greebles | slightly softer |
| Tone and grade stability | **drifts** — brightened toward a hazy daylight, gained a lens flare by ~4 s | **holds** the night look throughout |
| Sky and mountains | washes out late | stays crisp |

On this clip depth was the better default. Canny discards luminance entirely and is
per-frame with no temporal smoothing, so it left the grade unanchored. **But that
conclusion did not survive the next test** — see below; the drift turned out to be a
property of the first frame, not of Canny.

Two caveats on the first-frame step. Flux 2 Klein held the layout faithfully but
**reinterpreted the sky**, turning a magenta nebula with a bright vertical streak into a
green aurora — and because the first frame anchors the whole clip, that drift propagates
to every frame. Name the sky explicitly in the first-frame prompt if it matters. Also,
the Unity capture has the **mouse cursor** burned into it; Flux removed it from the
first frame, and neither control pass reproduced it, but it is worth cropping or hiding
at record time.

### Untextured massing, 10 seconds (Unity/OBS city capture)

The purest form of the authored-geometry case: an OBS capture of a Unity city scene
that is **flat-shaded massing only** — white and grey volumes with arbitrary placeholder
tints (purple, pink, green), window-grid geometry on many blocks, no materials, no
lighting, no skybox at all. Target: a golden-hour cinematic helicopter fly-over.
241 frames at 1024x576, 10.04 s, ~8 min per run.

**10 seconds is fine.** Double the frame count of every earlier run, no degradation, no
temporal breakup, and the grade held end to end. LTX's 8k+1 grid gives 241 frames; VRAM
peaked comfortably inside 32 GB at 1024x576.

**Placeholder tints are ignored, as hoped.** Depth discards colour outright, and even
Canny — which sees only edges — produced no purple buildings. Material IDs in a working
scene cost nothing here, so there is no need to clean up a scene before using it.

**Canny beat depth decisively on this source, reversing the Minerva result.** Depth
turned the larger volumes into blank white slabs, because a massing model's flat faces
carry no depth variation to restyle — the window grids that the geometry actually has
were thrown away. Canny kept them, and every tower came back with a real curtain wall.

The important part: **Canny did not drift here, over twice the duration that it drifted
on Minerva.** So the earlier "Canny leaves the grade unanchored" conclusion was wrong as
stated. What changed was the first frame. The Minerva anchor was almost entirely
structure with very little sky; this one was chosen for its large sky area and explicit
golden-hour gradient. The revised rule:

> Canny's grade stability is a property of the **first frame**, not of Canny. Choose an
> anchor with a generous, unambiguous sky and a clear lighting direction and Canny holds
> for at least 10 s — while keeping surface detail depth cannot.

Which control to reach for follows from what the source actually carries:

| Source | Control |
|---|---|
| Flat-shaded massing with window/panel geometry | **Canny** — it is the only thing that sees the detail |
| Textured, already-lit render (Minerva) | **Depth** — luminance is worth preserving |
| Real footage | **Depth** — temporally consistent, and edges are noisy |
| Pre-rendered depth / clay pass | **passthrough** |
| Replacing a performer with a different body | **Pose** — the only one that drops the silhouette |

Practical notes on capturing from an editor: crop the UI before anything else — this
capture had a Unity toolbar along the **top** edge as well as the Animation/Audio Mixer
bar along the bottom, and the first crop caught only the bottom one. The mouse cursor is
burned in again. And pick a window whose FIRST frame is a strong composition with sky
visible, since it anchors the whole clip; the obvious 10 s window here opened with the
camera buried against a tower face and had to be moved.

### Restyling changes surfaces, it does not add set dressing

Same 241-frame city control, same Canny, target changed to a rainy neon cyberpunk night.
The first frame was a Flux 2 Klein cyberpunk treatment of the source frame 0 and looked
exactly right: giant vertical neon signs down the facade, backlit screen panels, wet
roofs doubling every sign, low cloud lit hot orange from beneath.

**It survived about two seconds.** By 6 s the neon had decayed and the buildings were
back to flat pale grey. This is a different failure from the earlier grade drift — the
anchor was sky-rich and unambiguous, which is what fixed Canny before.

The distinction that explains it:

> Control-guided restyling can change how existing surfaces **look** — material,
> weathering, lighting, grade. It cannot sustain new **objects** that have no support in
> the control signal. Canny carries the source's building edges and nothing else, so
> there is nowhere for a neon sign to live. Golden hour held because sunlight on
> concrete is a property of surfaces the geometry already has; neon advertising is set
> dressing that does not exist in the scene.

`--ic-strength 0.6` (from 1.0) recovers most of it. Loosening the guide gives the prompt
and the anchor enough authority to hold night, wet streets, lit windows, coloured glow
and rain for the full 10 s. What it does **not** restore is the signage itself — the
large neon signs stay a first-frame-only feature. So ic_strength trades structural lock
for look authority, and it is the right knob when the target grade is far from what the
control implies; it is not a way to invent geometry.

The real fix for signage is upstream: **put emissive billboards in the Unity scene**.
Then the signs are in the geometry, Canny sees their edges, and they persist for the
same reason the window grids do. Untested here, but it follows directly from the
mechanism, and it is cheap for anyone who owns the scene.

Rough guide to `--ic-strength`:

| | |
|---|---|
| 1.0 | maximum structural lock; the control dictates the look, and a far-off target decays back toward it |
| ~0.6 | look holds against the control; geometry still tracked. Use when the target grade is far from the source |
| lower | untested here; expect the geometry lock to start slipping |

### Character replacement by pose control

A different job again: replace the performer in a video rather than restyle the scene.
Source was 5 s of a person side-on to a locked-off phone camera, playing a
motion-controlled game projected on an office wall. Target was a full-body husky mascot
costume, from a single reference photo.

**Control choice is forced here.** Depth and Canny both lock the *silhouette* of who was
filmed, so a bulkier body with a much larger head cannot replace a person under either —
you get a human-shaped mascot. An OpenPose skeleton carries the motion and deliberately
discards the outline, which is the only way the substitution has room to happen. This is
the mirror image of the city job, where discarding the silhouette was the problem.

**It works, and identity holds far better than the neon did.** Blizzard is present and
consistent across all 121 frames — head, jersey, sash, shorts, fur — with the room, the
score readout and the lighting intact. That is the set-dressing rule from above
confirmed from the other side: the mascot is not decoration added on top of the control,
it *is* the thing the control describes, so the model has a reason to keep drawing it.

Two honest limitations:

- **Motion tracks approximately, not exactly.** The gestures follow, but the mascot's
  shorter, bulkier arms do not reach where the performer's did, and the timing is loose
  frame to frame. Fine for a mascot gag; not a match-move.
- **The projected game graphics are largely lost.** The skeleton carries no room, so the
  bright hexagons and arcs on the wall exist only in the first frame and fade out. This
  is the same mechanism as the neon: anything outside the control signal decays.

The fix for the second one is post, not prompting. The camera is locked off, so the
original background is a perfectly good plate — mask the generated mascot and composite
it over the untouched source footage, and the real wall graphics come back for free.
Worth doing before reaching for a fancier control.

`--ic-strength 0.8` was used, between the 1.0 that let the neon decay and the 0.6 that
loosened the city geometry.

### Repairing the LTX IC-LoRA template

`video_ltx2_3_ic_lora` ships `runnable: false` here (7 errors) and needed three fixes
beyond the obvious model-name swaps, all in `build_v2v_ltx.py`:

- **Latent must divide by 64, not 32.** The IC-LoRA carries
  `reference_downscale_factor 2` and `LTXVAddGuide` requires the (w/32, h/32) latent to
  divide by it. 1120×640 validates clean and then dies at runtime with *"Latent spatial
  size 35x20 must be divisible by reference_downscale_factor 2"*. Use multiples of 64.
- **`LTXVEmptyLatentAudio.frame_rate` is an `io.MultiType`,** and comfy-cli's UI→API
  conversion consumes no widget value for a MultiType input — it leaves the schema
  default and passes the intended value on to the *next* widget, so `widgets_values[1]`
  lands on `batch_size`. The audio latent is shaped `(batch_size, …)`, so it then fails
  to concatenate with the video latent, and the run dies far away inside KSampler with
  *"Expected size 1 but got size 25"*, naming neither node nor widget. Pass `frame_rate`
  by **link**, and let `widgets_values` carry only `[frames_number, batch_size]`.
  Confirmed by reading the submitted prompt from ComfyUI's `/history/<prompt_id>` —
  which is the fastest way to settle any question of what comfy-cli actually sent.
- **MoGe is not installed and is the wrong tool anyway.** `video_depth_anything_vits.pth`
  is already on disk under `models/videodepthanything/`, and being temporally consistent
  it beats MoGe's per-frame estimate here: control flicker becomes output flicker.

Cost: 121 frames at 1088×640, 8 steps, ~4 min. H3 at 0.7 MP / 124 frames, 20 steps,
~7 min — both far cheaper than §6's figures, which were for 10 s at higher settings.

---

## 10a. Music-driven timing (first test, n=1)

**Mechanism.** `MiniMaxH3AddGuide` with an `audio` input pins a soundtrack onto the
target timeline at `frame_idx` (the streams share one time axis). The guide latent is
re-injected every step and never denoised, so the model draws picture against a fixed
track. `MiniMaxH3ReferenceToVideo`'s `ref_audio` is different: a style reference, not
a timeline anchor. `build_beat_test.py` builds t2va with or without the guide;
`beats.py` finds beats and cuts beat-aligned slices; `beat_sync_score.py` scores
motion against the beat grid and the music's onset curve.

**Test.** 10.2 s of *No Fucks at All* from 178.99 s (123 BPM, sliced to start on a
beat), t2va, locked-off dancer under one spotlight, 1120x640, 243 frames, seed 424242,
guided vs the same prompt and seed unguided. ~15 min each.

**The soundtrack survives.** Output audio correlates 0.90 with the guide at zero lag.

**Motion follows the song's structure, not a metronome.** This section is not
four-on-the-floor: big accents at 0.0 / 2.2 / 4.1 s, a near-silent break ~6.0-7.8 s,
full band from 7.8 s. The guided dancer bursts on each accent (trailing by ~4 frames),
stands still through the break, and hits every beat once the band enters. The unguided
dancer moves continuously at her own ~0.45 s pulse from start to finish, unrelated to
the song. By eye the difference is unmistakable.

**The numbers do not yet prove it.** Beat-phase vector strength 0.66 vs 0.17, but
p=0.14 against a circular-shift null; smoothed motion-vs-onset r=0.19 vs 0.13, p=0.28.
Onsets are spiky and the guided motion ignores some strong ones (5.0-5.5 s), and a
circular shift of a signal made of long quiet/loud blocks is a conservative null. One
seed is an anecdote. Next: more seeds, a loudness-envelope metric, and a clip with a
steady kick.

### Lip sync to a pinned vocal

**Test.** 10.2 s from 95.515 s ("So I filed it away / Under nope, not now, not ever
today / Traffic was a circus, but I floated above"), full mix pinned with AddGuide,
generic male singer close-up at a vintage mic, static camera, seed 515151. A: lyrics
in `<d>[English] ...</d>` tags at their Whisper timestamps. B: identical prompt with
"sings the verse" and no words. Scored with `mouth_track.py` (mediapipe inner-lip gap
over eye width) against the Demucs-isolated vocal's RMS (`lipsync_score.py`).

| | r (best lag) | lag | p (shift null) |
|---|---|---|---|
| A, lyrics in prompt | 0.35 | mouth leads 2 f | 0.001 |
| B, no lyrics | 0.33 | mouth leads 3 f | 0.001 |

**The audio drives the mouth, not the prompt.** Both lock to the vocal, and the two
mouth traces correlate 0.76 with each other. Writing the lyrics in bought almost
nothing on open/close timing. The mouth leading the voice by 2-3 frames is how real
singers look. Caveat: aperture vs loudness measures timing, not viseme shape (f, o, m);
whether the lyrics improve mouth *shapes* needs eyes on the 2-up (`out/lipsync_2up.mp4`).

**References plus guide is wired.** `model.py` places AddGuide keyframes after any
ref2v reference blocks on the same timeline, so character sheets and a pinned track
can combine. Untested; the ref2va checkpoint may not have seen audio guides in training.

Tooling: Demucs (`--two-stems vocals`) and faster-whisper large-v3 word timestamps in
`.venv_audio`; mediapipe 0.10.21 needs numpy<2, so face tracking lives in `.venv_face`.

## 10b. Character design pipeline (singer, 2026-09-27)

The user's manual method, which worked: face close-up in Krea -> angles and
expressions from that face in Flux -> full-body sheet in Krea guided by the face
sheet -> Flux to place him in the set.

- **Krea smooths faces toward handsome and neutral.** Detailed feature lists (hooked
  nose, gap teeth, jug ears) came back as a generic headshot. Leading with an expression
  and calling him an "eccentric character actor" unlocked odd features but aged him to
  ~55; asking for 24 brought youth back and flattened the features again. Krea would not
  render an open grin or a tooth gap at all; Flux did expressions easily.
- **Flux edit preserves a face well enough to add props.** Red glasses onto the chosen
  face: identity intact in 4/4. Tinted lenses leave a pink glow on the cheeks, which
  then propagates into everything built from that image.
- **Phrase angles as camera moves, not poses.** "A clean side profile facing right"
  gave three-quarter views facing the wrong way and Pinocchio noses (Klein 9B, 3-ref
  template). "Rotate the camera 90 degrees to the right, show the man in profile" gave
  true profiles both ways (the user's phrasing, Klein 9B).
- **`build_flux_batch.py` (user's Flux2_K8B_Batch_Prompt, Klein 9B, 4 steps) is ~15x
  faster:** 9 edits in 41 s versus 16 in ~10 min through `build_flux_multiref.py`. Both
  load the same distilled 9B; the multiref template just runs 20 steps. The model is
  distilled for 4, so pass `--steps 4`.
- **Full-body sheets lose the face.** Krea's purple-suit sheet nailed the costume, but at
  ~100 px per head he aged further and his spikes went to orange frizz. Carry identity
  with the face sheet and costume with the body sheet, as two references.

- **Three characters in one Flux pass: two hold, one slips.** Band on the s1 set, 4 refs
  (set + one combined body-over-face sheet per musician), 4 steps, 43 s for 4 takes.
  Singer and guitarist held; the drummer (smallest, furthest back) lost her face and
  her crimped hair became an afro-like mass, and one take made her hair all red.
- **A targeted repaint bleeds identity onto the most prominent face.** Re-running with
  "change only the drummer" fixed her but turned the singer into her as well. Fix:
  composite only the drummer's region from the repaint onto the original with a
  feathered mask. Flux output came back 1376 px wide against a 1360 px source; resize
  before compositing. Master frame: `refs/band/band_s1_master.png`.
- **Steps:** the user gets good results at 5-10 steps on both Klein and Krea.

### Lip sync with the designed band, i2v vs ref2v

Same 1:35.5 slice pinned by AddGuide, seed 616161, wide band shot cutting to a medium
close-up of the singer at 1.7 s. A: fl2va, `band_s1_master.png` as `first_frame`.
B: ref2va, four refs (three body-over-face combo sheets + the empty set) at `max`,
with AddGuide pinning **both** the master frame at frame 0 and the song.

- **ref2va + AddGuide image + AddGuide audio works.** The first untested combination:
  the pinned master held the opening frame, the cut landed, and the singer's face sat
  closer to his sheet than in i2v. (`build_beat_test.py --refs ... --guide-image ...`)
- **Scores looked weak (r 0.27 / 0.29, p ~0.2) but that is the window.** The earlier
  generic-singer clips, significant at p=0.001 over 10 s, drop to p~0.08 over the same
  8.2 s close-up window. Aperture-vs-RMS needs long windows.
- **The stronger evidence: mouth traces agree across renders.** All four lip-sync
  renders (two seeds, two different singers, both modes) correlate 0.67-0.88 with each
  other on this window. Different faces and noise moving their mouths the same way can
  only be the pinned audio. Use cross-render agreement, not r vs RMS alone.
- Soft spots in both: mouth barely opens on "was a circus" (7.3-8 s) and after 9.2 s.

### Text props survive in ref2v

Krea spelled a gold extruded "FUCK" correctly in 4/4 takes (`refs/props/prop_gold_word_*`).
Given to H3 ref2v as its own `<Picture>`/`<Subject>` with `fully_preserved` and the word
quoted in the retention line, the lettering stayed legible through a 5 s handling shot
(held up, turned, lowered into a chest); it only smeared while edge-on to camera.
Treat props like characters: a dedicated reference picture plus a subject definition.

### Production render costs (music video)

- Shot 1, fl2va i2v, 1120x640, 362 f: ~25 min.
- Shot 2, ref2va, 4 combo sheets at `max` + AddGuide image + audio, 1120x640, 345 f:
  **29:49 sampling (89 s/it)**, twice the 10 s ref2v cost in section 6. Four large sheets
  at `max` are no longer free at this length. Worth testing `match` or fewer steps.
- Shot 2 lip sync over 12 s of close-up singing: r=0.33 at lag 0, p=0.001, with a
  1.2 s crash zoom into the close-up before the first line.
- The comfy MCP `job wait` aborts after 1800 s of silence; poll `status` instead for
  renders over 30 min.

- **Small faces: crop and upscale before mouth tracking.** Shot 4's medium-wide framing
  gave mediapipe 0/362 faces; a 3x crop around the head gave 362/362 and r=0.54, the best
  sync score of the project. Short clips (5 s) are too short for the metric (shot 7:
  null median 0.27, so even real sync cannot clear it); judge those by eye.
- **Instrumental-pinned vignettes keep motion on the beat without anyone mouthing lyrics**
  (shots 3a/3b, 6). An audience ref2v shot from the lineup sheet brought back all six
  people, including the one Flux dropped from the establishing still.

### Act 2 production lessons (20 ref2va shots)

- **Many references make H3 play them as shots.** With 5-8 reference pictures, several
  renders opened on (or cut to) the reference sheets themselves on a grey backdrop:
  9a opened on the chest prop for 1.2 s, 12c stayed on the robot sheet's grey backdrop
  the whole time, and both finale takes (8 refs) spent 2-4 s on grey sheet shots. **Fix:
  pin a frame of the intended set at frame 0 with AddGuide** (12c fixed on the first
  retry), and in the edit pick the on-stage stretches. A flat mid-grey top band
  detects sheet frames reliably.
- **Pin both ends of a camera move with two AddGuide keyframes** (`frame_idx` 0 and -1).
  A closer tracking take pinned only at frame 0 lost the set to the sheets' grey backdrop
  after ~3 s, once the camera left the guide's coverage. Pinning a second crop at the last
  frame kept the stage for the full move and gave the most motion of any dance take.
  Crops of a wide render, upscaled, work fine as keyframes. (`build_beat_test.py --guide-end`
  via the 6th field of a `queue_act2.py` spec.)
- **Intercuts under lip sync must be song-aligned** (piece offset = song time - slot start);
  intercut helpers that resume each take on its own clock are only for silent vignettes.

- **Ten people in a wide static shot barely move.** The dance line's motion energy was
  below a single-singer medium shot; rewriting it as a named kick routine helped a little.
  Big group dances want a closer angle or a moving camera.
- **Costume swaps via Flux edit of the existing body sheet** (hat off, power suit on)
  kept the guitarist's identity far better than Krea from his face sheet, which put him
  back in the ringmaster coat in half the views.
- **Act 2 render time:** 20 shots + 3 redos, about 8 h unattended at 20 steps.

## 11. Upscaling (SeedVR2 3B int8, ComfyUI native)

Resolve's Super Scale is Studio-only; the installed Resolve 21.1 is the free edition (no
external scripting either). SeedVR2 via the `utility_seedvr2_3b_int8_upscale_video`
template needs `seedvr2_3b_int8_convrot` (3.46 GB) + `seedvr2_ema_vae_fp16` (0.5 GB).
`build_upscale.py` wraps it (`--scale`, `--color`, `--split`).

Tested on 3 s (72 f) of shot 4, 1120x640:

- **2x (2240x1280): ~100 s per 3 s** -> ~2.5 h for the whole video. Natural detail: hair
  strands, glasses wire, checkerboard, phone keys, calendar digits.
- **Native 4K (3.43x): ~360 s per 3 s** (~8 h), needs `--split` (temporal chunks; without
  it the sampler OOMs at 52 GB). Skin turns slightly painterly. Prefer 2x + Lanczos to 4K.
- **Free VRAM first.** Leftover H3 models (and an open Resolve) OOM'd even the 2x pass.
- **Colour:** uncorrected output drifts warm and +11% saturation. `wavelet` restores the
  source's colour and saturation (144.7 vs 143.1) and keeps the detail -- use it. `lab`
  lands slightly flatter than the source (137.4). Colour correction is post-processing
  only, so re-running with a new method reuses the cached sampling (6 s).
- **SeedVR2 caricatures small faces.** Faces a few dozen px wide in the source become
  crisp, wrong faces (black-ringed eyes, gaping mouths) -- worse than the soft original.
  Lower `denoise` does not help (one-step model: <1 just switches restoration off).
  **Fix: `face_composite.py`** -- YuNet (`models/face_detection_yunet_2023mar.onnx`, 230 KB,
  OpenCV zoo; finds 9-21 px faces mediapipe misses) on the source, then feathered head
  ellipses revert faces <40 px fully to Lanczos, fading out by 80 px, max-pooled over
  +-3 frames. Keeps 91% of SeedVR2 sharpness; close-ups untouched. Full video ~17 min.
  Output: `out/rough_cut_v5_2x_facefix.mp4`.

- No added flicker (frame-to-frame diff 1.6 vs 1.24 source, same as detail gain).

## 12. Families and multi-era casting (Grounded, 2026-09-29)

Character work for *Life in 2045* (recurring family across an album; a plane sequence
repeated in three eras with the same cast). All Flux 2 Klein 9B at 6-8 steps, Krea 2 at 8.

- **Relatives from a parent's face.** "Show his son instead: ... clearly inherited his
  face, the same heavy brows, grey-blue eyes, slightly crooked nose" on the grandfather's
  face gave four sons who read as related at a glance, and a "daughter" who did too. The
  flip side: a face derived from one character carries his brows and eyes, so a spouse
  must NOT be derived from her husband's family (she'd look like his sister). Give
  in-laws a fresh Krea face.
- **A child from both parents in one pass works.** Flux multi-reference with the father
  and mother faces as images 2 and 3 and "their son ... his father's brows, grey-blue eyes
  and nose, his mother's angular face and cheekbones" gave four near-identical boys who
  visibly took after both. A single-parent derivation read androgynous and too close to
  the mother.
- **Krea costume sheets drift the face and hair.** Body sheets from a face sheet grew the
  hair to the collar and narrowed the face. Fixed by a Flux multiref pass: image 1 the
  body sheet, images 2-3 the face sheet and master face, "keep image 1 exactly, change only
  his head in every view". Side effect: grey stubble grew into a short beard.
- **Flux angle sheets: 7-8 of 8 hold.** Right profile was the usual failure (hair grew,
  face changed); a re-roll phrased "a clean side profile, nose pointing to the right edge
  of the frame" fixed it. A big grin makes Flux de-age a face by ~10 years.
- **Era restyling of a group loses identities unless each person is named.** "Dress them
  for the 2040s ... the flight attendant ... her hair in the same low bun" turned the Black
  flight attendant into a white woman in both eras. A second Flux multiref pass (restyled
  lineup + original lineup, "give each person the face of the matching person in image 2")
  swung the other way and restored the original clothes. What worked: a single-reference
  edit whose prepend names every person's identity explicitly ("the tall Black woman with
  warm brown skin and a neat low bun keeps her exact face and skin; the elderly white man
  with ...") and says "changing only their clothes". 4/4 held.
- **Set redress keeps geometry.** "Keep the exact same camera position, lens, perspective,
  aisle, seat rows, window positions and cabin geometry" + an era restyle kept one cabin
  aligned across three eras, including replacing the cockpit bulkhead with a nose window.
  A mild restyle (2030s) came back too close to the original; name colours and materials
  to force a visible difference.
- **Multiref first frames with the same prompt skeleton match across eras.** One hand-off
  prompt on three redressed cabins + three era lineups gave three compositions with the
  attendant, passenger and aisle in nearly the same places.

- **A lineup sheet as a reference still makes H3 open on it, even with a first frame pinned.**
  Plane A v1 (refs: cast lineup, pilot sheet, cabin plate; start and end frames pinned by
  AddGuide) spent its first 2.5 s on the grey lineup sheet. Dropping both sheets and keeping
  only the cabin plate, with the people carried by the pinned start/end frames and described in
  prose, fixed it on the next take, and identities still held (they come from the frames).
- **Check which way the crowd faces in a first frame.** A forward-looking cabin shot came back
  from Flux with every passenger's face turned to the camera over the seat backs, i.e. sitting
  backwards; nobody noticed until the render (the user did). Spell out "every passenger faces
  the front of the plane, the camera sees the backs of their heads". H3 then also invented
  backwards-facing rows as the camera advanced (take 2) until the shot prose said the same
  thing and described the camera "overtaking each row from behind" (take 3).
- **Start + end frame pinning carries a long dolly move.** 15 s up an aisle into the cockpit,
  both ends pinned, the pilot-on-phone ending landed exactly as framed. Midway H3 passed a
  bulkhead into a second cabin section, which reads as a natural wipe.

- **Grounded first pass: 28 shots, 23 kept on the first render.** Failures: the storm
  flashback rendered as a calm dusk runway (fixed by describing rain, wipers and lightning
  "the whole time" / "every few seconds"); the departure-hall reveal lost Steve after 2 s
  (fixed by pinning the empty hall at frame 0 and Steve's framing at the last frame); an
  apron shot's radar dome morphed into a square antenna in all three takes, even after
  "sits motionless" (worked around in the edit: its clean first 3.6 s at half speed with
  `minterpolate` motion interpolation). Words like "turns" on an object invite H3 to
  transform it.
- **H3 adds its own cuts in single-subject shots** (fence close-up → through-the-wire
  close-up; wide fence → medium on Steve). Usually usable as coverage; check before re-rolling.

- **User review of rough cut v1, and what fixed each note:**
  - *A long dolly outruns its destination.* Planes A and B: the cockpit door visible at the
    start "warped" into a second cabin because the camera reached the front at ~8 s and H3 had
    to fill the rest before the pinned end frame. Slowing the push ("glides slowly", "Push with
    medium amplitude at slow speed", "the same cockpit door growing steadily larger the whole
    way", arrival stated at 00:12.500 of 15 s) gave one continuous cabin on both.
  - *Planes in the sky move like models on a string* when the plane is the subject of the
    motion: a plane "flying through a storm" rotated in place against a frozen lightning bolt,
    and planes "climbing" outside café windows hung and drifted. What worked: the camera
    moves, the plane "holds a steady, level course" (camera overtakes it, Truck), rain and
    "lightning flashing in different places every few seconds"; and a plate without a painted
    bolt. Distant takeoffs across a runway (fence shots, night takeoff roll) were fine.
    Planes seen through windows: remove them from the frame and cut to a separate exterior.
  - *Props need a reference image.* "Small silver captain's name badge" rendered as a police
    shield in two shots. A Krea prop plate of a crew ID card as its own `<Subject>` with
    `fully_preserved` and "CAPTAIN" quoted held in both re-renders (first frames rebuilt
    with the prop as a Flux multiref input).
  - *Terminal interiors seen through glass decay* (an airport's lit interior became a parking
    lot mid-shot): cut long establishing shots in half and add a second angle.
  - Adding a prop reference to a character shot made H3 cut straight to an insert of the
    prop on one seed; the next seed kept the pinned composition.

## 13. Dark first frames and horror characters (Black-eyed Children, 2026-09-30)

First tests for a night-time horror video built from 5 s clips. Paths are relative to
`projects/urban_legends/black_eyed_children/`.

- **A dark Flux first frame holds for 5 s.** Three takes of one chorus slice (124 f, 1120x640)
  from a low-key Flux multiref frame: mean luma 49.6 → 54.3 (ref2va, frame pinned by AddGuide),
  49.8 → 56.7 (fl2va, `first_frame`) and 59.1 → 59.8 (fl2va, static camera). The drift in the
  first two came with a camera push that opened up more of the lit street. This is the way
  round section 3: carry the darkness in the frame, not in the prompt. Untested beyond 5 s.
- **ref2va + pinned frame and fl2va + first frame gave the same shot** at the same seed, down to
  the mouth shapes. For a pinned-composition shot i2v is the simpler graph (5 min for 5 s).
- **Krea ignores "solid black eyes, pale skin" on a child's face** (12/12 ordinary children).
  The Krea LoRA `horrorstyle47b` (trigger `horrorstyle`) at strength 1.0 gave black eyes and
  pallor with real skin in 6/6; at 0.6 the eyes were only dark. A Flux edit of the plain Krea
  face also works but paints it on: white mask skin and oversized black holes.
- **Small black eyes do not survive a multiref first frame.** With the faces about 60 px wide
  the three children came back with ordinary eyes (one of three still dark). A second Flux pass
  on the finished frame ("give all three children solid glossy black eyes ...") fixed it, and
  H3 then held the black eyes and white skin for the whole clip.
- **A pinned vocal overrides "blank face".** With the full mix pinned, all three children
  mouthed "Please let us in" in unison in every take, but the long "ee" of "please" pulls the
  lips into a grin and the loud notes open the mouths wide. Rewriting the shot as flat,
  mechanical speech with frozen brows and cheeks changed nothing: the mouth shapes were the
  same at the same timestamps. Blank faces need the instrumental stem.
- **Flux angle sheets kept the black eyes in 24/24 views** (three children, eight views each,
  with "solid glossy black eyes from lid to lid" in the prepend).
- **Krea body sheets from a child's face lose the look and the age.** All nine sheets came back
  with ordinary eyes and skin, and "six, short and sturdy" came back as a toddler in 3/3;
  "a six-year-old schoolboy ... slim arms and long slim legs, a head about one sixth of his
  height" fixed the age in 3/3.
- **Putting the look back on a body sheet: swap the head, don't edit the eyes.** A single-image
  Flux edit ("give the child pale skin and solid black eyes in every view") turned all three
  children into white mannequins with huge eyes and changed their hair. The multiref head swap
  from section 12 (image 1 the body sheet, images 2-3 the face master and a profile, "change
  only the child's head in every view") gave natural black eyes and pallor in 6/6.
- **Opening a door by Flux edit keeps the plate.** "The front door now stands wide open ..."
  with a keep-the-camera prepend worked on 6/6 plates (three porches, three hallways), and the
  hallway versions invented a matching rainy street outside.

### The 5-second-clip video (80 shots, rough cut in one night)

Every shot fl2va from a Flux first frame, 124 frames, ~5 min each; three 15 s shots with a
pinned end frame. First pass 80 renders in ~7.5 h; 26 re-renders over two fix rounds.

- **69 of 80 first renders were usable.** With a first frame carrying the composition and the
  light, and only one action per 5 s, there is little left to go wrong.
- **Jump cuts on the beat grid work.** A 15 s push from wide to close, played two beats on and
  two beats off (`assemble.py`), reads as a deliberate stutter toward the subject and every cut
  stays on a beat. Pin the end frame, or the push has nowhere to go.
- **Empty plates brighten.** A street or house front with nobody in it and a camera push or the
  word "flickers" drifted and lifted from luma 25-30 to 48-105 within 2 s. `Static` plus
  "Nothing moves but the rain" held most of them (30 → 32); one view still brightened on three
  seeds while another take of the same plate held, so re-roll or reuse the stable take.
- **Lights going out works when both states are frames**: lit house at frame 0, a Flux "every
  window is now dark" edit pinned at the last frame, and a timestamp in the prompt.
- **A look string leaks everywhere.** "Night, heavy rain falling" appended to every frame prompt
  put rain inside the living rooms and hallways. Interiors need their own look line ("the air
  inside dry and still, rain only on the outside of the window glass").
- **Black eyes, by face size.** Faces under ~80 px in the frame: a single-image Flux edit
  "colour the eyes black ... inside the natural outline of the eye" (`frames.py ink`); it reads
  slightly like sunglasses on the smallest faces. Close-ups: that prompt leaves a dark iris with
  white around it; "make both eyeballs entirely glossy black from corner to corner, covering the
  whites" (`frames.py blacken`) is what works. A multiref pass from the face masters did nothing.
  Once the frame has them, H3 keeps black eyes for the whole clip, singing included.
- **Small figures seen from high above render as cartoons** in motion (pale blobs walking); the
  same action from road level, figures knee-up in the foreground, stayed photographic.
- **A close-up may simply not sing.** Two of nine single-child chorus close-ups kept their mouths
  shut on two seeds each; "his mouth opening wide on every word and his lips shaping each one
  clearly" plus a new seed fixed both.
- **Hands default to adult size.** "A child's small white fist" gave a man's arm twice; "a tiny
  fist no bigger than the brass knocker on a thin wrist" gave a child's.

## 14. Restyling real talking-head footage (spoken promo, 2026-10-02)

Phone footage of a presenter speaking to camera (vertical, selfie walk and a locked-off
wide), restyled into science-fiction sets while keeping the real voice.

- **Recipe: Flux 2 Klein edit of the take's own frame -> H3 fl2va with the speech slice
  pinned by AddGuide.** The Klein edit ("Keep the man exactly as he is. Transform the room
  behind him into ...", or a costume swap that names the features to keep) held the
  presenter's likeness in 7/7 frames at 8 steps, and relit him to match the new set. H3
  then invents the motion and lip-syncs to the real audio. 640x1120 portrait works as-is.
- **Speech lip sync holds, but aperture-vs-RMS cannot show it.** `lipsync_score.py` gave
  r ~0.1-0.2, p > 0.1 on the renders *and on the real footage itself* (r 0.03-0.06):
  speech has no long open vowels and a moustache hides the inner lip. Score against the
  **real footage's mouth trace** instead: generated vs real aperture r = 0.64 and 0.59 at
  lag 0 to -1 frames over 9 s and 15 s.
- **Added set dressing decays on a long walk.** A 15 s selfie-walk render kept its hologram
  panels and ceiling light strips for ~10 s, then walked into a plain corridor. Rendering
  the tail as its own 5 s shot from its own restyled first frame restored them. Same rule
  as section 9: dressing with no support fades; keep restyled walking shots short or re-anchor.
- A pause in the pinned speech is performed as a pause (hands drop, a glance aside), so one
  render can cover two lines and be jump-cut in the edit.
- Cost: 209 f ~17 min, 226 f ~19 min, 362 f ~30 min, 124 f ~10 min at 20 steps.

## 15. A solo singer through many sets and costumes (Not my Pig, Not my Farm, 2026-10-02/04)

One designed singer, six costumes, a recurring pig and its owner, a party host and baby, 22 locations, 71 shots of
5 s (fl2va from Flux first frames, the Black-eyed Children method). Three review rounds with the user, then a 2x
upscale. Paths are relative to `projects/not_my_pig/`.

### Designing the character

- **"Brunette" on a Black woman's hair comes back black from Krea** (16/16 faces). A Flux edit lightened it, but
  "rich warm chestnut", "auburn" and "caramel highlights" all went copper/ginger (4/4). What gave a natural
  brunette: "a deep dark brown, just a few shades lighter than it is now" and "dark cocoa brown".
- **"Eccentric character actor" aged a woman to ~55 again** (4/4), as it did the male singer in section 10b.
- **Costume changes as Flux edits of one body sheet: 5/5 kept her face, curls and makeup** (power suit, tracksuit,
  sequin dress, dress + leather jacket, silk robe + headwrap; Klein 9B, 6 steps, one batch in 30 s). Prepend:
  "Keep image exactly as it is: the same woman with the same face ... the same three poses ... Change only her clothes
  in all three views". Only flaw: the suit's back view shows the jacket front.

### First frames: masters, derived angles and colour rules

- **Derive every angle in a place from one master frame of her** (the user's rule: edits of the first reference you
  like beat regenerating). Multiref with the master as image 1 and her combo sheet as image 2, "The same place as
  image 1 ... the same woman in the same clothes": 33 derived frames, all in the right place and outfit. Later fixes
  followed the same rule — "one pig in the whole picture" still gave two pigs on two seeds, but an edit of the
  original one-pig frame adding only the missing detail worked first time; a baby handed to "the host at the frame
  edge" went to a stranger's arm until the frame was an edit of the previous shot, where the host already stood.
- **But shots without her start from the empty plate.** A single-image edit of her master asking for *someone else*
  gave her the action: "a dog walker trussed up in six leashes", edited from her sidewalk master, tied up *her*; a
  master with her on the stoop, asked for her walking through a crowd, gave two of her.
- **Keep the camera explicitly.** A derived angle "seen from further back so both doors are in frame" shortened the
  hallway; "Keep the exact same camera position, lens, hallway length, doors and lighting as image 1" kept it.
- **A colour rule in the look string leaks.** "She is the only person wearing purple" dressed a stranger in purple in
  11 of the 26 frames she is absent from, and put a crowd in lavender robes when she was in frame. Fixes: a separate
  look line for shots without her ("Everyone wears ordinary everyday colours: grey, navy, brown, denim, red and
  green", 11/11), and naming the crowd's colours when she is present ("white, grey, navy, yellow ... she alone wears
  violet"). Same mechanism as the indoor rain in section 13.
- **Extras need a distinct look**, not just clothes: a canvasser in an orange vest came back as a second copy of her.
  "A lanky young white man with messy red hair and freckles" fixed it.

### Props and text

- **Props drift between shots unless they have a reference.** One, two or a bucket-sized coffee cup; a different
  baby, and host, in every party shot. A trench sheet with the cup in her right hand (Flux edit of the body sheet:
  "Change only her right hand in all three views: she now holds one ordinary takeaway coffee cup ... the size of a
  normal sixteen-ounce coffee") held the cup in 11/11 rebuilt frames. A Krea baby sheet and a host combo (face +
  Hawaiian-shirt body) held the party; one frame still added a second Hawaiian-shirt man until "the other guests wear
  plain T-shirts ...; he is the only man in a Hawaiian shirt". The user's verdict: "prop consistency ... dramatically
  improved".
- **H3 takes size words literally**: "a giant coffee cup" grew to bucket size mid-shot.
- **Krea spells, Flux garbles.** Flux edits gave "DEPPARTMENT", "E-PR-R-T-MET", "BA ANC", "SALESNDE", "UNEXPCTED".
  Krea plates with the words in quotes spelled "WRONG DEPARTMENT", "DELI", "SALE" and "FOOD MART" right in 16/16. Flux
  multiref frames built on those plates keep short words but repainted "FOOD MART" as "A ART" until the prompt quoted
  the sign and added "its letters exactly as in image 1"; in H3 the DELI neon grew a fifth letter once ("always reads
  exactly DELI, four letters" fixed the re-roll). Where no word is needed, use a symbol (a red warning triangle).

### Renders

- **First pass: 71 renders in ~5.7 h, 70 usable**; the failure was a frame (two of her), not H3. Second pass 33
  re-renders, 31 kept first time.
- **Walk-and-sing toward a camera tracking backward works at 5 s**: every one of ~20 such shots kept her face,
  costume and set while she sang, the background gags playing out behind her.
- **A dance ensemble that moves**: eight dancers (six extras, the owner, the pig) in a line behind her on a "street
  falling apart" plate danced in all six finale shots — a named routine ("step-touch side to side on every beat, hips
  popping, arms snapping out and back"), medium-close framing and a moving camera, per the Act 2 lesson.
- **Timed events land on the render's clock, not the slot's.** A van wipe with the new costume pinned at the last
  frame revealed it at ~5 s of a 3.9 s slot (silent: play from 1.2 s in); the finale's V pose came at ~3 s of a 1.8 s
  lip-synced slot (fix: extend the slot, dropping the next short shot — an offset would break sync).
- **The H3 prompt can reintroduce what the frame removed**: a frame with no newspapers still rendered newspaper
  umbrellas while the prompt said "newspapers over their heads". Change the frame *and* the prompt.
- **Physical-contact failures are easier to stage around than to prompt out**: heads came up through taxi roofs in
  gridlock (moved the drivers out of the cars into a fender bender); an arm passed through a sash window (an open
  shuttered window, the action kept inside the room); a man chasing a truck ran backward toward the camera (shot from
  behind, running away); curtains drawn mid-room (say they hang from a rod over the window; to show them shut, "one
  continuous wall of curtain fabric ... no gap and no glass visible anywhere" — "two panels meeting in the middle"
  left the window open twice).

### Review and edit

- **Three rounds of notes went from structure to polish**: v1 props, a backward runner, a weak finale; v2 jarring
  transitions; the 2x cut, small physical errors that "leap out as errors". Upscaling sharpens them, so a frame-grid
  pass for contact errors (limbs through objects, duplicated people, floating props) is worth doing before the 2x.
- **An inserted wide followed by her in the same angle reads as her popping in**: give each cutaway its own angle.
- **A silent shot with a bad first second can start late** in the edit (o5 from 1.27 s, the render's whole headroom).
- **Waxy, creased skin in a close-up** softened with a single-image edit of the frame ("smooth, even, glowing skin")
  and a re-render; SeedVR2 makes this kind of texture more visible.

### Costs and tooling

- 72 first frames in ~35 min of Flux (masters first, then derived frames, 4 passes); 5-10 frame fixes per round.
- H3: ~4.8 min per 5 s shot at 1120x640, 20 steps.
- Upscale: SeedVR2 2x wavelet ~2.5 min per 4 s shot after the model load, 2 h 45 min for the cut; `face_composite.py`
  17 min. `upscale_shots.py` caches per edit piece, so after a round of fixes only the changed shots re-upscale (5
  shots, ~15 min) and a run cut off by a time limit resumes where it stopped.
- **Stale inputs:** `frames.py` reads masters from ComfyUI/input, so deleting a master's frame in `frames/` is not
  enough — the old `nmp_f_<id>.png` in input lets derived frames build from the old master. Delete both.

## 10. Toolkit

Shared scripts live in `tools/`; the music-video project scripts (`queue_act2.py`,
`assemble_full.py`, `review_act2.py`, `upscale_full.py`) live in `projects/no_fucks_at_all/`.
Paths like `refs/…`, `out/…`, `audio/…` in the sections above are relative to that project folder.
The 5-second-clip workflow (section 15) has its own set in `projects/not_my_pig/`: `shots.py` (shot list as data,
beat-snapped), `frames.py` (Flux first frames: masters, derived angles, fix passes), `make_sets.py`, `make_sheets.py`,
`queue_shots.py` (H3 fl2va per shot, `--seed N` re-rolls), `review_shots.py`, `assemble.py` + `takes.py`,
`upscale_shots.py` (per-shot cached SeedVR2) and `upscale_run.sh`.

| Script | Purpose |
|---|---|
| `build_r2v.py` | single-reference ref2v |
| `build_r2v_multiref.py` | three-reference ref2v (environment + two characters) |
| `build_r2v_video.py` | ref2v with a reference **video** on `ref_video_0` plus one plate |
| `build_v2v_ltx.py` | control-guided video-to-video, LTX 2.3 + IC-LoRA Union Control (`--control-mode estimate\|canny\|pose\|passthrough`) |
| `build_i2v.py` | image-to-video from a start frame |
| `build_plate.py` | Krea 2 text-to-image environment plates |
| `build_replate.py` | Krea 2 reference-guided re-angling of a location |
| `build_flux_multiref.py` | Flux 2 Klein multi-reference composites (start frames) |
| `build_beat_test.py` | t2va with an optional soundtrack pinned by `MiniMaxH3AddGuide` (`--queue` submits) |
| `beats.py` | beat analysis, ranked windows, beat-aligned slices (`.venv_audio`) |
| `beat_sync_score.py` | motion vs beat grid / music onsets, with shift-null p-values |
| `mouth_track.py` | per-frame mouth aperture via mediapipe (`.venv_face`) |
| `lipsync_score.py` | mouth aperture vs isolated vocal RMS, lag scan, shift-null p |
| `build_flux_batch.py` | Flux 2 Klein 9B single-reference edit batch, one output per prompt line |
| `queue_act2.py` | stage audio/refs and queue act 2 shots in ref2va from a spec table |
| `assemble_full.py` | beat-aligned edit list + intercuts, assembles the full video over the song |
| `review_act2.py` | collect the latest render per shot and write a frame grid |
| `build_upscale.py` | SeedVR2 video upscale from the ComfyUI template (`--scale`, `--color wavelet`, `--split`) |
| `face_composite.py` | revert small faces in an upscale to a plain resize (YuNet, feathered, temporally pooled) |
| `upscale_full.py` | segment-at-cuts SeedVR2 upscale of a whole cut, resumable |
| `grade.sh` | low-key cinematic grade pass |

All take `--prompt` as a path to a text file in `prompts/`, print the seed used, and
write a workflow into ComfyUI's workflow directory so it can be opened and tweaked in
the UI.

Model files live under `models/vae`, `models/text_encoders`, `models/diffusion_models`
— 59 GiB total for both `fl2va` and `ref2va` plus the shared VAEs and the
`qwen3vl_32b_minimax_h3_nvfp4_awq` text encoder (NVFP4, wants Blackwell).

---

## Open questions

- Do lyrics in `<d>` tags improve mouth *shapes* even though they add nothing to timing?
- Does AddGuide audio hold lip sync under ref2v with character sheets?
- Is the "one person, not three" hedge on turnaround sheets load-bearing?
- Does minimal identity description beat full enumeration? (CINEDANCE says minimal;
  fal's H3 guide says enumerate; we always enumerated.)
- Does putting identity anchors inside a shot description improve i2v close-ups?
  (Suggestive but confounded with a duration change.)
- Can `attribute_transfer` vs `fully_preserved` on an environment be felt in output?
- Does raising `CreateVideo.bit_depth` above 8 measurably improve heavy grades?
- Untextured/clay geometry vs a true Z-depth pass as the control input — does the
  extra shading information in a clay render help or fight the restyle?
- Does lowering `--ic-strength` below 1.0 trade structural lock for scale freedom
  gradually, or does it just get vague?
- Does a sky-rich anchor rescue Canny on a *night* source too, or was golden hour doing
  the work? (The anchor fixed it at golden hour; the Minerva night case is untested.)
- How far past 10 s does a single first frame hold before the grade wanders?
- Would depth and Canny combined — e.g. edges composited over a depth ramp as one
  control image — get both the surface detail and depth's volume cues?
- Do emissive billboards added in the Unity scene make neon signage persist, as the
  set-dressing mechanism predicts?
- How low can `--ic-strength` go before the geometry lock itself starts slipping?
- Does masking the pose-replaced character over the original locked-off footage give a
  clean composite, recovering the background the skeleton discards?
- Would H3 ref2v hold mascot identity better than a single LTX first frame, given §4's
  result that wardrobe transfers strongly from reference sheets? (It would cost the
  frame-accurate motion.)
- Does a denser pose control — DWPose, or DensePose's body-surface map — track limbs
  more closely than OpenPose without reintroducing the original silhouette?
- Does a Unity depth/normal pass via `passthrough` beat estimating depth from the
  beauty render, now that massing capture is known to work?
- Does feeding H3 both a reference video *and* the depth-locked LTX output as a second
  reference recover scale while keeping geometry?
