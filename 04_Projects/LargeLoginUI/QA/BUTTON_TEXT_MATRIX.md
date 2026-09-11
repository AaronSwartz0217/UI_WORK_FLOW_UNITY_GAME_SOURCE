# Button and Text Matrix

| Instance | Sprite family | Unity text | Rendering |
|---|---|---|---|
| LoginButton | `LargeLogin_ActionButton_*_312x56.png` | `登录` | TextMeshProUGUI |
| RegisterButton | `LargeLogin_ActionButton_*_312x56.png` | `注册` | TextMeshProUGUI |
| EquipmentCard1–5 | `LargeLogin_CharacterSetupEquipmentCard_*_184x164.png` | `武器名称` | TextMeshProUGUI |
| EnterGameButton | `LargeLogin_CharacterSetupEnterGameButton_*_368x72.png` | `进入游戏` | TextMeshProUGUI |

The login and enter-game sprite families contain `Normal`, `Hover`, `Pressed`, and `Disabled`. The equipment-card family additionally contains `Selected`. All state canvases and alpha silhouettes match within their family. Button text is not baked into any PNG.

Additional TMP strings in the prefab: `账号：`, `密码：`, `请输入账号`, `请输入密码`, status output, and the 16+ play-time notice.

Additional CharacterSetup TMP strings: `角色名称：`, `请输入名称`, `当前装备`, and status output.
