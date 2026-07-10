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

def get_selection():
    return cmds.ls(
        selection=True,
        long=True
    ) or []

def list_relatives(someTransform):
    return cmds.listRelatives(
        someTransform,
        allDescendents=True,
        fullPath=True
    ) or []

def get_hierarchy_selection():
    """
    Returns:
        descendants (leaf -> root)
        selected roots
    """

    descendants = []

    selection = get_selection()

    for node in selection:

        children = list_relatives(node)

        descendants.extend(children)

    return descendants, selection

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