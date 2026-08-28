#!/usr/bin/env python3
"""Scaffold an editable Development Flow executive review."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS = SKILL_ROOT / "assets"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("slug must contain a letter or number")
    return slug[:64]


def unique_directory(parent: Path, name: str) -> Path:
    candidate = parent / name
    suffix = 2
    while candidate.exists():
        candidate = parent / f"{name}-{suffix}"
        suffix += 1
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an executive review scaffold.")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    output = args.output.expanduser().resolve() if args.output else Path.cwd() / ".development-flow" / "executive-reviews" / now.strftime("%Y-%m-%d")
    output.mkdir(parents=True, exist_ok=True)
    destination = unique_directory(output, f"{slugify(args.slug)}-executive-review")
    destination.mkdir()

    shutil.copy2(ASSETS / "index.html", destination / "index.html")
    data = (ASSETS / "review-data.js").read_text(encoding="utf-8")
    data = data.replace('"__TITLE__"', json.dumps(args.title, ensure_ascii=False))
    data = data.replace("__DATE__", now.date().isoformat())
    (destination / "review-data.js").write_text(data, encoding="utf-8")
    print(destination)


if __name__ == "__main__":
    main()
