from collections import Counter

from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


SIDE_TOKENS = {
    "L",
    "R",
    "Left",
    "Right"
}


def find_side_naming_issues(nodes):

    issues = []

    sides = []

    for node in nodes:

        name = mUt.get_short_name(node)

        parts = name.split("_")

        if not parts:
            continue

        side = parts[0]

        if side not in SIDE_TOKENS:
            continue

        sides.append(side)

    counter = Counter(sides)

    if len(counter) <= 1:
        return issues

    if "L" in counter and "Left" in counter:

        issues.append(
            valUtil.build_issue(
                category="side",
                value="L / Left",
                message="Mixed left-side naming convention",
                suggestion="Use either L or Left consistently"
            )
        )

    if "R" in counter and "Right" in counter:

        issues.append(
            valUtil.build_issue(
                category="side",
                value="R / Right",
                message="Mixed right-side naming convention",
                suggestion="Use either R or Right consistently"
            )
        )

    return issues