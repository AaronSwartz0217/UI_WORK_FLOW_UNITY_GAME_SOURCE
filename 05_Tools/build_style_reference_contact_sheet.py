from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys

source = Path(sys.argv[1])
output = Path(sys.argv[2])
recursive = "--recursive" in sys.argv[3:]
files = sorted(
    path for path in (source.rglob("*") if recursive else source.glob("*.png"))
    if path.is_file()
    and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    and "元素参考" not in path.parts
)
thumb_w, thumb_h = 300, 210
label_h = 48
cols = 4
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), (32, 32, 32))
draw = ImageDraw.Draw(sheet)
font = ImageFont.load_default()

for index, path in enumerate(files):
    image = Image.open(path).convert("RGBA")
    checker = Image.new("RGB", image.size, (220, 220, 220))
    checker_draw = ImageDraw.Draw(checker)
    step = max(8, min(image.size) // 12)
    for y in range(0, image.height, step):
        for x in range(0, image.width, step):
            if (x // step + y // step) % 2:
                checker_draw.rectangle((x, y, x + step - 1, y + step - 1), fill=(155, 155, 155))
    checker = checker.convert("RGBA")
    checker.alpha_composite(image)
    preview = checker.convert("RGB")
    preview.thumbnail((thumb_w - 20, thumb_h - 20), Image.Resampling.LANCZOS)
    col, row = index % cols, index // cols
    x0 = col * thumb_w
    y0 = row * (thumb_h + label_h)
    px = x0 + (thumb_w - preview.width) // 2
    py = y0 + (thumb_h - preview.height) // 2
    sheet.paste(preview, (px, py))
    label = str(path.relative_to(source).with_suffix(""))
    if len(label) > 42:
        label = label[:39] + "..."
    draw.text((x0 + 8, y0 + thumb_h + 4), label, fill=(245, 245, 245), font=font)
    draw.text((x0 + 8, y0 + thumb_h + 22), f"{image.width}x{image.height} {image.mode}", fill=(190, 190, 190), font=font)

output.parent.mkdir(parents=True, exist_ok=True)
sheet.save(output, quality=94)
