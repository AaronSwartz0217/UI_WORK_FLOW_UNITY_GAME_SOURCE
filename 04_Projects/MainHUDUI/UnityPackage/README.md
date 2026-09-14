# MainHUDUI Unity Package

This folder mirrors the validated Unity assets from `C:/Users/Administrator/Desktop/UI场景测试`.

## Included

- `Assets/MainHUDUI/Art`: 57 semi-transparent formal PNG components and Unity `.meta` files.
- `Assets/MainHUDUI/Config`: supplied frosted-glass preset.
- `Assets/MainHUDUI/Editor/MainHUDPrefabBuilder.cs`: deterministic uGUI prefab generator and validator.
- `Assets/MainHUDUI/Materials`: generated URP glass materials.
- `Assets/MainHUDUI/Prefabs/MainHUD.prefab`: transparent gameplay HUD.
- `Assets/UI场景测试/Scenes/MainHUD.unity`: standalone HUD test scene.
- `Assets/UI场景测试/Scenes/LoginCharacterFlow.unity`: integrated three-page flow.
- `Assets/UI场景测试/Scripts/LoginToCharacterFlowController.cs`: login, character-selection, and Enter Game transitions.
- `Assets/Editor/LoginCharacterFlowBuilder.cs`: integrated scene builder and structural validator.

## Dependencies

Import the existing LargeLoginUI package and the repository's `WorkflowVariants/IPhoneGlassUIWorkflow/UnityPackage/Assets/URPFrostedGlass` runtime before rebuilding. The project must use URP, TextMeshPro, Source Han Sans SC Dynamic SDF, camera opaque texture, and post-processing.

The GitHub repository intentionally ignores raster images. The complete PNG set is available in the local workflow project and desktop delivery; `tools/export_hud_components.py` deterministically regenerates it.

## Runtime flow

```text
LoginScreen -> CharacterSelectionScreen -> MainHUDScreen
```

The character page's `EnterGameButton` is serialized into `LoginToCharacterFlowController`. The HUD has no full-screen background. Replace `PreviewWorldBackdrop_ReplaceWith3DScene` in the standalone scene with the real 3D scene when available.

Glass and hotbar centers use approximately 64/255 source Alpha. Functional fills remain more opaque. `_EdgeGlow` and `_SoftGlow` are disabled, and Bloom is threshold 0.92 / intensity 0.24 / scatter 0.46.
