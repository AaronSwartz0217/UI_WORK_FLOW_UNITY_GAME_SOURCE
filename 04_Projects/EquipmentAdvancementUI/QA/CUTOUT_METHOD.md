# Cutout Method

- Target Region source: measured from the approved `1078x1459` clean master.
- Isolation method: one named component per fixed legal target region.
- Parent/child separation: child target regions are replaced with neighboring parent texture before parent export.
- Alpha method: component-specific rounded silhouette masks; exterior pixels set to alpha `0`.
- Low-alpha cleanup: masks use binary opaque interiors and transparent exteriors.
- Visible Bounds method: exported canvas equals the measured legal component region.
- State Union Bounds method: every state is derived from one Normal master and reuses its alpha channel.
- CropOffset storage: recorded in `COMPONENT_COORDINATES.md`.
- 100% check: passed.
- 400% check: passed.
- Checkerboard check: passed.
- Result: `PASS`
