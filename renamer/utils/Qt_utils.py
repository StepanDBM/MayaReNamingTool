# renamer/utils/Qt_utils.py

from PySide2.QtGui import QColor


def lighter_color(hex_color, factor=160):
    """
    Returns a lighter version of a color.

    Parameters
    ----------
    hex_color : str
        Hex color string (e.g. "#ff3939")

    factor : int
        100 -> same color
        130 -> 30% lighter
        150 -> 50% lighter

    Returns
    -------
    str
        Hex color string.
    """

    return QColor(hex_color).lighter(factor).name()


def darker_color(hex_color, factor=130):
    """
    Returns a darker version of a color.

    Parameters
    ----------
    hex_color : str
        Hex color string (e.g. "#ff3939")

    factor : int
        100 -> same color
        130 -> 30% darker
        150 -> 50% darker

    Returns
    -------
    str
        Hex color string.
    """

    return QColor(hex_color).darker(factor).name()