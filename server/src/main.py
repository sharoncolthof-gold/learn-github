# import http.server
# import socketserver

# PORT = 8080

# class Handler(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/plain; charset=utf-8')
#         self.end_headers()
#         self.wfile.write("Hello from Server Container!".encode('utf-8'))

# if __name__ == "__main__":
#     with socketserver.TCPServer(("", PORT), Handler) as httpd:
#         print(f"Server running on port {PORT}...")
#         httpd.serve_forever()


"""Simple HTTP Server for app_server component."""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class AppRequestHandler(BaseHTTPRequestHandler):
    """Request handler implementing /health, /hello, and /echo."""

    def _send_json_response(self, status_code: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/health":
            self._send_json_response(
                200,
                {
                    "status": "ok",
                    "service": "app_server",
                    "version": "1.0.0",
                },
            )
        elif path == "/hello":
            name = query.get("name", ["World"])[0]
            self._send_json_response(
                200,
                {
                    "message": f"Hello, {name}!",
                    "service": "app_server",
                },
            )
        else:
            self._send_json_response(
                404,
                {
                    "error": "Not Found",
                    "path": path,
                },
            )

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/echo":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)
            try:
                payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
            except json.JSONDecodeError:
                payload = {"raw": raw_body.decode("utf-8", errors="replace")}

            self._send_json_response(
                200,
                {
                    "service": "app_server",
                    "echo": payload,
                },
            )
        else:
            self._send_json_response(
                404,
                {
                    "error": "Not Found",
                    "path": parsed.path,
                },
            )

    def log_message(self, format, *args):
        # Format log messages neatly to stdout
        sys.stdout.write(f"[app_server] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()


def run_server(host: str = "0.0.0.0", port: int = 8080):
    server = ThreadingHTTPServer((host, port), AppRequestHandler)
    print(f"[app_server] Starting server at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[app_server] Server shutting down...")
    finally:
        server.server_close()


if __name__ == "__main__":
    host = os.environ.get("SERVER_HOST", "0.0.0.0")
    port = int(os.environ.get("SERVER_PORT", "8080"))
    run_server(host, port)
