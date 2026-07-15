import json
import os
import copy


RULES_FILE = os.path.join(
    os.path.dirname(__file__),
    "namingRules.json"
)


DEFAULT_RULES = {
    "categories": {
        "duplicate_name": {
            "enabled": True,
            "label": "Duplicate Names",
            "solvable": False
        },
        "hierarchy": {
            "enabled": True,
            "label": "Hierarchy",
            "solvable": False
        },
        "naming": {
            "enabled": True,
            "label": "Naming",
            "solvable": False
        },
        "numbering": {
            "enabled": True,
            "label": "Numbering",
            "solvable": False
        },
        "prefix": {
            "enabled": True,
            "label": "Prefix",
            "solvable": True
        },
        "side": {
            "enabled": True,
            "label": "Side",
            "solvable": False
        },
        "structure": {
            "enabled": True,
            "label": "Structure",
            "solvable": False
        },
        "suffix": {
            "enabled": True,
            "label": "Suffix",
            "solvable": True
        },
        "token": {
            "enabled": True,
            "label": "Token",
            "solvable": False
        },
        "type": {
            "enabled": True,
            "label": "Type",
            "solvable": False
        },
        "underscore": {
            "enabled": True,
            "label": "Underscore",
            "solvable": True
        },
        "namespace": {
            "enabled": True,
            "label": "Namespaces",
            "solvable": True
        }
    },

    "prefixes": [
        "char",
        "character",
        "vehicle",
        "prop",
        "tentacle",
        "rope",
        "Left",
        "Right"
    ],

    "side_tokens": [
        "L",
        "R",
        "Left",
        "Right"
    ],

    "suffixes": [
        "geo",
        "grp",
        "jnt",
        "bnd",
        "drv",
        "ctrl",
        "anim",
        "auto",
        "offs",
        "loc",
        "cam",
        "lgt",
        "crv"
    ],

    "types": {
        "mesh": "geo",
        "joint": "jnt",
        "transform": "grp",
        "locator": "loc",
        "camera": "cam",
        "nurbsCurve": "ctrl",
        "light": "lgt"
    }
}


def _merge_defaults(defaults, data):

    result = copy.deepcopy(
        defaults
    )

    for key, value in data.items():

        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):

            result[key] = _merge_defaults(
                result[key],
                value
            )

        else:

            result[key] = value

    return result


def load_rules():

    if not os.path.exists(
        RULES_FILE
    ):

        restore_default_rules()

    with open(
        RULES_FILE,
        "r"
    ) as stream:

        loaded_rules = json.load(
            stream
        )

    rules = _merge_defaults(
        DEFAULT_RULES,
        loaded_rules
    )

    save_rules(
        rules
    )

    return rules


def save_rules(rules):

    with open(
        RULES_FILE,
        "w"
    ) as stream:

        json.dump(
            rules,
            stream,
            indent=4,
            sort_keys=True
        )


def restore_default_rules():

    rules = copy.deepcopy(
        DEFAULT_RULES
    )

    save_rules(
        rules
    )

    return copy.deepcopy(
        rules
    )