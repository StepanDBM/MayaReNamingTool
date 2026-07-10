from collections import Counter

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


def find_unknown_suffix_issues(nodes):

    issues = []

    suffixes = []

    for node in nodes:

        name = mUt.get_short_name(node)

        parts = name.split("_")

        if len(parts) < 2:
            continue

        suffixes.append(
            parts[-1]
        )

    counter = Counter(
        suffixes
    )

    for suffix in counter:

        if suffix in VALID_SUFFIXES:
            continue

        issues.append(
            valUtil.build_issue(
                category="suffix",
                value=suffix,
                message="Unknown suffix",
                suggestion="Use a known suffix"
            )
        )

    return issues