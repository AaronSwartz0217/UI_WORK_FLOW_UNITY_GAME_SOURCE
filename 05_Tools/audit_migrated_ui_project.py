import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image


project = Path(sys.argv[1])
config = json.loads((project / "project.json").read_text(encoding="utf-8"))
formal = project / config["formalOutput"]
files = sorted(formal.iterdir())
pngs = [path for path in files if path.suffix.lower() == ".png"]
errors = []
families = defaultdict(dict)

if len(pngs) != config["formalPngCount"]:
    errors.append(f"count: config={config['formalPngCount']} actual={len(pngs)}")
if any(path.suffix.lower() != ".png" for path in files):
    errors.append("formal output contains non-PNG files")

pattern = re.compile(r"^([A-Za-z0-9]+)_([A-Za-z0-9]+)_([A-Za-z]+)_(\d+)x(\d+)\.png$")
for path in pngs:
    match = pattern.match(path.name)
    if not match:
        errors.append(f"filename: {path.name}")
        continue
    image = Image.open(path)
    expected = (int(match.group(4)), int(match.group(5)))
    if image.size != expected:
        errors.append(f"size: {path.name} expected={expected} actual={image.size}")
    if image.mode != "RGBA":
        errors.append(f"mode: {path.name} mode={image.mode}")
    state = match.group(3)
    if state in {"Normal", "Hover", "Pressed", "Disabled"}:
        family = f"{match.group(1)}_{match.group(2)}"
        families[family][state] = image.size

required = {"Normal", "Hover", "Pressed", "Disabled"}
for family, states in sorted(families.items()):
    if set(states) != required:
        errors.append(f"states: {family} has={sorted(states)}")
    if len(set(states.values())) != 1:
        errors.append(f"state-size: {family} sizes={states}")

print(json.dumps({
    "projectId": config["projectId"],
    "formalPngCount": len(pngs),
    "stateFamilies": len(families),
    "errors": errors,
    "result": "PASS" if not errors else "FAIL",
}, ensure_ascii=False, indent=2))
