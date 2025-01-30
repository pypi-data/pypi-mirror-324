import json
import os
from typing import Union

from flask import Blueprint, Flask, request, jsonify
from ....app.sci_app import SciApp
from ..component_base import BaseComponent


class DraggingCanvas(BaseComponent):
    def __init__(
        self,
        component_name: str,
        service: Union[Flask, Blueprint],
        url_prefix: str = "",
    ) -> None:
        super().__init__(component_name, service, url_prefix)
        self.add_get_method("load_layout", self.load_layout)
        self.add_post_method("save_layout", self.save_layout)

    def save_layout(self, data):
        """
        保存布局
        """
        # data = json.loads(data)
        file_manager = SciApp.getInstance().configs_file_manager
        layout_file = file_manager.get_abspath("layouts/layout.json")
        layout_data = data["layout"]
        err = file_manager.json_dump(layout_data, layout_file)
        if err is not None:
            return err, 400
        else:
            return "Save layout succeeded", 200

    def load_layout(self):
        """
        加载布局
        """
        file_manager = SciApp.getInstance().configs_file_manager
        layout_file = file_manager.get_abspath("layouts/layout.json")
        if os.path.exists(layout_file):
            layout_data = file_manager.json_load(layout_file)
            return jsonify(layout_data), 200
        else:
            return "Layout file does not exist", 400
