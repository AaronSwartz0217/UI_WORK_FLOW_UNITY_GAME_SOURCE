# Glass Variant Specification

## 1. Required preset

The only approved runtime preset path is:

```text
Assets/SHADER/玻璃预设/毛玻璃.json
```

Rules:

1. Read this preset before every glass UI bake.
2. The GLSDD “读取指定预设” action loads this exact file.
3. Do not create per-UI presets under `into/GlassPresets`.
4. If the file is missing, unreadable, malformed, or has an unsupported version, stop the bake and report the failure.
5. Output width, output height, and corner radius may follow the current panel ratio. Refraction, blur, opacity, gloss, exposure, diffraction, and all other material parameters inherit the approved preset by default.
6. Non-default parameter edits remain candidate settings in memory. Only an explicit user confirmation permits overwriting the approved preset.
7. Project README, QA, and `project.json` record only the relative runtime path shown above.
8. The preset never belongs in `Components/out/<ProjectId>/`; formal output remains PNG-only.

The variant repository contains the user-supplied source file at:

```text
UnityPackage/Assets/SHADER/玻璃预设/毛玻璃.json
```

The install script copies it to the required runtime path without changing its values.

## 2. UI color ownership

Final UI color comes from the wireframe.

The wireframe owns:

- layout;
- panel proportions;
- component count;
- hierarchy and position;
- primary, secondary, local, warning, accent, and disabled colors;
- brightness relationships.

Style references own only:

- material response;
- border language;
- bevels;
- highlights and shadows;
- surface texture and wear;
- gloss character.

Style-reference colors must never replace wireframe colors.

## 3. Per-region extraction

For every required component region, record:

```text
WireframeSourceColor
GeneratedColor
HueDifference
SaturationAdjustment
BrightnessAdjustment
ColorDecision
```

The initial Tint must equal the confirmed `WireframeSourceColor`. Material tuning may adjust saturation and brightness, but must preserve hue identity. Blue stays blue; red, yellow, and green regions must not be converted to another theme.

If the wireframe region is neutral gray, too low in saturation, visually ambiguous, or contains conflicting dominant colors, set `ColorDecision: Pending` and request confirmation before formal generation.

## 4. Glass Tint and GLSDD

Use the generated `QA/WIREFRAME_COLOR_MAP.json` as the GLSDD Tint source:

1. Load the approved preset.
2. Enter the component ID.
3. Click “从白模颜色表应用 Tint”.
4. Confirm GLSDD reports a confirmed color decision.
5. Bake the RGBA PNG.

The editor blocks baking when either the required preset or confirmed wireframe Tint has not been loaded.

## 5. Baked and runtime responsibilities

The baked PNG contains:

- true-alpha silhouette;
- base translucent tint;
- border/highlight/gloss information that belongs to the glass surface.

The URP Shader contains:

- scene-dependent background blur;
- refraction;
- lens deformation;
- RGB diffraction;
- runtime exposure response.
- final composition that preserves the baked PNG Alpha, caps it with `_OutputAlpha`, and multiplies it by uGUI `Image.color.a`.

Do not fake scene refraction by baking a screenshot background into the PNG.
Do not convert the valid glass mask back to solid output Alpha. The mask controls where the effect exists; the lower of baked PNG Alpha and `_OutputAlpha` controls how transparent it remains in the scene.

## 6. QA

Besides the base QA contract, verify:

- required preset exists at the exact runtime path;
- preset version and required fields are valid;
- every glass output maps to one confirmed wireframe region;
- style-reference color did not replace wireframe color;
- Tint came from `WireframeSourceColor`;
- all six color QA fields are present;
- glass interior semi-transparency is intentional and recorded;
- pixels outside the real silhouette are Alpha `0`;
- runtime material uses `UI/URP Frosted Glass Diffraction`;
- runtime Shader output uses source PNG Alpha plus an explicit `_OutputAlpha` ceiling rather than a solid effect mask;
- color comparison, checkerboard, 100%, 400%, and reassembly checks pass.

## 7. Short invocation prompt

```text
使用 $produce-iphone-glass-ui-assets 处理当前 UI。

毛玻璃统一读取：
Assets/SHADER/玻璃预设/毛玻璃.json

所有 UI 和组件的主色、辅色、区域颜色及强调色必须来自白模 UI。
风格参考只能提供材质、边框、倒角、纹理、高光和磨损语言，
不得用风格参考的配色覆盖白模颜色。

毛玻璃 Tint 也从白模对应面板区域取色。
完成透明 PNG、URP Shader 接入、颜色对照、棋盘格检查、
原位回拼和两轮 QA 后再进入正式输出。
```
