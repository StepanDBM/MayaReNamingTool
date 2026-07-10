from maya import cmds

from operations.validators import validation_utils as valUtil
from utils import maya_utils as mUt


def find_empty_group_issues(nodes):

    issues = []

    for node in nodes:
        short_name = mUt.get_short_name(node)
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
                node=short_name,
                value=mUt.get_short_name(node),
                message="Empty group detected",
                suggestion="Delete or populate group",
                severity="mind_me"
            )
        )

    return issues