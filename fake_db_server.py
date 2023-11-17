#!/usr/bin/env python

"""
Fake DB Server is a proxy for a DB server to add fake latency when
handling "database" calls.

The async server runs sufficiently fast at around 44k requests/second

Additional (fake) latency can be applied per request by using
    `./fake_db_server.py --sleep $MILLI_SECONDS`

Remaining of the flags are passed through to the Uvicorn config.
"""

import time

from rng_server.response import get_body
from utils import get_kwargs_from_argv


def app_factory():
    config = get_kwargs_from_argv()
    sleep = 0

    if "sleep" in config:
        sleep = config["sleep"] / 1000

    async def app(scope, receive, send):
        assert scope["type"] == "http"
        if scope["path"] != "/":
            return await send_404(send)

        if sleep > 0:
            time.sleep(sleep)

        await send_200(send)

    return app


async def send_404(send):
    await send(
        {
            "type": "http.response.start",
            "status": 404,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        }
    )
    await send({"type": "http.response.body", "body": b"Not found"})


async def send_200(send):
    data = get_body()
    data_len = str(len(data)).encode()
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-length", data_len],
                [b"content-type", b"application/json"],
            ],
        }
    )
    await send({"type": "http.response.body", "body": data})


def run_server():
    global config
    import multiprocessing

    import uvicorn

    kwargs = get_kwargs_from_argv()

    options = {
        "port": 6161,
        "log_level": "error",
        "workers": (multiprocessing.cpu_count() * 2) + 1,
        **kwargs,
    }

    options["factory"] = True
    if "sleep" in options:
        del options["sleep"]

    print(options)
    config = uvicorn.Config("fake_db_server:app_factory", **options)
    server = uvicorn.Server(config)

    server.run()


if __name__ == "__main__":
    run_server()
