from maya import cmds

from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


TYPE_SUFFIXES = {
    "joint": "jnt",
    "mesh": "geo",
    "camera": "cam",
    "locator": "loc",
    "light": "lgt"
}


def find_type_issues(nodes):

    issues = []

    for node in nodes:

        expected_suffix = _get_expected_suffix(
            node
        )

        if not expected_suffix:
            continue

        name = mUt.get_short_name(node)

        parts = name.split("_")

        if len(parts) < 2:
            continue

        current_suffix = parts[-1]

        if current_suffix == expected_suffix:
            continue

        issues.append(
            valUtil.build_issue(
                category="type",
                value=name,
                message="Node type naming mismatch",
                suggestion=(
                    f"Object type: "
                    f"{expected_suffix} and '_{expected_suffix}'is expected."
                )
            )
        )

    return issues


def _get_expected_suffix(node):

    node_type = cmds.nodeType(node)

    if node_type == "joint":
        return TYPE_SUFFIXES["joint"]

    shapes = cmds.listRelatives(
        node,
        shapes=True,
        fullPath=True
    ) or []

    if not shapes:
        return None

    shape_type = cmds.nodeType(
        shapes[0]
    )

    return TYPE_SUFFIXES.get(
        shape_type
    )