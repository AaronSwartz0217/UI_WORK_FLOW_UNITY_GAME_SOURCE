# Component Coordinates

Source canvas: `1024x1536`. Format: `x,y,width,height`.

| Component | Target / Visible Bounds | CropOffset | Reassembly | Anchor |
|---|---|---|---|---|
| MainPanelBase | 34,72,951,1399 | 0,0 | 34,72 | top-left |
| MaterialSlot | 205,226,133,137 | 0,0 | see grid below | center |
| OutputPreviewPanel | 129,938,759,341 | 0,0 | 129,938 | center |
| SmeltButton (Union) | 314,1331,391,78 | 0,0 | 314,1331 | center |
| CloseButton (Union) | formal 52x50 | 0,0 | 875,114; display 64x62 | center |

MaterialSlot placements:

- X: `205, 365, 524, 684`
- Y: `226, 394, 561, 729`
- Cartesian product: 16 placements in row-major order.
