"""Word-level lyrics from the isolated vocal, transcribed in overlapping 30 s windows."""
import torch, json, librosa
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
y, sr = librosa.load("audio/stems/htdemucs/grounded/vocals.wav", sr=16000)
WIN, STEP = 30, 15
out = []
for s in range(0, int(len(y) / sr), STEP):
    segs, _ = m.transcribe(y[s * sr:(s + WIN) * sr], language="en", word_timestamps=True,
                           vad_filter=False, condition_on_previous_text=False)
    for seg in segs:
        for w in seg.words:
            t = s + w.start
            # keep each word from the window where it sits most centrally
            if (s == 0 or t >= s + 7.5) and t < s + 22.5 or (s + WIN >= len(y) / sr and t >= s + 7.5):
                out.append({"w": w.word.strip(), "s": round(t, 2), "e": round(s + w.end, 2), "p": round(w.probability, 2)})
out.sort(key=lambda d: d["s"])
json.dump(out, open("audio/whisper_words.json", "w"), indent=1)
line, last = [], 0
for d in out:
    if line and d["s"] - last > 0.9:
        print(f"{line[0]['s']:7.2f}  {' '.join(x['w'] for x in line)}"); line = []
    line.append(d); last = d["e"]
print(f"{line[0]['s']:7.2f}  {' '.join(x['w'] for x in line)}")
