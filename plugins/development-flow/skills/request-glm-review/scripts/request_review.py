#!/usr/bin/env python3
"""Invoke one approved GLM review without shell-dependent quoting."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


DENIED_TOOLS = "Edit,Write,NotebookEdit,Agent,Bash,ExitPlanMode,WebFetch,WebSearch"


def build_command(prefix: list[str], repository: str, prompt: str) -> list[str]:
    return [
        *prefix,
        "--cwd",
        repository,
        "--mode",
        "plan",
        "--disallowed-tools",
        DENIED_TOOLS,
        "--json",
        "-p",
        prompt,
    ]


def bundled_paths() -> tuple[Path | None, Path | None]:
    if sys.platform == "darwin":
        root = Path("/Applications/ZCode.app/Contents")
        return root / "Resources/glm/zcode.cjs", root / "MacOS/ZCode"
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            root = Path(local_app_data) / "Programs/ZCode"
            return root / "resources/glm/zcode.cjs", root / "ZCode.exe"
    return None, None


def cjs_prefix(cli: Path, app_runtime: Path | None) -> tuple[list[str], dict[str, str]]:
    environment = dict(os.environ)
    if app_runtime is not None and app_runtime.is_file():
        environment["ELECTRON_RUN_AS_NODE"] = "1"
        return [str(app_runtime), str(cli)], environment
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("zcode_runtime_missing: install Node 24+ or set ZCODE_BIN to an executable")
    return [node, str(cli)], environment


def resolve_zcode() -> tuple[list[str], dict[str, str]]:
    configured = os.environ.get("ZCODE_BIN")
    if configured:
        candidate = Path(configured).expanduser()
        if not candidate.is_file():
            raise RuntimeError(f"zcode_not_found: {candidate}")
        if candidate.suffix == ".cjs":
            bundled_cli, bundled_runtime = bundled_paths()
            runtime = bundled_runtime if bundled_cli == candidate else None
            return cjs_prefix(candidate, runtime)
        return [str(candidate)], dict(os.environ)

    command = shutil.which("zcode")
    if command:
        return [command], dict(os.environ)

    bundled_cli, bundled_runtime = bundled_paths()
    if bundled_cli is not None and bundled_cli.is_file():
        return cjs_prefix(bundled_cli, bundled_runtime)

    raise RuntimeError("zcode_not_found: install ZCode or set ZCODE_BIN")


def validate_configured_model(config_path: Path, approved_model: str) -> str:
    try:
        config = json.loads(config_path.expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise RuntimeError(f"model_config_missing: {config_path.expanduser()}") from error
    except (json.JSONDecodeError, OSError) as error:
        raise RuntimeError(f"model_config_invalid: {config_path.expanduser()}") from error
    configured = config.get("model")
    if not isinstance(configured, str) or not configured:
        raise RuntimeError("model_config_invalid: missing model")
    configured_name = configured.rsplit("/", 1)[-1]
    if configured_name != approved_model:
        raise RuntimeError(
            f"model_mismatch: approved {approved_model}, configured {configured_name}"
        )
    return configured_name


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one approved read-only GLM review.")
    parser.add_argument("--check", action="store_true", help="Resolve ZCode and print its version without sending a prompt.")
    parser.add_argument("--repository", type=Path)
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--model", required=True, help="exact owner-approved GLM model name")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args()

    try:
        prefix, environment = resolve_zcode()
    except RuntimeError as error:
        parser.error(str(error))

    try:
        validate_configured_model(Path.home() / ".zcode" / "cli" / "config.json", args.model)
    except RuntimeError as error:
        parser.error(str(error))

    if args.check:
        return subprocess.run([*prefix, "version"], env=environment, check=False).returncode

    if args.repository is None or args.prompt_file is None:
        parser.error("--repository and --prompt-file are required unless --check is used")
    if args.timeout_seconds <= 0:
        parser.error("--timeout-seconds must be greater than zero")

    repository = str(args.repository.expanduser().resolve())
    prompt = args.prompt_file.expanduser().read_text(encoding="utf-8")
    try:
        result = subprocess.run(
            build_command(prefix, repository, prompt),
            env=environment,
            timeout=args.timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print("glm_review_timeout: the approved review exceeded its wall-clock limit", file=sys.stderr)
        return 124
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
