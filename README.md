# UI WORK FLOW — Unity 游戏 UI 生产工作流

这是一个用于批量生产 Unity 游戏 UI 图片资源的本地工作流。它管理白膜输入、Cook 主风格、装备鉴定次风格、完整 UI 比例复核、父子组件拆分、按钮四态、真实 Alpha、400% 边缘检查、棋盘格检查和原位回拼。

## 当前结果

截至 2026-09-14：

- 项目：11 个
- 验证通过：11 个（主界面的最终 Game 视图截屏由用户复核）
- 正式 PNG：258 个
- `DesktopUIWireframes` 白膜：8/8 已处理
- Cook 为第一风格标准；Equipment Identification 只补充 Cook 未覆盖的按钮或槽位类型
- 普通文字、动态数字和本地化内容不写入图片；`X`、`?`、`+`、`-`、箭头等功能符号按需保留

详细结果见 [`06_Status/COMPLETED_PROJECTS.md`](06_Status/COMPLETED_PROJECTS.md)。

## 图片资源政策

本仓库只上传工作流组件、脚本、配置和文档，不上传 PNG/JPG/JPEG 等图片资源，也不上传包含图片的交付压缩包。图片只保存在本地制作环境。

| 图片类型 | 本地目录 | 用途 |
|---|---|---|
| Cook 主风格 | `01_References/Style/Standards/Primary_Cook/` | 材质、配色、边框、按钮四态第一标准 |
| 装备鉴定次风格 | `01_References/Style/Standards/Secondary_EquipmentIdentification/` | Cook 未覆盖的帮助按钮、槽位和竖版模板 |
| 共享功能组件 | `01_References/SharedComponents/` | 稳定的 X、?、+、-、箭头等组件 |
| UI 白膜 | `01_References/LayoutWireframes/DesktopUIWireframes/` | 结构、比例、数量、层级和坐标 |
| 项目完整 UI | `04_Projects/<ProjectId>/FullUI/` | 拆分前的完整效果图 |
| 候选、回拼与 400% 预览 | `04_Projects/<ProjectId>/into/` | 中间 QA，不是正式资源 |
| Unity 正式 PNG | `04_Projects/<ProjectId>/Components/out/<ProjectId>/` | 最终导入目录 |

克隆仓库后，可运行以下命令重建被 Git 忽略的图片目录：

```powershell
python 05_Tools/bootstrap_asset_folders.py
```

## 目录作用

| 目录 | 作用 |
|---|---|
| `00_CoreDocs/` | 最高制作规范、补充规则和交接说明 |
| `01_References/` | 白膜、主次风格和共享组件参考 |
| `02_InputQueue/` | 新任务输入入口 |
| `03_ProjectTemplate/` | 新项目标准目录与 QA 文档模板 |
| `04_Projects/` | 每个 UI 的脚本、配置、清单和验收记录 |
| `05_Tools/` | 脚手架、目录初始化和验证工具 |
| `06_Status/` | 生产队列和完成状态 |
| `SkillPackage/` | 可安装的 `produce-game-ui-assets` 技能源码 |

## 标准流程

1. 把白膜放入 `01_References/LayoutWireframes/DesktopUIWireframes/`，或放入项目的 `in/`。
2. 创建 `04_Projects/<ProjectId>/` 项目目录。
3. 生成完整 UI，并测量实际面板边界与白膜比例。
4. 删除普通文字与动态数字，只保留必要功能符号。
5. 按层级拆分父板、子板、槽位和按钮；父板不得残留子件。
6. 为交互按钮生成 `Normal / Hover / Pressed / Disabled` 四态。
7. 执行 100%、400%、透明棋盘格和原位回拼检查。
8. 只有通过 QA 的 PNG 才写入 `Components/out/<ProjectId>/`。

正式资源命名：

```text
ComponentPrefix_ComponentName_State_WidthxHeight.png
```

例如：

```text
CharacterAttributes_CloseButton_Normal_52x50.png
```

## Unity 导入建议

- Texture Type：Sprite (2D and UI)
- Filter Mode：Bilinear
- Wrap Mode：Clamp
- Mip Maps：Off
- Alpha Source：Input Texture Alpha
- Alpha Is Transparency：On
- 可拉伸面板使用九宫格；按钮、槽位和图标不要做非等比拉伸
- 所有可本地化和动态内容使用引擎文本节点

## 验证

```powershell
python SkillPackage/produce-game-ui-assets/scripts/validate_project.py --project 04_Projects/<ProjectId>
```

每个项目必须包含资产清单、组件坐标、比例循环、按钮文字矩阵、最终 QA 和项目配置。最高标准以 `00_CoreDocs/README_MASTER.md` 为准。

## 毛玻璃专用变体

`IPHONEE_VALID` 分支新增 [`WorkflowVariants/IPhoneGlassUIWorkflow`](WorkflowVariants/IPhoneGlassUIWorkflow/README.md)。该变体专门处理 GLSDD/URP 毛玻璃 UI：

- 随附用户确认的唯一 `毛玻璃.json`；
- Unity 中固定读取 `Assets/SHADER/玻璃预设/毛玻璃.json`，缺失时阻止烘焙；
- Tint 和各区域色相强制来自白模；
- 风格参考只提供材质、倒角、边框、高光、阴影、纹理与磨损；
- 提供白模区域取色、Unity 包安装、玻璃项目脚手架和专项验证脚本；
- 不上传白模、风格图、生成图或正式 PNG。

该分支也包含外部 [`UNITY_FIGHTCHRACTER_FLOW_PLUGIN`](https://github.com/AaronSwartz0217/UNITY_FIGHTCHRACTER_FLOW_PLUGIN) 的兼容契约与只读检查器。插件库存继续保存在原插件仓库，本仓库不复制 `Packages/`；动画重定向、刚性装备挂点、换装/蒙皮绑骨和 Animator 套动作的能力边界及运行时验收标准见毛玻璃变体说明。

## 登录、角色选择与主界面毛玻璃示例

[`04_Projects/LargeLoginUI`](04_Projects/LargeLoginUI/README.md) 与 [`04_Projects/MainHUDUI`](04_Projects/MainHUDUI/README.md) 组成当前变体的三页可运行示例。它不依赖 Cook、装备鉴定或旧工业模板，包含：

- 登录、角色选择和主界面的白模与用户确认稿记录；
- 无文字 PNG 的组件清单和按钮四态契约；
- Unity 2022.3 URP 的可重建 uGUI/TMP 预制体、独立场景、三页流程场景和毛玻璃材质；
- 可输入的登录页、角色选择页与 `EnterGameButton` 到主界面 HUD 的跳转；
- 57 个主界面透明组件，其中 13 个道具栏槽位具有 `Normal / Hover / Pressed / Disabled / Selected` 状态；
- 登录、角色选择、主界面按钮及道具栏的玻璃中部透明度统一为约 `64/255`；
- 运行时玻璃 Shader 保留 PNG 源 Alpha，并乘以 uGUI `Image.color.a`，避免场景中重新变成实心；
- 主界面不创建全屏蓝色背景，中央保持透明，供后续 3D 场景显示；
- 输入框、按钮、状态接口、颜色对照、回拼和两轮 QA；
- Unity CLI 构建与结构验证记录。

三页运行顺序为：

```text
LoginScreen -> CharacterSelectionScreen -> MainHUDScreen
```

当前集成场景验证为 2 个登录输入框、1 个角色名称输入框、29 个按钮、37 个实时玻璃面板、0 个额外 SoftGlow 和 1 个 EventSystem。Bloom 已收敛为低强度配置，组件不烘焙辉光或硬描边。

仓库继续遵守图片资源排除策略：Git 保存预制体、材质、Shader、脚本、配置和说明，PNG/JPG 只保留在本地工作文件夹。
