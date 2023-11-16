import json
from datetime import datetime
from random import random


def get_body():
    content = dict(
        timestamp=datetime.timestamp(datetime.now()),
        data=random(),
    )
    return json.dumps(content).encode()
