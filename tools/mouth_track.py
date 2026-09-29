"""Per-frame mouth aperture from a video, for lip-sync scoring. Runs in .venv_face
(mediapipe 0.10.21 needs numpy<2, which librosa in .venv_audio cannot share).

aperture = inner-lip gap (landmarks 13-14) / outer eye-corner distance (33-263),
so it is independent of face size. Frames with no face are written as null.

  .venv_face/Scripts/python.exe mouth_track.py out/clip.mp4   -> out/clip.mouth.json
"""
import json, sys
import cv2
import numpy as np
import mediapipe as mp


def track(path):
    cap = cv2.VideoCapture(path)
    mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1,
                                           refine_landmarks=True, min_detection_confidence=0.5)
    out = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        r = mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if not r.multi_face_landmarks:
            out.append(None)
            continue
        lm = r.multi_face_landmarks[0].landmark
        p = lambda i: np.array([lm[i].x * frame.shape[1], lm[i].y * frame.shape[0]])
        out.append(float(np.linalg.norm(p(13) - p(14)) / np.linalg.norm(p(33) - p(263))))
    return out


if __name__ == "__main__":
    for v in sys.argv[1:]:
        a = track(v)
        dst = v.rsplit(".", 1)[0] + ".mouth.json"
        json.dump(a, open(dst, "w"))
        found = sum(x is not None for x in a)
        print(f"{v}: face in {found}/{len(a)} frames -> {dst}")
