# 大型登录界面交付包

## 文件夹

- `UI/`：用户确认的完整视觉稿、无文字回拼稿和干净背景模板。
- `Components/`：可直接导入 Unity 的正式 PNG；输入框复用一张，登录/注册复用同一按钮四态。
- `UnityPackage/Assets/`：uGUI/TMP 预制体、预览场景、材质、URP 毛玻璃 Shader、预设和重建工具。
- `QA/`：组件坐标、颜色对照、透明棋盘格、最终检查和资产清单。

## Unity 使用

1. 将 `UnityPackage/Assets` 合并到 Unity 2022.3 URP 项目的 `Assets`。
2. 在 Unity 中执行 `Tools > Large Login UI > Rebuild Glass Login`。
3. 打开 `Assets/LargeLoginUI/Scenes/LargeLoginPreview.unity`，或将 `Assets/LargeLoginUI/Prefabs/LargeLoginScreen.prefab` 放入自己的场景。
4. 给 TextMeshPro 配置项目自己的中文字体/fallback。
5. 在 `LargeLoginScreenView` 上订阅登录和注册事件；本包不包含实际账号验证或场景切换。

实时玻璃依赖 URP Opaque Texture，重建命令会为找到的 URP Asset 开启该选项。

旧 Cook、装备鉴定和工业风模板不属于本项目的视觉依据。
