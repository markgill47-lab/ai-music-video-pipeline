"""Assemble the full music video from rendered shots against the song.

Each EDL entry is (clip, song_start, song_end, src_offset): the piece covers
[song_start, song_end) of the song and is taken from the clip starting at src_offset
seconds. Straight shots use src_offset 0. Intercuts between two renders of the same
slot shift their source only by whole multiples of 8 or 6 beats, so motion that was
pinned to the music stays on the beat. Cut points snap to the detected beat grid.
Missing clips are replaced by a labelled slate so partial assemblies still play.
  python assemble_full.py [out.mp4]
"""
import json, os, subprocess, sys
import numpy as np

SONG = r"audio\No Fucks at All.mp3"
FPS, W, H = 24, 1120, 640
BEATS = np.array(json.load(open("audio/beats_full.json")))


def beat(t):
    return float(BEATS[np.argmin(abs(BEATS - t))])


def intercut(a, b, start, end, n_beats, a_skip=0.0, b_skip=0.0):
    """Alternate a/b every n_beats, each clip advancing through its own timeline.
    a_skip/b_skip drop a clip's opening seconds (e.g. a reference image H3 played as a shot)."""
    step = n_beats * float(np.median(np.diff(BEATS)))
    pts = [start] + [beat(start + step * k) for k in range(1, 4)] + [end]
    # a0 b0 a1 b1: each clip's second piece continues its own clock where its first stopped
    d0, d1 = pts[1] - pts[0], pts[2] - pts[1]
    return [(a, pts[0], pts[1], a_skip), (b, pts[1], pts[2], b_skip),
            (a, pts[2], pts[3], a_skip + d0), (b, pts[3], pts[4], b_skip + d1)]


def edl():
    o = "out/"
    a2 = "out/act2/"
    # opening: establishing truck broken up by crew inserts on 8/4-beat boundaries;
    # the last establishing piece resumes at its own song-aligned time so the push lands on the band
    e = [(o + "shot1_establish.mp4", 0.0, 3.924, 0), (a2 + "crew_flat.mp4", 3.924, 7.848, 0),
         (a2 + "crew_light.mp4", 7.848, 9.799, 0), (a2 + "crew_countdown.mp4", 9.799, 11.749, 0.9),
         (o + "shot1_establish.mp4", 11.749, 14.676, 11.749), (o + "shot2_zoom.mp4", 14.676, 28.816, 0),
         (o + "shot3a_bedroom.mp4", 28.816, 38.081, 0), (o + "shot3b_bedroom.mp4", 38.081, 47.345, 0),
         (o + "shot4_office.mp4", 47.345, 62.438, 0), (o + "shot5a_band.mp4", 62.438, 71.70, 0),
         (o + "shot5b_band.mp4", 71.70, 78.04, 0), (o + "shot6_audience.mp4", 78.04, 81.92, 0),
         (o + "shot7_certificate.mp4", 81.92, 86.796, 0),
         (a2 + "shot8a_boss.mp4", 86.796, 95.527, 0), (a2 + "shot8b_nope.mp4", 95.527, 100.867, 0),
         (a2 + "shot8c_dance.mp4", 100.867, 110.109, 0)]
    # 9a opens on ~1.2 s of the chest reference played as a shot; skip it (1.217 s = 29 frames)
    e += intercut(a2 + "shot9a_tv.mp4", a2 + "shot9b_chapel.mp4", 110.109, 125.643, 8, a_skip=1.217)
    e += [(a2 + "shot10a_chorus.mp4", 125.643, 133.399, 0), (a2 + "shot10b_chorus.mp4", 133.399, 139.668, 0)]
    e += intercut(a2 + "shot11a_tv_sad.mp4", a2 + "shot11b_chapel_sad.mp4", 139.668, 151.208, 6)
    e += [(a2 + "shot12a_ship.mp4", 151.208, 156.038, 0), 
          # bridge v2 (fast arc): drop frames 130-142, where the camera passes behind a foil flat and goes black
          (a2 + "shot12b_bridge_v2.mp4", 156.038, 156.038 + 130 / 24, 0),
          (a2 + "shot12b_bridge_v2.mp4", 156.038 + 130 / 24, 164.188, 143 / 24),
          (a2 + "shot12c_robot.mp4", 164.188, 175.682, 0), (a2 + "shot12d_robot.mp4", 175.682, 184.529, 0),
          (a2 + "shot12e_captain.mp4", 184.529, 187.130, 0),
          (a2 + "shot13a_chorus.mp4", 187.130, 200.969, 0), (a2 + "shot13b_rush.mp4", 200.969, 205.264, 0),
          ]
    # dance line: closer moving takes intercut every 6 beats. A2 trucks right (both ends
    # pinned to crops of the wide take), B is a low angle trucking left; both song-aligned.
    # the singer lip-syncs here, so every piece plays from its song-aligned point (not intercut's own clock)
    d0 = 205.264
    for k, (clip, s, t, _) in enumerate(intercut(a2 + "shot13c_line_A2.mp4", a2 + "shot13c_line_B.mp4", d0, 217.687, 6)):
        e.append((clip, s, t, s - d0))
    # finale: all / ECU / all / ECU / all / ECU. Both "all" takes cut to grey sheet shots
    # partway (v1 until 4.42 s, v2 from 2.29 to 6.2 s), so each "all" piece comes from
    # whichever take is on stage then. Offsets stay song-aligned (both rendered from t0).
    t0 = 217.687
    cuts = [t0, beat(219.8), beat(222.1), beat(224.0), beat(225.8), beat(227.4), 229.227]
    alls = [(a2 + "shot14_all_v2.mp4", 0.0), (a2 + "shot14_all.mp4", 4.42), (a2 + "shot14_all.mp4", None)]
    for k in range(6):
        if k % 2:
            e.append((a2 + "shot14_ecu.mp4", cuts[k], cuts[k + 1], cuts[k] - t0))
        else:
            clip, off = alls[k // 2]
            e.append((clip, cuts[k], cuts[k + 1], max(off or 0.0, cuts[k] - t0)))
    e.append((a2 + "shot14_end.mp4", 229.227, 241.68, 0.125))  # frame 0 is a guide-blend smear
    return e


def render(pieces, out):
    os.makedirs("out/edit_full", exist_ok=True)
    files = []
    for i, (clip, s, t, off) in enumerate(pieces):
        n = round(t * FPS) - round(s * FPS)
        f = f"out/edit_full/p{i:03d}.mp4"
        if os.path.exists(clip):
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{off:.3f}", "-i", clip, "-frames:v", str(n), "-an",
                   "-vf", f"scale={W}:{H},fps={FPS}"]
        else:
            label = os.path.basename(clip).replace(".mp4", "")
            cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x202020:s={W}x{H}:r={FPS}",
                   "-frames:v", str(n), "-vf", f"drawbox=x=0:y=300:w={W}:h=40:color=0x505050:t=fill"]
            print("  missing:", label)
        subprocess.run(cmd + ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", f], check=True)
        files.append(f)
    open("out/edit_full/list.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/edit_full/list.txt",
                    "-c", "copy", "out/edit_full/video.mp4"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "out/edit_full/video.mp4", "-i", SONG, "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", out], check=True)
    print("wrote", out)


if __name__ == "__main__":
    render(edl(), sys.argv[1] if len(sys.argv) > 1 else "out/rough_cut_v3.mp4")
