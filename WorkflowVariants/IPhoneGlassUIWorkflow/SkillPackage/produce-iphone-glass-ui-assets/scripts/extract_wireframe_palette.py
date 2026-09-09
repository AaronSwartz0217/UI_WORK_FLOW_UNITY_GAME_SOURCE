import argparse
import colorsys
import json
import math
import os
from collections import Counter
from pathlib import Path

from PIL import Image


def relative_reference(source: Path, document: Path) -> str:
    return Path(os.path.relpath(source.resolve(), document.resolve().parent)).as_posix()


def rect_to_pixels(rect: dict, mode: str, width: int, height: int) -> tuple[int, int, int, int]:
    values = [rect.get(key) for key in ("x", "y", "width", "height")]
    if any(value is None for value in values):
        raise ValueError("region rect requires x, y, width, and height")
    x, y, w, h = map(float, values)
    if mode == "normalized":
        x, w = x * width, w * width
        y, h = y * height, h * height
    elif mode != "pixels":
        raise ValueError(f"unsupported coordinateMode: {mode}")
    left = max(0, min(width, int(round(x))))
    top = max(0, min(height, int(round(y))))
    right = max(left, min(width, int(round(x + w))))
    bottom = max(top, min(height, int(round(y + h))))
    if right <= left or bottom <= top:
        raise ValueError(f"empty or out-of-bounds region: {(left, top, right, bottom)}")
    return left, top, right, bottom


def representative_color(crop: Image.Image) -> tuple[tuple[int, int, int], float, bool, str]:
    sample = crop.convert("RGBA")
    sample.thumbnail((160, 160), Image.Resampling.LANCZOS)
    pixels = [(r, g, b) for r, g, b, a in sample.getdata() if a >= 24]
    if not pixels:
        raise ValueError("region has no visible pixels")

    buckets = Counter((r // 16, g // 16, b // 16) for r, g, b in pixels)
    dominant_bucket, _ = buckets.most_common(1)[0]
    dominant_pixels = [
        (r, g, b) for r, g, b in pixels
        if (r // 16, g // 16, b // 16) == dominant_bucket
    ]
    color = tuple(round(sum(channel) / len(dominant_pixels)) for channel in zip(*dominant_pixels))
    _, saturation, _ = colorsys.rgb_to_hsv(*(channel / 255.0 for channel in color))

    hue_bins = Counter()
    saturated_count = 0
    for r, g, b in pixels:
        hue, sat, _ = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        if sat < 0.12:
            continue
        saturated_count += 1
        hue_bins[int(hue * 24) % 24] += 1

    conflict = False
    if saturated_count and len(hue_bins) >= 2:
        first, second = hue_bins.most_common(2)
        first_share = first[1] / saturated_count
        second_share = second[1] / saturated_count
        bin_distance = abs(first[0] - second[0])
        circular_distance = min(bin_distance, 24 - bin_distance)
        conflict = first_share >= 0.25 and second_share >= 0.25 and circular_distance >= 4

    if saturation < 0.08:
        return color, saturation, False, "low-saturation or neutral wireframe region"
    if conflict:
        return color, saturation, False, "multiple conflicting dominant hues"
    return color, saturation, True, "dominant wireframe hue is unambiguous"


def color_object(rgb: tuple[int, int, int]) -> dict:
    r, g, b = rgb
    return {
        "r": round(r / 255.0, 6),
        "g": round(g / 255.0, 6),
        "b": round(b / 255.0, 6),
        "a": 1.0,
        "hex": f"#{r:02X}{g:02X}{b:02X}",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract per-region UI colors from a wireframe.")
    parser.add_argument("--wireframe", required=True, type=Path)
    parser.add_argument("--regions", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()

    wireframe = args.wireframe.resolve()
    region_path = args.regions.resolve()
    output = args.out.resolve()
    markdown = args.markdown.resolve() if args.markdown else output.with_name("GLASS_COLOR_QA.md")
    if not wireframe.is_file():
        raise SystemExit(f"missing wireframe: {wireframe}")
    if not region_path.is_file():
        raise SystemExit(f"missing region config: {region_path}")

    region_config = json.loads(region_path.read_text(encoding="utf-8"))
    mode = region_config.get("coordinateMode", "normalized")
    source = Image.open(wireframe).convert("RGBA")
    records = []
    for region in region_config.get("regions", []):
        component_id = region.get("componentId", "").strip()
        if not component_id:
            raise SystemExit("every region requires componentId")
        pixel_rect = rect_to_pixels(region.get("rect", {}), mode, source.width, source.height)
        rgb, saturation, confirmed, reason = representative_color(source.crop(pixel_rect))
        color = color_object(rgb)
        records.append({
            "ComponentId": component_id,
            "Required": bool(region.get("required", True)),
            "SourceRect": {"x": pixel_rect[0], "y": pixel_rect[1], "width": pixel_rect[2] - pixel_rect[0], "height": pixel_rect[3] - pixel_rect[1]},
            "WireframeSourceColor": color,
            "GeneratedColor": color.copy(),
            "HueDifference": 0.0,
            "SaturationAdjustment": 0.0,
            "BrightnessAdjustment": 0.0,
            "ColorDecision": "Confirmed" if confirmed else "Pending",
            "DecisionReason": reason,
            "MeasuredSaturation": round(saturation, 6),
        })

    if not records:
        raise SystemExit("region config contains no regions")

    output.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "version": 1,
        "Wireframe": relative_reference(wireframe, output),
        "RegionConfig": relative_reference(region_path, output),
        "regions": records,
    }
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    markdown.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Glass Color QA",
        "",
        f"- Wireframe: `{relative_reference(wireframe, markdown)}`",
        f"- Color map: `{relative_reference(output, markdown)}`",
        "- Rule: white-model/wireframe colors own hue; style-reference colors cannot override them.",
        "",
        "| Component | WireframeSourceColor | GeneratedColor | HueDifference | SaturationAdjustment | BrightnessAdjustment | ColorDecision | Reason |",
        "|---|---|---|---:|---:|---:|---|---|",
    ]
    for record in records:
        lines.append(
            "| {ComponentId} | {source} | {generated} | {HueDifference:.1f} | {SaturationAdjustment:.3f} | {BrightnessAdjustment:.3f} | {ColorDecision} | {DecisionReason} |".format(
                source=record["WireframeSourceColor"]["hex"],
                generated=record["GeneratedColor"]["hex"],
                **record,
            )
        )
    lines.extend(["", "`Pending` entries require user confirmation before formal generation.", ""])
    markdown.write_text("\n".join(lines), encoding="utf-8")

    pending = [record["ComponentId"] for record in records if record["ColorDecision"] == "Pending"]
    print(json.dumps({"result": "PENDING" if pending else "PASS", "records": len(records), "pending": pending, "output": str(output)}, ensure_ascii=False, indent=2))
    raise SystemExit(2 if pending else 0)


if __name__ == "__main__":
    main()
