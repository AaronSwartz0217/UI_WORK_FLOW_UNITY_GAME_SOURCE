# 属性界面 / CharacterAttributesUI

```text
ProjectDisplayName: 属性界面
ProjectId: CharacterAttributesUI
ComponentPrefix: CharacterAttributes
Status: full_ui_pending_user_review
```

## Inputs

- Layout-only wireframe: `in/CharacterAttributesUI_Wireframe_815x1110.jpeg`
- Primary style: `in/StylePrimary_Cook/` (25 PNG)
- Secondary style: `in/StyleSecondary_EquipmentIdentification/` (15 PNG)
- Cook is authoritative whenever the style sets disagree.
- Reference images remain unchanged.

## Text policy

The full-UI draft is text-clean from the first generation. Remove ordinary/localized text and dynamic numbers; retain only functional symbols such as the close `X`. Reconstruct complete solid surfaces beneath removed text.

## Proportion

- Wireframe canvas: `815x1110`
- Measured UI panel bounds: approximately `x=97, y=57, width=639, height=924`
- Measured UI panel ratio: approximately `0.691558`
- Target full-UI canvas: `1024x1536`; preserve the measured panel ratio inside the canvas.
- `ScaleX == ScaleY`; no single-axis correction.

## Layout hierarchy

```text
MainPanelBase
|- NormalAttributesTab
|- VariantAttributesTab
|- CloseButton
|- CombatPowerRegion
|- RankAndAlignmentRegion
|- ExperienceTrack
|- SatietyTrack
`- AttributeColumns
   |- PrimaryAttributeColumn
   `- DerivedAttributeColumn
```

## Gate

Current review image: `FullUI/CharacterAttributesUI_FullUI_Review02_1024x1536.png`.

The review image is text-clean and structurally complete. Its measured panel ratio differs from the wireframe by approximately `1.97%`; this is recorded as pending user acceptance. Do not split components before approval.
## Current production result

- Approved full-UI basis: CharacterAttributesUI Review02.
- Formal component output: 13 PNG files.
- Stable control reuse: the complete Cook Close/X 52x50 four-state family is copied verbatim and renamed with the CharacterAttributes prefix.
- Repeated tabs, progress tracks, short rows, and long rows are exported once and placed by coordinates.
- Review the reassembly and checkerboard previews in QA/Previews before final acceptance.
