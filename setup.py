import sys
from cx_Freeze import setup, Executable
sys.argv.append("bdist_msi")
# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}
directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|Postura"),
]
msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", None, None, "Medical application for clinical evaluation of GAIT disease.", "IconId", None),
    ],
    "Icon": [
        ("IconId", "Icon.ico"),
    ],
}
bdist_msi_options = {
    "add_to_path": True,
    "data": msi_data,
    # "environment_variables": [
    #     ("E_MYAPP_VAR", "=-*MYAPP_VAR", "1", "TARGETDIR")
    # ],
    "upgrade_code": "{00000000-0000-0000-0000-000000000001}",
}
# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Postura",
    version="1.0",
    description="Medical application for clinical evaluation of GAIT disease.",
    options={"build_exe": build_exe_options,"bdist_msi": bdist_msi_options,},
    executables=[Executable("Main.py", base=base,shortcutName="Postura",shortcutDir="DesktopFolder",icon="Icon.ico")],
)