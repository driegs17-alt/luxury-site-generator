#!/usr/bin/env python3
"""
Local dev server: serves the generated site and provides a /submit endpoint
that saves lead emails to leads/emails.json.
Run from project root. Generate site with --leads-action pointing at this server.
"""

import json
import os
from datetime import datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PROJECT_ROOT = Path(__file__).resolve().parent
LEADS_JSON = PROJECT_ROOT / "leads" / "emails.json"
SUBMIT_PATH = "/submit"


class LeadCaptureHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        self.base_directory = directory or PROJECT_ROOT
        super().__init__(*args, directory=str(self.base_directory), **kwargs)

    def do_POST(self):
        if self.path != SUBMIT_PATH:
            self.send_error(404)
            return
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8", errors="replace")
        parsed = parse_qs(body)
        email = (parsed.get("email") or [None])[0]
        if not email or "@" not in email:
            self.send_response(400)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Invalid email")
            return
        # Load, append, save
        entries = []
        if LEADS_JSON.exists():
            try:
                entries = json.loads(LEADS_JSON.read_text())
            except (json.JSONDecodeError, OSError):
                pass
        if not isinstance(entries, list):
            entries = []
        entries.append({
            "email": email.strip(),
            "source": "website",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        LEADS_JSON.parent.mkdir(parents=True, exist_ok=True)
        LEADS_JSON.write_text(json.dumps(entries, indent=2), encoding="utf-8")
        # Redirect back to home so user sees the site again
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Serve site and /submit lead endpoint")
    parser.add_argument("-d", "--dir", default="output", help="Directory to serve (default: output)")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port (default: 8080)")
    parser.add_argument("--bind", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    args = parser.parse_args()
    directory = Path(args.dir).resolve()
    if not directory.exists():
        directory.mkdir(parents=True)
    endpoint = f"http://{args.bind}:{args.port}{SUBMIT_PATH}"
    print(f"Serving {directory} at http://{args.bind}:{args.port}")
    print(f"Lead form endpoint: {endpoint}")
    print("Generate site with: python3 generator.py <template> -o output --leads-action", endpoint)
    server = HTTPServer(
        (args.bind, args.port),
        lambda r, a, s: LeadCaptureHandler(r, a, s, directory=directory),
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down")
        server.shutdown()


if __name__ == "__main__":
    main()
