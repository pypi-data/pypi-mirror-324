import base64
import json
import mimetypes
import os
import shutil
from typing import Any, Callable, Union, Tuple


def parse_dataurl(dataurl: str):
    """
    解析前端传来的dataurl
    """
    if not dataurl.startswith("data:"):
        raise ValueError("Invalid DataURL")

    # 提取 MIME 类型和编码后的数据
    mime_type, encoded_data = dataurl[5:].split(";base64,", 1)

    # 解码数据
    decoded_data = base64.b64decode(encoded_data)

    return mime_type, decoded_data


def file_to_dataurl(file_path: str):
    """
    将文件转为dataurl
    """
    mimetype, _ = mimetypes.guess_type(file_path, strict=True)
    with open(file_path, "rb") as file:
        file_content = file.read()
        data_url = base64.b64encode(file_content).decode("ascii")

        return f"data:{mimetype};base64,{data_url}"


def convert_encodings(
    src_folder: str,
    file_filter: Callable[[str], bool],
    src_encoding: Union[str, Callable[[str], str]],
    dst_encoding: Union[str, Callable[[str], str]],
    dst_folder: str,
    errors: str = "replace",
):
    """
    中文：

    将``src_folder``文件夹下指定类型的文件，转换为指定的编码方式。

    :src_folder: 待转换的文件所在的文件夹
    :file_filter: 一个函数，输入为文件名(str)，输出True或者False，代表是否转换此文件的编码方式。
        例如输入``lambda name: name.endswith('.c')``，可以过滤出所有以``.c``结尾的文件
    :src_encoding: 源文件编码方式。如果输入一个字符串如``"gb2312"``，那么会假定所有输入文件均为gb2312编码。
        也可以输入一个函数，通过文件的绝对路径，选择解析该文件的编码方式。
        （当然，你可以在这个回调函数里面调用chardet来达到目的）
    :dst_encoding: 目标编码方式。如果输入一个字符串如``"utf8"``，那么会将所有文件均转为utf8编码。
        也可以输入一个函数，通过原文件的绝对路径，选择该文件的编码方式
    :dst_folder:  目标文件夹路径。如果值与src_folder相等，则代表在原文件上直接更改编码方式
    :errors: 处理编码方式错误的方法。默认为``"replace"``。可用的取值与``open``中的``errors``参数相同
    """

    # 如果目标文件夹为空，则使用源文件夹作为目标文件夹
    if not dst_folder:
        dst_folder = src_folder
    get_src_encoding = (
        src_encoding if callable(src_encoding) else (lambda _: src_encoding)
    )
    get_dst_encoding = (
        dst_encoding if callable(dst_encoding) else (lambda _: dst_encoding)
    )

    # 遍历源文件夹中的所有文件
    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            relpath = os.path.relpath(root, src_folder)
            dst_file_dir = os.path.join(dst_folder, relpath)
            dst_file_path = os.path.join(dst_file_dir, file)

            # 使用文件过滤器判断是否需要转换编码
            if file_filter(file_path):
                # 获取文件的原始编码
                _src_encoding = get_src_encoding(file_path)
                # 获取期望输出的编码方式
                _dst_encoding = get_dst_encoding(file_path)

                # 转换文件编码
                if _src_encoding != _dst_encoding:
                    with open(file_path, "rb") as f:
                        raw_data = f.read()

                    converted_data = raw_data.decode(
                        _src_encoding, errors=errors
                    ).encode(_dst_encoding, errors=errors)

                    # 若输出路径不存在，则创建
                    if not os.path.exists(dst_file_dir):
                        os.makedirs(dst_file_dir)

                    # 保存转换后的文件到目标文件夹
                    with open(dst_file_path, "wb") as f:
                        f.write(converted_data)
                else:
                    # 如果源编码和目标编码相同，则直接复制文件到目标文件夹
                    dst_file_path = os.path.join(dst_folder, file)
                    shutil.copy(file_path, dst_file_path)


def abspath_from_current_file(rel_path: str, current_file: str) -> str:
    """
    Convert the relative path to absolute path.

    TODO: Deprecated method
    """
    return os.path.abspath(
        os.path.join(
            os.path.dirname(current_file),
            rel_path,
        )
    )


def abspath_from_file(rel_path: str, file: str) -> str:
    """
    Convert the relative path to absolute path.
    """
    return os.path.abspath(
        os.path.join(
            os.path.dirname(file),
            rel_path,
        )
    )


def decorator_path_ensure(func):
    """
    装饰器，确保路径存在。如果路径不存在，就创建一个文件夹
    """

    def wrapper(self: "FileManager", obj: Any, file_relpath, *args, **kwargs):
        dirname = os.path.dirname(self.get_abspath(file_relpath))
        if not os.path.exists(dirname) and self.auto_create_folder:
            os.makedirs(dirname)
        result = func(self, obj, file_relpath, *args, **kwargs)
        return result

    return wrapper
