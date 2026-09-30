"""Block until the ComfyUI queue is empty or max_minutes pass; print progress."""
import json, sys, time, urllib.request
limit = float(sys.argv[1]) * 60 if len(sys.argv) > 1 else 3300
t0 = time.time()
def n():
    q = json.load(urllib.request.urlopen("http://127.0.0.1:8188/queue"))
    return len(q["queue_running"]) + len(q["queue_pending"])
start = n()
while n() and time.time() - t0 < limit:
    time.sleep(30)
print(f"queue {start} -> {n()} after {int((time.time()-t0)/60)} min")
