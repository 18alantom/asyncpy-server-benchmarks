"""
Stupid Async App

This makes use of async BUT doesn't make use of async io.
The db request is made synchronously.
"""
import json
import urllib.request
from datetime import datetime

from httpcore import AsyncConnectionPool
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse
from starlette.routing import Route

from utils import get_template

template = get_template()
http = AsyncConnectionPool()


async def send_home(request):
    page = template.render(
        server_type="Starlette :: ASGI App (stupid async)",
        date=datetime.now().isoformat(),
    )
    return HTMLResponse(page)


async def send_api(request):
    db_resp = urllib.request.urlopen("http://127.0.0.1:6161").read()
    db_resp_data = json.loads(db_resp)

    data = {"message": "SUCCESS", **db_resp_data}
    return JSONResponse(data)


async def send_404(request):
    return PlainTextResponse("Not Found", status_code=404)


app = Starlette(
    debug=True,
    routes=[
        Route("/", send_home),
        Route("/api", send_api),
    ],
    exception_handlers={404: send_404},
    on_shutdown=[http.aclose],
)
