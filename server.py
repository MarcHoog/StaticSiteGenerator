import os
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler


class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

def run(
    server_class=HTTPServer,
    handler_class=CORSHTTPRequestHandler,
    port=8888,
    directory=None,
):
    if directory:  # Change the current working directory if directory is specified
        os.chdir(directory)
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving HTTP on http://localhost:{port} from directory '{directory}'...")
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP Server with CORS")
    parser.add_argument(
        "--dir", type=str, help="Directory to serve files from", default="./public"
    )
    parser.add_argument("--port", type=int, help="Port to serve HTTP on", default=8080)
    args = parser.parse_args()

    run(port=args.port, directory=args.dir)