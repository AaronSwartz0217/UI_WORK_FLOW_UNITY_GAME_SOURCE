from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps, ImageDraw


PROJECT = Path(r"C:\Users\Administrator\Desktop\UIWorkflow\04_Projects\TeamInvitationPopupUI")
SOURCE = PROJECT / "FullUI" / "TeamInvitationPopupUI_FullUI_Review06_1536x1024.png"
CANDIDATES = PROJECT / "into" / "Candidates" / "SplitV01"
PREVIEWS = PROJECT / "into" / "ReassemblyPreview"
FORMAL = PROJECT / "Components" / "out" / "TeamInvitationPopupUI"
TEMPLATES = PROJECT / "Templates"
QA = PROJECT / "QA"
PREFIX = "TeamInvitation"

for folder in (CANDIDATES, PREVIEWS, FORMAL, TEMPLATES, QA):
    folder.mkdir(parents=True, exist_ok=True)


def crop(box: tuple[int, int, int, int]) -> Image.Image:
    return Image.open(SOURCE).convert("RGB").crop(box).convert("RGBA")


def chamfer_mask(size: tuple[int, int], cut: int) -> Image.Image:
    w, h = size
    cut = max(2, min(cut, w // 4, h // 4))
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(
        [(cut, 0), (w - cut - 1, 0), (w - 1, cut), (w - 1, h - cut - 1),
         (w - cut - 1, h - 1), (cut, h - 1), (0, h - cut - 1), (0, cut)],
        fill=255,
    )
    return mask


def apply_mask(im: Image.Image, cut: int) -> Image.Image:
    out = im.copy().convert("RGBA")
    out.putalpha(chamfer_mask(out.size, cut))
    return out


def tile_fill(texture: Image.Image, size: tuple[int, int]) -> Image.Image:
    # ImageOps.fit avoids visible tile seams in broad parent-panel cleanup.
    return ImageOps.fit(texture.convert("RGB"), size, method=Image.Resampling.LANCZOS)


def clean(im: Image.Image, texture: Image.Image,
          soft_regions: list[tuple[int, int, int, int]],
          hard_regions: list[tuple[int, int, int, int]]) -> Image.Image:
    out = im.convert("RGBA")
    for region in soft_regions:
        x0, y0, x1, y1 = region
        fill = tile_fill(texture, (x1 - x0, y1 - y0)).convert("RGBA")
        alpha = Image.new("L", fill.size, 210)
        fill.putalpha(alpha)
        out.alpha_composite(fill, (x0, y0))
    for region in hard_regions:
        x0, y0, x1, y1 = region
        fill = tile_fill(texture, (x1 - x0, y1 - y0)).convert("RGBA")
        fill.putalpha(255)
        out.alpha_composite(fill, (x0, y0))
    return out


def save_component(role: str, state: str, im: Image.Image) -> Path:
    w, h = im.size
    path = CANDIDATES / f"{PREFIX}_{role}_{state}_{w}x{h}.png"
    im.save(path)
    return path


def button_states(normal: Image.Image) -> dict[str, Image.Image]:
    rgba = normal.convert("RGBA")
    alpha = rgba.getchannel("A")
    rgb = rgba.convert("RGB")
    hover = ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(1.08)).enhance(1.14)
    pressed = ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(0.94)).enhance(0.80)
    disabled = ImageEnhance.Brightness(ImageOps.grayscale(rgb).convert("RGB")).enhance(0.52)
    states = {"Normal": rgb, "Hover": hover, "Pressed": pressed, "Disabled": disabled}
    result: dict[str, Image.Image] = {}
    for state, state_rgb in states.items():
        out = state_rgb.convert("RGBA")
        out.putalpha(alpha)
        result[state] = out
    return result


def checkerboard(size: tuple[int, int], cell: int = 24) -> Image.Image:
    out = Image.new("RGBA", size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            c = 180 if (x // cell + y // cell) % 2 == 0 else 235
            draw.rectangle((x, y, min(x + cell - 1, size[0] - 1), min(y + cell - 1, size[1] - 1)), fill=(c, c, c, 255))
    return out


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# Review06 measured regions.
outer_box = (134, 44, 1400, 965)
header_box = (156, 72, 1376, 179)
list_box = (157, 185, 1376, 942)
row_box = (188, 214, 1349, 315)
accept_box = (968, 223, 1140, 300)
reject_box = (1164, 223, 1328, 300)

source = Image.open(SOURCE).convert("RGB")
body_texture = source.crop((220, 340, 1320, 900))
header_texture = source.crop((260, 98, 1180, 154))
row_texture = source.crop((220, 225, 930, 300))

main = crop(outer_box)
main = clean(
    main,
    body_texture,
    [],
    [(22, 25, 1244, 895)],
)
main = apply_mask(main, 25)

header = crop(header_box)
header = clean(header, header_texture, [], [(12, 10, 1208, 96)])
header = apply_mask(header, 10)

list_panel = crop(list_box)
list_texture = source.crop((220, 340, 1320, 900))
list_panel = clean(list_panel, list_texture, [], [(20, 24, 1198, 735)])
list_panel = apply_mask(list_panel, 14)

row = crop(row_box)
row = clean(
    row,
    row_texture,
    [],
    [(8, 8, 1152, 93)],
)
row = apply_mask(row, 10)

accept = apply_mask(crop(accept_box), 12)
reject = apply_mask(crop(reject_box), 12)

saved: list[Path] = []
saved.append(save_component("MainPanelBase", "Empty", main))
saved.append(save_component("HeaderPanel", "Empty", header))
saved.append(save_component("InvitationListPanel", "Empty", list_panel))
saved.append(save_component("InvitationRow", "Empty", row))
for state, im in button_states(accept).items():
    saved.append(save_component("AcceptButton", state, im))
for state, im in button_states(reject).items():
    saved.append(save_component("RejectButton", state, im))

close_source = PROJECT / "in" / "StylePrimary_Cook"
close_paths: dict[str, Path] = {}
for state in ("Normal", "Hover", "Pressed", "Disabled"):
    src = close_source / f"Cook_CloseButton_{state}_52x50.png"
    dst = CANDIDATES / f"{PREFIX}_CloseButton_{state}_52x50.png"
    dst.write_bytes(src.read_bytes())
    close_paths[state] = dst
    saved.append(dst)

# Reassemble at original positions for visual QA.
canvas = Image.new("RGBA", (1536, 1024), (0, 0, 0, 0))
canvas.alpha_composite(main, (outer_box[0], outer_box[1]))
canvas.alpha_composite(header, (header_box[0], header_box[1]))
canvas.alpha_composite(list_panel, (list_box[0], list_box[1]))
canvas.alpha_composite(row, (row_box[0], row_box[1]))
canvas.alpha_composite(accept, (accept_box[0], accept_box[1]))
canvas.alpha_composite(reject, (reject_box[0], reject_box[1]))
close = Image.open(close_paths["Normal"]).convert("RGBA").resize((62, 60), Image.Resampling.LANCZOS)
canvas.alpha_composite(close, (1298, 87))
preview = PREVIEWS / "TeamInvitation_Reassembled_SplitV01_1536x1024.png"
canvas.save(preview)
checker = checkerboard(canvas.size)
checker.alpha_composite(canvas)
checker_path = PREVIEWS / "TeamInvitation_Reassembled_SplitV01_Checkerboard_1536x1024.png"
checker.save(checker_path)

for name, im in (("InvitationRow", row), ("AcceptButton", accept), ("RejectButton", reject)):
    im.resize((im.width * 4, im.height * 4), Image.Resampling.NEAREST).save(
        PREVIEWS / f"TeamInvitation_{name}_SplitV01_400Percent.png"
    )

state_strip = Image.new("RGBA", (accept.width * 4 + 18, accept.height), (0, 0, 0, 0))
for i, state in enumerate(("Normal", "Hover", "Pressed", "Disabled")):
    state_strip.alpha_composite(button_states(accept)[state], (i * accept.width + i * 6, 0))
state_strip.save(PREVIEWS / "TeamInvitation_AcceptButton_SplitV01_FourStates.png")

main.save(TEMPLATES / "TeamInvitation_CleanTemplate_Empty_1266x921.png")
manifest = {
    "projectId": "TeamInvitationPopupUI",
    "source": str(SOURCE),
    "splitVersion": "SplitV01",
    "candidateCount": len(saved),
    "sourceBounds": {
        "MainPanelBase": outer_box,
        "HeaderPanel": header_box,
        "InvitationListPanel": list_box,
        "InvitationRow": row_box,
        "AcceptButton": accept_box,
        "RejectButton": reject_box,
        "CloseButtonDisplay": (1298, 87, 62, 60),
    },
    "files": [{"name": p.name, "sha256": sha256(p)} for p in sorted(saved)],
}
(QA / "split_v01_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"candidateCount": len(saved), "candidateFolder": str(CANDIDATES), "preview": str(preview), "checkerboard": str(checker_path)}, indent=2))
