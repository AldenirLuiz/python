
import tkinter
import sys
from cx_Freeze import setup, Executable
import os



# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": ["tkinter", "dataBase"],"include_files": ["add_user.png", "pessoa.png", "cellNames.json", "corro.ico"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = 'Win32GUI'


if sys.platform == "win32":
    base = "Console"

setup(  name = "interface",
        version = "1.0",
        description = "Corro Variedades",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main_view.py", base=base)])