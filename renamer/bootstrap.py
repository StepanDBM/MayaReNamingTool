import sys
from importlib import reload


MODULES_TO_RELOAD = [
    "ui.styleSheets",
    "ui.main_window",
    "launcher"
]


def run():
    """
    Development bootstrap.
    """

    for module_name in MODULES_TO_RELOAD:
        if module_name in sys.modules:
            reload(sys.modules[module_name])

    import launcher

    launcher.show()