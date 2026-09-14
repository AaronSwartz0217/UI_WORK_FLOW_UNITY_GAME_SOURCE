# Cutout Method

- Target Region source: exact rectangles measured from `MainHUD_Wireframe_1559x880.jpg` and recorded in `COMPONENT_COORDINATES.md`.
- Isolation method: deterministic per-component rendering; no screenshot rectangles or surrounding background pixels are copied.
- Alpha method: supersampled rounded masks at 4x, downsampled with Lanczos antialiasing. Glass surfaces use intentional interior translucency; functional fills remain opaque.
- User override: the latest direction explicitly requires semi-transparent glass PNG interiors so the generated URP shader can show through. The ordinary solid-button-interior rule is therefore recorded as Not Applicable for these shader-driven glass controls.
- Low-alpha cleanup: pixels are generated from a clean mask; no chroma-key conversion and no color spill exist.
- Visible Bounds method: each component canvas equals its whiteframe Target Region. Rounded corners contain only necessary antialiasing transparency.
- State Union Bounds method: every state family is rendered from one Normal geometry and uses the same canvas, mask, position, and anchor.
- CropOffset storage: `0,0` for all formal components because the exact Target Region is already the tight component canvas.
- 100% check: Pass via `export_hud_components.py` and direct checkerboard review.
- 400% check: Pass; no hard outline, chroma fringe, black fringe, or detached glow layer.
- Checkerboard check: Pass in `MainHUD_AlphaCheckerboard_1559x880.png` and `MainHUD_ButtonStates.png`.
- Shader-readiness check: Pass; median safe-area Alpha for button/slot glass is constrained to 48–96, with the normal neutral glass center at approximately 64/255 to match the login and character pages.
- Result: PASS
