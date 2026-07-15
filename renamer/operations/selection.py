# operations/selection.py

from maya import cmds

from utils import maya_utils as mUt


_STORED_SELECTION_UUIDS = []
_SELECTION_PRESETS = {}


def _log(message):
    print(f"[reSelection] {message}")


def _unique(nodes):

    seen = set()
    result = []

    for node in nodes:
        if node in seen:
            continue
        seen.add(node)
        result.append(node)
    return result


def _select_nodes(
    nodes,
    mode="replace"
):
    nodes = [
        node
        for node in nodes
        if cmds.objExists(node)
    ]
    nodes = _unique(nodes)

    if not nodes:
        if mode == "replace":
            cmds.select(clear=True)
        _log("No nodes found.")
        return []
    if mode == "add":
        cmds.select(nodes, add=True)
    elif mode == "remove":
        cmds.select(nodes, deselect=True)
    else:
        cmds.select(nodes, replace=True)
    _log(f"{mode.title()} {len(nodes)} node(s).")

    return nodes


def _shape_parents_from_type(shape_type):
    shapes = cmds.ls(
        type=shape_type,
        long=True
    ) or []

    parents = []
    for shape in shapes:
        parent = cmds.listRelatives(
            shape,
            parent=True,
            fullPath=True
        ) or []
        parents.extend(parent)

    return _unique(parents)


def _get_selected_short_parts():
    selection = cmds.ls(
        selection=True,
        long=True
    ) or []
    if not selection:
        return None
    name = mUt.get_short_name(selection[0])
    parts = name.split("_")

    if len(parts) < 2:
        return None

    return parts


def _get_selected_type_category():

    selection = cmds.ls(
        selection=True,
        long=True
    ) or []

    if not selection:
        return None

    node = selection[0]

    node_type = cmds.nodeType(
        node
    )

    if node_type == "joint":
        return "joint"

    if node_type == "camera":
        return "camera"

    if node_type == "locator":
        return "locator"

    shapes = cmds.listRelatives(
        node,
        shapes=True,
        fullPath=True
    ) or []

    if not shapes:
        return "transform"

    shape_type = cmds.nodeType(shapes[0])

    if shape_type == "mesh":
        return "mesh"

    if shape_type == "nurbsCurve":
        return "curve"

    if shape_type == "camera":
        return "camera"

    if shape_type == "locator":
        return "locator"

    return node_type

def get_next_preset_name():
    index = 1

    while True:
        name = (
            f"Selection {index:02d}"
        )
        if name not in _SELECTION_PRESETS:
            return name
        index += 1


def get_selection_preset_names():
    return sorted(_SELECTION_PRESETS.keys())


def store_selection_preset(name):
    name = name.strip()

    if not name:
        name = get_next_preset_name()

    uuids = mUt.get_selected_uuids()
    if not uuids:
        _log("No selection to store.")
        return []

    _SELECTION_PRESETS[name] = uuids
    _log(f"Stored preset '{name}' with {len(uuids)} node(s).")

    return uuids


def restore_selection_preset(
    name,
    mode="replace"
):
    if name not in _SELECTION_PRESETS:
        _log(f"Preset '{name}' does not exist.")
        return []

    nodes = mUt.get_nodes_from_uuids(_SELECTION_PRESETS[name])

    return _select_nodes(nodes, mode=mode)


def delete_selection_preset(name):

    if name not in _SELECTION_PRESETS:
        return []

    del _SELECTION_PRESETS[name]

    _log(f"Deleted preset '{name}'.")

    return []


def select_hierarchy(mode="replace"):

    selection = cmds.ls(
        selection=True,
        long=True
    ) or []

    if not selection:

        return _select_nodes(
            [],
            mode=mode
        )

    result = []

    for node in selection:

        result.append(node)

        descendants = cmds.listRelatives(
            node,
            allDescendents=True,
            fullPath=True
        ) or []

        result.extend(descendants)

    return _select_nodes(result, mode=mode)


def select_children(mode="replace"):
    selection = cmds.ls(
        selection=True,
        long=True
    ) or []

    result = []
    for node in selection:
        children = cmds.listRelatives(
            node,
            children=True,
            fullPath=True
        ) or []
        result.extend(children)
    return _select_nodes(result, mode=mode)


def select_parents(mode="replace"):
    selection = cmds.ls(
        selection=True,
        long=True
    ) or []

    result = []
    for node in selection:
        parents = cmds.listRelatives(
            node,
            parent=True,
            fullPath=True
        ) or []

        result.extend(parents)
    return _select_nodes(result, mode=mode)


def select_type_joints(mode="replace"):
    nodes = cmds.ls(
        type="joint",
        long=True
    ) or []

    return _select_nodes(nodes, mode=mode)


def select_type_meshes(mode="replace"):
    nodes = _shape_parents_from_type("mesh")
    return _select_nodes(nodes, mode=mode)


def select_type_curves(mode="replace"):
    nodes = _shape_parents_from_type("nurbsCurve")
    return _select_nodes(nodes, mode=mode)


def select_type_locators(mode="replace"):
    nodes = _shape_parents_from_type("locator")
    return _select_nodes(nodes, mode=mode)


def select_type_cameras(mode="replace"):
    nodes = _shape_parents_from_type("camera")
    return _select_nodes(nodes, mode=mode)

def select_type_transforms(mode="replace"):
    nodes = cmds.ls(
        type="transform",
        long=True
    ) or []
    return _select_nodes(nodes, mode=mode)


def select_same_type(mode="replace"):
    category = _get_selected_type_category()
    if not category:
        return _select_nodes([], mode=mode)
    if category == "joint":
        return select_type_joints(mode=mode)
    if category == "mesh":
        return select_type_meshes(mode=mode)
    if category == "curve":
        return select_type_curves(mode=mode)
    if category == "locator":
        return select_type_locators(mode=mode)
    if category == "camera":
        return select_type_cameras(mode=mode)
    if category == "transform":
        return select_type_transforms(mode=mode)

    nodes = cmds.ls(
        type=category,
        long=True
    ) or []

    return _select_nodes(nodes, mode=mode)


def select_same_prefix(mode="replace"):
    parts = _get_selected_short_parts()
    if not parts:
        return _select_nodes([], mode=mode)

    prefix = parts[0]
    nodes = mUt.get_all_naming_nodes()
    matches = []

    for node in nodes:
        name = mUt.get_short_name(node)
        node_parts = name.split("_")
        if len(node_parts) < 2:
            continue

        if node_parts[0] != prefix:
            continue
        matches.append(node)

    return _select_nodes(matches, mode=mode)


def select_same_suffix(mode="replace"):
    parts = _get_selected_short_parts()
    if not parts:
        return _select_nodes([], mode=mode)

    suffix = parts[-1]
    nodes = mUt.get_all_naming_nodes()
    matches = []

    for node in nodes:
        name = mUt.get_short_name(node)
        node_parts = name.split("_")
        if len(node_parts) < 2:
            continue
        if node_parts[-1] != suffix:
            continue
        matches.append(node)

    return _select_nodes(matches, mode=mode)


def select_by_pattern(
    pattern,
    mode="replace"
):
    pattern = pattern.strip()

    if not pattern:
        return _select_nodes([], mode=mode)
    nodes = cmds.ls(
        pattern,
        long=True
    ) or []
    nodes = mUt.get_naming_nodes(nodes)

    return _select_nodes(nodes, mode=mode)


def invert_selection(mode="replace"):

    selected = set(
        cmds.ls(
            selection=True,
            long=True
        ) or []
    )
    all_nodes = set(mUt.get_all_naming_nodes())
    inverted = list(all_nodes - selected)

    return _select_nodes(inverted, mode=mode)


def store_selection():
    global _STORED_SELECTION_UUIDS
    uuids = mUt.get_selected_uuids()
    if not uuids:
        _STORED_SELECTION_UUIDS = []
        _log("Stored selection cleared. No selection found.")

        return []

    _STORED_SELECTION_UUIDS = uuids
    _log(f"Stored {len(_STORED_SELECTION_UUIDS)} node UUID(s).")

    return _STORED_SELECTION_UUIDS


def restore_selection(mode="replace"):
    nodes = mUt.get_nodes_from_uuids(
        _STORED_SELECTION_UUIDS
    )
    return _select_nodes(nodes, mode=mode)