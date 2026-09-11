# LargeLoginUI Unity package

Copy the contained `Assets` folder into a Unity 2022.3 URP project, then run:

`Tools > Large Login UI > Login Screen > Rebuild`

Generated entry points:

- `Assets/LargeLoginUI/LoginScreen/Prefabs/LargeLoginScreen.prefab`
- `Assets/LargeLoginUI/LoginScreen/Scenes/LargeLoginPreview.unity`
- `Assets/LargeLoginUI/LoginScreen/Materials/LargeLogin_GlassInput.mat`
- `Assets/LargeLoginUI/LoginScreen/Materials/LargeLogin_GlassButton.mat`
- `Assets/LargeLoginUI/CharacterSetup/` (second layout; generated independently after full-UI approval)

The two layouts use separate art, material, prefab, scene, script, and editor folders. They do not share filenames. The prefab uses TextMeshPro for all visible text; no text is baked into PNG assets. Assign the host project's CJK TMP font/fallback chain before shipping. The controller only exposes login/register UI events. Authentication, account storage and scene switching remain the responsibility of the host game.

The glass shader requires URP Opaque Texture. The rebuild command enables it on URP assets found in the current project.
