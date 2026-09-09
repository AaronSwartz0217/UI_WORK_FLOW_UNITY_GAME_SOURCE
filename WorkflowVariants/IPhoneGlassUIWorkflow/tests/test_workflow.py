import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


VARIANT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = VARIANT_ROOT / "SkillPackage" / "produce-iphone-glass-ui-assets" / "scripts"


def run_script(name: str, *args: str, expected: int = 0) -> subprocess.CompletedProcess:
    process = subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    if process.returncode != expected:
        raise AssertionError(
            f"{name} returned {process.returncode}, expected {expected}\nstdout:\n{process.stdout}\nstderr:\n{process.stderr}"
        )
    return process


class WorkflowTests(unittest.TestCase):
    def test_palette_marks_colored_region_confirmed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            wireframe = root / "wireframe.png"
            Image.new("RGB", (80, 60), (28, 112, 212)).save(wireframe)
            regions = root / "regions.json"
            regions.write_text(json.dumps({
                "version": 1,
                "coordinateMode": "normalized",
                "regions": [{
                    "componentId": "MainPanelBase",
                    "rect": {"x": 0, "y": 0, "width": 1, "height": 1},
                    "required": True,
                }],
            }), encoding="utf-8")
            output = root / "QA" / "WIREFRAME_COLOR_MAP.json"
            markdown = root / "QA" / "GLASS_COLOR_QA.md"
            run_script(
                "extract_wireframe_palette.py",
                "--wireframe", str(wireframe),
                "--regions", str(regions),
                "--out", str(output),
                "--markdown", str(markdown),
            )
            record = json.loads(output.read_text(encoding="utf-8"))["regions"][0]
            self.assertEqual(record["ColorDecision"], "Confirmed")
            self.assertEqual(record["WireframeSourceColor"], record["GeneratedColor"])

    def test_palette_marks_neutral_region_pending(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            wireframe = root / "wireframe.png"
            Image.new("RGB", (64, 64), (128, 128, 128)).save(wireframe)
            regions = root / "regions.json"
            regions.write_text(json.dumps({
                "version": 1,
                "coordinateMode": "pixels",
                "regions": [{
                    "componentId": "NeutralPanel",
                    "rect": {"x": 0, "y": 0, "width": 64, "height": 64},
                }],
            }), encoding="utf-8")
            output = root / "map.json"
            run_script(
                "extract_wireframe_palette.py",
                "--wireframe", str(wireframe),
                "--regions", str(regions),
                "--out", str(output),
                expected=2,
            )
            record = json.loads(output.read_text(encoding="utf-8"))["regions"][0]
            self.assertEqual(record["ColorDecision"], "Pending")

    def test_scaffold_install_and_validate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workflow = root / "workflow"
            (workflow / "04_Projects").mkdir(parents=True)
            unity = root / "unity"
            (unity / "Assets").mkdir(parents=True)

            run_script("install_unity_package.py", "--unity-project", str(unity))
            run_script(
                "scaffold_glass_project.py",
                "--workflow-root", str(workflow),
                "--project-id", "GlassDemoUI",
                "--display-name", "玻璃演示",
                "--component-prefix", "GlassDemo",
            )
            project = workflow / "04_Projects" / "GlassDemoUI"
            wireframe = project / "in" / "GlassDemoUI_Wireframe_80x60.png"
            Image.new("RGB", (80, 60), (36, 132, 214)).save(wireframe)
            regions = project / "in" / "GlassDemoUI_WireframeRegions.json"
            regions.write_text(json.dumps({
                "version": 1,
                "coordinateMode": "normalized",
                "regions": [{
                    "componentId": "MainPanelBase",
                    "rect": {"x": 0, "y": 0, "width": 1, "height": 1},
                }],
            }), encoding="utf-8")
            run_script(
                "extract_wireframe_palette.py",
                "--wireframe", str(wireframe),
                "--regions", str(regions),
                "--out", str(project / "QA" / "WIREFRAME_COLOR_MAP.json"),
                "--markdown", str(project / "QA" / "GLASS_COLOR_QA.md"),
            )
            run_script(
                "validate_glass_project.py",
                "--project", str(project),
                "--unity-project", str(unity),
            )


if __name__ == "__main__":
    unittest.main()
