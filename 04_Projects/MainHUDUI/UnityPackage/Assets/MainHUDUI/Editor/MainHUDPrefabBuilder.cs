#if UNITY_EDITOR
using System;
using System.Collections.Generic;
using System.IO;
using TMPro;
using UnityEditor;
using UnityEngine;

public static class MainHUDPrefabBuilder
{
    public const string PrefabPath = "Assets/MainHUDUI/Prefabs/MainHUD.prefab";

    const string Root = "Assets/MainHUDUI";
    const string Art = Root + "/Art";
    const string Config = Root + "/Config/MainHUD_FrostedGlassPreset.json";
    const string Materials = Root + "/Materials";
    const string FontPath =
        "Assets/LargeLoginUI/Shared/Fonts/SourceHanSansSC-DynamicSDF.asset";
    const string GlassShaderName = "UI/URP Frosted Glass Diffraction";
    const float CanvasWidth = 1559f;
    const float CanvasHeight = 880f;

    static readonly string[] HotbarKeys =
    {
        "1", "2", "3", "Q", "W", "E", "R", "T", "D", "F", "Z", "X", "C"
    };

    static readonly int[] HotbarX =
    {
        315, 372, 429, 496, 553, 609, 666, 722, 779, 835, 891, 948, 1004
    };

    [MenuItem("Tools/UI Scene Test/Rebuild Main HUD Prefab")]
    public static GameObject BuildPrefab()
    {
        EnsureFolders();
        AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
        ConfigureSprites();

        GlassUIBakerPreset preset = LoadPreset();
        Shader shader = Shader.Find(GlassShaderName);
        if (shader == null)
            throw new InvalidOperationException("Required frosted-glass shader is missing: " + GlassShaderName);

        Material panelMaterial = CreateGlassMaterial(
            Materials + "/MainHUD_GlassPanel.mat",
            shader,
            preset,
            new Color(0.12f, 0.25f, 0.36f, 0.15f),
            0.08f,
            0.13f);
        Material buttonMaterial = CreateGlassMaterial(
            Materials + "/MainHUD_GlassButton.mat",
            shader,
            preset,
            new Color(0.39f, 0.56f, 0.72f, 0.11f),
            0.07f,
            0.16f);
        Material slotMaterial = CreateGlassMaterial(
            Materials + "/MainHUD_GlassSlot.mat",
            shader,
            preset,
            new Color(0.10f, 0.23f, 0.34f, 0.12f),
            0.06f,
            0.14f);

        TMP_FontAsset font = AssetDatabase.LoadAssetAtPath<TMP_FontAsset>(FontPath);
        if (font == null)
            throw new FileNotFoundException("CJK TMP font is missing", FontPath);

        GameObject root = BuildHierarchy(panelMaterial, buttonMaterial, slotMaterial, font);
        GameObject prefab = PrefabUtility.SaveAsPrefabAsset(root, PrefabPath);
        UnityEngine.Object.DestroyImmediate(root);
        if (prefab == null)
            throw new InvalidDataException("Unable to save Main HUD prefab.");

        ValidatePrefab(prefab);
        AssetDatabase.SaveAssets();
        Debug.Log(
            "[MainHUD] PREFAB_BUILD_PASS path=" + PrefabPath +
            " canvas=1559x880 buttons=21 fullscreenBackground=none edgeGlow=0");
        return prefab;
    }

    static GameObject BuildHierarchy(
        Material panelMaterial,
        Material buttonMaterial,
        Material slotMaterial,
        TMP_FontAsset font)
    {
        GameObject root = new GameObject(
            "MainHUD",
            typeof(RectTransform),
            typeof(Canvas),
            typeof(UnityEngine.UI.CanvasScaler),
            typeof(UnityEngine.UI.GraphicRaycaster),
            typeof(CanvasGroup));

        Canvas canvas = root.GetComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.pixelPerfect = false;

        UnityEngine.UI.CanvasScaler scaler =
            root.GetComponent<UnityEngine.UI.CanvasScaler>();
        scaler.uiScaleMode = UnityEngine.UI.CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(CanvasWidth, CanvasHeight);
        scaler.screenMatchMode =
            UnityEngine.UI.CanvasScaler.ScreenMatchMode.MatchWidthOrHeight;
        scaler.matchWidthOrHeight = 0.5f;

        CreateGlassImage(root.transform, "LowerHUDPlate", Rect(15, 594, 1253, 282),
            SpritePath("LowerHUDPlate", "Default", 1253, 282), panelMaterial, false);

        CreateButton(root.transform, "ExpandArrowButton", Rect(15, 15, 79, 39),
            "ExpandArrowButton", 79, 39, string.Empty, buttonMaterial, font, 18f);
        CreateButton(root.transform, "TeamInviteButton", Rect(909, 31, 69, 21),
            "TeamInviteButton", 69, 21, "邀请组队", buttonMaterial, font, 12f);
        CreateButton(root.transform, "ModeDropdownButton", Rect(1279, 15, 84, 40),
            "ModeDropdownButton", 84, 40, "普杀", buttonMaterial, font, 17f);
        CreateButton(root.transform, "GMToolsButton", Rect(1372, 15, 80, 39),
            "GMToolsButton", 80, 39, "GM工具", buttonMaterial, font, 16f);
        CreateButton(root.transform, "MenuButton", Rect(1462, 15, 80, 39),
            "MenuButton", 80, 39, "菜单", buttonMaterial, font, 17f);

        CreateText(root.transform, "PartyName", "队伍名称", Rect(15, 56, 82, 16),
            font, 11f, TextAlignmentOptions.MidlineLeft, new Color(0.93f, 0.97f, 1f, 0.96f));
        CreateImage(root.transform, "PartyHealthFill", Rect(15, 72, 75, 12),
            SpritePath("PartyHealthFill", "Default", 75, 12), false);
        CreateImage(root.transform, "PartyManaFill", Rect(15, 86, 75, 4),
            SpritePath("PartyManaFill", "Default", 75, 4), false);

        CreateText(root.transform, "PlayerName", "Name", Rect(704, 31, 150, 21),
            font, 17f, TextAlignmentOptions.Center, Color.white);
        CreateImage(root.transform, "PlayerHealthTrack", Rect(576, 53, 406, 20),
            SpritePath("PlayerHealthTrack", "Default", 406, 20), false);
        CreateImage(root.transform, "PlayerHealthFill", Rect(577, 54, 162, 17),
            SpritePath("PlayerHealthFill", "Default", 162, 17), false);
        CreateText(root.transform, "PlayerHealthValue", "9999", Rect(739, 54, 243, 17),
            font, 11f, TextAlignmentOptions.Center, new Color(0.22f, 0.25f, 0.29f, 0.95f));

        CreateImage(root.transform, "LoadingTrack", Rect(576, 696, 405, 18),
            SpritePath("LoadingTrack", "Default", 405, 18), false);
        CreateImage(root.transform, "LoadingFill", Rect(577, 697, 119, 16),
            SpritePath("LoadingFill", "Default", 119, 16), false);
        CreateText(root.transform, "LoadingLabel", "加载中…", Rect(696, 697, 285, 16),
            font, 11f, TextAlignmentOptions.Center, new Color(0.94f, 0.97f, 1f, 0.96f));

        CreateImage(root.transform, "MutationTrack", Rect(496, 722, 566, 17),
            SpritePath("MutationTrack", "Default", 566, 17), false);
        CreateImage(root.transform, "MutationFill", Rect(497, 723, 486, 15),
            SpritePath("MutationFill", "Default", 486, 15), false);
        CreateText(root.transform, "MutationLabel", "异化中…", Rect(497, 723, 565, 15),
            font, 10f, TextAlignmentOptions.Center, new Color(0.96f, 0.97f, 1f, 0.96f));

        CreateImage(root.transform, "ResourceTrack", Rect(455, 782, 646, 21),
            SpritePath("ResourceTrack", "Default", 646, 21), false);
        CreateImage(root.transform, "ResourceHealthFill", Rect(456, 782, 344, 20),
            SpritePath("ResourceHealthFill", "Default", 344, 20), false);
        CreateImage(root.transform, "ResourceManaFill", Rect(800, 782, 301, 20),
            SpritePath("ResourceManaFill", "Default", 301, 20), false);
        CreateText(root.transform, "HealthValue", "100/100", Rect(640, 782, 160, 20),
            font, 11f, TextAlignmentOptions.Center, new Color(0.08f, 0.34f, 0.09f, 0.95f));
        CreateText(root.transform, "ManaValue", "100/100", Rect(800, 782, 160, 20),
            font, 11f, TextAlignmentOptions.Center, new Color(0.04f, 0.21f, 0.50f, 0.95f));

        for (int index = 0; index < HotbarX.Length; index++)
        {
            UnityEngine.UI.Button button = CreateButton(
                root.transform,
                "HotbarSlot" + (index + 1),
                Rect(HotbarX[index], 809, 56, 56),
                "HotbarSlot",
                56,
                56,
                HotbarKeys[index],
                slotMaterial,
                font,
                13f);
            button.targetGraphic.raycastTarget = true;
        }

        CreateButton(root.transform, "MutationButton", Rect(1073, 809, 56, 56),
            "MutationButton", 56, 56, "异化", buttonMaterial, font, 14f);

        CreateGlassImage(root.transform, "MinimapMeterTrack", Rect(1268, 586, 23, 242),
            SpritePath("MinimapMeterTrack", "Default", 23, 242), panelMaterial, false);
        CreateImage(root.transform, "MinimapMeterWarningFill", Rect(1268, 586, 23, 81),
            SpritePath("MinimapMeterWarningFill", "Default", 23, 81), false);
        CreateImage(root.transform, "MinimapMeterDangerFill", Rect(1268, 667, 23, 161),
            SpritePath("MinimapMeterDangerFill", "Default", 23, 161), false);
        CreateGlassImage(root.transform, "MinimapPanel", Rect(1303, 586, 239, 243),
            SpritePath("MinimapPanel", "Default", 239, 243), panelMaterial, false);
        CreateText(root.transform, "MinimapCoordinates", "(-999,-999)", Rect(1368, 693, 108, 25),
            font, 14f, TextAlignmentOptions.Center, new Color(0.96f, 0.97f, 1f, 0.94f));
        CreateText(root.transform, "CoordinateLabel", "坐标位置：(—,—)", Rect(1400, 797, 138, 25),
            font, 12f, TextAlignmentOptions.MidlineRight, new Color(0.93f, 0.96f, 1f, 0.90f));
        CreateButton(root.transform, "ReturnCityButton", Rect(1306, 793, 62, 29),
            "ReturnCityButton", 62, 29, "回城", buttonMaterial, font, 14f);

        CreateImage(root.transform, "CurrencyIconLeft", Rect(1268, 836, 29, 29),
            SpritePath("CurrencyIconLeft", "Default", 29, 29), false);
        CreateImage(root.transform, "CurrencyPlateLeft", Rect(1305, 836, 64, 29),
            SpritePath("CurrencyPlateLeft", "Default", 64, 29), false);
        CreateText(root.transform, "CurrencyValueLeft", "9999", Rect(1305, 836, 64, 29),
            font, 14f, TextAlignmentOptions.Center, Color.white);
        CreateImage(root.transform, "CurrencyIconRight", Rect(1377, 836, 28, 29),
            SpritePath("CurrencyIconRight", "Default", 28, 29), false);
        CreateImage(root.transform, "CurrencyPlateRight", Rect(1412, 836, 69, 29),
            SpritePath("CurrencyPlateRight", "Default", 69, 29), false);
        CreateText(root.transform, "CurrencyValueRight", "9999", Rect(1412, 836, 69, 29),
            font, 14f, TextAlignmentOptions.Center, Color.white);
        CreateButton(root.transform, "RechargeButton", Rect(1487, 838, 54, 25),
            "RechargeButton", 54, 25, "充值", buttonMaterial, font, 13f);

        return root;
    }

    static UnityEngine.UI.Button CreateButton(
        Transform parent,
        string name,
        Vector4 rect,
        string family,
        int width,
        int height,
        string label,
        Material material,
        TMP_FontAsset font,
        float fontSize)
    {
        GameObject go = new GameObject(
            name,
            typeof(RectTransform),
            typeof(CanvasRenderer),
            typeof(UnityEngine.UI.Image),
            typeof(URPFrostedGlassPanel),
            typeof(UnityEngine.UI.Button));
        go.transform.SetParent(parent, false);
        Place(go.GetComponent<RectTransform>(), rect);

        UnityEngine.UI.Image image = go.GetComponent<UnityEngine.UI.Image>();
        image.sprite = LoadSprite(SpritePath(family, "Normal", width, height));
        image.material = material;
        image.type = UnityEngine.UI.Image.Type.Simple;
        image.raycastTarget = true;

        UnityEngine.UI.Button button = go.GetComponent<UnityEngine.UI.Button>();
        button.transition = UnityEngine.UI.Selectable.Transition.SpriteSwap;
        button.spriteState = new UnityEngine.UI.SpriteState
        {
            highlightedSprite = LoadSprite(SpritePath(family, "Hover", width, height)),
            pressedSprite = LoadSprite(SpritePath(family, "Pressed", width, height)),
            selectedSprite = LoadSprite(SpritePath(family, "Hover", width, height)),
            disabledSprite = LoadSprite(SpritePath(family, "Disabled", width, height))
        };

        if (!string.IsNullOrEmpty(label))
        {
            TMP_Text text = CreateText(
                go.transform,
                "Label",
                label,
                new Vector4(0f, 0f, width, height),
                font,
                fontSize,
                TextAlignmentOptions.Center,
                family == "MutationButton"
                    ? new Color(1f, 0.91f, 0.90f, 0.98f)
                    : new Color(0.96f, 0.98f, 1f, 0.98f));
            text.rectTransform.anchorMin = Vector2.zero;
            text.rectTransform.anchorMax = Vector2.one;
            text.rectTransform.pivot = new Vector2(0.5f, 0.5f);
            text.rectTransform.offsetMin = Vector2.zero;
            text.rectTransform.offsetMax = Vector2.zero;
            text.raycastTarget = false;
        }
        return button;
    }

    static UnityEngine.UI.Image CreateGlassImage(
        Transform parent,
        string name,
        Vector4 rect,
        string spritePath,
        Material material,
        bool raycastTarget)
    {
        GameObject go = new GameObject(
            name,
            typeof(RectTransform),
            typeof(CanvasRenderer),
            typeof(UnityEngine.UI.Image),
            typeof(URPFrostedGlassPanel));
        go.transform.SetParent(parent, false);
        Place(go.GetComponent<RectTransform>(), rect);
        UnityEngine.UI.Image image = go.GetComponent<UnityEngine.UI.Image>();
        image.sprite = LoadSprite(spritePath);
        image.material = material;
        image.type = UnityEngine.UI.Image.Type.Simple;
        image.raycastTarget = raycastTarget;
        return image;
    }

    static UnityEngine.UI.Image CreateImage(
        Transform parent,
        string name,
        Vector4 rect,
        string spritePath,
        bool raycastTarget)
    {
        GameObject go = new GameObject(
            name,
            typeof(RectTransform),
            typeof(CanvasRenderer),
            typeof(UnityEngine.UI.Image));
        go.transform.SetParent(parent, false);
        Place(go.GetComponent<RectTransform>(), rect);
        UnityEngine.UI.Image image = go.GetComponent<UnityEngine.UI.Image>();
        image.sprite = LoadSprite(spritePath);
        image.type = UnityEngine.UI.Image.Type.Simple;
        image.raycastTarget = raycastTarget;
        return image;
    }

    static TMP_Text CreateText(
        Transform parent,
        string name,
        string value,
        Vector4 rect,
        TMP_FontAsset font,
        float fontSize,
        TextAlignmentOptions alignment,
        Color color)
    {
        GameObject go = new GameObject(
            name,
            typeof(RectTransform),
            typeof(CanvasRenderer),
            typeof(TextMeshProUGUI));
        go.transform.SetParent(parent, false);
        Place(go.GetComponent<RectTransform>(), rect);
        TextMeshProUGUI text = go.GetComponent<TextMeshProUGUI>();
        text.text = value;
        text.font = font;
        text.fontSize = fontSize;
        text.alignment = alignment;
        text.color = color;
        text.enableWordWrapping = false;
        text.overflowMode = TextOverflowModes.Ellipsis;
        text.raycastTarget = false;
        return text;
    }

    static void Place(RectTransform transform, Vector4 rect)
    {
        float x = rect.x;
        float y = rect.y;
        float width = rect.z;
        float height = rect.w;
        transform.anchorMin = new Vector2(0.5f, 0.5f);
        transform.anchorMax = new Vector2(0.5f, 0.5f);
        transform.pivot = new Vector2(0.5f, 0.5f);
        transform.sizeDelta = new Vector2(width, height);
        transform.anchoredPosition = new Vector2(
            x + width * 0.5f - CanvasWidth * 0.5f,
            CanvasHeight * 0.5f - y - height * 0.5f);
    }

    static Vector4 Rect(float x, float y, float width, float height)
    {
        return new Vector4(x, y, width, height);
    }

    static string SpritePath(string family, string state, int width, int height)
    {
        return Art + "/MainHUD_" + family + "_" + state + "_" + width + "x" + height + ".png";
    }

    static Sprite LoadSprite(string path)
    {
        Sprite sprite = AssetDatabase.LoadAssetAtPath<Sprite>(path);
        if (sprite == null)
            throw new FileNotFoundException("HUD sprite is missing", path);
        return sprite;
    }

    static GlassUIBakerPreset LoadPreset()
    {
        string absolute = Path.Combine(Directory.GetCurrentDirectory(), Config);
        if (!File.Exists(absolute))
            throw new FileNotFoundException("Frosted-glass preset is missing", absolute);
        GlassUIBakerPreset preset = JsonUtility.FromJson<GlassUIBakerPreset>(File.ReadAllText(absolute));
        if (preset == null)
            throw new InvalidDataException("Unable to parse frosted-glass preset: " + Config);
        return preset;
    }

    static Material CreateGlassMaterial(
        string path,
        Shader shader,
        GlassUIBakerPreset preset,
        Color tint,
        float spriteOverlay,
        float outputAlpha)
    {
        Material material = AssetDatabase.LoadAssetAtPath<Material>(path);
        if (material == null)
        {
            material = new Material(shader);
            AssetDatabase.CreateAsset(material, path);
        }
        else
        {
            material.shader = shader;
        }

        material.SetColor("_TintColor", tint);
        material.SetFloat("_Opacity", Mathf.Min(preset.shaderEffectOpacity, 0.78f));
        material.SetFloat("_OutputAlpha", outputAlpha);
        material.SetFloat("_MaskThreshold", 0.02f);
        material.SetFloat("_MaskSoftness", 0.035f);
        material.SetFloat("_SpriteOverlay", spriteOverlay);
        material.SetFloat("_CornerRadius", 7f);
        material.SetFloat("_Inset", 1f);
        material.SetFloat("_BorderWidth", 0f);
        material.SetColor("_BorderColor", new Color(tint.r, tint.g, tint.b, 0f));
        material.SetFloat("_Refraction", preset.shaderRefraction);
        material.SetFloat("_RefractionEdgeWidth", preset.shaderRefractionEdgeWidth);
        material.SetFloat("_LensStrength", preset.shaderLensStrength);
        material.SetFloat("_LensPower", preset.shaderLensPower);
        material.SetFloat("_Diffraction", preset.shaderDiffraction);
        material.SetFloat("_BlurRadius", preset.shaderBlurRadius);
        material.SetFloat("_BlurStrength", Mathf.Min(preset.shaderBlurStrength, 0.82f));
        material.SetFloat("_Brightness", 1f);
        material.SetFloat("_Saturation", 1f);
        material.SetFloat("_LuminancePreservation", preset.shaderLuminancePreservation);
        material.SetFloat("_Exposure", 1.20f);
        material.SetFloat("_ShadowLift", Mathf.Min(preset.shaderShadowLift, 0.10f));
        material.SetFloat("_TopHighlight", Mathf.Min(preset.topHighlight, 0.20f));
        material.SetFloat("_BottomShade", Mathf.Min(preset.bottomShade, 0.16f));
        material.SetFloat("_EdgeGlow", 0f);
        material.SetFloat("_EdgeGlowWidth", 1f);
        material.SetColor("_EdgeGlowColor", new Color(1f, 1f, 1f, 0f));
        material.SetFloat("_SpecularSheen", 0.13f);
        EditorUtility.SetDirty(material);
        return material;
    }

    static void ConfigureSprites()
    {
        string[] guids = AssetDatabase.FindAssets("t:Texture2D", new[] { Art });
        if (guids.Length != 57)
            throw new InvalidDataException("Expected 57 Main HUD PNG assets, found " + guids.Length + ".");

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;
            if (importer == null)
                throw new InvalidDataException("Texture importer is unavailable: " + path);
            importer.textureType = TextureImporterType.Sprite;
            importer.spriteImportMode = SpriteImportMode.Single;
            importer.alphaIsTransparency = true;
            importer.mipmapEnabled = false;
            importer.wrapMode = TextureWrapMode.Clamp;
            importer.filterMode = FilterMode.Bilinear;
            importer.textureCompression = TextureImporterCompression.Uncompressed;
            importer.maxTextureSize = 2048;
            importer.spritePixelsPerUnit = 100f;
            importer.SaveAndReimport();
        }
    }

    static void ValidatePrefab(GameObject prefab)
    {
        if (prefab.GetComponent<Canvas>() == null ||
            prefab.GetComponent<UnityEngine.UI.GraphicRaycaster>() == null ||
            prefab.GetComponent<CanvasGroup>() == null)
            throw new InvalidDataException("Main HUD root UI components are incomplete.");

        UnityEngine.UI.Button[] buttons =
            prefab.GetComponentsInChildren<UnityEngine.UI.Button>(true);
        URPFrostedGlassPanel[] glassPanels =
            prefab.GetComponentsInChildren<URPFrostedGlassPanel>(true);
        if (buttons.Length != 21)
            throw new InvalidDataException("Expected 21 Main HUD buttons, found " + buttons.Length + ".");
        if (glassPanels.Length != 24)
            throw new InvalidDataException("Expected 24 Main HUD glass panels, found " + glassPanels.Length + ".");
        if (prefab.transform.Find("Background") != null)
            throw new InvalidDataException("Main HUD must not include a full-screen background.");

        foreach (UnityEngine.UI.Button button in buttons)
        {
            UnityEngine.UI.SpriteState state = button.spriteState;
            if (button.transition != UnityEngine.UI.Selectable.Transition.SpriteSwap ||
                state.highlightedSprite == null || state.pressedSprite == null ||
                state.disabledSprite == null)
                throw new InvalidDataException(button.name + " is missing a complete sprite state group.");
        }
    }

    static void EnsureFolders()
    {
        EnsureFolder("Assets", "MainHUDUI");
        EnsureFolder(Root, "Art");
        EnsureFolder(Root, "Config");
        EnsureFolder(Root, "Editor");
        EnsureFolder(Root, "Materials");
        EnsureFolder(Root, "Prefabs");
    }

    static void EnsureFolder(string parent, string child)
    {
        string path = parent + "/" + child;
        if (!AssetDatabase.IsValidFolder(path))
            AssetDatabase.CreateFolder(parent, child);
    }
}
#endif
