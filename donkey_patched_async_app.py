"""
Donkey Patched Async App

This makes use of async but the root doesn't run async only everything
inside a single request runs async, i.e for every request an event loop
is created to evaluate the coroutine using `async.run`.
"""
import json
from datetime import datetime

from httpcore import AsyncConnectionPool
from werkzeug.wrappers import Request, Response

from utils import async_to_sync, get_template

http = AsyncConnectionPool()

template = get_template()


@Request.application
@async_to_sync
async def app(request: Request):
    if request.path == "/" and request.method == "GET":
        return await send_home()
    elif request.path == "/api" and request.method == "GET":
        return await send_api()
    else:
        return await send_404()


async def send_home():
    page = template.render(
        server_type="Werkzeug :: WSGI App (donkey patched async)",
        date=datetime.now().isoformat(),
    )
    return Response(page, mimetype="text/html")


async def send_api():
    # get from fake db server
    async with AsyncConnectionPool() as http:
            resp = await http.request("GET", "http://127.0.0.1:6161")

    resp_data = json.dumps({"message": "SUCCESS", **json.loads(resp.content)}).encode()
    return Response(resp_data, mimetype="application/json")


async def send_404():
    return Response("Not Found", status=404)
