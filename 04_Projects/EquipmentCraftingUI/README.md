# Equipment Crafting UI

## Button text contract

Buttons carrying an action label or identifying symbol in the layout reference keep it inside every exported state. This project preserves `鉴定`, `×`, and `?`.

## References

- `in/EquipmentCrafting_LayoutReference_800x1006.jpg`: strict portrait layout reference.
- `in/EquipmentCrafting_StyleReference_1620x952.jpg`: strict industrial visual-style reference.

## Selection

`PanelSelectionMode: ConfirmSelection`

User confirmation: all 17 detected resources included.

## Text policy

- Page title, attribute labels, quality, values, material quantities and status messages are engine text.
- `?` and `×` remain baked because they identify button actions.
- The primary action label remains separate engine text.

## Migrated workflow location

- Project root: `04_Projects/EquipmentCraftingUI/`
- Formal output: `Components/out/EquipmentCraftingUI/`
- QA: `QA/`
- The original desktop project remains unchanged as a migration source.
- Current workflow validation: `Needs Revision`; coordinate and proportion-loop documents are missing.

## Output policy

- Complete no-text effect mockup is stored in `into`.
- `Components/out/EquipmentCraftingUI` contains one component per PNG.
- Components use true Alpha and are cropped to the high-confidence outer border.
- Filename dimensions equal actual canvas dimensions.
- No prototype blue, ordinary text, dynamic value, item image or screenshot background appears in components.

## Shared masters

- SpecialAttributeRow and SpecialSkillRow use one shared visual master but separate files and responsibilities.
- EquipmentSlot, SkillSlot, MaterialSlotLeft and MaterialSlotRight use one shared slot master.

## Button states

All three button groups include `Normal`, `Hover`, `Pressed`, and `Disabled`.

- Every state group uses an identical canvas and Alpha mask.
- Hover is brighter and slightly more saturated.
- Pressed is darker with increased inset contrast.
- Disabled is desaturated, darker, and lower contrast.
- `QA/BUTTON_STATE_COMPARISON.png` provides the visual comparison.
- `QA/BUTTON_STATE_MATRIX.md` records validation.
