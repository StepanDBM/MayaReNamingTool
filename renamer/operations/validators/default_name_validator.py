import re

from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


DEFAULT_NAME_PATTERNS = [

    r"^pCube\d+$",
    r"^pSphere\d+$",
    r"^pCylinder\d+$",
    r"^pPlane\d+$",
    r"^pCone\d+$",
    r"^pTorus\d+$",

    r"^polySurface\d+$",

    r"^group\d+$",

    r"^joint\d+$",

    r"^locator\d+$",

    r"^nurbsCircle\d+$"
]


def find_default_name_issues(nodes):

    issues = []

    for node in nodes:

        name = mUt.get_short_name(node)

        if not _is_default_name(name):
            continue

        issues.append(
            valUtil.build_issue(
                category="naming",
                value=name,
                message="Default Maya name detected",
                suggestion=(
                    "Rename object using "
                    "the project naming convention"
                )
            )
        )

    return issues


def _is_default_name(name):

    for pattern in DEFAULT_NAME_PATTERNS:

        if re.match(pattern, name):
            return True

    return False