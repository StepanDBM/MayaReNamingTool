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
    valid_type_suffixes = set(TYPE_SUFFIXES.values())
    for node in nodes:
        expected_suffix = (_get_expected_suffix(node))
        if not expected_suffix:
            continue
        display_name = mUt.get_short_name(node)
        clean_name = mUt.get_short_name_without_namespace(node)
        parts = clean_name.split("_")
        if len(parts) < 2:
            continue

        current_suffix = parts[-1]
        # Unknown suffix?
        # Let unknown_suffix_validator
        # handle it instead.
        if current_suffix not in valid_type_suffixes:
            continue

        # Correct type.
        if current_suffix == expected_suffix:
            continue
        issues.append(
            valUtil.build_issue(
                category="type",
                node=display_name,
                value=current_suffix,
                message="Node type naming mismatch",
                suggestion=(
                    f"Expected '_{expected_suffix}' "
                    f"for this node type."
                ),
                severity="error"
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
    shape_type = cmds.nodeType(shapes[0])

    return TYPE_SUFFIXES.get(shape_type)