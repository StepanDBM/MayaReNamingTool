from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


def find_double_underscore_issues(nodes):
    issues = []
    for node in nodes:
        display_name = mUt.get_short_name(node)
        clean_name = mUt.get_short_name_without_namespace(node)

        if "__" not in clean_name:
            continue
        issues.append(
            valUtil.build_issue(
                category="underscore",
                node=display_name,
                value=clean_name,
                message="Double underscore detected",
                suggestion="Remove redundant separators",
                severity="warning",
                solver="collapse_underscores",
                solvable=True
            )
        )
    return issues