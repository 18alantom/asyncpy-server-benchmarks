import json
from datetime import datetime

import urllib.request
from werkzeug.wrappers import Request, Response

from utils import get_template

template = get_template()


@Request.application
def app(request: Request):
    if request.path == "/" and request.method == "GET":
        return send_home()
    elif request.path == "/api" and request.method == "GET":
        return send_api()
    else:
        return send_404()


def send_home():
    page = template.render(
        server_type="Werkzeug :: WSGI App (sync)",
        date=datetime.now().isoformat(),
    )
    return Response(page, mimetype="text/html")


def send_api():
    # get from fake db server
    db_resp = urllib.request.urlopen("http://127.0.0.1:6161").read()
    db_resp_data = json.loads(db_resp)

    resp_data = json.dumps({"message": "SUCCESS", **db_resp_data}).encode()
    return Response(resp_data, mimetype="application/json")


def send_404():
    return Response("Not Found", status=404)
