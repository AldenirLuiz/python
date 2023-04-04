
import tkinter
import sys
from cx_Freeze import setup, Executable
import os, platform

print(platform.system())
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"], 
    "includes": ["tkinter", "dataBase"],
    "include_files": [
        "add_user.png", 
        "pessoa.png", 
        "cellNames.json", 
        "app.ico"
    ]
}
target = Executable(
    script="main_view.py",
    base=None,
    icon="app.ico",
)

base = None

setup(  name = "interface",
        version = "1.0",
        description = "Corro Variedades",
        autthor="Aldenir Luiz",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main_view.py", base=base)])
