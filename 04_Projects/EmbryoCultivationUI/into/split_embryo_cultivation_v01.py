from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps


PROJECT = Path(r"C:\Users\Administrator\Desktop\UIWorkflow\04_Projects\EmbryoCultivationUI")
SOURCE = PROJECT / "FullUI" / "EmbryoCultivationUI_FullUI_Review03_1024x1536.png"
CANDIDATES = PROJECT / "into" / "Candidates" / "SplitV01"
PREVIEWS = PROJECT / "into" / "ReassemblyPreview"
FORMAL = PROJECT / "Components" / "out" / "EmbryoCultivationUI"
TEMPLATES = PROJECT / "Templates"
QA = PROJECT / "QA"
PREFIX = "EmbryoCultivation"
for folder in (CANDIDATES, PREVIEWS, FORMAL, TEMPLATES, QA):
    folder.mkdir(parents=True, exist_ok=True)


def crop(box):
    return Image.open(SOURCE).convert("RGB").crop(box).convert("RGBA")


def mask(size, cut):
    w, h = size
    cut = max(2, min(cut, w // 4, h // 4))
    out = Image.new("L", size, 0)
    ImageDraw.Draw(out).polygon([(cut, 0), (w-cut-1, 0), (w-1, cut), (w-1, h-cut-1),
                                (w-cut-1, h-1), (cut, h-1), (0, h-cut-1), (0, cut)], fill=255)
    return out


def masked(im, cut):
    out = im.convert("RGBA")
    out.putalpha(mask(out.size, cut))
    return out


def fit_fill(texture, size):
    return ImageOps.fit(texture.convert("RGB"), size, method=Image.Resampling.LANCZOS).convert("RGBA")


def clean_interior(im, texture, region):
    out = im.convert("RGBA")
    x0, y0, x1, y1 = region
    fill = fit_fill(texture, (x1-x0, y1-y0))
    fill.putalpha(255)
    out.alpha_composite(fill, (x0, y0))
    return out


def save(role, state, im):
    w, h = im.size
    path = CANDIDATES / f"{PREFIX}_{role}_{state}_{w}x{h}.png"
    im.save(path)
    return path


def states(normal):
    rgba = normal.convert("RGBA")
    a = rgba.getchannel("A")
    rgb = rgba.convert("RGB")
    variants = {
        "Normal": rgb,
        "Hover": ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(1.08)).enhance(1.14),
        "Pressed": ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(0.94)).enhance(0.80),
        "Disabled": ImageEnhance.Brightness(ImageOps.grayscale(rgb).convert("RGB")).enhance(0.50),
    }
    result = {}
    for state, base in variants.items():
        out = base.convert("RGBA")
        out.putalpha(a)
        result[state] = out
    return result


def checkerboard(size, cell=24):
    out = Image.new("RGBA", size, (255,255,255,255))
    d = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            c = 180 if (x//cell + y//cell) % 2 == 0 else 235
            d.rectangle((x,y,min(x+cell-1,size[0]-1),min(y+cell-1,size[1]-1)), fill=(c,c,c,255))
    return out


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


outer_box = (41, 72, 984, 1434)
header_box = (74, 96, 951, 220)
tab_left_box = (140, 241, 501, 334)
tab_right_pos = (527, 241)
content_box = (88, 338, 939, 1260)
embryo_slot_box = (407, 416, 617, 635)
card_left_box = (108, 1087, 492, 1224)
card_right_pos = (533, 1087)
material_slot_box = (127, 1104, 223, 1204)
material_slot_right_pos = (552, 1104)
action_panel_box = (88, 1265, 940, 1410)
action_button_box = (285, 1284, 742, 1399)
close_display = (856, 121, 72, 67)

source = Image.open(SOURCE).convert("RGB")
body_texture = source.crop((220, 680, 810, 1020))
header_texture = source.crop((220, 122, 760, 190))
card_texture = source.crop((250, 1110, 470, 1190))

main = masked(clean_interior(crop(outer_box), body_texture, (25, 28, 918, 1332)), 25)
header = masked(clean_interior(crop(header_box), header_texture, (12, 10, 865, 113)), 12)
content = masked(clean_interior(crop(content_box), body_texture, (14, 14, 837, 908)), 14)
embryo_slot = masked(crop(embryo_slot_box), 16)
material_card = masked(clean_interior(crop(card_left_box), card_texture, (10, 10, 374, 127)), 10)
material_slot = masked(crop(material_slot_box), 10)
action_panel = masked(clean_interior(crop(action_panel_box), body_texture, (12, 12, 840, 133)), 12)
tab_button = masked(crop(tab_left_box), 14)
action_button = masked(crop(action_button_box), 16)

saved = [
    save("MainPanelBase", "Empty", main),
    save("HeaderPanel", "Empty", header),
    save("ContentPanel", "Empty", content),
    save("EmbryoSlot", "Empty", embryo_slot),
    save("MaterialCard", "Empty", material_card),
    save("MaterialSlot", "Empty", material_slot),
    save("ActionPanel", "Empty", action_panel),
]
for state, im in states(tab_button).items():
    saved.append(save("TabButton", state, im))
for state, im in states(action_button).items():
    saved.append(save("CultivateButton", state, im))

close_paths = {}
for state in ("Normal", "Hover", "Pressed", "Disabled"):
    src = PROJECT / "in" / "StylePrimary_Cook" / f"Cook_CloseButton_{state}_52x50.png"
    dst = CANDIDATES / f"{PREFIX}_CloseButton_{state}_52x50.png"
    dst.write_bytes(src.read_bytes())
    close_paths[state] = dst
    saved.append(dst)

canvas = Image.new("RGBA", (1024,1536), (0,0,0,0))
canvas.alpha_composite(main, outer_box[:2])
canvas.alpha_composite(header, header_box[:2])
canvas.alpha_composite(tab_button, tab_left_box[:2])
canvas.alpha_composite(tab_button, tab_right_pos)
canvas.alpha_composite(content, content_box[:2])
canvas.alpha_composite(embryo_slot, embryo_slot_box[:2])
canvas.alpha_composite(material_card, card_left_box[:2])
canvas.alpha_composite(material_card, card_right_pos)
canvas.alpha_composite(material_slot, material_slot_box[:2])
canvas.alpha_composite(material_slot, material_slot_right_pos)
canvas.alpha_composite(action_panel, action_panel_box[:2])
canvas.alpha_composite(action_button, action_button_box[:2])
close = Image.open(close_paths["Normal"]).convert("RGBA").resize((72,67), Image.Resampling.LANCZOS)
canvas.alpha_composite(close, close_display[:2])
preview = PREVIEWS / "EmbryoCultivation_Reassembled_SplitV01_1024x1536.png"
canvas.save(preview)
cb = checkerboard(canvas.size); cb.alpha_composite(canvas)
checker_path = PREVIEWS / "EmbryoCultivation_Reassembled_SplitV01_Checkerboard_1024x1536.png"
cb.save(checker_path)

for name, im in (("EmbryoSlot",embryo_slot),("MaterialCard",material_card),("TabButton",tab_button),("CultivateButton",action_button)):
    im.resize((im.width*4, im.height*4), Image.Resampling.NEAREST).save(PREVIEWS / f"EmbryoCultivation_{name}_SplitV01_400Percent.png")

strip = Image.new("RGBA", (tab_button.width*4+18, tab_button.height), (0,0,0,0))
tab_states = states(tab_button)
for i, state in enumerate(("Normal","Hover","Pressed","Disabled")):
    strip.alpha_composite(tab_states[state], (i*tab_button.width+i*6, 0))
strip.save(PREVIEWS / "EmbryoCultivation_TabButton_SplitV01_FourStates.png")

main.save(TEMPLATES / "EmbryoCultivation_CleanTemplate_Empty_943x1362.png")
manifest = {
    "projectId":"EmbryoCultivationUI", "splitVersion":"SplitV01", "candidateCount":len(saved),
    "source":str(SOURCE),
    "sourceBounds":{"MainPanelBase":outer_box,"HeaderPanel":header_box,"TabButtonLeft":tab_left_box,
                    "TabButtonRight":(*tab_right_pos,tab_button.width,tab_button.height),"ContentPanel":content_box,
                    "EmbryoSlot":embryo_slot_box,"MaterialCardLeft":card_left_box,
                    "MaterialCardRight":(*card_right_pos,material_card.width,material_card.height),
                    "MaterialSlotLeft":material_slot_box,"MaterialSlotRight":(*material_slot_right_pos,material_slot.width,material_slot.height),
                    "ActionPanel":action_panel_box,"CultivateButton":action_button_box,"CloseButtonDisplay":close_display},
    "files":[{"name":p.name,"sha256":sha(p)} for p in sorted(saved)]
}
(QA/"split_v01_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"candidateCount":len(saved),"candidateFolder":str(CANDIDATES),"preview":str(preview),"checkerboard":str(checker_path)},indent=2))
