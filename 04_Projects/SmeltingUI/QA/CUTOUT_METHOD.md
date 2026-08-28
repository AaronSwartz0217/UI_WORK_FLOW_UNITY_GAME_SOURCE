# Cutout Method

- PanelSelectionMode: `AllDetected` under explicit full-automation authorization.
- Source: `FullUI/SmeltingUI_FullUI_Review02_1024x1536.png`.
- Bounds: native-resolution connected-edge measurement followed by manual visual confirmation.
- Alpha: component-specific 4x supersampled chamfer silhouettes; values 1-5 cleaned to 0.
- Parent reconstruction: horizontal and vertical blank same-source textures blended into one continuous background, then used to replace every child region.
- Close button: Cook canonical family copied verbatim with project-prefix rename.
- Button states: all derived from one Normal master and reuse its alpha mask.
- Visible Bounds / Union Bounds / CropOffset: recorded in `split_v01_manifest.json` and `COMPONENT_COORDINATES.md`.
- 100% reassembly: PASS.
- 400% edge inspection: PASS.
- Checkerboard: PASS.
- Parent child-residue inspection: PASS.

Result: `PASS`.
