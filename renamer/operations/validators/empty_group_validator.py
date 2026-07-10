from maya import cmds

from operations.validators import validation_utils as valUtil


def find_empty_group_issues(nodes):

    issues = []

    for node in nodes:

        if cmds.nodeType(node) != "transform":
            continue

        children = cmds.listRelatives(
            node,
            children=True,
            fullPath=True
        ) or []

        if children:
            continue

        issues.append(
            valUtil.build_issue(
                category="hierarchy",
                value=node,
                message="Empty group detected",
                suggestion="Delete or populate group"
            )
        )

    return issues