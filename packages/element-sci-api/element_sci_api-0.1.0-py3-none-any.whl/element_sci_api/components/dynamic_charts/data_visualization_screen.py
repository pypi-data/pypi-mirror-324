import os
from ..base import BaseComponent, DraggingCanvas
from ...app import SciApp
from flask import Flask, Blueprint
from typing import Callable, Union


class DataVisualizationLargeScreen(BaseComponent):
    def __init__(
        self,
        component_name: str,
        service: Union[Flask, Blueprint],
        chart_options_getter: Union[Callable[[], dict], dict],
        url_prefix: str = "",
        default_chart_style_options: dict = None,
    ):
        super().__init__(component_name, service, url_prefix)
        self.chart_options_getter = chart_options_getter if callable(
            chart_options_getter) else lambda: chart_options_getter
        self.chart_style_options = default_chart_style_options
        self.draggingContainer = DraggingCanvas(
            f"{self.component_name}.dragging-canvas", self.service
        )
        self.add_get_method("chart_options", self.get_chart_options)
        self.add_get_method("chart_style_options",
                            self.get_chart_style_options)
        self.add_post_method("save_chart_style_config",
                             self.save_chart_style_config)

    def get_chart_options(self):
        return self.chart_options_getter()

    def get_chart_style_options(self):
        """
        Get chart style options.
        """
        sci_app = SciApp.getInstance()
        file_manager = sci_app.configs_file_manager
        config_file_path = file_manager.get_abspath(
            f"chart_configs/{self.component_name}/chart_config.json")
        if os.path.exists(config_file_path):
            self.chart_style_options = file_manager.json_load(config_file_path)
        return self.chart_style_options

    def save_chart_style_config(self, data: dict):
        """
        Save the chart style config to the file system
        """
        chart_name, chart_style_config = data["chartName"], data["config"]
        self.chart_style_options[chart_name] = chart_style_config

        sci_app = SciApp.getInstance()
        file_manager = sci_app.configs_file_manager
        config_file_path = file_manager.get_abspath(
            f"chart_configs/{self.component_name}/chart_config.json")

        # if os.path.exists(config_file_path):
        file_manager.json_dump(self.chart_style_options, config_file_path)
        # 创建新的
        return "Saving Layout successful", 200
