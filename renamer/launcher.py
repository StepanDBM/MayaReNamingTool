import __main__

from ui.main_window import RenamerMainWindow
from utils.maya_utils import maya_main_window


def show():

    try:
        __main__.RENAMER_WINDOW.close()
        __main__.RENAMER_WINDOW.deleteLater()
    except Exception:
        pass

    __main__.RENAMER_WINDOW = RenamerMainWindow(
        parent=maya_main_window()
    )

    __main__.RENAMER_WINDOW.show()