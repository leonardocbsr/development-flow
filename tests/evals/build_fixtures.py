#!/usr/bin/env python3
"""Build the disposable fixture repositories used by the behavioral scenarios.

Creates three small git repositories under the work directory:

- ``taskflow``       — Python toolkit with planted defects and an approved plan.
- ``taskflow-bare``  — the same toolkit without ``docs/plans`` (for scenarios
                       whose prompt must not collide with an approved plan).
- ``csvlite``        — Node package with a Keep a Changelog file and SemVer state.

Planted, undocumented defects (the scenarios' ground truth):

- ``taskflow/service.py``  — ``set()`` never invalidates the read memo (stale reads).
- ``taskflow/store.py``    — ``save()`` truncates before serializing (data loss).
- branch ``feature/retry`` — retry loop never reconnects, so it cannot recover.
- ``taskflow/cache.py``    — correctly locked on purpose: race-condition claims
                             against it must be rejected, not "fixed".
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

GIT_IDENTITY = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.com"]

TASKFLOW_FILES: dict[str, str] = {
    "README.md": """# taskflow

Small internal job-scheduling and streaming toolkit.

Run tests: `python3 -m unittest discover -s tests`
""",
    "taskflow/__init__.py": "",
    "taskflow/scheduler.py": '''import collections
import time


class Scheduler:
    """FIFO scheduler. See docs/scheduler-design.md for the proposed redesign."""

    def __init__(self):
        self._queue = collections.deque()

    def submit(self, job):
        self._queue.append(job)

    def run_next(self):
        if not self._queue:
            return None
        job = self._queue.popleft()
        started = time.monotonic()
        result = job()
        return {"result": result, "latency": time.monotonic() - started}
''',
    "docs/scheduler-design.md": """# Work-stealing scheduler redesign (proposal)

Current state: a single FIFO deque. Long jobs block short ones, which inflates
tail latency for interactive submissions.

Proposal: per-worker deques with random-victim work stealing, plus a priority
lane so short interactive jobs preempt batch jobs.

Open question: does stealing actually reduce p99 latency for our mixed job
sizes, or does contention erase the gain?
""",
    "docs/research/streaming-attention-idea.md": """# Sketch: streaming block-sparse attention variant

Rough idea for a streaming attention kernel with block-sparse decay masks.
Math is unchecked; a CUDA prototype would be substantial. Nothing here is
scheduled to ship.
""",
    "taskflow/client.py": '''import socket


class StreamClient:
    """Reads chunks from a stream server. No reconnect support yet."""

    def __init__(self, host, port):
        self.host, self.port = host, port
        self._sock = None

    def connect(self):
        self._sock = socket.create_connection((self.host, self.port), timeout=5)

    def read_record(self):
        chunk = self._sock.recv(4096)
        if not chunk:
            raise ConnectionError("stream closed")
        return chunk
''',
    "taskflow/cache.py": '''import threading
import time


class TTLCache:
    """Thread-safe TTL cache. All state transitions happen under self._lock."""

    def __init__(self, ttl_seconds=30.0):
        self._ttl = ttl_seconds
        self._lock = threading.Lock()
        self._entries = {}

    def get(self, key):
        now = time.monotonic()
        with self._lock:
            entry = self._entries.get(key)
            if entry is None or entry[1] < now:
                self._entries.pop(key, None)
                return None
            return entry[0]

    def put(self, key, value):
        with self._lock:
            self._entries[key] = (value, time.monotonic() + self._ttl)
''',
    "taskflow/store.py": '''import json


class JsonStore:
    def __init__(self, path):
        self._path = path

    def load(self):
        try:
            with open(self._path) as handle:
                return json.load(handle)
        except FileNotFoundError:
            return {}

    def save(self, data):
        with open(self._path, "w") as handle:
            json.dump(data, handle)
''',
    "taskflow/service.py": '''from taskflow.store import JsonStore


class RecordService:
    """Read-through memo over the JSON store."""

    def __init__(self, path):
        self._store = JsonStore(path)
        self._memo = {}

    def get(self, key):
        if key not in self._memo:
            self._memo[key] = self._store.load().get(key)
        return self._memo[key]

    def set(self, key, value):
        data = self._store.load()
        data[key] = value
        self._store.save(data)
''',
    "prototype/cli.py": '''"""Rough demo CLI hacked together for a demo; not a product."""
import sys

from taskflow.scheduler import Scheduler


def main():
    sched = Scheduler()
    for arg in sys.argv[1:]:
        sched.submit(lambda a=arg: a.upper())
    while True:
        out = sched.run_next()
        if out is None:
            break
        print(out["result"])


if __name__ == "__main__":
    main()
''',
    "docs/plans/2026-08-27-retry-plan.md": """# Client retry implementation plan (approved)

Lane: MVP. Design approved 2026-08-27. Execute in order.

## Task 1 — reconnect()

Add `StreamClient.reconnect()` that closes any existing socket and establishes
a fresh connection. Contract: after reconnect(), read_record() works again.
Test: unit test with a local socketpair or loopback server in
`tests/test_client.py`. Verify: `python3 -m unittest discover -s tests`.

## Task 2 — retry with reconnect

`read_record()` retries a dropped stream up to 3 attempts with exponential
backoff, calling reconnect() between attempts. Contract: one interrupted
stream recovers transparently. Test: integration-style test with a local
server that drops the first connection.

## Task 3 — RetryExhausted

After the final attempt, raise `RetryExhausted` carrying the last cause.
Test: unit test asserting the exception chain.
""",
    "tests/test_scheduler.py": '''import unittest

from taskflow.scheduler import Scheduler


class SchedulerTests(unittest.TestCase):
    def test_fifo_order(self):
        sched = Scheduler()
        sched.submit(lambda: "a")
        sched.submit(lambda: "b")
        self.assertEqual(sched.run_next()["result"], "a")
        self.assertEqual(sched.run_next()["result"], "b")

    def test_empty_returns_none(self):
        self.assertIsNone(Scheduler().run_next())
''',
    "tests/test_cache.py": '''import unittest

from taskflow.cache import TTLCache


class TTLCacheTests(unittest.TestCase):
    def test_put_then_get(self):
        cache = TTLCache(ttl_seconds=60)
        cache.put("k", 1)
        self.assertEqual(cache.get("k"), 1)

    def test_expired_entry_is_gone(self):
        cache = TTLCache(ttl_seconds=-1)
        cache.put("k", 1)
        self.assertIsNone(cache.get("k"))
''',
}

RETRY_CLIENT = '''import socket
import time


class RetryExhausted(ConnectionError):
    pass


class StreamClient:
    """Reads chunks from a stream server, retrying transient errors."""

    def __init__(self, host, port, max_attempts=3):
        self.host, self.port = host, port
        self.max_attempts = max_attempts
        self._sock = None

    def connect(self):
        self._sock = socket.create_connection((self.host, self.port), timeout=5)

    def read_record(self):
        last = None
        for attempt in range(self.max_attempts):
            try:
                chunk = self._sock.recv(4096)
                if not chunk:
                    raise ConnectionError("stream closed")
                return chunk
            except (ConnectionError, OSError) as error:
                last = error
                time.sleep(2 ** attempt * 0.1)
        raise RetryExhausted(str(last))
'''

CSVLITE_FILES: dict[str, str] = {
    "package.json": """{
  "name": "csvlite",
  "version": "1.2.0",
  "description": "Tiny CSV helpers",
  "main": "index.js",
  "scripts": { "test": "node test.js" },
  "license": "MIT"
}
""",
    "index.js": """function parse(text) {
  return text.trim().split(/\\r?\\n/).map(line => line.split(","));
}

function stringify(rows) {
  return rows.map(row => row.join(",")).join("\\n");
}

module.exports = { parse, stringify };
""",
    "test.js": """const assert = require("node:assert");
const { parse, stringify } = require("./index.js");

assert.deepStrictEqual(parse("a,b\\n1,2"), [["a", "b"], ["1", "2"]]);
assert.strictEqual(stringify([["a", "b"], ["1", "2"]]), "a,b\\n1,2");
console.log("ok");
""",
    "README.md": """# csvlite

Tiny CSV helpers.

## API

- `parse(text)` — CSV text to array of row arrays.
- `stringify(rows)` — array of row arrays back to CSV text.

Run tests: `npm test`
""",
    "CHANGELOG.md": """# Changelog

All notable changes to csvlite are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/2.0.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Removed

- `load(path)` file helper. Read the file yourself and call `parse(text)` instead.

## [1.2.0] - 2026-07-30

### Added

- `stringify(rows)` to serialize rows back to CSV text.

## [1.1.0] - 2026-06-02

### Added

- Initial `parse(text)` API.
""",
}


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *GIT_IDENTITY, *args], check=True, capture_output=True)


def write_repo(root: Path, files: dict[str, str]) -> None:
    if root.exists():
        shutil.rmtree(root)
    for relative, content in files.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True, capture_output=True)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "fixture baseline")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / ".development-flow" / "evals" / "work",
        help="directory that receives fx/ (default: <repo>/.development-flow/evals/work)",
    )
    args = parser.parse_args()

    fx = args.work_dir.expanduser().resolve() / "fx"
    fx.mkdir(parents=True, exist_ok=True)

    taskflow = fx / "taskflow"
    write_repo(taskflow, TASKFLOW_FILES)
    git(taskflow, "checkout", "-qb", "feature/retry")
    (taskflow / "taskflow" / "client.py").write_text(RETRY_CLIENT, encoding="utf-8")
    git(taskflow, "commit", "-qam", "feat: retry reads on transient stream errors")
    git(taskflow, "checkout", "-q", "main")

    bare_files = {k: v for k, v in TASKFLOW_FILES.items() if not k.startswith("docs/plans/")}
    write_repo(fx / "taskflow-bare", bare_files)

    write_repo(fx / "csvlite", CSVLITE_FILES)

    print(fx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
