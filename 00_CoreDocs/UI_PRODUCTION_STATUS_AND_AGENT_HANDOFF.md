# UI 制作状态与 Agent 交接说明

> 用途：告诉后续 Agent 当前已经完成哪些 UI、接下来按什么顺序制作，以及正式组件必须如何命名和导出。
>
> 最高规范：`./README_MASTER.md`。本文件只记录项目状态、目录约定和执行顺序，不得降低主 README 的抠图、透明、拆分、状态、命名和 QA 要求。

## 1. 已完成项目

以下项目已经生成完整 UI、正式组件、回拼预览和最终 QA：

| 中文 UI | ProjectId | ComponentPrefix | 正式 PNG 数量 | 项目目录 |
|---|---|---|---:|---|
| 属性界面 | `CharacterAttributesUI` | `CharacterAttributes` | 19 | `../04_Projects/CharacterAttributesUI/` |
| 附魔界面 | `EquipmentEnchantingUI` | `EquipmentEnchanting` | 22 | `../04_Projects/EquipmentEnchantingUI/` |
| 组队邀请弹窗 | `TeamInvitationPopupUI` | `TeamInvitationPopup` | 16 | `../04_Projects/TeamInvitationPopupUI/` |
| 熔炼界面 | `SmeltingUI` | `Smelting` | 12 | `../04_Projects/SmeltingUI/` |
| 胚体养成 | `EmbryoCultivationUI` | `EmbryoCultivation` | 22 | `../04_Projects/EmbryoCultivationUI/` |
| 装备界面 | `EquipmentUI` | `Equipment` | 21 | `../04_Projects/EquipmentUI/` |
| 装备打造 | `EquipmentCraftingUI` | `EquipmentCrafting` | 26 | `../04_Projects/EquipmentCraftingUI/`（已迁移，Needs Revision） |

历史 PASS 项目登记合计：138 个正式 PNG。装备打造已迁移 26 个 PNG，但因缺少坐标与比例 QA 文档，当前状态为 `Needs Revision`，不计入 PASS 合计。

已迁移的烹饪模式项目：`../04_Projects/CookingModeUI/`，31 个正式 PNG；因缺少坐标与比例 QA 文档，当前状态为 `Needs Revision`。

注意：若复查已完成项目时发现不符合最新主 README，必须把该项目状态改为 `Needs Revision`，修复并重新通过 QA 后才能继续标记为完成。不得因为目录中已有文件就自动视为合格。

## 2. 尚未完成及处理顺序

### 2.1 第一优先级：根目录白膜

根目录目前只剩：

1. `../02_InputQueue/01_RootPriority/EquipmentAdvancementUI/Wireframe/EquipmentAdvancementUI_Wireframe.jpeg`

建议标识：

```text
ProjectDisplayName: 装备进阶
ProjectId: EquipmentAdvancementUI
ComponentPrefix: EquipmentAdvancement
```

完成并由用户逐项审核后，再进入子文件夹 UI。

### 2.2 第二优先级：子文件夹 UI

每次只制作一个完整 UI，先交完整效果图审核；用户确认后才能拆组件。推荐按以下顺序继续：

1. `主界面/`
   - `主界面.jpeg`
   - `功能按钮弹窗.jpeg`
   - `排行榜.jpeg`
2. `修复/`
   - `批量修复.jpeg`
   - `装备修复.jpeg`
3. `商城/`
   - `充值.jpeg`
   - `商品详情.jpeg`
   - `商城.jpeg`
4. `好友系统/`
   - `好友列表.jpeg`
   - `好友申请.jpeg`
   - `添加好友.jpeg`
5. `工会/`
   - `创建工会.jpeg`
   - `工会信息.jpeg`
   - `工会邀请.jpeg`
   - `成员列表.jpeg`
   - `申请列表.jpeg`
   - `退会弹窗.jpeg`
   - `邀请入会弹窗.jpeg`
6. `技能/`
   - `技能介绍.jpeg`
   - `技能背包.jpeg`
7. `映照/`
   - `映照.jpeg`
   - `补签弹窗.jpeg`
   - `领取记录.jpeg`
8. `登录/`
   - `创建角色.jpeg`
   - `加载.jpeg`
   - `登录.jpeg`
9. `背包/`
   - `使用弹窗.jpeg`
   - `物品详情弹窗.jpeg`
   - `背包.jpeg`
10. `设置/`
    - `按键设置.jpeg`
    - `视频设置.jpeg`
    - `音频设置.jpeg`

同一文件夹中的多个白膜仍然分别建立独立 `ProjectId` 项目，不要把多个完整界面混入同一个组件输出目录，除非用户明确要求它们属于同一个项目。

## 3. 每个项目必须使用的目录结构

```text
ProjectId/
├─ in/
│  ├─ ProjectId_Wireframe_WidthxHeight.ext
│  └─ ProjectId_StyleReference_01_WidthxHeight.ext
├─ into/
│  ├─ Candidates/
│  ├─ Rejected/
│  └─ ReassemblyPreview/
├─ Components/
│  └─ out/
│     └─ ProjectId/
│        └─ 最终导出的组件 PNG
├─ Templates/
├─ FullUI/
├─ QA/
└─ README.md
```

强制要求：

- 最终组件唯一导出位置为：`ProjectId/Components/out/ProjectId/`。
- 同一项目的左侧、右侧、上层、下层组件全部放在同一个 `Components/out/ProjectId/` 文件夹。
- 不得建立 `Left/`、`Right/`、`Buttons/` 等二次正式输出目录。
- `FullUI` 只放完整效果图；`Templates` 只放模板；`QA` 只放检查文件；`into` 只放候选、废稿和回拼预览。
- 未通过最终 QA、缺状态、未真透明、未紧裁或仍含文字的资源禁止进入 `out`。
- `out` 中不得保留旧版、重复版、候选版、临时文件或回拼图。

## 3.1 强制风格参考输入

### 当前标准参考优先级

所有后续 UI 必须执行以下优先级：

1. `../01_References/Style/Standards/Primary_Cook/`：主风格标准，决定整体材质、配色、边框、倒角、磨损、按钮状态、卡片和滑轨语言。
2. `../01_References/Style/Standards/Secondary_EquipmentIdentification/`：次级补充标准，只补充帮助按钮、装备/材料槽、竖版模板和紧凑操作按钮等 Cook 未完整覆盖的类型。
3. `../01_References/Style/StyleReference_01.jpg`：旧版氛围参考，不得覆盖前两项。

发生冲突时始终以 Cook 为准。当前白膜仍然是结构、比例、数量、坐标和层级的唯一依据。装备鉴定参考中的 `鉴定` 属于示例业务文字，不得复制到无关 UI。

参考图原文件必须保持不变。后续新生成的完整 UI 初稿即执行去文字：删除普通文字、本地化文字和动态数字，补全文字下方的实心表面；保留 `X`、`?`、`+`、`-` 和箭头等功能识别符号。详细规则见 `../01_References/ReferenceNotes/FUTURE_UI_TEXT_POLICY.md`。

每个后续 Agent 制作任何 UI 时，都必须读取并实际参考以下文件夹中的风格图：

```text
../01_References/Style/
```

当前主要风格参考图：

```text
../01_References/Style/StyleReference_01.jpg
```

输入职责必须明确区分：

| 输入 | 职责 | 不得用于 |
|---|---|---|
| 当前 UI 白膜 | 界面结构、实际面板比例、板块数量、槽位和按钮位置、层级关系 | 随意决定最终材质和美术风格 |
| `元素参考/` 风格图 | 黑钢材质、克制琥珀色点缀、金属磨损、倒角语言、边框精度、按钮质感和整体视觉统一 | 改变白膜结构、增加未经要求的板块或移动组件 |

强制执行规则：

- 开工前必须枚举并查看 `元素参考/` 中的全部风格图片，不得只凭记忆描述风格。
- 图像生成时必须同时提供“当前白膜”和“元素参考风格图”，并在提示词中标明各自角色。
- 白膜优先决定结构；元素参考优先决定外观。两者冲突时，不得用风格图改变白膜布局。
- 风格必须保持现代末世工业黑钢体系：深色金属底、清晰分层倒角、细致磨损纹理、克制的琥珀/警示色点缀和高精度边缘。
- 禁止每个 UI 自行创造无关的新美术体系、颜色主题或边框语言。
- 每个项目必须把实际采用的风格参考复制到项目的 `in/`，建议命名：

```text
ProjectId_StyleReference_01_WidthxHeight.jpg
```

- 项目 README 和 QA 必须记录采用了哪些风格参考文件。
- 完整 UI 初稿审核时，除比例和结构外，还必须检查它与 `元素参考/` 风格图在材质、配色、倒角、磨损密度和按钮质感上的一致性。

## 4. 项目和组件命名规范

### 4.1 项目标识

每个项目开工前必须明确：

```text
ProjectDisplayName: 中文界面名称
ProjectId: 稳定英文项目标识，以 UI 结尾
ComponentPrefix: 稳定英文组件前缀，通常为 ProjectId 去掉 UI
```

规则：

- 只使用英文 ASCII、数字和 PascalCase。
- 禁止中文文件名、空格、拼音缩写和无意义编号。
- `ProjectId` 必须唯一，建立后不得随意更改。
- 项目重命名时必须同步文件夹、组件前缀、README、QA、清单和所有引用。

### 4.2 正式组件文件名

统一格式：

```text
ComponentPrefix_ComponentName_State_WidthxHeight.png
```

字段含义：

- `ComponentPrefix`：项目英文前缀，例如 `EquipmentCrafting`。
- `ComponentName`：组件职责，使用 PascalCase，例如 `CloseButton`、`MainPanelBase`、`MaterialSlot`。
- `State`：`Normal`、`Hover`、`Pressed`、`Disabled`、`Default` 或 `Empty`。
- `WidthxHeight`：真透明紧边裁剪后 PNG 的实际像素尺寸，必须与文件属性完全一致。

正确示例：

```text
EquipmentCrafting_MainPanelBase_Empty_1536x999.png
EquipmentCrafting_RecipeListPanel_Empty_481x830.png
EquipmentCrafting_CloseButton_Normal_65x63.png
EquipmentCrafting_CloseButton_Hover_65x63.png
EquipmentCrafting_CloseButton_Pressed_65x63.png
EquipmentCrafting_CloseButton_Disabled_65x63.png
EquipmentCrafting_MaterialSlot_Empty_151x145.png
EquipmentCrafting_CraftButton_Normal_400x86.png
```

错误示例：

```text
按钮1.png
close final.png
左边按钮.png
CloseButton.png
CloseButton_Normal.png
CloseButton_Normal_64x64.png    # 缺少 ComponentPrefix
```

### 4.3 状态组命名

按钮默认必须包含：

```text
Normal
Hover
Pressed
Disabled
```

同一状态组：

- 只有 `State` 字段允许变化。
- `ComponentPrefix`、`ComponentName`、`WidthxHeight` 必须完全一致。
- 必须使用同一个 `Union Bounds`、画布尺寸、主体位置、锚点和 `CropOffset`。
- 缺少必需状态的资源不能作为正式完成版进入 `out`。
- 只有产品或配置明确证明某状态永远不存在时，才允许在 QA 中记录 `Not Applicable`；不能用“以后补”代替。

## 5. 拆分层级规范

必须按以下层级拆分：

```text
MainPanelBase
└─ LargeChildPanel
   └─ SmallPanel / Slot / Button / Icon / Track / Thumb
```

- `MainPanelBase` 只保留最外层父框和连续背景，不得烘焙任何小板或按钮。
- 每个可见大子板独立导出；大子板内部不得烘焙其上的小板、槽位和按钮。
- 小板放在大板上方，通过坐标和 `CropOffset` 原位组装。
- 重复槽位允许输出一套可复用资源，但必须在 QA 中列出全部回拼坐标。
- 原位回拼图必须放在 `into/ReassemblyPreview/`，不能放进正式 `out`。

## 6. 文字、符号和按钮内部规则

- 普通按钮文字、标题、说明文字、动态数字、本地化文字全部从美术 PNG 中去除。
- X、加号、减号、箭头等承担功能识别的符号保留。
- 非符号按钮去字后必须补全文字下方的底板和纹理。
- 按钮和槽位是完整实心板件；内部安全区 Alpha 必须为 `255`。
- 透明像素只允许存在于真实外轮廓之外，不能从按钮或槽位内部透出棋盘格。
- 禁止使用会穿透内部底板的全图差分 Alpha 蒙版。

## 7. 真透明与紧边裁剪

必须执行主 README 的流程：

```text
Target Region
→ 单组件隔离
→ 真实轮廓 Alpha
→ 清除低 Alpha 背景残留
→ Visible Bounds
→ 状态组 Union Bounds
→ 紧边正式画布
→ CropOffset
→ 原位回拼
```

验收要求：

- 裁切不等于抠图；固定圆角、固定倒角或只透明四角不算真实抠图。
- 组件轮廓外 `Alpha = 0`，实体内部接近 `Alpha = 255`。
- 正式画布必须贴到最外层有效实体边缘，不保留无意义透明安全边。
- 文件名尺寸必须等于正式 PNG 的真实尺寸。
- 阴影属于组件时计入包围盒；公共背景和环境阴影必须删除。
- 进行 100% 整体检查、400% 边缘检查和棋盘格检查。
- 记录 `Target Region`、`Visible Bounds`、`Union Bounds`、`CropOffset` 和原位坐标。

## 8. 比例与防变形回环

- 开工前测量白膜实际 UI 面板比例；白膜外部演示留白不计入面板比例。
- 禁止单轴缩放，必须满足 `ScaleX = ScaleY`。
- 比例不符时只能原生重生成，或使用等比缩放配合裁切/补边。
- 不得通过横向压缩或纵向压缩“修正比例”。
- 数值检查之外还必须检查方形槽位、圆形图标、边框厚度、文字和符号是否变形。
- 每一轮完整图、拆分图、回拼图都必须重新执行比例检查。

## 9. 固定制作与审核流程

每个 UI 严格执行：

1. 阅读主 README 和本交接文档。
2. 枚举并查看本项目所有输入图。
3. 强制枚举并查看 `../01_References/Style/` 中的全部风格图。
4. 标记白膜、元素参考风格图和其他输入的职责；白膜负责结构，元素参考负责视觉风格。
5. 确认 `ProjectDisplayName`、`ProjectId`、`ComponentPrefix`。
6. 测量白膜实际 UI 面板比例。
7. 创建标准项目目录，并把白膜和实际采用的风格图复制到 `in/`。
8. 同时参考白膜结构与元素参考风格生成一张完整 UI 效果图。
9. 执行比例、形变和风格一致性回环。
10. 只把完整效果图交给用户审核。
11. 用户确认后才能去字和拆分。
12. 生成纯父底板及各级空子板。
13. 单组件真实 Alpha 抠图。
14. 生成按钮四态并计算 `Union Bounds`。
15. 真透明紧边裁剪，记录尺寸和 `CropOffset`。
16. 原位回拼。
17. 执行 Alpha、按钮内部、文字、符号、比例、风格和边缘 QA。
18. 只有全部通过后，按正式英文命名写入 `Components/out/ProjectId/`。
19. 更新项目 README、组件清单、坐标表和 `FINAL_QA.md`。
20. 把正式输出目录和审核图路径交给用户。
21. 等待用户确认，再开始下一个 UI。

## 10. 完成状态判断

只有同时满足以下条件才能在本文件的“已完成项目”中新增记录：

- 完整 UI 已由用户确认；
- 父板和子板层级正确；
- 所有组件完成真实 Alpha 和紧边裁剪；
- 普通文字与动态数字已清除；
- 功能符号正确保留；
- 所有按钮状态齐全；
- 按钮内部不透明；
- 比例与形变回环通过；
- 原位回拼通过；
- `Components/out/ProjectId/` 只包含当前正式资源；
- 文件命名、真实尺寸、文档和目录一致；
- `QA/FINAL_QA.md` 结论为 `PASS`；
- 用户完成本项目最终审核。

如果任意一项未满足，状态只能是 `Draft`、`Pending Review`、`Needs Revision` 或 `Fail`，不得汇报为“已完成”。
