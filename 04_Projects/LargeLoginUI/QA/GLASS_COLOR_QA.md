# Glass Color QA

The source controls in the wireframe are neutral gray/white, while the surrounding white-model screen establishes a warm black-gold identity. The generated warm-neutral and amber Tints were explicitly accepted with the full UI on 2026-09-11. Because the source samples are achromatic, `HueDifference` is recorded as 0 and the approval decision is the controlling evidence.

| Component | WireframeSourceColor | GeneratedColor | HueDifference | SaturationAdjustment | BrightnessAdjustment | ColorDecision |
|---|---|---|---:|---:|---:|---|
| InputField | `#9D9D9DFF` | `#C7B8A3FF` | 0.0 | +0.160 | +0.098 | Confirmed |
| ActionButton | `#F5F5F5FF` | `#F5CC8FFF` | 0.0 | +0.420 | -0.010 | Confirmed |
| CharacterSetupMainPanel | `#999999FF` | `#AD8F66FF` | 0.0 | +0.410 | +0.078 | Confirmed |
| CharacterSetupNameInput | `#F5F5F5FF` | `#C7B8A3FF` | 0.0 | +0.180 | -0.181 | Confirmed |
| CharacterSetupCurrentEquipmentSlot | `#FAFAFAFF` | `#D1B080FF` | 0.0 | +0.388 | -0.160 | Confirmed |
| CharacterSetupEquipmentCard | `#F5F5F5FF` | `#D1B385FF` | 0.0 | +0.364 | -0.141 | Confirmed |
| CharacterSetupEnterGameButton | `#F5F5F5FF` | `#F5CC8FFF` | 0.0 | +0.420 | -0.010 | Confirmed |

No style-reference palette overrides these colors.

The CharacterSetup source regions are also achromatic. Their warm black-gold resolution follows the presented complete draft; the user's request to split that presented draft into components is recorded as approval evidence on 2026-09-11. `HueDifference` remains 0 because the source hue is undefined.
