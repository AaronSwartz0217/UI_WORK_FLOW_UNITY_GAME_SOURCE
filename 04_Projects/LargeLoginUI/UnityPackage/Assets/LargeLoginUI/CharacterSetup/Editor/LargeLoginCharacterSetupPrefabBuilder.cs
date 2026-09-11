#if UNITY_EDITOR
using System;
using System.IO;
using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.Rendering.Universal;
using UnityEngine.SceneManagement;

namespace LargeLoginUIEditor
{
    public static class LargeLoginCharacterSetupPrefabBuilder
    {
        const string Root = "Assets/LargeLoginUI/CharacterSetup";
        const string Art = Root + "/Art";
        const string Materials = Root + "/Materials";
        const string Prefabs = Root + "/Prefabs";
        const string Scenes = Root + "/Scenes";
        const string PresetPath = "Assets/SHADER/玻璃预设/毛玻璃.json";
        const string ShaderName = "UI/URP Frosted Glass Diffraction";
        const string LoginBackground =
            "Assets/LargeLoginUI/LoginScreen/Art/LargeLogin_Background_Default_1464x828.png";

        const int CanvasWidth = 1464;
        const int CanvasHeight = 828;

        static readonly Vector2 MainPanelSize = new Vector2(1012f, 328f);
        static readonly Vector2 NameInputSize = new Vector2(482f, 50f);
        static readonly Vector2 EquipmentSlotSize = new Vector2(222f, 214f);
        static readonly Vector2 EquipmentCardSize = new Vector2(184f, 164f);
        static readonly Vector2 EnterButtonSize = new Vector2(368f, 72f);

        static readonly Vector2 MainPanelPosition = new Vector2(0f, 152f);
        static readonly Vector2 NameInputPosition = new Vector2(-98f, 278f);
        static readonly Vector2 EquipmentSlotPosition = new Vector2(1f, 122f);
        static readonly Vector2 EnterButtonPosition = new Vector2(1f, -269f);
        static readonly float[] CardX = { -412f, -206f, 0f, 206f, 412f };
        const float CardY = -109f;

        [MenuItem("Tools/Large Login UI/Character Setup/Rebuild")]
        public static void Build()
        {
            EnsureFolders();
            EnsureTmpEssentials();
            EnableOpaqueTexture();

            GlassUIBakerPreset preset = LoadPreset();
            CopyBackground();
            GenerateGlassPngs(preset);
            AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
            ConfigureTextureImporters();

            Shader shader = Shader.Find(ShaderName);
            if (shader == null)
                throw new InvalidOperationException("Missing shader: " + ShaderName);

            Material mainMaterial = CreateGlassMaterial(
                Materials + "/LargeLoginCharacterSetup_GlassMainPanel.mat",
                shader,
                preset,
                MainPanelSize,
                30f,
                new Color(0.68f, 0.56f, 0.40f, preset.fillOpacity));
            Material inputMaterial = CreateGlassMaterial(
                Materials + "/LargeLoginCharacterSetup_GlassNameInput.mat",
                shader,
                preset,
                NameInputSize,
                11f,
                new Color(0.78f, 0.72f, 0.64f, preset.fillOpacity));
            Material slotMaterial = CreateGlassMaterial(
                Materials + "/LargeLoginCharacterSetup_GlassEquipmentSlot.mat",
                shader,
                preset,
                EquipmentSlotSize,
                17f,
                new Color(0.82f, 0.69f, 0.50f, preset.fillOpacity));
            Material cardMaterial = CreateGlassMaterial(
                Materials + "/LargeLoginCharacterSetup_GlassEquipmentCard.mat",
                shader,
                preset,
                EquipmentCardSize,
                15f,
                new Color(0.82f, 0.70f, 0.52f, preset.fillOpacity));
            Material buttonMaterial = CreateGlassMaterial(
                Materials + "/LargeLoginCharacterSetup_GlassEnterButton.mat",
                shader,
                preset,
                EnterButtonSize,
                18f,
                new Color(0.96f, 0.80f, 0.56f, preset.fillOpacity));

            TMP_FontAsset font = AssetDatabase.LoadAssetAtPath<TMP_FontAsset>(
                "Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF.asset");

            GameObject screen = BuildScreen(
                mainMaterial,
                inputMaterial,
                slotMaterial,
                cardMaterial,
                buttonMaterial,
                font);
            string prefabPath = Prefabs + "/LargeLoginCharacterSetup.prefab";
            PrefabUtility.SaveAsPrefabAsset(screen, prefabPath);

            Scene scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            GameObject instance = PrefabUtility.InstantiatePrefab(
                AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath), scene) as GameObject;
            if (instance == null)
                throw new InvalidOperationException("Unable to instantiate generated character setup prefab.");

            GameObject eventSystem = new GameObject(
                "EventSystem",
                typeof(EventSystem),
                typeof(StandaloneInputModule));
            eventSystem.transform.SetAsLastSibling();
            string scenePath = Scenes + "/LargeLoginCharacterSetupPreview.unity";
            EditorSceneManager.SaveScene(scene, scenePath);

            ValidateGeneratedAssets(prefabPath, scene);

            UnityEngine.Object.DestroyImmediate(screen);
            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
            Debug.Log("[LargeLoginCharacterSetup] BUILD_SUCCESS prefab=" + prefabPath +
                      " scene=" + scenePath);
        }

        static void ValidateGeneratedAssets(string prefabPath, Scene previewScene)
        {
            GameObject contents = PrefabUtility.LoadPrefabContents(prefabPath);
            try
            {
                Canvas canvas = contents.GetComponent<Canvas>();
                UnityEngine.UI.CanvasScaler scaler =
                    contents.GetComponent<UnityEngine.UI.CanvasScaler>();
                TMP_InputField[] inputs = contents.GetComponentsInChildren<TMP_InputField>(true);
                UnityEngine.UI.Button[] buttons =
                    contents.GetComponentsInChildren<UnityEngine.UI.Button>(true);
                URPFrostedGlassPanel[] glassPanels =
                    contents.GetComponentsInChildren<URPFrostedGlassPanel>(true);

                Require(canvas != null && canvas.renderMode == RenderMode.ScreenSpaceOverlay,
                    "Prefab requires one Screen Space Overlay Canvas.");
                Require(scaler != null &&
                        scaler.uiScaleMode ==
                        UnityEngine.UI.CanvasScaler.ScaleMode.ScaleWithScreenSize,
                    "CanvasScaler must use Scale With Screen Size.");
                Require(scaler != null &&
                        scaler.referenceResolution == new Vector2(CanvasWidth, CanvasHeight),
                    "CanvasScaler reference resolution is incorrect.");
                Require(inputs.Length == 1, "Prefab must contain one character-name input field.");
                Require(buttons.Length == 6,
                    "Prefab must contain five equipment cards and one enter-game button.");
                Require(glassPanels.Length == 9,
                    "Prefab must contain nine runtime glass surfaces.");
                Require(contents.GetComponentsInChildren<EventSystem>(true).Length == 0,
                    "Portable prefab must not embed an EventSystem.");

                RequireSize(contents.transform.Find("MainPanel"), MainPanelSize);
                RequireSize(contents.transform.Find("NameInput"), NameInputSize);
                RequireSize(contents.transform.Find("CurrentEquipmentSlot"), EquipmentSlotSize);
                RequireSize(contents.transform.Find("EnterGameButton"), EnterButtonSize);

                for (int i = 0; i < 5; i++)
                {
                    Transform card = contents.transform.Find("EquipmentCard" + (i + 1));
                    RequireSize(card, EquipmentCardSize);
                    UnityEngine.UI.Button button = card.GetComponent<UnityEngine.UI.Button>();
                    RequireCompleteSpriteState(button, card.name);
                }

                RequireCompleteSpriteState(
                    contents.transform.Find("EnterGameButton")
                        .GetComponent<UnityEngine.UI.Button>(),
                    "EnterGameButton");

                foreach (URPFrostedGlassPanel panel in glassPanels)
                {
                    UnityEngine.UI.Graphic graphic = panel.GetComponent<UnityEngine.UI.Graphic>();
                    Require(graphic != null && graphic.material != null &&
                            graphic.material.shader.name == ShaderName,
                        panel.name + " is not bound to the glass shader.");
                }
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }

            int eventSystemCount = 0;
            foreach (GameObject root in previewScene.GetRootGameObjects())
                eventSystemCount += root.GetComponentsInChildren<EventSystem>(true).Length;
            Require(eventSystemCount == 1, "Preview scene must contain exactly one EventSystem.");
            Debug.Log(
                "[LargeLoginCharacterSetup] VALIDATION_PASS inputs=1 buttons=6 glassPanels=9 eventSystems=1");
        }

        static void RequireSize(Transform target, Vector2 expected)
        {
            Require(target != null, "Missing required object.");
            RectTransform rect = target.GetComponent<RectTransform>();
            Require(rect != null && rect.sizeDelta == expected,
                target.name + " has an incorrect RectTransform size.");
        }

        static void RequireCompleteSpriteState(UnityEngine.UI.Button button, string label)
        {
            Require(button != null, label + " is missing its Button component.");
            UnityEngine.UI.SpriteState state = button.spriteState;
            Require(state.highlightedSprite != null &&
                    state.pressedSprite != null &&
                    state.selectedSprite != null &&
                    state.disabledSprite != null,
                label + " is missing one or more required sprite states.");
        }

        static void Require(bool condition, string message)
        {
            if (!condition)
                throw new InvalidDataException(message);
        }

        static void EnsureFolders()
        {
            EnsureFolder("Assets", "LargeLoginUI");
            EnsureFolder("Assets/LargeLoginUI", "CharacterSetup");
            EnsureFolder(Root, "Art");
            EnsureFolder(Root, "Materials");
            EnsureFolder(Root, "Prefabs");
            EnsureFolder(Root, "Scenes");
            EnsureFolder(Root, "Scripts");
            EnsureFolder(Root, "Editor");
        }

        static void EnsureFolder(string parent, string child)
        {
            string path = parent + "/" + child;
            if (!AssetDatabase.IsValidFolder(path))
                AssetDatabase.CreateFolder(parent, child);
        }

        static void EnsureTmpEssentials()
        {
            const string settings = "Assets/TextMesh Pro/Resources/TMP Settings.asset";
            if (AssetDatabase.LoadAssetAtPath<TMP_Settings>(settings) != null)
                return;

            TMP_PackageResourceImporter.ImportResources(true, false, false);
            AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
        }

        static void EnableOpaqueTexture()
        {
            string[] guids = AssetDatabase.FindAssets("t:UniversalRenderPipelineAsset");
            foreach (string guid in guids)
            {
                string path = AssetDatabase.GUIDToAssetPath(guid);
                UniversalRenderPipelineAsset asset =
                    AssetDatabase.LoadAssetAtPath<UniversalRenderPipelineAsset>(path);
                if (asset == null || asset.supportsCameraOpaqueTexture)
                    continue;

                asset.supportsCameraOpaqueTexture = true;
                EditorUtility.SetDirty(asset);
            }
        }

        static GlassUIBakerPreset LoadPreset()
        {
            TextAsset json = AssetDatabase.LoadAssetAtPath<TextAsset>(PresetPath);
            if (json == null)
                throw new FileNotFoundException("Required glass preset not found", PresetPath);

            GlassUIBakerPreset preset = JsonUtility.FromJson<GlassUIBakerPreset>(json.text);
            if (preset == null || preset.version != 1)
                throw new InvalidDataException("Unsupported glass preset at " + PresetPath);
            return preset;
        }

        static void CopyBackground()
        {
            string destination = Art +
                "/LargeLogin_CharacterSetupBackground_Default_1464x828.png";
            string projectRoot = Directory.GetParent(Application.dataPath).FullName;
            string sourceFile = Path.Combine(
                projectRoot,
                LoginBackground.Replace('/', Path.DirectorySeparatorChar));
            string destinationFile = Path.Combine(
                projectRoot,
                destination.Replace('/', Path.DirectorySeparatorChar));
            if (!File.Exists(sourceFile))
                throw new FileNotFoundException("Login background source is missing", sourceFile);

            Directory.CreateDirectory(Path.GetDirectoryName(destinationFile));
            File.Copy(sourceFile, destinationFile, true);
        }

        static void GenerateGlassPngs(GlassUIBakerPreset preset)
        {
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupMainPanel_Default_1012x328.png",
                preset,
                1012,
                328,
                30f,
                new Color(0.68f, 0.56f, 0.40f, 1f));
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupNameInput_Default_482x50.png",
                preset,
                482,
                50,
                11f,
                new Color(0.78f, 0.72f, 0.64f, 1f));
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupCurrentEquipmentSlot_Empty_222x214.png",
                preset,
                222,
                214,
                17f,
                new Color(0.82f, 0.69f, 0.50f, 1f));

            WriteCardFamily(preset);
            WriteButtonFamily(preset);
        }

        static void WriteCardFamily(GlassUIBakerPreset preset)
        {
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupEquipmentCard_Normal_184x164.png",
                preset,
                184,
                164,
                15f,
                new Color(0.82f, 0.70f, 0.52f, 1f),
                42);
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupEquipmentCard_Hover_184x164.png",
                preset,
                184,
                164,
                15f,
                new Color(0.96f, 0.82f, 0.61f, 1f),
                42);
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupEquipmentCard_Pressed_184x164.png",
                preset,
                184,
                164,
                15f,
                new Color(0.67f, 0.52f, 0.34f, 1f),
                42);
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupEquipmentCard_Disabled_184x164.png",
                preset,
                184,
                164,
                15f,
                new Color(0.49f, 0.47f, 0.43f, 1f),
                42);
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupEquipmentCard_Selected_184x164.png",
                preset,
                184,
                164,
                15f,
                new Color(1.00f, 0.75f, 0.34f, 1f),
                42);
        }

        static void WriteButtonFamily(GlassUIBakerPreset preset)
        {
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupEnterGameButton_Normal_368x72.png",
                preset,
                368,
                72,
                18f,
                new Color(0.96f, 0.80f, 0.56f, 1f));
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupEnterGameButton_Hover_368x72.png",
                preset,
                368,
                72,
                18f,
                new Color(1.00f, 0.88f, 0.65f, 1f));
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupEnterGameButton_Pressed_368x72.png",
                preset,
                368,
                72,
                18f,
                new Color(0.76f, 0.57f, 0.34f, 1f));
            WriteGlassPng(
                Art + "/LargeLogin_CharacterSetupEnterGameButton_Disabled_368x72.png",
                preset,
                368,
                72,
                18f,
                new Color(0.58f, 0.56f, 0.53f, 1f));
        }

        static void WriteGlassPng(
            string assetPath,
            GlassUIBakerPreset preset,
            int width,
            int height,
            float radius,
            Color tint,
            int footerHeight = 0)
        {
            float clampedRadius = Mathf.Clamp(radius, 0f, height * 0.5f - 2f);
            float border = Mathf.Clamp(preset.borderWidth, 0f, 24f);
            Vector2 center = new Vector2(width * 0.5f, height * 0.5f);
            // The silhouette touches the canvas at the straight edges. Rounded corners
            // remain transparent, but there is no arbitrary transparent padding.
            Vector2 halfSize = center - Vector2.one * 0.5f;
            Color32[] pixels = new Color32[width * height];

            for (int y = 0; y < height; y++)
            {
                float vertical = y / Mathf.Max(1f, height - 1f);
                for (int x = 0; x < width; x++)
                {
                    Vector2 p = new Vector2(x + 0.5f, y + 0.5f) - center;
                    float sdf = RoundedBoxSdf(p, halfSize, clampedRadius);
                    float coverage = Mathf.Clamp01(0.5f - sdf);
                    float borderMask = coverage *
                        (1f - SmoothStep(
                            Mathf.Max(0f, border - 1f),
                            border + 1f,
                            Mathf.Abs(sdf)));
                    float innerEdge = coverage *
                        (1f - SmoothStep(
                            0f,
                            Mathf.Max(clampedRadius * 0.55f, 1f),
                            -sdf));
                    float highlight = (1f - vertical) * innerEdge * preset.topHighlight;
                    float shade = vertical * innerEdge * preset.bottomShade;
                    float horizontal = x / Mathf.Max(1f, width - 1f);
                    float gloss = CalculateGloss(horizontal, vertical, preset) * coverage;
                    float baseAlpha = coverage * preset.fillOpacity;
                    float alpha = Mathf.Max(baseAlpha, borderMask * preset.borderOpacity);
                    alpha = Mathf.Max(baseAlpha * 0.62f,
                        Mathf.Clamp01(alpha + highlight + gloss - shade));

                    Color pixelTint = tint;
                    if (footerHeight > 0 && y < footerHeight)
                    {
                        float footerBlend = Mathf.SmoothStep(
                            footerHeight + 2f,
                            Mathf.Max(0f, footerHeight - 4f),
                            y);
                        pixelTint = Color.Lerp(
                            tint,
                            new Color(tint.r * 0.29f, tint.g * 0.27f, tint.b * 0.23f, 1f),
                            footerBlend);
                        alpha = Mathf.Max(alpha, coverage * 0.54f * footerBlend);
                    }

                    pixels[y * width + x] = alpha <= 0.0001f
                        ? new Color32(0, 0, 0, 0)
                        : (Color32)new Color(pixelTint.r, pixelTint.g, pixelTint.b, alpha);
                }
            }

            Texture2D texture = new Texture2D(width, height, TextureFormat.RGBA32, false, false);
            texture.SetPixels32(pixels);
            texture.Apply(false, false);
            string fullPath = Path.Combine(
                Directory.GetParent(Application.dataPath).FullName,
                assetPath.Replace('/', Path.DirectorySeparatorChar));
            Directory.CreateDirectory(Path.GetDirectoryName(fullPath));
            File.WriteAllBytes(fullPath, texture.EncodeToPNG());
            UnityEngine.Object.DestroyImmediate(texture);
        }

        static float RoundedBoxSdf(Vector2 p, Vector2 halfSize, float radius)
        {
            Vector2 q = new Vector2(Mathf.Abs(p.x), Mathf.Abs(p.y)) -
                        (halfSize - Vector2.one * radius);
            Vector2 outside = new Vector2(Mathf.Max(q.x, 0f), Mathf.Max(q.y, 0f));
            return outside.magnitude + Mathf.Min(Mathf.Max(q.x, q.y), 0f) - radius;
        }

        static float SmoothStep(float a, float b, float value)
        {
            float t = Mathf.Clamp01((value - a) / Mathf.Max(b - a, 0.00001f));
            return t * t * (3f - 2f * t);
        }

        static float CalculateGloss(float u, float v, GlassUIBakerPreset preset)
        {
            float radians = preset.glossAngle * Mathf.Deg2Rad;
            float coordinate = (u - 0.5f) * Mathf.Sin(radians) +
                               (v - 0.5f) * Mathf.Cos(radians) + 0.5f;
            float distance = Mathf.Abs(coordinate - preset.glossPosition);
            float band = 1f - SmoothStep(
                preset.glossWidth * 0.25f,
                preset.glossWidth * 0.5f,
                distance);
            return band * preset.glossIntensity;
        }

        static void ConfigureTextureImporters()
        {
            ConfigureSprite(
                Art + "/LargeLogin_CharacterSetupBackground_Default_1464x828.png",
                false,
                2048);
            ConfigureSprite(
                Art + "/LargeLogin_CharacterSetupMainPanel_Default_1012x328.png",
                true,
                2048);
            ConfigureSprite(
                Art + "/LargeLogin_CharacterSetupNameInput_Default_482x50.png",
                true,
                512);
            ConfigureSprite(
                Art + "/LargeLogin_CharacterSetupCurrentEquipmentSlot_Empty_222x214.png",
                true,
                512);

            foreach (string state in new[] { "Normal", "Hover", "Pressed", "Disabled", "Selected" })
            {
                ConfigureSprite(
                    Art + "/LargeLogin_CharacterSetupEquipmentCard_" + state + "_184x164.png",
                    true,
                    512);
            }

            foreach (string state in new[] { "Normal", "Hover", "Pressed", "Disabled" })
            {
                ConfigureSprite(
                    Art + "/LargeLogin_CharacterSetupEnterGameButton_" + state + "_368x72.png",
                    true,
                    512);
            }
        }

        static void ConfigureSprite(string path, bool alpha, int maxTextureSize)
        {
            TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;
            if (importer == null)
                throw new FileNotFoundException("Sprite source not found", path);

            importer.textureType = TextureImporterType.Sprite;
            importer.spriteImportMode = SpriteImportMode.Single;
            importer.alphaIsTransparency = alpha;
            importer.mipmapEnabled = false;
            importer.wrapMode = TextureWrapMode.Clamp;
            importer.filterMode = FilterMode.Bilinear;
            importer.textureCompression = TextureImporterCompression.Uncompressed;
            importer.maxTextureSize = maxTextureSize;
            importer.spritePixelsPerUnit = 100f;
            importer.SaveAndReimport();
        }

        static Material CreateGlassMaterial(
            string path,
            Shader shader,
            GlassUIBakerPreset preset,
            Vector2 rectSize,
            float cornerRadius,
            Color tint)
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
            material.SetFloat("_Opacity", preset.shaderEffectOpacity);
            material.SetFloat("_MaskThreshold", 0.02f);
            material.SetFloat("_MaskSoftness", 0.035f);
            material.SetFloat("_SpriteOverlay", 0.22f);
            material.SetFloat("_CornerRadius", cornerRadius);
            material.SetFloat("_Inset", 2f);
            material.SetFloat("_BorderWidth", preset.borderWidth);
            material.SetColor("_BorderColor",
                new Color(tint.r, tint.g, tint.b, preset.borderOpacity));
            material.SetFloat("_Refraction", preset.shaderRefraction);
            material.SetFloat("_RefractionEdgeWidth", preset.shaderRefractionEdgeWidth);
            material.SetFloat("_LensStrength", preset.shaderLensStrength);
            material.SetFloat("_LensPower", preset.shaderLensPower);
            material.SetFloat("_Diffraction", preset.shaderDiffraction);
            material.SetFloat("_BlurRadius", preset.shaderBlurRadius);
            material.SetFloat("_BlurStrength", preset.shaderBlurStrength);
            material.SetFloat("_Brightness", 1f);
            material.SetFloat("_Saturation", 1f);
            material.SetFloat("_LuminancePreservation", preset.shaderLuminancePreservation);
            material.SetFloat("_Exposure", preset.shaderExposure);
            material.SetFloat("_ShadowLift", preset.shaderShadowLift);
            material.SetFloat("_TopHighlight", preset.topHighlight);
            material.SetFloat("_BottomShade", preset.bottomShade);
            material.SetVector("_RectSize", new Vector4(rectSize.x, rectSize.y, 0f, 0f));
            EditorUtility.SetDirty(material);
            return material;
        }

        static GameObject BuildScreen(
            Material mainMaterial,
            Material inputMaterial,
            Material slotMaterial,
            Material cardMaterial,
            Material buttonMaterial,
            TMP_FontAsset font)
        {
            GameObject root = new GameObject(
                "LargeLoginCharacterSetup",
                typeof(RectTransform),
                typeof(Canvas),
                typeof(UnityEngine.UI.CanvasScaler),
                typeof(UnityEngine.UI.GraphicRaycaster));
            Canvas canvas = root.GetComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.pixelPerfect = false;

            UnityEngine.UI.CanvasScaler scaler =
                root.GetComponent<UnityEngine.UI.CanvasScaler>();
            scaler.uiScaleMode =
                UnityEngine.UI.CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = new Vector2(CanvasWidth, CanvasHeight);
            scaler.screenMatchMode =
                UnityEngine.UI.CanvasScaler.ScreenMatchMode.MatchWidthOrHeight;
            scaler.matchWidthOrHeight = 0.5f;

            UnityEngine.UI.Image background =
                CreateImage(root.transform, "Background", Vector2.zero, Vector2.zero);
            Stretch(background.rectTransform);
            background.sprite = LoadSprite(
                Art + "/LargeLogin_CharacterSetupBackground_Default_1464x828.png");
            background.preserveAspect = false;
            background.raycastTarget = false;

            UnityEngine.UI.Image mainPanel = CreateGlassImage(
                root.transform,
                "MainPanel",
                MainPanelSize,
                MainPanelPosition,
                Art + "/LargeLogin_CharacterSetupMainPanel_Default_1012x328.png",
                mainMaterial,
                false);

            CreateText(
                mainPanel.transform,
                "NameLabel",
                "角色名称：",
                new Vector2(132f, 50f),
                new Vector2(-440f, 126f),
                font,
                22f,
                TextAlignmentOptions.MidlineRight,
                new Color(1f, 0.96f, 0.90f, 0.96f));

            CreateNameInput(root.transform, inputMaterial, font);

            CreateText(
                mainPanel.transform,
                "CurrentEquipmentLabel",
                "当前装备",
                new Vector2(150f, 50f),
                new Vector2(392f, 126f),
                font,
                22f,
                TextAlignmentOptions.Center,
                new Color(1f, 0.96f, 0.90f, 0.96f));

            CreateGlassImage(
                root.transform,
                "CurrentEquipmentSlot",
                EquipmentSlotSize,
                EquipmentSlotPosition,
                Art + "/LargeLogin_CharacterSetupCurrentEquipmentSlot_Empty_222x214.png",
                slotMaterial,
                false);

            for (int i = 0; i < CardX.Length; i++)
                CreateEquipmentCard(root.transform, i + 1, new Vector2(CardX[i], CardY), cardMaterial, font);

            TMP_Text status = CreateText(
                root.transform,
                "StatusMessage",
                string.Empty,
                new Vector2(620f, 34f),
                new Vector2(0f, -204f),
                font,
                18f,
                TextAlignmentOptions.Center,
                new Color(1f, 0.29f, 0.19f, 1f));
            status.gameObject.SetActive(false);

            CreateEnterButton(root.transform, buttonMaterial, font);
            return root;
        }

        static TMP_InputField CreateNameInput(
            Transform parent,
            Material material,
            TMP_FontAsset font)
        {
            GameObject go = new GameObject(
                "NameInput",
                typeof(RectTransform),
                typeof(CanvasRenderer),
                typeof(UnityEngine.UI.Image),
                typeof(URPFrostedGlassPanel),
                typeof(TMP_InputField));
            go.transform.SetParent(parent, false);
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = NameInputSize;
            rect.anchoredPosition = NameInputPosition;

            UnityEngine.UI.Image image = go.GetComponent<UnityEngine.UI.Image>();
            image.sprite = LoadSprite(
                Art + "/LargeLogin_CharacterSetupNameInput_Default_482x50.png");
            image.material = material;
            image.type = UnityEngine.UI.Image.Type.Simple;

            RectTransform textArea = CreateRect(go.transform, "Text Area", Vector2.zero, Vector2.zero);
            Stretch(textArea, 18f, 8f, 18f, 8f);
            textArea.gameObject.AddComponent<UnityEngine.UI.RectMask2D>();

            TMP_Text placeholder = CreateText(
                textArea,
                "Placeholder",
                "请输入名称",
                Vector2.zero,
                Vector2.zero,
                font,
                19f,
                TextAlignmentOptions.MidlineLeft,
                new Color(1f, 0.96f, 0.90f, 0.52f));
            Stretch(placeholder.rectTransform);

            TMP_Text value = CreateText(
                textArea,
                "Text",
                string.Empty,
                Vector2.zero,
                Vector2.zero,
                font,
                19f,
                TextAlignmentOptions.MidlineLeft,
                new Color(1f, 0.97f, 0.92f, 1f));
            Stretch(value.rectTransform);

            TMP_InputField input = go.GetComponent<TMP_InputField>();
            input.textViewport = textArea;
            input.textComponent = value;
            input.placeholder = placeholder;
            input.contentType = TMP_InputField.ContentType.Standard;
            input.lineType = TMP_InputField.LineType.SingleLine;
            input.characterLimit = 16;
            input.caretColor = new Color(1f, 0.78f, 0.42f, 1f);
            input.selectionColor = new Color(1f, 0.69f, 0.29f, 0.35f);
            return input;
        }

        static UnityEngine.UI.Button CreateEquipmentCard(
            Transform parent,
            int index,
            Vector2 position,
            Material material,
            TMP_FontAsset font)
        {
            GameObject go = new GameObject(
                "EquipmentCard" + index,
                typeof(RectTransform),
                typeof(CanvasRenderer),
                typeof(UnityEngine.UI.Image),
                typeof(URPFrostedGlassPanel),
                typeof(UnityEngine.UI.Button));
            go.transform.SetParent(parent, false);
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = EquipmentCardSize;
            rect.anchoredPosition = position;

            UnityEngine.UI.Image image = go.GetComponent<UnityEngine.UI.Image>();
            image.sprite = LoadSprite(
                Art + "/LargeLogin_CharacterSetupEquipmentCard_Normal_184x164.png");
            image.material = material;
            image.type = UnityEngine.UI.Image.Type.Simple;

            UnityEngine.UI.Button button = go.GetComponent<UnityEngine.UI.Button>();
            button.transition = UnityEngine.UI.Selectable.Transition.SpriteSwap;
            button.spriteState = new UnityEngine.UI.SpriteState
            {
                highlightedSprite = LoadSprite(
                    Art + "/LargeLogin_CharacterSetupEquipmentCard_Hover_184x164.png"),
                pressedSprite = LoadSprite(
                    Art + "/LargeLogin_CharacterSetupEquipmentCard_Pressed_184x164.png"),
                selectedSprite = LoadSprite(
                    Art + "/LargeLogin_CharacterSetupEquipmentCard_Selected_184x164.png"),
                disabledSprite = LoadSprite(
                    Art + "/LargeLogin_CharacterSetupEquipmentCard_Disabled_184x164.png")
            };

            TMP_Text label = CreateText(
                rect,
                "Label",
                "武器名称",
                new Vector2(160f, 34f),
                new Vector2(0f, -61f),
                font,
                18f,
                TextAlignmentOptions.Center,
                new Color(1f, 0.96f, 0.90f, 0.96f));
            label.raycastTarget = false;
            return button;
        }

        static UnityEngine.UI.Button CreateEnterButton(
            Transform parent,
            Material material,
            TMP_FontAsset font)
        {
            GameObject go = new GameObject(
                "EnterGameButton",
                typeof(RectTransform),
                typeof(CanvasRenderer),
                typeof(UnityEngine.UI.Image),
                typeof(URPFrostedGlassPanel),
                typeof(UnityEngine.UI.Button));
            go.transform.SetParent(parent, false);
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = EnterButtonSize;
            rect.anchoredPosition = EnterButtonPosition;

            UnityEngine.UI.Image image = go.GetComponent<UnityEngine.UI.Image>();
            image.sprite = LoadSprite(
                Art + "/LargeLogin_CharacterSetupEnterGameButton_Normal_368x72.png");
            image.material = material;
            image.type = UnityEngine.UI.Image.Type.Simple;

            UnityEngine.UI.Button button = go.GetComponent<UnityEngine.UI.Button>();
            button.transition = UnityEngine.UI.Selectable.Transition.SpriteSwap;
            button.spriteState = new UnityEngine.UI.SpriteState
            {
                highlightedSprite = LoadSprite(
                    Art + "/LargeLogin_CharacterSetupEnterGameButton_Hover_368x72.png"),
                pressedSprite = LoadSprite(
                    Art + "/LargeLogin_CharacterSetupEnterGameButton_Pressed_368x72.png"),
                selectedSprite = LoadSprite(
                    Art + "/LargeLogin_CharacterSetupEnterGameButton_Hover_368x72.png"),
                disabledSprite = LoadSprite(
                    Art + "/LargeLogin_CharacterSetupEnterGameButton_Disabled_368x72.png")
            };

            TMP_Text label = CreateText(
                rect,
                "Label",
                "进入游戏",
                Vector2.zero,
                Vector2.zero,
                font,
                22f,
                TextAlignmentOptions.Center,
                new Color(0.16f, 0.11f, 0.065f, 0.96f));
            Stretch(label.rectTransform);
            label.raycastTarget = false;
            return button;
        }

        static UnityEngine.UI.Image CreateGlassImage(
            Transform parent,
            string name,
            Vector2 size,
            Vector2 position,
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
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = size;
            rect.anchoredPosition = position;
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
            Vector2 size,
            Vector2 position)
        {
            GameObject go = new GameObject(
                name,
                typeof(RectTransform),
                typeof(CanvasRenderer),
                typeof(UnityEngine.UI.Image));
            go.transform.SetParent(parent, false);
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = size;
            rect.anchoredPosition = position;
            return go.GetComponent<UnityEngine.UI.Image>();
        }

        static TMP_Text CreateText(
            Transform parent,
            string name,
            string value,
            Vector2 size,
            Vector2 position,
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
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = size;
            rect.anchoredPosition = position;

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

        static RectTransform CreateRect(
            Transform parent,
            string name,
            Vector2 size,
            Vector2 position)
        {
            GameObject go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(parent, false);
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = size;
            rect.anchoredPosition = position;
            return rect;
        }

        static void Stretch(
            RectTransform rect,
            float left = 0f,
            float bottom = 0f,
            float right = 0f,
            float top = 0f)
        {
            rect.anchorMin = Vector2.zero;
            rect.anchorMax = Vector2.one;
            rect.offsetMin = new Vector2(left, bottom);
            rect.offsetMax = new Vector2(-right, -top);
        }

        static Sprite LoadSprite(string path)
        {
            Sprite sprite = AssetDatabase.LoadAssetAtPath<Sprite>(path);
            if (sprite == null)
                throw new FileNotFoundException("Sprite not imported", path);
            return sprite;
        }
    }
}
#endif
