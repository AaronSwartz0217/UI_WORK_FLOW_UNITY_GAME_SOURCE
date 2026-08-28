import argparse
import json
import shutil
from pathlib import Path


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-root", required=True, type=Path)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--component-prefix", required=True)
    args = parser.parse_args()

    if not args.project_id.isascii() or not args.project_id.endswith("UI"):
        raise SystemExit("project-id must be ASCII and end with UI")
    if not args.component_prefix.isascii():
        raise SystemExit("component-prefix must be ASCII")

    template = Path(__file__).resolve().parent.parent / "assets" / "project-template"
    target = args.workflow_root.resolve() / "04_Projects" / args.project_id
    if target.exists():
        raise SystemExit(f"refusing to overwrite existing project: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, target)
    placeholder_out = target / "Components" / "out" / "ProjectId"
    formal_out = target / "Components" / "out" / args.project_id
    if placeholder_out.exists():
        placeholder_out.rename(formal_out)
    replace_tokens(target, args.project_id, args.display_name, args.component_prefix)

    config_path = target / "project.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["projectDisplayName"] = args.display_name
    config["projectId"] = args.project_id
    config["componentPrefix"] = args.component_prefix
    config["formalOutput"] = f"Components/out/{args.project_id}"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
