from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
import hashlib
import json
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "FullUI" / "EquipmentEnchantingUI_FullUI_Review02_1024x1536.png"
CANDIDATES = ROOT / "into" / "Candidates" / "SplitV01"
PREVIEWS = ROOT / "into" / "ReassemblyPreview"
FORMAL = ROOT / "Components" / "out" / "EquipmentEnchantingUI"
TEMPLATES = ROOT / "Templates"
QA = ROOT / "QA"
COOK = ROOT.parents[1] / "01_References" / "Style" / "Standards" / "Primary_Cook"
SECONDARY = ROOT.parents[1] / "01_References" / "Style" / "Standards" / "Secondary_EquipmentIdentification"

for folder in (CANDIDATES, PREVIEWS, FORMAL, TEMPLATES, QA):
    folder.mkdir(parents=True, exist_ok=True)

src = Image.open(SOURCE).convert("RGBA")


def polygon_mask(size, points, supersample=8):
    width, height = size
    large = Image.new("L", (width * supersample, height * supersample), 0)
    ImageDraw.Draw(large).polygon([(x * supersample, y * supersample) for x, y in points], fill=255)
    return large.resize(size, Image.Resampling.LANCZOS).point(lambda value: 0 if value <= 5 else value)


def chamfer_points(width, height, chamfer):
    right, bottom = width - 1, height - 1
    return [
        (chamfer, 0), (right - chamfer, 0), (right, chamfer),
        (right, bottom - chamfer), (right - chamfer, bottom),
        (chamfer, bottom), (0, bottom - chamfer), (0, chamfer),
    ]


def cut_chamfered(box, chamfer):
    image = src.crop(box).convert("RGBA")
    image.putalpha(polygon_mask(image.size, chamfer_points(image.width, image.height, chamfer)))
    return image


def pad_transparent(image, padding):
    result = Image.new("RGBA", (image.width + padding * 2, image.height + padding * 2), (0, 0, 0, 0))
    result.alpha_composite(image, (padding, padding))
    return result


def tiled_texture(size, texture):
    result = Image.new("RGBA", size, (8, 8, 8, 255))
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


def fill_local(image, region, synthetic, feather=0):
    x0, y0, x1, y1 = region
    patch = synthetic.crop(region)
    width, height = patch.size
    if feather:
        mask = Image.new("L", patch.size, 0)
        ImageDraw.Draw(mask).rectangle((feather, feather, width - feather - 1, height - feather - 1), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(feather))
    else:
        mask = Image.new("L", patch.size, 255)
    image.paste(patch, (x0, y0), mask)


def clean_child_regions(image, soft_regions, hard_regions, texture):
    synthetic = tiled_texture(image.size, texture).filter(ImageFilter.GaussianBlur(0.25))
    for region in soft_regions:
        fill_local(image, region, synthetic, feather=16)
    for region in hard_regions:
        fill_local(image, region, synthetic, feather=0)
    return image


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
    filename = f"EquipmentEnchanting_{component}_{state}_{image.width}x{image.height}.png"
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
    "MainPanelBase": (27, 100, 996, 1477),
    "EquipmentDisplayPanel": (58, 203, 965, 459),
    "EquipmentSlot": (412, 241, 601, 429),
    "AttributeListPanel": (58, 473, 965, 985),
    "AttributeRow": (131, 501, 886, 585),
    "AttributeToggleSlot": (792, 510, 862, 580),
    "MaterialPanel": (58, 998, 965, 1219),
    "MaterialCard": (522, 1033, 924, 1187),
    "MaterialSlot": (540, 1053, 656, 1169),
    "ControlPanel": (58, 1233, 965, 1452),
    "EnchantButton": (331, 1266, 690, 1353),
    "ModeCheckbox": (463, 1369, 518, 1425),
}

base_texture = src.crop((100, 225, 380, 430)).convert("RGBA")

main = cut_chamfered(boxes["MainPanelBase"], 15)
main = clean_child_regions(
    main,
    soft_regions=[(760, 10, 950, 115), (15, 80, 950, 1370)],
    hard_regions=[(770, 12, 945, 105), (20, 92, 945, 1365)],
    texture=base_texture,
)
main.putalpha(polygon_mask(main.size, chamfer_points(main.width, main.height, 15)))

equipment_panel = cut_chamfered(boxes["EquipmentDisplayPanel"], 11)
equipment_panel = clean_child_regions(
    equipment_panel,
    soft_regions=[(320, 20, 585, 238)],
    hard_regions=[(340, 28, 565, 232)],
    texture=base_texture,
)
equipment_panel.putalpha(polygon_mask(equipment_panel.size, chamfer_points(equipment_panel.width, equipment_panel.height, 11)))

equipment_slot = cut_chamfered(boxes["EquipmentSlot"], 8)

attribute_panel = cut_chamfered(boxes["AttributeListPanel"], 11)
attribute_panel = clean_child_regions(
    attribute_panel,
    soft_regions=[(45, 10, 865, 505)],
    hard_regions=[(60, 18, 850, 495)],
    texture=base_texture,
)
attribute_panel.putalpha(polygon_mask(attribute_panel.size, chamfer_points(attribute_panel.width, attribute_panel.height, 11)))

attribute_row = cut_chamfered(boxes["AttributeRow"], 8)
attribute_row = clean_child_regions(
    attribute_row,
    soft_regions=[(630, 2, 748, 82)],
    hard_regions=[(648, 6, 738, 78)],
    texture=base_texture,
)
attribute_row.putalpha(polygon_mask(attribute_row.size, chamfer_points(attribute_row.width, attribute_row.height, 8)))
obsolete_toggle = CANDIDATES / "EquipmentEnchanting_AttributeToggleSlot_Empty_64x64.png"
if obsolete_toggle.exists():
    obsolete_toggle.unlink()
toggle_slot = pad_transparent(cut_chamfered(boxes["AttributeToggleSlot"], 7), 2)

material_panel = cut_chamfered(boxes["MaterialPanel"], 11)
material_panel = clean_child_regions(
    material_panel,
    soft_regions=[(20, 12, 890, 210)],
    hard_regions=[(30, 20, 880, 202)],
    texture=base_texture,
)
material_panel.putalpha(polygon_mask(material_panel.size, chamfer_points(material_panel.width, material_panel.height, 11)))

material_card = cut_chamfered(boxes["MaterialCard"], 8)
material_card = clean_child_regions(
    material_card,
    soft_regions=[(2, 2, 155, 152)],
    hard_regions=[(8, 8, 145, 146)],
    texture=base_texture,
)
material_card.putalpha(polygon_mask(material_card.size, chamfer_points(material_card.width, material_card.height, 8)))
material_slot = cut_chamfered(boxes["MaterialSlot"], 7)

control_panel = cut_chamfered(boxes["ControlPanel"], 11)
control_panel = clean_child_regions(
    control_panel,
    soft_regions=[(250, 12, 660, 205)],
    hard_regions=[(265, 20, 645, 200)],
    texture=base_texture,
)
control_panel.putalpha(polygon_mask(control_panel.size, chamfer_points(control_panel.width, control_panel.height, 11)))

enchant_button = cut_chamfered(boxes["EnchantButton"], 10)
mode_checkbox = cut_chamfered(boxes["ModeCheckbox"], 5)

for component, image in (
    ("MainPanelBase", main),
    ("EquipmentDisplayPanel", equipment_panel),
    ("EquipmentSlot", equipment_slot),
    ("AttributeListPanel", attribute_panel),
    ("AttributeRow", attribute_row),
    ("AttributeToggleSlot", toggle_slot),
    ("MaterialPanel", material_panel),
    ("MaterialCard", material_card),
    ("MaterialSlot", material_slot),
    ("ControlPanel", control_panel),
    ("ModeCheckbox", mode_checkbox),
):
    save(image, component, "Empty")

for state, image in make_states(enchant_button).items():
    save(image, "EnchantButton", state)

for state in ("Normal", "Hover", "Pressed", "Disabled"):
    help_source = SECONDARY / f"EquipmentIdentification_HelpButton_{state}_52x56.png"
    help_target = CANDIDATES / f"EquipmentEnchanting_HelpButton_{state}_52x56.png"
    shutil.copy2(help_source, help_target)
    close_source = COOK / f"Cook_CloseButton_{state}_52x50.png"
    close_target = CANDIDATES / f"EquipmentEnchanting_CloseButton_{state}_52x50.png"
    shutil.copy2(close_source, close_target)

row_positions = [(131, y) for y in (501, 595, 688, 782, 876)]
toggle_positions = [(790, y) for y in (508, 602, 696, 790, 884)]
card_positions = [(99, 1033), (522, 1033)]
material_slot_positions = [(116, 1053), (540, 1053)]

canvas = Image.new("RGBA", src.size, (0, 0, 0, 0))
canvas.alpha_composite(main, boxes["MainPanelBase"][:2])
canvas.alpha_composite(equipment_panel, boxes["EquipmentDisplayPanel"][:2])
canvas.alpha_composite(equipment_slot, boxes["EquipmentSlot"][:2])
canvas.alpha_composite(attribute_panel, boxes["AttributeListPanel"][:2])
for position in row_positions:
    canvas.alpha_composite(attribute_row, position)
for position in toggle_positions:
    canvas.alpha_composite(toggle_slot, position)
canvas.alpha_composite(material_panel, boxes["MaterialPanel"][:2])
for position in card_positions:
    canvas.alpha_composite(material_card, position)
for position in material_slot_positions:
    canvas.alpha_composite(material_slot, position)
canvas.alpha_composite(control_panel, boxes["ControlPanel"][:2])
canvas.alpha_composite(enchant_button, boxes["EnchantButton"][:2])
canvas.alpha_composite(mode_checkbox, boxes["ModeCheckbox"][:2])

help_normal = Image.open(CANDIDATES / "EquipmentEnchanting_HelpButton_Normal_52x56.png").convert("RGBA")
close_normal = Image.open(CANDIDATES / "EquipmentEnchanting_CloseButton_Normal_52x50.png").convert("RGBA")
canvas.alpha_composite(help_normal.resize((58, 62), Image.Resampling.LANCZOS), (823, 126))
canvas.alpha_composite(close_normal.resize((58, 56), Image.Resampling.LANCZOS), (892, 128))

preview = PREVIEWS / "EquipmentEnchanting_Reassembled_SplitV01_1024x1536.png"
checker_preview = PREVIEWS / "EquipmentEnchanting_Reassembled_SplitV01_Checkerboard_1024x1536.png"
canvas.save(preview)
checkerboard(canvas).save(checker_preview)

for name, image in {
    "AttributeRow": attribute_row,
    "MaterialCard": material_card,
    "EquipmentSlot": equipment_slot,
    "EnchantButton": enchant_button,
}.items():
    zoom = image.resize((image.width * 4, image.height * 4), Image.Resampling.NEAREST)
    checkerboard(zoom, 32).save(PREVIEWS / f"EquipmentEnchanting_{name}_SplitV01_400Percent.png")

states_preview = Image.new("RGBA", (enchant_button.width * 4, enchant_button.height), (0, 0, 0, 0))
for index, state in enumerate(("Normal", "Hover", "Pressed", "Disabled")):
    image = Image.open(CANDIDATES / f"EquipmentEnchanting_EnchantButton_{state}_{enchant_button.width}x{enchant_button.height}.png").convert("RGBA")
    states_preview.alpha_composite(image, (index * enchant_button.width, 0))
checkerboard(states_preview).save(PREVIEWS / "EquipmentEnchanting_EnchantButton_SplitV01_FourStates.png")

clean_low_alpha(main).save(TEMPLATES / f"EquipmentEnchanting_CleanTemplate_Empty_{main.width}x{main.height}.png")

coordinates = {
    component: {"targetRegion": list(box), "visibleBounds": list(box), "cropOffset": [0, 0], "reassembly": list(box[:2])}
    for component, box in boxes.items()
}
coordinates["AttributeRow"]["reassembly"] = row_positions
coordinates["AttributeToggleSlot"]["reassembly"] = toggle_positions
coordinates["AttributeToggleSlot"]["visibleBounds"] = [2, 2, 72, 72]
coordinates["AttributeToggleSlot"]["cropOffset"] = [-2, -2]
coordinates["MaterialCard"]["reassembly"] = card_positions
coordinates["MaterialSlot"]["reassembly"] = material_slot_positions
coordinates["EnchantButton"]["unionBounds"] = list(boxes["EnchantButton"])
coordinates["HelpButton"] = {"targetRegion": [820, 122, 885, 190], "visibleBounds": [0, 0, 52, 56], "unionBounds": [0, 0, 52, 56], "cropOffset": [0, 0], "reassembly": [823, 126], "displaySize": [58, 62]}
coordinates["CloseButton"] = {"targetRegion": [889, 122, 955, 190], "visibleBounds": [0, 0, 52, 50], "unionBounds": [0, 0, 52, 50], "cropOffset": [0, 0], "reassembly": [892, 128], "displaySize": [58, 56]}

manifest = {
    "version": "SplitV01",
    "panelSelectionMode": "AllDetected",
    "source": "FullUI/EquipmentEnchantingUI_FullUI_Review02_1024x1536.png",
    "formalAutomationAuthorized": True,
    "candidateCount": len(list(CANDIDATES.glob("*.png"))),
    "coordinates": coordinates,
    "canonicalHashParity": {
        "HelpButton": {state: sha256(SECONDARY / f"EquipmentIdentification_HelpButton_{state}_52x56.png") == sha256(CANDIDATES / f"EquipmentEnchanting_HelpButton_{state}_52x56.png") for state in ("Normal", "Hover", "Pressed", "Disabled")},
        "CloseButton": {state: sha256(COOK / f"Cook_CloseButton_{state}_52x50.png") == sha256(CANDIDATES / f"EquipmentEnchanting_CloseButton_{state}_52x50.png") for state in ("Normal", "Hover", "Pressed", "Disabled")},
    },
}
(QA / "split_v01_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps({
    "candidateCount": manifest["candidateCount"],
    "candidateFolder": str(CANDIDATES),
    "preview": str(preview),
    "checkerboard": str(checker_preview),
}, ensure_ascii=False, indent=2))
