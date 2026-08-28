# Cutout Method

- Target Region source: hand-audited on confirmed Review02 at native 1024x1536 resolution.
- Isolation method: crop stops at the outermost visible edge of each component; no parent-panel padding.
- Alpha method: 4x supersampled chamfer silhouette, downsampled with Lanczos.
- Low-alpha cleanup: alpha values 1-5 are forced to 0.
- Visible Bounds: stored per component in `precision_cutout_v03_manifest.json`.
- State Union Bounds: one shared alpha mask per four-state button family.
- CropOffset: `0,0` for V03 component crops.
- Parent reconstruction: blank source texture tiled at original pixel density with mirrored seams and feathered transitions.
- 100% reassembly: PASS.
- 400% edge inspection: PASS.
- Checkerboard inspection: PASS.
- Result: PASS.
