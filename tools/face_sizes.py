"""Largest detected face width (pixels, at source resolution) per EDL piece of a cut.
Runs in .venv_face (mediapipe). Samples 5 frames per piece; writes out/face_sizes.json
as [song_start, song_end, clip, median_largest_face_px or null].
  .venv_face/Scripts/python.exe face_sizes.py out/rough_cut_v5.mp4 pieces.json
pieces.json is a dump of assemble_full.edl() (made by the caller, since this venv lacks librosa).
"""
import json, sys
import cv2
import numpy as np
import mediapipe as mp

src, pieces = sys.argv[1], json.load(open(sys.argv[2]))
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
det = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.4)
out = []
for clip, s, t, _ in pieces:
    widths = []
    for k in range(5):
        f = int((s + (t - s) * (k + 0.5) / 5) * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, f)
        ok, img = cap.read()
        if not ok:
            continue
        r = det.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if r.detections:
            widths.append(max(d.location_data.relative_bounding_box.width for d in r.detections) * img.shape[1])
    med = float(np.median(widths)) if widths else None
    out.append([s, t, clip.split("/")[-1], med])
    print(f"{s:7.2f}-{t:7.2f}  {clip.split('/')[-1]:26s} {'-' if med is None else round(med)}")
json.dump(out, open("out/face_sizes.json", "w"), indent=0)
