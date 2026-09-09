#!/usr/bin/env python3
"""Validate the external UNITY_FIGHTCHRACTER_FLOW_PLUGIN checkout without copying it."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_LOCK = (
    Path(__file__).resolve().parents[3]
    / "external-plugins"
    / "fight-character-plugin.lock.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check an external Fight Character Flow Plugin repository against the workflow lock."
    )
    parser.add_argument("--plugin-repo", required=True, type=Path)
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


def git(repo: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return process.stdout.strip()


def canonical_repository(value: str) -> str:
    normalized = value.strip().replace("\\", "/")
    if normalized.startswith("git@github.com:"):
        normalized = "https://github.com/" + normalized[len("git@github.com:") :]
    if normalized.endswith(".git"):
        normalized = normalized[:-4]
    return normalized.rstrip("/").lower()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def validate(repo: Path, lock_path: Path) -> dict[str, Any]:
    repo = repo.resolve()
    lock_path = lock_path.resolve()
    lock = load_json(lock_path)
    errors: list[str] = []
    packages: list[dict[str, Any]] = []

    report: dict[str, Any] = {
        "schemaVersion": 1,
        "checkedAtUtc": datetime.now(timezone.utc).isoformat(),
        "pluginCheckoutPathRecorded": False,
        "lockFile": lock_path.name,
        "sourceOfTruth": "external-repository",
        "pluginInventoryCopied": False,
        "expectedRepository": lock.get("repository", ""),
        "expectedCommit": lock.get("verifiedCommit", ""),
        "actualRepository": "",
        "actualCommit": "",
        "workingTreeClean": False,
        "packages": packages,
        "errors": errors,
    }

    if not repo.is_dir():
        errors.append("Plugin repository directory does not exist.")
        report["status"] = "fail"
        return report

    try:
        inside = git(repo, "rev-parse", "--is-inside-work-tree")
        if inside.lower() != "true":
            errors.append("The plugin path is not a Git working tree.")
            report["status"] = "fail"
            return report

        actual_repository = git(repo, "config", "--get", "remote.origin.url")
        actual_commit = git(repo, "rev-parse", "HEAD")
        dirty = git(repo, "status", "--porcelain")
        report["actualRepository"] = actual_repository
        report["actualCommit"] = actual_commit
        report["workingTreeClean"] = not bool(dirty)

        if canonical_repository(actual_repository) != canonical_repository(
            str(lock.get("repository", ""))
        ):
            errors.append("remote.origin.url does not match the locked source repository.")
        if actual_commit != lock.get("verifiedCommit"):
            errors.append(
                f"Commit drift: expected {lock.get('verifiedCommit')}, got {actual_commit}."
            )
        if dirty:
            errors.append("The external plugin working tree contains uncommitted changes.")
    except RuntimeError as exc:
        errors.append(str(exc))
        report["status"] = "fail"
        return report

    for contract in lock.get("packages", []):
        package_root = repo / contract["path"]
        package_result: dict[str, Any] = {
            "id": contract["id"],
            "expectedVersion": contract["version"],
            "actualVersion": None,
            "path": contract["path"],
            "status": "pass",
        }
        packages.append(package_result)

        manifest_path = package_root / "package.json"
        if not manifest_path.is_file():
            errors.append(f"Missing package manifest: {contract['path']}/package.json")
            package_result["status"] = "fail"
            continue

        try:
            manifest = load_json(manifest_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid package manifest {contract['path']}/package.json: {exc}")
            package_result["status"] = "fail"
            continue

        package_result["actualVersion"] = manifest.get("version")
        if manifest.get("name") != contract["id"]:
            errors.append(
                f"Package id mismatch at {manifest_path}: expected {contract['id']}, got {manifest.get('name')}."
            )
            package_result["status"] = "fail"
        if manifest.get("version") != contract["version"]:
            errors.append(
                f"Package version drift for {contract['id']}: expected {contract['version']}, got {manifest.get('version')}."
            )
            package_result["status"] = "fail"

        for relative in contract.get("requiredPaths", []):
            required = package_root / relative
            if not required.is_file():
                errors.append(f"Required plugin file is missing: {contract['path']}/{relative}")
                package_result["status"] = "fail"

        for relative, tokens in contract.get("requiredText", {}).items():
            source_path = package_root / relative
            if not source_path.is_file():
                continue
            source = source_path.read_text(encoding="utf-8-sig")
            for token in tokens:
                if token not in source:
                    errors.append(
                        f"Required API marker {token!r} is missing from {contract['path']}/{relative}."
                    )
                    package_result["status"] = "fail"

    report["status"] = "pass" if not errors else "fail"
    return report


def main() -> int:
    args = parse_args()
    try:
        report = validate(args.plugin_repo, args.lock)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Compatibility check could not start: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
