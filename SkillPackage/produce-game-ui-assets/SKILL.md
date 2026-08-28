---
name: produce-game-ui-assets
description: Create, review, split, validate, and export production-ready raster game UI assets from wireframes and style references. Use when Codex is asked to generate a game UI screen or popup, continue a UI production queue, remove UI text, split parent/child panels, create four-state buttons, produce true-alpha cutouts, preserve wireframe proportions, reassemble components for QA, or export final PNGs into a project Components/out/ProjectId folder.
---

# Produce Game UI Assets

Build one reviewed UI project at a time from a structural wireframe and shared style references.

## Required reading

Before producing or modifying assets, read `references/master-spec.md` completely. Then read:

- `references/project-contract.md` for paths, naming, project stages, and output rules.
- `references/qa-contract.md` before splitting, exporting, or reporting completion.

Use `references/status-and-queue.md` only when the user asks what is finished, requests the next queued UI, or continues the bundled workflow.

## Locate the workspace

Prefer a user-supplied workflow root. Otherwise search the current workspace for `UIWorkflow/README.md`.

Treat every path stored in Markdown or JSON as relative to the file containing it. Do not introduce machine-specific absolute paths. Import external inputs into the workflow before storing references to them.

## Establish inputs

For every project, identify and label:

- wireframe: structure, panel ratio, count, position, hierarchy;
- style references: materials, palette, wear, bevels, borders, button finish;
- other references: project-specific visual content only.

Always enumerate and inspect every file under the workflow style-reference directory. Copy the references actually used into the project `in/` directory.

Also enumerate `01_References/SharedComponents/` when it exists. Read `references/shared-components.md`, inspect the bundled examples under `assets/shared-components/`, and copy every shared component actually used into the active project's `in/` directory. Treat these files as shape, material, symbol, and state references unless the user explicitly authorizes direct reuse.

Never let a style reference change the wireframe layout. Never let a wireframe substitute for the required visual style.

## Create a project

Set `ProjectDisplayName`, `ProjectId`, and `ComponentPrefix` before generation. Use ASCII PascalCase; end `ProjectId` with `UI`.

Create a project with:

```text
python scripts/scaffold_project.py \
  --workflow-root <UIWorkflow> \
  --project-id <ProjectId> \
  --display-name <ProjectDisplayName> \
  --component-prefix <ComponentPrefix>
```

Do not overwrite an existing project. Resume it from its `project.json` and QA documents.

## Execute the gated workflow

1. Read inputs and measure the actual UI panel bounds. Ignore presentation margins.
2. Generate a full UI at a native matching ratio. Enforce `ScaleX == ScaleY`.
3. Run numerical and visual proportion checks: squares, circles, border thickness, symbols, and text deformation.
4. Save the full draft under `FullUI/` and stop for user review.
5. Only after approval, remove ordinary/localized text and dynamic numbers. Retain functional symbols such as X, plus, minus, and arrows.
6. Produce a pure `MainPanelBase`, then empty large child panels, then grandchildren such as slots, buttons, icons, tracks, and thumbs.
7. Keep child panels out of their parent images. Place them back by coordinates in the reassembly preview.
8. Extract one component at a time using its true silhouette. Cropping alone is not extraction.
9. Keep button and slot interiors solid. Their interior safe region must remain alpha 255.
10. Generate Normal, Hover, Pressed, and Disabled from one Normal master. Use one Union Bounds, canvas, anchor, and CropOffset for the family.
11. Tight-crop static components to Visible Bounds. Record Target Region, Visible Bounds, Union Bounds, CropOffset, and reassembly position.
12. Reassemble at original coordinates under `into/ReassemblyPreview/`.
13. Run 100%, 400%, checkerboard, naming, alpha, state, ratio, hierarchy, and reassembly QA.
14. Export only passing final PNGs to `Components/out/ProjectId/`.
15. Update project README, manifest, coordinates, button matrix, proportion loop, cutout method, and final QA.
16. Report the full-UI or final-output folder and wait for user review before starting another UI.

## Generate or edit raster UI

When raster generation or editing is required, use the available image-generation capability and follow its own skill instructions. Explicitly state each input image role in the prompt. Preserve invariants aggressively during edits.

## Naming

Use:

```text
ComponentPrefix_ComponentName_State_WidthxHeight.png
```

Example:

```text
EquipmentCrafting_CloseButton_Normal_65x63.png
```

The dimensions must equal the final PNG canvas. Within a state family only `State` may change.

## Validate

Run:

```text
python scripts/validate_project.py --project <project-directory>
```

Treat any error as a failed export. Do not report completion while required states, alpha integrity, naming, documentation, or user review are missing.

## Output boundary

The only formal asset directory is:

```text
<ProjectId>/Components/out/<ProjectId>/
```

Keep left, right, upper, and lower components together. Do not place Markdown, JSON, previews, candidates, rejected assets, scripts, or old versions in formal output.
