from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


VALID_SUFFIXES = {

    "geo",
    "jnt",
    "ctrl",
    "grp",
    "loc",
    "cam",
    "lgt",
    "drv"
}


def find_missing_suffix_issues(nodes):

    issues = []

    for node in nodes:

        name = mUt.get_short_name(node)

        parts = name.split("_")

        if len(parts) != 2:
            continue

        if parts[-1] in VALID_SUFFIXES:
            continue

        issues.append(
            valUtil.build_issue(
                category="suffix",
                node=name,
                value=name,
                message="Missing naming suffix",
                suggestion="Add a valid suffix",
                severity="warning"
            )
        )

    return issues