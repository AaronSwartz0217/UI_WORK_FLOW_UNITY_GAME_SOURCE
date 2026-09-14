# Production Queue

当前磁盘中已发现的 8 张桌面 UI 白膜均已处理；加上独立的烹饪模式项目，以及新毛玻璃登录流程和主界面 HUD，共 11 项完成。

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
| 10 | 大型登录界面 | LargeLoginUI | 19 | PASS | complete |
| 11 | 主界面 HUD | MainHUDUI | 57 | PASS | user Game-view screenshot review |

合计：258 个正式 PNG，11/11 项目验证通过。主界面最终 Game 视图截屏由用户复核。

新白膜进入 `../01_References/LayoutWireframes/DesktopUIWireframes/` 后，再按一项目一目录追加队列。正式输出始终位于 `../04_Projects/<ProjectId>/Components/out/<ProjectId>/`。
