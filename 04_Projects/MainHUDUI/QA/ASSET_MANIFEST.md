# Asset Manifest

| ID | Position | Component | Parent | Selection | States | Text policy | Current result |
|---|---|---|---|---|---|---|---|
| HUD01 | Root | Main HUD layout | Root | Include | Default | TMP/dynamic layers separate | Pass; transparent gameplay viewport |
| BTN01 | TopLeft | Expand arrow button | Header | Include | Normal/Hover/Pressed/Disabled | Retain `>` | Pass |
| BTN02 | TopCenter | Team invite button | Header | Include | Normal/Hover/Pressed/Disabled | TMP | Pass |
| BTN03 | TopRight | Mode dropdown button | Header | Include | Normal/Hover/Pressed/Disabled | TMP; retain arrow | Pass |
| BTN04 | TopRight | GM tools button | Header | Include | Normal/Hover/Pressed/Disabled | TMP | Pass |
| BTN05 | TopRight | Menu button | Header | Include | Normal/Hover/Pressed/Disabled | TMP | Pass |
| BTN06 | BottomRight | Return city button | MinimapPanel | Include | Normal/Hover/Pressed/Disabled | TMP | Pass |
| BTN07 | BottomRight | Recharge button | MinimapPanel | Include | Normal/Hover/Pressed/Disabled | TMP | Pass |
| SLOT01 | BottomCenter | Hotbar slot family | BottomHUD | Include | Normal/Hover/Pressed/Disabled/Selected | TMP shortcut labels | Pass |
| BTN09 | BottomCenter | Mutation button | BottomHUD | Include | Normal/Hover/Pressed/Disabled | TMP | Pass |
| BTN08 | BottomCenter | Unlabelled white rectangle | BottomHUD | Pending | Unknown | Unknown | Excluded until role confirmed |
| POPUP01 | Related page | Functional-button popup | Separate screen | Exclude | N/A | N/A | Future project/pass |
| RANKING01 | Related page | Ranking panel | Separate screen | Exclude | N/A | N/A | Future project/pass |

## Formal output groups

| Group | PNG count | Result |
|---|---:|---|
| 8 named button families | 32 | Pass |
| Hotbar slot family | 5 | Pass |
| Static panel/bar/minimap/currency components | 20 | Pass |
| Total | 57 | Pass |

Glass controls are deliberately semi-transparent for shader sampling. Their state canvases and Alpha silhouettes are identical within each family. The unconfirmed center marker is stored only under `into/Candidates`.
