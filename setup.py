
import tkinter
import sys
from cx_Freeze import setup, Executable
import os
import json
import webbrowser

from datetime import datetime

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
    base='Win32GUI',
    icon="app.ico",
)

base = "Console"

setup(  name = "Sistema de Gerenciamento de Dados de Crediario | Corro Variedades",
        version = "1.0",
        description = "Corro Variedades",
        autthor="Aldenir Luiz",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main_view.py", base=base)])
