# Button Text Preservation Matrix

| Component | Expected content | Role | Normal | Hover | Pressed | Disabled | Result |
|---|---|---|---|---|---|---|---|---|
| PrimaryActionButton | `鉴定` | EmbeddedActionText | Pass | Pass | Pass | Pass | Pass |
| CloseButton | `×` | Symbol | Pass | Pass | Pass | Pass | Pass |
| HelpButton | `?` | Symbol | Pass | Pass | Pass | Pass | Pass |

Rules applied:
- Text or symbols originally embedded in a button are preserved in every required state.
- Only dynamic values or text explicitly assigned to an engine text node may be removed.
- State generation may change lighting/color response, but not wording, glyph identity, spelling, alignment, or text presence.
