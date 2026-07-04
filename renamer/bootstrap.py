import sys
from importlib import reload


MODULES_TO_RELOAD = [
    "ui.styleSheets",
    "ui.main_window",
    "ui.color_widget",
    "ui.rename_widget",
    "ui.search_widget",
    "ui.suffix_widget",
    
    "operations.rename",
    "operations.search_replace",
    "operations.colors",

    "utils.undo",
    "utils.Qt_utils",
    "utils.maya_utils",
    
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