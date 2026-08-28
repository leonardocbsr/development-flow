#!/usr/bin/env python3
"""Digest stream-json scenario transcripts into judgeable summaries.

Reads ``<work-dir>/out/<id>.jsonl`` and writes ``<id>.digest.txt`` next to it:
the run result line, the ordered tool trace (skills invoked, commands
attempted, files edited, permission denials), and the session's final text.
Judge each digest against the matching "Expected" section in ../scenarios.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def describe_tool(name: str, inputs: dict) -> str:
    if name == "Skill":
        return str(inputs.get("skill") or inputs.get("command", ""))
    if name == "Bash":
        return str(inputs.get("command") or "")[:220]
    if name in ("Write", "Edit", "MultiEdit", "NotebookEdit", "Read"):
        return str(inputs.get("file_path", ""))
    if name in ("Task", "Agent"):
        return f"{inputs.get('description', '')} :: {str(inputs.get('prompt') or '')[:260]}"
    if name in ("Glob", "Grep"):
        return str(inputs.get("pattern", ""))
    return json.dumps(inputs)[:200]


def digest(path: Path) -> str:
    lines: list[str] = []
    result = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        kind = event.get("type")
        if kind == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    lines.append(f"TOOL {block.get('name', '?')}: {describe_tool(block.get('name', ''), block.get('input', {}))}")
        elif kind == "user":
            content = event.get("message", {}).get("content")
            if isinstance(content, list):
                for block in content:
                    if block.get("type") == "tool_result" and block.get("is_error"):
                        text = block.get("content")
                        if isinstance(text, list):
                            text = " ".join(str(item.get("text", "")) for item in text if isinstance(item, dict))
                        lines.append(f"DENIED/ERROR: {str(text)[:200]}")
        elif kind == "result":
            result = event
    header = []
    if result:
        header.append(
            f"RESULT subtype={result.get('subtype')} turns={result.get('num_turns')} "
            f"cost=${result.get('total_cost_usd') or 0:.2f} duration={round((result.get('duration_ms') or 0) / 1000)}s"
        )
    return "\n".join(
        header
        + ["--- tool trace ---"]
        + lines
        + ["--- final text ---", (result or {}).get("result") or "(no result text)"]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("scenarios", nargs="*", help="scenario ids (default: every transcript found)")
    parser.add_argument("--work-dir", type=Path,
                        default=REPO / ".development-flow" / "evals" / "work")
    args = parser.parse_args()

    out = args.work_dir.expanduser().resolve() / "out"
    ids = args.scenarios or sorted(path.stem for path in out.glob("s*.jsonl"))
    for scenario_id in ids:
        source = out / f"{scenario_id}.jsonl"
        if not source.exists():
            print(f"{scenario_id}: missing transcript")
            continue
        (out / f"{scenario_id}.digest.txt").write_text(digest(source), encoding="utf-8")
        print(f"{scenario_id}: digest written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
