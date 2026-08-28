# 组队邀请弹窗 / TeamInvitationPopupUI

- 状态：`complete_automated_user_authorized`
- 正式完整 UI：`FullUI/TeamInvitationPopupUI_FullUI_Review06_1536x1024.png`
- 正式组件：`Components/out/TeamInvitationPopupUI/`
- 正式 PNG：16
- 验证：PASS

主风格使用 Cook，关闭按钮复用 Cook 已确认的完整四态。普通标题、邀请人、队伍人数、邀请类型、计时、按钮文字与空状态文案全部移除，只保留功能性 `X`。

```text
MainPanelBase
├─ HeaderPanel
│  └─ CloseButton
└─ InvitationListPanel
   └─ InvitationRow
      ├─ AcceptButton
      └─ RejectButton
```

父板均不包含可独立子件；正式目录只含最终 PNG。
