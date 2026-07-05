from maya import OpenMayaUI
from shiboken2 import wrapInstance
from PySide2 import QtWidgets
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
def get_selected_uuids():
    return cmds.ls(
        selection=True,
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