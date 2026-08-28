# UI 工作流文档索引

## A. 必须加载的核心文档

### A1. 主规范（最高优先级）

```text
./README_MASTER.md
```

用途：完整制作规范，包括输入职责、生成顺序、真实 Alpha、紧边裁剪、`Visible Bounds`、`Union Bounds`、`CropOffset`、父子板拆分、按钮四态、英文命名、QA 和交付条件。

工作流必须首先读取这份文件。其他文档与其冲突时，以这份为准。

### A2. 当前进度和 Agent 交接

```text
./UI_PRODUCTION_STATUS_AND_AGENT_HANDOFF.md
```

用途：已完成项目、待完成队列、目录结构、正式输出位置、项目命名、组件命名、元素参考要求和逐项目审核流程。

### A3. 通用流程补充

```text
./README_UI_PIPELINE_ADDENDUM.md
```

用途：补充比例回环、禁止单轴缩放、父子板结构、按钮内部不透明和项目正式输出目录等本轮迭代规则。

### A4. 推荐工作流目录设计

```text
./UI_WORKFLOW_FOLDER_LAYOUT.md
```

用途：搭建可长期运行的工作流根目录、项目模板、输入队列、工具层、状态层和归档层。

## B. 工作区总览文档

```text
../README.md
./WORKFLOW_DOCUMENT_INDEX.md
```

用途：早期工作区总览和目录说明。可作为背景资料，但不得覆盖 A1 主规范和 A2 最新交接文档。

## C. 强制输入位置

### C0. 桌面白膜参考库

```text
../01_References/LayoutWireframes/DesktopUIWireframes/
../01_References/LayoutWireframes/WIREFRAME_REFERENCE_INDEX.md
```

用途：保存从桌面迁入的 40 张 UI 结构白膜。正式生产前每次只选择一张，复制到 `02_InputQueue/<category>/<ProjectId>/Wireframe/`。该库只决定结构，不决定视觉风格。

### C1. 白膜及待制作 UI

```text
../02_InputQueue/
```

用途：当前 UI 的结构、比例、组件数量、坐标和层级依据。

### C2. 元素风格参考

```text
../01_References/Style/
```

当前主要文件：

```text
../01_References/Style/Standards/Primary_Cook/                  # 主标准
../01_References/Style/Standards/Secondary_EquipmentIdentification/ # 次级补充
../01_References/Style/StyleReference_01.jpg
```

冲突规则：Cook 优先；装备鉴定只补充 Cook 未覆盖的组件类型；白膜始终负责结构和坐标。

用途：黑钢材质、琥珀点缀、磨损、倒角、边框和按钮质感。每个项目必须查看并把实际使用的风格图复制到项目 `in/`。

## D. 每个项目必须维护的文档

项目根路径统一为：

```text
../04_Projects/ProjectId/
```

每个项目至少维护：

```text
ProjectId/README.md
ProjectId/QA/FINAL_QA.md
ProjectId/QA/COMPONENT_COORDINATES.md
ProjectId/QA/BUTTON_TEXT_MATRIX.md
ProjectId/QA/PROPORTION_LOOP_01.md
ProjectId/QA/CUTOUT_METHOD.md              # 使用复杂抠图时
ProjectId/ASSET_MANIFEST.md                # 或放在 QA 中
```

用途：

- `README.md`：项目身份、输入、比例、结构和输出位置。
- `FINAL_QA.md`：最终通过条件和结论。
- `COMPONENT_COORDINATES.md`：原位坐标、尺寸和 `CropOffset`。
- `BUTTON_TEXT_MATRIX.md`：按钮文字/符号分类和四态完整性。
- `PROPORTION_LOOP_01.md`：白膜比例、正式画布比例和形变检查。
- `CUTOUT_METHOD.md`：`Target Region`、Alpha 方法、`Visible Bounds` 和 `Union Bounds`。
- `ASSET_MANIFEST.md`：最终资产清单。

## E. 已完成项目实例文档

### E1. 属性界面

```text
...\CharacterAttributesUI\README.md
...\CharacterAttributesUI\INTRODUCTION.md
...\CharacterAttributesUI\ASSET_MANIFEST.md
...\CharacterAttributesUI\QA\FINAL_QA.md
...\CharacterAttributesUI\QA\BUTTON_TEXT_MATRIX.md
...\CharacterAttributesUI\QA\NATIVE_REVISION_METRICS.md
...\CharacterAttributesUI\QA\PROPORTION_LOOP_01.md
```

适合参考：原生比例修订、拒绝压缩版本、进度条与标签状态。

### E2. 附魔界面

```text
...\EquipmentEnchantingUI\README.md
...\EquipmentEnchantingUI\INTRODUCTION.md
...\EquipmentEnchantingUI\ASSET_MANIFEST.md
...\EquipmentEnchantingUI\QA\FINAL_QA.md
...\EquipmentEnchantingUI\QA\PANEL_SELECTION.md
...\EquipmentEnchantingUI\QA\BUTTON_TEXT_MATRIX.md
```

适合参考：父板、大子板、小子板、左右组件同目录和按钮四态。

### E3. 组队邀请弹窗

```text
...\TeamInvitationPopupUI\README.md
...\TeamInvitationPopupUI\INTRODUCTION.md
...\TeamInvitationPopupUI\ASSET_MANIFEST.md
...\TeamInvitationPopupUI\QA\FINAL_QA.md
...\TeamInvitationPopupUI\QA\BUTTON_TEXT_MATRIX.md
```

适合参考：弹窗、标题板、列表板、列表行和接受/拒绝按钮。

### E4. 熔炼界面

```text
...\SmeltingUI\README.md
...\SmeltingUI\INTRODUCTION.md
...\SmeltingUI\ASSET_MANIFEST.md
...\SmeltingUI\QA\FINAL_QA.md
...\SmeltingUI\QA\SLOT_COORDINATES.md
...\SmeltingUI\QA\BUTTON_TEXT_MATRIX.md
...\SmeltingUI\QA\PROPORTION_LOOP_01.md
```

适合参考：可复用槽位、输出板、竖屏原生比例和回拼坐标。

### E5. 胚体养成

```text
...\EmbryoCultivationUI\README.md
...\EmbryoCultivationUI\QA\FINAL_QA.md
...\EmbryoCultivationUI\QA\COMPONENT_COORDINATES.md
...\EmbryoCultivationUI\QA\BUTTON_TEXT_MATRIX.md
...\EmbryoCultivationUI\QA\PROPORTION_LOOP_01.md
```

适合参考：按钮内部不透明、展示板与中心槽分层。

### E6. 装备界面

```text
...\EquipmentUI\README.md
...\EquipmentUI\QA\FINAL_QA.md
...\EquipmentUI\QA\COMPONENT_COORDINATES.md
...\EquipmentUI\QA\PROPORTION_LOOP_01.md
```

适合参考：大量重复装备槽复用、竖屏布局和回拼坐标。

### E7. 装备打造

```text
...\EquipmentCraftingUI\README.md
...\EquipmentCraftingUI\QA\FINAL_QA.md
...\EquipmentCraftingUI\QA\COMPONENT_COORDINATES.md
...\EquipmentCraftingUI\QA\BUTTON_TEXT_MATRIX.md
...\EquipmentCraftingUI\QA\PROPORTION_LOOP_01.md
...\EquipmentCraftingUI\QA\CUTOUT_METHOD.md
```

适合参考：横屏比例、三级父子板、真实 Alpha 修订、滑轨/滑块及复杂控件。

以上路径中的 `...` 代表：

```text
../04_Projects
```

## F. 当前处理脚本

脚本目录：

```text
../05_Tools/ProjectScripts/
```

主要脚本：

```text
build_character_attributes_native.py
build_enchanting_panel_hierarchy.py
build_team_popup.py
build_smelting_native.py
build_embryo_cultivation_native.py
build_equipment_ui.py
build_equipment_crafting_ui.py
normalize_equipment_fullui.py
normalize_equipment_crafting_fullui.py
```

这些是项目实例脚本，不应直接硬套到新项目。可复用的逻辑包括：

- 画布尺寸校验；
- 禁止非等比缩放；
- 四态统一画布；
- Alpha 棋盘格；
- 原位回拼；
- 文件数量、尺寸和内部 Alpha 检查。

坐标、裁剪框、轮廓和组件清单必须根据新白膜重新确定。

## G. 推荐工作流加载顺序

```text
1. 主 README
2. UI_PRODUCTION_STATUS_AND_AGENT_HANDOFF.md
3. README_UI_PIPELINE_ADDENDUM.md
4. 当前白膜
5. 元素参考文件夹全部风格图
6. 当前项目 README（若已存在）
7. 当前项目 QA 和坐标文档（若已存在）
8. 选择一个结构相近的已完成项目作为实例
```

不要一次加载所有项目文档；只加载与当前 UI 结构最接近的实例，避免旧项目细节污染当前项目。
