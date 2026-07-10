from utils import maya_utils as mUt

from importlib import reload

from operations.validators import validation_utils as valUtil
from config import namingConventions
reload(namingConventions)


def find_missing_suffix_issues(nodes):

    issues = []

    for node in nodes:

        name = mUt.get_short_name(node)

        parts = name.split("_")

        if len(parts) != 2:
            continue

        if parts[-1] in namingConventions.KNOWN_SUFFIXES:
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