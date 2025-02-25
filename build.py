from __future__ import annotations

import os
import pathlib
import shutil
from typing import Any

import PyInstaller.__main__
import pyinstaller_versionfile
from tomlkit.api import parse

BASE_DIR = pathlib.Path(__file__).parent

# 设置 Python 优化模式
os.environ["PYTHONOPTIMIZE"] = "1"


def _get_project_meta() -> Any:
    """从 pyproject.toml 中获取项目元数据"""
    with open("./pyproject.toml") as pyproject:
        file_contents = pyproject.read()

    return parse(file_contents)["tool"]["poetry"]  # type: ignore


# 获取项目元数据
pkg_meta = _get_project_meta()
project = str(pkg_meta["name"])
version = str(pkg_meta["version"])

# 创建版本文件
pyinstaller_versionfile.create_versionfile(
    output_file=str(BASE_DIR / "version_file.txt"),
    version=version + ".0",
    file_description="Snooker Ball Tracker",
    internal_name="Snooker Ball Tracker",
    original_filename=project + ".exe",
    product_name="Snooker Ball Tracker",
)

# 动态设置路径分隔符（Windows 用 `;`，其他系统用 `:`）
separator = ";" if os.name == "nt" else ":"

# 使用 PyInstaller 打包
PyInstaller.__main__.run(
    [
        str(BASE_DIR / "src" / project / "gui.py"),  # 主入口文件
        "--onefile",  # 打包为单个可执行文件
        "--windowed",  # 不显示控制台窗口
        "-y",  # 覆盖输出文件
        "--add-data",
        str(BASE_DIR / "src" / project / "resources" / "icon.ico") + separator + "icon.ico",  # 添加资源文件
        "-i",
        str(BASE_DIR / "src" / project / "resources" / "icon.ico"),  # 设置图标
        "-n",
        project + ".exe",  # 输出文件名
        "--clean",  # 清理临时文件
        "--version-file",
        str(BASE_DIR / "version_file.txt"),  # 版本信息文件
    ]
)

# 复制资源文件到 dist 目录
shutil.copy(
    str(BASE_DIR / "src" / project / "resources" / "icon.ico"), str(BASE_DIR / "dist")
)
shutil.copy(
    str(BASE_DIR / "src" / project / "resources" / "default_settings.json"),
    str(BASE_DIR / "dist"),
)
