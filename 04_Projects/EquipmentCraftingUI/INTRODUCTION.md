# Equipment Crafting UI Introduction

## Goal

Convert the supplied equipment-crafting layout into a reusable industrial post-apocalyptic UI kit.

## Recommended hierarchy

```text
RootWindow
├─ HeaderBar
│  ├─ TitleTextNode
│  ├─ HelpButton
│  └─ CloseButton
├─ EquipmentRegionPanel
│  ├─ EquipmentSlot
│  └─ InstructionTextNode
├─ SectionDivider
├─ AttributesMainPanel
│  ├─ AttributesTitleTextNode
│  ├─ BaseAttributePanel
│  ├─ SpecialAttributeRow
│  └─ SpecialSkillRow
│     └─ SkillSlot
├─ MaterialRequirementsPanel
│  ├─ MaterialSlotLeft
│  ├─ MaterialSlotRight
│  └─ QuantityTextNodes
└─ BottomActionPanel
   ├─ PrimaryActionButton
   └─ StatusTextNode
```

## Import

- Filter Mode: Bilinear
- Wrap Mode: Clamp
- MipMaps: Off
- Alpha Source: Input Texture Alpha
- Alpha Is Transparency: On
- Use nine-slice for the root and rectangular panels.
- Do not uniformly stretch square slots or square buttons.
- Use engine text for all localizable and dynamic content.

All three interactive button groups include complete four-state assets.
