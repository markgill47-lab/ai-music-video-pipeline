"""Tiny helpers for the overnight run: queue UI/API workflows via comfy-cli, wait for an empty queue.
  python comfyq.py run wf1.json wf2.json ...
  python comfyq.py wait [max_seconds]
"""
import json, os, subprocess, sys, time, urllib.request
COMFY = r"D:\Projects_26\Comfyu\ComfyUI\venv\Scripts\comfy.exe"
WF = r"D:\Projects_26\Comfyu\ComfyUI\user\default\workflows"

def pending():
    q = json.load(urllib.request.urlopen("http://127.0.0.1:8188/queue"))
    return len(q["queue_running"]) + len(q["queue_pending"])

if __name__ == "__main__":
    if sys.argv[1] == "run":
        for w in sys.argv[2:]:
            p = w if ("\\" in w or "/" in w) else os.path.join(WF, w)
            r = subprocess.run([COMFY, "run", "--workflow", p], capture_output=True, text=True)
            print(w, "ok" if r.returncode == 0 else r.stdout[-400:] + r.stderr[-400:])
    else:
        limit = float(sys.argv[2]) if len(sys.argv) > 2 else 580
        t0 = time.time()
        while pending() and time.time() - t0 < limit:
            time.sleep(10)
        print("pending", pending(), "after", int(time.time() - t0), "s")
