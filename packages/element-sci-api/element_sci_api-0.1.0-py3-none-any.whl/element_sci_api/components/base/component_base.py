import functools
import json
from typing import Any, Callable, Union

from flask import Blueprint, Flask, request


class BaseComponent:
    def __init__(
        self,
        component_name: str,
        service: Union[Flask, Blueprint],
        url_prefix: str = "",
    ) -> None:
        self.component_name = component_name
        self.service = service
        self.url_prefix = url_prefix

    def url_concat(self, endpoint: str):
        url_prefix = f"{self.url_prefix}/{self.component_name}".lstrip("/")
        return f"/{url_prefix}/{endpoint}"

    def add_get_method(self, endpoint: str, view_func: Callable):
        """
        添加一个Get方法的映射
        """
        @functools.wraps(view_func)
        def wrapper():
            args = request.args
            # try:
            if len(args) > 0:
                return view_func(args)
            else:
                return view_func()
            # except TypeError as e:
            #     if "unexpected" in str(e) and "argument" in str(e):
            #         raise TypeError(f"The GET handler {view_func} on {endpoint} got error: {e}")
            #     else:
            #         raise e
        self.service.add_url_rule(
            self.url_concat(endpoint), view_func=wrapper, methods=["GET"]
        )

    def add_post_method(self, endpoint: str, view_func):
        """
        添加一个Post方法的映射
        """
        @functools.wraps(view_func)
        def wrapper():
            data = json.loads(request.data)
            if len(data) > 0:
                return view_func(data)
            else:
                return view_func()
        self.service.add_url_rule(
            self.url_concat(endpoint), view_func=wrapper, methods=["POST"]
        )
