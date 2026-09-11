# 大型登录界面 / LargeLoginUI

## 结果

这是独立于旧 Cook、装备鉴定和工业风共享模板的新登录界面项目。登录白模决定布局与黑金色倾向，用户确认的完整稿决定材质观感，`毛玻璃.json` 决定实时折射、模糊、透明、曝光与高光参数。

所有 PNG 均不包含文字。账号、密码、状态、登录、注册和底部提示全部由 Unity TextMeshPro 渲染。

## 输入与视觉依据

- 白模：`in/LargeLoginUI_Wireframe_1464x828.jpg`
- 用户确认的完整稿：`FullUI/LargeLoginUI_FullUI_Draft_1464x828.png`
- 毛玻璃预设：`UnityPackage/Assets/SHADER/玻璃预设/毛玻璃.json`
- 旧 Cook、Equipment identification 和旧共享工业模板：已排除，不参与本项目生成。

## 正式图片

正式 PNG 位于：

`Components/out/LargeLoginUI/`

包含一张 1464×828 干净背景、一个 312×56 输入框和一个 312×56 按钮四态族。两个输入框复用同一 Sprite；登录与注册复用同一按钮四态族。

## Unity 预制体

Unity 内容位于：

`UnityPackage/Assets/`

主要入口：

- 账号登录版式：`UnityPackage/Assets/LargeLoginUI/LoginScreen/`
- 角色创建与装备选择版式：`UnityPackage/Assets/LargeLoginUI/CharacterSetup/`
- 登录预制体：`UnityPackage/Assets/LargeLoginUI/LoginScreen/Prefabs/LargeLoginScreen.prefab`
- 登录预览场景：`UnityPackage/Assets/LargeLoginUI/LoginScreen/Scenes/LargeLoginPreview.unity`
- 登录输入框材质：`UnityPackage/Assets/LargeLoginUI/LoginScreen/Materials/LargeLogin_GlassInput.mat`
- 登录按钮材质：`UnityPackage/Assets/LargeLoginUI/LoginScreen/Materials/LargeLogin_GlassButton.mat`
- 实时 Shader：`UnityPackage/Assets/URPFrostedGlass/URPFrostedGlassUI.shader`
- 登录版式重建工具：`UnityPackage/Assets/LargeLoginUI/LoginScreen/Editor/LargeLoginPrefabBuilder.cs`

把 `UnityPackage/Assets` 合并到 Unity 2022.3 URP 项目的 `Assets` 后，执行：

`Tools > Large Login UI > Login Screen > Rebuild`

两个版式使用不同的图片文件名、组件目录和预制体目录。重建工具会读取固定预设、生成透明组件、创建材质与预制体，并打开 URP Opaque Texture。登录验证、账号存储和场景切换不在本 UI 包内；`LargeLoginScreenView` 只提供登录/注册事件和状态文本接口。

发布前请给 TMP 配置项目自己的中文字体与 fallback 链。PNG 中没有烘焙字体。

## 验证

- Unity 版本：2022.3.62f3c1
- URP：14.0.12
- Unity CLI 构建：通过
- Prefab 结构检查：2 个 TMP 输入框、2 个按钮、4 个实时毛玻璃面板
- 预览场景：恰好 1 个 EventSystem
- 按钮四态：相同尺寸、相同 alpha 轮廓
- 正式目录：仅 PNG
