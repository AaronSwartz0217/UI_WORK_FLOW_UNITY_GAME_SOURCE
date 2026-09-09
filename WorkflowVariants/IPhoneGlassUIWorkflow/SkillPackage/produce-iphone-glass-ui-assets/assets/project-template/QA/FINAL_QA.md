# Final QA

- [ ] 完整 UI 已由用户确认。
- [ ] 白膜结构和实际面板比例一致。
- [ ] `ScaleX == ScaleY`，无压扁或拉长。
- [ ] 风格与 `01_References/Style/` 一致。
- [ ] 父板和各级子板职责正确。
- [ ] 普通文字及动态数字已移除。
- [ ] 功能符号正确保留。
- [ ] 组件外部为真实透明 Alpha。
- [ ] 按钮和槽位内部安全区 Alpha 为 255。
- [ ] 单组件使用自身 `Visible Bounds`。
- [ ] 状态组使用统一 `Union Bounds`。
- [ ] 文件名尺寸与真实 PNG 尺寸一致。
- [ ] 100% 整体检查通过。
- [ ] 400% 边缘检查通过。
- [ ] 棋盘格检查通过。
- [ ] 原位回拼通过。
- [ ] `out` 中没有文档、废稿、旧版和临时文件。
- [ ] 用户完成最终审核。
- [ ] Unity 项目存在 `Assets/SHADER/玻璃预设/毛玻璃.json`。
- [ ] 每次烘焙前已读取唯一指定预设，未静默使用默认值。
- [ ] 每个玻璃组件均有已确认的白模区域颜色记录。
- [ ] 毛玻璃 Tint 来自 `WireframeSourceColor`，未被风格参考配色覆盖。
- [ ] `WireframeSourceColor`、`GeneratedColor`、`HueDifference`、`SaturationAdjustment`、`BrightnessAdjustment`、`ColorDecision` 均已记录。
- [ ] 玻璃半透明内部属于明确的 `ComponentMaterial: Glass`，外部仍为真实 Alpha 0。
- [ ] 运行时材质使用 `UI/URP Frosted Glass Diffraction`。
- [ ] 模糊、折射和色散由运行时 Shader 实现，未烘焙截图背景。

结论：PENDING
