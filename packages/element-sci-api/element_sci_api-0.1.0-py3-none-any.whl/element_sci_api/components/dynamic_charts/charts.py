import json
from typing import Any, Generic, TypeVar

from flask_sock import Sock
from ...api import BaseFlaskSock
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

T = TypeVar("T")


class DynamicChartComponent(BaseFlaskSock, Generic[T]):
    pass


class DynamicEChartComponent(BaseFlaskSock, Generic[T]):
    def __init__(self, sock: Sock, rel_url: str, initial_data: Any):
        super().__init__(sock, rel_url)
        self.initial_data = initial_data

    # def format_initial_data(self):
    #     raise NotImplementedError("Must return initial data here")

    def on_open(self, ws):
        ws.send(json.dumps(self.initial_data))
