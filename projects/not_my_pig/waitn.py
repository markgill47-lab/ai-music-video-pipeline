"""Block until N H3 renders exist in ComfyUI/output/video (or the queue empties), then print the count.
  python waitn.py N [max_minutes]"""
import glob, json, sys, time, urllib.request
n = int(sys.argv[1]); limit = float(sys.argv[2]) * 60 if len(sys.argv) > 2 else 6 * 3600
t0 = time.time()
def count():
    return len(glob.glob(r"D:\Projects_26\Comfyu\ComfyUI\output\video\H3_nmp_*_00001_.mp4"))
def pending():
    q = json.load(urllib.request.urlopen("http://127.0.0.1:8188/queue"))
    return len(q["queue_running"]) + len(q["queue_pending"])
while count() < n and pending() and time.time() - t0 < limit:
    time.sleep(20)
print(f"{count()} renders, {pending()} still queued, waited {int((time.time() - t0) / 60)} min")
