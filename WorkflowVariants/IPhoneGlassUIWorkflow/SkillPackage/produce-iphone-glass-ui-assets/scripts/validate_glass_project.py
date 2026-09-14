import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


RUNTIME_PRESET = "Assets/SHADER/玻璃预设/毛玻璃.json"
RUNTIME_SHADER = "UI/URP Frosted Glass Diffraction"
REQUIRED_PRESET_FIELDS = {
    "version", "outputWidth", "outputHeight", "cornerRadius", "borderWidth",
    "fillOpacity", "borderOpacity", "topHighlight", "bottomShade",
    "glossIntensity", "glossWidth", "glossPosition", "glossAngle", "tint",
    "useShaderPreview", "shaderEffectOpacity", "shaderRefraction",
    "shaderRefractionEdgeWidth", "shaderLensStrength", "shaderLensPower",
    "shaderDiffraction", "shaderBlurRadius", "shaderBlurStrength",
    "shaderLuminancePreservation", "shaderExposure", "shaderShadowLift",
}
REQUIRED_COLOR_FIELDS = {
    "WireframeSourceColor", "GeneratedColor", "HueDifference",
    "SaturationAdjustment", "BrightnessAdjustment", "ColorDecision",
}


def is_relative_portable(value: str) -> bool:
    return bool(value) and not Path(value).is_absolute() and not re.match(r"^[A-Za-z]:", value) and "\\" not in value


def valid_color(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    try:
        return all(0.0 <= float(value[channel]) <= 1.0 for channel in ("r", "g", "b", "a"))
    except (KeyError, TypeError, ValueError):
        return False


def run_base_validation(project: Path) -> tuple[dict, list[str]]:
    script = Path(__file__).resolve().parent / "validate_project.py"
    process = subprocess.run(
        [sys.executable, str(script), "--project", str(project)],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError:
        return {}, [f"base validator did not return JSON: {process.stdout or process.stderr}"]
    return result, [f"base: {error}" for error in result.get("errors", [])]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a wireframe-colored glass UI project.")
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--unity-project", required=True, type=Path)
    parser.add_argument("--allow-pending-colors", action="store_true", help="Preflight only; never use for formal delivery.")
    args = parser.parse_args()

    project = args.project.resolve()
    unity_project = args.unity_project.resolve()
    base_result, errors = run_base_validation(project)

    config_path = project / "project.json"
    if not config_path.is_file():
        raise SystemExit("missing project.json")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("workflowVariant") != "IPhoneGlassUIWorkflow":
        errors.append("project.json workflowVariant must be IPhoneGlassUIWorkflow")

    glass = config.get("glass")
    if not isinstance(glass, dict):
        errors.append("project.json is missing glass configuration")
        glass = {}
    if glass.get("enabled") is not True:
        errors.append("glass.enabled must be true")
    if glass.get("preset") != RUNTIME_PRESET:
        errors.append(f"glass.preset must be {RUNTIME_PRESET}")
    if glass.get("colorSource") != "wireframe":
        errors.append("glass.colorSource must be wireframe")
    if glass.get("styleReferenceMayOverrideHue") is not False:
        errors.append("styleReferenceMayOverrideHue must be false")
    if glass.get("runtimeShader") != RUNTIME_SHADER:
        errors.append(f"glass.runtimeShader must be {RUNTIME_SHADER}")

    for key in ("preset", "colorMap"):
        value = glass.get(key, "")
        if not is_relative_portable(value):
            errors.append(f"glass.{key} must be a portable relative path")

    preset_path = unity_project / Path(RUNTIME_PRESET)
    if not preset_path.is_file():
        errors.append(f"missing required Unity preset: {RUNTIME_PRESET}")
    else:
        try:
            preset = json.loads(preset_path.read_text(encoding="utf-8"))
            missing = sorted(REQUIRED_PRESET_FIELDS - set(preset))
            if missing:
                errors.append(f"preset is missing fields: {missing}")
            if preset.get("version") != 1:
                errors.append("preset version must be 1")
            if not valid_color(preset.get("tint")):
                errors.append("preset tint must contain normalized r/g/b/a values")
        except (OSError, json.JSONDecodeError) as exception:
            errors.append(f"invalid required preset: {exception}")

    shader_path = unity_project / "Assets" / "URPFrostedGlass" / "URPFrostedGlassUI.shader"
    if not shader_path.is_file():
        errors.append("missing URP glass shader source: Assets/URPFrostedGlass/URPFrostedGlassUI.shader")
    else:
        shader_source = shader_path.read_text(encoding="utf-8")
        if RUNTIME_SHADER not in shader_source:
            errors.append(f"URP shader does not declare {RUNTIME_SHADER}")
        if "half sourceAlpha = saturate(bakedSprite.a);" not in shader_source or \
                "min(sourceAlpha, _OutputAlpha)" not in shader_source or \
                "* input.color.a" not in shader_source:
            errors.append("URP glass shader must preserve source PNG alpha, its output-alpha cap, and uGUI Image color alpha")
        if "_OutputAlpha (\"Maximum Rendered Opacity\"" not in shader_source:
            errors.append("URP glass shader must expose Maximum Rendered Opacity")
        if "half alpha = effectMask * input.color.a;" in shader_source:
            errors.append("URP glass shader still forces the valid glass mask to solid alpha")

    color_map_rel = glass.get("colorMap", "")
    color_map_path = project / color_map_rel if is_relative_portable(color_map_rel) else project / "__invalid__"
    records = []
    if not color_map_path.is_file():
        errors.append(f"missing glass color map: {color_map_rel or '<empty>'}")
    else:
        try:
            color_map = json.loads(color_map_path.read_text(encoding="utf-8"))
            records = color_map.get("regions", [])
            if not records:
                errors.append("glass color map contains no region records")
            for index, record in enumerate(records):
                component = record.get("ComponentId") or f"record[{index}]"
                missing = sorted(REQUIRED_COLOR_FIELDS - set(record))
                if missing:
                    errors.append(f"{component} color record is missing fields: {missing}")
                if not valid_color(record.get("WireframeSourceColor")):
                    errors.append(f"{component} has invalid WireframeSourceColor")
                if not valid_color(record.get("GeneratedColor")):
                    errors.append(f"{component} has invalid GeneratedColor")
                decision = record.get("ColorDecision")
                if decision not in {"Confirmed", "Pass"} and not args.allow_pending_colors:
                    errors.append(f"{component} ColorDecision is {decision or 'missing'}")
                try:
                    if abs(float(record.get("HueDifference", 999))) > float(glass.get("maxHueDifferenceDegrees", 12.0)):
                        errors.append(f"{component} exceeds allowed HueDifference")
                except (TypeError, ValueError):
                    errors.append(f"{component} has invalid HueDifference")
        except (OSError, json.JSONDecodeError) as exception:
            errors.append(f"invalid glass color map: {exception}")

    components = glass.get("components", [])
    record_ids = {record.get("ComponentId") for record in records if isinstance(record, dict)}
    for component in components if isinstance(components, list) else []:
        if component not in record_ids:
            errors.append(f"glass component has no wireframe color record: {component}")
    if base_result.get("formalPngCount", 0) > 0 and not components:
        errors.append("formal glass project must list glass.components")

    qa_path = project / "QA" / "GLASS_COLOR_QA.md"
    if not qa_path.is_file():
        errors.append("missing QA/GLASS_COLOR_QA.md")
    else:
        qa_text = qa_path.read_text(encoding="utf-8")
        for field in sorted(REQUIRED_COLOR_FIELDS):
            if field not in qa_text:
                errors.append(f"GLASS_COLOR_QA.md does not mention {field}")

    result = {
        "projectId": config.get("projectId", ""),
        "baseResult": base_result.get("result", "FAIL"),
        "requiredPreset": RUNTIME_PRESET,
        "colorRecordCount": len(records),
        "errors": errors,
        "result": "PASS" if not errors else "FAIL",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
