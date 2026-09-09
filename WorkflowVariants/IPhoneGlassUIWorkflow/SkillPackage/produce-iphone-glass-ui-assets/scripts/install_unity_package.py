import argparse
import hashlib
import json
import shutil
from pathlib import Path


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tga", ".tif", ".tiff", ".psd"}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Install the GLSDD glass package and approved preset into Unity.")
    parser.add_argument("--unity-project", required=True, type=Path)
    parser.add_argument("--force", action="store_true", help="Overwrite conflicting files after explicit approval.")
    args = parser.parse_args()

    unity_project = args.unity_project.resolve()
    assets = unity_project / "Assets"
    if not assets.is_dir():
        raise SystemExit(f"not a Unity project (missing Assets): {unity_project}")

    variant_root = Path(__file__).resolve().parents[3]
    source_assets = variant_root / "UnityPackage" / "Assets"
    if not source_assets.is_dir():
        raise SystemExit(f"missing packaged Assets directory: {source_assets}")

    sources = [p for p in source_assets.rglob("*") if p.is_file() and p.suffix.lower() not in IMAGE_SUFFIXES]
    conflicts = []
    skipped = []
    planned = []
    for source in sources:
        relative = source.relative_to(source_assets)
        destination = assets / relative
        if destination.exists():
            if digest(source) == digest(destination):
                skipped.append(relative.as_posix())
            elif not args.force:
                conflicts.append(relative.as_posix())
            else:
                planned.append((source, destination, "updated"))
        else:
            planned.append((source, destination, "created"))

    if conflicts:
        print(json.dumps({"result": "BLOCKED", "conflicts": conflicts}, ensure_ascii=False, indent=2))
        raise SystemExit("conflicting Unity files found; review them and rerun with --force only after explicit approval")

    installed = []
    for source, destination, action in planned:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        installed.append({"path": destination.relative_to(unity_project).as_posix(), "action": action})

    preset = unity_project / "Assets" / "SHADER" / "玻璃预设" / "毛玻璃.json"
    if not preset.is_file():
        raise SystemExit("installation failed: required preset was not installed")

    print(json.dumps({
        "result": "PASS",
        "installed": installed,
        "unchanged": skipped,
        "requiredPreset": "Assets/SHADER/玻璃预设/毛玻璃.json",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
