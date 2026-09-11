#if UNITY_EDITOR
using System;
using System.IO;
using LargeLoginUI;
using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.Rendering.Universal;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

namespace LargeLoginUIEditor
{
    public static class LargeLoginPrefabBuilder
    {
        const string Root = "Assets/LargeLoginUI/LoginScreen";
        const string Art = Root + "/Art";
        const string Materials = Root + "/Materials";
        const string Prefabs = Root + "/Prefabs";
        const string Scenes = Root + "/Scenes";
        const string PresetPath = "Assets/SHADER/玻璃预设/毛玻璃.json";
        const string ShaderName = "UI/URP Frosted Glass Diffraction";
        const int CanvasWidth = 1464;
        const int CanvasHeight = 828;
        static readonly Vector2 ControlSize = new Vector2(312f, 56f);

        [MenuItem("Tools/Large Login UI/Login Screen/Rebuild")]
        public static void Build()
        {
            EnsureFolders();
            EnsureTmpEssentials();
            EnableOpaqueTexture();

            GlassUIBakerPreset preset = LoadPreset();
            GenerateGlassPngs(preset);
            AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
            ConfigureTextureImporters();

            Shader shader = Shader.Find(ShaderName);
            if (shader == null)
                throw new InvalidOperationException("Missing shader: " + ShaderName);

            Material inputMaterial = CreateGlassMaterial(
                Materials + "/LargeLogin_GlassInput.mat",
                shader,
                preset,
                new Color(0.78f, 0.72f, 0.64f, preset.fillOpacity));
            Material buttonMaterial = CreateGlassMaterial(
                Materials + "/LargeLogin_GlassButton.mat",
                shader,
                preset,
                new Color(0.96f, 0.80f, 0.56f, preset.fillOpacity));

            TMP_FontAsset font = AssetDatabase.LoadAssetAtPath<TMP_FontAsset>(
                "Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF.asset");

            GameObject screen = BuildScreen(inputMaterial, buttonMaterial, font);
            string prefabPath = Prefabs + "/LargeLoginScreen.prefab";
            PrefabUtility.SaveAsPrefabAsset(screen, prefabPath);

            Scene scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            GameObject instance = PrefabUtility.InstantiatePrefab(
                AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath), scene) as GameObject;
            if (instance == null)
                throw new InvalidOperationException("Unable to instantiate generated prefab.");

            GameObject eventSystem = new GameObject(
                "EventSystem",
                typeof(EventSystem),
                typeof(StandaloneInputModule));
            eventSystem.transform.SetAsLastSibling();
            EditorSceneManager.SaveScene(scene, Scenes + "/LargeLoginPreview.unity");

            ValidateGeneratedAssets(prefabPath, scene);

            UnityEngine.Object.DestroyImmediate(screen);
            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
            Debug.Log("[LargeLoginUI] BUILD_SUCCESS prefab=" + prefabPath +
                      " scene=" + Scenes + "/LargeLoginPreview.unity");
        }

        static void ValidateGeneratedAssets(string prefabPath, Scene previewScene)
        {
            GameObject contents = PrefabUtility.LoadPrefabContents(prefabPath);
            try
            {
                Canvas canvas = contents.GetComponent<Canvas>();
                CanvasScaler scaler = contents.GetComponent<CanvasScaler>();
                TMP_InputField[] inputs = contents.GetComponentsInChildren<TMP_InputField>(true);
                Button[] buttons = contents.GetComponentsInChildren<Button>(true);
                URPFrostedGlassPanel[] glassPanels =
                    contents.GetComponentsInChildren<URPFrostedGlassPanel>(true);

                Require(canvas != null && canvas.renderMode == RenderMode.ScreenSpaceOverlay,
                    "Prefab requires one Screen Space Overlay Canvas.");
                Require(scaler != null && scaler.uiScaleMode == CanvasScaler.ScaleMode.ScaleWithScreenSize,
                    "CanvasScaler must use Scale With Screen Size.");
                Require(scaler != null && scaler.referenceResolution == new Vector2(CanvasWidth, CanvasHeight),
                    "CanvasScaler reference resolution is incorrect.");
                Require(inputs.Length == 2, "Prefab must contain two TMP input fields.");
                Require(buttons.Length == 2, "Prefab must contain two action buttons.");
                Require(glassPanels.Length == 4, "All four controls must use runtime glass panels.");
                Require(contents.GetComponentsInChildren<EventSystem>(true).Length == 0,
                    "Portable prefab must not embed an EventSystem.");
                Require(inputs[1].contentType == TMP_InputField.ContentType.Password,
                    "Password field must mask its value.");

                foreach (TMP_InputField input in inputs)
                {
                    RectTransform rect = input.GetComponent<RectTransform>();
                    Image image = input.GetComponent<Image>();
                    Require(rect != null && rect.sizeDelta == ControlSize,
                        input.name + " has an incorrect RectTransform size.");
                    Require(image != null && image.material != null &&
                            image.material.shader.name == ShaderName,
                        input.name + " is not bound to the glass shader.");
                }

                foreach (Button button in buttons)
                {
                    RectTransform rect = button.GetComponent<RectTransform>();
                    Image image = button.GetComponent<Image>();
                    SpriteState state = button.spriteState;
                    Require(rect != null && rect.sizeDelta == ControlSize,
                        button.name + " has an incorrect RectTransform size.");
                    Require(image != null && image.material != null &&
                            image.material.shader.name == ShaderName,
                        button.name + " is not bound to the glass shader.");
                    Require(state.highlightedSprite != null && state.pressedSprite != null &&
                            state.disabledSprite != null,
                        button.name + " is missing one or more sprite states.");
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
            Debug.Log("[LargeLoginUI] VALIDATION_PASS inputs=2 buttons=2 glassPanels=4 eventSystems=1");
        }

        static void Require(bool condition, string message)
        {
            if (!condition)
                throw new InvalidDataException(message);
        }

        static void EnsureFolders()
        {
            EnsureFolder("Assets", "LargeLoginUI");
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
                UniversalRenderPipelineAsset asset = AssetDatabase.LoadAssetAtPath<UniversalRenderPipelineAsset>(path);
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

        static void GenerateGlassPngs(GlassUIBakerPreset preset)
        {
            WriteGlassPng(
                Art + "/LargeLogin_InputField_Default_312x56.png",
                preset,
                new Color(0.78f, 0.72f, 0.64f, 1f));

            WriteGlassPng(
                Art + "/LargeLogin_ActionButton_Normal_312x56.png",
                preset,
                new Color(0.96f, 0.80f, 0.56f, 1f));
            WriteGlassPng(
                Art + "/LargeLogin_ActionButton_Hover_312x56.png",
                preset,
                new Color(1.00f, 0.88f, 0.65f, 1f));
            WriteGlassPng(
                Art + "/LargeLogin_ActionButton_Pressed_312x56.png",
                preset,
                new Color(0.76f, 0.57f, 0.34f, 1f));
            WriteGlassPng(
                Art + "/LargeLogin_ActionButton_Disabled_312x56.png",
                preset,
                new Color(0.58f, 0.56f, 0.53f, 1f));
        }

        static void WriteGlassPng(string assetPath, GlassUIBakerPreset preset, Color tint)
        {
            const int width = 312;
            const int height = 56;
            float radius = Mathf.Clamp(
                preset.cornerRadius * height / Mathf.Max(1f, preset.outputHeight),
                0f,
                height * 0.5f - 2f);
            float border = Mathf.Clamp(preset.borderWidth, 0f, 24f);
            Vector2 center = new Vector2(width * 0.5f, height * 0.5f);
            Vector2 halfSize = center - Vector2.one * 2f;
            Color32[] pixels = new Color32[width * height];

            for (int y = 0; y < height; y++)
            {
                float vertical = y / Mathf.Max(1f, height - 1f);
                for (int x = 0; x < width; x++)
                {
                    Vector2 p = new Vector2(x + 0.5f, y + 0.5f) - center;
                    float sdf = RoundedBoxSdf(p, halfSize, radius);
                    float coverage = Mathf.Clamp01(0.5f - sdf);
                    float borderMask = coverage *
                        (1f - SmoothStep(Mathf.Max(0f, border - 1f), border + 1f, Mathf.Abs(sdf)));
                    float innerEdge = coverage *
                        (1f - SmoothStep(0f, Mathf.Max(radius * 0.55f, 1f), -sdf));
                    float highlight = (1f - vertical) * innerEdge * preset.topHighlight;
                    float shade = vertical * innerEdge * preset.bottomShade;
                    float horizontal = x / Mathf.Max(1f, width - 1f);
                    float gloss = CalculateGloss(horizontal, vertical, preset) * coverage;
                    float alpha = Mathf.Max(coverage * preset.fillOpacity, borderMask * preset.borderOpacity);
                    alpha = Mathf.Clamp01(alpha + highlight + gloss - shade);
                    pixels[y * width + x] = alpha <= 0.0001f
                        ? new Color32(0, 0, 0, 0)
                        : (Color32)new Color(tint.r, tint.g, tint.b, alpha);
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
            ConfigureSprite(Art + "/LargeLogin_Background_Default_1464x828.png", false);
            ConfigureSprite(Art + "/LargeLogin_InputField_Default_312x56.png", true);
            ConfigureSprite(Art + "/LargeLogin_ActionButton_Normal_312x56.png", true);
            ConfigureSprite(Art + "/LargeLogin_ActionButton_Hover_312x56.png", true);
            ConfigureSprite(Art + "/LargeLogin_ActionButton_Pressed_312x56.png", true);
            ConfigureSprite(Art + "/LargeLogin_ActionButton_Disabled_312x56.png", true);
        }

        static void ConfigureSprite(string path, bool alpha)
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
            importer.maxTextureSize = path.Contains("Background") ? 2048 : 512;
            importer.spritePixelsPerUnit = 100f;
            importer.SaveAndReimport();
        }

        static Material CreateGlassMaterial(
            string path,
            Shader shader,
            GlassUIBakerPreset preset,
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

            float radius = preset.cornerRadius * ControlSize.y / Mathf.Max(1f, preset.outputHeight);
            material.SetColor("_TintColor", tint);
            material.SetFloat("_Opacity", preset.shaderEffectOpacity);
            material.SetFloat("_MaskThreshold", 0.02f);
            material.SetFloat("_MaskSoftness", 0.035f);
            material.SetFloat("_SpriteOverlay", 0.22f);
            material.SetFloat("_CornerRadius", radius);
            material.SetFloat("_Inset", 2f);
            material.SetFloat("_BorderWidth", preset.borderWidth);
            material.SetColor("_BorderColor", new Color(tint.r, tint.g, tint.b, preset.borderOpacity));
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
            material.SetVector("_RectSize", new Vector4(ControlSize.x, ControlSize.y, 0f, 0f));
            EditorUtility.SetDirty(material);
            return material;
        }

        static GameObject BuildScreen(Material inputMaterial, Material buttonMaterial, TMP_FontAsset font)
        {
            GameObject root = new GameObject(
                "LargeLoginScreen",
                typeof(RectTransform),
                typeof(Canvas),
                typeof(CanvasScaler),
                typeof(GraphicRaycaster));
            Canvas canvas = root.GetComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.pixelPerfect = false;

            CanvasScaler scaler = root.GetComponent<CanvasScaler>();
            scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = new Vector2(CanvasWidth, CanvasHeight);
            scaler.screenMatchMode = CanvasScaler.ScreenMatchMode.MatchWidthOrHeight;
            scaler.matchWidthOrHeight = 0.5f;

            Image background = CreateImage(root.transform, "Background", Vector2.zero, Vector2.zero);
            Stretch(background.rectTransform);
            background.sprite = LoadSprite(Art + "/LargeLogin_Background_Default_1464x828.png");
            background.preserveAspect = false;
            background.raycastTarget = false;

            RectTransform form = CreateRect(root.transform, "LoginForm", new Vector2(520f, 430f), Vector2.zero);

            CreateText(form, "AccountLabel", "账号：", new Vector2(96f, 56f), new Vector2(-208f, 109f),
                font, 22f, TextAlignmentOptions.MidlineRight, new Color(1f, 0.96f, 0.90f, 1f));
            TMP_InputField account = CreateInputField(
                form, "AccountInput", "请输入账号", new Vector2(0f, 109f), false,
                inputMaterial, font);

            CreateText(form, "PasswordLabel", "密码：", new Vector2(96f, 56f), new Vector2(-208f, 33f),
                font, 22f, TextAlignmentOptions.MidlineRight, new Color(1f, 0.96f, 0.90f, 1f));
            TMP_InputField password = CreateInputField(
                form, "PasswordInput", "请输入密码", new Vector2(0f, 33f), true,
                inputMaterial, font);

            TMP_Text status = CreateText(form, "StatusMessage", "", new Vector2(420f, 34f),
                new Vector2(0f, -35f), font, 18f, TextAlignmentOptions.Center,
                new Color(1f, 0.29f, 0.19f, 1f));
            status.gameObject.SetActive(false);

            Button login = CreateButton(form, "LoginButton", "登录", new Vector2(0f, -83f),
                buttonMaterial, font);
            Button register = CreateButton(form, "RegisterButton", "注册", new Vector2(0f, -157f),
                buttonMaterial, font);

            CreateText(root.transform, "AgeNotice", "本游戏适合16周岁及以上用户，请合理安排游戏时间。",
                new Vector2(760f, 42f), new Vector2(0f, -389f), font, 15f,
                TextAlignmentOptions.Center, new Color(1f, 0.94f, 0.84f, 0.92f));

            LargeLoginScreenView view = root.AddComponent<LargeLoginScreenView>();
            view.Configure(account, password, login, register, status);
            return root;
        }

        static TMP_InputField CreateInputField(
            Transform parent,
            string name,
            string placeholderText,
            Vector2 position,
            bool password,
            Material material,
            TMP_FontAsset font)
        {
            GameObject go = new GameObject(
                name,
                typeof(RectTransform),
                typeof(CanvasRenderer),
                typeof(Image),
                typeof(URPFrostedGlassPanel),
                typeof(TMP_InputField));
            go.transform.SetParent(parent, false);
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = ControlSize;
            rect.anchoredPosition = position;

            Image image = go.GetComponent<Image>();
            image.sprite = LoadSprite(Art + "/LargeLogin_InputField_Default_312x56.png");
            image.material = material;
            image.type = Image.Type.Simple;

            RectTransform textArea = CreateRect(go.transform, "Text Area", Vector2.zero, Vector2.zero);
            Stretch(textArea, 18f, 11f, 18f, 9f);
            textArea.gameObject.AddComponent<RectMask2D>();

            TMP_Text placeholder = CreateText(textArea, "Placeholder", placeholderText, Vector2.zero,
                Vector2.zero, font, 19f, TextAlignmentOptions.MidlineLeft,
                new Color(1f, 0.96f, 0.90f, 0.52f));
            Stretch(placeholder.rectTransform);

            TMP_Text value = CreateText(textArea, "Text", "", Vector2.zero, Vector2.zero, font, 19f,
                TextAlignmentOptions.MidlineLeft, new Color(1f, 0.97f, 0.92f, 1f));
            Stretch(value.rectTransform);

            TMP_InputField input = go.GetComponent<TMP_InputField>();
            input.textViewport = textArea;
            input.textComponent = value;
            input.placeholder = placeholder;
            input.contentType = password
                ? TMP_InputField.ContentType.Password
                : TMP_InputField.ContentType.Standard;
            input.lineType = TMP_InputField.LineType.SingleLine;
            input.caretColor = new Color(1f, 0.78f, 0.42f, 1f);
            input.selectionColor = new Color(1f, 0.69f, 0.29f, 0.35f);
            return input;
        }

        static Button CreateButton(
            Transform parent,
            string name,
            string label,
            Vector2 position,
            Material material,
            TMP_FontAsset font)
        {
            GameObject go = new GameObject(
                name,
                typeof(RectTransform),
                typeof(CanvasRenderer),
                typeof(Image),
                typeof(URPFrostedGlassPanel),
                typeof(Button));
            go.transform.SetParent(parent, false);
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = ControlSize;
            rect.anchoredPosition = position;

            Image image = go.GetComponent<Image>();
            image.sprite = LoadSprite(Art + "/LargeLogin_ActionButton_Normal_312x56.png");
            image.material = material;
            image.type = Image.Type.Simple;

            Button button = go.GetComponent<Button>();
            button.transition = Selectable.Transition.SpriteSwap;
            SpriteState state = new SpriteState
            {
                highlightedSprite = LoadSprite(Art + "/LargeLogin_ActionButton_Hover_312x56.png"),
                pressedSprite = LoadSprite(Art + "/LargeLogin_ActionButton_Pressed_312x56.png"),
                selectedSprite = LoadSprite(Art + "/LargeLogin_ActionButton_Hover_312x56.png"),
                disabledSprite = LoadSprite(Art + "/LargeLogin_ActionButton_Disabled_312x56.png")
            };
            button.spriteState = state;

            TMP_Text text = CreateText(rect, "Label", label, Vector2.zero, Vector2.zero, font, 22f,
                TextAlignmentOptions.Center, new Color(0.16f, 0.11f, 0.065f, 0.96f));
            Stretch(text.rectTransform);
            text.raycastTarget = false;
            return button;
        }

        static Image CreateImage(Transform parent, string name, Vector2 size, Vector2 position)
        {
            GameObject go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
            go.transform.SetParent(parent, false);
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = size;
            rect.anchoredPosition = position;
            return go.GetComponent<Image>();
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
            GameObject go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(TextMeshProUGUI));
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

        static RectTransform CreateRect(Transform parent, string name, Vector2 size, Vector2 position)
        {
            GameObject go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(parent, false);
            RectTransform rect = go.GetComponent<RectTransform>();
            rect.sizeDelta = size;
            rect.anchoredPosition = position;
            return rect;
        }

        static void Stretch(RectTransform rect, float left = 0f, float bottom = 0f, float right = 0f, float top = 0f)
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
