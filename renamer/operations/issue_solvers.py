# operations/issue_solvers.py

import re

from maya import cmds

from utils import maya_utils as mUt
from utils.undo import undo_chunk
from utils.loaders import loadNamingRules as N_Rules


def _get_solver_map():

    return {
        "strip_namespace": solve_namespace_issue,
        "replace_token": solve_typo_issue,
        "collapse_underscores": solve_underscore_issue,
    }


def can_solve(issue):

    if not issue:
        return False

    if issue.get("solvable") is False:
        return False

    category = issue.get("category")
    solver_name = issue.get("solver")

    if not category or not solver_name:
        return False

    rules = N_Rules.load_rules()

    category_data = (
        rules
        .get("categories", {})
        .get(category, {})
    )

    if not category_data.get("solvable", False):
        return False

    return solver_name in _get_solver_map()


def _get_issue_node(issue):

    node_name = issue.get("node")

    if not node_name:
        return None

    matches = cmds.ls(node_name, long=True) or []

    if len(matches) == 1:
        return matches[0]

    if not matches:
        cmds.warning(f"Cannot find node: {node_name}")
        return None

    cmds.warning(f"Cannot uniquely identify node: {node_name}")
    return None


def _split_namespace(short_name):

    if ":" not in short_name:
        return "", short_name

    namespace, clean_name = short_name.rsplit(":", 1)

    return namespace, clean_name


def _rename_node(node, new_short_name):

    try:
        renamed = cmds.rename(node, new_short_name)

    except RuntimeError as error:
        cmds.warning(str(error))
        return None

    return renamed


@undo_chunk
def solve_issue(issue):

    if not can_solve(issue):
        cmds.warning("No solver available for this issue.")
        return []

    solver_name = issue.get("solver")
    solver = _get_solver_map().get(solver_name)

    if not solver:
        cmds.warning(f"No solver registered for: {solver_name}")
        return []

    return solver(issue)


def solve_namespace_issue(issue):

    node = _get_issue_node(issue)

    if not node:
        return []

    short_name = mUt.get_short_name(node)

    if ":" not in short_name:
        return []

    namespace, clean_name = _split_namespace(short_name)

    # Leading ":" means rename into root namespace.
    new_name = f":{clean_name}"

    renamed = _rename_node(node, new_name)

    if not renamed:
        return []

    cmds.select(renamed, replace=True)

    return [renamed]


def solve_typo_issue(issue):

    node = _get_issue_node(issue)

    if not node:
        return []

    category = issue.get("category")
    old_value = issue.get("value")
    new_value = issue.get("suggestion")

    if not old_value or not new_value:
        return []

    short_name = mUt.get_short_name(node)
    namespace, clean_name = _split_namespace(short_name)
    parts = clean_name.split("_")

    if len(parts) < 2:
        return []

    if category == "prefix":

        if parts[0] != old_value:
            return []

        parts[0] = new_value

    elif category == "suffix":

        if parts[-1] != old_value:
            return []

        parts[-1] = new_value

    else:
        cmds.warning(f"Typo solver does not support category: {category}")
        return []

    new_clean_name = "_".join(parts)

    if namespace:
        new_short_name = f"{namespace}:{new_clean_name}"

    else:
        new_short_name = new_clean_name

    renamed = _rename_node(node, new_short_name)

    if not renamed:
        return []

    cmds.select(renamed, replace=True)

    return [renamed]


def solve_underscore_issue(issue):

    node = _get_issue_node(issue)

    if not node:
        return []

    short_name = mUt.get_short_name(node)
    namespace, clean_name = _split_namespace(short_name)

    fixed_name = re.sub(r"_+", "_", clean_name)
    fixed_name = fixed_name.strip("_")

    if fixed_name == clean_name:
        return []

    if namespace:
        new_short_name = f"{namespace}:{fixed_name}"

    else:
        new_short_name = fixed_name

    renamed = _rename_node(node, new_short_name)

    if not renamed:
        return []

    cmds.select(renamed, replace=True)

    return [renamed]