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


def run_git(repo: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if process.returncode != 0:
        raise AssertionError(
            f"git {' '.join(args)} failed\nstdout:\n{process.stdout}\nstderr:\n{process.stderr}"
        )
    return process.stdout.strip()


class WorkflowTests(unittest.TestCase):
    def test_external_plugin_contract_is_metadata_only(self) -> None:
        variant = json.loads((VARIANT_ROOT / "workflow-variant.json").read_text(encoding="utf-8"))
        integration = variant["externalUnityPlugins"][0]
        self.assertEqual(integration["sourceOfTruth"], "external-repository")
        self.assertFalse(integration["copyInventory"])

        lock_path = VARIANT_ROOT / integration["lock"]
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertFalse(lock["ownership"]["vendorIntoWorkflowRepository"])
        self.assertFalse(lock["ownership"]["copyPluginInventory"])
        self.assertEqual(
            {package["id"]: package["version"] for package in lock["packages"]},
            {
                "com.codex.split-rig-retargeter": "1.4.0",
                "com.codex.mixamo-attachment-toolkit": "0.3.0",
            },
        )
        self.assertFalse((VARIANT_ROOT / "Packages").exists())

    def test_external_plugin_checker_detects_dirty_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "plugin"
            package = repo / "Packages" / "com.example.fixture"
            runtime = package / "Runtime"
            runtime.mkdir(parents=True)
            (package / "package.json").write_text(
                json.dumps({"name": "com.example.fixture", "version": "1.0.0"}),
                encoding="utf-8",
            )
            source = runtime / "Controller.cs"
            source.write_text("public sealed class Controller {}\n", encoding="utf-8")

            run_git(repo, "init")
            run_git(repo, "config", "user.name", "Workflow Test")
            run_git(repo, "config", "user.email", "workflow-test@example.invalid")
            run_git(repo, "remote", "add", "origin", "git@github.com:example/plugin.git")
            run_git(repo, "add", ".")
            run_git(repo, "commit", "-m", "fixture")
            commit = run_git(repo, "rev-parse", "HEAD")

            lock_path = root / "lock.json"
            lock_path.write_text(json.dumps({
                "repository": "https://github.com/example/plugin",
                "verifiedCommit": commit,
                "packages": [{
                    "id": "com.example.fixture",
                    "version": "1.0.0",
                    "path": "Packages/com.example.fixture",
                    "requiredPaths": ["package.json", "Runtime/Controller.cs"],
                    "requiredText": {
                        "Runtime/Controller.cs": ["public sealed class Controller"],
                    },
                }],
            }), encoding="utf-8")

            passing = run_script(
                "check_fight_character_plugin.py",
                "--plugin-repo", str(repo),
                "--lock", str(lock_path),
            )
            self.assertEqual(json.loads(passing.stdout)["status"], "pass")

            source.write_text("public sealed class ChangedController {}\n", encoding="utf-8")
            failing = run_script(
                "check_fight_character_plugin.py",
                "--plugin-repo", str(repo),
                "--lock", str(lock_path),
                expected=2,
            )
            report = json.loads(failing.stdout)
            self.assertEqual(report["status"], "fail")
            self.assertFalse(report["workingTreeClean"])
            self.assertTrue(any("uncommitted changes" in error for error in report["errors"]))

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
