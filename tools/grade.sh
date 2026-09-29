#!/usr/bin/env bash
# Apply a low-key cinematic grade to an H3 clip.
#   usage: grade.sh <in.mp4> <out.mp4> [strength: medium|heavy]
set -euo pipefail

FF="C:/Users/karni/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin/ffmpeg.EXE"
IN="$1"; OUT="$2"; STRENGTH="${3:-medium}"

if [ "$STRENGTH" = "heavy" ]; then
  CURVE="0/0 0.30/0.045 0.55/0.30 0.78/0.66 1/0.97"
  EQ="contrast=1.40:brightness=-0.10:saturation=0.80"
  CB="rs=-0.08:gs=-0.03:bs=0.14:rh=0.10:gh=0.03:bh=-0.08"
  VIG="PI/3.6"
else
  CURVE="0/0 0.25/0.085 0.50/0.36 0.75/0.71 1/1"
  EQ="contrast=1.22:brightness=-0.06:saturation=0.88"
  CB="rs=-0.05:gs=-0.02:bs=0.09:rh=0.07:gh=0.02:bh=-0.05"
  VIG="PI/4.6"
fi

"$FF" -v error -y -i "$IN" \
  -vf "curves=m='${CURVE}',eq=${EQ},colorbalance=${CB},vignette=${VIG}" \
  -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -c:a copy "$OUT"

echo "graded [$STRENGTH]: $OUT"
