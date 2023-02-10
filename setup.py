import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "tkinter",
        "sys",
        "PySide2",
        "PIL",
        "io",
        "ctypes",
        "google.cloud",
        "google.oauth2",
        "pyperclip",
        "glob",
        "environment_check",
        "cloud_vision"
    ],
    "excludes": [
    ],
    # 取り込みたいファイルやフォルダ名を記載します。
    "include_files": [
        "api-key/"
    ],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Snipping2Text",
    version="0.5",
    description="Crop the image and convert it to text.",
    options={
        "build_exe": build_exe_options,
    },
    executables=[
        Executable(
            script="Snipping2Text.py",
            base=base,
        ),
    ],
)
