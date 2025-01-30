import json
import os
from typing import Any, Union
from ..utils.files import decorator_path_ensure
import logging
logger = logging.getLogger("FileManager")


class FileManager:
    def __init__(self, base_dir: str, auto_create_folder=True) -> None:
        self.dir = os.path.abspath(base_dir)
        logger.info(f"FileManager created with base_dir={self.dir}")
        self.auto_create_folder = auto_create_folder
        if self.auto_create_folder:
            self.ensure_folder_exist(self.dir)
        assert os.path.exists(self.dir)

    def get_abspath(self, file_relpath: str) -> str:
        assert not file_relpath.startswith("/")
        return os.path.abspath(os.path.join(self.dir, file_relpath))

    def ensure_folder_exist(self, folder_path: str):
        folder_path = self.get_abspath(folder_path)
        if self.auto_create_folder:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def json_load(self, file_relpath: str):
        """
        Load json from file
        """
        file = self.get_abspath(file_relpath)
        with open(file, "r") as f:
            return json.load(f)

    def json_load_with_default(self, file_relpath: str, default: Union[list, dict]):
        """
        Load json from file, if file not exist, return default value and create this file.
        """
        file = self.get_abspath(file_relpath)
        if not os.path.exists(file):
            self.json_dump(default, file_relpath)
        with open(file, "r") as f:
            return json.load(f)

    @decorator_path_ensure
    def json_dump(self, data: Any, file_relpath: str, indent=2, ensure_ascii=False):
        """
        Dump json to file.
        Be careful that the `ensure_ascii` parameter was `False` by default,
          different from the standard library `json`.
        """
        assert file_relpath.endswith(".json"), "extension should be *.json"
        file = self.get_abspath(file_relpath)
        with open(file, "w") as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
