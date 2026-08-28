# Button Text Preservation Matrix

| Component | Expected content | Role | Normal | Hover | Pressed | Disabled | Result |
|---|---|---|---|---|---|---|---|---|
| CloseButton | `×` | Symbol | Pass | Pass | Pass | Pass | Pass |
| MaximumButton | `最大` | EmbeddedActionText | Pass | Pass | Pass | Pass | Pass |
| QuantityMinusButton | `−` | Symbol | Pass | Pass | Pass | Pass | Pass |
| QuantityPlusButton | `+` | Symbol | Pass | Pass | Pass | Pass | Pass |
| RecipeSelectionButton | `菜名` | EmbeddedActionText | Pass | Pass | Pass | Pass | Pass |
| StartButton | `开始` | EmbeddedActionText | Pass | Pass | Pass | Pass | Pass |

Rules applied:
- Text or symbols originally embedded in a button are preserved in every required state.
- Only dynamic values or text explicitly assigned to an engine text node may be removed.
- State generation may change lighting/color response, but not wording, glyph identity, spelling, alignment, or text presence.
