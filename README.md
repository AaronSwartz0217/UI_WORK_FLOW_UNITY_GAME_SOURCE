# UI WORK FLOW — Unity Game UI Source

这是一套面向 Unity 游戏 UI 的生产工作流，负责管理白膜输入、风格参考、完整界面审核、组件拆分、按钮四态、透明度检查、坐标回拼和最终交付。

本仓库只保存可复用的工作流组件，包括：

- Markdown 制作规范和 QA 合同；
- JSON 项目配置、队列与状态记录；
- Python/PowerShell 工具脚本；
- 项目模板、技能包源码和目录说明；
- 各项目的组件清单、坐标、按钮状态及验收记录。

## 图片资源政策

本仓库不上传任何图片资源或生成图片，包括 PNG、JPG、JPEG、WEBP、GIF、BMP、TGA、TIFF 和 PSD，也不上传包含图片的 ZIP 交付包。

因此，克隆仓库后看到图片路径为空是正常情况，并不代表仓库损坏。图片由本地制作环境单独保存，Git 只管理流程、规则、脚本和配置。

图片应放到以下位置：

| 图片类型 | 本地放置目录 | 用途 |
|---|---|---|
| Cook 主风格标准 | 01_References/Style/Standards/Primary_Cook/ | 材质、配色、边框、按钮四态的第一优先级 |
| 装备鉴定次风格 | 01_References/Style/Standards/Secondary_EquipmentIdentification/ | 补充帮助按钮、槽位、竖版模板等 |
| 共享功能按钮 | 01_References/SharedComponents/ | X、?、+、-、方向箭头等稳定组件参考 |
| UI 白膜图库 | 01_References/LayoutWireframes/DesktopUIWireframes/ | 决定结构、比例、数量、层级和坐标 |
| 当前任务白膜 | 02_InputQueue/任务类别/ProjectId/Wireframe/ | 单个项目正式输入 |
| 项目完整效果图 | 04_Projects/ProjectId/FullUI/ | 用户审核通过后才能开始拆分 |
| 中间候选与回拼图 | 04_Projects/ProjectId/into/ | 候选、废稿、400% 检查和回拼预览 |
| 正式组件 PNG | 04_Projects/ProjectId/Components/out/ProjectId/ | Unity 最终导入目录 |

运行以下命令可以重新建立不会被 Git 保存的图片目录：

    python 05_Tools/bootstrap_asset_folders.py

## 目录作用

| 目录 | 作用 |
|---|---|
| 00_CoreDocs/ | 最高制作规范、补充规则、目录索引和 Agent 交接说明 |
| 01_References/ | 白膜、主次风格、共享组件以及参考规则 |
| 02_InputQueue/ | 待制作项目的请求、白膜和配置入口 |
| 03_ProjectTemplate/ | 新项目必须复制的标准目录和 QA 文档模板 |
| 04_Projects/ | 每个 UI 的独立生产目录、脚本、清单和验收记录 |
| 05_Tools/ | 项目脚手架、尺寸测量、资源审计和验证工具 |
| 06_Status/ | 生产队列、完成状态、失败或返工记录 |
| 07_Archive/ | 历史归档位置 |
| SkillPackage/ | 可安装的 produce-game-ui-assets 技能源码 |

## 开始使用

1. 阅读 00_CoreDocs/README_MASTER.md。
2. 阅读 00_CoreDocs/README_UI_PIPELINE_ADDENDUM.md。
3. 阅读 00_CoreDocs/UI_PRODUCTION_STATUS_AND_AGENT_HANDOFF.md。
4. 补齐 01_References/ 下的本地图片资源。
5. 将目标白膜复制到 02_InputQueue/任务类别/ProjectId/Wireframe/。
6. 从 03_ProjectTemplate/ProjectId/ 创建独立项目。
7. 先生成完整 UI，并等待用户确认。
8. 审核通过后再拆分组件、生成按钮四态并执行真透明处理。
9. 通过 100%、400%、棋盘格、坐标回拼和第二轮 QA 后，才允许写入正式组件目录。

正式资源命名：

    ComponentPrefix_ComponentName_State_WidthxHeight.png

示例：

    CharacterAttributes_CloseButton_Normal_52x50.png

## 关键生产规则

- 白膜只决定结构、比例、数量、层级和坐标；风格参考不能改变白膜布局。
- Cook 是主要风格标准，Equipment Identification 只补充 Cook 未覆盖的类型。
- 普通文字、本地化文字和动态数字不烘焙进新 UI；X、?、+、-、箭头等功能识别符号保留。
- 稳定功能按钮允许直接复用已经审核的完整四态母版，只修改项目文件名前缀。
- 裁切不等于抠图。正式组件必须沿真实轮廓建立 Alpha，外部 Alpha 为 0，实心内部安全区 Alpha 为 255。
- 静态组件按自身 Visible Bounds 紧边裁切；按钮四态使用统一 Union Bounds、画布、锚点和 CropOffset。
- 父板不得烘焙子组件；所有子组件按记录坐标回拼。
- 未通过最终 QA、仍含图片背景、缺少状态或只有近似轮廓的文件不得进入 Components/out。

## Unity 导入建议

- Texture Type: Sprite (2D and UI)
- Filter Mode: Bilinear
- Wrap Mode: Clamp
- Mip Maps: Off
- Alpha Source: Input Texture Alpha
- Alpha Is Transparency: On
- 可拉伸面板使用九宫格；小型按钮和图标不要非等比拉伸。

## 验证

技能包项目可使用：

    python SkillPackage/produce-game-ui-assets/scripts/validate_project.py --project 04_Projects/ProjectId

正式交付条件以 00_CoreDocs/README_MASTER.md 为最高标准。项目文档可以补充细节，但不能降低其透明度、拆分、命名、状态和 QA 要求。
