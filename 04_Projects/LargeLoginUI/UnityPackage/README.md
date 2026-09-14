# LargeLoginUI Unity package

Copy the contained `Assets` folder into a Unity 2022.3 URP project, then run:

`Tools > Large Login UI > Login Screen > Rebuild`

Generated entry points:

- `Assets/LargeLoginUI/LoginScreen/Prefabs/LargeLoginScreen.prefab`
- `Assets/LargeLoginUI/LoginScreen/Scenes/LargeLoginPreview.unity`
- `Assets/LargeLoginUI/LoginScreen/Materials/LargeLogin_GlassInput.mat`
- `Assets/LargeLoginUI/LoginScreen/Materials/LargeLogin_GlassButton.mat`
- `Assets/LargeLoginUI/CharacterSetup/Prefabs/LargeLoginCharacterSetup.prefab`
- `Assets/LargeLoginUI/CharacterSetup/Scenes/LargeLoginCharacterSetupPreview.unity`
- `Assets/UI场景测试/Scenes/UI场景测试.unity`
- `Assets/UI场景测试/Scenes/LoginCharacterFlow.unity`

Rebuild the second layout with:

`Tools > Large Login UI > Character Setup > Rebuild`

Rebuild the camera-backed glass showcase with:

`Tools > UI Scene Test > Rebuild Showcase Scene`

Rebuild the integrated login-to-character test flow with:

`Tools > UI Scene Test > Rebuild Login To Character Flow`

The showcase uses a Screen Space Camera canvas and an opaque background quad. This is intentional: it puts the background into `_CameraOpaqueTexture`, allowing the frosted-glass shader to perform live blur, refraction, gloss, and dispersion instead of displaying only a static transparent PNG.

The two layouts use separate art, material, prefab, scene, script, and editor folders. They do not share filenames. Both prefabs use TextMeshPro for all visible text; no text is baked into PNG assets.

The integrated scene includes a self-contained Source Han Sans SC dynamic TMP font, two editable login fields, Enter-to-submit, a test-only non-empty credential check, and a cross-fade into the character-selection screen. Replace the demo acceptance path with the host game's account service before shipping. `NotifyLoginSucceeded()` and `NotifyLoginFailed(string)` are the integration callbacks.

Runtime glass lighting uses a narrow HDR inner highlight, one low-opacity soft-glow layer per glass panel, and restrained URP Bloom/ACES. The soft-glow layer keeps the edge response visible when Bloom contribution differs between editor and player; Bloom is intentionally subtle.

The glass shader requires URP Opaque Texture. The rebuild command enables it on URP assets found in the current project.
