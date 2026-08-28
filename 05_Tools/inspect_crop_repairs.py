from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(r"C:\Users\Administrator\Desktop\UIWorkflow")

CASES = (
    {
        "name": "EquipmentAdvancement_RightEquipmentSlot",
        "source": ROOT / "04_Projects/EquipmentAdvancementUI/into/EquipmentAdvancementUI_NoOrdinaryText_Master_1078x1459.png",
        "old": (571, 867, 657, 956),
        "expanded": (559, 855, 669, 968),
        "output": ROOT / "04_Projects/EquipmentAdvancementUI/QA/CropRepairV01",
    },
    {
        "name": "TeamInvitation_RejectButton",
        "source": ROOT / "04_Projects/TeamInvitationPopupUI/FullUI/TeamInvitationPopupUI_FullUI_Review06_1536x1024.png",
        "old": (1164, 223, 1328, 300),
        "expanded": (1148, 211, 1344, 312),
        "output": ROOT / "04_Projects/TeamInvitationPopupUI/QA/CropRepairV01",
    },
    {
        "name": "EquipmentEnchanting_AttributeToggleSlot",
        "source": ROOT / "04_Projects/EquipmentEnchantingUI/FullUI/EquipmentEnchantingUI_FullUI_Review02_1024x1536.png",
        "old": (795, 513, 859, 577),
        "expanded": (783, 501, 871, 589),
        "output": ROOT / "04_Projects/EquipmentEnchantingUI/QA/CropRepairV01",
    },
)


def main() -> None:
    for case in CASES:
        source = Image.open(case["source"]).convert("RGBA")
        ex = case["expanded"]
        old = case["old"]
        crop = source.crop(ex)
        draw = ImageDraw.Draw(crop)
        old_local = (
            old[0] - ex[0],
            old[1] - ex[1],
            old[2] - ex[0] - 1,
            old[3] - ex[1] - 1,
        )
        draw.rectangle(old_local, outline=(255, 0, 255, 255), width=1)
        out = case["output"]
        out.mkdir(parents=True, exist_ok=True)
        crop.save(out / f"{case['name']}_ExpandedSource_WithOldBounds.png")
        crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.NEAREST).save(
            out / f"{case['name']}_ExpandedSource_WithOldBounds_400Percent.png"
        )
        print(out / f"{case['name']}_ExpandedSource_WithOldBounds_400Percent.png")


if __name__ == "__main__":
    main()
