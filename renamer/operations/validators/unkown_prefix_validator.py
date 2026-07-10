from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


KNOWN_PREFIXES = {
    "char",
    "character",
    "vehicle",
    "prop",
    "tentacle",
    "rope",
    "L",
    "R",
    "Left",
    "Right"
}


def find_unknown_prefix_issues(nodes):

    issues = []

    for node in nodes:

        name = mUt.get_short_name(node)

        parts = name.split("_")

        if len(parts) < 2:
            continue

        prefix = parts[0]

        if prefix in KNOWN_PREFIXES:
            continue

        issues.append(
            valUtil.build_issue(
                category="prefix",
                node=name,
                value=prefix,
                message="Unknown prefix",
                suggestion="Use a known prefix",
                severity="warning"
            )
        )

    return issues