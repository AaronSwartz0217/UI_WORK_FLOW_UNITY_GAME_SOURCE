# Full UI generation prompt

Mode: built-in image generation, two-image style-transfer followed by one precise edge-treatment edit.

## Input roles

- `in/MainHUD_Wireframe_1559x880.jpg`: absolute authority for layout, hierarchy, count, placement, size, spacing, and color identity.
- `in/MainHUD_CurrentGlassMaterialReference_1464x828.png`: material-only reference for frosted translucency, rounded softness, and restrained gloss.

## Final prompt summary

Create a flat 1559x880 Unity game HUD that preserves the wireframe layout and navy/cyan/green/blue/red/yellow palette. Remove ordinary text and dynamic values while retaining the top-left greater-than arrow and dropdown chevron. Apply low-contrast Apple-like frosted glass with mild inner blur and a faint broad top sheen. Do not use gold recoloring, industrial metal, scratches, hard borders, closed luminous rims, halos, duplicate glow layers, heavy bloom, new controls, or layout changes.

The second pass changed only edge treatment: all closed strokes and bright perimeter lines were removed while geometry, color, count, and placement were preserved.

After user review, the generated draft was retained only as the visual-style master. The final review overlay was reconstructed at exact whiteframe coordinates by `tools/build_hud_overlay.py`: the blue full-screen field was removed, bar heights were restored to 17-21 px, hotbar slots to 56x56, and the lower HUD/minimap regions to their measured whiteframe bounds.
