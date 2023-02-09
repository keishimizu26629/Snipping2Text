import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "tkinter",
    ],
    "excludes": [
        "pandas",
    ],
    # 取り込みたいファイルやフォルダ名を記載します。
    "include_files": [
        "test.csv",
        "tests/"
    ],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="MyApp",
    version="0.1",
    description="My GUI application!",
    options={
        "build_exe": build_exe_options,
    },
    executables=[
        Executable(
            script="myApp.py",
            base=base,
        ),
    ],
)
