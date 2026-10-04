#!/bin/sh
# 2x SeedVR2 per shot, then the small-face fix, then put the song back on (face_composite writes no audio).
set -e
cd "$(dirname "$0")"
../../.venv_audio/Scripts/python.exe upscale_shots.py out/rough_cut_v4.mp4 out/rough_cut_v4_2x.mp4
../../.venv_face/Scripts/python.exe ../../tools/face_composite.py out/rough_cut_v4.mp4 out/rough_cut_v4_2x.mp4 out/v4_2x_faces_noaudio.mp4
ffmpeg -v error -y -i out/v4_2x_faces_noaudio.mp4 -i out/rough_cut_v4_2x.mp4 -map 0:v -map 1:a -c copy out/not_my_pig_v4_2x.mp4
echo done
