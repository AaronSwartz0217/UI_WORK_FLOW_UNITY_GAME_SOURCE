# Cutout Method

- Target Region source: measured from the approved `1078x1459` clean master.
- Isolation method: one named component per fixed legal target region.
- Parent/child separation: CleanParentV02 replaces child regions with blank same-source black-steel texture at original pixel density; no directional smear fill remains.
- Alpha method: component-specific rounded silhouette masks; exterior pixels set to alpha `0`.
- Low-alpha cleanup: masks use binary opaque interiors and transparent exteriors.
- Visible Bounds method: exported canvas equals the measured legal component region.
- State Union Bounds method: every state is derived from one Normal master and reuses its alpha channel.
- CropOffset storage: recorded in `COMPONENT_COORDINATES.md`.
- 100% check: passed.
- 400% check: passed.
- Checkerboard check: passed.
- Clean parent version: `V02` (main panel, four section panels, two equipment rows).
- Result: `PASS`
