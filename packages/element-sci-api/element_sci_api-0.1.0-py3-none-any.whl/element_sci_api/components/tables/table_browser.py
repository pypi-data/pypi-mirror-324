from typing import Any, Union, Dict, List

from flask import Blueprint, Flask
from ..base.component_base import BaseComponent
from dataclasses_json import DataClassJsonMixin, config
from dataclasses import dataclass, field


@dataclass
class QueriedData(DataClassJsonMixin):
    total_records: int = field(metadata=config(
        field_name="totalRecords"))
    data: List[Dict[str, Any]]
    fields: List[Dict[str, str]]


class TableBrowserComponent(BaseComponent):
    def __init__(self, component_name: str, service: Union[Flask, Blueprint], url_prefix: str = "") -> None:
        super().__init__(component_name, service, url_prefix)
        self.add_get_method("table_names", self.get_table_names)
        self.add_get_method("query", self.query_data)

    def get_table_names(self):
        return ["hello", "aaaaa", "bbbbbb"]

    def query_data(self) -> QueriedData:
        return QueriedData([
            {"name": "aaa", "age": 12},
            {"name": "aab", "age": 13},
        ],  [{"name": "name", "type": "string"}, {"name": "age", "type": "int"}]
        ).to_dict()
