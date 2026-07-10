import sys
from importlib import reload


MODULES_TO_RELOAD = [

    # UI
    "config.severityTypes",
    "ui.style.styleSheets",
    "ui.style.QtColoring",
    "ui.main_window",

    "ui.tabs.rename_tab",
    "ui.tabs.recolors_tab",
    "ui.tabs.validation_tab",

    "ui.widgets.collapsibleSection",

    # Operations

    "operations.rename",
    "operations.search_replace",
    "operations.colors",
    "operations.validation",

    # Validators
    "operations.validators.typo_validator",
    "operations.validators.numbering_validator",
    "operations.validators.default_name_validator",
    "operations.validators.underscore_valdiator",
    "operations.validators.side_validator",
    "operations.validators.unknown_suffix_validator",
    "operations.validators.duplicate_name_validator",
    "operations.validators.type_validator",
    "operations.validators.missing_suffix_validator",
    "operations.validators.consistent_padding_validator",
    "operations.validators.unkown_prefix_validator",
    "operations.validators.empty_group_validator",
    "operations.validators.token_count_validator",

    # Utils

    "utils.qt",
    "utils.undo",
    "utils.maya_utils",
    "utils.infoFormatting",
    "utils.brokenNamingSceneCreator",

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