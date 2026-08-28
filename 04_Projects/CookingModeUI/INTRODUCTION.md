# Cooking Mode UI Introduction

ProjectDisplayName: 烹饪模式  
ProjectId: `CookingModeUI`  
ComponentPrefix: `CookingMode`

## Goal

Convert the supplied cooking layout into a reusable post-apocalyptic industrial UI kit while preserving the layout reference and applying the equipment-crafting visual language.

## Directory

```text
CookingModeUI/
├─ README.md
├─ INTRODUCTION.md
├─ in/
├─ into/
├─ Components/out/CookingModeUI/
└─ QA/
```

## Recommended assembly hierarchy

```text
RootWindow
├─ HeaderTextNode
├─ LevelAndExperienceTextNode
├─ CloseButton
├─ LeftSidebarPanel
│  ├─ SidebarTitleTextNode
│  └─ RecipeSelectionButton
└─ MainContentPanel
   ├─ RecipeTitleTextNode
   ├─ RecipeDescriptionTextNode
   ├─ RecipePreviewPanel
   │  └─ MaterialSlot
   ├─ QuantityTextNodes
   ├─ QuantityMinusButton
   ├─ QuantityPlusButton
   ├─ MaximumButton
   ├─ StartButton
   ├─ ProgressTrack
   │  └─ ProgressFill
   └─ FooterMessageTextNode
```

## Import recommendations

- Filter Mode: Bilinear
- Wrap Mode: Clamp
- MipMaps: Off
- Alpha Source: Input Texture Alpha
- Alpha Is Transparency: On
- Use nine-slice for the root, structural panels and wide buttons.
- Do not uniformly stretch square buttons or the material slot.
- Use separate engine text nodes for localizable and dynamic content.

## Extension

- Establish nine-slice insets after testing at the target runtime resolution.
- Record final anchors and reassembly coordinates in the implementation configuration.

All six interactive button groups include complete four-state assets.
