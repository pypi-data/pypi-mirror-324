import json
from typing import List, Union
from flask import Flask, Blueprint, request
from .params import ParamsManager, ParamsType


class DynamicForm:
    def __init__(
        self,
        service: Union[Flask, Blueprint],
        url_prefix: str,
        params: List[ParamsType],
    ):
        self.service = service
        # self.blueprint_dynamic_form = Blueprint(url_prefix, '_blueprint_name_'+ url_prefix)
        # print("created blueprint", self.blueprint_dynamic_form)
        # self.service.register_blueprint(self.blueprint_dynamic_form)
        self.service.add_url_rule(
            f"/{url_prefix}/all_params", view_func=self.get_all_params
        )
        self.service.add_url_rule(
            f"/{url_prefix}/initial_data", view_func=self.get_initial_data
        )
        self.service.add_url_rule(
            f"/{url_prefix}/update_values", view_func=self.update_values
        )
        self.params_manager = ParamsManager()
        for param in params:
            self.params_manager.add_param(param)

    def get_initial_data(self):
        return self.params_manager.to_frontend_model()

    def get_all_params(self):
        return self.params_manager.to_json()

    def update_values(self, **kwargs):
        """Update values of parameters"""
        data = json.loads(request.data)
        print(data)
