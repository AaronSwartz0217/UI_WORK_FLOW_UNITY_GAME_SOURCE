# CharacterSetup QA

ProjectDisplayName: 大型登录界面 / 角色创建与装备选择

ProjectId: `LargeLoginUI`

ComponentPrefix: `LargeLoginCharacterSetup`

## Result

- Formal PNG count: 13
- Text baked into PNG: none
- Static component alpha: PASS
- Tight crop and rounded-corner alpha: PASS
- Equipment-card five-state canvas and silhouette: PASS
- Enter-game four-state canvas and silhouette: PASS
- Reassembly at 1464×828: PASS
- Unity prefab validation: PASS — 1 TMP input, 6 buttons, 9 runtime glass panels
- Preview scene validation: PASS — exactly 1 EventSystem
- Runtime shader: `UI/URP Frosted Glass Diffraction`
- Required preset: `Assets/SHADER/玻璃预设/毛玻璃.json`

## Unity entries

- Prefab: `UnityPackage/Assets/LargeLoginUI/CharacterSetup/Prefabs/LargeLoginCharacterSetup.prefab`
- Scene: `UnityPackage/Assets/LargeLoginUI/CharacterSetup/Scenes/LargeLoginCharacterSetupPreview.unity`
- Rebuild command: `Tools > Large Login UI > Character Setup > Rebuild`

Result: PASS
