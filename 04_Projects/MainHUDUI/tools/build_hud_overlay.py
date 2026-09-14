from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
FULL_UI = ROOT / "FullUI"
QA = ROOT / "QA"
WIDTH, HEIGHT = 1559, 880
SCALE = 4


def scaled_box(box):
    x, y, w, h = box
    return x * SCALE, y * SCALE, w * SCALE, h * SCALE


def rounded_gradient(canvas, box, top, bottom, radius, sheen=0):
    x, y, w, h = box
    sw, sh = w * SCALE, h * SCALE
    top_v = np.asarray(top, dtype=np.float32)
    bottom_v = np.asarray(bottom, dtype=np.float32)
    t = np.linspace(0.0, 1.0, sh, dtype=np.float32)[:, None, None]
    pixels = np.broadcast_to(top_v, (sh, sw, 4)).copy()
    pixels += (bottom_v - top_v) * t
    layer = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8), "RGBA")

    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, sw - 1, sh - 1),
        radius=radius * SCALE,
        fill=255,
    )
    alpha = np.asarray(layer.getchannel("A"), dtype=np.uint16)
    alpha = (alpha * np.asarray(mask, dtype=np.uint16) // 255).astype(np.uint8)
    layer.putalpha(Image.fromarray(alpha, "L"))

    if sheen:
        sheen_layer = Image.new("RGBA", (sw, sh), (255, 255, 255, 0))
        sheen_alpha = np.zeros((sh, sw), dtype=np.uint8)
        sheen_height = max(1, int(sh * 0.36))
        values = np.linspace(sheen, 0, sheen_height, dtype=np.uint8)
        sheen_alpha[:sheen_height, :] = values[:, None]
        sheen_alpha = (
            sheen_alpha.astype(np.uint16)
            * np.asarray(mask, dtype=np.uint16)
            // 255
        ).astype(np.uint8)
        sheen_layer.putalpha(Image.fromarray(sheen_alpha, "L"))
        layer = Image.alpha_composite(layer, sheen_layer)

    canvas.alpha_composite(layer, (x * SCALE, y * SCALE))


def draw_chevron(draw, center, size, color=(248, 250, 255, 235)):
    cx, cy = center
    s = size
    width = max(1, int(2.4 * SCALE))
    draw.line(
        ((cx - s) * SCALE, (cy - s * 0.35) * SCALE, cx * SCALE, (cy + s * 0.55) * SCALE),
        fill=color,
        width=width,
    )
    draw.line(
        (cx * SCALE, (cy + s * 0.55) * SCALE, (cx + s) * SCALE, (cy - s * 0.35) * SCALE),
        fill=color,
        width=width,
    )


def draw_greater_than(draw, center, size, color=(248, 250, 255, 235)):
    cx, cy = center
    s = size
    width = max(1, int(2.4 * SCALE))
    draw.line(
        ((cx - s * 0.45) * SCALE, (cy - s) * SCALE, (cx + s * 0.55) * SCALE, cy * SCALE),
        fill=color,
        width=width,
    )
    draw.line(
        ((cx + s * 0.55) * SCALE, cy * SCALE, (cx - s * 0.45) * SCALE, (cy + s) * SCALE),
        fill=color,
        width=width,
    )


def build_overlay():
    canvas = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), (0, 0, 0, 0))

    # The large lower HUD plate is the only broad background surface. The main
    # gameplay viewport remains fully transparent for the future 3D camera.
    rounded_gradient(
        canvas,
        (15, 594, 1253, 282),
        (25, 50, 73, 92),
        (12, 31, 49, 118),
        5,
        sheen=8,
    )

    neutral_button_top = (202, 220, 241, 205)
    neutral_button_bottom = (86, 116, 151, 185)
    dark_button_top = (76, 107, 143, 205)
    dark_button_bottom = (30, 58, 87, 222)

    rounded_gradient(canvas, (15, 15, 79, 39), neutral_button_top, neutral_button_bottom, 7, sheen=18)
    rounded_gradient(canvas, (909, 31, 69, 21), neutral_button_top, neutral_button_bottom, 5, sheen=14)
    rounded_gradient(canvas, (1279, 15, 84, 40), dark_button_top, dark_button_bottom, 7, sheen=12)
    rounded_gradient(canvas, (1372, 15, 80, 39), neutral_button_top, neutral_button_bottom, 7, sheen=16)
    rounded_gradient(canvas, (1462, 15, 80, 39), neutral_button_top, neutral_button_bottom, 7, sheen=16)

    draw = ImageDraw.Draw(canvas)
    draw_greater_than(draw, (55, 35), 6)
    draw_chevron(draw, (1321, 34), 6)

    # Party resource strips, exact wireframe thickness.
    rounded_gradient(canvas, (15, 72, 75, 12), (119, 255, 105, 255), (12, 224, 41, 255), 2)
    rounded_gradient(canvas, (15, 86, 75, 4), (51, 147, 255, 255), (6, 88, 225, 255), 1)

    # Top-center health bar: outer 406x20, inner visible content 403x17.
    rounded_gradient(canvas, (576, 53, 406, 20), (210, 223, 238, 220), (111, 137, 166, 220), 6, sheen=10)
    rounded_gradient(canvas, (577, 54, 162, 17), (255, 77, 88, 255), (185, 7, 19, 255), 5, sheen=8)

    # Bottom loading and state bars use the original thin 18/17 px profiles.
    rounded_gradient(canvas, (576, 696, 405, 18), (41, 78, 108, 210), (18, 43, 65, 226), 4, sheen=5)
    rounded_gradient(canvas, (577, 697, 119, 16), (45, 242, 248, 255), (0, 184, 198, 255), 3, sheen=8)
    rounded_gradient(canvas, (496, 722, 566, 17), (64, 79, 104, 210), (23, 47, 71, 230), 3, sheen=4)
    rounded_gradient(canvas, (497, 723, 486, 15), (190, 31, 53, 255), (113, 10, 24, 255), 3, sheen=5)

    # Combined health/mana resource bar and the pending neutral center marker.
    rounded_gradient(canvas, (455, 782, 646, 21), (55, 84, 112, 210), (20, 45, 69, 225), 3)
    rounded_gradient(canvas, (456, 782, 344, 20), (116, 255, 83, 255), (26, 218, 36, 255), 3, sheen=7)
    rounded_gradient(canvas, (800, 782, 301, 20), (53, 140, 255, 255), (0, 79, 232, 255), 3, sheen=7)
    rounded_gradient(canvas, (740, 778, 78, 30), (237, 244, 251, 225), (153, 176, 204, 205), 5, sheen=12)

    # Thirteen exact wireframe hotbar slots, with the group break before Q.
    slot_x = [315, 372, 429, 496, 553, 609, 666, 722, 779, 835, 891, 948, 1004]
    for x in slot_x:
        rounded_gradient(canvas, (x, 809, 56, 56), (58, 87, 120, 218), (21, 45, 68, 238), 5, sheen=7)
        draw = ImageDraw.Draw(canvas)
        draw.polygon(
            [(x * SCALE, 809 * SCALE), ((x + 24) * SCALE, 809 * SCALE), ((x + 13) * SCALE, 813 * SCALE), (x * SCALE, 813 * SCALE)],
            fill=(255, 207, 64, 240),
        )
        draw.polygon(
            [((x + 56) * SCALE, 865 * SCALE), ((x + 27) * SCALE, 865 * SCALE), ((x + 39) * SCALE, 860 * SCALE), ((x + 56) * SCALE, 860 * SCALE)],
            fill=(255, 195, 27, 240),
        )

    rounded_gradient(canvas, (1073, 809, 56, 56), (190, 28, 43, 245), (101, 5, 16, 252), 4, sheen=6)

    # Minimap stack and currency/action strip.
    rounded_gradient(canvas, (1268, 586, 23, 242), (74, 97, 120, 210), (25, 48, 69, 225), 5)
    rounded_gradient(canvas, (1268, 586, 23, 81), (255, 208, 57, 255), (244, 164, 4, 255), 5, sheen=7)
    rounded_gradient(canvas, (1268, 667, 23, 161), (225, 26, 45, 255), (147, 4, 17, 255), 3, sheen=4)
    rounded_gradient(canvas, (1303, 586, 239, 243), (179, 200, 223, 205), (111, 139, 171, 195), 7, sheen=14)
    rounded_gradient(canvas, (1306, 793, 62, 29), neutral_button_top, neutral_button_bottom, 5, sheen=10)
    rounded_gradient(canvas, (1268, 836, 29, 29), (235, 244, 252, 230), (146, 170, 198, 210), 4, sheen=10)
    rounded_gradient(canvas, (1305, 836, 64, 29), dark_button_top, dark_button_bottom, 4, sheen=5)
    rounded_gradient(canvas, (1377, 836, 28, 29), (235, 244, 252, 230), (146, 170, 198, 210), 4, sheen=10)
    rounded_gradient(canvas, (1412, 836, 69, 29), dark_button_top, dark_button_bottom, 4, sheen=5)
    rounded_gradient(canvas, (1487, 838, 54, 25), neutral_button_top, neutral_button_bottom, 5, sheen=10)

    return canvas.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def checkerboard(size, tile=20):
    w, h = size
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    colors = ((48, 51, 57, 255), (78, 82, 90, 255))
    for y in range(h):
        for x in range(w):
            arr[y, x] = colors[((x // tile) + (y // tile)) & 1]
    return Image.fromarray(arr, "RGBA")


def main():
    FULL_UI.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    overlay = build_overlay()
    overlay.save(FULL_UI / "MainHUD_FullUI_TransparentOverlay_1559x880.png")
    preview = checkerboard((WIDTH, HEIGHT))
    preview.alpha_composite(overlay)
    preview.save(QA / "MainHUD_TransparentCheckerboard_1559x880.png")


if __name__ == "__main__":
    main()
