import os
import subprocess
import sys
import time
from pathlib import Path, WindowsPath
from shutil import which


# ruff: noqa: T201
def find_pythons():
        python = None
        pythons = [
            "python3.9",
            "python3.10",
            "python3.11",
            "python3.12",
            "python3.13",
            "python3.14",
        ]
        installed_pythons = None
        if os.getenv("LOCALAPPDATA", None):
            lad = Path(
                os.getenv("LOCALAPPDATA", None),
                "Microsoft/WindowsApps/",
            ).resolve()
            installed_pythons = [x.stem for x in list(lad.glob("python*"))]
        for pyt in pythons:
            if which(pyt):
                python = pyt
            if installed_pythons and pyt in installed_pythons:
                python = str(lad / pyt)
        if not python:
            print(
                "Failed to find a compatible python! Looked for:"
                f" {', '.join(pythons)}",
            )
            sys.exit(1)
        return python

def python_checks():
    me = Path(sys.argv[0])

    if me.is_absolute() and isinstance(me, WindowsPath):
        print(
            "This script can not be ran directly, please restart as 'python"
            f" {me.name}'",
        )

        time.sleep(30)
        sys.exit(1)

    if  sys.version_info < (3, 10):  # noqa: UP036
        print(
            f"Requires Python 3.10 or newer, this is %s.%s"  # noqa: F541
            % (sys.version_info.major, sys.version_info.minor),
        )
        newest_python = find_pythons()
        print("Found %s, reloading..." % (newest_python,))  # noqa: UP031
        subprocess.run(
            [   # noqa: S603
                newest_python,
                os.path.abspath(sys.argv[0]),  # noqa: PTH100
                "no-git"],
                check=False,
        )
        sys.exit(0)

    if (
        "VIRTUAL_ENV" not in os.environ
        or os.environ["VIRTUAL_ENV"].strip() == ""
    ) and not os.access("./.venv", os.R_OK):
        venv_inp = input(
            "No python python virtual environment. Create one in ./.venv?"
            " (Y/n): ",
        )
        print(
            f"Using python {sys.version_info.major}.{sys.version_info.minor}",
        )
        if venv_inp.lower() == "y" or venv_inp == "":
            from importlib.util import find_spec

            venv_loader = find_spec("venv")
            if not venv_loader:
                print(
                    "Failed to find venv module using"
                    f" {sys.executable} "
                    f"({sys.version_info.major}.{sys.version_info.minor})."
                    " Please install it using your system package manager.",
                )
                sys.exit(1)
            from venv import create

            create("./.venv", with_pip=True)
            print("Please activate the new venv,then re-run the script")
        sys.exit()

    elif (
        "VIRTUAL_ENV" not in os.environ
        or os.environ["VIRTUAL_ENV"].strip() == ""
    ):
        print(
            "Please activate the python virtual "
            "environment before running this script.",
        )
        sys.exit(1)
