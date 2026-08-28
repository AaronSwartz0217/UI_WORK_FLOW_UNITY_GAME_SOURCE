from pathlib import Path
from PIL import Image
import re

root = Path(__file__).resolve().parents[1]
folder = root / "04_Projects" / "EquipmentAdvancementUI" / "Components" / "out" / "EquipmentAdvancementUI"
files = sorted(folder.glob("*.png"))
bad = []
families = {}
for path in files:
    image = Image.open(path).convert("RGBA")
    match = re.search(r"_(\d+)x(\d+)\.png$", path.name)
    corners = [(0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1)]
    if not match or image.size != (int(match.group(1)), int(match.group(2))):
        bad.append(f"size:{path.name}")
    if any(image.getpixel(point)[3] != 0 for point in corners):
        bad.append(f"corner-alpha:{path.name}")
    for state in ("Normal", "Hover", "Pressed", "Disabled"):
        token = f"_{state}_"
        if token in path.name:
            family = path.name.split(token)[0]
            families.setdefault(family, set()).add(image.size)
for family, sizes in families.items():
    if len(sizes) != 1:
        bad.append(f"state-canvas:{family}")
print({"png_count": len(files), "bad_files": bad, "state_family_canvas_counts": {k: len(v) for k, v in families.items()}, "result": "PASS" if not bad else "FAIL"})
