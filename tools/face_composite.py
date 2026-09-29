"""Put small faces back to a plain resize inside a SeedVR2 upscale.

SeedVR2 turns faces that were only a few pixels wide into crisp, wrong caricatures.
Per frame, YuNet finds faces in the SOURCE; each face narrower than --full px (source
pixels) is fully replaced by the Lanczos-resized source, fading to untouched by --none px.
Masks are feathered ellipses around the head, max-pooled over +-3 frames so a detector
dropout for a frame or two does not make a face pop sharp and back.
Runs in .venv_face (OpenCV 4.11 has FaceDetectorYN).

  .venv_face/Scripts/python.exe face_composite.py SRC UPSCALED OUT [--start F --count N] [--debug]
SRC and UPSCALED must be the same cut, frame for frame.
"""
import argparse, os, subprocess
from collections import deque
import cv2
import numpy as np

MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "face_detection_yunet_2023mar.onnx")


def frames(path, w, h, start, count):
    vf = f"select='gte(n\\,{start})',setpts=N/24/TB" if start else "null"
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "bgr24"]
    if count:
        cmd += ["-frames:v", str(count)]
    p = subprocess.Popen(cmd + ["-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)


def size(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return tuple(int(v) for v in out.strip().split(","))


def face_mask(faces, sw, sh, W, H, full, none):
    m = np.zeros((H, W), np.float32)
    s = W / sw
    for x, y, fw, fh in faces:
        wgt = float(np.clip((none - fw) / (none - full), 0, 1))
        if wgt <= 0:
            continue
        cx, cy = (x + fw / 2) * s, (y + fh / 2) * s
        # head + hair: wider and taller than the detector box
        ax, ay = fw * s * 0.95, fh * s * 1.15
        cv2.ellipse(m, (int(cx), int(cy - fh * s * 0.1)), (int(ax), int(ay)), 0, 0, 360, wgt, -1)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("up"); ap.add_argument("out")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--count", type=int, default=0)
    ap.add_argument("--full", type=float, default=40, help="faces narrower than this (source px) fully reverted")
    ap.add_argument("--none", type=float, default=80, help="faces this wide or wider are left as upscaled")
    ap.add_argument("--crf", type=int, default=10)
    ap.add_argument("--debug", action="store_true", help="tint the mask red to check coverage")
    a = ap.parse_args()

    sw, sh = size(a.src); W, H = size(a.up)
    det = cv2.FaceDetectorYN.create(MODEL, "", (sw, sh), 0.5, 0.3, 5000)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", "24", "-i", "-", "-c:v", "libx264", "-crf", str(a.crf), "-preset", "slow",
                            "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
    K = 3                                   # temporal max-pool radius
    buf = deque()                           # (up_frame, src_frame, faces)
    feather = int(W / 120) | 1
    n = hits = 0

    def emit(i):
        up, src, _ = buf[i]
        m = np.zeros((H, W), np.float32)
        for _, _, f in buf:
            m = np.maximum(m, face_mask(f, sw, sh, W, H, a.full, a.none))
        if m.any():
            m = cv2.GaussianBlur(m, (0, 0), feather)[..., None]
            soft = cv2.resize(src, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
            out = up.astype(np.float32) * (1 - m) + soft * m
            if a.debug:
                out[..., 2] = np.maximum(out[..., 2], m[..., 0] * 255)
            return out.clip(0, 255).astype(np.uint8)
        return up

    for up, src in zip(frames(a.up, W, H, a.start, a.count), frames(a.src, sw, sh, a.start, a.count)):
        _, f = det.detect(src)
        faces = [] if f is None else [tuple(r[:4]) for r in f]
        hits += bool(faces)
        buf.append((up, src, faces))
        if len(buf) > 2 * K + 1:
            buf.popleft()
        if len(buf) == 2 * K + 1:
            for i in (range(K + 1) if n == 0 else [K]):   # first full window also emits the head frames
                enc.stdin.write(emit(i).tobytes()); n += 1
    # tail: frames after the last emitted centre (or all of them if the clip was shorter than a window)
    for i in range(K + 1 if n else 0, len(buf)):
        enc.stdin.write(emit(i).tobytes()); n += 1
    enc.stdin.close(); enc.wait()
    print(f"wrote {a.out}: {n} frames, faces found in {hits}")


if __name__ == "__main__":
    main()
