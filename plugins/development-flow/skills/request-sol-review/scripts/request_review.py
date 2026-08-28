#!/usr/bin/env python3
"""Invoke one approved Sol review without shell-dependent quoting."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess


def build_command(repository: str, prompt: str) -> list[str]:
    return [
        "codex",
        "exec",
        "--cd",
        repository,
        "--model",
        "gpt-5.6-sol",
        "--sandbox",
        "read-only",
        "--ephemeral",
        "--disable",
        "multi_agent",
        prompt,
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one approved read-only Sol review.")
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    args = parser.parse_args()
    repository = str(args.repository.expanduser().resolve())
    prompt = args.prompt_file.expanduser().read_text(encoding="utf-8")
    return subprocess.run(build_command(repository, prompt), check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
