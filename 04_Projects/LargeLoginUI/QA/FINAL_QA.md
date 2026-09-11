# Final QA

- [x] User approved the complete visual draft before component splitting.
- [x] Legacy Cook, Equipment identification and industrial shared templates are excluded.
- [x] The wireframe controls layout, placement and black/gold color tendency.
- [x] No text is baked into formal PNG assets.
- [x] Background, input surface and action-button states have exact filename dimensions.
- [x] Transparent glass components have alpha 0 outside the rounded silhouette.
- [x] The four action-button states use the same 312×56 canvas and identical alpha silhouette.
- [x] Reassembly preview exists at `into/ReassemblyPreview/LargeLoginUI_Reassembly_NoText_1464x828.png`.
- [x] Glass Tint originates from the login wireframe and the user-approved full UI, not a legacy style template.
- [x] `WireframeSourceColor`, `GeneratedColor`, `HueDifference`, `SaturationAdjustment`, `BrightnessAdjustment`, and `ColorDecision` are recorded.
- [x] The copied preset SHA-256 matches the supplied source preset.
- [x] Unity 2022.3.62f3c1 compiled the package through Unity CLI.
- [x] Generated prefab contains 2 TMP input fields, 2 buttons and 4 `URPFrostedGlassPanel` components.
- [x] Password input uses `TMP_InputField.ContentType.Password`.
- [x] Preview scene contains exactly one EventSystem; the portable prefab contains none.
- [x] URP Opaque Texture is enabled by the rebuild tool.
- [x] Formal output contains PNG files only.

## CharacterSetup addendum

- [x] The user's request to split the presented CharacterSetup draft is recorded as the full-UI approval gate.
- [x] CharacterSetup is separated from LoginScreen by folder and the validator-compatible `LargeLogin_CharacterSetup` filename prefix.
- [x] The parent panel does not bake in the name input, current-equipment slot, cards, labels, or button.
- [x] Thirteen CharacterSetup PNGs have exact filename dimensions.
- [x] Every rounded component is tight-cropped to the straight edges and has alpha 0 only outside its true rounded silhouette.
- [x] All glass centers remain intentionally translucent and are recorded as `ComponentMaterial: Glass`.
- [x] Equipment-card `Normal`, `Hover`, `Pressed`, `Disabled`, and `Selected` use one 184×164 canvas and identical alpha silhouette.
- [x] Enter-game `Normal`, `Hover`, `Pressed`, and `Disabled` use one 368×72 canvas and identical alpha silhouette.
- [x] CharacterSetup reassembly preview exists at `into/ReassemblyPreview/LargeLoginCharacterSetup_Reassembly_NoText_1464x828.png`.
- [x] CharacterSetup checkerboard exists at `QA/LargeLoginCharacterSetup_AlphaCheckerboard.png`.
- [x] Unity 2022.3.62f3c1 compiled and generated the CharacterSetup package.
- [x] CharacterSetup prefab contains 1 TMP input field, 6 buttons, and 9 `URPFrostedGlassPanel` components.
- [x] CharacterSetup preview scene contains exactly one EventSystem; its portable prefab contains none.

Result: PASS
