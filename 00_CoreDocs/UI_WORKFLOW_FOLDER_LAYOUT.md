# UI 自动化工作流推荐目录

## 1. 推荐的工作流根目录

```text
UIWorkflow/
├─ 00_CoreDocs/
├─ 01_References/
├─ 02_InputQueue/
├─ 03_ProjectTemplate/
├─ 04_Projects/
├─ 05_Tools/
├─ 06_Status/
├─ 07_Archive/
└─ README.md
```

数字前缀用于固定读取顺序，并避免 Agent 随意猜测哪个目录优先。

## 2. 完整推荐结构

```text
UIWorkflow/
├─ 00_CoreDocs/
│  ├─ README_MASTER.md
│  ├─ UI_PRODUCTION_STATUS_AND_AGENT_HANDOFF.md
│  ├─ README_UI_PIPELINE_ADDENDUM.md
│  ├─ UI_WORKFLOW_FOLDER_LAYOUT.md
│  ├─ NAMING_STANDARD.md
│  ├─ QA_STANDARD.md
│  └─ WORKFLOW_DOCUMENT_INDEX.md
│
├─ 01_References/
│  ├─ Style/
│  │  ├─ StyleReference_01.jpg
│  │  └─ STYLE_REFERENCE_INDEX.md
│  ├─ SharedComponents/
│  │  ├─ CloseButtons/
│  │  ├─ Slots/
│  │  ├─ PanelBorders/
│  │  └─ Icons/
│  └─ ReferenceNotes/
│     └─ STYLE_RULES.md
│
├─ 02_InputQueue/
│  ├─ 01_RootPriority/
│  │  └─ EquipmentAdvancementUI/
│  │     ├─ Wireframe/
│  │     └─ REQUEST.md
│  ├─ 02_MainUI/
│  ├─ 03_Repair/
│  ├─ 04_Shop/
│  ├─ 05_Friends/
│  ├─ 06_Guild/
│  ├─ 07_Skills/
│  ├─ 08_Reflection/
│  ├─ 09_Login/
│  ├─ 10_Inventory/
│  └─ 11_Settings/
│
├─ 03_ProjectTemplate/
│  └─ ProjectId/
│     ├─ in/
│     ├─ into/
│     │  ├─ Candidates/
│     │  ├─ Rejected/
│     │  └─ ReassemblyPreview/
│     ├─ Components/
│     │  └─ out/
│     │     └─ ProjectId/
│     ├─ Templates/
│     ├─ FullUI/
│     ├─ QA/
│     │  ├─ FINAL_QA.md
│     │  ├─ ASSET_MANIFEST.md
│     │  ├─ COMPONENT_COORDINATES.md
│     │  ├─ BUTTON_TEXT_MATRIX.md
│     │  ├─ PROPORTION_LOOP_01.md
│     │  └─ CUTOUT_METHOD.md
│     ├─ project.json
│     └─ README.md
│
├─ 04_Projects/
│  ├─ CharacterAttributesUI/
│  ├─ EquipmentEnchantingUI/
│  ├─ TeamInvitationPopupUI/
│  ├─ SmeltingUI/
│  ├─ EmbryoCultivationUI/
│  ├─ EquipmentUI/
│  ├─ EquipmentCraftingUI/
│  └─ EquipmentAdvancementUI/
│
├─ 05_Tools/
│  ├─ Common/
│  │  ├─ validate_project.py
│  │  ├─ validate_alpha.py
│  │  ├─ validate_state_union.py
│  │  ├─ validate_dimensions.py
│  │  ├─ validate_naming.py
│  │  ├─ build_checkerboard.py
│  │  ├─ build_reassembly.py
│  │  └─ generate_manifest.py
│  ├─ ProjectScripts/
│  │  └─ ProjectId/
│  ├─ Schemas/
│  │  ├─ project.schema.json
│  │  ├─ manifest.schema.json
│  │  └─ qa.schema.json
│  └─ README.md
│
├─ 06_Status/
│  ├─ PROJECT_STATUS.json
│  ├─ PRODUCTION_QUEUE.md
│  ├─ COMPLETED_PROJECTS.md
│  └─ FAILED_OR_REVIEW_REQUIRED.md
│
├─ 07_Archive/
│  ├─ RejectedRevisions/
│  ├─ SupersededProjects/
│  └─ MigrationBackups/
│
└─ README.md
```

## 3. 项目内部固定结构

无论工作流根目录如何调整，每个 UI 项目内部都保持：

```text
ProjectId/
├─ in/
├─ into/
│  ├─ Candidates/
│  ├─ Rejected/
│  └─ ReassemblyPreview/
├─ Components/
│  └─ out/
│     └─ ProjectId/
├─ Templates/
├─ FullUI/
├─ QA/
├─ project.json
└─ README.md
```

正式组件唯一位置：

```text
04_Projects/ProjectId/Components/out/ProjectId/*.png
```

不要在正式输出目录中放：

- Markdown 文档；
- 回拼图；
- 棋盘格图；
- 候选图；
- 废稿；
- 源图；
- 脚本；
- JSON 配置；
- 旧版本 PNG。

`Components/out/ProjectId/` 应只包含可以直接导入项目的最终 PNG。

## 4. 推荐的 project.json

每个项目使用一个机器可读配置，减少 Agent 依赖聊天记忆：

```json
{
  "projectDisplayName": "装备进阶",
  "projectId": "EquipmentAdvancementUI",
  "componentPrefix": "EquipmentAdvancement",
  "status": "draft",
  "wireframe": "in/EquipmentAdvancementUI_Wireframe_WidthxHeight.jpeg",
  "styleReferences": [
    "in/EquipmentAdvancementUI_StyleReference_01_WidthxHeight.jpg"
  ],
  "canvas": {
    "width": 0,
    "height": 0,
    "scaleX": 1.0,
    "scaleY": 1.0
  },
  "formalOutput": "Components/out/EquipmentAdvancementUI",
  "requiresFullUIApproval": true,
  "requiresFourButtonStates": true,
  "requiresTrueAlpha": true,
  "requiresReassembly": true,
  "requiresFinalQA": true
}
```

状态建议固定为：

```text
queued
draft
pending_fullui_review
approved_for_split
splitting
qa
needs_revision
pending_final_review
complete
```

## 5. 推荐的全局状态文件

`06_Status/PROJECT_STATUS.json` 建议保存：

```json
{
  "activeProject": "EquipmentAdvancementUI",
  "projects": {
    "EquipmentCraftingUI": {
      "status": "complete",
      "finalPngCount": 42,
      "finalOutput": "04_Projects/EquipmentCraftingUI/Components/out/EquipmentCraftingUI",
      "finalQa": "04_Projects/EquipmentCraftingUI/QA/FINAL_QA.md"
    },
    "EquipmentAdvancementUI": {
      "status": "queued",
      "finalPngCount": 0
    }
  }
}
```

Agent 开始工作前读取该文件；完成或退回修订时更新，避免重复制作或跳过审核。

## 6. 工具拆分建议

通用逻辑放在 `05_Tools/Common/`，项目坐标和清单放在 `05_Tools/ProjectScripts/ProjectId/`。

### 通用脚本负责

- 目录结构校验；
- 英文命名校验；
- 文件名尺寸与真实 PNG 尺寸校验；
- Alpha 通道、透明角和内部安全区校验；
- 四态 `Union Bounds` 和画布一致性校验；
- `ScaleX == ScaleY` 校验；
- 棋盘格生成；
- 原位回拼；
- 正式资产清单生成；
- 检查 `out` 是否混入非正式文件。

### 项目脚本只负责

- 当前白膜坐标；
- 当前项目组件清单；
- 当前项目层级；
- 每个组件的 `Target Region`；
- 当前项目特有的轮廓或九宫格参数。

禁止为每个项目重复复制整套通用 QA 代码。

## 7. 输入队列建议

原始白膜统一导入工作流相对目录：

```text
../02_InputQueue/
```

工作流中的 `02_InputQueue/` 采用以下方式：

### 方案 A：复制输入（正式工作流采用）

将当前待处理白膜复制到对应队列项目中。优点是工作流完全自包含；缺点是容易产生重复文件。

### 方案 B：只记录源路径（仅导入前临时使用）

每个队列项目只建立 `REQUEST.md` 或 `request.json`，记录原始白膜绝对路径；项目正式建立时再复制到 `in/`。

示例：

```json
{
  "sourceWireframe": "02_InputQueue/01_RootPriority/EquipmentAdvancementUI/Wireframe/EquipmentAdvancementUI_Wireframe.jpeg",
  "styleReferenceFolder": "01_References/Style",
  "priority": 1
}
```

## 8. 文档权威顺序

Agent 遇到冲突时按照以下优先级执行：

```text
1. 00_CoreDocs/README_MASTER.md
2. 用户当前明确指令
3. UI_PRODUCTION_STATUS_AND_AGENT_HANDOFF.md
4. README_UI_PIPELINE_ADDENDUM.md
5. 当前项目 README 和 project.json
6. 相似项目实例文档
7. 项目脚本中的默认值
```

项目实例不能覆盖主规范。

## 9. 最小可用版本

如果暂时不想一次搭建全部目录，可以先建立：

```text
UIWorkflow/
├─ CoreDocs/
│  ├─ README_MASTER.md
│  ├─ UI_PRODUCTION_STATUS_AND_AGENT_HANDOFF.md
│  └─ WORKFLOW_DOCUMENT_INDEX.md
├─ References/
│  └─ Style/
├─ InputQueue/
├─ ProjectTemplate/
├─ Projects/
├─ Tools/
└─ Status/
```

其中最关键的是：主规范、元素参考、项目模板、项目目录、通用验证工具和全局状态文件。
