import requests
import argparse
import json

DATA = {"User": "Patrick"}
HEADERS = {"Content-type": "application/json"}


def request_HEAD(url) -> None:
    requests.head(url, data=json.dumps(DATA), headers=HEADERS)


def request_GET(url) -> None:
    requests.get(url)


def request_DELETE(url) -> None:
    requests.delete(url, data=json.dumps(DATA), headers=HEADERS)


def request_POST(url) -> None:
    requests.post(url, data=json.dumps(DATA), headers=HEADERS)


def request_PUT(url) -> None:
    requests.put(url, data=json.dumps(DATA), headers=HEADERS)


def request_PATCH(url) -> None:
    requests.patch(url, data=json.dumps(DATA), headers=HEADERS)


def main(port: int) -> None:
    url = f"http://localhost:{port}"
    for func in [
        request_HEAD,
        request_GET,
        request_DELETE,
        request_POST,
        request_PUT,
        request_PATCH,
    ]:
        func(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Simple HTTP Client for testing",
    )
    parser.add_argument("port", default=8000, type=int)
    args = parser.parse_args()

    main(args.port)
