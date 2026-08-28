# Production Queue

当前磁盘中已发现的 8 张桌面 UI 白膜均已处理；加上独立的烹饪模式项目，共 9 项完成。

| Priority | 项目 | ProjectId | Formal PNG | Status | Next action |
|---:|---|---|---:|---|---|
| 1 | 属性 | CharacterAttributesUI | 19 | PASS | complete |
| 2 | 装备进阶 | EquipmentAdvancementUI | 25 | PASS | complete |
| 3 | 熔炼 | SmeltingUI | 11 | PASS | complete |
| 4 | 附魔 | EquipmentEnchantingUI | 23 | PASS | complete |
| 5 | 组队邀请弹窗 | TeamInvitationPopupUI | 16 | PASS | complete |
| 6 | 胚体养成 | EmbryoCultivationUI | 19 | PASS | complete |
| 7 | 装备 | EquipmentUI | 12 | PASS | complete |
| 8 | 装备打造 | EquipmentCraftingUI | 26 | PASS / legacy retained | complete |
| 9 | 烹饪模式 | CookingModeUI | 31 | PASS / legacy retained | complete |

合计：182 个正式 PNG，9/9 项目验证通过。

新白膜进入 `../01_References/LayoutWireframes/DesktopUIWireframes/` 后，再按一项目一目录追加队列。正式输出始终位于 `../04_Projects/<ProjectId>/Components/out/<ProjectId>/`。
