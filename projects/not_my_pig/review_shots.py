"""Review sheets of renders: one row of frames per clip, six clips per sheet.
  python review_shots.py NAME clip [clip ...]     # clips are ids (out/<id>.mp4) or take names (c1a_r1)
Each frame is labelled with its time; the row label carries the mean luma of the first and last frame.
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

TW, TH, N = 336, 192, 6


def frames(clip):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", clip, "-vf", f"scale={TW}:{TH}", "-f", "rawvideo",
                                   "-pix_fmt", "rgb24", "-"])
    return np.frombuffer(raw, np.uint8).reshape(-1, TH, TW, 3)


def sheet(name, ids):
    font = ImageFont.truetype("arialbd.ttf", 18)
    os.makedirs("out/review", exist_ok=True)
    for page in range(0, len(ids), 6):
        chunk = ids[page:page + 6]
        im = Image.new("RGB", (TW * N, TH * len(chunk)), (20, 20, 20))
        d = ImageDraw.Draw(im)
        for r, sid in enumerate(chunk):
            clip = f"out/{sid}.mp4"
            if not os.path.exists(clip):
                d.text((8, r * TH + 8), f"{sid}: no render", font=font, fill=(255, 80, 80)); continue
            fs = frames(clip)
            idx = [round(i * (len(fs) - 1) / (N - 1)) for i in range(N)]
            for c, i in enumerate(idx):
                im.paste(Image.fromarray(fs[i]), (c * TW, r * TH))
                label = f"{i / 24:.1f}s" if c else f"{sid}  L{fs[0].mean():.0f}>{fs[-1].mean():.0f}"
                box = d.textbbox((c * TW + 4, r * TH + 2), label, font=font)
                d.rectangle((box[0] - 3, box[1] - 2, box[2] + 3, box[3] + 2), fill=(0, 0, 0))
                d.text((c * TW + 4, r * TH + 2), label, font=font, fill=(255, 230, 0))
        out = f"out/review/{name}_{page // 6 + 1:02d}.jpg"
        im.save(out, quality=88)
        print("wrote", out)


if __name__ == "__main__":
    sheet(sys.argv[1], sys.argv[2:])
