# config/namingRules.py

KNOWN_PREFIXES = {

    "char",
    "character",

    "vehicle",

    "prop",

    "tentacle",
    "rope",

    "Left",
    "Right"
}

SIDE_TOKENS = {
    "L",
    "R",
    "Left",
    "Right"
}

KNOWN_SUFFIXES = {

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
}


KNOWN_TYPES = {

    "mesh": "geo",
    "joint": "jnt",
    "transform": "grp",
    "locator": "loc",
    "camera": "cam",
    "nurbsCurve": "ctrl",
    "light": "lgt"
}

NAMING_CATEGORIES = {
    "prefix": {
        "label": "Prefix",
        "enabled": True
    },
    "suffix": {
        "label": "Suffix",
        "enabled": True
    },
    "numbering": {
        "label": "Numbering",
        "enabled": True
    },
    "type": {
        "label": "Type",
        "enabled": True
    },
    "naming": {
        "label": "Naming",
        "enabled": True
    },
    "underscore": {
        "label": "Underscore",
        "enabled": True
    },
    "token": {
        "label": "Token",
        "enabled": True
    },
    "side": {
        "label": "Side",
        "enabled": True
    },
    "duplicate_name": {
        "label": "Duplicate Names",
        "enabled": True
    },
    "hierarchy": {
        "label": "Hierarchy",
        "enabled": True
    },
    "structure": {
        "label": "Structure",
        "enabled": True
    }
}