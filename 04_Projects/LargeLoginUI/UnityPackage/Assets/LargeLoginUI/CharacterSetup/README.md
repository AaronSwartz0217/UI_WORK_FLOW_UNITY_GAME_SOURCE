# CharacterSetup layout

This folder contains the independently generated character-name and equipment-selection layout. Its art, materials, prefab, preview scene and editor builder do not share filenames with `../LoginScreen/`.

Component filenames use the validator-compatible `LargeLogin_CharacterSetup` prefix. The generated set contains a background, empty main panel, name input, current-equipment slot, five-state reusable equipment card, and four-state enter-game button.

Unity entry points:

- `Prefabs/LargeLoginCharacterSetup.prefab`
- `Scenes/LargeLoginCharacterSetupPreview.unity`
- `Editor/LargeLoginCharacterSetupPrefabBuilder.cs`
- Menu: `Tools > Large Login UI > Character Setup > Rebuild`

All visible copy is rendered with TextMeshPro. The PNG files contain no baked text or weapon imagery. The prefab contains no EventSystem; the preview scene contains exactly one.
