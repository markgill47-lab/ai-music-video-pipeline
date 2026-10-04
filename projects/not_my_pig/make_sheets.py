"""Reference sheets for H3 and Flux: the singer's 4x2 face sheet, and one combo (body sheet over face
sheet) per costume; the owner's face sheet and combo. Run from the project folder."""
from PIL import Image

W = 1672


def fit_width(im, w=W):
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def stack(top, bottom, out):
    top, bottom = fit_width(Image.open(top).convert("RGB")), fit_width(Image.open(bottom).convert("RGB"))
    combo = Image.new("RGB", (W, top.height + bottom.height))
    combo.paste(top, (0, 0)); combo.paste(bottom, (0, top.height))
    combo.save(out)
    print("wrote", out, combo.size)


def face_sheet(views, out, cols=4):
    rows = (len(views) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 512, rows * 512), (200, 200, 200))
    for i, v in enumerate(views):
        sheet.paste(Image.open(v).convert("RGB").resize((512, 512), Image.LANCZOS), ((i % cols) * 512, (i // cols) * 512))
    sheet.save(out)


face_sheet([f"refs/cast/nmp_singer_view_{i:05d}_.png" for i in range(1, 9)], "refs/cast/singer_face_sheet.png")
LOOKS = {"trench": "refs/cast/singer_body_trench.png", "suit": "refs/cast/nmp_costume_00001_.png",
         "track": "refs/cast/nmp_costume_00002_.png", "dress": "refs/cast/nmp_costume_00003_.png",
         "jacket": "refs/cast/nmp_costume_00004_.png", "robe": "refs/cast/nmp_costume_00005_.png"}
for look, body in LOOKS.items():
    stack(body, "refs/cast/singer_face_sheet.png", f"refs/cast/singer_{look}_combo.png")
face_sheet(["refs/cast/owner_face.png"] + [f"refs/cast/nmp_owner_view_{i:05d}_.png" for i in range(1, 5)][1:], "refs/cast/owner_face_sheet.png")
stack("refs/cast/owner_body.png", "refs/cast/owner_face_sheet.png", "refs/cast/owner_combo.png")

# rough cut v1 notes: one cup in her hand (Flux edit of the trench sheet), a consistent party host
stack("refs/cast/singer_body_trenchcup.png", "refs/cast/singer_face_sheet.png", "refs/cast/singer_trenchcup_combo.png")
stack("refs/cast/host_body.png", "refs/cast/host_face.png", "refs/cast/host_combo.png")
