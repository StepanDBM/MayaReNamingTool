from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


def find_double_underscore_issues(nodes):

    issues = []

    for node in nodes:

        name = mUt.get_short_name(node)

        if "__" not in name:
            continue

        issues.append(
            valUtil.build_issue(
                category="underscore",
                value=name,
                message="Double underscore detected",
                suggestion="Remove redundant separators"
            )
        )

    return issues


def find_empty_token_issues(nodes):

    issues = []

    for node in nodes:

        name = mUt.get_short_name(node)

        parts = name.split("_")

        if "" not in parts:
            continue

        issues.append(
            valUtil.build_issue(
                category="token",
                value=name,
                message="Empty naming token detected",
                suggestion="Remove empty sections"
            )
        )

    return issues