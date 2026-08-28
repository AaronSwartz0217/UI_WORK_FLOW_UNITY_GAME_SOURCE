# 装备附魔 / EquipmentEnchantingUI

## 结果

- 状态：`complete_automated_user_authorized`
- 正式完整 UI：`FullUI/EquipmentEnchantingUI_FullUI_Review02_1024x1536.png`
- 正式组件：`Components/out/EquipmentEnchantingUI/`
- 正式 PNG 数量：23
- 拆分版本：`SplitV01`
- 项目验证：PASS

## 输入与风格

- 线框：`in/EquipmentEnchantingUI_Wireframe.jpeg`
- 主风格：`in/StylePrimary_Cook/`
- 次风格：`in/StyleSecondary_EquipmentIdentification/`
- 稳定组件示范：`in/SharedComponents_StyleBoard.png`

普通文字和动态数值均未写入图片；仅保留问号与关闭叉号等功能符号。问号按钮复用装备鉴定标准四态，关闭按钮复用烹饪标准四态。

## 层级

```text
MainPanelBase
├─ HelpButton / CloseButton
├─ EquipmentDisplayPanel
│  └─ EquipmentSlot
├─ AttributeListPanel
│  └─ AttributeRow × 5
│     └─ AttributeToggleSlot
├─ MaterialPanel
│  └─ MaterialCard × 2
│     └─ MaterialSlot
└─ ControlPanel
   ├─ EnchantButton
   └─ ModeCheckbox
```

父级底板均已去除可独立复用的子级图形。正式目录只含最终 PNG。
