# 主界面 HUD / MainHUDUI

## Identity

```text
ProjectDisplayName: 主界面 HUD
ProjectId: MainHUDUI
ComponentPrefix: MainHUD
Status: unity_integrated_manual_screenshot_pending
```

## Input roles

- `in/MainHUD_Wireframe_1559x880.jpg`: layout, hierarchy, component count, placement, and all color identities.
- `in/MainHUD_GlassStyleReference_1670x942.png`: primary authority for semi-transparent glass density, surface sheen, and blue-grey glass response.
- `in/MainHUD_CurrentGlassMaterialReference_1464x828.png`: secondary runtime material reference from the earlier login/character flow.
- `in/MainHUD_FrostedGlassPreset.json`: Unity runtime glass parameter source.
- Cook, Equipment identification, and legacy black-steel/amber shared components are explicitly excluded from this page.

## Selection

`PanelSelectionMode: ExplicitOnly`

- Include the 1559x880 main HUD and its explicit arrow, team invite, mode dropdown, GM tools, menu, return-city, recharge, mutation, and hotbar-slot controls.
- Keep the functional `>` and dropdown arrow symbols.
- Render localized labels, names, shortcut-key labels, coordinates, health values, currency values, and other dynamic numbers with TMP.
- The unlabelled bottom-center white rectangle is `Pending` and is excluded from formal assets until its role is confirmed.
- `功能按钮弹窗.jpeg` and `排行榜.jpeg` are related future pages, not children of this production pass.

## Visual rules

- Whiteframe colors remain authoritative: navy background, darker lower HUD plate, neutral pale controls, cyan/green/blue/red/yellow functional accents.
- Use rounded Apple-like frosted glass with a gradual edge transition, semi-transparent interiors, and slight surface gloss.
- Do not add `_EdgeGlow`, duplicate `_SoftGlow`, hard strokes, bright rim outlines, industrial metal, scratches, or worn black-and-amber decoration.
- Bloom remains subtle and is not baked into individual component silhouettes.
- The full-screen blue field is not an asset. The formal HUD overlay uses alpha 0 so the future 3D gameplay camera remains visible.
- Only the lower HUD plate and individual controls retain translucent glass surfaces.
- Glass buttons and slots intentionally keep a median safe-area alpha around 64/255, matching the first two pages so the runtime shader can refract and blur the game view. Colored health, mana, loading, mutation, and warning fills remain substantially opaque for readability.

## Proportion

- Whiteframe actual UI bounds: full 1559x880 canvas.
- Whiteframe ratio: 1.77159.
- Formal canvas: 1559x880.
- ScaleX: 1.0.
- ScaleY: 1.0.

## Planned Unity hierarchy

```text
MainHUD
├── Header
│   ├── PartyPanel
│   ├── PlayerStatusPanel
│   └── TopRightActions
├── BottomHUD
│   ├── ProgressBars
│   ├── ResourceBars
│   ├── Hotbar
│   └── MutationButton
└── MinimapPanel
    ├── ReturnCityButton
    └── CurrencyAndRecharge
```

The page is configured in `UI场景测试` as:

- `Assets/MainHUDUI/Prefabs/MainHUD.prefab`
- `Assets/UI场景测试/Scenes/MainHUD.unity`
- `Assets/UI场景测试/Scenes/LoginCharacterFlow.unity`

Runtime flow:

```text
LoginScreen
  -> successful login
CharacterSelectionScreen
  -> EnterGameButton
MainHUDScreen
```

`MainHUDScreen` contains no full-screen `Background` object. The standalone test scene uses `PreviewWorldBackdrop_ReplaceWith3DScene` only as a temporary opaque source for glass sampling; replace it with the future 3D world.

## Formal output

`Components/out/MainHUDUI/` contains 57 formal transparent PNG files:

- 9 interactive families with Normal/Hover/Pressed/Disabled states;
- Hotbar also includes Selected;
- 20 static panel/bar/minimap/currency components;
- no localized text or dynamic numbers baked into PNG files;
- `>` and dropdown chevron remain in their functional symbol buttons.

QA references:

- `QA/MainHUD_AlphaCheckerboard_1559x880.png`
- `QA/MainHUD_ButtonStates.png`
- `into/ReassemblyPreview/MainHUD_Reassembly_NoText_1559x880.png`

Unity text uses the dynamic Source Han Sans SC TMP font. Final in-Editor screenshot review remains assigned to the user.
