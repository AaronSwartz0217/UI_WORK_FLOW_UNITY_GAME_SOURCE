from pathlib import Path
from PIL import Image, ImageChops
import json
import sys

path = Path(sys.argv[1])
image = Image.open(path).convert("RGB")
threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 18
mask = Image.new("L", image.size, 0)
src = image.load()
dst = mask.load()
for y in range(image.height):
    for x in range(image.width):
        if max(src[x, y]) > threshold:
            dst[x, y] = 255
bounds = mask.getbbox()
if bounds:
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    ratio = width / height
else:
    width = height = 0
    ratio = 0
print(json.dumps({"file": path.name, "canvas": image.size, "threshold": threshold, "bounds": bounds, "width": width, "height": height, "ratio": ratio}, indent=2))
