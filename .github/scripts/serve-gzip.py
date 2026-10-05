"""Serve a directory with gzip, like GitHub Pages, for local Lighthouse checks.

Usage: python serve-gzip.py DIRECTORY [PORT]
"""
import gzip
import http.server
import io
import os
import sys

COMPRESSIBLE = (".html", ".css", ".js", ".json", ".svg", ".txt", ".xml")


class GzipHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
        accepts_gzip = "gzip" in self.headers.get("Accept-Encoding", "")
        if not (accepts_gzip and path.endswith(COMPRESSIBLE)
                and os.path.isfile(path)):
            return super().send_head()
        with open(path, "rb") as source:
            body = gzip.compress(source.read())
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Vary", "Accept-Encoding")
        self.end_headers()
        return io.BytesIO(body)


if __name__ == "__main__":
    directory = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    handler = lambda *args, **kwargs: GzipHandler(  # noqa: E731
        *args, directory=directory, **kwargs)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
