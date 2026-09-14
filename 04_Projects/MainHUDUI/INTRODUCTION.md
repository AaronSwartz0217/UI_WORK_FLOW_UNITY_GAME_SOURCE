# MainHUDUI Introduction

## Identity

```text
ProjectDisplayName: 主界面 HUD
ProjectId: MainHUDUI
ComponentPrefix: MainHUD
TargetCanvas: 1559x880
TargetPlatform: Unity uGUI / URP
```

## Design authority

- Layout, scale, coordinates, and functional colors: `in/MainHUD_Wireframe_1559x880.jpg`.
- Primary glass appearance: `in/MainHUD_GlassStyleReference_1670x942.png`.
- Runtime glass parameters: `in/MainHUD_FrostedGlassPreset.json`.
- The blue field in the style reference is not exported. The gameplay viewport remains transparent.
- Legacy Cook, Equipment identification, and black-steel/amber assets are excluded.

## Directory roles

```text
in/                         immutable references
into/                       candidates and reassembly previews
Components/out/MainHUDUI/   formal component PNG files
Templates/                  clean structural template
FullUI/                     complete-page visual references
QA/                         manifests and visual/data checks
tools/                      deterministic component exporters
UnityPackage/               portable Unity source package
```

## Assets and states

- 57 formal component PNG files.
- Expand, team invite, mode dropdown, GM tools, menu, return-city, recharge, mutation, and hotbar controls have Normal/Hover/Pressed/Disabled states.
- Hotbar also has Selected.
- Glass surfaces use a center alpha around 64/255, synchronized with the login and character pages so the URP glass shader can sample the scene.
- Functional colored fills remain opaque enough to read.
- Localized labels, shortcut keys, player values, health values, coordinates, and currencies are TMP nodes.
- Only the `>` and dropdown chevron are baked because they are stable functional symbols.

## Anchoring and assembly

All coordinates use top-left `x, y, width, height` values on a 1559x880 reference canvas. Unity converts them to centered RectTransform coordinates. `CanvasScaler` uses Scale With Screen Size, reference resolution 1559x880, and match value 0.5.

The main groups are:

```text
MainHUDScreen
├── top-left party controls
├── top-center player health
├── top-right action buttons
├── lower HUD plate
│   ├── loading/mutation/resource bars
│   ├── 13 hotbar buttons
│   └── mutation button
└── minimap, return-city, currencies, and recharge
```

No full-screen Image is present on `MainHUDScreen`, allowing the 3D scene to render behind it.

## Unity import and runtime material

- Texture Type: Sprite (2D and UI)
- Sprite Mode: Single
- Filter Mode: Bilinear
- Wrap Mode: Clamp
- Mip Maps: Off
- Compression: Uncompressed
- Alpha Is Transparency: On
- Runtime shader: `UI/URP Frosted Glass Diffraction`
- `_EdgeGlow = 0`, no `_SoftGlow` helper layer
- Bloom threshold 0.92, intensity 0.24, scatter 0.46

Generated Unity assets:

- `Assets/MainHUDUI/Prefabs/MainHUD.prefab`
- `Assets/UI场景测试/Scenes/MainHUD.unity`
- `Assets/UI场景测试/Scenes/LoginCharacterFlow.unity`

The integrated scene routes `CharacterSelectionScreen/EnterGameButton` to `MainHUDScreen` through `LoginToCharacterFlowController`.

## Known limitation

The unlabelled 78x30 white center marker remains `Pending`; it is present only in the reassembly preview and is not a formal Unity component. The standalone HUD scene contains a temporary non-blue backdrop named `PreviewWorldBackdrop_ReplaceWith3DScene`; replace it when the real 3D environment is supplied.

## QA result

Data, alpha, state, reassembly, prefab, and scene-builder validation pass. Final screenshot judgement in the Unity Game view is intentionally left to the user.
