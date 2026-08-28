from collections import defaultdict
from pathlib import Path
from PIL import Image
import json
import re
import sys

folder = Path(sys.argv[1])
files = sorted(folder.glob("*.png"))
errors = []
families = defaultdict(dict)
pattern = re.compile(r"^(.+)_([A-Za-z]+)_(\d+)x(\d+)\.png$")
states = {"Normal", "Hover", "Pressed", "Disabled"}

for path in files:
    image = Image.open(path)
    match = pattern.match(path.name)
    if not match:
        errors.append(f"filename: {path.name}")
        continue
    expected = (int(match.group(3)), int(match.group(4)))
    if image.size != expected:
        errors.append(f"size: {path.name} expected={expected} actual={image.size}")
    if image.mode != "RGBA":
        errors.append(f"mode: {path.name}={image.mode}")
    state = match.group(2)
    if state in states:
        families[match.group(1)][state] = image.size

for family, variants in sorted(families.items()):
    if set(variants) != states:
        errors.append(f"states: {family}={sorted(variants)}")
    if len(set(variants.values())) != 1:
        errors.append(f"canvas: {family}={variants}")

print(json.dumps({
    "folder": folder.name,
    "pngCount": len(files),
    "stateFamilies": len(families),
    "errors": errors,
    "result": "PASS" if not errors else "FAIL"
}, ensure_ascii=False, indent=2))
