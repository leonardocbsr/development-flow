#!/usr/bin/env python3
"""Small authenticated local relay for Development Flow visual decisions."""

from __future__ import annotations

import argparse
import html
import json
import secrets
import threading
import time
import webbrowser
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


SKILL_ROOT = Path(__file__).resolve().parents[1]
FRAME_PATH = SKILL_ROOT / "assets" / "frame.html"
MAX_EVENT_BYTES = 64 * 1024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve a Development Flow visual companion session.")
    parser.add_argument("--project-dir", type=Path, required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--url-host", default=None)
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--title", default="Visual Companion")
    parser.add_argument("--open", action="store_true", dest="open_browser")
    return parser.parse_args()


class Session:
    def __init__(self, project_dir: Path, title: str) -> None:
        project = project_dir.expanduser().resolve()
        project.mkdir(parents=True, exist_ok=True)
        session_name = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + f"-{secrets.token_hex(3)}"
        self.root = project / ".development-flow" / "visual-companion" / session_name
        self.content = self.root / "content"
        self.state = self.root / "state"
        self.content.mkdir(parents=True)
        self.state.mkdir(parents=True)
        self.key = secrets.token_urlsafe(24)
        self.title = title
        self.event_lock = threading.Lock()

    def latest(self) -> dict[str, str | int | None]:
        screens = sorted(
            self.content.glob("*.html"),
            key=lambda path: (path.stat().st_mtime_ns, path.name),
        )
        if not screens:
            return {"name": None, "html": "", "version": 0}
        latest = screens[-1]
        return {
            "name": latest.name,
            "html": latest.read_text(encoding="utf-8"),
            "version": latest.stat().st_mtime_ns,
        }

    def record_event(self, event: dict[str, object]) -> None:
        event = dict(event)
        event["timestamp"] = datetime.now(timezone.utc).isoformat()
        line = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
        with self.event_lock:
            with (self.state / "events.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(line + "\n")


def make_handler(session: Session):
    frame = FRAME_PATH.read_text(encoding="utf-8")

    class Handler(BaseHTTPRequestHandler):
        server_version = "DevelopmentFlowVisual/0.1"

        def log_message(self, format: str, *args: object) -> None:
            return

        def authorized(self) -> bool:
            query = parse_qs(urlparse(self.path).query)
            return secrets.compare_digest(query.get("key", [""])[0], session.key)

        def send_bytes(self, status: HTTPStatus, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def send_json(self, status: HTTPStatus, value: object) -> None:
            self.send_bytes(status, json.dumps(value, ensure_ascii=False).encode(), "application/json; charset=utf-8")

        def reject(self) -> None:
            self.send_json(HTTPStatus.FORBIDDEN, {"error": "invalid session key"})

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if not self.authorized():
                self.reject()
                return
            if parsed.path == "/":
                safe_title = html.escape(session.title, quote=True)
                body = frame.replace("__SESSION_KEY__", session.key).replace("__SESSION_TITLE__", safe_title)
                self.send_bytes(HTTPStatus.OK, body.encode(), "text/html; charset=utf-8")
                return
            if parsed.path == "/api/latest":
                self.send_json(HTTPStatus.OK, session.latest())
                return
            if parsed.path == "/api/health":
                self.send_json(HTTPStatus.OK, {"status": "ok"})
                return
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            if not self.authorized():
                self.reject()
                return
            if parsed.path == "/api/stop":
                self.send_response(HTTPStatus.NO_CONTENT)
                self.end_headers()
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return
            if parsed.path != "/api/events":
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = 0
            if length <= 0 or length > MAX_EVENT_BYTES:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid event size"})
                return
            try:
                event = json.loads(self.rfile.read(length))
            except (json.JSONDecodeError, UnicodeDecodeError):
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid JSON"})
                return
            if not isinstance(event, dict):
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "event must be an object"})
                return
            session.record_event(event)
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()

    return Handler


def main() -> None:
    args = parse_args()
    session = Session(args.project_dir, args.title)
    server = ThreadingHTTPServer((args.host, args.port), make_handler(session))
    port = server.server_address[1]
    url_host = args.url_host or ("127.0.0.1" if args.host == "0.0.0.0" else args.host)
    base_url = f"http://{url_host}:{port}"
    info = {
        "type": "server-started",
        "pid": __import__("os").getpid(),
        "port": port,
        "url": f"{base_url}/?key={session.key}",
        "api_url": f"{base_url}/api",
        "key": session.key,
        "screen_dir": str(session.content),
        "state_dir": str(session.state),
        "session_dir": str(session.root),
    }
    (session.state / "server-info.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(info), flush=True)
    if args.open_browser:
        threading.Timer(0.2, webbrowser.open, args=(info["url"],)).start()
    try:
        server.serve_forever(poll_interval=0.25)
    finally:
        server.server_close()
        (session.state / "server-stopped").write_text(str(time.time()) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
