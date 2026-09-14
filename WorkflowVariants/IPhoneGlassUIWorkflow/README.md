# IPhone Glass UI Workflow

`IPhoneGlassUIWorkflow` 是现有 `produce-game-ui-assets` 的毛玻璃专用变体。它保留原工作流的白模结构、组件拆分、四态、真 Alpha、回拼和两轮 QA 门槛，并增加两条强制规则：

1. 所有玻璃面板从同一个已批准预设开始；
2. 最终颜色由白模对应区域决定，风格图不得覆盖白模色相。

此目录不包含任何 PNG、JPG 或其他图片资源。白模和风格参考仍由使用者放入本地项目的 `in/` 目录。

## 目录

```text
IPhoneGlassUIWorkflow/
├─ README.md
├─ workflow-variant.json
├─ external-plugins/
│  └─ fight-character-plugin.lock.json
├─ SkillPackage/produce-iphone-glass-ui-assets/
│  ├─ SKILL.md
│  ├─ references/
│  ├─ scripts/
│  └─ assets/project-template/
└─ UnityPackage/Assets/
   ├─ SHADER/玻璃预设/毛玻璃.json
   └─ URPFrostedGlass/
```

## 唯一预设

仓库随附的预设源：

```text
UnityPackage/Assets/SHADER/玻璃预设/毛玻璃.json
```

安装后的 Unity 运行时路径：

```text
Assets/SHADER/玻璃预设/毛玻璃.json
```

预设是用户提供的原文件，本变体不修改其中的参数。安装脚本只负责把它与 GLSDD/URP 组件复制到目标 Unity 项目。

## 安装到 Unity

要求 Unity 2022.3、URP 14，并在活动 URP Asset 中开启 Opaque Texture。

```powershell
python SkillPackage/produce-iphone-glass-ui-assets/scripts/install_unity_package.py `
  --unity-project <UnityProjectRoot>
```

目标文件已存在且内容不同时，脚本会停止，不会静默覆盖。只有明确确认覆盖后才添加 `--force`。

Unity 编译完成后打开：

```text
Tools > URP Frosted Glass > Transparent PNG Baker
```

窗口会从固定运行时路径读取预设。缺失或格式无效时，烘焙会被阻止。

## 新建玻璃 UI 项目

```powershell
python SkillPackage/produce-iphone-glass-ui-assets/scripts/scaffold_glass_project.py `
  --workflow-root <UIWorkflow> `
  --project-id <ProjectIdEndingWithUI> `
  --display-name <ProjectDisplayName> `
  --component-prefix <ComponentPrefix>
```

项目仍输出到：

```text
04_Projects/<ProjectId>/Components/out/<ProjectId>/
```

正式输出目录只能包含通过 QA 的 PNG。

## 从白模生成颜色表

先在项目 `in/` 中建立区域文件，格式见：

```text
SkillPackage/produce-iphone-glass-ui-assets/assets/wireframe-regions.example.json
```

然后运行：

```powershell
python SkillPackage/produce-iphone-glass-ui-assets/scripts/extract_wireframe_palette.py `
  --wireframe <project/in/wireframe.png> `
  --regions <project/in/wireframe-regions.json> `
  --out <project/QA/WIREFRAME_COLOR_MAP.json> `
  --markdown <project/QA/GLASS_COLOR_QA.md>
```

纯灰、低饱和度或多主色冲突的区域会被标为 `Pending`，不得进入正式生成。确认后的颜色表可在 GLSDD 中通过“从白模颜色表应用 Tint”加载。

## 验证

```powershell
python SkillPackage/produce-iphone-glass-ui-assets/scripts/validate_glass_project.py `
  --project <UIWorkflow/04_Projects/ProjectId> `
  --unity-project <UnityProjectRoot>
```

验证同时执行基础 UI 检查和玻璃专项检查，包括固定预设、白模取色记录、颜色决策、相对路径、Shader 接入和正式输出边界。

## 关键原则

- 白模决定结构、比例、层级、主色、辅色、强调色和局部颜色。
- 风格参考只决定材质、倒角、边框语言、纹理、高光、阴影和磨损。
- GLSDD 每次先读取已批准预设，再允许按当前面板比例调整输出尺寸与圆角。
- Tint 只能从当前白模区域的已确认颜色记录应用。
- 未经用户明确确认，不得覆盖全局 `毛玻璃.json`。
- 透明 PNG 只保存遮罩、透明色和表面光泽；实时模糊、折射与色散由 URP Shader 完成。
- 运行时 Shader 必须保留 PNG 的源 Alpha，并继续乘以 uGUI `Image.color.a`；`Maximum Rendered Opacity` 可作为明确的运行时上限，不得把玻璃有效区域重新输出为 Alpha `1`。
- 玻璃组件允许设计所需的半透明内部；非玻璃按钮和槽位继续执行内部安全区 Alpha `255` 的基础规则。

## 外部角色插件适配

此分支已按外部仓库 `UNITY_FIGHTCHRACTER_FLOW_PLUGIN` 的当前版本更新兼容契约，但不复制插件库存。插件源码、UPM 包和后续版本仍以原仓库为唯一来源：

```text
https://github.com/AaronSwartz0217/UNITY_FIGHTCHRACTER_FLOW_PLUGIN
```

当前锁定并验证：

| 包 | 版本 | 用途 |
|---|---:|---|
| `com.codex.split-rig-retargeter` | `1.4.0` | 分离骨架动画重定向、动画修复与烘焙 |
| `com.codex.mixamo-attachment-toolkit` | `0.3.0` | Mixamo/Humanoid 刚性装备挂点、运行时装备/卸载和姿态偏移 |

对应外部提交为 `095dc3c9a0920c221b681f9ecf10508873451a97`。详细模式边界和验收规则见：

```text
SkillPackage/produce-iphone-glass-ui-assets/references/fight-character-plugin.md
```

检查本地插件仓库：

```powershell
python SkillPackage/produce-iphone-glass-ui-assets/scripts/check_fight_character_plugin.py `
  --plugin-repo <LocalPluginRepository> `
  --report <ProjectId>/QA/FIGHT_CHARACTER_PLUGIN_COMPATIBILITY.json
```

检查器只读取外部仓库，不会复制其 `Packages/`、角色模型或资源。版本、提交、关键 API 或必需文件不匹配时会失败，要求先复核再更新锁文件。
