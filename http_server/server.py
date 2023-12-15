import argparse
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

SUPPORT_METHOD = set(["HEAD", "GET", "DELETE", "POST", "PUT", "PATCH"])
RED_COLOR_IN = "\033[1;31m"
RED_COLOR_OUT = "\033[00m"
FORMAT = f"%(asctime)s\t\t%(message)s%(contents)s"

logging.basicConfig(format=FORMAT, level=logging.INFO)


def log(message, contents=""):
    if message in SUPPORT_METHOD:
        message = f"Method: {RED_COLOR_IN}{message}{RED_COLOR_OUT}"
    contents = f"\n\t\t\t\tContents: {contents}" if contents else ""

    logging.info(message, extra={"contents": contents})


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def process(self, http_method: str) -> None:
        if not (length := self.headers.get("content-length")):
            length = 0
        data = self.rfile.read(int(length)).decode("utf-8")
        json_data = json.dumps(data, indent=4)

        log(http_method, contents=json_data)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json_data.encode("utf-8"))

    def log_message(self, *args, **kwargs):
        pass

    def do_HEAD(self) -> None:
        self.process(http_method="HEAD")

    def do_GET(self) -> None:
        self.process(http_method="GET")

    def do_DELETE(self) -> None:
        self.process(http_method="DELETE")

    def do_POST(self) -> None:
        self.process(http_method="POST")

    def do_PUT(self) -> None:
        self.process(http_method="PUT")

    def do_PATCH(self) -> None:
        self.process(http_method="PATCH")


def main(port: int) -> None:
    server = HTTPServer(("", port), HTTPRequestHandler)
    try:
        print(f"Listening on localhost:{port} ...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Close the HTTP server.")
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Simple HTTP Server", description="The title says it all."
    )
    parser.add_argument("port", default=8000, type=int)
    args = parser.parse_args()

    main(args.port)
