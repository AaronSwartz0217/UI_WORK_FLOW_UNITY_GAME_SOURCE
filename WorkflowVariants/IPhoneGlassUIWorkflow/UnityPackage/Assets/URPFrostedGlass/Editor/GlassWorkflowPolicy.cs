using System;
using System.IO;
using UnityEditor;
using UnityEngine;

[Serializable]
public sealed class WireframeColorMapDocument
{
    public int version = 1;
    public string Wireframe;
    public WireframeColorRegion[] regions;
}

[Serializable]
public sealed class WireframeColorRegion
{
    public string ComponentId;
    public bool Required;
    public Color WireframeSourceColor = Color.white;
    public Color GeneratedColor = Color.white;
    public float HueDifference;
    public float SaturationAdjustment;
    public float BrightnessAdjustment;
    public string ColorDecision;
    public string DecisionReason;
}

public static class GlassWorkflowPolicy
{
    public const string RequiredPresetAssetPath = "Assets/SHADER/玻璃预设/毛玻璃.json";

    public static bool TryLoadRequiredPreset(out GlassUIBakerPreset preset, bool showDialog = true)
    {
        preset = null;
        string fullPath = GetRequiredPresetFullPath();
        if (!File.Exists(fullPath))
        {
            ReportFailure(
                "缺少指定毛玻璃预设",
                $"必须先安装并读取：\n{RequiredPresetAssetPath}\n\n已停止毛玻璃烘焙。",
                showDialog);
            return false;
        }

        try
        {
            preset = JsonUtility.FromJson<GlassUIBakerPreset>(File.ReadAllText(fullPath));
            if (preset == null || preset.version != 1)
                throw new InvalidDataException("预设版本无效，当前只支持 version = 1。");
            return true;
        }
        catch (Exception exception)
        {
            preset = null;
            ReportFailure("读取指定毛玻璃预设失败", exception.Message, showDialog);
            return false;
        }
    }

    public static void SaveCandidatePreset(GlassUIBakerPreset preset, string defaultName)
    {
        string path = EditorUtility.SaveFilePanel(
            "保存候选效果（不会覆盖指定预设）",
            Application.dataPath,
            string.IsNullOrWhiteSpace(defaultName) ? "GlassCandidate" : defaultName,
            "json");
        if (string.IsNullOrEmpty(path))
            return;

        try
        {
            File.WriteAllText(path, JsonUtility.ToJson(preset, true));
            RefreshIfInsideProject(path);
            Debug.Log($"Saved glass candidate preset: {path}");
        }
        catch (Exception exception)
        {
            Debug.LogException(exception);
            EditorUtility.DisplayDialog("保存候选预设失败", exception.Message, "OK");
        }
    }

    public static bool SaveApprovedPreset(GlassUIBakerPreset preset)
    {
        bool confirmed = EditorUtility.DisplayDialog(
            "覆盖唯一毛玻璃预设",
            "只有用户已经明确确认当前候选效果时才能覆盖：\n" +
            RequiredPresetAssetPath + "\n\n是否确认已经获得用户批准？",
            "已获得用户确认并覆盖",
            "取消");
        if (!confirmed)
            return false;

        try
        {
            string path = GetRequiredPresetFullPath();
            if (!TryLoadRequiredPreset(out GlassUIBakerPreset approvedPreset, false))
            {
                EditorUtility.DisplayDialog(
                    "覆盖指定预设失败",
                    "原指定预设已经缺失或无效。根据工作流规则，不允许从默认值重新创建。",
                    "OK");
                return false;
            }
            // Per-panel wireframe Tint never becomes a global palette override.
            preset.tint = approvedPreset.tint;
            Directory.CreateDirectory(Path.GetDirectoryName(path));
            File.WriteAllText(path, JsonUtility.ToJson(preset, true));
            AssetDatabase.Refresh();
            Debug.Log($"Overwrote approved frosted-glass preset: {RequiredPresetAssetPath}");
            return true;
        }
        catch (Exception exception)
        {
            Debug.LogException(exception);
            EditorUtility.DisplayDialog("覆盖指定预设失败", exception.Message, "OK");
            return false;
        }
    }

    public static bool TrySelectWireframeTint(
        string componentId,
        out Color tint,
        out string sourceDescription)
    {
        tint = Color.white;
        sourceDescription = string.Empty;
        if (string.IsNullOrWhiteSpace(componentId))
        {
            EditorUtility.DisplayDialog("缺少组件 ID", "请先输入颜色表中的 ComponentId。", "OK");
            return false;
        }

        string path = EditorUtility.OpenFilePanel("选择白模颜色表", Application.dataPath, "json");
        if (string.IsNullOrEmpty(path))
            return false;

        try
        {
            WireframeColorMapDocument document = JsonUtility.FromJson<WireframeColorMapDocument>(File.ReadAllText(path));
            if (document == null || document.version != 1 || document.regions == null)
                throw new InvalidDataException("颜色表格式无效或不受支持。");

            foreach (WireframeColorRegion region in document.regions)
            {
                if (region == null || !string.Equals(region.ComponentId, componentId.Trim(), StringComparison.Ordinal))
                    continue;
                if (!string.Equals(region.ColorDecision, "Confirmed", StringComparison.OrdinalIgnoreCase) &&
                    !string.Equals(region.ColorDecision, "Pass", StringComparison.OrdinalIgnoreCase))
                {
                    EditorUtility.DisplayDialog(
                        "白模颜色尚未确认",
                        $"{region.ComponentId} 的 ColorDecision 为 {region.ColorDecision ?? "Missing"}。\n" +
                        "请先确认颜色，再执行正式烘焙。",
                        "OK");
                    return false;
                }

                tint = new Color(
                    Mathf.Clamp01(region.WireframeSourceColor.r),
                    Mathf.Clamp01(region.WireframeSourceColor.g),
                    Mathf.Clamp01(region.WireframeSourceColor.b),
                    1f);
                sourceDescription = $"{Path.GetFileName(path)} / {region.ComponentId} / {region.ColorDecision}";
                return true;
            }

            EditorUtility.DisplayDialog("找不到白模颜色", $"颜色表中不存在 ComponentId：{componentId}", "OK");
            return false;
        }
        catch (Exception exception)
        {
            Debug.LogException(exception);
            EditorUtility.DisplayDialog("读取白模颜色表失败", exception.Message, "OK");
            return false;
        }
    }

    static string GetRequiredPresetFullPath()
    {
        string projectRoot = Directory.GetParent(Application.dataPath).FullName;
        return Path.GetFullPath(Path.Combine(projectRoot, RequiredPresetAssetPath));
    }

    static void ReportFailure(string title, string message, bool showDialog)
    {
        Debug.LogError($"{title}: {message}");
        if (showDialog)
            EditorUtility.DisplayDialog(title, message, "OK");
    }

    static void RefreshIfInsideProject(string path)
    {
        string normalizedPath = Path.GetFullPath(path).Replace('\\', '/');
        string projectRoot = Path.GetFullPath(Directory.GetParent(Application.dataPath).FullName)
            .Replace('\\', '/').TrimEnd('/') + "/";
        if (normalizedPath.StartsWith(projectRoot, StringComparison.OrdinalIgnoreCase))
            AssetDatabase.Refresh();
    }
}
