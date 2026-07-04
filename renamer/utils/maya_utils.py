from maya import OpenMayaUI
from shiboken2 import wrapInstance
from PySide2 import QtWidgets


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