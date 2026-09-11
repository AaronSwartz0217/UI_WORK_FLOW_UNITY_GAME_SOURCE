# Proportion Loop 01

| Check | Source | Output | Result |
|---|---:|---:|---|
| Canvas | 1464×828 | 1464×828 | PASS |
| Aspect ratio | 1.7681 | 1.7681 | PASS |
| Horizontal scale | 1.0 | 1.0 | PASS |
| Vertical scale | 1.0 | 1.0 | PASS |
| Shared control size | approximately 304×54 in wireframe | 312×56 in approved draft | PASS — follows approved draft |
| Control center line | x≈732 | x=732 | PASS |

No non-uniform full-screen stretch was used. `CanvasScaler` uses `Scale With Screen Size`, reference resolution 1464×828, match value 0.5.

## CharacterSetup layout

| Check | Source / approved draft | Output | Result |
|---|---:|---:|---|
| Canvas | 1464×828 | 1464×828 | PASS |
| Main panel | approximately 1012×327 | 1012×328 | PASS |
| Name input | approximately 482×50 | 482×50 | PASS |
| Current equipment slot | approximately 222×214 | 222×214 | PASS |
| Equipment cards | approximately 184×163 | 184×164 | PASS |
| Enter-game button | approximately 368×72 | 368×72 | PASS |
| Card center spacing | approximately 206 px | 206 px | PASS |

All CharacterSetup components are placed at native pixel size. No independent X/Y stretch is used.
