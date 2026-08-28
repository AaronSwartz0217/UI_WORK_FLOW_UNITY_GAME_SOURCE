# 熔炼 / SmeltingUI

当前状态：无文字完整界面 Review02 已生成，等待确认后拆分组件。

## 输入

- 白膜：`in/SmeltingUI_Wireframe.jpeg`（800x969）
- 主风格：`in/StylePrimary_Cook/`
- 次风格：`in/StyleSecondary_EquipmentIdentification/`
- 风格板：`in/SharedComponents_StyleBoard.png`
- 主风格冲突时以 Cook 为准；参考图保持不变。

## 完整界面

- Review01：结构正确，但主面板比例 `0.617`，偏窄，已淘汰。
- Review02：`FullUI/SmeltingUI_FullUI_Review02_1024x1536.png`
- Review02 主面板可见范围约 `x=33, y=71, width=952, height=1401`。
- 白膜主面板比例 `0.694175`，Review02 比例 `0.679515`，偏差约 `2.11%`。
- `ScaleX == ScaleY`；16 个材料槽保持正方形，没有单轴拉伸。

## 结构

```text
MainPanelBase
|- CloseButton (functional X)
|- MaterialSlot x16 (4 columns x 4 rows)
|- OutputPreviewPanel
`- SmeltButton (blank four-state family after split)
```

## 文字策略

标题、说明、动态数字和按钮文字均移除；仅保留功能关闭 `X`。槽位和产出预览区保持空白。

## 正式目录

`Components/out/SmeltingUI/` 当前为空。完整界面确认前不进入拆分。
