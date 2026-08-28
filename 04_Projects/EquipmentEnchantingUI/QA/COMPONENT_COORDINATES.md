# Component Coordinates

坐标格式：`x, y, width, height`，以 1024×1536 完整 UI 左上角为原点。

| Component | Target Region / Reassembly Position | Reuse |
|---|---|---|
| MainPanelBase | `27, 100, 969, 1377` | 1 |
| HelpButton | `823, 126, 58, 62`（原件 52×56，预览等比缩放） | 1 |
| CloseButton | `892, 128, 58, 56`（原件 52×50，预览等比缩放） | 1 |
| EquipmentDisplayPanel | `58, 203, 907, 256` | 1 |
| EquipmentSlot | `412, 241, 189, 188` | 1 |
| AttributeListPanel | `58, 473, 907, 512` | 1 |
| AttributeRow | `131, 501, 755, 84`; Y=`595, 688, 782, 876` | 5 |
| AttributeToggleSlot | `790, 508, 74, 74`; Y=`602, 696, 790, 884` | 5 |
| MaterialPanel | `58, 998, 907, 221` | 1 |
| MaterialCard | `99, 1033, 402, 154`; `522, 1033, 402, 154` | 2 |
| MaterialSlot | `116, 1053, 116, 116`; `540, 1053, 116, 116` | 2 |
| ControlPanel | `58, 1233, 907, 219` | 1 |
| EnchantButton | `331, 1266, 359, 87` | 1 |
| ModeCheckbox | `463, 1369, 55, 56` | 1 |

所有父级面板的导出图均为空父板；上述子件由 Unity 按坐标单独挂载。
