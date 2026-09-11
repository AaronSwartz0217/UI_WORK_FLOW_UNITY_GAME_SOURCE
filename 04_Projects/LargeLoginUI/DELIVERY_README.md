# 大型登录界面交付包

## 文件夹

- `LoginScreen/UI/`：账号密码登录版式的完整视觉稿、无文字回拼稿和干净背景模板。
- `LoginScreen/Components/`：账号密码登录版式拆成单块后的正式 PNG。
- `LoginScreen/QA/`：账号密码登录版式检查记录。
- `CharacterSetup/UI/`：角色创建与装备选择版式的白模、完整稿和无字回拼稿。
- `CharacterSetup/Components/`：角色创建与装备选择版式拆成单块后的 13 张独立 PNG。
- `CharacterSetup/QA/`：角色创建版式的坐标、状态、透明棋盘格和颜色检查。
- `UnityPackage/Assets/`：uGUI/TMP 预制体、预览场景、材质、URP 毛玻璃 Shader、预设和重建工具。

## Unity 使用

1. 将 `UnityPackage/Assets` 合并到 Unity 2022.3 URP 项目的 `Assets`。
2. 账号密码登录版式执行 `Tools > Large Login UI > Login Screen > Rebuild`；角色创建与装备选择版式执行 `Tools > Large Login UI > Character Setup > Rebuild`。
3. 账号登录资源位于 `Assets/LargeLoginUI/LoginScreen/`，角色创建与装备选择资源位于 `Assets/LargeLoginUI/CharacterSetup/`。
4. 给 TextMeshPro 配置项目自己的中文字体/fallback。
5. 在 `LargeLoginScreenView` 上订阅登录和注册事件；本包不包含实际账号验证或场景切换。

实时玻璃依赖 URP Opaque Texture，重建命令会为找到的 URP Asset 开启该选项。

旧 Cook、装备鉴定和工业风模板不属于本项目的视觉依据。
