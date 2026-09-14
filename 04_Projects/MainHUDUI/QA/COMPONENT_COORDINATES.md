# Component Coordinates

Coordinate format: `x, y, width, height` on the 1559x880 whiteframe canvas.

| ID | Component | Target Region | Anchor | Result |
|---|---|---|---|---|
| BTN01 | Expand arrow button | `15, 15, 79, 39` | TopLeft | Matched |
| BAR01 | Party health strip | `15, 72, 75, 12` | TopLeft | Matched |
| BAR02 | Party mana strip | `15, 86, 75, 4` | TopLeft | Matched |
| BTN02 | Team invite button | `909, 31, 69, 21` | TopCenter | Matched |
| BAR03 | Player health track | `576, 53, 406, 20` | TopCenter | Matched |
| BAR03_FILL | Player health fill | `577, 54, 162, 17` | TopCenter | Matched |
| BTN03 | Mode dropdown button | `1279, 15, 84, 40` | TopRight | Matched |
| BTN04 | GM tools button | `1372, 15, 80, 39` | TopRight | Matched |
| BTN05 | Menu button | `1462, 15, 80, 39` | TopRight | Matched |
| PANEL01 | Lower HUD plate | `15, 594, 1253, 282` | BottomLeft | Matched; translucent |
| BAR04 | Loading track | `576, 696, 405, 18` | BottomCenter | Matched |
| BAR04_FILL | Loading fill | `577, 697, 119, 16` | BottomCenter | Matched |
| BAR05 | Mutation track | `496, 722, 566, 17` | BottomCenter | Matched |
| BAR05_FILL | Mutation fill | `497, 723, 486, 15` | BottomCenter | Matched |
| BAR06 | Health/mana track | `455, 782, 646, 21` | BottomCenter | Matched |
| BTN08 | Pending center marker | `740, 778, 78, 30` | BottomCenter | Pending role; geometry retained |
| SLOT01 | Hotbar slots 1-3 | `315/372/429, 809, 56, 56` | BottomCenter | Matched |
| SLOT01 | Hotbar slots Q-C | `496/553/609/666/722/779/835/891/948/1004, 809, 56, 56` | BottomCenter | Matched |
| BTN09 | Mutation button | `1073, 809, 56, 56` | BottomCenter | Matched |
| BAR07 | Minimap vertical meter | `1268, 586, 23, 242` | BottomRight | Matched |
| PANEL02 | Minimap panel | `1303, 586, 239, 243` | BottomRight | Matched |
| BTN06 | Return city button | `1306, 793, 62, 29` | BottomRight | Matched |
| BTN07 | Recharge button | `1487, 838, 54, 25` | BottomRight | Matched |

The generated style image is not used as coordinate authority. Every listed region is reconstructed from the whiteframe and uses the same 1559x880 reference canvas.
