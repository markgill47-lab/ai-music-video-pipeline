# Project instructions

This folder is the **public** repo `markgill47-lab/ai-music-video-pipeline`, a local
music-video pipeline built on MiniMax H3 in ComfyUI. Finished and published: *No Fucks at All*
(karnivore23, release v1.0) and *Not my Pig, Not my Farm* (release not-my-pig-v1.0). More videos
will be made here, one per folder under `projects/`.

## Read first

- `docs/PIPELINE.md` — the step-by-step recipe. Follow it for a new video.
- `docs/FINDINGS.md` — measured results. Check the relevant section before re-testing
  anything; it records what failed as well as what worked.
- The `music-video-pipeline` skill (`.claude/skills/`) summarises the workflow and the
  lessons that were expensive to learn.
- `projects/no_fucks_at_all/` — the first worked example: band, ref2va, long shots.
- `projects/not_my_pig/` — the second, and the better template for a vignette video: 71 five-second
  fl2va shots from Flux first frames, one designed singer in six costumes, prop sheets, Krea sign
  plates, three review rounds recorded as fix passes at the end of `frames.py`. See FINDINGS §15.
- `projects/life_in_2045/` — the concept album *Life in 2045*. `shared/refs/` holds the recurring family
  (Steve, Zach, Nicole, Alec: face masters, face sheets, body sheets, combos); `grounded/` is track 1,
  finished (no singer, instrumental pinned on every shot; `queue_shots.py` uses beat-index slots,
  `assemble.py` picks takes, `upscale_shots.py` caches per shot). The album mp3s and synopsis live in
  `album/`, gitignored. The Grounded video is kept local, not released.

## Starting a new video

1. `projects/<snake_case_name>/` with `audio/`, `refs/`, `prompts/`, `out/`, `frames/`
   and a `SHOTLIST.md`. Put a copy of the song in `audio/`.
2. Copy the scripts from `projects/not_my_pig/` (`shots.py`, `frames.py`, `make_sets.py`,
   `make_sheets.py`, `queue_shots.py`, `review_shots.py`, `assemble.py`, `takes.py`,
   `upscale_shots.py`, `upscale_run.sh`, `contact.py`, `comfyq.py`, `waitn.py`) and replace the
   project data: the shot table, the frame specs, the prompts. For band/ref2va work, start from
   `projects/no_fucks_at_all/` instead. Do not edit the originals; they document finished videos.
3. Follow `docs/PIPELINE.md`: song analysis, shot list on the beat grid, characters
   (face → Flux angles → Krea costume → combo sheet), sets and props, first frames, H3
   renders, review, assembly, upscale, small-face fix.
4. Add new measured results to `docs/FINDINGS.md` as you go.

## Environment (this machine)

- ComfyUI: `D:\Projects_26\Comfyu\ComfyUI`, venv inside it, serves on
  `http://127.0.0.1:8188`; the `comfy` MCP server is configured in `.mcp.json`.
  RTX 5090 32 GB, 64 GB RAM, Windows 11.
- The `tools/build_*.py` builders read workflow templates from ComfyUI's
  `user/default/workflows/` by absolute path; copies are in `tools/templates/comfyui/`.
  Run builders with ComfyUI's venv python.
- `.venv_audio` (librosa, demucs, faster-whisper, CUDA torch) and `.venv_face`
  (mediapipe 0.10.21 + OpenCV 4.11, numpy<2) at the repo root; not committed. Recreate
  per `docs/PIPELINE.md` §0 if missing.
- Run project scripts from inside their project folder.
- ffmpeg is on PATH (winget build).

## Operating notes

- Renders take ~2 min per second of video (H3, 1120x640, 20 steps). Queue batches with
  `wait=False` and poll `job status`; the comfy MCP `job wait` aborts after 30 min of silence.
- Free VRAM (`POST /free`) before switching between H3, Flux/Krea and SeedVR2.
- Partner nodes under `partner/…` spend API credits; the local H3 nodes are under
  `model/conditioning/minimax`. Never use partner nodes without asking.
- Downloads (models, detectors) need the user's OK first: name the file, source and size.
- Review work visually: contact sheets of stills, frame grids of renders, short clips.
  Recommend one option when offering choices.
- When the user likes a reference or first frame, make further angles/takes/fixes as Flux
  **edits of that frame**, not regenerations. Recurring props get their own reference sheet.
  Text on signs/screens: Krea plates, not Flux edits.
- Background tasks stop at 2 h: run the upscale in chunks (it resumes from its per-shot cache).
- Before upscaling, check the grids for contact errors (limbs through objects, duplicated
  people, floating props); the 2x makes them leap out and the user will catch them.

## Publishing

- Everything committed is public. Before pushing, check `git status` and scan new text
  files for secrets or personal info. Credit the artist as **karnivore23** only.
- Git identity is set repo-locally to the GitHub no-reply address; don't change it.
- Rendered video is gitignored (`*.mp4`); publish finished videos, shot renders and
  experiment clips as **GitHub Release** assets (up to 2 GB each).
- License: **CC0 1.0** for everything we create (code, docs, prompts, images, audio,
  video). Third-party files go in `THIRD_PARTY_NOTICES.md`.
- `projects/earlier_tests/` holds pre-music-video experiments; it is gitignored and stays local.
