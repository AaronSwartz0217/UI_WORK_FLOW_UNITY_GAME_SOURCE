---
name: produce-iphone-glass-ui-assets
description: Create and validate production-ready frosted or liquid-glass game UI assets from a structural wireframe, using one required GLSDD preset, wireframe-derived per-region colors, URP runtime refraction, true-alpha PNGs, reassembly, and two-round QA.
---

# Produce iPhone-style Glass UI Assets

This is the glass-specialized variant of `produce-game-ui-assets`.

## Required reading and precedence

Before acting, read these files completely in order:

1. `references/master-spec.md`
2. `references/project-contract.md`
3. `references/qa-contract.md`
4. `references/glass-spec.md`

`glass-spec.md` is the variant override. If the inherited documents conflict with it, the glass specification wins only for glass preset handling, color ownership, glass interior alpha, and URP runtime effects. All other base workflow gates remain mandatory.

## Required inputs

Identify and label every input:

- wireframe: structure, panel ratio, count, position, hierarchy, and all UI colors;
- style references: material, bevel, border language, texture, highlight, shadow, and wear only;
- approved preset: `Assets/SHADER/玻璃预设/毛玻璃.json` inside the target Unity project;
- other references: project-specific content only.

Import external files into the active project before storing references. All Markdown and JSON paths must be relative to the file containing them.

## Project creation

Set `ProjectDisplayName`, `ProjectId`, and `ComponentPrefix`. Use ASCII PascalCase and end `ProjectId` with `UI`.

```text
python scripts/scaffold_glass_project.py \
  --workflow-root <UIWorkflow> \
  --project-id <ProjectId> \
  --display-name <ProjectDisplayName> \
  --component-prefix <ComponentPrefix>
```

Do not overwrite an existing project.

## Mandatory glass workflow

1. Enumerate and inspect every input under the project `in/` directory.
2. Measure actual UI bounds and preserve the wireframe with `ScaleX == ScaleY`.
3. Record per-region wireframe colors before applying visual style.
4. Run `scripts/extract_wireframe_palette.py` with an explicit region map.
5. Stop before formal generation if any required region is `Pending`.
6. Confirm the target Unity project contains `Assets/SHADER/玻璃预设/毛玻璃.json`.
7. In GLSDD, load the required preset. Never use silent defaults.
8. Apply Tint from the confirmed wireframe region record. Do not take Tint from a style reference.
9. Preserve preset refraction, blur, opacity, gloss, exposure, diffraction, and related values by default. Only output width, output height, and corner radius may change automatically to match the panel.
10. Treat any other parameter edit as an in-memory candidate. Do not overwrite the approved preset without explicit user confirmation.
11. Generate one complete UI and stop for full-UI approval.
12. After approval, split components and follow the base true-alpha, state-family, hierarchy, crop, reassembly, and output rules.
13. Use the baked transparent PNG as the UI mask/overlay and `UI/URP Frosted Glass Diffraction` for runtime blur, refraction, and color dispersion.
14. Complete the white-model-color-to-generated-color comparison, checkerboard, 100%, 400%, reassembly, and two-round QA.
15. Run `scripts/validate_glass_project.py --project <project> --unity-project <UnityProjectRoot>`.

## Color hard rules

- Wireframe colors own hue identity and regional color assignment.
- Style references must not override wireframe colors.
- Brightness, saturation, and contrast may change only to express material.
- Every glass component needs `WireframeSourceColor`, `GeneratedColor`, `HueDifference`, `SaturationAdjustment`, `BrightnessAdjustment`, and `ColorDecision` records.
- Neutral, ambiguous, or conflicting wireframe regions are `Pending` until the user confirms a color.

## Alpha exception scope

Only components explicitly marked `ComponentMaterial: Glass` may use intentional semi-transparent interiors. Non-glass buttons and slots keep Alpha `255` in their safe interior. Every component still requires true Alpha `0` outside its real silhouette.

## Formal output

Only passing PNGs may enter:

```text
<ProjectId>/Components/out/<ProjectId>/
```

Never place presets, JSON, Markdown, previews, candidates, scripts, materials, shaders, or rejected assets in formal output.
