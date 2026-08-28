#!/usr/bin/env python3
"""Contract tests for Development Flow's executable visual scaffolds."""

from __future__ import annotations

import json
import importlib.util
import os
import select
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "development-flow"
VISUAL_SERVER = PLUGIN / "skills" / "visual-companion" / "scripts" / "server.py"
VISUAL_STOP = PLUGIN / "skills" / "visual-companion" / "scripts" / "stop-server.py"
REVIEW_GENERATOR = PLUGIN / "skills" / "executive-review" / "scripts" / "new_review.py"
EXECUTIVE_REVIEW_TEMPLATE = PLUGIN / "skills" / "executive-review" / "assets" / "index.html"
VISUAL_COMPANION_TEMPLATE = PLUGIN / "skills" / "visual-companion" / "assets" / "frame.html"
EXECUTIVE_REVIEW_SKILL = PLUGIN / "skills" / "executive-review" / "SKILL.md"
VISUAL_COMPANION_SKILL = PLUGIN / "skills" / "visual-companion" / "SKILL.md"
FABLE_REVIEW_SKILL = PLUGIN / "skills" / "request-fable-review" / "SKILL.md"
SOL_REVIEW_SKILL = PLUGIN / "skills" / "request-sol-review" / "SKILL.md"
GLM_REVIEW_SKILL = PLUGIN / "skills" / "request-glm-review" / "SKILL.md"
FABLE_REVIEW_RUNNER = PLUGIN / "skills" / "request-fable-review" / "scripts" / "request_review.py"
SOL_REVIEW_RUNNER = PLUGIN / "skills" / "request-sol-review" / "scripts" / "request_review.py"
GLM_REVIEW_RUNNER = PLUGIN / "skills" / "request-glm-review" / "scripts" / "request_review.py"
PLANNING_SKILL = PLUGIN / "skills" / "planning-development" / "SKILL.md"
IMPLEMENTING_SKILL = PLUGIN / "skills" / "implementing-plans" / "SKILL.md"
MIGRATION_SKILL = PLUGIN / "skills" / "migrating-from-superpowers" / "SKILL.md"
ROUTER_SKILL = PLUGIN / "skills" / "using-development-flow" / "SKILL.md"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LocalArtifactContractTests(unittest.TestCase):
    def test_plans_use_milestones_and_control_writer_ownership(self) -> None:
        planning = PLANNING_SKILL.read_text()
        implementing = IMPLEMENTING_SKILL.read_text()
        self.assertIn("observable outcome", planning)
        self.assertIn("literary sequence of microtasks", planning)
        self.assertNotIn("<topic>-design.md", planning)
        self.assertIn("only one is active at a time", implementing)
        self.assertIn("test writer changes tests", implementing)
        self.assertIn("Never run two implementation writers concurrently", implementing)
        self.assertIn("Do not request a review automatically for each task", implementing)

    def test_migration_uses_the_current_recoverable_claude_command(self) -> None:
        migration = MIGRATION_SKILL.read_text()
        self.assertIn("claude plugin disable", migration)
        self.assertNotIn("claude plugin uninstall", migration)

    def test_root_router_frontloads_critical_skill_dispatch(self) -> None:
        router = ROUTER_SKILL.read_text()
        dispatch = router.split("## Start", 1)[0]
        for skill in (
            "testing-stable-contracts",
            "implementing-plans",
            "debugging-systematically",
            "adversarial-reviewing",
            "speaking-plainly",
            "verifying-claims",
            "keeping-a-changelog",
            "migrating-from-superpowers",
            "visual-companion",
            "executive-review",
        ):
            self.assertIn(skill, dispatch)

    def test_html_scaffolds_do_not_load_remote_subresources(self) -> None:
        for template in (EXECUTIVE_REVIEW_TEMPLATE, VISUAL_COMPANION_TEMPLATE):
            with self.subTest(template=template):
                html = template.read_text()
                self.assertNotRegex(html, r'''(?:src|href)=["']https?://''')

    def test_plugin_has_no_shell_only_launcher(self) -> None:
        shell_launchers = sorted(path.relative_to(PLUGIN) for path in PLUGIN.rglob("*.sh"))
        self.assertEqual(shell_launchers, [])

    def test_python_scaffolds_document_mac_linux_and_windows_launchers(self) -> None:
        for skill in (EXECUTIVE_REVIEW_SKILL, VISUAL_COMPANION_SKILL):
            with self.subTest(skill=skill):
                instructions = skill.read_text()
                self.assertIn("macOS or Linux", instructions)
                self.assertIn("Windows PowerShell or Command Prompt", instructions)
                self.assertIn("python3", instructions)
                self.assertIn("py -3", instructions)

    def test_paid_review_commands_do_not_require_posix_shell_syntax(self) -> None:
        for skill in (FABLE_REVIEW_SKILL, SOL_REVIEW_SKILL, GLM_REVIEW_SKILL):
            with self.subTest(skill=skill):
                instructions = skill.read_text()
                self.assertNotRegex(instructions, r"(?m)^[a-z_]+=")
                self.assertNotRegex(instructions, r"(?m)\\$")
                self.assertIn("python3", instructions)
                self.assertIn("py -3", instructions)
                self.assertIn("without shell parsing", instructions)

    def test_glm_review_uses_one_portable_quota_consuming_invocation(self) -> None:
        instructions = GLM_REVIEW_SKILL.read_text()
        self.assertNotIn("prompt probe", instructions.lower())
        self.assertIn("version", instructions)
        self.assertIn("one quota-consuming", instructions.lower())

        runner = load_module(GLM_REVIEW_RUNNER, "glm_review_runner")
        prompt = 'Review "quoted" text with 100% confidence!\nSecond line.'
        repository = r"C:\Users\dev\My Project"
        command = runner.build_command(["zcode"], repository, prompt)
        self.assertEqual(command[0], "zcode")
        self.assertEqual(command[1:3], ["--cwd", repository])
        self.assertEqual(command[-2:], ["-p", prompt])
        self.assertIn("plan", command)
        denied = command[command.index("--disallowed-tools") + 1]
        self.assertIn("Agent", denied)
        self.assertIn("Bash", denied)
        self.assertIn("ExitPlanMode", denied)

    def test_glm_review_requires_the_approved_configured_model(self) -> None:
        runner = load_module(GLM_REVIEW_RUNNER, "glm_review_model_contract")
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / "config.json"
            config.write_text(json.dumps({"model": "builtin:zai-coding-plan/GLM-5.3"}))
            self.assertEqual(runner.validate_configured_model(config, "GLM-5.3"), "GLM-5.3")
            with self.assertRaisesRegex(RuntimeError, "model_mismatch"):
                runner.validate_configured_model(config, "GLM-5.3-Flash")

    def test_removed_review_router_is_not_packaged(self) -> None:
        self.assertFalse((PLUGIN / "skills" / "reviewing-changes").exists())

    def test_fable_runner_passes_prompt_without_shell_parsing(self) -> None:
        runner = load_module(FABLE_REVIEW_RUNNER, "fable_review_runner")
        prompt = 'Review "quoted" text with 100% confidence!\nSecond line.'
        command = runner.build_command(prompt, "7.50")
        self.assertEqual(command[0:5], ["claude", "-p", prompt, "--model", "fable"])
        self.assertIn("--max-budget-usd", command)
        self.assertIn("--no-session-persistence", command)
        self.assertIn("Agent", command)

    def test_fable_runner_pins_the_review_repository(self) -> None:
        runner = load_module(FABLE_REVIEW_RUNNER, "fable_review_repository_contract")
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary).resolve()
            with mock.patch.object(runner.subprocess, "run") as run:
                run.return_value.returncode = 0
                code = runner.run_review(repository, "Review this revision", "1.50")
            self.assertEqual(code, 0)
            self.assertEqual(run.call_args.kwargs["cwd"], repository)

    def test_sol_runner_passes_paths_and_prompt_without_shell_parsing(self) -> None:
        runner = load_module(SOL_REVIEW_RUNNER, "sol_review_runner")
        prompt = 'Review "quoted" text with 100% confidence!\nSecond line.'
        repository = r"C:\Users\dev\My Project"
        command = runner.build_command(repository, prompt)
        self.assertEqual(command[0:3], ["codex", "exec", "--cd"])
        self.assertEqual(command[3], repository)
        self.assertEqual(command[-1], prompt)
        self.assertIn("read-only", command)
        self.assertIn("multi_agent", command)


class ExecutiveReviewScaffoldTests(unittest.TestCase):
    def test_scaffold_starts_without_a_production_lane_and_supports_safe_links(self) -> None:
        data = (PLUGIN / "skills" / "executive-review" / "assets" / "review-data.js").read_text()
        html = EXECUTIVE_REVIEW_TEMPLATE.read_text()
        self.assertIn('lane: "Unknown"', data)
        self.assertIn("safeHref", html)
        self.assertIn("item.href", html)

    def test_generator_creates_editable_responsive_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                [
                    sys.executable,
                    str(REVIEW_GENERATOR),
                    "--output",
                    temporary,
                    "--slug",
                    "scheduler",
                    "--title",
                    "Scheduler rewrite",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            review_dir = Path(result.stdout.strip())
            self.assertTrue(review_dir.is_dir())
            self.assertTrue((review_dir / "index.html").is_file())
            self.assertTrue((review_dir / "review-data.js").is_file())
            self.assertIn("Scheduler rewrite", (review_dir / "review-data.js").read_text())
            html = (review_dir / "index.html").read_text()
            self.assertIn('name="viewport"', html)
            self.assertIn("review-data.js", html)
            self.assertIn("Executive Review", html)

    def test_generator_serializes_hostile_multiline_title_as_valid_javascript(self) -> None:
        title = 'Line one\nLine "two" \\ path </script>'
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                [
                    sys.executable,
                    str(REVIEW_GENERATOR),
                    "--output",
                    temporary,
                    "--slug",
                    "hostile-title",
                    "--title",
                    title,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            data_path = Path(result.stdout.strip()) / "review-data.js"
            data = data_path.read_text()
            self.assertNotIn('title: "Line one\n', data)
            subprocess.run(["node", "--check", str(data_path)], check=True, capture_output=True, text=True)

    def test_default_output_is_project_local(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            environment = dict(os.environ)
            environment["HOME"] = temporary
            result = subprocess.run(
                [sys.executable, str(REVIEW_GENERATOR), "--slug", "release", "--title", "Release"],
                cwd=temporary,
                env=environment,
                check=True,
                capture_output=True,
                text=True,
            )
            review_dir = Path(result.stdout.strip())
            # macOS exposes /var through /private/var, so compare canonical paths.
            expected_parent = (Path(temporary) / ".development-flow" / "executive-reviews").resolve()
            review_dir = review_dir.resolve()
            self.assertTrue(review_dir.is_relative_to(expected_parent))


class ClaudeHookTests(unittest.TestCase):
    def test_prompt_hook_injects_only_a_small_development_router(self) -> None:
        hook = PLUGIN / "hooks" / "prompt-router.js"
        result = subprocess.run(
            ["node", str(hook)],
            input=json.dumps({"prompt": "Fix the package release bug"}),
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertLess(len(context), 500)
        self.assertIn("development-flow:using-development-flow", context)
        self.assertIn("requires a Skill tool call", context)
        self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        self.assertIn("session cwd", context)
        self.assertNotIn("must", context.lower())

    def test_prompt_hook_leaves_unrelated_conversation_alone(self) -> None:
        hook = PLUGIN / "hooks" / "prompt-router.js"
        result = subprocess.run(
            ["node", str(hook)],
            input=json.dumps({"prompt": "Write a birthday poem about the ocean"}),
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stdout, "")

    def test_prompt_hook_names_applicable_routes_without_injecting_skill_bodies(self) -> None:
        hook = PLUGIN / "hooks" / "prompt-router.js"
        cases = {
            "Mock every collaborator in this test": "testing-stable-contracts",
            "Apply this review feedback": "adversarial-reviewing",
            "Add a backward-compatible package export": "keeping-a-changelog",
            "Start the Visual Companion": "visual-companion",
            "Hand off this approved milestone across writers": "implementing-plans",
        }
        for prompt, expected in cases.items():
            with self.subTest(prompt=prompt):
                result = subprocess.run(
                    ["node", str(hook)],
                    input=json.dumps({"prompt": prompt}),
                    check=True,
                    capture_output=True,
                    text=True,
                )
                context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
                self.assertIn(f"development-flow:{expected}", context)
                self.assertLess(len(context), 500)

    def test_hook_manifest_routes_at_prompt_submission(self) -> None:
        manifest = json.loads((PLUGIN / "hooks" / "hooks.json").read_text())
        self.assertIn("UserPromptSubmit", manifest["hooks"])
        self.assertNotIn("SessionStart", manifest["hooks"])


class VisualCompanionScaffoldTests(unittest.TestCase):
    def test_stop_command_uses_the_keyed_session_api_instead_of_a_pid(self) -> None:
        stopper = load_module(VISUAL_STOP, "visual_stop_contract")
        response = mock.MagicMock()
        response.__enter__.return_value.status = 204
        with mock.patch.object(stopper.urllib.request, "urlopen", return_value=response) as open_url:
            stopper.stop_session({"api_url": "http://127.0.0.1:4321/api", "key": "secret"})
        request = open_url.call_args.args[0]
        self.assertEqual(request.full_url, "http://127.0.0.1:4321/api/stop?key=secret")
        self.assertEqual(request.method, "POST")

    def test_stop_command_stops_the_exact_server_session(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            process = subprocess.Popen(
                [sys.executable, str(VISUAL_SERVER), "--project-dir", temporary, "--port", "0"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                ready, _, _ = select.select([process.stdout], [], [], 5)
                self.assertTrue(ready, "visual server did not announce its session")
                info = json.loads(process.stdout.readline())
                result = subprocess.run(
                    [sys.executable, str(VISUAL_STOP), info["session_dir"]],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                self.assertIn("stopped visual companion session", result.stdout)
                process.wait(timeout=5)
                self.assertIsNotNone(process.returncode)
            finally:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
                if process.stdout is not None:
                    process.stdout.close()
                if process.stderr is not None:
                    process.stderr.close()

    def test_choice_controls_use_valid_toggle_button_state(self) -> None:
        html = VISUAL_COMPANION_TEMPLATE.read_text()
        self.assertNotIn("aria-selected", html)
        self.assertIn("aria-pressed", html)

    def test_server_escapes_session_title_as_html_text(self) -> None:
        hostile_title = '<img src=x onerror="globalThis.injected=true">'
        with tempfile.TemporaryDirectory() as temporary:
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(VISUAL_SERVER),
                    "--project-dir",
                    temporary,
                    "--port",
                    "0",
                    "--title",
                    hostile_title,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                ready, _, _ = select.select([process.stdout], [], [], 5)
                self.assertTrue(ready, "visual server did not announce its session")
                info = json.loads(process.stdout.readline())
                with urllib.request.urlopen(info["url"], timeout=2) as response:
                    html = response.read().decode()
                self.assertNotIn(hostile_title, html)
                self.assertIn("&lt;img src=x onerror=&quot;globalThis.injected=true&quot;&gt;", html)
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout is not None:
                    process.stdout.close()
                if process.stderr is not None:
                    process.stderr.close()

    def test_server_protects_session_and_relays_latest_screen_and_events(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(VISUAL_SERVER),
                    "--project-dir",
                    temporary,
                    "--port",
                    "0",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                ready, _, _ = select.select([process.stdout], [], [], 5)
                self.assertTrue(ready, "visual server did not announce its session")
                info = json.loads(process.stdout.readline())
                self.assertEqual(info["type"], "server-started")
                self.assertTrue(info["url"].startswith("http://"))

                with self.assertRaises(urllib.error.HTTPError) as denied:
                    urllib.request.urlopen(info["url"].split("?", 1)[0], timeout=2)
                self.assertEqual(denied.exception.code, 403)
                denied.exception.close()

                screen_dir = Path(info["screen_dir"])
                (screen_dir / "lane-choice.html").write_text(
                    '<section><button data-choice="poc">PoC</button></section>',
                    encoding="utf-8",
                )
                with urllib.request.urlopen(info["api_url"] + "/latest?key=" + info["key"], timeout=2) as response:
                    payload = json.loads(response.read())
                self.assertEqual(payload["name"], "lane-choice.html")
                self.assertIn('data-choice="poc"', payload["html"])

                request = urllib.request.Request(
                    info["api_url"] + "/events?key=" + info["key"],
                    data=json.dumps({"type": "choice", "choice": "poc"}).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(request, timeout=2) as response:
                    self.assertEqual(response.status, 204)
                event = json.loads((Path(info["state_dir"]) / "events.jsonl").read_text().strip())
                self.assertEqual(event["choice"], "poc")
                self.assertIn("timestamp", event)
            finally:
                process.terminate()
                process.wait(timeout=5)
                if process.stdout is not None:
                    process.stdout.close()
                if process.stderr is not None:
                    process.stderr.close()


if __name__ == "__main__":
    unittest.main()
