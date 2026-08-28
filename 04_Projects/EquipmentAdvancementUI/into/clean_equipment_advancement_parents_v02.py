from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import json
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FULL_UI = ROOT / "FullUI" / "EquipmentAdvancementUI_FullUI_Review02.png"
FORMAL = ROOT / "Components" / "out" / "EquipmentAdvancementUI"
CANDIDATES = ROOT / "into" / "Candidates" / "CleanParentV02"
PREVIEWS = ROOT / "into" / "ReassemblyPreview"
QA = ROOT / "QA"

CANDIDATES.mkdir(parents=True, exist_ok=True)
PREVIEWS.mkdir(parents=True, exist_ok=True)

for source in FORMAL.glob("*.png"):
    shutil.copy2(source, CANDIDATES / source.name)

full_ui = Image.open(SOURCE_FULL_UI).convert("RGBA")
# Blank black-steel area inside the approved top equipment panel. It contains no
# labels, controls, slots, or borders and therefore provides a faithful texture.
texture = full_ui.crop((150, 220, 430, 410)).convert("RGBA")
texture.save(PREVIEWS / "EquipmentAdvancementUI_CleanTextureSourceV02.png")


def tiled_texture(size):
    width, height = size
    result = Image.new("RGBA", size, (0, 0, 0, 255))
    tile_width, tile_height = texture.size
    for row, y in enumerate(range(0, height, tile_height)):
        for column, x in enumerate(range(0, width, tile_width)):
            tile = texture
            if column % 2:
                tile = ImageOps.mirror(tile)
            if row % 2:
                tile = ImageOps.flip(tile)
            result.alpha_composite(tile, (x, y))
    return result


def clean_interior(filename, inset_x, inset_y, feather):
    path = CANDIDATES / filename
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    x0, y0 = inset_x, inset_y
    x1, y1 = image.width - inset_x, image.height - inset_y
    patch = tiled_texture((x1 - x0, y1 - y0))
    mask = Image.new("L", patch.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((feather, feather, patch.width - feather - 1, patch.height - feather - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    image.paste(patch, (x0, y0), mask)
    image.putalpha(alpha)
    image.save(path)


clean_specs = {
    "EquipmentAdvancement_MainPanelBase_Default_985x1384.png": (24, 27, 10),
    "EquipmentAdvancement_TopEquipmentPanel_Empty_883x332.png": (28, 28, 9),
    "EquipmentAdvancement_QualityPanel_Empty_880x211.png": (28, 28, 9),
    "EquipmentAdvancement_EquipmentPairPanel_Empty_880x282.png": (28, 28, 9),
    "EquipmentAdvancement_ProgressActionPanel_Empty_880x307.png": (28, 28, 9),
    "EquipmentAdvancement_LeftEquipmentRow_Empty_351x127.png": (18, 18, 7),
    "EquipmentAdvancement_RightEquipmentRow_Empty_355x127.png": (18, 18, 7),
}

for filename, (inset_x, inset_y, feather) in clean_specs.items():
    clean_interior(filename, inset_x, inset_y, feather)


regions = {
    "MainPanelBase": (47, 43),
    "TopEquipmentPanel": (96, 168),
    "QualityPanel": (97, 529),
    "EquipmentPairPanel": (98, 774),
    "ProgressActionPanel": (98, 1083),
    "LeftEquipmentRow": (175, 849),
    "RightEquipmentRow": (553, 849),
    "TopEquipmentSlot": (458, 218),
    "LeftEquipmentSlot": (191, 867),
    "RightEquipmentSlot": (571, 867),
    "QualityArrow": (516, 608),
    "ProgressTrack": (174, 1117),
    "ProgressFill": (174, 1117),
    "HelpButton": (847, 76),
    "CloseButton": (936, 75),
    "AdvanceButton": (345, 1244),
}

normal_files = {
    "MainPanelBase": "EquipmentAdvancement_MainPanelBase_Default_985x1384.png",
    "TopEquipmentPanel": "EquipmentAdvancement_TopEquipmentPanel_Empty_883x332.png",
    "QualityPanel": "EquipmentAdvancement_QualityPanel_Empty_880x211.png",
    "EquipmentPairPanel": "EquipmentAdvancement_EquipmentPairPanel_Empty_880x282.png",
    "ProgressActionPanel": "EquipmentAdvancement_ProgressActionPanel_Empty_880x307.png",
    "LeftEquipmentRow": "EquipmentAdvancement_LeftEquipmentRow_Empty_351x127.png",
    "RightEquipmentRow": "EquipmentAdvancement_RightEquipmentRow_Empty_355x127.png",
    "TopEquipmentSlot": "EquipmentAdvancement_TopEquipmentSlot_Default_158x165.png",
    "LeftEquipmentSlot": "EquipmentAdvancement_LeftEquipmentSlot_Default_86x89.png",
    "RightEquipmentSlot": "EquipmentAdvancement_RightEquipmentSlot_Default_86x89.png",
    "QualityArrow": "EquipmentAdvancement_QualityArrow_Default_56x47.png",
    "ProgressTrack": "EquipmentAdvancement_ProgressTrack_Default_732x38.png",
    "ProgressFill": "EquipmentAdvancement_ProgressFill_Default_143x38.png",
    "HelpButton": "EquipmentAdvancement_HelpButton_Normal_69x65.png",
    "CloseButton": "EquipmentAdvancement_CloseButton_Normal_69x67.png",
    "AdvanceButton": "EquipmentAdvancement_AdvanceButton_Normal_384x103.png",
}

canvas = Image.new("RGBA", full_ui.size, (0, 0, 0, 0))
for component in (
    "MainPanelBase",
    "TopEquipmentPanel",
    "QualityPanel",
    "EquipmentPairPanel",
    "ProgressActionPanel",
    "LeftEquipmentRow",
    "RightEquipmentRow",
    "TopEquipmentSlot",
    "LeftEquipmentSlot",
    "RightEquipmentSlot",
    "QualityArrow",
    "ProgressTrack",
    "ProgressFill",
    "HelpButton",
    "CloseButton",
    "AdvanceButton",
):
    component_image = Image.open(CANDIDATES / normal_files[component]).convert("RGBA")
    canvas.alpha_composite(component_image, regions[component])

preview = PREVIEWS / "EquipmentAdvancementUI_Reassembly_CleanParentV02_1078x1459.png"
checker = PREVIEWS / "EquipmentAdvancementUI_Reassembly_CleanParentV02_Checkerboard_1078x1459.png"
canvas.save(preview)

background = Image.new("RGB", canvas.size, "white")
draw = ImageDraw.Draw(background)
cell = 24
for y in range(0, canvas.height, cell):
    for x in range(0, canvas.width, cell):
        if (x // cell + y // cell) % 2:
            draw.rectangle((x, y, min(x + cell - 1, canvas.width - 1), min(y + cell - 1, canvas.height - 1)), fill=(188, 188, 188))
background.paste(canvas, mask=canvas.getchannel("A"))
background.save(checker)

for filename in clean_specs:
    image = Image.open(CANDIDATES / filename).convert("RGBA")
    zoom = image.resize((image.width * 4, image.height * 4), Image.Resampling.NEAREST)
    zoom.save(PREVIEWS / f"{Path(filename).stem}_CleanParentV02_400Percent.png")

manifest = {
    "version": "CleanParentV02",
    "sourceFullUI": "FullUI/EquipmentAdvancementUI_FullUI_Review02.png",
    "candidateCount": len(list(CANDIDATES.glob("*.png"))),
    "cleanedParents": list(clean_specs),
    "textureSourceRegion": [150, 220, 430, 410],
    "method": "same-source blank texture mirrored at original pixel density with feathered interior transitions",
    "preview": str(preview.relative_to(ROOT)),
    "checkerboard": str(checker.relative_to(ROOT)),
}
(QA / "clean_parent_v02_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps(manifest, ensure_ascii=False, indent=2))
