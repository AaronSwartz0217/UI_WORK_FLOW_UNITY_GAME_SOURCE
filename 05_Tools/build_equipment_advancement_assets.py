from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import json

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "04_Projects" / "EquipmentAdvancementUI"
SOURCE = PROJECT / "into" / "EquipmentAdvancementUI_NoOrdinaryText_Master_1078x1459.png"
OUT = PROJECT / "Components" / "out" / "EquipmentAdvancementUI"
PREVIEW = PROJECT / "into" / "ReassemblyPreview"

PREFIX = "EquipmentAdvancement"

REGIONS = {
    "MainPanelBase": (47, 43, 1032, 1427),
    "TopEquipmentPanel": (96, 168, 979, 500),
    "QualityPanel": (97, 529, 977, 740),
    "EquipmentPairPanel": (98, 774, 978, 1056),
    "ProgressActionPanel": (98, 1083, 978, 1390),
    "TopEquipmentSlot": (458, 218, 616, 383),
    "LeftEquipmentRow": (175, 849, 526, 976),
    "RightEquipmentRow": (553, 849, 908, 976),
    "LeftEquipmentSlot": (191, 867, 277, 956),
    "RightEquipmentSlot": (571, 867, 657, 956),
    "QualityArrow": (516, 608, 572, 655),
    "ProgressTrack": (174, 1117, 906, 1155),
    "ProgressFill": (174, 1117, 317, 1155),
    "HelpButton": (847, 76, 916, 141),
    "CloseButton": (936, 75, 1005, 142),
    "AdvanceButton": (345, 1244, 729, 1347),
}

PARENT_CHILDREN = {
    "MainPanelBase": ["TopEquipmentPanel", "QualityPanel", "EquipmentPairPanel", "ProgressActionPanel", "HelpButton", "CloseButton"],
    "TopEquipmentPanel": ["TopEquipmentSlot"],
    "QualityPanel": ["QualityArrow"],
    "EquipmentPairPanel": ["LeftEquipmentRow", "RightEquipmentRow"],
    "LeftEquipmentRow": ["LeftEquipmentSlot"],
    "RightEquipmentRow": ["RightEquipmentSlot"],
    "ProgressActionPanel": ["ProgressTrack", "AdvanceButton"],
}

def rgba_crop(img, box, radius=8):
    crop = img.crop(box).convert("RGBA")
    w, h = crop.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((1, 1, w - 2, h - 2), radius=radius, fill=255)
    crop.putalpha(mask)
    return crop

def fill_region_with_texture(img, target, sample, inset=0):
    x0, y0, x1, y1 = target
    sx0, sy0, sx1, sy1 = sample
    tile = img.crop((sx0, sy0, sx1, sy1)).resize((max(1, x1-x0), max(1, y1-y0)))
    img.paste(tile, (x0, y0))

def empty_parent(master, name):
    box = REGIONS[name]
    panel = master.crop(box).convert("RGBA")
    bx, by = box[0], box[1]
    for child in PARENT_CHILDREN.get(name, []):
        cx0, cy0, cx1, cy1 = REGIONS[child]
        local = (cx0-bx, cy0-by, cx1-bx, cy1-by)
        w, h = panel.size
        pad = 12
        sample = (max(20, local[0]), max(20, local[1]-pad-24), min(w-20, local[2]), max(21, local[1]-pad))
        if sample[2] <= sample[0] or sample[3] <= sample[1]:
            sample = (w//3, h//3, min(w-20, w//3+64), min(h-20, h//3+64))
        fill_region_with_texture(panel, local, sample)
    mask = Image.new("L", panel.size, 0)
    d = ImageDraw.Draw(mask)
    radius = 18 if name == "MainPanelBase" else 8
    d.rounded_rectangle((1, 1, panel.width-2, panel.height-2), radius=radius, fill=255)
    panel.putalpha(mask)
    return panel

def state_variant(normal, state):
    rgb = normal.convert("RGB")
    if state == "Hover":
        rgb = ImageEnhance.Brightness(rgb).enhance(1.16)
        rgb = ImageEnhance.Color(rgb).enhance(1.12)
    elif state == "Pressed":
        rgb = ImageEnhance.Brightness(rgb).enhance(0.78)
        rgb = ImageEnhance.Contrast(rgb).enhance(1.15)
    elif state == "Disabled":
        rgb = ImageEnhance.Color(rgb).enhance(0.18)
        rgb = ImageEnhance.Brightness(rgb).enhance(0.62)
    out = rgb.convert("RGBA")
    out.putalpha(normal.getchannel("A"))
    return out

def save_named(img, component, state):
    name = f"{PREFIX}_{component}_{state}_{img.width}x{img.height}.png"
    img.save(OUT / name)
    return name

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PREVIEW.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.png"):
        f.unlink()
    master = Image.open(SOURCE).convert("RGBA")
    manifest = []

    for component in ["MainPanelBase", "TopEquipmentPanel", "QualityPanel", "EquipmentPairPanel", "ProgressActionPanel", "LeftEquipmentRow", "RightEquipmentRow"]:
        asset = empty_parent(master, component)
        fn = save_named(asset, component, "Empty" if component != "MainPanelBase" else "Default")
        manifest.append((fn, component, "Empty" if component != "MainPanelBase" else "Default", asset.size))

    for component in ["TopEquipmentSlot", "LeftEquipmentSlot", "RightEquipmentSlot", "QualityArrow", "ProgressTrack", "ProgressFill"]:
        radius = 3 if component in ("QualityArrow", "ProgressFill") else 7
        if component == "RightEquipmentSlot":
            asset = rgba_crop(master, REGIONS["LeftEquipmentSlot"], radius)
        else:
            asset = rgba_crop(master, REGIONS[component], radius)
        fn = save_named(asset, component, "Default")
        manifest.append((fn, component, "Default", asset.size))

    for component in ["HelpButton", "CloseButton", "AdvanceButton"]:
        normal = rgba_crop(master, REGIONS[component], 9)
        for state in ["Normal", "Hover", "Pressed", "Disabled"]:
            asset = normal if state == "Normal" else state_variant(normal, state)
            fn = save_named(asset, component, state)
            manifest.append((fn, component, state, asset.size))

    preview = Image.new("RGBA", master.size, (0,0,0,0))
    order = ["MainPanelBase", "TopEquipmentPanel", "QualityPanel", "EquipmentPairPanel", "ProgressActionPanel", "LeftEquipmentRow", "RightEquipmentRow", "TopEquipmentSlot", "LeftEquipmentSlot", "RightEquipmentSlot", "QualityArrow", "ProgressTrack", "ProgressFill", "HelpButton", "CloseButton", "AdvanceButton"]
    for component in order:
        state = "Default"
        if component == "MainPanelBase": state = "Default"
        elif component in PARENT_CHILDREN: state = "Empty"
        elif component in ["HelpButton", "CloseButton", "AdvanceButton"]: state = "Normal"
        pattern = f"{PREFIX}_{component}_{state}_*.png"
        path = next(OUT.glob(pattern))
        asset = Image.open(path).convert("RGBA")
        x, y = REGIONS[component][:2]
        preview.alpha_composite(asset, (x, y))
    preview.save(PREVIEW / "EquipmentAdvancementUI_Reassembly_Default_1078x1459.png")

    checker = Image.new("RGB", master.size, "white")
    d = ImageDraw.Draw(checker)
    s = 24
    for y in range(0, master.height, s):
        for x in range(0, master.width, s):
            if (x//s + y//s) % 2:
                d.rectangle((x,y,x+s-1,y+s-1), fill=(185,185,185))
    checker = checker.convert("RGBA")
    checker.alpha_composite(preview)
    checker.convert("RGB").save(PREVIEW / "EquipmentAdvancementUI_Reassembly_Checkerboard_1078x1459.jpg", quality=94)

    data = {"manifest": [{"filename": f, "component": c, "state": s, "width": z[0], "height": z[1]} for f,c,s,z in manifest], "regions": REGIONS}
    (PROJECT / "into" / "equipment_advancement_build.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
