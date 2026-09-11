#if UNITY_EDITOR
using System;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.Rendering.Universal;
using UnityEngine.SceneManagement;

public static class UISceneTestProjectBuilder
{
    const string Root = "Assets/UI场景测试";
    const string ScenePath = Root + "/Scenes/UI场景测试.unity";
    const string MaterialPath = Root + "/Materials/UI场景测试_BackgroundOpaque.mat";
    const string PrefabPath =
        "Assets/LargeLoginUI/CharacterSetup/Prefabs/LargeLoginCharacterSetup.prefab";
    const string BackgroundTexturePath =
        "Assets/LargeLoginUI/CharacterSetup/Art/" +
        "LargeLogin_CharacterSetupBackground_Default_1464x828.png";
    const string GlassShaderName = "UI/URP Frosted Glass Diffraction";

    [MenuItem("Tools/UI Scene Test/Rebuild Showcase Scene")]
    public static void Build()
    {
        EnsureFolder("Assets", "UI场景测试");
        EnsureFolder(Root, "Scenes");
        EnsureFolder(Root, "Materials");
        EnableOpaqueTexture();

        GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(PrefabPath);
        if (prefab == null)
            throw new FileNotFoundException("CharacterSetup prefab is missing", PrefabPath);

        Texture2D backgroundTexture =
            AssetDatabase.LoadAssetAtPath<Texture2D>(BackgroundTexturePath);
        if (backgroundTexture == null)
            throw new FileNotFoundException("Background texture is missing", BackgroundTexturePath);

        Scene scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        Camera camera = CreateCamera();
        CreateOpaqueBackground(backgroundTexture);

        GameObject instance = PrefabUtility.InstantiatePrefab(prefab, scene) as GameObject;
        if (instance == null)
            throw new InvalidOperationException("Unable to instantiate CharacterSetup prefab.");

        Canvas canvas = instance.GetComponent<Canvas>();
        if (canvas == null)
            throw new InvalidDataException("CharacterSetup prefab has no Canvas.");
        canvas.renderMode = RenderMode.ScreenSpaceCamera;
        canvas.worldCamera = camera;
        canvas.planeDistance = 1f;

        Transform uiBackground = instance.transform.Find("Background");
        if (uiBackground != null)
            uiBackground.gameObject.SetActive(false);

        GameObject eventSystem = new GameObject(
            "EventSystem",
            typeof(EventSystem),
            typeof(StandaloneInputModule));
        eventSystem.transform.SetAsLastSibling();

        EditorSceneManager.SaveScene(scene, ScenePath);
        EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(ScenePath, true) };
        PlayerSettings.productName = "UI场景测试";
        Validate(scene, instance, camera);
        AssetDatabase.SaveAssets();
        Debug.Log("[UI场景测试] BUILD_SUCCESS scene=" + ScenePath +
                  " glassShader=" + GlassShaderName +
                  " opaqueTexture=enabled");
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
        camera.backgroundColor = new Color(0.015f, 0.012f, 0.008f, 1f);
        camera.orthographic = true;
        camera.orthographicSize = 4.14f;
        camera.nearClipPlane = 0.1f;
        camera.farClipPlane = 100f;

        UniversalAdditionalCameraData data =
            go.GetComponent<UniversalAdditionalCameraData>();
        data.requiresColorOption = CameraOverrideOption.On;
        data.renderPostProcessing = false;
        return camera;
    }

    static void CreateOpaqueBackground(Texture2D texture)
    {
        GameObject quad = GameObject.CreatePrimitive(PrimitiveType.Quad);
        quad.name = "OpaqueBackgroundForGlassSampling";
        quad.transform.position = Vector3.zero;
        quad.transform.localScale = new Vector3(14.64f, 8.28f, 1f);
        Collider collider = quad.GetComponent<Collider>();
        if (collider != null)
            UnityEngine.Object.DestroyImmediate(collider);

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

        material.name = "UI场景测试 Background Opaque";
        material.mainTexture = texture;
        if (material.HasProperty("_BaseMap"))
            material.SetTexture("_BaseMap", texture);
        if (material.HasProperty("_BaseColor"))
            material.SetColor("_BaseColor", Color.white);
        material.renderQueue = (int)UnityEngine.Rendering.RenderQueue.Geometry;
        EditorUtility.SetDirty(material);
        quad.GetComponent<MeshRenderer>().sharedMaterial = material;
    }

    static void EnableOpaqueTexture()
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
            EditorUtility.SetDirty(asset);
        }
    }

    static void Validate(Scene scene, GameObject instance, Camera camera)
    {
        if (!scene.IsValid() || !scene.isLoaded)
            throw new InvalidDataException("Showcase scene is not loaded.");
        if (camera == null || !camera.orthographic)
            throw new InvalidDataException("Showcase camera is invalid.");

        Canvas canvas = instance.GetComponent<Canvas>();
        if (canvas == null || canvas.renderMode != RenderMode.ScreenSpaceCamera ||
            canvas.worldCamera != camera)
            throw new InvalidDataException("Canvas is not bound to the showcase camera.");

        int eventSystems = 0;
        foreach (GameObject root in scene.GetRootGameObjects())
            eventSystems += root.GetComponentsInChildren<EventSystem>(true).Length;
        if (eventSystems != 1)
            throw new InvalidDataException("Showcase scene must contain exactly one EventSystem.");

        URPFrostedGlassPanel[] panels =
            instance.GetComponentsInChildren<URPFrostedGlassPanel>(true);
        if (panels.Length != 9)
            throw new InvalidDataException("Expected nine runtime glass panels.");

        foreach (URPFrostedGlassPanel panel in panels)
        {
            UnityEngine.UI.Graphic graphic = panel.GetComponent<UnityEngine.UI.Graphic>();
            if (graphic == null || graphic.material == null ||
                graphic.material.shader.name != GlassShaderName)
                throw new InvalidDataException(panel.name + " is missing the glass shader.");
        }

        GameObject opaqueBackground = GameObject.Find("OpaqueBackgroundForGlassSampling");
        if (opaqueBackground == null || opaqueBackground.GetComponent<MeshRenderer>() == null)
            throw new InvalidDataException("Opaque background for glass sampling is missing.");

        Debug.Log(
            "[UI场景测试] VALIDATION_PASS canvas=ScreenSpaceCamera glassPanels=9 " +
            "eventSystems=1 opaqueBackground=1 opaqueTexture=enabled");
    }

    static void EnsureFolder(string parent, string child)
    {
        string path = parent + "/" + child;
        if (!AssetDatabase.IsValidFolder(path))
            AssetDatabase.CreateFolder(parent, child);
    }
}
#endif
