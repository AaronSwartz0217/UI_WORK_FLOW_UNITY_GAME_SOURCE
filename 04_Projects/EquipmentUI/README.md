# 装备 / EquipmentUI

- 状态：`complete_automated_user_authorized`
- 完整 UI：`FullUI/EquipmentUI_FullUI_Review03_1024x1536.png`
- 正式组件：`Components/out/EquipmentUI/`
- 正式 PNG：12
- 运行时槽位：19（1 个 WeaponSlot + EquipmentSlot 复用 18 次）
- 验证：PASS

普通页签文字、装备名称、编号和物品图标全部移除，仅保留功能性 `X`。正式槽位经过几何标准化：常规槽 143×143，武器槽 220×220。

```text
MainPanelBase
├─ TabButton × 2
├─ CloseButton
└─ EquipmentContentPanel
   ├─ WeaponSlot × 1
   └─ EquipmentSlot × 18
```
