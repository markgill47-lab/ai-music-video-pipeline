---
name: music-video-pipeline
description: Make a music video (or any song-driven video) locally with MiniMax H3 in ComfyUI, from song analysis through characters, sets, lip-synced and beat-synced shots, beat-aligned assembly and SeedVR2 upscaling. Use this whenever the user wants to start or continue a music video, sync video to a song, lip-sync a character to vocals, design recurring characters or sets for video shots, render or re-render shots with H3, assemble a cut against a song, or upscale a finished cut — even if they don't say "pipeline" or name the tools. Also use it for questions about how the No Fucks at All video in this repo was made.
---

# Music video pipeline (MiniMax H3 + ComfyUI)

This repo made *No Fucks at All* (4:01, 1980s public-access-TV style) end to end on one
RTX 5090. The recipe, the scripts and the measurements are all here; your job is to run
the same pipeline for the next song and to avoid re-learning the lessons already paid for.

Read before acting:
- `docs/PIPELINE.md` — the step-by-step recipe with commands. Read it first, every time.
- `docs/FINDINGS.md` — measured results. Consult the relevant section before changing a
  technique; it records what failed as well as what worked.
- `projects/no_fucks_at_all/` — a complete worked example: `SHOTLIST.md`, the spec table
  in `queue_act2.py`, the edit list in `assemble_full.py`, prompt generators in
  `prompts/shots/`.
- `projects/not_my_pig/` — the 5-second-clip variant (PIPELINE.md, "Variant"): `shots.py` →
  `frames.py` → `queue_shots.py` → `assemble.py`/`takes.py` → `upscale_run.sh`. The better
  starting point for a vignette video with a recurring cast.

## Layout and conventions

- Shared scripts: `tools/`. One folder per video: `projects/<name>/` holding its song,
  `audio/`, `refs/`, `prompts/`, `out/`, `frames/`, `SHOTLIST.md` and project scripts.
  Start a new video by creating a new project folder; copy and adapt the No Fucks at All
  project scripts rather than editing them.
- Run project scripts from inside the project folder (paths like `refs/…` are relative to it).
- Two venvs at the repo root: `.venv_audio` (librosa, demucs, faster-whisper, torch) and
  `.venv_face` (mediapipe 0.10.21, OpenCV — needs numpy<2, so it cannot share a venv).
  ComfyUI's own venv runs the `build_*` builders.
- ComfyUI serves on `http://127.0.0.1:8188`. Free VRAM (`POST /free`) before switching
  between H3, Flux/Krea and SeedVR2; leftover models cause OOMs.
- Renders are long (about 2 minutes per second of video). Queue batches and let them run;
  poll job status rather than holding a wait open for over 30 minutes.

## The pipeline in brief

1. **Song** — beats (`tools/beats.py`), Demucs stems, word-level Whisper lyrics on the
   isolated vocal. Everything downstream is timed from these.
2. **Shot list** — boundaries snapped to beats; each render 5–15.08 s. Decide per shot
   whether anyone sings: pin the full mix for singing, the instrumental stem for silent
   vignettes (otherwise whoever is on screen mouths the lyrics).
3. **Characters** — face in Krea 2 → angles and expressions in Flux 2 Klein 9B
   (camera-move phrasing) → costume sheet in Krea 2 → body-over-face combo reference.
4. **Sets and props** — Krea plates; props get their own reference and `<Subject>`.
5. **First frames** — Flux multi-reference; repair one character by masked composite.
6. **Shots** — H3 ref2va with the song slice pinned by `MiniMaxH3AddGuide`; pin the set
   (and the end frame of any camera move) to stop drift. `tools/build_beat_test.py`.
7. **Review** — frame grids; lip sync and beat scores in `tools/`.
8. **Assemble** — beat-aligned edit list, song laid under; lip-synced pieces stay
   song-aligned.
9. **Upscale** — SeedVR2 2x + wavelet colour, segmented at cuts; then
   `tools/face_composite.py` to stop small faces turning into caricatures.

## Lessons that are expensive to rediscover

- Lip sync and beat timing come from the **pinned audio**, not from lyrics in the prompt.
- Describe what you want, never what you don't: naming an unwanted thing summons it.
- Many reference sheets make H3 cut to the sheets themselves on a grey backdrop — pin a
  set frame at frame 0.
- Big group dances from a wide static camera barely move; go closer and move the camera.
- A targeted repaint bleeds identity onto the most prominent face; composite the region back.
- SeedVR2 `denoise` < 1 does not mean "gentler" — it switches restoration off.
- Once a frame is liked, derive every other angle and fix **by editing it**; regenerating drifts
  character, costume and set. But build shots *without* the singer from the empty plate, or she
  takes over the action.
- Props held or carried across shots need their own reference sheet (or a body sheet edited to
  hold them); prompts alone give a different cup, baby or host every time.
- Words on signs and screens: make them Krea plates (it spells); Flux edits garble text.
- A colour or look rule in a shared prompt string leaks into every shot that carries it.
- Contact errors (limbs through frames, heads through roofs, duplicated people) are easier
  to stage around than to prompt out; catch them before the 2x upscale.

## Working with the user

The user directs the creative choices (story, look, casting, which take to keep). Show
contact sheets and short clips rather than describing them, pick a recommendation when
offering options, and confirm before downloads, anything that spends API credits
(partner nodes under `partner/`), or publishing. Record new measured results in
`docs/FINDINGS.md` and new shots in the project's `SHOTLIST.md` as you go.
