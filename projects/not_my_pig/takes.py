"""Which render plays for each shot, and from what offset (seconds). Default is out/<id>.mp4 from 0."""
TAKES = {
    "k5": ("out/k5_r2.mp4", 1.2),     # the van wipe reveals the dress at ~5 s; start late so it lands in the slot (silent shot)
    "f3": ("out/f3_r3.mp4", 0.0),     # r2: the DELI sign grew a letter
}
# v2: the user's notes on rough cut v1 (one cup, one host and baby, the umbrella in her hand, the hallway, the garbage
# chase, curtains, Krea signs, the new finale on her street)
for _s in ("i04", "i06", "i07", "v1a", "v1c", "v1e", "p1b", "p1c", "p1d", "c1a", "c1c", "k3", "k1", "k7", "b1", "b2", "b3",
           "b5", "o5", "c2b", "c2c", "c2f", "d1", "d2", "d3", "d4", "f1", "f2", "f4", "f5", "f6"):
    TAKES[_s] = (f"out/{_s}_r2.mp4", 0.0)
# v3: the user's notes on rough cut v2 (transitions)
TAKES["o5"] = ("out/o5_r2.mp4", 1.27)     # start after she has dropped the curtain panel (silent shot; the whole headroom)
for _s in ("p1a", "q1", "q4", "c2b", "b2"):
    TAKES[_s] = (f"out/{_s}_r3.mp4", 0.0)
TAKES["c1f"] = ("out/c1f_r4.mp4", 0.0)    # r3: the newspapers came back from the H3 prompt
# v4: the user's notes on the 2x cut
for _s in ("i02", "p1d", "c1a", "b6", "o6"):
    TAKES[_s] = (f"out/{_s}_r5.mp4", 0.0)
