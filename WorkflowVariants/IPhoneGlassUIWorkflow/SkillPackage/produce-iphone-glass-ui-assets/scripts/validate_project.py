import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

from PIL import Image


REQUIRED_DIRS = ["in", "into", "Components/out", "Templates", "FullUI", "QA"]
REQUIRED_DOCS = [
    "README.md",
    "QA/FINAL_QA.md",
    "QA/ASSET_MANIFEST.md",
    "QA/COMPONENT_COORDINATES.md",
    "QA/BUTTON_TEXT_MATRIX.md",
    "QA/PROPORTION_LOOP_01.md",
]
STATES = {"Normal", "Hover", "Pressed", "Disabled", "Default", "Empty", "Selected"}
FOUR_STATES = {"Normal", "Hover", "Pressed", "Disabled"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    errors = []

    config_path = project / "project.json"
    if not config_path.exists():
        raise SystemExit("missing project.json")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    project_id = config.get("projectId", "")
    prefix = config.get("componentPrefix", "")

    for rel in REQUIRED_DIRS:
        if not (project / rel).is_dir():
            errors.append(f"missing directory: {rel}")
    for rel in REQUIRED_DOCS:
        if not (project / rel).is_file():
            errors.append(f"missing document: {rel}")

    out = project / "Components" / "out" / project_id
    if not out.is_dir():
        errors.append(f"missing formal output: Components/out/{project_id}")
        files = []
    else:
        files = list(out.iterdir())

    non_png = [p.name for p in files if p.is_file() and p.suffix.lower() != ".png"]
    if non_png:
        errors.append(f"non-PNG files in formal output: {non_png}")

    pattern = re.compile(
        rf"^{re.escape(prefix)}_(?P<component>[A-Za-z0-9]+)_(?P<state>[A-Za-z]+)_(?P<w>\d+)x(?P<h>\d+)\.png$"
    )
    families = defaultdict(dict)
    for path in sorted(p for p in files if p.is_file() and p.suffix.lower() == ".png"):
        match = pattern.match(path.name)
        if not match:
            errors.append(f"invalid filename: {path.name}")
            continue
        state = match.group("state")
        if state not in STATES:
            errors.append(f"unsupported state in {path.name}: {state}")
        image = Image.open(path).convert("RGBA")
        expected = (int(match.group("w")), int(match.group("h")))
        if image.size != expected:
            errors.append(f"filename size mismatch: {path.name} != {image.size}")
        alpha = image.getchannel("A")
        if alpha.getbbox() is None:
            errors.append(f"empty alpha: {path.name}")
        component = match.group("component")
        families[component][state] = (image.size, alpha.tobytes())

    for component, state_map in families.items():
        present = set(state_map)
        if component.endswith(("Button", "Tab")) and present & FOUR_STATES and not FOUR_STATES <= present:
            errors.append(f"incomplete four-state family {component}: {sorted(present)}")
        if FOUR_STATES <= present:
            sizes = {state_map[state][0] for state in FOUR_STATES}
            masks = {state_map[state][1] for state in FOUR_STATES}
            if len(sizes) != 1:
                errors.append(f"state canvas mismatch: {component}")
            if len(masks) != 1:
                errors.append(f"state alpha silhouette mismatch: {component}")

    result = {
        "projectId": project_id,
        "formalPngCount": sum(1 for p in files if p.is_file() and p.suffix.lower() == ".png"),
        "errors": errors,
        "result": "PASS" if not errors else "FAIL",
    }
    if config.get("status") in {"pending_final_review", "complete"} and result["formalPngCount"] == 0:
        errors.append("final-stage project has no formal PNG assets")
        result["result"] = "FAIL"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
