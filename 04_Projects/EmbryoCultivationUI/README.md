# 胚体养成 / EmbryoCultivationUI

- 状态：`complete_automated_user_authorized`
- 正式完整 UI：`FullUI/EmbryoCultivationUI_FullUI_Review03_1024x1536.png`
- 正式组件：`Components/out/EmbryoCultivationUI/`
- 正式 PNG：19
- 验证：PASS

主风格为 Cook。普通标题、页签文字、成功率、百分比、物品名和按钮文字全部移除，只保留功能性 `X`。两个页签复用同一个四态按钮组件，两个材料区复用同一套卡片与槽位。

```text
MainPanelBase
├─ HeaderPanel → CloseButton
├─ TabButton × 2
├─ ContentPanel
│  ├─ EmbryoSlot
│  └─ MaterialCard × 2 → MaterialSlot
└─ ActionPanel → CultivateButton
```
