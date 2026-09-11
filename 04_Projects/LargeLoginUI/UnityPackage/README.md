# LargeLoginUI Unity package

Copy the contained `Assets` folder into a Unity 2022.3 URP project, then run:

`Tools > Large Login UI > Rebuild Glass Login`

Generated entry points:

- `Assets/LargeLoginUI/Prefabs/LargeLoginScreen.prefab`
- `Assets/LargeLoginUI/Scenes/LargeLoginPreview.unity`
- `Assets/LargeLoginUI/Materials/LargeLogin_GlassInput.mat`
- `Assets/LargeLoginUI/Materials/LargeLogin_GlassButton.mat`

The prefab uses TextMeshPro for all visible text; no text is baked into PNG assets. Assign the host project's CJK TMP font/fallback chain before shipping. The controller only exposes login/register UI events. Authentication, account storage and scene switching remain the responsibility of the host game.

The glass shader requires URP Opaque Texture. The rebuild command enables it on URP assets found in the current project.
