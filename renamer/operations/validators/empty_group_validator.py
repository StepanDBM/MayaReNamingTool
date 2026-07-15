import re
from maya import cmds
from operations.validators import validation_utils as valUtil
from utils import maya_utils as mUt

"""
EXAMPLES

transform1
transform2
transform15

character_rig_grp
vehicle_grp

arm_ctrl
spine_ctrl

arm_crv
faceCurve
"""


def find_empty_group_issues(nodes):
    issues = []
    for node in nodes:
        if cmds.nodeType(node) != "transform":
            continue
        display_name = mUt.get_short_name(node)
        clean_name = mUt.get_short_name_without_namespace(node)
        children = cmds.listRelatives(
            node,
            children=True,
            fullPath=True
        ) or []

        if children:
            continue

        clean_name_lower = clean_name.lower()
        is_default_transform = bool(
            re.match(
                r"^transform\d+$",
                clean_name
            )
        )
        is_group = (
            clean_name.endswith("_grp")
        )
        is_control = ("_ctrl" in clean_name)
        is_curve = (
            "_crv" in clean_name
            or "curve" in clean_name_lower
        )
        if not any(
            (
                is_default_transform,
                is_group,
                is_control,
                is_curve
            )
        ):
            continue

        issues.append(
            valUtil.build_issue(
                category="hierarchy",
                node=display_name,
                value=clean_name,
                message="Empty transform detected",
                suggestion=(
                    "Delete it or restore "
                    "the missing contents"
                ),
                severity="mind_me"
            )
        )
    return issues