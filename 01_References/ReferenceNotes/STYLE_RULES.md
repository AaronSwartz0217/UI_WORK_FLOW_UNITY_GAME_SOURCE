# Style Rules

## Canonical hierarchy

```text
Current wireframe: structure and coordinates only
Cook: primary visual standard
Equipment Identification: secondary component supplement
StyleReference_01.jpg: legacy atmosphere fallback
```

## Primary visual language — Cook

- Modern post-apocalyptic industrial black steel.
- Continuous dark metal surfaces with controlled, readable inset depth.
- Fine silver/steel outer rims and precise layered bevels.
- Restrained amber/gold highlights for active, hover, selected or emphasized states.
- Red is reserved for danger, close, missing or warning states.
- Wear and scratches are visible but controlled; avoid noisy over-decoration.
- Buttons, slots, cards and panels retain complete solid interiors.
- Normal, Hover, Pressed and Disabled variants keep one canvas, silhouette, anchor and subject position.
- Small `+`, `-` and `X` controls use compact square black-steel plates with functional symbols retained.
- Long buttons use the Cook 354x81 family as the preferred proportion and material baseline when the wireframe permits that shape.

## Secondary additions — Equipment Identification

- Use its help-button treatment when a `?` button is required.
- Use its amber-corner slot treatment for equipment or material slots when Cook has no closer match.
- Use its portrait template only for surface, bevel and hierarchy cues; never copy its panel layout.
- Use its IdentifyButton only as a structural/material reference. Do not copy the baked `鉴定` text into unrelated UI.

## Non-negotiable precedence

- The wireframe decides what exists, where it is and how large it is.
- Cook decides how the UI looks.
- Equipment Identification only fills gaps.
- If colors, bevels, wear, button response or border language conflict, follow Cook.
- Never stretch a reference non-uniformly to fit a new target.
- Never let either style set add panels, buttons, slots, labels or content absent from the wireframe.

## Text policy for future generation

- Keep every canonical reference image unchanged, including any text visible inside it.
- Reference text is evidence of typography placement or button treatment only; it is not content to copy.
- Newly generated full-UI review images must omit titles, descriptions, localized labels, action words and dynamic numbers by default.
- After removing text, reconstruct the complete metal, panel or button surface below it; do not leave blur, holes or transparent interiors.
- Preserve functional identification symbols: `X`, `?`, `+`, `-`, arrows and equivalent universally recognizable controls.
- If a future project explicitly requires baked decorative text, record the exception verbatim in its README and `QA/BUTTON_TEXT_MATRIX.md`.
## Stable functional button reuse

- Canonical functional controls such as Close (X), Help (?), Plus (+), Minus (-), and direction arrows may be reused directly from an already validated four-state family.
- Reuse the complete Normal / Hover / Pressed / Disabled family. Rename only the project prefix; do not regenerate, repaint, crop, or resample the source PNGs.
- Preserve the original canvas size, alpha silhouette, pivot, and state-to-state alignment.
- If a different display size is required, resize uniformly in the game engine (or use an approved nine-slice setup). Never non-uniformly stretch or bake a resized replacement.
- Direct reuse is allowed only when the functional role and symbol are identical. Record the source family in the project README, manifest, and button-state matrix.
