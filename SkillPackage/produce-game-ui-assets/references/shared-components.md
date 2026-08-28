# Shared Component References

The bundled files under `assets/shared-components/` are mandatory visual references when their component class appears in a project.

## Inventory

| File | Role | Invariant |
|---|---|---|
| `CloseButtons/Shared_CloseButton_RedX_Reference_52x56.png` | red close button | retain the functional X symbol and the complete solid button plate |
| `Buttons/Shared_HelpButton_AmberQuestion_Reference_52x56.png` | help button | retain the functional question-mark symbol and complete solid plate |
| `Buttons/Shared_LongButton_DarkNormal_Reference_354x81.png` | long dark button, baseline appearance | use as the structural/state-family baseline |
| `Buttons/Shared_LongButton_AmberHighlight_Reference_354x81.png` | matching amber highlight appearance | pair only with the 354x81 dark baseline; preserve canvas and silhouette |
| `Slots/Shared_SquareSlot_AmberCorners_Reference_94x90.png` | compact slot or inset panel | preserve the near-square source ratio and corner accents |
| `PanelBorders/Shared_LargeSquarePanel_BlackSteel_Reference_227x227.png` | large black-steel square panel | preserve the 1:1 ratio, layered rim, and amber fastener accents |

## Use rules

- Wireframes remain authoritative for layout, count, target dimensions, and hierarchy.
- These references define visual language: black forged steel, restrained amber accents, beveled rims, wear, inset depth, and functional-symbol treatment.
- Do not stretch a reference to fit. Generate at the target ratio or apply uniform scaling plus crop/pad.
- The two 354x81 long-button files are a matched appearance pair, not unrelated layouts.
- X and question mark are functional identification symbols and remain in exported symbol-button assets.
- For non-symbol buttons, remove localized/action text only, then reconstruct the solid underlying plate and texture.
- Reference PNGs are inputs, not automatic formal outputs. Direct reuse still requires project naming, state completion, alpha checks, and user approval.
