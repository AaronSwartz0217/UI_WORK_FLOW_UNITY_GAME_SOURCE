# Login-to-character runtime test

Open `Assets/UI场景测试/Scenes/LoginCharacterFlow.unity` and enter Play Mode.

1. Type any non-empty value into account and password.
2. Click 登录, or press Enter while the password field is focused.
3. The test controller waits briefly and cross-fades to the character-selection page.
4. 注册 only displays a test-scene status because no registration service is connected.

The test credential rule exists only for UI verification. For production, disable
`acceptAnyNonEmptyCredentialsForDemo` and connect the account service to:

- `LoginToCharacterFlowController.NotifyLoginSucceeded()`
- `LoginToCharacterFlowController.NotifyLoginFailed(string message)`

Runtime rendering requirements:

- Unity 2022.3 URP
- Opaque Texture enabled
- HDR and camera post-processing enabled
- `LoginCharacterFlow_GlassLighting.asset` assigned to the global Volume
- the opaque background quad kept active for `_CameraOpaqueTexture` sampling

The Source Han Sans SC dynamic SDF asset is included so Chinese UI does not rely
on `LiberationSans SDF` or a machine-local font. The glass preset remains unchanged;
the flow scene adds a reduced HDR highlight, subtle Bloom, and one low-opacity
soft-glow layer per glass panel for consistent Play Mode visibility.

Automated checks validate structure and feature wiring. Final screenshot comparison
is intentionally manual.
