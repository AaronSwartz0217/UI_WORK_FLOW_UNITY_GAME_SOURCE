#if UNITY_EDITOR
using System;
using System.Collections.Generic;
using System.IO;
using LargeLoginUI;
using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine.SceneManagement;
using UnityEngine.TextCore.LowLevel;

public static class LoginCharacterFlowBuilder
{
    // Rebuilds three screens whose glass opacity is synchronized by the component sources.
    const string Root = "Assets/UI场景测试";
    const string ScenePath = Root + "/Scenes/LoginCharacterFlow.unity";
    const string MainHudScenePath = Root + "/Scenes/MainHUD.unity";
    const string MaterialPath = Root + "/Materials/LoginCharacterFlow_BackgroundOpaque.mat";
    const string ProfilePath = Root + "/Settings/LoginCharacterFlow_GlassLighting.asset";
    const string SourceFontPath =
        "Assets/LargeLoginUI/Shared/Fonts/SourceHanSansSC-Normal.otf";
    const string CjkFontAssetPath =
        "Assets/LargeLoginUI/Shared/Fonts/SourceHanSansSC-DynamicSDF.asset";
    const string LoginPrefabPath =
        "Assets/LargeLoginUI/LoginScreen/Prefabs/LargeLoginScreen.prefab";
    const string CharacterPrefabPath =
        "Assets/LargeLoginUI/CharacterSetup/Prefabs/LargeLoginCharacterSetup.prefab";
    const string LoginBackgroundPath =
        "Assets/LargeLoginUI/LoginScreen/Art/LargeLogin_Background_Default_1464x828.png";
    const string CharacterBackgroundPath =
        "Assets/LargeLoginUI/CharacterSetup/Art/" +
        "LargeLogin_CharacterSetupBackground_Default_1464x828.png";
    const string GlassShaderName = "UI/URP Frosted Glass Diffraction";

    [MenuItem("Tools/UI Scene Test/Rebuild Login To Character Flow")]
    public static void Build()
    {
        EnsureFolders();
        DeleteObsoleteFontAssets();
        EnableUrpFeatures();
        TuneGlassMaterials();

        GameObject loginPrefab = LoadRequired<GameObject>(LoginPrefabPath);
        GameObject characterPrefab = LoadRequired<GameObject>(CharacterPrefabPath);
        Texture2D loginBackground = LoadRequired<Texture2D>(LoginBackgroundPath);
        Texture2D characterBackground = LoadRequired<Texture2D>(CharacterBackgroundPath);
        TMP_FontAsset cjkFontAsset = CreateOrUpdateCjkFontAsset();
        GameObject mainHudPrefab = MainHUDPrefabBuilder.BuildPrefab();
        // Sprite reimports inside the HUD builder can invalidate cached UnityEngine.Object
        // references, so reacquire the font before assigning it to scene instances.
        cjkFontAsset = LoadRequired<TMP_FontAsset>(CjkFontAssetPath);

        Scene scene = EditorSceneManager.NewScene(
            NewSceneSetup.EmptyScene,
            NewSceneMode.Single);

        Camera camera = CreateCamera();
        Material backgroundMaterial = CreateOpaqueBackground(loginBackground);
        VolumeProfile profile = CreateLightingProfile();
        CreateGlobalVolume(profile);

        GameObject loginRoot = InstantiatePrefab(loginPrefab, scene, "LoginScreen");
        GameObject characterRoot = InstantiatePrefab(
            characterPrefab,
            scene,
            "CharacterSelectionScreen");
        GameObject mainHudRoot = InstantiatePrefab(
            mainHudPrefab,
            scene,
            "MainHUDScreen");

        CanvasGroup loginGroup = ConfigureCanvas(loginRoot, camera, 10);
        CanvasGroup characterGroup = ConfigureCanvas(characterRoot, camera, 10);
        CanvasGroup mainHudGroup = ConfigureCanvas(mainHudRoot, camera, 20);
        AssignCjkFont(loginRoot, cjkFontAsset);
        AssignCjkFont(characterRoot, cjkFontAsset);
        AssignCjkFont(mainHudRoot, cjkFontAsset);
        characterRoot.SetActive(false);
        mainHudRoot.SetActive(false);

        GameObject eventSystem = new GameObject(
            "EventSystem",
            typeof(EventSystem),
            typeof(StandaloneInputModule));
        eventSystem.transform.SetAsLastSibling();

        LargeLoginScreenView loginView = loginRoot.GetComponent<LargeLoginScreenView>();
        if (loginView == null)
            throw new InvalidDataException("Login prefab is missing LargeLoginScreenView.");
        UnityEngine.UI.Button enterGameButton = FindButton(characterRoot, "EnterGameButton");

        GameObject flowObject = new GameObject("LoginToCharacterFlow");
        LoginToCharacterFlowController flow =
            flowObject.AddComponent<LoginToCharacterFlowController>();
        flow.Configure(
            loginRoot,
            characterRoot,
            loginView,
            loginGroup,
            characterGroup,
            mainHudRoot,
            mainHudGroup,
            enterGameButton,
            backgroundMaterial,
            loginBackground,
            characterBackground,
            cjkFontAsset);

        EditorSceneManager.SaveScene(scene, ScenePath);
        ConfigureBuildSettings();
        PlayerSettings.productName = "UI场景测试";
        Validate(
            scene,
            camera,
            loginRoot,
            characterRoot,
            mainHudRoot,
            flow,
            backgroundMaterial,
            profile,
            enterGameButton);

        BuildStandaloneHudScene(mainHudPrefab, cjkFontAsset, profile, backgroundMaterial, characterBackground);
        SceneManager.SetActiveScene(scene);
        backgroundMaterial.mainTexture = loginBackground;
        if (backgroundMaterial.HasProperty("_BaseMap"))
            backgroundMaterial.SetTexture("_BaseMap", loginBackground);
        EditorUtility.SetDirty(backgroundMaterial);

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
        Debug.Log(
            "[LoginCharacterFlow] BUILD_SUCCESS scene=" + ScenePath +
            " flow=LoginScreen->CharacterSelectionScreen->MainHUDScreen " +
            "glassShader=" + GlassShaderName + " bloom=enabled");
    }

    static T LoadRequired<T>(string path) where T : UnityEngine.Object
    {
        T asset = AssetDatabase.LoadAssetAtPath<T>(path);
        if (asset == null)
            throw new FileNotFoundException(typeof(T).Name + " is missing", path);
        return asset;
    }

    static void DeleteObsoleteFontAssets()
    {
        string[] obsoletePaths =
        {
            "Assets/LargeLoginUI/Shared/Fonts/NotoSansSC-DynamicSDF.asset",
            "Assets/LargeLoginUI/Shared/Fonts/NotoSansSC-VF.ttf"
        };

        foreach (string path in obsoletePaths)
        {
            if (AssetDatabase.LoadMainAssetAtPath(path) != null)
                AssetDatabase.DeleteAsset(path);
        }
    }

    static TMP_FontAsset CreateOrUpdateCjkFontAsset()
    {
        AssetDatabase.ImportAsset(SourceFontPath, ImportAssetOptions.ForceSynchronousImport);
        Font sourceFont = LoadRequired<Font>(SourceFontPath);
        TMP_FontAsset fontAsset =
            AssetDatabase.LoadAssetAtPath<TMP_FontAsset>(CjkFontAssetPath);

        if (fontAsset == null)
        {
            fontAsset = TMP_FontAsset.CreateFontAsset(
                sourceFont,
                56,
                6,
                GlyphRenderMode.SDFAA,
                2048,
                2048,
                AtlasPopulationMode.Dynamic,
                true);
            if (fontAsset == null)
                throw new InvalidDataException(
                    "Unable to create the Source Han Sans SC TMP font asset.");

            fontAsset.name = "SourceHanSansSC Dynamic SDF";
            Texture2D atlas = fontAsset.atlasTextures[0];
            Material material = fontAsset.material;
            atlas.name = "SourceHanSansSC Dynamic SDF Atlas";
            material.name = "SourceHanSansSC Dynamic SDF Material";

            AssetDatabase.CreateAsset(fontAsset, CjkFontAssetPath);
            AssetDatabase.AddObjectToAsset(atlas, fontAsset);
            AssetDatabase.AddObjectToAsset(material, fontAsset);
        }

        fontAsset.atlasPopulationMode = AtlasPopulationMode.Dynamic;
        fontAsset.isMultiAtlasTexturesEnabled = true;
        EditorUtility.SetDirty(fontAsset);
        return fontAsset;
    }

    static void AssignCjkFont(GameObject root, TMP_FontAsset fontAsset)
    {
        TMP_Text[] texts = root.GetComponentsInChildren<TMP_Text>(true);
        string requiredCharacters = string.Empty;
        foreach (TMP_Text text in texts)
        {
            text.font = fontAsset;
            text.havePropertiesChanged = true;
            requiredCharacters += text.text;
            EditorUtility.SetDirty(text);
        }

        List<char> missingCharacters;
        if (!fontAsset.HasCharacters(requiredCharacters, out missingCharacters))
        {
            fontAsset.TryAddCharacters(requiredCharacters, out string ignoredMissingCharacters);
            if (!fontAsset.HasCharacters(requiredCharacters, out missingCharacters))
                throw new InvalidDataException(
                    "Source Han Sans SC is missing required UI characters: " +
                    new string(missingCharacters.ToArray()));
        }

        EditorUtility.SetDirty(fontAsset);
    }

    static GameObject InstantiatePrefab(GameObject prefab, Scene scene, string name)
    {
        GameObject instance = PrefabUtility.InstantiatePrefab(prefab, scene) as GameObject;
        if (instance == null)
            throw new InvalidOperationException("Unable to instantiate " + prefab.name + ".");
        instance.name = name;
        return instance;
    }

    static UnityEngine.UI.Button FindButton(GameObject root, string name)
    {
        foreach (UnityEngine.UI.Button button in
                 root.GetComponentsInChildren<UnityEngine.UI.Button>(true))
        {
            if (button.name == name)
                return button;
        }
        throw new InvalidDataException(root.name + " is missing button " + name + ".");
    }

    static CanvasGroup ConfigureCanvas(GameObject root, Camera camera, int sortingOrder)
    {
        Canvas canvas = root.GetComponent<Canvas>();
        if (canvas == null)
            throw new InvalidDataException(root.name + " has no Canvas.");

        canvas.renderMode = RenderMode.ScreenSpaceCamera;
        canvas.worldCamera = camera;
        canvas.planeDistance = 1f;
        canvas.overrideSorting = true;
        canvas.sortingOrder = sortingOrder;

        Transform internalBackground = root.transform.Find("Background");
        if (internalBackground != null)
            internalBackground.gameObject.SetActive(false);

        CanvasGroup group = root.GetComponent<CanvasGroup>();
        if (group == null)
            group = root.AddComponent<CanvasGroup>();
        return group;
    }

    static Camera CreateCamera()
    {
        GameObject go = new GameObject(
            "Main Camera",
            typeof(Camera),
            typeof(UniversalAdditionalCameraData));
        go.tag = "MainCamera";
        go.transform.position = new Vector3(0f, 0f, -10f);

        Camera camera = go.GetComponent<Camera>();
        camera.clearFlags = CameraClearFlags.SolidColor;
        camera.backgroundColor = new Color(0.012f, 0.009f, 0.006f, 1f);
        camera.orthographic = true;
        camera.orthographicSize = 4.14f;
        camera.nearClipPlane = 0.1f;
        camera.farClipPlane = 100f;
        camera.allowHDR = true;

        UniversalAdditionalCameraData data =
            go.GetComponent<UniversalAdditionalCameraData>();
        data.requiresColorOption = CameraOverrideOption.On;
        data.renderPostProcessing = true;
        data.volumeLayerMask = 1;
        data.dithering = true;
        return camera;
    }

    static Material CreateOpaqueBackground(Texture2D texture)
    {
        Shader shader = Shader.Find("Universal Render Pipeline/Unlit");
        if (shader == null)
            throw new InvalidOperationException("URP Unlit shader is missing.");

        Material material = AssetDatabase.LoadAssetAtPath<Material>(MaterialPath);
        if (material == null)
        {
            material = new Material(shader);
            AssetDatabase.CreateAsset(material, MaterialPath);
        }
        else
        {
            material.shader = shader;
        }

        material.name = "Login Character Flow Background Opaque";
        material.mainTexture = texture;
        if (material.HasProperty("_BaseMap"))
            material.SetTexture("_BaseMap", texture);
        if (material.HasProperty("_BaseColor"))
            material.SetColor("_BaseColor", Color.white);
        material.renderQueue = (int)RenderQueue.Geometry;
        EditorUtility.SetDirty(material);

        GameObject quad = GameObject.CreatePrimitive(PrimitiveType.Quad);
        quad.name = "OpaqueBackgroundForGlassSampling";
        quad.transform.position = Vector3.zero;
        quad.transform.localScale = new Vector3(14.64f, 8.28f, 1f);
        Collider collider = quad.GetComponent<Collider>();
        if (collider != null)
            UnityEngine.Object.DestroyImmediate(collider);
        quad.GetComponent<MeshRenderer>().sharedMaterial = material;
        return material;
    }

    static VolumeProfile CreateLightingProfile()
    {
        VolumeProfile profile = AssetDatabase.LoadAssetAtPath<VolumeProfile>(ProfilePath);
        if (profile == null)
        {
            profile = ScriptableObject.CreateInstance<VolumeProfile>();
            AssetDatabase.CreateAsset(profile, ProfilePath);
        }

        Bloom bloom;
        if (!profile.TryGet(out bloom))
            bloom = profile.Add<Bloom>(true);
        bloom.active = true;
        bloom.threshold.Override(0.92f);
        bloom.intensity.Override(0.24f);
        bloom.scatter.Override(0.46f);
        bloom.tint.Override(new Color(1f, 0.82f, 0.58f, 1f));
        bloom.highQualityFiltering.Override(true);

        Tonemapping tonemapping;
        if (!profile.TryGet(out tonemapping))
            tonemapping = profile.Add<Tonemapping>(true);
        tonemapping.active = true;
        tonemapping.mode.Override(TonemappingMode.ACES);

        ColorAdjustments colorAdjustments;
        if (!profile.TryGet(out colorAdjustments))
            colorAdjustments = profile.Add<ColorAdjustments>(true);
        colorAdjustments.active = true;
        colorAdjustments.postExposure.Override(0.05f);
        colorAdjustments.contrast.Override(4f);
        colorAdjustments.saturation.Override(2f);

        Vignette vignette;
        if (!profile.TryGet(out vignette))
            vignette = profile.Add<Vignette>(true);
        vignette.active = true;
        vignette.intensity.Override(0.12f);
        vignette.smoothness.Override(0.52f);

        EditorUtility.SetDirty(profile);
        return profile;
    }

    static void CreateGlobalVolume(VolumeProfile profile)
    {
        GameObject go = new GameObject("Global Glass Lighting");
        Volume volume = go.AddComponent<Volume>();
        volume.isGlobal = true;
        volume.priority = 10f;
        volume.sharedProfile = profile;
    }

    static void EnableUrpFeatures()
    {
        string[] guids = AssetDatabase.FindAssets("t:UniversalRenderPipelineAsset");
        if (guids.Length == 0)
            throw new InvalidOperationException("No UniversalRenderPipelineAsset found.");

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            UniversalRenderPipelineAsset asset =
                AssetDatabase.LoadAssetAtPath<UniversalRenderPipelineAsset>(path);
            if (asset == null)
                continue;

            asset.supportsCameraOpaqueTexture = true;
            asset.supportsHDR = true;
            EditorUtility.SetDirty(asset);
        }
    }

    static void TuneGlassMaterials()
    {
        string[] guids = AssetDatabase.FindAssets(
            "t:Material",
            new[] { "Assets/LargeLoginUI" });

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            Material material = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (material == null || material.shader == null ||
                material.shader.name != GlassShaderName)
                continue;

            float sheen = material.name.Contains("Input") ? 0.16f : 0.22f;

            material.SetFloat("_EdgeGlow", 0f);
            material.SetFloat("_EdgeGlowWidth", 1f);
            material.SetColor(
                "_EdgeGlowColor",
                new Color(1.12f, 0.78f, 0.46f, 0f));
            material.SetFloat("_SpecularSheen", sheen);
            material.SetFloat("_Exposure", 1.28f);
            material.SetFloat("_SpriteOverlay", 0.10f);
            EditorUtility.SetDirty(material);
        }
    }

    [MenuItem("Tools/UI Scene Test/Remove Added Glass Outline Layers")]
    public static void RemoveAddedOutlineLayers()
    {
        Scene scene = SceneManager.GetActiveScene();
        if (!scene.IsValid() || scene.path != ScenePath)
            scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);

        int removed = 0;
        foreach (GameObject rootObject in scene.GetRootGameObjects())
        {
            Transform[] transforms = rootObject.GetComponentsInChildren<Transform>(true);
            for (int i = transforms.Length - 1; i >= 0; i--)
            {
                Transform transform = transforms[i];
                if (!transform.name.EndsWith("_SoftGlow", StringComparison.Ordinal))
                    continue;

                UnityEngine.Object.DestroyImmediate(transform.gameObject);
                removed++;
            }
        }

        TuneGlassMaterials();
        EditorSceneManager.MarkSceneDirty(scene);
        EditorSceneManager.SaveScene(scene, ScenePath);
        AssetDatabase.SaveAssets();

        int remaining = 0;
        foreach (GameObject rootObject in scene.GetRootGameObjects())
        {
            foreach (Transform transform in rootObject.GetComponentsInChildren<Transform>(true))
            {
                if (transform.name.EndsWith("_SoftGlow", StringComparison.Ordinal))
                    remaining++;
            }
        }

        if (remaining != 0)
            throw new InvalidDataException("Added soft-glow outline layers remain in the scene.");

        Debug.Log(
            "[LoginCharacterFlow] OUTLINE_REMOVAL_PASS removed=" + removed +
            " edgeGlow=0 softGlows=0 bloom=preserved");
    }

    static void ConfigureBuildSettings()
    {
        List<EditorBuildSettingsScene> scenes = new List<EditorBuildSettingsScene>
        {
            new EditorBuildSettingsScene(ScenePath, true)
        };

        foreach (EditorBuildSettingsScene existing in EditorBuildSettings.scenes)
        {
            if (!string.Equals(existing.path, ScenePath, StringComparison.OrdinalIgnoreCase))
                scenes.Add(existing);
        }

        EditorBuildSettings.scenes = scenes.ToArray();
    }

    static void BuildStandaloneHudScene(
        GameObject mainHudPrefab,
        TMP_FontAsset font,
        VolumeProfile profile,
        Material backgroundMaterial,
        Texture2D previewBackground)
    {
        Scene previous = SceneManager.GetActiveScene();
        Scene hudScene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
        SceneManager.SetActiveScene(hudScene);

        Camera camera = CreateCamera();
        backgroundMaterial.mainTexture = previewBackground;
        if (backgroundMaterial.HasProperty("_BaseMap"))
            backgroundMaterial.SetTexture("_BaseMap", previewBackground);

        GameObject quad = GameObject.CreatePrimitive(PrimitiveType.Quad);
        quad.name = "PreviewWorldBackdrop_ReplaceWith3DScene";
        quad.transform.position = Vector3.zero;
        quad.transform.localScale = new Vector3(14.64f, 8.28f, 1f);
        Collider collider = quad.GetComponent<Collider>();
        if (collider != null)
            UnityEngine.Object.DestroyImmediate(collider);
        quad.GetComponent<MeshRenderer>().sharedMaterial = backgroundMaterial;

        CreateGlobalVolume(profile);
        GameObject hud = InstantiatePrefab(mainHudPrefab, hudScene, "MainHUDScreen");
        ConfigureCanvas(hud, camera, 20);
        AssignCjkFont(hud, font);

        new GameObject("EventSystem", typeof(EventSystem), typeof(StandaloneInputModule));
        EditorSceneManager.SaveScene(hudScene, MainHudScenePath);
        EditorSceneManager.CloseScene(hudScene, true);
        SceneManager.SetActiveScene(previous);
    }

    static void Validate(
        Scene scene,
        Camera camera,
        GameObject loginRoot,
        GameObject characterRoot,
        GameObject mainHudRoot,
        LoginToCharacterFlowController flow,
        Material backgroundMaterial,
        VolumeProfile profile,
        UnityEngine.UI.Button enterGameButton)
    {
        if (!scene.IsValid() || !scene.isLoaded)
            throw new InvalidDataException("Login flow scene is not loaded.");

        UniversalAdditionalCameraData cameraData =
            camera.GetComponent<UniversalAdditionalCameraData>();
        if (!camera.allowHDR || cameraData == null ||
            !cameraData.renderPostProcessing ||
            cameraData.requiresColorOption != CameraOverrideOption.On)
            throw new InvalidDataException("Camera HDR, post-processing or opaque texture is disabled.");

        ValidateCanvas(loginRoot, camera);
        ValidateCanvas(characterRoot, camera);
        ValidateCanvas(mainHudRoot, camera);

        TMP_InputField[] loginInputs =
            loginRoot.GetComponentsInChildren<TMP_InputField>(true);
        TMP_InputField[] characterInputs =
            characterRoot.GetComponentsInChildren<TMP_InputField>(true);
        int buttonCount = 0;
        int glassPanelCount = 0;
        int softGlowCount = 0;
        int eventSystemCount = 0;
        foreach (GameObject rootObject in scene.GetRootGameObjects())
        {
            buttonCount += rootObject.GetComponentsInChildren<UnityEngine.UI.Button>(true).Length;
            glassPanelCount += rootObject.GetComponentsInChildren<URPFrostedGlassPanel>(true).Length;
            Transform[] transforms = rootObject.GetComponentsInChildren<Transform>(true);
            foreach (Transform transform in transforms)
            {
                if (transform.name.EndsWith("_SoftGlow", StringComparison.Ordinal))
                    softGlowCount++;
            }
            eventSystemCount += rootObject.GetComponentsInChildren<EventSystem>(true).Length;
        }

        if (loginInputs.Length != 2 || characterInputs.Length != 1)
            throw new InvalidDataException("Expected two login inputs and one character-name input.");
        if (buttonCount != 29)
            throw new InvalidDataException("Expected twenty-nine buttons across all three screens.");
        if (glassPanelCount != 37)
            throw new InvalidDataException("Expected thirty-seven runtime glass panels.");
        if (softGlowCount != 0)
            throw new InvalidDataException("Added soft-glow outline layers must not exist.");
        if (eventSystemCount != 1)
            throw new InvalidDataException("Flow scene must contain exactly one EventSystem.");
        if (flow == null || loginRoot.GetComponent<LargeLoginScreenView>() == null ||
            enterGameButton == null)
            throw new InvalidDataException("Login flow controller wiring is incomplete.");
        if (mainHudRoot.transform.Find("Background") != null)
            throw new InvalidDataException("Main HUD must leave the gameplay viewport transparent.");
        if (backgroundMaterial == null || backgroundMaterial.mainTexture == null)
            throw new InvalidDataException("Opaque background sampling material is incomplete.");

        Bloom bloom;
        if (!profile.TryGet(out bloom) || !bloom.active ||
            !bloom.intensity.overrideState || bloom.intensity.value <= 0f)
            throw new InvalidDataException("Bloom is not enabled in the glass lighting profile.");

        Debug.Log(
            "[LoginCharacterFlow] VALIDATION_PASS loginInputs=2 characterInputs=1 " +
            "buttons=29 glassPanels=37 softGlows=0 eventSystems=1 " +
            "hdr=enabled bloom=enabled");
    }

    static void ValidateCanvas(GameObject root, Camera camera)
    {
        Canvas canvas = root.GetComponent<Canvas>();
        if (canvas == null || canvas.renderMode != RenderMode.ScreenSpaceCamera ||
            canvas.worldCamera != camera)
            throw new InvalidDataException(root.name + " is not bound to the flow camera.");

        if (root.GetComponent<UnityEngine.UI.GraphicRaycaster>() == null)
            throw new InvalidDataException(root.name + " is missing GraphicRaycaster.");
    }

    static void EnsureFolders()
    {
        EnsureFolder("Assets", "UI场景测试");
        EnsureFolder(Root, "Scenes");
        EnsureFolder(Root, "Materials");
        EnsureFolder(Root, "Settings");
        EnsureFolder(Root, "Scripts");
    }

    static void EnsureFolder(string parent, string child)
    {
        string path = parent + "/" + child;
        if (!AssetDatabase.IsValidFolder(path))
            AssetDatabase.CreateFolder(parent, child);
    }
}

[InitializeOnLoad]
static class CodexApplyLoginCharacterFlowOnce
{
    const string RequestPath = "Library/CodexLoginCharacterFlow.request";
    const string SuccessPath = "Library/CodexLoginCharacterFlow.success";
    const string FailurePath = "Library/CodexLoginCharacterFlow.failure";

    static CodexApplyLoginCharacterFlowOnce()
    {
        if (File.Exists(RequestPath))
            EditorApplication.delayCall += TryBuild;
    }

    static void TryBuild()
    {
        if (!File.Exists(RequestPath))
            return;

        if (EditorApplication.isCompiling || EditorApplication.isUpdating)
        {
            EditorApplication.delayCall += TryBuild;
            return;
        }

        if (EditorApplication.isPlayingOrWillChangePlaymode)
        {
            EditorApplication.isPlaying = false;
            EditorApplication.delayCall += TryBuild;
            return;
        }

        try
        {
            if (File.Exists(SuccessPath))
                File.Delete(SuccessPath);
            if (File.Exists(FailurePath))
                File.Delete(FailurePath);

            LoginCharacterFlowBuilder.Build();
            File.WriteAllText(
                SuccessPath,
                DateTime.UtcNow.ToString("O") + Environment.NewLine +
                "Assets/UI场景测试/Scenes/LoginCharacterFlow.unity");
            File.Delete(RequestPath);
            Debug.Log("[CodexLoginCharacterFlow] AUTO_BUILD_SUCCESS");
        }
        catch (Exception exception)
        {
            File.WriteAllText(FailurePath, exception.ToString());
            File.Delete(RequestPath);
            Debug.LogException(exception);
        }
    }
}

[InitializeOnLoad]
static class CodexRemoveGlassOutlineOnce
{
    const string RequestPath = "Library/CodexRemoveGlassOutline.request";
    const string SuccessPath = "Library/CodexRemoveGlassOutline.success";
    const string FailurePath = "Library/CodexRemoveGlassOutline.failure";

    static CodexRemoveGlassOutlineOnce()
    {
        if (File.Exists(RequestPath))
            EditorApplication.delayCall += TryRemove;
    }

    static void TryRemove()
    {
        if (!File.Exists(RequestPath))
            return;

        if (EditorApplication.isCompiling || EditorApplication.isUpdating)
        {
            EditorApplication.delayCall += TryRemove;
            return;
        }

        if (EditorApplication.isPlayingOrWillChangePlaymode)
        {
            EditorApplication.isPlaying = false;
            EditorApplication.delayCall += TryRemove;
            return;
        }

        try
        {
            if (File.Exists(SuccessPath))
                File.Delete(SuccessPath);
            if (File.Exists(FailurePath))
                File.Delete(FailurePath);

            LoginCharacterFlowBuilder.RemoveAddedOutlineLayers();
            File.WriteAllText(SuccessPath, DateTime.UtcNow.ToString("O"));
            File.Delete(RequestPath);
            Debug.Log("[CodexRemoveGlassOutline] AUTO_REMOVE_SUCCESS");
        }
        catch (Exception exception)
        {
            File.WriteAllText(FailurePath, exception.ToString());
            File.Delete(RequestPath);
            Debug.LogException(exception);
        }
    }
}
#endif
