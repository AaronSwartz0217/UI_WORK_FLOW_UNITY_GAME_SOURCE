# Component Manifest

| ID | File | Role | State | Text |
|---|---|---|---|---|
| P01 | `CookingMode_RootWindow_Empty_1347x802.png` | Root window and header structure | Empty | Separate |
| P02 | `CookingMode_LeftSidebarPanel_Empty_423x1311.png` | Left recipe-list container | Empty | Separate |
| P03 | `CookingMode_MainContentPanel_Empty_1038x963.png` | Main content container | Empty | Separate |
| P04 | `CookingMode_RecipePreviewPanel_Empty_1481x595.png` | Recipe preview container | Empty | Separate |
| S01 | `CookingMode_MaterialSlot_Empty_792x795.png` | Empty material slot | Empty | Quantity separate |
| C01 | `CookingMode_RecipeSelectionButton_{State}_1609x359.png` | Recipe selection | Normal/Hover/Pressed/Disabled | Label separate |
| C02 | `CookingMode_CloseButton_{State}_715x723.png` | Close action | Normal/Hover/Pressed/Disabled | `×` retained |
| C03 | `CookingMode_QuantityMinusButton_{State}_677x693.png` | Decrease quantity | Normal/Hover/Pressed/Disabled | `−` retained |
| C04 | `CookingMode_QuantityPlusButton_{State}_712x740.png` | Increase quantity | Normal/Hover/Pressed/Disabled | `+` retained |
| C05 | `CookingMode_MaximumButton_{State}_997x316.png` | Set maximum | Normal/Hover/Pressed/Disabled | Label separate |
| C06 | `CookingMode_StartButton_{State}_1513x349.png` | Start cooking | Normal/Hover/Pressed/Disabled | Label separate |
| C07 | `CookingMode_ProgressTrack_Empty_1666x111.png` | Progress background channel | Empty | None |
| C08 | `CookingMode_ProgressFill_Default_1534x139.png` | Progress fill | Default | None |

All component canvases are cropped to the visible component boundary. Original placement belongs to the implementation/reassembly configuration, not the component PNG.

`{State}` expands to `Normal`, `Hover`, `Pressed`, and `Disabled`; all four files exist for every button group.
