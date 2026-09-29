# Third-party files

Everything in this repository is dedicated to the public domain under **CC0 1.0**
(see [LICENSE](LICENSE)) **except** the files below, which are redistributed under their
own licenses. Both are MIT, so they are also free to use, modify and redistribute; just
keep their copyright notices.

| File | Source | License |
|---|---|---|
| `models/face_detection_yunet_2023mar.onnx` | YuNet face detector, [opencv/opencv_zoo](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet) — Copyright (c) 2020 Shiqi Yu | MIT |
| `tools/templates/ltx23_ic_lora_union_control.json` | Modified from the `video_ltx2_3_ic_lora` workflow in [Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates) | MIT |
| `tools/templates/comfyui/*.json` | ComfyUI workflows the builders start from, exported from the local install. Those taken from the ComfyUI template gallery ([Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates)) are MIT; those authored for this project (e.g. `Flux2_K8B_Batch_Prompt.json`) are CC0 like the rest. | MIT / CC0 |

Models used to *generate* the assets (MiniMax H3, Krea 2, Flux 2 Klein, SeedVR2, Demucs,
Whisper) are not included in this repository; they have their own licenses, which apply
to downloading and running them.
