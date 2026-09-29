# AI music video pipeline

A local, open-model pipeline for making music videos: characters, sets, lip-synced and
beat-synced performance, vignettes, edit and upscale, all driven by the song. Built and
measured while making **[No Fucks at All](projects/no_fucks_at_all/)** by karnivore23, a
4-minute 1980s public-access-TV music video rendered on a single RTX 5090.

▶ **Watch it:** see the [latest release](../../releases/latest) for the finished video
(2240×1280, upscaled), the 1120×640 edit and every rendered shot.

| | |
|---|---|
| Video | MiniMax H3 (fl2va + ref2va) in ComfyUI, song slices pinned with `MiniMaxH3AddGuide` |
| Stills | Krea 2 (faces, costumes, sets), Flux 2 Klein 9B (angles, expressions, compositing) |
| Audio | librosa beats, Demucs stems, faster-whisper word timings |
| Upscale | SeedVR2 3B int8 at 2x with wavelet colour, plus a small-face fix (YuNet) |

## Start here

- **[docs/PIPELINE.md](docs/PIPELINE.md)** — the recipe, step by step, with commands.
- **[docs/FINDINGS.md](docs/FINDINGS.md)** — what was measured: prompt format, lip sync and
  beat sync tests, character consistency, failure modes and fixes, render costs, upscaling.
- **[.claude/skills/music-video-pipeline/](.claude/skills/music-video-pipeline/SKILL.md)** —
  a Claude Code skill that packages the workflow; it loads automatically when Claude Code
  runs in this repo.

## Layout

```
docs/                    PIPELINE.md, FINDINGS.md
tools/                   shared scripts: ComfyUI workflow builders, beat/lip-sync
                         scoring, SeedVR2 upscale, small-face fix
  templates/comfyui/     the ComfyUI workflows the builders start from
models/                  YuNet face detector (OpenCV zoo)
projects/
  no_fucks_at_all/       the first video
    SHOTLIST.md          every shot, its song time, lyric and render notes
    audio/               the song, Demucs stems, beat grid, word timings, per-shot slices
    refs/                character face/body sheets, sets, props, audience, crew
    prompts/             every prompt, plus the generators in prompts/shots/
    frames/              review grids and comparisons
    out/                 analysis outputs (renders are in the release)
    queue_act2.py        spec table -> slices audio, stages refs, queues H3 renders
    assemble_full.py     beat-aligned edit decision list -> full cut over the song
    upscale_full.py      segmented SeedVR2 upscale of a finished cut
```

Each new video goes in its own `projects/<name>/` folder.

## Requirements

ComfyUI with MiniMax H3, Krea 2, Flux 2 Klein and SeedVR2 models (the H3 checkpoints and
text encoder are ~59 GB); Python venvs described in [PIPELINE.md](docs/PIPELINE.md#0-setup).
The builders reference a local ComfyUI install at `D:\Projects_26\Comfyu\ComfyUI` and
templates from the ComfyUI gallery by name; adjust the paths for your machine.

## License

**Public domain — [CC0 1.0](LICENSE).** Code, docs, prompts, reference images, the song,
its stems and the finished video are all free to use, modify and redistribute for any
purpose, commercial or not, with no attribution required. Two third-party files (a face
detector model and a workflow template) are MIT-licensed; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Credits

Song, lyrics and creative direction: karnivore23. Pipeline and tooling built
in collaboration with Claude (Anthropic) in Claude Code.
