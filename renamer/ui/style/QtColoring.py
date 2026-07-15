from utils.qt import (
    QColor
)

from config import severityTypes
DEFAULT_TEXT_COLOR = QColor(
    220,
    220,
    220
)

def get_severity_color(severity):

    color = severityTypes.SEVERITY_TYPES[
        severity
    ]["color"]

    return QColor(*color)
def get_category_color(category):

    colors = {

        "prefix": QColor(255, 220, 120),
        "suffix": QColor(255, 180, 120),
        "numbering": QColor(120, 220, 255),
        "type": QColor(255, 120, 120),
        "hierarchy": QColor(220, 120, 255),
        "side": QColor(180, 255, 180),
        "token": QColor(220, 220, 120),
        "structure": QColor(150, 200, 255),
        "naming": QColor(180, 180, 180),
        "namespace": QColor(120, 255, 220)
    }

    return colors.get(
        category,
        QColor(220, 220, 220)
    )

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

def apply_severity_color(
    widget,
    severity=None,
    bold=True
):
    if severity:
        color = get_severity_color(severity).name()

    else:
        color = DEFAULT_TEXT_COLOR

    style = f"color:{color};"

    if bold:
        style += "font-weight:bold;"

    widget.setStyleSheet(
        style
    )