"""Labelled contact sheet of stills.
  python contact.py OUT.jpg [--cols N] [--width W] label=path [label=path ...]
A bare path is labelled with its file stem.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

args = sys.argv[2:]
cols, width = 4, 560
while args and args[0].startswith("--"):
    if args[0] == "--cols": cols = int(args[1])
    if args[0] == "--width": width = int(args[1])
    args = args[2:]
items = [a.split("=", 1) if "=" in a else (os.path.splitext(os.path.basename(a))[0], a) for a in args]
font = ImageFont.truetype("arialbd.ttf", 30)
tiles = []
for label, path in items:
    im = Image.open(path).convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    box = d.textbbox((10, 8), label, font=font)
    d.rectangle((box[0] - 6, box[1] - 4, box[2] + 6, box[3] + 4), fill=(0, 0, 0))
    d.text((10, 8), label, font=font, fill=(255, 230, 0))
    tiles.append(im)
cols = min(cols, len(tiles))
rows = [tiles[i:i + cols] for i in range(0, len(tiles), cols)]
heights = [max(t.height for t in r) for r in rows]
sheet = Image.new("RGB", (cols * width, sum(heights)), (20, 20, 20))
y = 0
for r, h in zip(rows, heights):
    for i, t in enumerate(r):
        sheet.paste(t, (i * width, y))
    y += h
sheet.save(sys.argv[1], quality=90)
print("wrote", sys.argv[1], sheet.size)
