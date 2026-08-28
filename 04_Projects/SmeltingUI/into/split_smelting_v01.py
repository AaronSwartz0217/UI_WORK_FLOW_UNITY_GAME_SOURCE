from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
import hashlib
import json
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "FullUI" / "SmeltingUI_FullUI_Review02_1024x1536.png"
CANDIDATES = ROOT / "into" / "Candidates" / "SplitV01"
PREVIEWS = ROOT / "into" / "ReassemblyPreview"
FORMAL = ROOT / "Components" / "out" / "SmeltingUI"
TEMPLATES = ROOT / "Templates"
QA = ROOT / "QA"
COOK = ROOT.parents[1] / "01_References" / "Style" / "Standards" / "Primary_Cook"

for folder in (CANDIDATES, PREVIEWS, FORMAL, TEMPLATES, QA):
    folder.mkdir(parents=True, exist_ok=True)

src = Image.open(SOURCE).convert("RGBA")


def polygon_mask(size, points, supersample=4):
    width, height = size
    large = Image.new("L", (width * supersample, height * supersample), 0)
    ImageDraw.Draw(large).polygon([(x * supersample, y * supersample) for x, y in points], fill=255)
    mask = large.resize(size, Image.Resampling.LANCZOS)
    return mask.point(lambda value: 0 if value <= 5 else value)


def chamfer_points(width, height, chamfer):
    right = width - 1
    bottom = height - 1
    return [
        (chamfer, 0),
        (right - chamfer, 0),
        (right, chamfer),
        (right, bottom - chamfer),
        (right - chamfer, bottom),
        (chamfer, bottom),
        (0, bottom - chamfer),
        (0, chamfer),
    ]


def cut_chamfered(box, chamfer):
    image = src.crop(box).convert("RGBA")
    image.putalpha(polygon_mask(image.size, chamfer_points(image.width, image.height, chamfer)))
    return image


def tiled_texture(size, texture):
    result = Image.new("RGBA", size, (7, 7, 7, 255))
    tile_width, tile_height = texture.size
    for row, y in enumerate(range(0, size[1], tile_height)):
        for column, x in enumerate(range(0, size[0], tile_width)):
            tile = texture
            if column % 2:
                tile = ImageOps.mirror(tile)
            if row % 2:
                tile = ImageOps.flip(tile)
            result.alpha_composite(tile, (x, y))
    return result


def fill_region(image, image_origin, abs_region, synthetic_texture, feather=10):
    origin_x, origin_y = image_origin
    x0, y0, x1, y1 = abs_region
    local_x0, local_y0 = x0 - origin_x, y0 - origin_y
    width, height = x1 - x0, y1 - y0
    patch = synthetic_texture.crop((local_x0, local_y0, local_x0 + width, local_y0 + height))
    mask = Image.new("L", patch.size, 0)
    ImageDraw.Draw(mask).rectangle((feather, feather, width - feather - 1, height - feather - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    image.paste(patch, (local_x0, local_y0), mask)


def clean_low_alpha(image):
    image = image.copy()
    image.putalpha(image.getchannel("A").point(lambda value: 0 if value <= 5 else value))
    return image


def make_states(normal):
    alpha = normal.getchannel("A")
    disabled = ImageOps.grayscale(normal.convert("RGB")).convert("RGBA")
    states = {
        "Normal": normal.copy(),
        "Hover": ImageEnhance.Brightness(normal).enhance(1.14),
        "Pressed": ImageEnhance.Brightness(normal).enhance(0.76),
        "Disabled": ImageEnhance.Brightness(disabled).enhance(0.50),
    }
    for image in states.values():
        image.putalpha(alpha)
    return states


def save(image, component, state):
    image = clean_low_alpha(image)
    filename = f"Smelting_{component}_{state}_{image.width}x{image.height}.png"
    image.save(CANDIDATES / filename)
    return filename


def checkerboard(image, cell=24):
    background = Image.new("RGB", image.size, "white")
    draw = ImageDraw.Draw(background)
    for y in range(0, image.height, cell):
        for x in range(0, image.width, cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, min(x + cell - 1, image.width - 1), min(y + cell - 1, image.height - 1)), fill=(188, 188, 188))
    background.paste(image, mask=image.getchannel("A"))
    return background


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


boxes = {
    "MainPanelBase": (34, 72, 985, 1471),
    "MaterialSlot": (205, 226, 338, 363),
    "OutputPreviewPanel": (129, 938, 888, 1279),
    "SmeltButton": (314, 1331, 705, 1409),
}

panel = cut_chamfered(boxes["MainPanelBase"], 15)
panel_origin = boxes["MainPanelBase"][:2]
horizontal_texture = src.crop((100, 102, 820, 210)).convert("RGBA")
vertical_texture = src.crop((80, 100, 120, 1440)).convert("RGBA")
horizontal_texture.save(PREVIEWS / "Smelting_SplitV01_TextureSource.png")
synthetic_texture = Image.blend(
    tiled_texture(panel.size, horizontal_texture),
    tiled_texture(panel.size, vertical_texture),
    0.45,
).filter(ImageFilter.GaussianBlur(0.35))
for region in (
    (820, 80, 970, 220),
    (150, 180, 870, 910),
    (80, 880, 930, 1320),
    (250, 1285, 760, 1450),
):
    fill_region(panel, panel_origin, region, synthetic_texture, feather=20)
for region in (
    (850, 98, 952, 192),
    (188, 210, 833, 883),
    (114, 920, 903, 1295),
    (295, 1315, 724, 1425),
):
    fill_region(panel, panel_origin, region, synthetic_texture, feather=0)
panel.putalpha(polygon_mask(panel.size, chamfer_points(panel.width, panel.height, 15)))

slot = cut_chamfered(boxes["MaterialSlot"], 6)
output_panel = cut_chamfered(boxes["OutputPreviewPanel"], 13)
smelt_button = cut_chamfered(boxes["SmeltButton"], 13)

save(panel, "MainPanelBase", "Empty")
save(slot, "MaterialSlot", "Empty")
save(output_panel, "OutputPreviewPanel", "Empty")
for state, image in make_states(smelt_button).items():
    save(image, "SmeltButton", state)

for state in ("Normal", "Hover", "Pressed", "Disabled"):
    source = COOK / f"Cook_CloseButton_{state}_52x50.png"
    target = CANDIDATES / f"Smelting_CloseButton_{state}_52x50.png"
    shutil.copy2(source, target)

slot_positions = [
    (x, y)
    for y in (226, 394, 561, 729)
    for x in (205, 365, 524, 684)
]

canvas = Image.new("RGBA", src.size, (0, 0, 0, 0))
canvas.alpha_composite(panel, panel_origin)
for position in slot_positions:
    canvas.alpha_composite(slot, position)
canvas.alpha_composite(output_panel, boxes["OutputPreviewPanel"][:2])
canvas.alpha_composite(smelt_button, boxes["SmeltButton"][:2])
close = Image.open(CANDIDATES / "Smelting_CloseButton_Normal_52x50.png").convert("RGBA")
canvas.alpha_composite(close.resize((64, 62), Image.Resampling.LANCZOS), (875, 114))

preview = PREVIEWS / "Smelting_Reassembled_SplitV01_1024x1536.png"
checker_preview = PREVIEWS / "Smelting_Reassembled_SplitV01_Checkerboard_1024x1536.png"
canvas.save(preview)
checkerboard(canvas).save(checker_preview)

for name, image in {
    "MaterialSlot": slot,
    "OutputPreviewPanel": output_panel,
    "SmeltButton": smelt_button,
}.items():
    zoom = image.resize((image.width * 4, image.height * 4), Image.Resampling.NEAREST)
    checkerboard(zoom, 32).save(PREVIEWS / f"Smelting_{name}_SplitV01_400Percent.png")

states_preview = Image.new("RGBA", (smelt_button.width * 4, smelt_button.height), (0, 0, 0, 0))
for index, state in enumerate(("Normal", "Hover", "Pressed", "Disabled")):
    image = Image.open(CANDIDATES / f"Smelting_SmeltButton_{state}_{smelt_button.width}x{smelt_button.height}.png").convert("RGBA")
    states_preview.alpha_composite(image, (index * smelt_button.width, 0))
checkerboard(states_preview).save(PREVIEWS / "Smelting_SmeltButton_SplitV01_FourStates.png")

template_path = TEMPLATES / f"Smelting_CleanTemplate_Empty_{panel.width}x{panel.height}.png"
clean_low_alpha(panel).save(template_path)

coordinates = {
    "MainPanelBase": {"targetRegion": list(boxes["MainPanelBase"]), "visibleBounds": list(boxes["MainPanelBase"]), "cropOffset": [0, 0], "reassembly": list(panel_origin)},
    "MaterialSlot": {"targetRegion": list(boxes["MaterialSlot"]), "visibleBounds": list(boxes["MaterialSlot"]), "cropOffset": [0, 0], "reassembly": slot_positions},
    "OutputPreviewPanel": {"targetRegion": list(boxes["OutputPreviewPanel"]), "visibleBounds": list(boxes["OutputPreviewPanel"]), "cropOffset": [0, 0], "reassembly": list(boxes["OutputPreviewPanel"][:2])},
    "SmeltButton": {"targetRegion": list(boxes["SmeltButton"]), "visibleBounds": list(boxes["SmeltButton"]), "unionBounds": list(boxes["SmeltButton"]), "cropOffset": [0, 0], "reassembly": list(boxes["SmeltButton"][:2])},
    "CloseButton": {"targetRegion": [872, 110, 941, 180], "visibleBounds": [0, 0, 52, 50], "unionBounds": [0, 0, 52, 50], "cropOffset": [0, 0], "reassembly": [875, 114], "displaySize": [64, 62], "source": "Cook_CloseButton_{State}_52x50.png"},
}

manifest = {
    "version": "SplitV01",
    "panelSelectionMode": "AllDetected",
    "source": "FullUI/SmeltingUI_FullUI_Review02_1024x1536.png",
    "formalAutomationAuthorized": True,
    "candidateCount": len(list(CANDIDATES.glob("*.png"))),
    "coordinates": coordinates,
    "closeButtonHashParity": {
        state: {
            "source": sha256(COOK / f"Cook_CloseButton_{state}_52x50.png"),
            "candidate": sha256(CANDIDATES / f"Smelting_CloseButton_{state}_52x50.png"),
        }
        for state in ("Normal", "Hover", "Pressed", "Disabled")
    },
}
(QA / "split_v01_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps({
    "candidateCount": manifest["candidateCount"],
    "candidateFolder": str(CANDIDATES),
    "preview": str(preview),
    "checkerboard": str(checker_preview),
    "template": str(template_path),
}, ensure_ascii=False, indent=2))
