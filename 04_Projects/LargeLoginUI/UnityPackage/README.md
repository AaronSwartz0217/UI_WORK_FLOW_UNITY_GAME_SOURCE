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

Rebuild the second layout with:

`Tools > Large Login UI > Character Setup > Rebuild`

Rebuild the camera-backed glass showcase with:

`Tools > UI Scene Test > Rebuild Showcase Scene`

The showcase uses a Screen Space Camera canvas and an opaque background quad. This is intentional: it puts the background into `_CameraOpaqueTexture`, allowing the frosted-glass shader to perform live blur, refraction, gloss, and dispersion instead of displaying only a static transparent PNG.

The two layouts use separate art, material, prefab, scene, script, and editor folders. They do not share filenames. Both prefabs use TextMeshPro for all visible text; no text is baked into PNG assets. Assign the host project's CJK TMP font/fallback chain before shipping. The login controller only exposes login/register UI events. Authentication, account storage and scene switching remain the responsibility of the host game.

The glass shader requires URP Opaque Texture. The rebuild command enables it on URP assets found in the current project.
