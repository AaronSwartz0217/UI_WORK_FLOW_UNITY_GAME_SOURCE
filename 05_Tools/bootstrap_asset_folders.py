from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ASSET_DIRECTORIES = [
    "01_References/Style/Standards/Primary_Cook",
    "01_References/Style/Standards/Secondary_EquipmentIdentification",
    "01_References/SharedComponents/Buttons",
    "01_References/SharedComponents/CloseButtons",
    "01_References/SharedComponents/PanelBorders",
    "01_References/SharedComponents/Slots",
    "01_References/LayoutWireframes/DesktopUIWireframes",
    "02_InputQueue/01_RootPriority/CharacterAttributesUI/Wireframe",
    "02_InputQueue/01_RootPriority/EquipmentAdvancementUI/Wireframe",
    "04_Projects/CharacterAttributesUI/FullUI",
    "04_Projects/CharacterAttributesUI/in",
    "04_Projects/CharacterAttributesUI/into/Candidates",
    "04_Projects/CharacterAttributesUI/into/Rejected",
    "04_Projects/CharacterAttributesUI/into/ReassemblyPreview",
    "04_Projects/CharacterAttributesUI/Components/out/CharacterAttributesUI",
    "04_Projects/EquipmentAdvancementUI/FullUI",
    "04_Projects/EquipmentAdvancementUI/in",
    "04_Projects/EquipmentAdvancementUI/into/Candidates",
    "04_Projects/EquipmentAdvancementUI/into/Rejected",
    "04_Projects/EquipmentAdvancementUI/into/ReassemblyPreview",
    "04_Projects/EquipmentAdvancementUI/Components/out/EquipmentAdvancementUI",
]


def main() -> None:
    for relative in ASSET_DIRECTORIES:
        (ROOT / relative).mkdir(parents=True, exist_ok=True)
    print(f"Prepared {len(ASSET_DIRECTORIES)} local asset directories under {ROOT}")


if __name__ == "__main__":
    main()
