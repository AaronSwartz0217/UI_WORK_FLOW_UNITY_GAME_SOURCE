from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Components" / "out" / "MainHUDUI"
INTO = ROOT / "into"
QA = ROOT / "QA"
TEMPLATES = ROOT / "Templates"
WIDTH, HEIGHT = 1559, 880
SCALE = 4


BUTTON_RECTS = {
    "ExpandArrowButton": (15, 15, 79, 39),
    "TeamInviteButton": (909, 31, 69, 21),
    "ModeDropdownButton": (1279, 15, 84, 40),
    "GMToolsButton": (1372, 15, 80, 39),
    "MenuButton": (1462, 15, 80, 39),
    "ReturnCityButton": (1306, 793, 62, 29),
    "RechargeButton": (1487, 838, 54, 25),
    "MutationButton": (1073, 809, 56, 56),
}

HOTBAR_X = [315, 372, 429, 496, 553, 609, 666, 722, 779, 835, 891, 948, 1004]

STATIC_RECTS = {
    "LowerHUDPlate": (15, 594, 1253, 282),
    "PartyHealthFill": (15, 72, 75, 12),
    "PartyManaFill": (15, 86, 75, 4),
    "PlayerHealthTrack": (576, 53, 406, 20),
    "PlayerHealthFill": (577, 54, 162, 17),
    "LoadingTrack": (576, 696, 405, 18),
    "LoadingFill": (577, 697, 119, 16),
    "MutationTrack": (496, 722, 566, 17),
    "MutationFill": (497, 723, 486, 15),
    "ResourceTrack": (455, 782, 646, 21),
    "ResourceHealthFill": (456, 782, 344, 20),
    "ResourceManaFill": (800, 782, 301, 20),
    "MinimapMeterTrack": (1268, 586, 23, 242),
    "MinimapMeterWarningFill": (1268, 586, 23, 81),
    "MinimapMeterDangerFill": (1268, 667, 23, 161),
    "MinimapPanel": (1303, 586, 239, 243),
    "CurrencyIconLeft": (1268, 836, 29, 29),
    "CurrencyPlateLeft": (1305, 836, 64, 29),
    "CurrencyIconRight": (1377, 836, 28, 29),
    "CurrencyPlateRight": (1412, 836, 69, 29),
}


def _scale_rgba(color, factor, grayscale=False):
    rgb = np.array(color[:3], dtype=np.float32)
    if grayscale:
        value = float(np.dot(rgb, [0.299, 0.587, 0.114]))
        rgb = np.array([value, value, value], dtype=np.float32)
    rgb = np.clip(rgb * factor, 0, 255).astype(np.uint8)
    return tuple(int(value) for value in rgb) + (int(color[3]),)


def rounded_gradient(size, top, bottom, radius, sheen=0, solid_interior=False):
    width, height = size
    sw, sh = width * SCALE, height * SCALE
    top_value = np.asarray(top, dtype=np.float32)
    bottom_value = np.asarray(bottom, dtype=np.float32)
    blend = np.linspace(0.0, 1.0, sh, dtype=np.float32)[:, None, None]
    pixels = np.broadcast_to(top_value, (sh, sw, 4)).copy()
    pixels += (bottom_value - top_value) * blend
    if solid_interior:
        pixels[:, :, 3] = 255
    layer = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8), "RGBA")

    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, sw - 1, sh - 1), radius=radius * SCALE, fill=255
    )
    alpha = np.asarray(layer.getchannel("A"), dtype=np.uint16)
    alpha = (alpha * np.asarray(mask, dtype=np.uint16) // 255).astype(np.uint8)
    layer.putalpha(Image.fromarray(alpha, "L"))

    if sheen:
        shine = Image.new("RGBA", (sw, sh), (255, 255, 255, 0))
        shine_alpha = np.zeros((sh, sw), dtype=np.uint8)
        shine_height = max(1, int(sh * 0.34))
        shine_alpha[:shine_height, :] = np.linspace(
            sheen, 0, shine_height, dtype=np.uint8
        )[:, None]
        shine_alpha = (
            shine_alpha.astype(np.uint16) * np.asarray(mask, dtype=np.uint16) // 255
        ).astype(np.uint8)
        shine.putalpha(Image.fromarray(shine_alpha, "L"))
        layer = Image.alpha_composite(layer, shine)

    return layer.resize((width, height), Image.Resampling.LANCZOS)


def button_art(name, size, state):
    if name in {"ModeDropdownButton"}:
        top, bottom = (76, 107, 143, 64), (30, 58, 87, 64)
    elif name == "MutationButton":
        top, bottom = (190, 28, 43, 72), (101, 5, 16, 72)
    else:
        top, bottom = (202, 220, 241, 64), (86, 116, 151, 64)

    if state == "Hover":
        top = _scale_rgba(top, 1.10)
        bottom = _scale_rgba(bottom, 1.10)
        sheen = 25
    elif state == "Pressed":
        top = _scale_rgba(top, 0.82)
        bottom = _scale_rgba(bottom, 0.82)
        sheen = 8
    elif state == "Disabled":
        top = _scale_rgba(top, 0.66, True)
        bottom = _scale_rgba(bottom, 0.66, True)
        sheen = 4
    else:
        sheen = 16

    radius = max(3, min(size) // 5)
    image = rounded_gradient(size, top, bottom, radius, sheen, solid_interior=False)
    # State appearance may change RGB/sheen, but the interaction silhouette must
    # use one identical alpha mask to prevent a one-pixel flicker on SpriteSwap.
    alpha_master = rounded_gradient(
        size,
        (0, 0, 0, top[3]),
        (0, 0, 0, bottom[3]),
        radius,
        0,
        solid_interior=False,
    ).getchannel("A")
    image.putalpha(alpha_master)
    draw = ImageDraw.Draw(image)
    if name == "ExpandArrowButton":
        cx, cy = size[0] // 2, size[1] // 2
        draw.line((cx - 3, cy - 6, cx + 4, cy), fill=(248, 250, 255, 238), width=2)
        draw.line((cx + 4, cy, cx - 3, cy + 6), fill=(248, 250, 255, 238), width=2)
    elif name == "ModeDropdownButton":
        cx, cy = size[0] - 16, size[1] // 2
        draw.line((cx - 5, cy - 2, cx, cy + 3), fill=(248, 250, 255, 238), width=2)
        draw.line((cx, cy + 3, cx + 5, cy - 2), fill=(248, 250, 255, 238), width=2)
    return image


def hotbar_art(state):
    top, bottom = (58, 87, 120, 64), (21, 45, 68, 64)
    if state == "Hover":
        top, bottom = _scale_rgba(top, 1.12), _scale_rgba(bottom, 1.12)
    elif state == "Pressed":
        top, bottom = _scale_rgba(top, 0.80), _scale_rgba(bottom, 0.80)
    elif state == "Disabled":
        top, bottom = _scale_rgba(top, 0.62, True), _scale_rgba(bottom, 0.62, True)
    elif state == "Selected":
        top, bottom = (72, 112, 153, 72), (25, 61, 91, 72)

    image = rounded_gradient((56, 56), top, bottom, 5, 7, solid_interior=False)
    alpha_master = rounded_gradient(
        (56, 56),
        (0, 0, 0, 64),
        (0, 0, 0, 64),
        5,
        0,
        solid_interior=False,
    ).getchannel("A")
    image.putalpha(alpha_master)
    draw = ImageDraw.Draw(image)
    accent = (255, 222, 95, 245) if state == "Selected" else (255, 196, 31, 238)
    draw.polygon([(0, 0), (24, 0), (13, 4), (0, 4)], fill=accent)
    draw.polygon([(56, 56), (27, 56), (39, 51), (56, 51)], fill=accent)
    return image


def static_art(name, size):
    styles = {
        "LowerHUDPlate": ((25, 50, 73, 64), (12, 31, 49, 72), 5, 8),
        "PartyHealthFill": ((119, 255, 105, 255), (12, 224, 41, 255), 2, 0),
        "PartyManaFill": ((51, 147, 255, 255), (6, 88, 225, 255), 1, 0),
        "PlayerHealthTrack": ((210, 223, 238, 220), (111, 137, 166, 220), 6, 10),
        "PlayerHealthFill": ((255, 77, 88, 255), (185, 7, 19, 255), 5, 8),
        "LoadingTrack": ((41, 78, 108, 210), (18, 43, 65, 226), 4, 5),
        "LoadingFill": ((45, 242, 248, 255), (0, 184, 198, 255), 3, 8),
        "MutationTrack": ((64, 79, 104, 210), (23, 47, 71, 230), 3, 4),
        "MutationFill": ((190, 31, 53, 255), (113, 10, 24, 255), 3, 5),
        "ResourceTrack": ((55, 84, 112, 210), (20, 45, 69, 225), 3, 0),
        "ResourceHealthFill": ((116, 255, 83, 255), (26, 218, 36, 255), 3, 7),
        "ResourceManaFill": ((53, 140, 255, 255), (0, 79, 232, 255), 3, 7),
        "MinimapMeterTrack": ((74, 97, 120, 72), (25, 48, 69, 80), 5, 0),
        "MinimapMeterWarningFill": ((255, 208, 57, 255), (244, 164, 4, 255), 5, 7),
        "MinimapMeterDangerFill": ((225, 26, 45, 255), (147, 4, 17, 255), 3, 4),
        "MinimapPanel": ((179, 200, 223, 64), (111, 139, 171, 72), 7, 14),
        "CurrencyIconLeft": ((235, 244, 252, 140), (146, 170, 198, 120), 4, 10),
        "CurrencyPlateLeft": ((76, 107, 143, 72), (30, 58, 87, 80), 4, 5),
        "CurrencyIconRight": ((235, 244, 252, 140), (146, 170, 198, 120), 4, 10),
        "CurrencyPlateRight": ((76, 107, 143, 72), (30, 58, 87, 80), 4, 5),
    }
    top, bottom, radius, sheen = styles[name]
    return rounded_gradient(size, top, bottom, radius, sheen)


def checkerboard(size, tile=18):
    width, height = size
    yy, xx = np.indices((height, width))
    cells = ((xx // tile) + (yy // tile)) & 1
    colors = np.array([[48, 51, 57, 255], [78, 82, 90, 255]], dtype=np.uint8)
    return Image.fromarray(colors[cells], "RGBA")


def save_formal_components():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.png"):
        old.unlink()

    for name, (_, _, width, height) in BUTTON_RECTS.items():
        for state in ("Normal", "Hover", "Pressed", "Disabled"):
            image = button_art(name, (width, height), state)
            image.save(OUT / f"MainHUD_{name}_{state}_{width}x{height}.png")

    for state in ("Normal", "Hover", "Pressed", "Disabled", "Selected"):
        hotbar_art(state).save(OUT / f"MainHUD_HotbarSlot_{state}_56x56.png")

    for name, (_, _, width, height) in STATIC_RECTS.items():
        static_art(name, (width, height)).save(
            OUT / f"MainHUD_{name}_Default_{width}x{height}.png"
        )


def build_reassembly():
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))

    for name, (x, y, width, height) in STATIC_RECTS.items():
        asset = OUT / f"MainHUD_{name}_Default_{width}x{height}.png"
        canvas.alpha_composite(Image.open(asset).convert("RGBA"), (x, y))

    for name, (x, y, width, height) in BUTTON_RECTS.items():
        asset = OUT / f"MainHUD_{name}_Normal_{width}x{height}.png"
        canvas.alpha_composite(Image.open(asset).convert("RGBA"), (x, y))

    slot = Image.open(OUT / "MainHUD_HotbarSlot_Normal_56x56.png").convert("RGBA")
    for x in HOTBAR_X:
        canvas.alpha_composite(slot, (x, 809))

    # This white marker has no confirmed business role, so it remains outside formal output.
    marker = rounded_gradient(
        (78, 30), (237, 244, 251, 225), (153, 176, 204, 205), 5, 12
    )
    (INTO / "Candidates").mkdir(parents=True, exist_ok=True)
    marker.save(INTO / "Candidates" / "MainHUD_CenterMarker_Pending_78x30.png")
    canvas.alpha_composite(marker, (740, 778))

    (INTO / "ReassemblyPreview").mkdir(parents=True, exist_ok=True)
    canvas.save(
        INTO / "ReassemblyPreview" / "MainHUD_Reassembly_NoText_1559x880.png"
    )
    TEMPLATES.mkdir(parents=True, exist_ok=True)
    canvas.save(TEMPLATES / "MainHUD_CleanTemplate_Empty_1559x880.png")
    return canvas


def build_qa(reassembly):
    QA.mkdir(parents=True, exist_ok=True)
    preview = checkerboard((WIDTH, HEIGHT))
    preview.alpha_composite(reassembly)
    preview.save(QA / "MainHUD_AlphaCheckerboard_1559x880.png")

    names = list(BUTTON_RECTS) + ["HotbarSlot"]
    widths = [BUTTON_RECTS[name][2] for name in BUTTON_RECTS] + [56]
    heights = [BUTTON_RECTS[name][3] for name in BUTTON_RECTS] + [56]
    states = ("Normal", "Hover", "Pressed", "Disabled")
    cell_width = max(widths) + 28
    row_height = max(heights) + 28
    sheet = checkerboard((cell_width * len(states), row_height * len(names)), 12)
    for row, name in enumerate(names):
        width = widths[row]
        height = heights[row]
        for column, state in enumerate(states):
            path = OUT / f"MainHUD_{name}_{state}_{width}x{height}.png"
            image = Image.open(path).convert("RGBA")
            x = column * cell_width + (cell_width - width) // 2
            y = row * row_height + (row_height - height) // 2
            sheet.alpha_composite(image, (x, y))
    sheet.save(QA / "MainHUD_ButtonStates.png")


def validate():
    failures = []
    for path in sorted(OUT.glob("*.png")):
        image = Image.open(path).convert("RGBA")
        width, height = image.size
        if not path.stem.endswith(f"_{width}x{height}"):
            failures.append(f"size/name mismatch: {path.name}")
        alpha = np.asarray(image.getchannel("A"))
        if alpha.max() == 0:
            failures.append(f"empty alpha: {path.name}")
        if any(token in path.name for token in ("Button_", "HotbarSlot_")):
            safe = alpha[height // 3 : max(height // 3 + 1, height * 2 // 3),
                         width // 3 : max(width // 3 + 1, width * 2 // 3)]
            median_alpha = float(np.median(safe))
            if not 48 <= median_alpha <= 96:
                failures.append(
                    f"button safe-area alpha is not shader-ready translucent: {path.name} "
                    f"({median_alpha:.1f})"
                )

    for name, (_, _, width, height) in BUTTON_RECTS.items():
        shapes = []
        for state in ("Normal", "Hover", "Pressed", "Disabled"):
            path = OUT / f"MainHUD_{name}_{state}_{width}x{height}.png"
            shapes.append(np.asarray(Image.open(path).convert("RGBA").getchannel("A")) > 0)
        if any(not np.array_equal(shapes[0], candidate) for candidate in shapes[1:]):
            failures.append(f"state alpha silhouette mismatch: {name}")

    if failures:
        raise RuntimeError("\n".join(failures))
    return len(list(OUT.glob("*.png")))


def main():
    save_formal_components()
    reassembly = build_reassembly()
    build_qa(reassembly)
    count = validate()
    print(f"MainHUD component export PASS: {count} PNG files")


if __name__ == "__main__":
    main()
