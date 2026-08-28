#!/usr/bin/env python3
"""Contract tests for the behavioral scenario harness in tests/evals."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "tests" / "evals"
SCENARIOS = ROOT / "tests" / "scenarios.md"

FAKE_CLI = """#!/usr/bin/env python3
import json, sys
prompt = sys.argv[sys.argv.index("-p") + 1]
print(json.dumps({"type": "system", "subtype": "argv", "argv": sys.argv}))
print(json.dumps({"type": "assistant", "message": {"content": [
    {"type": "tool_use", "name": "Skill", "input": {"skill": "development-flow:using-development-flow"}}]}}))
print(json.dumps({"type": "result", "subtype": "success", "num_turns": 1,
                  "total_cost_usd": 0.0, "duration_ms": 10, "result": "echo: " + prompt}))
"""


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ManifestContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = load_module(EVALS / "run_scenarios.py", "run_scenarios")
        self.scenarios = self.runner.read_manifest(EVALS / "manifest.txt")

    def test_manifest_rows_are_well_formed_and_unique(self) -> None:
        ids = [scenario["id"] for scenario in self.scenarios]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids, [f"s{index:02d}" for index in range(1, len(ids) + 1)])
        for scenario in self.scenarios:
            self.assertRegex(scenario["id"], r"^s\d{2}$")
            self.assertIn(scenario["fixture"], self.runner.KNOWN_FIXTURES)
            self.assertIn(scenario["branch"], ("main", "feature/retry"))
            self.assertGreater(len(scenario["prompt"]), 20)

    def test_manifest_covers_every_scenario_in_scenarios_md(self) -> None:
        headings = re.findall(r"(?m)^## ", SCENARIOS.read_text(encoding="utf-8"))
        self.assertEqual(len(self.scenarios), len(headings))

    def test_no_external_model_cli_is_allowlisted(self) -> None:
        joined = " ".join(self.runner.REVIEW_SAFE_TOOLS).lower()
        for cli in ("codex", "claude", "zcode"):
            self.assertNotIn(cli, joined)

    def test_reviewer_approval_scenarios_cannot_tunnel_through_interpreters(self) -> None:
        joined = " ".join(self.runner.REVIEW_SAFE_TOOLS)
        self.assertNotIn("Bash(python3:*)", joined)
        self.assertNotIn("Bash(node:*)", joined)
        self.assertEqual(self.runner.REVIEW_APPROVAL_SCENARIOS, {"s14", "s15", "s16", "s17"})
        self.assertIn("Workflow", self.runner.DISALLOWED_TOOLS)
        # A scenario session must not recruit other live sessions as writers.
        self.assertIn("SendMessage", self.runner.DISALLOWED_TOOLS)
        self.assertIn("ListAgents", self.runner.DISALLOWED_TOOLS)


class HarnessPipelineTests(unittest.TestCase):
    @unittest.skipIf(os.name == "nt", "stub CLI uses a POSIX shebang")
    def test_pipeline_runs_end_to_end_with_a_stub_cli(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / "work"
            stub = Path(temporary) / "fake-claude"
            stub.write_text(FAKE_CLI, encoding="utf-8")
            stub.chmod(stub.stat().st_mode | stat.S_IEXEC)

            run = subprocess.run(
                [sys.executable, str(EVALS / "run_scenarios.py"), "s01", "s16",
                 "--claude-bin", str(stub), "--work-dir", str(work), "--jobs", "2",
                 "--plugin-dir", "plugins/development-flow"],
                capture_output=True, text=True, cwd=ROOT,
            )
            self.assertEqual(run.returncode, 0, run.stderr)

            transcript = (work / "out" / "s16.jsonl").read_text(encoding="utf-8")
            events = [json.loads(line) for line in transcript.splitlines()]
            result = events[-1]
            self.assertNotIn("{HEAD_MAIN}", result["result"])
            self.assertRegex(result["result"], r"commit [0-9a-f]{7}")

            argv = next(event["argv"] for event in events if event.get("subtype") == "argv")
            plugin_dir = Path(argv[argv.index("--plugin-dir") + 1])
            self.assertTrue(plugin_dir.is_absolute(), "relative --plugin-dir must be resolved before spawning sessions")
            self.assertTrue(plugin_dir.is_dir())

            extract = subprocess.run(
                [sys.executable, str(EVALS / "extract_digests.py"), "--work-dir", str(work)],
                capture_output=True, text=True,
            )
            self.assertEqual(extract.returncode, 0, extract.stderr)
            digest = (work / "out" / "s01.digest.txt").read_text(encoding="utf-8")
            self.assertIn("TOOL Skill: development-flow:using-development-flow", digest)
            self.assertIn("--- final text ---", digest)


if __name__ == "__main__":
    unittest.main()
