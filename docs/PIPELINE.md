# Making a music video with MiniMax H3 — the pipeline

This is the process that produced *No Fucks at All* (karnivore23, 4:01): a 1980s
public-access-TV music video with a band, vignettes, lip-synced singing and dancing,
rendered entirely locally. The measurements behind every recommendation are in
[FINDINGS.md](FINDINGS.md); this document is the recipe.

**Stack:** ComfyUI with MiniMax H3 (fl2va + ref2va checkpoints) for video, Krea 2 and
Flux 2 Klein 9B for stills, SeedVR2 3B for upscaling. Python helpers in `tools/`.
Everything ran on one RTX 5090 (32 GB).

```
song ─▶ beats + lyrics ─▶ shot list ─▶ characters, sets, props ─▶ first frames
     ─▶ H3 renders (song slice pinned) ─▶ review / redo ─▶ beat-aligned assembly
     ─▶ SeedVR2 2x upscale ─▶ small-face fix ─▶ final
```

---

## 0. Setup

- ComfyUI with the MiniMax H3 nodes (`MiniMaxH3ImageToVideo`, `MiniMaxH3ReferenceToVideo`,
  `MiniMaxH3AddGuide`), Krea 2 and Flux 2 Klein templates, and the SeedVR2 3B int8 models
  (`seedvr2_3b_int8_convrot`, `seedvr2_ema_vae_fp16`).
- Two Python venvs at the repo root, because mediapipe needs numpy<2 and librosa needs numpy>=2:
  - `.venv_audio`: `librosa soundfile matplotlib demucs faster-whisper` + CUDA torch
  - `.venv_face`: `mediapipe==0.10.21 opencv-python-headless<4.11`
- `models/face_detection_yunet_2023mar.onnx` (OpenCV zoo, for the small-face fix).
- The `tools/build_*.py` scripts write workflows into ComfyUI's
  `user/default/workflows/`, where they open in the UI; builders that take `--queue`
  also submit to `http://127.0.0.1:8188`. Template paths inside them point at a local
  ComfyUI install — adjust for yours.

Each video is a folder under `projects/`; run project scripts from inside it.

## 1. Analyse the song

```bash
python ../../tools/beats.py analyse "audio/song.mp3"          # tempo, beat grid, ranked windows
python -m demucs --two-stems vocals -n htdemucs -o audio/stems "audio/song.mp3"
```
Then word-level lyrics with faster-whisper large-v3 on the **isolated vocal** (it misses
lines on the full mix; transcribing in overlapping windows recovers more). Keep the
result as JSON: every shot boundary and every `<d>` timestamp comes from it.

## 2. Shot list on the beat grid

Write `SHOTLIST.md`: one row per shot with song time, lyric, set and picture. Snap every
boundary to a detected beat. Constraints:

- H3 renders **5 to 15.08 s** (max 362 frames). Split longer shots into two renders,
  ideally two angles you can intercut on the beat.
- Shorter than 5 s: render 5 s and trim.
- Decide per shot who sings: pin the **full mix** where someone lip-syncs, the
  **instrumental stem** where nobody should (otherwise whoever is on screen mouths the lyrics).

## 3. Characters (the face-first pipeline)

1. **Face close-up in Krea 2** until the face is right. Krea smooths faces toward
   handsome/neutral; lead with an expression and "eccentric character actor" for odd
   features (it ages them — accept it or age down in Flux).
2. **Angles and expressions in Flux 2 Klein 9B** from that one face
   (`tools/build_flux_batch.py`, 4-6 steps, one output per prompt line). Phrase angles as
   camera moves: *"Rotate the camera 90 degrees to the right, show the man in profile."*
   Assemble 8 views into a face sheet.
3. **Full-body costume sheet in Krea 2**, guided by the face sheet (`tools/build_replate.py`).
4. For H3, stack body sheet over face sheet into one **combo reference** per character:
   the face sheet carries identity, the body sheet carries costume.

Costume changes: Flux-edit the existing body sheet (hat off, suit on) rather than
regenerating from the face sheet.

## 4. Sets and props

- Sets: Krea 2 plates of each set as a studio flat, with studio edges visible
  (`tools/build_plate.py`). Carry locations with images, never prose.
- Props: their own reference image and their own `<Subject>` with `fully_preserved`.
  Text props work (a gold extruded "FUCK" stayed legible) if the word is quoted in the
  retention line. State scale explicitly ("fits in the palm of his hand").

## 5. First frames (Flux multi-reference)

`tools/build_flux_multiref.py`: set + one combo sheet per character. Three people in one
pass: the most prominent two hold, the smallest one slips. Fix it with a targeted
repaint and **composite only that region back** — a repaint bleeds the fixed identity onto
the most prominent face. Fix small colour errors by hue mask rather than regenerating.

## 6. Render the shots in H3

`tools/build_beat_test.py` builds the graph (API format, `--queue` submits). The
production recipe is **ref2va**:

- refs: character combo sheets + set plate (+ props), `ref_image_size=max`
- `MiniMaxH3AddGuide`: the song slice pinned at frame 0 (lip sync and beat timing come
  from this, not from lyrics in the prompt), plus a first frame pinned at frame 0 where
  composition matters
- the six-field ref2v prompt; see `projects/no_fucks_at_all/prompts/shots/make_prompts*.py`
  for shared subject blocks so every shot describes each character identically
- 1120x640, 20 steps; ~2 min of render per second of video

Project batch: `queue_act2.py` holds a spec table (slot start, length, stem, refs,
guide frames) and slices audio, stages inputs and queues everything.

**Failure modes and fixes**

| Symptom | Fix |
|---|---|
| Opens on / cuts to a reference sheet on grey | pin a frame of the set at frame 0 with AddGuide |
| Tracking shot loses the set mid-move | pin both ends: AddGuide at frame 0 and at frame -1 (`guide_end`) |
| Crowd dance barely moves | closer angle + moving camera, named routine ("kicks a leg high on every beat") |
| Camera passes behind a flat and goes black | cut the dark frames in the edit |
| Brief glitch (extra prop, grey flash) | trim around it in the edit |

## 7. Review

`review_act2.py` collects the latest render per shot and writes an 8-frame grid.
Objective checks in `tools/`: `beat_sync_score.py` (motion vs beats), `mouth_track.py`
+ `lipsync_score.py` (mouth aperture vs isolated vocal; crop and enlarge small faces
first, and judge clips under ~8 s by eye). Agreement between the mouth traces of
different renders of the same slice is the strongest evidence that the pinned audio is
driving the mouth.

## 8. Assemble

`assemble_full.py` is an edit decision list: each piece is
`(clip, song_start, song_end, source_offset)`, cut on the beat grid, the song laid
under the whole thing. Rules:

- Lip-synced pieces play from their song-aligned offset (`song_start - slot_start`).
- Silent intercuts may resume each take on its own clock.
- Skip opening frames where a render shows a reference sheet (`source_offset > 0`).

## 9. Upscale

1. `upscale_full.py CUT.mp4 OUT.mp4` — SeedVR2 3B int8 at **2x** with **wavelet** colour
   correction, split into segments at the edit's own cuts (seams are invisible, resumable).
   ~11 min per 15 s on a 5090; free VRAM first.
2. `tools/face_composite.py SRC UPSCALED OUT` — SeedVR2 turns faces a few dozen pixels
   wide into crisp caricatures. This reverts faces under 40 px (source) to a plain resize,
   fading out by 80 px, and keeps everything else sharp. ~17 min for 4 minutes.
3. For 4K, resize the 2x result at export. Native 4K SeedVR2 is 3x slower and painterly.

---

## Budget (No Fucks at All)

| | |
|---|---|
| Shots rendered | ~35 incl. redos, 1120x640, 5-15 s each |
| H3 render time | ~15 h total, unattended |
| Stills | a few hundred Krea/Flux images, 25-70 s per batch |
| Upscale | 3 h (2x) + 17 min face fix |
