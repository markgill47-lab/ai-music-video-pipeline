"""Assemble Grounded against the song. Each shot fills its beat slot from queue_shots.SPECS;
TAKES picks which render plays (default out/<name>.mp4) and from what offset. A render shorter
than its slot holds its last frame (the opening shot holds its first frame instead); the last
shot fades to black. Missing renders become grey slates so partial cuts still play.
  python assemble.py [out.mp4]"""
import os, subprocess, sys
from queue_shots import SPECS, slot

SONG = r"audio\grounded.mp3"
FPS, W, H = 24, 1120, 640
# name: (clip, source offset seconds)
TAKES = {
    "s11_planeA": ("out/s11_planeA_r30.mp4", 0.0),
    "s20_planeB": ("out/s20_planeB_r30.mp4", 0.0),
    "s27_planeC": ("out/s27_planeC_r3.mp4", 0.0),
    # the dome morphs into a square antenna after ~3.6 s in every take; first 3.6 s at half speed
    "s14_apron": ("out/s14_apron_slow.mp4", 0.0),
}
TAKES.update({
    "s16_storm": ("out/s16_storm_r10.mp4", 0.0),
    # 7.2 s slot: the last half of the reveal take (crowd, then Steve slides in)
    "s22_departure": ("out/s22_departure_r10.mp4", 7.17),
    "s28_night": ("out/s28_night_r40.mp4", 0.0),
    "s25_alec": ("out/s25_alec_r40.mp4", 0.0),
    "s26_two": ("out/s26_two_r40.mp4", 0.0),
    "s03_badge": ("out/s03_badge_r41.mp4", 0.0),
})
for _n in ("s01b_house", "s23a_flyby", "s23b_cockpit", "s23c_window", "s26b_takeoff"):
    TAKES[_n] = (f"out/{_n}_r40.mp4", 0.0)


def render(out):
    os.makedirs("out/edit", exist_ok=True)
    files, t_prev = [], 0.0
    names = list(SPECS)
    for i, name in enumerate(names):
        s, t = slot(name)
        if i == 0:
            s = 0.0
        n = round(t * FPS) - round(s * FPS)
        clip, off = TAKES.get(name, (f"out/{name}.mp4", 0.0))
        f = f"out/edit/p{i:03d}.mp4"
        if os.path.exists(clip):
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                        "csv=p=0", clip], capture_output=True, text=True).stdout) - off
            short = max(0.0, n / FPS - dur)
            vf = f"scale={W}:{H},fps={FPS}"
            if short > 0:
                vf += f",tpad={'start' if i == 0 else 'stop'}_mode=clone:{'start' if i == 0 else 'stop'}_duration={short:.3f}"
            if i == len(names) - 1:
                vf += f",fade=t=out:st={n / FPS - 4:.3f}:d=4"
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{off:.3f}", "-i", clip, "-frames:v", str(n), "-an", "-vf", vf]
        else:
            cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x303030:s={W}x{H}:r={FPS}",
                   "-frames:v", str(n)]
            print("  missing:", name)
        subprocess.run(cmd + ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", f], check=True)
        files.append(f)
    open("out/edit/list.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/edit/list.txt",
                    "-c", "copy", "out/edit/video.mp4"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "out/edit/video.mp4", "-i", SONG, "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", out], check=True)
    print("wrote", out)


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else "out/rough_cut_v1.mp4")
