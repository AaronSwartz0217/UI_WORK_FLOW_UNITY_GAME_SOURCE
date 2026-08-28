from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps


ROOT = Path(r"C:\Users\Administrator\Desktop\UIWorkflow")
DESKTOP_UI = Path(r"C:\Users\Administrator\Desktop\ui")


def polygon_mask(size: tuple[int, int], points: list[tuple[int, int]], supersample: int = 8) -> Image.Image:
    width, height = size
    large = Image.new("L", (width * supersample, height * supersample), 0)
    ImageDraw.Draw(large).polygon(
        [(x * supersample, y * supersample) for x, y in points],
        fill=255,
    )
    mask = large.resize(size, Image.Resampling.LANCZOS)
    return mask.point(lambda value: 0 if value <= 5 else value)


def cut_component(source: Path, box: tuple[int, int, int, int], chamfer: int) -> Image.Image:
    image = Image.open(source).convert("RGBA").crop(box)
    right, bottom = image.width - 1, image.height - 1
    points = [
        (chamfer, 0),
        (right - chamfer, 0),
        (right, chamfer),
        (right, bottom - chamfer),
        (right - chamfer, bottom),
        (chamfer, bottom),
        (0, bottom - chamfer),
        (0, chamfer),
    ]
    image.putalpha(polygon_mask(image.size, points))
    return image


def pad_transparent(image: Image.Image, padding: int) -> Image.Image:
    padded = Image.new("RGBA", (image.width + padding * 2, image.height + padding * 2), (0, 0, 0, 0))
    padded.alpha_composite(image, (padding, padding))
    return padded


def button_states(normal: Image.Image) -> dict[str, Image.Image]:
    rgba = normal.convert("RGBA")
    alpha = rgba.getchannel("A")
    rgb = rgba.convert("RGB")
    states = {
        "Normal": rgb,
        "Hover": ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(1.08)).enhance(1.14),
        "Pressed": ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(0.94)).enhance(0.80),
        "Disabled": ImageEnhance.Brightness(ImageOps.grayscale(rgb).convert("RGB")).enhance(0.52),
    }
    result: dict[str, Image.Image] = {}
    for state, state_rgb in states.items():
        image = state_rgb.convert("RGBA")
        image.putalpha(alpha)
        result[state] = image
    return result


def checkerboard(size: tuple[int, int], cell: int = 8) -> Image.Image:
    image = Image.new("RGBA", size, (226, 226, 226, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, min(x + cell - 1, size[0] - 1), min(y + cell - 1, size[1] - 1)), fill=(150, 150, 150, 255))
    return image


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_qa(image: Image.Image, qa_dir: Path, stem: str) -> None:
    qa_dir.mkdir(parents=True, exist_ok=True)
    image.save(qa_dir / f"{stem}_100Percent.png")
    image.resize((image.width * 4, image.height * 4), Image.Resampling.NEAREST).save(
        qa_dir / f"{stem}_400Percent.png"
    )
    checker = checkerboard(image.size)
    checker.alpha_composite(image)
    checker.resize((image.width * 4, image.height * 4), Image.Resampling.NEAREST).save(
        qa_dir / f"{stem}_Checkerboard_400Percent.png"
    )


def validate(images: dict[str, Image.Image]) -> dict[str, object]:
    report: dict[str, object] = {"files": {}, "status": "PASS"}
    reference_alpha: bytes | None = None
    for filename, image in images.items():
        alpha = image.getchannel("A")
        extrema = alpha.getextrema()
        low_alpha = sum(1 for value in alpha.get_flattened_data() if 0 < value <= 5)
        if image.mode != "RGBA" or extrema != (0, 255) or low_alpha != 0:
            report["status"] = "FAIL"
        if "RejectButton" in filename:
            alpha_bytes = alpha.tobytes()
            if reference_alpha is None:
                reference_alpha = alpha_bytes
            elif alpha_bytes != reference_alpha:
                report["status"] = "FAIL"
        report["files"][filename] = {
            "mode": image.mode,
            "size": list(image.size),
            "alphaExtrema": list(extrema),
            "lowAlpha1To5": low_alpha,
            "visibleBounds": list(alpha.getbbox() or (0, 0, 0, 0)),
        }
    return report


def copy_promoted(source: Path, formal_dir: Path, desktop_dir: Path) -> None:
    formal_dir.mkdir(parents=True, exist_ok=True)
    desktop_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, formal_dir / source.name)
    shutil.copy2(source, desktop_dir / source.name)


def unlink_exact(paths: list[Path]) -> None:
    for path in paths:
        if path.exists():
            path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--promote", action="store_true", help="Replace formal and desktop delivery assets after validation passes.")
    args = parser.parse_args()

    advancement_project = ROOT / "04_Projects/EquipmentAdvancementUI"
    team_project = ROOT / "04_Projects/TeamInvitationPopupUI"
    enchanting_project = ROOT / "04_Projects/EquipmentEnchantingUI"

    # The paired left slot is the closest approved reference for this exact screen.
    # Reusing it keeps both equipment slots pixel-identical and avoids another approximate crop.
    advancement = Image.open(
        advancement_project / "Components/out/EquipmentAdvancementUI/EquipmentAdvancement_LeftEquipmentSlot_Default_86x89.png"
    ).convert("RGBA")
    reject_normal = pad_transparent(
        cut_component(
            team_project / "FullUI/TeamInvitationPopupUI_FullUI_Review06_1536x1024.png",
            (1157, 223, 1335, 306),
            12,
        ),
        3,
    )
    toggle = pad_transparent(
        cut_component(
            enchanting_project / "FullUI/EquipmentEnchantingUI_FullUI_Review02_1024x1536.png",
            (792, 510, 862, 580),
            7,
        ),
        2,
    )

    advancement_candidate = advancement_project / "into/Candidates/CropRepairV01"
    team_candidate = team_project / "into/Candidates/CropRepairV01"
    enchanting_candidate = enchanting_project / "into/Candidates/CropRepairV01"
    for directory in (advancement_candidate, team_candidate, enchanting_candidate):
        directory.mkdir(parents=True, exist_ok=True)

    images: dict[str, Image.Image] = {}
    advancement_name = "EquipmentAdvancement_RightEquipmentSlot_Default_86x89.png"
    advancement.save(advancement_candidate / advancement_name)
    images[advancement_name] = advancement

    for state, image in button_states(reject_normal).items():
        filename = f"TeamInvitation_RejectButton_{state}_184x89.png"
        image.save(team_candidate / filename)
        images[filename] = image

    enchanting_name = "EquipmentEnchanting_AttributeToggleSlot_Empty_74x74.png"
    toggle.save(enchanting_candidate / enchanting_name)
    images[enchanting_name] = toggle

    save_qa(advancement, advancement_project / "QA/CropRepairV01", advancement_name.removesuffix(".png"))
    save_qa(images["TeamInvitation_RejectButton_Hover_184x89.png"], team_project / "QA/CropRepairV01", "TeamInvitation_RejectButton_Hover_184x89")
    save_qa(toggle, enchanting_project / "QA/CropRepairV01", enchanting_name.removesuffix(".png"))

    report = validate(images)
    report["sourceBounds"] = {
        "EquipmentAdvancement_RightEquipmentSlot": "Components/out/EquipmentAdvancementUI/EquipmentAdvancement_LeftEquipmentSlot_Default_86x89.png",
        "TeamInvitation_RejectButton": [1157, 223, 1335, 306],
        "EquipmentEnchanting_AttributeToggleSlot": [792, 510, 862, 580],
    }
    report["replacementMap"] = {
        "EquipmentAdvancement_RightEquipmentSlot_Default_86x89.png": "same filename; pixels reused from LeftEquipmentSlot",
        "TeamInvitation_RejectButton_*_164x77.png": "TeamInvitation_RejectButton_*_184x89.png",
        "EquipmentEnchanting_AttributeToggleSlot_Empty_64x64.png": enchanting_name,
    }

    report_path = ROOT / "05_Tools/crop_repair_v01_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if report["status"] != "PASS":
        raise SystemExit(f"Validation failed; inspect {report_path}")

    if args.promote:
        advancement_formal = advancement_project / "Components/out/EquipmentAdvancementUI"
        team_formal = team_project / "Components/out/TeamInvitationPopupUI"
        enchanting_formal = enchanting_project / "Components/out/EquipmentEnchantingUI"

        old_paths = [
            advancement_formal / "EquipmentAdvancement_RightEquipmentSlot_Default_86x89.png",
            DESKTOP_UI / "装备进阶/EquipmentAdvancement_RightEquipmentSlot_Default_86x89.png",
            advancement_formal / "EquipmentAdvancement_RightEquipmentSlot_Default_94x90.png",
            DESKTOP_UI / "装备进阶/EquipmentAdvancement_RightEquipmentSlot_Default_94x90.png",
            advancement_project / "into/Candidates/CleanParentV02/EquipmentAdvancement_RightEquipmentSlot_Default_86x89.png",
            advancement_project / "into/Candidates/CleanParentV02/EquipmentAdvancement_RightEquipmentSlot_Default_94x90.png",
            advancement_project / "into/Candidates/CropRepairV01/EquipmentAdvancement_RightEquipmentSlot_Default_92x96.png",
            advancement_project / "into/Candidates/CropRepairV01/EquipmentAdvancement_RightEquipmentSlot_Default_94x90.png",
            enchanting_formal / "EquipmentEnchanting_AttributeToggleSlot_Empty_64x64.png",
            DESKTOP_UI / "附魔/EquipmentEnchanting_AttributeToggleSlot_Empty_64x64.png",
            enchanting_project / "into/Candidates/CropRepairV01/EquipmentEnchanting_AttributeToggleSlot_Empty_72x68.png",
            enchanting_project / "into/Candidates/CropRepairV01/EquipmentEnchanting_AttributeToggleSlot_Empty_70x70.png",
        ]
        for state in ("Normal", "Hover", "Pressed", "Disabled"):
            old_paths.extend(
                [
                    team_formal / f"TeamInvitation_RejectButton_{state}_164x77.png",
                    DESKTOP_UI / f"组队邀请弹窗/TeamInvitation_RejectButton_{state}_164x77.png",
                    team_project / f"into/Candidates/CropRepairV01/TeamInvitation_RejectButton_{state}_178x83.png",
                ]
            )
        unlink_exact(old_paths)

        copy_promoted(advancement_candidate / advancement_name, advancement_formal, DESKTOP_UI / "装备进阶")
        copy_promoted(enchanting_candidate / enchanting_name, enchanting_formal, DESKTOP_UI / "附魔")
        for state in ("Normal", "Hover", "Pressed", "Disabled"):
            filename = f"TeamInvitation_RejectButton_{state}_184x89.png"
            copy_promoted(team_candidate / filename, team_formal, DESKTOP_UI / "组队邀请弹窗")

        promoted = [
            advancement_formal / advancement_name,
            enchanting_formal / enchanting_name,
            *[team_formal / f"TeamInvitation_RejectButton_{state}_184x89.png" for state in ("Normal", "Hover", "Pressed", "Disabled")],
        ]
        report["promoted"] = [{"path": str(path), "sha256": sha256(path)} for path in promoted]
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"status": report["status"], "promoted": args.promote, "report": str(report_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
