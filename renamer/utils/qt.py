# qt.py
# Maya Qt Compatibility Layer
#
# Usage:
#
# from qt import (
#     QtWidgets,
#     QtCore,
#     QtGui,
#     QColor,
#     QIcon,
#     QPixmap,
#     QFont,
#     wrapInstance,
# )
#
# qt.py

QT_BINDING = None
QT_VERSION = None

QtCore = None
QtGui = None
QtWidgets = None
QtUiTools = None

wrapInstance = None

QColor = None
QIcon = None
QPixmap = None
QFont = None
QBrush = None
QPen = None
QPalette = None
QPainter = None
QPainterPath = None


# --------------------------------------------------
# PySide6 (Maya 2025+)
# --------------------------------------------------

try:

    from PySide6 import QtCore
    from PySide6 import QtGui
    from PySide6 import QtWidgets

    try:
        from PySide6 import QtUiTools
    except ImportError:
        pass

    from shiboken6 import wrapInstance

    QT_BINDING = "PySide6"
    QT_VERSION = 6

# --------------------------------------------------
# PySide2 (Maya 2017-2024)
# --------------------------------------------------

except ImportError:

    try:

        from PySide2 import QtCore
        from PySide2 import QtGui
        from PySide2 import QtWidgets

        try:
            from PySide2 import QtUiTools
        except ImportError:
            pass

        from shiboken2 import wrapInstance

        QT_BINDING = "PySide2"
        QT_VERSION = 2

    # --------------------------------------------------
    # Ancient PySide
    # --------------------------------------------------

    except ImportError:

        try:

            from PySide import QtCore
            from PySide import QtGui

            # PySide did not have QtWidgets
            QtWidgets = QtGui

            try:
                from PySide import QtUiTools
            except ImportError:
                pass

            from shiboken import wrapInstance

            QT_BINDING = "PySide"
            QT_VERSION = 1

        except ImportError:

            raise ImportError(
                "Could not find a supported Qt binding "
                "(PySide6, PySide2 or PySide)."
            )


# --------------------------------------------------
# Common aliases
# --------------------------------------------------

if QtGui is not None:

    QColor = QtGui.QColor

    QIcon = QtGui.QIcon

    QPixmap = QtGui.QPixmap

    QFont = QtGui.QFont

    QBrush = QtGui.QBrush

    QPen = QtGui.QPen

    QPalette = QtGui.QPalette

    QPainter = QtGui.QPainter

    QPainterPath = QtGui.QPainterPath


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def is_qt6():
    return QT_BINDING == "PySide6"


def is_qt5():
    return QT_BINDING == "PySide2"


def is_qt4():
    return QT_BINDING == "PySide"


def print_qt_info():

    print(
        "Qt Binding:",
        QT_BINDING,
        "| Version:",
        QT_VERSION
    )

try:
    import maya.cmds as cmds
    MAYA_VERSION = cmds.about(version=True)
except Exception:
    MAYA_VERSION = "Unknown"


def get_environment_info():
    return (
        f"{MAYA_VERSION} | "
        f"{QT_BINDING}"
    )