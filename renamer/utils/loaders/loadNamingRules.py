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
            "label": "Duplicate Names"
        },
        "hierarchy": {
            "enabled": True,
            "label": "Hierarchy"
        },
        "naming": {
            "enabled": True,
            "label": "Naming"
        },
        "numbering": {
            "enabled": True,
            "label": "Numbering"
        },
        "prefix": {
            "enabled": True,
            "label": "Prefix"
        },
        "side": {
            "enabled": True,
            "label": "Side"
        },
        "structure": {
            "enabled": True,
            "label": "Structure"
        },
        "suffix": {
            "enabled": True,
            "label": "Suffix"
        },
        "token": {
            "enabled": True,
            "label": "Token"
        },
        "type": {
            "enabled": True,
            "label": "Type"
        },
        "underscore": {
            "enabled": True,
            "label": "Underscore"
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
        "lgt"
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

def load_rules():

    with open(
        RULES_FILE,
        "r"
    ) as stream:

        return json.load(stream)


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
        import copy

def restore_default_rules():

    save_rules(
        copy.deepcopy(
            DEFAULT_RULES
        )
    )

    return copy.deepcopy(
        DEFAULT_RULES
    )