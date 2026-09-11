# Glass Color QA

The source controls in the wireframe are neutral gray/white, while the surrounding white-model screen establishes a warm black-gold identity. The generated warm-neutral and amber Tints were explicitly accepted with the full UI on 2026-09-11. Because the source samples are achromatic, `HueDifference` is recorded as 0 and the approval decision is the controlling evidence.

| Component | WireframeSourceColor | GeneratedColor | HueDifference | SaturationAdjustment | BrightnessAdjustment | ColorDecision |
|---|---|---|---:|---:|---:|---|
| InputField | `#9D9D9DFF` | `#C7B8A3FF` | 0.0 | +0.160 | +0.098 | Confirmed |
| ActionButton | `#F5F5F5FF` | `#F5CC8FFF` | 0.0 | +0.420 | -0.010 | Confirmed |

No style-reference palette overrides these colors.
