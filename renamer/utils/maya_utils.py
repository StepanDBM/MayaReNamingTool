from utils.qt import QtWidgets, wrapInstance
from maya import OpenMayaUI
from maya import cmds


def maya_main_window():
    """
    Returns Maya's main window as a QWidget.
    """

    ptr = OpenMayaUI.MQtUtil.mainWindow()

    if ptr is None:
        return None

    return wrapInstance(
        int(ptr),
        QtWidgets.QWidget
    )
def get_uuids_from_nodes(nodes):

    return cmds.ls(
        nodes,
        uuid=True
    ) or []

def get_selected_uuids():
    return cmds.ls(
        selection=True,
        uuid=True
    ) or []

def get_hierarchy_uuids():
    """
    Returns hierarchy nodes as UUIDs in
    safe rename order (deepest -> shallowest).
    """

    nodes = get_hierarchy_rename_order()

    return cmds.ls(
        nodes,
        uuid=True
    ) or []

def get_nodes_from_uuids(uuids):

    nodes = []

    for uuid in uuids:

        matches = cmds.ls(
            uuid,
            long=True
        ) or []

        nodes.extend(
            matches
        )

    return nodes

def get_selection():
    return cmds.ls(
        selection=True,
        long=True
    ) or []

def get_naming_nodes(nodes=None):

    if nodes is None:
        nodes = get_selection()

    return [
        node
        for node in nodes
        if not cmds.objectType(
            node,
            isAType="shape"
        )
    ]

def get_all_naming_nodes():

    return get_naming_nodes(
        cmds.ls(long=True)
    )

def list_relatives(someTransform):
    return cmds.listRelatives(
        someTransform,
        allDescendents=True,
        fullPath=True
    ) or []

def get_hierarchy_selection():

    selection = get_selection()

    roots = []

    for node in selection:

        is_child_of_selected = False

        for other in selection:

            if node == other:
                continue

            if node.startswith(
                other + "|"
            ):
                is_child_of_selected = True
                break

        if not is_child_of_selected:
            roots.append(node)

    descendants = set()

    for root in roots:

        descendants.update(
            list_relatives(root)
        )

    return (
        list(descendants),
        roots
    )

def get_short_name(node):
    """ ditch DAG path :: |...|group|cube_geo -> cube_geo
    """
    return node.split("|")[-1]



def sort_nodes_for_rename(nodes):
    """
    Deepest DAG nodes first.
    """

    return sorted(
        nodes,
        key=lambda node: node.count("|"),
        reverse=True
    )
def get_hierarchy_rename_order():
    """
    Returns selected hierarchy sorted deepest -> shallowest.

    Safe for renaming operations.

    Returns
    -------
    list[str]
    """

    descendants, roots = get_hierarchy_selection()

    return sort_nodes_for_rename(
        descendants + roots
    )

def frame_object_on_name(node_name):

    matches = cmds.ls(
        node_name,
        long=True
    ) or []

    if len(matches) != 1:

        cmds.warning(
            f"Cannot uniquely identify: {node_name}"
        )

        return

    cmds.select(
        matches[0],
        replace=True
    )

    cmds.viewFit()


def strip_namespace_from_name(name):

    return name.rsplit(
        ":",
        1
    )[-1]


def get_short_name_without_namespace(node):

    short_name = get_short_name(
        node
    )

    return strip_namespace_from_name(
        short_name
    )


def has_namespace(node):

    short_name = get_short_name(
        node
    )

    return ":" in short_name