from pathlib import Path
from collections import deque
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "FullUI" / "CharacterAttributesUI_FullUI_Review02_1024x1536.png"
CANDIDATES = ROOT / "into" / "Candidates" / "PrecisionCutoutV02"
PREVIEWS = ROOT / "into" / "ReassemblyPreview"
COOK = ROOT.parents[1] / "01_References" / "Style" / "Standards" / "Primary_Cook"

CANDIDATES.mkdir(parents=True, exist_ok=True)
PREVIEWS.mkdir(parents=True, exist_ok=True)
src = Image.open(SOURCE).convert("RGBA")

def dilate(mask, iterations=1):
    value = mask.copy()
    for _ in range(iterations):
        padded = np.pad(value, 1, mode="constant")
        value = np.logical_or.reduce([
            padded[dy:dy+value.shape[0], dx:dx+value.shape[1]]
            for dy in range(3) for dx in range(3)
        ])
    return value

def erode(mask, iterations=1):
    value = mask.copy()
    for _ in range(iterations):
        padded = np.pad(value, 1, mode="constant", constant_values=False)
        value = np.logical_and.reduce([
            padded[dy:dy+value.shape[0], dx:dx+value.shape[1]]
            for dy in range(3) for dx in range(3)
        ])
    return value

def close_mask(mask, iterations=1):
    return erode(dilate(mask, iterations), iterations)

def border_flood_open(open_pixels):
    h, w = open_pixels.shape
    outside = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        if open_pixels[0, x]: outside[0, x] = True; q.append((0, x))
        if open_pixels[h-1, x] and not outside[h-1, x]: outside[h-1, x] = True; q.append((h-1, x))
    for y in range(h):
        if open_pixels[y, 0] and not outside[y, 0]: outside[y, 0] = True; q.append((y, 0))
        if open_pixels[y, w-1] and not outside[y, w-1]: outside[y, w-1] = True; q.append((y, w-1))
    while q:
        y, x = q.popleft()
        if y and open_pixels[y-1, x] and not outside[y-1, x]:
            outside[y-1, x] = True; q.append((y-1, x))
        if y+1 < h and open_pixels[y+1, x] and not outside[y+1, x]:
            outside[y+1, x] = True; q.append((y+1, x))
        if x and open_pixels[y, x-1] and not outside[y, x-1]:
            outside[y, x-1] = True; q.append((y, x-1))
        if x+1 < w and open_pixels[y, x+1] and not outside[y, x+1]:
            outside[y, x+1] = True; q.append((y, x+1))
    return outside

def connected_from_seed(mask, seed):
    h, w = mask.shape
    sy, sx = seed
    if not mask[sy, sx]:
        ys, xs = np.where(mask)
        if len(xs) == 0:
            raise RuntimeError("No foreground detected")
        nearest = np.argmin((ys-sy)**2 + (xs-sx)**2)
        sy, sx = int(ys[nearest]), int(xs[nearest])
    component = np.zeros_like(mask)
    component[sy, sx] = True
    q = deque([(sy, sx)])
    while q:
        y, x = q.popleft()
        for ny, nx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not component[ny, nx]:
                component[ny, nx] = True
                q.append((ny, nx))
    return component

def precise_closed_cutout(abs_box, bright_floor=36, gradient_floor=18, close_iterations=2):
    crop = src.crop(abs_box).convert("RGBA")
    rgb = np.asarray(crop.convert("RGB"), dtype=np.int16)
    mx = rgb.max(axis=2)
    gray = (rgb[:,:,0]*30 + rgb[:,:,1]*59 + rgb[:,:,2]*11) // 100
    gx = np.zeros_like(gray)
    gy = np.zeros_like(gray)
    gx[:,1:] = np.abs(gray[:,1:] - gray[:,:-1])
    gy[1:,:] = np.abs(gray[1:,:] - gray[:-1,:])
    grad = np.maximum(gx, gy)
    border_values = np.concatenate((mx[:4,:].ravel(), mx[-4:,:].ravel(), mx[:,:4].ravel(), mx[:,-4:].ravel()))
    bright_threshold = max(bright_floor, int(np.percentile(border_values, 98)) + 10)
    amber = (rgb[:,:,0] > rgb[:,:,1]*1.15) & (rgb[:,:,0] > rgb[:,:,2]*1.35) & (rgb[:,:,0] > 38)
    barrier = (mx >= bright_threshold) | (grad >= gradient_floor) | amber
    barrier = close_mask(barrier, close_iterations)
    outside = border_flood_open(~barrier)
    enclosed = ~outside
    component = connected_from_seed(enclosed, (enclosed.shape[0]//2, enclosed.shape[1]//2))
    component = close_mask(component, 1)
    alpha = Image.fromarray((component.astype(np.uint8)*255), "L")
    soft = alpha.filter(ImageFilter.GaussianBlur(0.42))
    solid = Image.fromarray((erode(component, 1).astype(np.uint8)*255), "L")
    alpha = Image.fromarray(np.maximum(np.asarray(soft), np.asarray(solid)).astype(np.uint8), "L")
    low_clean = np.asarray(alpha).copy()
    low_clean[low_clean < 6] = 0
    alpha = Image.fromarray(low_clean, "L")
    bbox = alpha.getbbox()
    if not bbox:
        raise RuntimeError(f"Empty alpha for {abs_box}")
    rgba = crop.copy()
    rgba.putalpha(alpha)
    rgba = rgba.crop(bbox)
    x0, y0, _, _ = abs_box
    global_box = (x0+bbox[0], y0+bbox[1], x0+bbox[2], y0+bbox[3])
    return rgba, global_box

def amber_fill_cutout(abs_box):
    crop = src.crop(abs_box).convert("RGBA")
    rgb = np.asarray(crop.convert("RGB"), dtype=np.int16)
    seed = (rgb[:,:,0] > rgb[:,:,1]*1.12) & (rgb[:,:,0] > rgb[:,:,2]*1.55) & (rgb[:,:,0] > 34)
    seed = close_mask(seed, 3)
    ys, xs = np.where(seed)
    if len(xs) == 0:
        raise RuntimeError("Amber fill not found")
    y0, y1 = int(ys.min()), int(ys.max())
    body = np.zeros_like(seed)
    valid_rows = []
    for y in range(y0, y1+1):
        row = np.where(seed[y])[0]
        if len(row) >= 10:
            body[y, int(row.min()):int(row.max())+1] = True
            valid_rows.append(y)
    body = close_mask(body, 2)
    body = connected_from_seed(body, (int(np.mean(valid_rows)), int(np.median(xs))))
    alpha = Image.fromarray((body.astype(np.uint8)*255), "L").filter(ImageFilter.GaussianBlur(0.38))
    arr = np.asarray(alpha).copy()
    arr[arr < 6] = 0
    alpha = Image.fromarray(arr, "L")
    bbox = alpha.getbbox()
    rgba = crop.copy()
    rgba.putalpha(alpha)
    rgba = rgba.crop(bbox)
    x0, y0a, _, _ = abs_box
    global_box = (x0+bbox[0], y0a+bbox[1], x0+bbox[2], y0a+bbox[3])
    return rgba, global_box

def filename(component, state, image):
    return f"CharacterAttributes_{component}_{state}_{image.width}x{image.height}.png"

def save_candidate(image, component, state):
    name = filename(component, state, image)
    image.save(CANDIDATES / name)
    return name

def make_states(normal):
    alpha = normal.getchannel("A")
    disabled_rgb = ImageOps.grayscale(normal.convert("RGB")).convert("RGBA")
    states = {
        "Normal": normal,
        "Hover": ImageEnhance.Brightness(normal).enhance(1.16),
        "Pressed": ImageEnhance.Brightness(normal).enhance(0.78),
        "Disabled": ImageEnhance.Brightness(disabled_rgb).enhance(0.55),
    }
    for im in states.values():
        im.putalpha(alpha)
    return states

components = {}
coordinates = {}

panel, panel_bounds = precise_closed_cutout((20, 85, 1004, 1475), bright_floor=32, gradient_floor=16, close_iterations=3)
panel_origin = (panel_bounds[0], panel_bounds[1])
texture = src.crop((500, 250, 700, 400)).convert("RGBA")
for abs_region in [
    (52, 112, 463, 213),
    (872, 112, 979, 213),
    (66, 438, 958, 650),
    (66, 652, 480, 1164),
    (478, 652, 958, 1438),
]:
    rx0 = max(0, abs_region[0] - panel_origin[0])
    ry0 = max(0, abs_region[1] - panel_origin[1])
    rx1 = min(panel.width, abs_region[2] - panel_origin[0])
    ry1 = min(panel.height, abs_region[3] - panel_origin[1])
    if rx1 > rx0 and ry1 > ry0:
        patch = ImageOps.fit(texture, (rx1-rx0, ry1-ry0), Image.Resampling.BICUBIC)
        panel.alpha_composite(patch, (rx0, ry0))
components["MainPanelBase"] = panel
coordinates["MainPanelBase"] = {"targetRegion": [20,85,1004,1475], "visibleBounds": list(panel_bounds), "cropOffset": [panel_bounds[0]-20,panel_bounds[1]-85], "reassembly": list(panel_origin)}
save_candidate(panel, "MainPanelBase", "Empty")

tab_specs = {
    "NormalAttributesTabButton": (52, 114, 261, 210),
    "VariantAttributesTabButton": (253, 114, 462, 210),
}
for component, box in tab_specs.items():
    normal, bounds = precise_closed_cutout(box, bright_floor=32, gradient_floor=15, close_iterations=2)
    components[component] = normal
    coordinates[component] = {"targetRegion": list(box), "visibleBounds": list(bounds), "cropOffset": [bounds[0]-box[0],bounds[1]-box[1]], "reassembly": [bounds[0],bounds[1]], "unionBounds": list(bounds)}
    for state, image in make_states(normal).items():
        save_candidate(image, component, state)

track, track_bounds = precise_closed_cutout((70, 445, 954, 545), bright_floor=32, gradient_floor=14, close_iterations=2)
fill, fill_bounds = amber_fill_cutout((84, 563, 625, 631))
for component in ("ExperienceTrack", "SatietyTrack"):
    components[component] = track
    save_candidate(track, component, "Empty")
for component in ("ExperienceFill", "SatietyFill"):
    components[component] = fill
    save_candidate(fill, component, "Default")
coordinates["ExperienceTrack"] = {"targetRegion": [70,445,954,545], "visibleBounds": list(track_bounds), "cropOffset": [track_bounds[0]-70,track_bounds[1]-445], "reassembly": [track_bounds[0],track_bounds[1]]}
coordinates["SatietyTrack"] = {"targetRegion": [70,548,954,648], "visibleBounds": [track_bounds[0],track_bounds[1]+101,track_bounds[2],track_bounds[3]+101], "cropOffset": [track_bounds[0]-70,track_bounds[1]-445], "reassembly": [track_bounds[0],track_bounds[1]+101]}
coordinates["ExperienceFill"] = {"targetRegion": [84,563,625,631], "visibleBounds": list(fill_bounds), "cropOffset": [fill_bounds[0]-84,fill_bounds[1]-563], "reassembly": [fill_bounds[0],fill_bounds[1]]}
coordinates["SatietyFill"] = {"targetRegion": [84,563,625,631], "visibleBounds": list(fill_bounds), "cropOffset": [fill_bounds[0]-84,fill_bounds[1]-563], "reassembly": [fill_bounds[0],fill_bounds[1]]}

short_row, short_bounds = precise_closed_cutout((70, 660, 477, 760), bright_floor=30, gradient_floor=14, close_iterations=2)
long_row, long_bounds = precise_closed_cutout((483, 660, 955, 760), bright_floor=30, gradient_floor=14, close_iterations=2)
components["AttributeRowShort"] = short_row
components["AttributeRowLong"] = long_row
save_candidate(short_row, "AttributeRowShort", "Empty")
save_candidate(long_row, "AttributeRowLong", "Empty")
coordinates["AttributeRowShort"] = {"targetRegion": [70,660,477,760], "visibleBounds": list(short_bounds), "cropOffset": [short_bounds[0]-70,short_bounds[1]-660], "reassembly": [short_bounds[0],short_bounds[1]]}
coordinates["AttributeRowLong"] = {"targetRegion": [483,660,955,760], "visibleBounds": list(long_bounds), "cropOffset": [long_bounds[0]-483,long_bounds[1]-660], "reassembly": [long_bounds[0],long_bounds[1]]}

for state in ("Normal", "Hover", "Pressed", "Disabled"):
    source = COOK / f"Cook_CloseButton_{state}_52x50.png"
    target = CANDIDATES / f"CharacterAttributes_CloseButton_{state}_52x50.png"
    shutil.copy2(source, target)
coordinates["CloseButton"] = {
    "targetRegion": [890,128,960,195],
    "visibleBounds": [0,0,52,50],
    "cropOffset": [0,0],
    "reassembly": [899,136],
    "displaySize": [62,60],
    "source": "Cook_CloseButton_{State}_52x50.png"
}

canvas = Image.new("RGBA", src.size, (0,0,0,0))
canvas.alpha_composite(panel, panel_origin)
for component in tab_specs:
    image = components[component]
    pos = tuple(coordinates[component]["reassembly"])
    canvas.alpha_composite(image, pos)
close = Image.open(CANDIDATES / "CharacterAttributes_CloseButton_Normal_52x50.png").convert("RGBA")
close_display = close.resize((62,60), Image.Resampling.LANCZOS)
canvas.alpha_composite(close_display, (899,136))
canvas.alpha_composite(track, tuple(coordinates["ExperienceTrack"]["reassembly"]))
canvas.alpha_composite(track, tuple(coordinates["SatietyTrack"]["reassembly"]))
canvas.alpha_composite(fill, tuple(coordinates["SatietyFill"]["reassembly"]))
for y in (short_bounds[1], short_bounds[1]+84, short_bounds[1]+168, short_bounds[1]+251, short_bounds[1]+335):
    canvas.alpha_composite(short_row, (short_bounds[0], y))
for y in (long_bounds[1], long_bounds[1]+84, long_bounds[1]+168, long_bounds[1]+251, long_bounds[1]+335, long_bounds[1]+418, long_bounds[1]+502, long_bounds[1]+585, long_bounds[1]+669):
    canvas.alpha_composite(long_row, (long_bounds[0], y))
canvas.save(PREVIEWS / "CharacterAttributes_PrecisionV02_Reassembled.png")

def checkerboard(image, cell=16):
    bg = Image.new("RGB", image.size, "white")
    draw = ImageDraw.Draw(bg)
    for y in range(0, image.height, cell):
        for x in range(0, image.width, cell):
            if (x//cell + y//cell) % 2:
                draw.rectangle((x,y,min(x+cell-1,image.width-1),min(y+cell-1,image.height-1)), fill=(190,190,190))
    bg.paste(image, mask=image.getchannel("A"))
    return bg

checkerboard(canvas, 32).save(PREVIEWS / "CharacterAttributes_PrecisionV02_Reassembled_Checkerboard.png")
for key in ("NormalAttributesTabButton", "VariantAttributesTabButton", "AttributeRowShort", "AttributeRowLong", "ExperienceTrack", "SatietyFill"):
    image = components.get(key, fill if key == "SatietyFill" else None)
    zoom = image.resize((image.width*4, image.height*4), Image.Resampling.NEAREST)
    checkerboard(zoom, 32).save(PREVIEWS / f"CharacterAttributes_PrecisionV02_{key}_400Percent.png")

manifest = {
    "stage": "precision_cutout_candidate",
    "formalPromotion": "blocked_until_visual_QA",
    "source": "FullUI/CharacterAttributesUI_FullUI_Review02_1024x1536.png",
    "alphaMethod": "component-specific closed-contour edge barrier, exterior flood fill, interior solidification, subpixel edge feather",
    "lowAlphaCleanupThreshold": 6,
    "componentCount": len(list(CANDIDATES.glob("*.png"))),
    "coordinates": coordinates
}
(ROOT / "QA" / "precision_cutout_v02_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"candidateCount": manifest["componentCount"], "candidateFolder": str(CANDIDATES), "previewFolder": str(PREVIEWS)}, indent=2))
