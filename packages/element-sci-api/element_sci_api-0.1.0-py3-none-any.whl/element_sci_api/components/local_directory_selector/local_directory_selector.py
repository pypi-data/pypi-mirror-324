import os
from typing import Union, List
from flask import request, Flask, Blueprint


class LocalDirectorySelector:
    def __init__(self, service: Union[Flask, Blueprint], url_prefix: str):
        self.service = service
        self.service.add_url_rule(
            f"/{url_prefix}/go_to_parent_dir", view_func=self.go_to_parent
        )
        self.service.add_url_rule(
            f"/{url_prefix}/go_to_sub_dir", view_func=self.go_to_sub
        )
        self.service.add_url_rule(
            f"/{url_prefix}/get_fs_items", view_func=self.get_fs_items
        )

    def go_to_parent(self):
        directory = request.args["directory"]
        if directory == "":
            directory = os.path.join(os.path.expanduser("~"), "Desktop")
        directory = os.path.dirname(directory)
        return {
            "currentDirectory": directory,
            "fsItemsList": self.get_all_file_items(directory),
        }

    def go_to_sub(self):
        directory = request.args["directory"]
        subdir = request.args["subdir"]
        if directory == "":
            directory = os.path.join(os.path.expanduser("~"), "Desktop")
        directory = os.path.join(directory, subdir)
        return {
            "currentDirectory": directory,
            "fsItemsList": self.get_all_file_items(directory),
        }

    def get_fs_items(self):
        directory: str = request.args["directory"]
        if directory == "":
            # directory = os.path.join(os.path.expanduser("~"), "Desktop")
            directory = os.getcwd()
        if os.path.exists(directory):
            return {
                "currentDirectory": directory,
                "fsItemsList": self.get_all_file_items(directory),
            }
        else:
            return f"Directory {directory} does not exist!", 404

    def get_all_file_items(self, directory: str, one_layer=True):
        assert isinstance(directory, str), directory
        items = []
        for root, dirs, files in os.walk(directory):
            if not os.path.samefile(root, directory):
                continue
            else:
                got_dirs = []
                got_files = []
                for dir_name in dirs:
                    got_dirs.append(
                        {
                            "name": dir_name,
                            "type": "directory",
                            "absPath": os.path.join(root, dir_name),
                        }
                    )
                for file in files:
                    got_files.append(
                        {
                            "name": file,
                            "type": "file",
                            "absPath": os.path.join(root, file),
                        }
                    )
            got_dirs.sort(key=lambda item: item["name"])
            got_files.sort(key=lambda item: item["name"])
            items.extend(got_dirs)

            items.extend(got_files)
            if one_layer:
                break

        return items
