# Cooking Mode UI

## Button text contract

Buttons carrying an action label in the layout reference keep that label inside every exported state. This project preserves `菜名`, `最大`, `开始`, `×`, `−`, and `+`.

ProjectDisplayName: 烹饪模式  
ProjectId: `CookingModeUI`  
ComponentPrefix: `CookingMode`

## Migrated workflow location

- Project root: `04_Projects/CookingModeUI/`
- Formal output: `Components/out/CookingModeUI/`
- QA: `QA/`
- The original desktop project remains unchanged as a migration source.
- Current workflow validation: `Needs Revision`; coordinate and proportion-loop documents are missing.

## Input roles

- `in/CookingMode_LayoutReference_1698x1133.jpg`: strict layout reference.
- `in/CookingMode_StyleReference_1620x952.jpg`: strict visual-style reference.
- Layout reference controls panel count, placement, proportions, hierarchy and nesting.
- Style reference controls metal, color, bevel, wear, lighting and decorative language.

## Panel selection

`PanelSelectionMode: ConfirmSelection`

User confirmation: all detected resources included.

| ID | Position | Component | Selection |
|---|---|---|---|
| P01 | Root | RootWindow | Include |
| P02 | LeftSidebar | LeftSidebarPanel | Include |
| P03 | CenterRight | MainContentPanel | Include |
| P04 | Center | RecipePreviewPanel | Include |
| C01 | Nested / TopLeft | RecipeSelectionButton | Include |
| C02 | TopRight | CloseButton | Include |
| C03 | BottomCenter | QuantityMinusButton | Include |
| C04 | BottomCenter | QuantityPlusButton | Include |
| C05 | BottomCenter | MaximumButton | Include |
| C06 | BottomRight | StartButton | Include |
| C07 | BottomCenter | ProgressTrack | Include |
| C08 | BottomCenter | ProgressFill | Include |
| S01 | Nested / CenterLeft | MaterialSlot | Include |

## Text policy

- Titles, descriptions, quantity values, level, experience and progress copy are engine text.
- `×`, `−`, and `+` remain baked because they identify their button actions.
- Recipe, maximum and start button labels remain separate engine text.

## Output policy

- `into` contains the complete visual mockup.
- `Components/out/CookingModeUI` contains one component per PNG.
- Components use true Alpha and are cropped to the high-confidence outer visible border.
- Filename dimensions equal actual canvas dimensions.
- No prototype blue, screenshot background, dynamic numbers or ordinary text appears in component assets.

## Button states

All six button groups include `Normal`, `Hover`, `Pressed`, and `Disabled`.

- Every state group uses an identical canvas and Alpha mask.
- Hover is brighter and slightly more saturated.
- Pressed is darker with increased inset contrast.
- Disabled is desaturated, darker, and lower contrast.
- `QA/BUTTON_STATE_COMPARISON.png` provides the visual comparison.
- `QA/BUTTON_STATE_MATRIX.md` records validation.
