import argparse
import json
import re
import shutil
from pathlib import Path


PROJECT_ID_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]*UI$")
PREFIX_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]*$")
PROJECT_DIRS = [
    "in",
    "into/Candidates",
    "into/Rejected",
    "into/ReassemblyPreview",
    "Components/out/ProjectId",
    "Templates",
    "FullUI",
    "QA",
]


def replace_tokens(root: Path, project_id: str, display_name: str, prefix: str) -> None:
    replacements = {
        "ProjectDisplayName": display_name,
        "ProjectId": project_id,
        "ComponentPrefix": prefix,
    }
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a wireframe-colored glass UI project.")
    parser.add_argument("--workflow-root", required=True, type=Path)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--component-prefix", required=True)
    args = parser.parse_args()

    if not PROJECT_ID_PATTERN.fullmatch(args.project_id):
        raise SystemExit("project-id must be ASCII PascalCase and end with UI")
    if not PREFIX_PATTERN.fullmatch(args.component_prefix):
        raise SystemExit("component-prefix must be ASCII PascalCase")

    workflow_root = args.workflow_root.resolve()
    target = workflow_root / "04_Projects" / args.project_id
    if target.exists():
        raise SystemExit(f"refusing to overwrite existing project: {target}")

    template = Path(__file__).resolve().parent.parent / "assets" / "project-template"
    target.mkdir(parents=True)
    for rel in PROJECT_DIRS:
        (target / rel).mkdir(parents=True, exist_ok=True)

    for source in template.rglob("*"):
        if source.is_dir():
            continue
        relative = source.relative_to(template)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    placeholder_out = target / "Components" / "out" / "ProjectId"
    formal_out = target / "Components" / "out" / args.project_id
    if placeholder_out.exists():
        placeholder_out.rename(formal_out)
    else:
        formal_out.mkdir(parents=True, exist_ok=True)

    region_template = Path(__file__).resolve().parent.parent / "assets" / "wireframe-regions.example.json"
    shutil.copy2(region_template, target / "in" / f"{args.project_id}_WireframeRegions.json")
    replace_tokens(target, args.project_id, args.display_name, args.component_prefix)

    config_path = target / "project.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["projectDisplayName"] = args.display_name
    config["projectId"] = args.project_id
    config["componentPrefix"] = args.component_prefix
    config["formalOutput"] = f"Components/out/{args.project_id}"
    config["wireframeRegionConfig"] = f"in/{args.project_id}_WireframeRegions.json"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
