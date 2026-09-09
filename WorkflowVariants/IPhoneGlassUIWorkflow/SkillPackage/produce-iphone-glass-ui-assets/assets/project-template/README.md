# ProjectDisplayName / ProjectId

## Identity

```text
ProjectDisplayName:
ProjectId:
ComponentPrefix:
Status: queued
```

## Inputs

- Wireframe:
- Style references:
- Other references:

## Glass variant

- WorkflowVariant: `IPhoneGlassUIWorkflow`
- RequiredPreset: `Assets/SHADER/玻璃预设/毛玻璃.json`
- ColorSource: `wireframe`
- ColorMap: `QA/WIREFRAME_COLOR_MAP.json`
- RuntimeShader: `UI/URP Frosted Glass Diffraction`
- StyleReferenceMayOverrideHue: `false`
- GlassComponents:

执行顺序：先读取唯一预设，再从白模对应区域应用 Tint。纯灰、低饱和度或颜色冲突时，将 `ColorDecision` 标记为 `Pending`，正式生成前请求确认。

## Proportion

- Whiteframe actual UI bounds:
- Whiteframe ratio:
- Formal canvas:
- Formal ratio:
- ScaleX:
- ScaleY:

## Hierarchy

```text
MainPanelBase
└─ LargeChildPanel
   └─ SmallPanel / Slot / Button / Icon
```

## Formal output

```text
Components/out/ProjectId/
```

正式目录只允许最终 PNG。

预设、颜色表、Shader、Material、预览和 QA 文档不得放入正式目录。
