#!/usr/bin/env python3
"""Stop one explicit Visual Companion session."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import urllib.parse
import urllib.request


def stop_session(info: dict[str, object]) -> None:
    api_url = str(info["api_url"]).rstrip("/")
    key = urllib.parse.quote(str(info["key"]), safe="")
    request = urllib.request.Request(f"{api_url}/stop?key={key}", data=b"", method="POST")
    with urllib.request.urlopen(request, timeout=5) as response:
        if response.status != 204:
            raise RuntimeError(f"visual_stop_failed: HTTP {response.status}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("session_dir", type=Path)
    args = parser.parse_args()
    session = args.session_dir.expanduser().resolve()
    info_path = session / "state" / "server-info.json"
    info = json.loads(info_path.read_text(encoding="utf-8"))
    stop_session(info)
    print(f"stopped visual companion session: {session}")


if __name__ == "__main__":
    main()
