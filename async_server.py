import asyncio
import json
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
        server_type="Starlette :: ASGI App (async)",
        date=datetime.now().isoformat(),
    )
    return HTMLResponse(page)


async def send_api(request):
    resp = await http.request("GET", "http://127.0.0.1:6161")
    data = {"message": "SUCCESS", **json.loads(resp.content)}
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
