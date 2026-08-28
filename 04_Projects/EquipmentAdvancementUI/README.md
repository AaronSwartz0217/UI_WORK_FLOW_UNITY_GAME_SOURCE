# Equipment Advancement / EquipmentAdvancementUI

```text
ProjectDisplayName: Equipment Advancement
ProjectId: EquipmentAdvancementUI
ComponentPrefix: EquipmentAdvancement
Status: final_components_pending_user_review
```

## Inputs

- Layout reference: `in/EquipmentAdvancementUI_Wireframe.jpeg` (`704x954`)
- Primary style reference: `in/StyleReference_01.jpg`
- Shared style board: `in/SharedComponents_StyleBoard.png`
- Shared component references: `in/SharedComponents/`
- Approved full UI: `FullUI/EquipmentAdvancementUI_FullUI_Review02.png`
- Clean extraction master: `into/EquipmentAdvancementUI_NoOrdinaryText_Master_1078x1459.png`

## Proportion

- Wireframe canvas ratio: `704 / 954 = 0.737945`
- Formal canvas ratio: `1078 / 1459 = 0.738862`
- Ratio deviation: approximately `0.12%`
- Generation and correction used uniform scaling; `ScaleX == ScaleY`.

## Hierarchy

```text
MainPanelBase
|- TopEquipmentPanel -> TopEquipmentSlot
|- QualityPanel -> QualityArrow
|- EquipmentPairPanel
|  |- LeftEquipmentRow -> LeftEquipmentSlot
|  `- RightEquipmentRow -> RightEquipmentSlot
|- ProgressActionPanel -> ProgressTrack, ProgressFill, AdvanceButton
|- HelpButton
`- CloseButton
```

Ordinary/localized text and dynamic numbers are absent from formal assets. Functional `?`, `X`, and quality arrow symbols are retained.

## Review and output

- Default reassembly: `into/ReassemblyPreview/EquipmentAdvancementUI_Reassembly_Default_1078x1459.png`
- Checkerboard preview: `into/ReassemblyPreview/EquipmentAdvancementUI_Reassembly_Checkerboard_1078x1459.jpg`
- Formal output: `Components/out/EquipmentAdvancementUI/`
- Formal PNG count: `25`
- Automated validator: `PASS`
- Final user review: `PENDING`
