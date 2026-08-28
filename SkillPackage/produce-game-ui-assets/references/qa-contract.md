# QA Contract

## Proportion

- Measure the actual wireframe panel, excluding presentation margins.
- Enforce `ScaleX == ScaleY`.
- Correct mismatches only through native regeneration or uniform scale plus crop/pad.
- Inspect squares, circles, borders, text, and symbols visually.

## True alpha and crop

- Define a legal Target Region per component.
- Isolate one component without shared background or neighbors.
- Set pixels outside the true silhouette to alpha 0.
- Keep solid interiors near alpha 255; button safe interiors must be 255.
- Clean low-alpha contamination before calculating Visible Bounds.
- Tight-crop static components to Visible Bounds.
- Use the family Union Bounds for interaction states.
- Record CropOffset and original reassembly position.

Fixed rounded/chamfer masks are invalid unless they trace that specific component's actual silhouette. Transparent corners alone do not prove extraction.

## Text and symbols

- Remove ordinary text, localized text, descriptions, and dynamic numbers.
- Retain functional identification symbols.
- Reconstruct the full underlying button or panel surface after text removal.

## States

Buttons normally require Normal, Hover, Pressed, and Disabled.

- Use one Normal master.
- Keep canvas, alpha silhouette, subject position, anchor, and dimensions identical.
- Only state-specific appearance may change.
- Missing required states means fail unless a product-backed Not Applicable entry exists.

## Required project documents

- `README.md`
- `QA/FINAL_QA.md`
- `QA/ASSET_MANIFEST.md`
- `QA/COMPONENT_COORDINATES.md`
- `QA/BUTTON_TEXT_MATRIX.md`
- `QA/PROPORTION_LOOP_01.md`
- `QA/CUTOUT_METHOD.md` for nontrivial extraction

## Completion

Require passing 100%, 400%, checkerboard, hierarchy, naming, size, alpha, state-family, proportion, and reassembly checks plus user approval.
