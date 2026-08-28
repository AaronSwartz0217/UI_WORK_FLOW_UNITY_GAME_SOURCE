from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
import hashlib
import json
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "FullUI" / "CharacterAttributesUI_FullUI_Review02_1024x1536.png"
CANDIDATES = ROOT / "into" / "Candidates" / "PrecisionCutoutV03"
PREVIEWS = ROOT / "into" / "ReassemblyPreview"
QA = ROOT / "QA"
COOK = ROOT.parents[1] / "01_References" / "Style" / "Standards" / "Primary_Cook"

CANDIDATES.mkdir(parents=True, exist_ok=True)
PREVIEWS.mkdir(parents=True, exist_ok=True)
QA.mkdir(parents=True, exist_ok=True)

src = Image.open(SOURCE).convert("RGBA")


def polygon_mask(size, points, supersample=4):
    w, h = size
    large = Image.new("L", (w * supersample, h * supersample), 0)
    draw = ImageDraw.Draw(large)
    draw.polygon([(x * supersample, y * supersample) for x, y in points], fill=255)
    mask = large.resize((w, h), Image.Resampling.LANCZOS)
    pixels = mask.load()
    for y in range(h):
        for x in range(w):
            if pixels[x, y] < 5:
                pixels[x, y] = 0
    return mask


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


def cut_progress_fill(box, chamfer=6):
    image = src.crop(box).convert("RGBA")
    w, h = image.size
    points = [(chamfer, 0), (w - 1, 0), (w - 1, h - 1), (chamfer, h - 1), (0, h - 1 - chamfer), (0, chamfer)]
    image.putalpha(polygon_mask(image.size, points))
    return image


def feathered_texture_fill(image, image_origin, abs_region, texture):
    ix, iy = image_origin
    x0, y0, x1, y1 = abs_region
    local = (x0 - ix, y0 - iy, x1 - ix, y1 - iy)
    lx0, ly0, lx1, ly1 = local
    target_width = lx1 - lx0
    target_height = ly1 - ly0
    patch = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 255))
    tile_width, tile_height = texture.size
    row = 0
    for y in range(0, target_height, tile_height):
        column = 0
        for x in range(0, target_width, tile_width):
            tile = texture
            if column % 2:
                tile = ImageOps.mirror(tile)
            if row % 2:
                tile = ImageOps.flip(tile)
            patch.alpha_composite(tile, (x, y))
            column += 1
        row += 1
    mask = Image.new("L", patch.size, 0)
    ImageDraw.Draw(mask).rectangle((10, 10, patch.width - 11, patch.height - 11), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(9))
    image.paste(patch, (lx0, ly0), mask)


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
    image = image.copy()
    alpha = image.getchannel("A").point(lambda value: 0 if value <= 5 else value)
    image.putalpha(alpha)
    name = f"CharacterAttributes_{component}_{state}_{image.width}x{image.height}.png"
    image.save(CANDIDATES / name)
    return name


def checkerboard(image, cell=16):
    background = Image.new("RGB", image.size, "white")
    draw = ImageDraw.Draw(background)
    for y in range(0, image.height, cell):
        for x in range(0, image.width, cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, min(x + cell - 1, image.width - 1), min(y + cell - 1, image.height - 1)), fill=(190, 190, 190))
    background.paste(image, mask=image.getchannel("A"))
    return background


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


# Hand-audited bounds from the confirmed 1024x1536 full UI. These boxes stop on
# the outermost component edge and never include the surrounding parent texture.
boxes = {
    "MainPanelBase": (30, 97, 994, 1463),
    "NormalAttributesTabButton": (63, 127, 253, 198),
    "VariantAttributesTabButton": (263, 127, 448, 198),
    "ExperienceTrack": (81, 456, 942, 535),
    "SatietyTrack": (81, 558, 942, 631),
    "ExperienceFill": (91, 568, 617, 621),
    "SatietyFill": (91, 568, 617, 621),
    "AttributeRowShort": (82, 671, 463, 747),
    "AttributeRowLong": (495, 671, 943, 747),
}

panel = cut_chamfered(boxes["MainPanelBase"], 14)
panel_origin = boxes["MainPanelBase"][:2]
texture = src.crop((462, 216, 955, 435)).convert("RGBA")
feathered_texture_fill(panel, panel_origin, (52, 112, 978, 214), texture)
feathered_texture_fill(panel, panel_origin, (66, 438, 958, 1440), texture)

tab_normal = cut_chamfered(boxes["NormalAttributesTabButton"], 8)
tab_variant = cut_chamfered(boxes["VariantAttributesTabButton"], 8)
experience_track = cut_chamfered(boxes["ExperienceTrack"], 8)
satiety_track = experience_track.resize(
    (boxes["SatietyTrack"][2] - boxes["SatietyTrack"][0], boxes["SatietyTrack"][3] - boxes["SatietyTrack"][1]),
    Image.Resampling.LANCZOS,
)
experience_fill = cut_progress_fill(boxes["ExperienceFill"])
satiety_fill = experience_fill.copy()
short_row = cut_chamfered(boxes["AttributeRowShort"], 8)
long_row = cut_chamfered(boxes["AttributeRowLong"], 8)

save(panel, "MainPanelBase", "Empty")
for component, normal in (
    ("NormalAttributesTabButton", tab_normal),
    ("VariantAttributesTabButton", tab_variant),
):
    for state, image in make_states(normal).items():
        save(image, component, state)
save(experience_track, "ExperienceTrack", "Empty")
save(satiety_track, "SatietyTrack", "Empty")
save(experience_fill, "ExperienceFill", "Default")
save(satiety_fill, "SatietyFill", "Default")
save(short_row, "AttributeRowShort", "Empty")
save(long_row, "AttributeRowLong", "Empty")

for state in ("Normal", "Hover", "Pressed", "Disabled"):
    source = COOK / f"Cook_CloseButton_{state}_52x50.png"
    target = CANDIDATES / f"CharacterAttributes_CloseButton_{state}_52x50.png"
    shutil.copy2(source, target)

canvas = Image.new("RGBA", src.size, (0, 0, 0, 0))
canvas.alpha_composite(panel, panel_origin)
canvas.alpha_composite(tab_normal, boxes["NormalAttributesTabButton"][:2])
canvas.alpha_composite(tab_variant, boxes["VariantAttributesTabButton"][:2])
close = Image.open(CANDIDATES / "CharacterAttributes_CloseButton_Normal_52x50.png").convert("RGBA")
canvas.alpha_composite(close.resize((62, 60), Image.Resampling.LANCZOS), (899, 136))
canvas.alpha_composite(experience_track, boxes["ExperienceTrack"][:2])
canvas.alpha_composite(satiety_track, boxes["SatietyTrack"][:2])
canvas.alpha_composite(satiety_fill, boxes["SatietyFill"][:2])

short_positions = [(82, y) for y in (671, 755, 839, 923, 1007)]
long_positions = [(495, y) for y in (671, 755, 839, 923, 1007, 1091, 1175, 1259, 1343)]
for position in short_positions:
    canvas.alpha_composite(short_row, position)
for position in long_positions:
    canvas.alpha_composite(long_row, position)

preview = PREVIEWS / "CharacterAttributes_PrecisionV03_Reassembled.png"
checker_preview = PREVIEWS / "CharacterAttributes_PrecisionV03_Reassembled_Checkerboard.png"
canvas.save(preview)
checkerboard(canvas, 32).save(checker_preview)

review_components = {
    "NormalAttributesTabButton": tab_normal,
    "VariantAttributesTabButton": tab_variant,
    "ExperienceTrack": experience_track,
    "SatietyFill": satiety_fill,
    "AttributeRowShort": short_row,
    "AttributeRowLong": long_row,
}
for key, image in review_components.items():
    zoom = image.resize((image.width * 4, image.height * 4), Image.Resampling.NEAREST)
    checkerboard(zoom, 32).save(PREVIEWS / f"CharacterAttributes_PrecisionV03_{key}_400Percent.png")

coordinates = {}
for component, box in boxes.items():
    coordinates[component] = {
        "targetRegion": list(box),
        "visibleBounds": list(box),
        "cropOffset": [0, 0],
        "reassembly": list(box[:2]),
    }
coordinates["CloseButton"] = {
    "targetRegion": [890, 128, 960, 195],
    "visibleBounds": [0, 0, 52, 50],
    "cropOffset": [0, 0],
    "reassembly": [899, 136],
    "displaySize": [62, 60],
    "source": "Cook_CloseButton_{State}_52x50.png",
}

files = sorted(CANDIDATES.glob("*.png"))
manifest = {
    "stage": "precision_cutout_candidate_v03",
    "formalPromotion": "blocked_until_visual_QA",
    "source": "FullUI/CharacterAttributesUI_FullUI_Review02_1024x1536.png",
    "alphaMethod": "hand-audited source bounds plus supersampled chamfer silhouette; no exterior parent pixels",
    "componentCount": len(files),
    "coordinates": coordinates,
    "repeatedReassembly": {
        "AttributeRowShort": short_positions,
        "AttributeRowLong": long_positions,
    },
    "closeButtonHashParity": {
        state: {
            "source": sha256(COOK / f"Cook_CloseButton_{state}_52x50.png"),
            "candidate": sha256(CANDIDATES / f"CharacterAttributes_CloseButton_{state}_52x50.png"),
        }
        for state in ("Normal", "Hover", "Pressed", "Disabled")
    },
}
(QA / "precision_cutout_v03_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

print(json.dumps({
    "candidateCount": len(files),
    "candidateFolder": str(CANDIDATES),
    "preview": str(preview),
    "checkerboard": str(checker_preview),
}, ensure_ascii=False, indent=2))
