# RobotPy Utility
# Benjamin Ward 2018
# Allows easy PyCharm test/deploy of FRC RobotPy applications 

import sys
import platform
import py
import pytest
import wpilib
import hal

from subprocess import call


def _test():
    call(["python", "robot2.py", "test", "--", "-x"], shell=True)


def _deploy():
    if len(sys.argv) > 2:
        if "--skip-tests" in sys.argv[2]:
            call(["python", "robot2.py", "deploy", "--skip-tests"], shell=True)
            return

    call(["python", "robot2.py", "deploy"], shell=True)


def _deploy_netconsole():
    if len(sys.argv) > 2:
        if "--skip-tests" in sys.argv[2]:
            call(["python", "robot2.py", "deploy", "--nc", "--skip-tests"], shell=True)
            return

    call(["python", "robot2.py", "deploy", "--nc"], shell=True)


def _update_robotpy():
    call(["python", "-m", "robotpy_installer", "download-robotpy"], shell=True)
    call(["python", "-m", "robotpy_installer", "download-opkg", "python36-robotpy-ctre"])


def _install_robotpy():
    call(["python", "-m", "robotpy_installer", "install-robotpy"], shell=True)
    call(["python", "-m", "robotpy_installer", "install-opkg", "python36-robotpy-ctre"])


def _install_packages():
    pass


def _flash():
    _install_robotpy()
    _install_packages()


def _pass():
    pass


if __name__ == "__main__":
    action = ""
    if len(sys.argv) > 1:
        action = sys.argv[1]

    actions = {
        "test": _test,
        "deploy": _deploy,
        "deploync": _deploy_netconsole,
        "update": _update_robotpy,
        "flash": _flash,
        "": _pass
    }

    # Note: py.io is not imported in py's __init__.py but does exist.
    # See http://py.readthedocs.io/en/latest/io.html

    # Markup options are: black, red, green, yellow, blue, purple, cyan, white,
    # Black, Red, Green, Yellow, Blue, Purpole, Cyan, White, bold, light, blink, invert

    tw = py.io.TerminalWriter()
    tw.hasmarkup = True

    tw.line()
    tw.line("Platform %s \nPython %s" % (sys.platform, platform.python_version()))
    tw.line("pytest-%s, py-%s" % (pytest.__version__, py.__version__))
    tw.line("wpilib-%s, hal-%s" % (wpilib.__version__, hal.__version__))

    tw.sep('=', "Running action: " + (action if action != "" else "none"), bold=True, green=True)
    try:
        actions[action]()
    except:
        tw.line("No entry for " + action, bold=True, Red=True)