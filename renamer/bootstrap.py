import sys
from importlib import reload


MODULES_TO_RELOAD = [

    # UI

    "ui.style.styleSheets",
    "ui.style.coloring",
    "ui.main_window",

    "ui.tabs.rename_tab",
    "ui.tabs.validation_tab",

    # Operations

    "operations.rename",
    "operations.search_replace",
    "operations.colors",
    "operations.validation",

    # Validators

    "operations.validators.typo_validator",
    "operations.validators.numbering_validator",
    "operations.validators.default_name_validator",
    "operations.validators.underscore_validator",
    "operations.validators.side_validator",

    # Utils

    "utils.undo",
    "utils.Qt_utils",
    "utils.maya_utils",
    "utils.qt",
    "utils.infoFormatting",

    # Entry

    "launcher"
]


def run():
    """
    Development bootstrap.
    """

    for module_name in MODULES_TO_RELOAD:

        if module_name in sys.modules:
            reload(
                sys.modules[module_name]
            )

    import launcher

    launcher.show()