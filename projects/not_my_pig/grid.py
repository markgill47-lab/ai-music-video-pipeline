"""Frame grid of a render for review, plus mean luma per sampled frame.
  python grid.py CLIP.mp4 OUT.jpg [n_frames] [crop x0,y0,x1,y1 as fractions]
"""
import subprocess, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

clip, out = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
crop = [float(v) for v in sys.argv[4].split(",")] if len(sys.argv) > 4 else None
info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
        "-show_entries", "stream=width,height,nb_read_packets", "-of", "json", clip]))["streams"][0]
w, h, total = info["width"], info["height"], int(info["nb_read_packets"])
raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", clip, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
frames = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
idx = [round(i * (len(frames) - 1) / (n - 1)) for i in range(n)]
font = ImageFont.truetype("arialbd.ttf", 26)
tiles = []
for i in idx:
    im = Image.fromarray(frames[i])
    luma = float(np.asarray(im.convert("L")).mean())
    if crop:
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    im = im.resize((560, round(im.height * 560 / im.width)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 250, 34), fill=(0, 0, 0))
    d.text((6, 2), f"f{i} {i / 24:.2f}s L{luma:.0f}", font=font, fill=(255, 230, 0))
    tiles.append(im)
cols = 4
rows = (len(tiles) + cols - 1) // cols
th = tiles[0].height
sheet = Image.new("RGB", (cols * 560, rows * th))
for k, t in enumerate(tiles):
    sheet.paste(t, ((k % cols) * 560, (k // cols) * th))
sheet.save(out, quality=90)
print("wrote", out, f"{len(frames)} frames", "luma first/last:", tiles and f"{np.asarray(Image.fromarray(frames[0]).convert('L')).mean():.1f} / {np.asarray(Image.fromarray(frames[-1]).convert('L')).mean():.1f}")
