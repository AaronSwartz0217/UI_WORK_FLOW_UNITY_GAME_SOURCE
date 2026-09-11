# Component Coordinates

Canvas: 1464×828. Pixel coordinates use the top-left as origin.

| Instance | Component asset | Top-left | Size | Reuse |
|---|---|---:|---:|---|
| Background | `LargeLogin_Background_Default_1464x828.png` | (0, 0) | 1464×828 | 1 |
| AccountInput | `LargeLogin_InputField_Default_312x56.png` | (576, 277) | 312×56 | Shared |
| PasswordInput | `LargeLogin_InputField_Default_312x56.png` | (576, 353) | 312×56 | Shared |
| LoginButton | `LargeLogin_ActionButton_*_312x56.png` | (576, 469) | 312×56 | Shared |
| RegisterButton | `LargeLogin_ActionButton_*_312x56.png` | (576, 543) | 312×56 | Shared |

Unity anchored positions relative to the screen center through `LoginForm`: account `(0, 109)`, password `(0, 33)`, login `(0, -83)`, register `(0, -157)`.

## CharacterSetup layout

| Instance | Component asset | Top-left | Size | Reuse |
|---|---|---:|---:|---|
| Background | `LargeLogin_CharacterSetupBackground_Default_1464x828.png` | (0, 0) | 1464×828 | 1 |
| MainPanel | `LargeLogin_CharacterSetupMainPanel_Default_1012x328.png` | (226, 98) | 1012×328 | 1 |
| NameInput | `LargeLogin_CharacterSetupNameInput_Default_482x50.png` | (393, 111) | 482×50 | 1 |
| CurrentEquipmentSlot | `LargeLogin_CharacterSetupCurrentEquipmentSlot_Empty_222x214.png` | (622, 185) | 222×214 | 1 |
| EquipmentCard1 | `LargeLogin_CharacterSetupEquipmentCard_*_184x164.png` | (228, 440) | 184×164 | Shared state family |
| EquipmentCard2 | `LargeLogin_CharacterSetupEquipmentCard_*_184x164.png` | (434, 440) | 184×164 | Shared state family |
| EquipmentCard3 | `LargeLogin_CharacterSetupEquipmentCard_*_184x164.png` | (640, 440) | 184×164 | Shared state family |
| EquipmentCard4 | `LargeLogin_CharacterSetupEquipmentCard_*_184x164.png` | (846, 440) | 184×164 | Shared state family |
| EquipmentCard5 | `LargeLogin_CharacterSetupEquipmentCard_*_184x164.png` | (1052, 440) | 184×164 | Shared state family |
| EnterGameButton | `LargeLogin_CharacterSetupEnterGameButton_*_368x72.png` | (549, 647) | 368×72 | 1 state family |

Unity anchored positions relative to the 1464×828 screen center: main panel `(0, 152)`, name input `(-98, 278)`, current equipment slot `(1, 122)`, cards `(-412/-206/0/206/412, -109)`, and enter-game button `(1, -269)`.
