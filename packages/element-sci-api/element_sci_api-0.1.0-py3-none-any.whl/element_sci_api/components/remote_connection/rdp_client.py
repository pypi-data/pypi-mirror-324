import os
import json
from typing import Union, List
from flask import request, Flask, Blueprint


class RDPConnector:
    def __init__(self, service: Union[Flask, Blueprint], url_prefix: str):
        self.service = service
        self.service.add_url_rule(
            f"/{url_prefix}/start_rdp", view_func=self.start_rdp, methods=["POST"]
        )

    def start_rdp(self):
        data = json.loads(request.data)
        ip = data["ip"]
        port = data["port"] if ("port" in data and data["port"]) else 3389
        ret = os.system(f"mstsc /f /v:{ip}:{port}")
        return {"status": "success"}
