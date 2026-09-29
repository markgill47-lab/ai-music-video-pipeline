# Project instructions

This folder is the **public** repo `markgill47-lab/ai-music-video-pipeline`, a local
music-video pipeline built on MiniMax H3 in ComfyUI. The first video, *No Fucks at All*
(karnivore23), is finished and published as release v1.0. More videos will be made here,
one per folder under `projects/`.

## Read first

- `docs/PIPELINE.md` — the step-by-step recipe. Follow it for a new video.
- `docs/FINDINGS.md` — measured results. Check the relevant section before re-testing
  anything; it records what failed as well as what worked.
- The `music-video-pipeline` skill (`.claude/skills/`) summarises the workflow and the
  lessons that were expensive to learn.
- `projects/no_fucks_at_all/` — the complete worked example to copy from.

## Starting a new video

1. `projects/<snake_case_name>/` with `audio/`, `refs/`, `prompts/`, `out/`, `frames/`
   and a `SHOTLIST.md`. Put a copy of the song in `audio/`.
2. Copy `queue_act2.py`, `assemble_full.py`, `review_act2.py`, `upscale_full.py` and
   `prompts/shots/make_prompts*.py` from `projects/no_fucks_at_all/` and adapt them: the
   `SPECS` table, the edit list, the shared subject blocks. Do not edit the originals;
   they document the finished video.
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

## Publishing

- Everything committed is public. Before pushing, check `git status` and scan new text
  files for secrets or personal info. Credit the artist as **karnivore23** only.
- Git identity is set repo-locally to the GitHub no-reply address; don't change it.
- Rendered video is gitignored (`*.mp4`); publish finished videos, shot renders and
  experiment clips as **GitHub Release** assets (up to 2 GB each).
- License: **CC0 1.0** for everything we create (code, docs, prompts, images, audio,
  video). Third-party files go in `THIRD_PARTY_NOTICES.md`.
- `projects/earlier_tests/` holds pre-music-video experiments; it is gitignored and stays local.
