from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image


PREFIX = "LargeLogin_CharacterSetup"
REQUIRED = {
    "LargeLogin_CharacterSetupBackground_Default_1464x828.png": (1464, 828),
    "LargeLogin_CharacterSetupMainPanel_Default_1012x328.png": (1012, 328),
    "LargeLogin_CharacterSetupNameInput_Default_482x50.png": (482, 50),
    "LargeLogin_CharacterSetupCurrentEquipmentSlot_Empty_222x214.png": (222, 214),
    **{
        f"LargeLogin_CharacterSetupEquipmentCard_{state}_184x164.png": (184, 164)
        for state in ("Normal", "Hover", "Pressed", "Disabled", "Selected")
    },
    **{
        f"LargeLogin_CharacterSetupEnterGameButton_{state}_368x72.png": (368, 72)
        for state in ("Normal", "Hover", "Pressed", "Disabled")
    },
}


def open_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def checkerboard(size: tuple[int, int], tile: int = 24) -> Image.Image:
    image = Image.new("RGBA", size, (0, 0, 0, 255))
    pixels = image.load()
    colors = ((47, 52, 60, 255), (83, 90, 101, 255))
    for y in range(size[1]):
        for x in range(size[0]):
            pixels[x, y] = colors[((x // tile) + (y // tile)) & 1]
    return image


def mask_bytes(image: Image.Image) -> bytes:
    return bytes(255 if alpha > 0 else 0 for alpha in image.getchannel("A").tobytes())


def validate(formal: Path) -> dict[str, object]:
    errors: list[str] = []
    records: list[dict[str, object]] = []
    images: dict[str, Image.Image] = {}
    size_pattern = re.compile(r"_(\d+)x(\d+)\.png$")

    for name, expected_size in REQUIRED.items():
        path = formal / name
        if not path.exists():
            errors.append(f"missing: {name}")
            continue
        image = open_rgba(path)
        images[name] = image
        alpha = image.getchannel("A")
        bbox = alpha.getbbox()
        corners = [
            image.getpixel((0, 0))[3],
            image.getpixel((image.width - 1, 0))[3],
            image.getpixel((0, image.height - 1))[3],
            image.getpixel((image.width - 1, image.height - 1))[3],
        ]
        match = size_pattern.search(name)
        filename_size = (int(match.group(1)), int(match.group(2))) if match else None
        center_alpha = image.getpixel((image.width // 2, image.height // 2))[3]

        if image.size != expected_size:
            errors.append(f"size mismatch: {name}: {image.size} != {expected_size}")
        if filename_size != image.size:
            errors.append(f"filename dimension mismatch: {name}")
        if name.endswith("Background_Default_1464x828.png"):
            if alpha.getextrema() != (255, 255):
                errors.append(f"background is not opaque: {name}")
        else:
            if alpha.getextrema()[0] != 0 or alpha.getextrema()[1] <= 0:
                errors.append(f"invalid alpha range: {name}: {alpha.getextrema()}")
            if bbox != (0, 0, image.width, image.height):
                errors.append(f"not tight-cropped: {name}: {bbox}")
            if any(corners):
                errors.append(f"rounded component corners are not transparent: {name}: {corners}")
            if not 0 < center_alpha < 255:
                errors.append(f"glass center alpha is not intentionally translucent: {name}: {center_alpha}")

        records.append(
            {
                "file": name,
                "size": image.size,
                "alphaRange": alpha.getextrema(),
                "visibleBounds": bbox,
                "centerAlpha": center_alpha,
                "cornerAlpha": corners,
            }
        )

    for component, states in {
        "EquipmentCard": ("Normal", "Hover", "Pressed", "Disabled", "Selected"),
        "EnterGameButton": ("Normal", "Hover", "Pressed", "Disabled"),
    }.items():
        family = [
            images.get(
                f"{PREFIX}{component}_{state}_"
                f"{'184x164' if component == 'EquipmentCard' else '368x72'}.png"
            )
            for state in states
        ]
        if any(image is None for image in family):
            continue
        dimensions = {image.size for image in family if image is not None}
        silhouettes = {mask_bytes(image) for image in family if image is not None}
        if len(dimensions) != 1:
            errors.append(f"state canvas mismatch: {component}")
        if len(silhouettes) != 1:
            errors.append(f"state silhouette mismatch: {component}")

    return {"result": "PASS" if not errors else "FAIL", "errors": errors, "files": records}


def make_reassembly(formal: Path, output: Path) -> None:
    background = open_rgba(formal / "LargeLogin_CharacterSetupBackground_Default_1464x828.png")
    canvas = background.copy()
    placements = [
        ("LargeLogin_CharacterSetupMainPanel_Default_1012x328.png", (226, 98)),
        ("LargeLogin_CharacterSetupNameInput_Default_482x50.png", (393, 111)),
        ("LargeLogin_CharacterSetupCurrentEquipmentSlot_Empty_222x214.png", (622, 185)),
        ("LargeLogin_CharacterSetupEquipmentCard_Normal_184x164.png", (228, 440)),
        ("LargeLogin_CharacterSetupEquipmentCard_Normal_184x164.png", (434, 440)),
        ("LargeLogin_CharacterSetupEquipmentCard_Normal_184x164.png", (640, 440)),
        ("LargeLogin_CharacterSetupEquipmentCard_Normal_184x164.png", (846, 440)),
        ("LargeLogin_CharacterSetupEquipmentCard_Normal_184x164.png", (1052, 440)),
        ("LargeLogin_CharacterSetupEnterGameButton_Normal_368x72.png", (549, 647)),
    ]
    for name, position in placements:
        canvas.alpha_composite(open_rgba(formal / name), dest=position)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def make_checkerboard(formal: Path, output: Path) -> None:
    canvas = checkerboard((1600, 760))
    placements = [
        ("LargeLogin_CharacterSetupMainPanel_Default_1012x328.png", (20, 20)),
        ("LargeLogin_CharacterSetupNameInput_Default_482x50.png", (1060, 20)),
        ("LargeLogin_CharacterSetupCurrentEquipmentSlot_Empty_222x214.png", (1060, 90)),
        *[
            (f"LargeLogin_CharacterSetupEquipmentCard_{state}_184x164.png", (20 + index * 205, 380))
            for index, state in enumerate(("Normal", "Hover", "Pressed", "Disabled", "Selected"))
        ],
        *[
            (f"LargeLogin_CharacterSetupEnterGameButton_{state}_368x72.png", (20 + index * 390, 590))
            for index, state in enumerate(("Normal", "Hover", "Pressed", "Disabled"))
        ],
    ]
    for name, position in placements:
        canvas.alpha_composite(open_rgba(formal / name), dest=position)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--formal", type=Path, required=True)
    parser.add_argument("--reassembly", type=Path, required=True)
    parser.add_argument("--checkerboard", type=Path, required=True)
    args = parser.parse_args()

    result = validate(args.formal)
    if result["result"] == "PASS":
        make_reassembly(args.formal, args.reassembly)
        make_checkerboard(args.formal, args.checkerboard)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=list))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
