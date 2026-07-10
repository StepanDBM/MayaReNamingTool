from utils.qt import (
    QtWidgets,
    QtCore
)
from importlib import reload

from ui.style.styleSheets import MAYA_STYLE
from ui.tabs import rename_tab, validation_tab

reload(rename_tab)
reload(validation_tab)


from utils.qt import get_environment_info


class RenamerMainWindow(QtWidgets.QWidget):

    WINDOW_TITLE = (
        "reNamePro "
        + get_environment_info()
        + " - by Styopa DBM"
    )

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            self.WINDOW_TITLE
        )

        self.setMinimumWidth(320)

        self.setWindowFlags(
            QtCore.Qt.Window
        )

        self.setStyleSheet(
            MAYA_STYLE
        )

        self.build_ui()

    def build_ui(self):

        layout = QtWidgets.QVBoxLayout(self)

        self.tabs = QtWidgets.QTabWidget()

        layout.addWidget(
            self.tabs
        )

        self.main_splitter = QtWidgets.QSplitter(
            QtCore.Qt.Horizontal
        )

        layout.addWidget(
            self.main_splitter
        )

        self.rename_tab = rename_tab.RenameTab()
        self.rename_tab.setMinimumWidth(
            320
        )

        self.validation_tab = validation_tab.ValidationTab()
        self.validation_tab.setMinimumWidth(
            400
        )

        self.main_splitter.addWidget(
            self.rename_tab
        )

        self.main_splitter.addWidget(
            self.validation_tab
        )

        self.main_splitter.setStretchFactor(0,1)

        self.main_splitter.setStretchFactor(1,2)

