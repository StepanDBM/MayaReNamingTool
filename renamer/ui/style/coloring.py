from utils.qt import QtGui

def get_category_color(category):

    colors = {

        "prefix": QtGui.QColor(255, 220, 120),

        "suffix": QtGui.QColor(255, 180, 120),

        "numbering": QtGui.QColor(120, 220, 255),

        "type": QtGui.QColor(255, 120, 120),

        "hierarchy": QtGui.QColor(220, 120, 255),

        "side": QtGui.QColor(180, 255, 180),

        "token": QtGui.QColor(220, 220, 120),

        "structure": QtGui.QColor(150, 200, 255),

        "naming": QtGui.QColor(180, 180, 180)
    }

    return colors.get(
        category,
        QtGui.QColor(220, 220, 220)
    )