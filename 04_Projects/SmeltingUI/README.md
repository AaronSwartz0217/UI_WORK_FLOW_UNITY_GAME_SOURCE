# 熔炼 / SmeltingUI

当前状态：Review02 已按用户“全自动”授权完成拆分，11 个正式 PNG 已通过内部 QA。

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

`Components/out/SmeltingUI/`：11 PNG。

- `MainPanelBase`：1
- `MaterialSlot`：1 个复用件，回装 16 次
- `OutputPreviewPanel`：1
- `SmeltButton`：Normal/Hover/Pressed/Disabled，共 4
- `CloseButton`：直接复用 Cook 标准四态，共 4

SplitV01 使用人工核对边界、组件专用倒角 Alpha、低 Alpha 清理和同源纹理重建。父面板不包含槽位、产出面板或按钮残影。

## QA

- 真 Alpha：PASS
- 按钮安全区 Alpha 255：PASS
- 四态画布/轮廓一致：PASS
- 100% 回装、400% 边缘、棋盘格：PASS
- 项目验证器：PASS
