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
        self.settings = QtCore.QSettings(
            "StyopaDBM",
            "reNamePro"
        )

        self.setWindowTitle(
            self.WINDOW_TITLE
        )

        self.setMinimumWidth(340)

        self.setWindowFlags(
            QtCore.Qt.Window
        )

        self.setStyleSheet(
            MAYA_STYLE
        )

        self.build_ui()

    def resizeEvent(self, event):

        super().resizeEvent(event)

        width = self.width()

        if width >= 800:

            self.validation_tab.show()

            self.validation_tab.filters_widget.show()

            self.validation_tab.rules_widget.show()

        elif width >= 580:

            self.validation_tab.show()

            self.validation_tab.filters_widget.hide()

            self.validation_tab.rules_widget.hide()

        else:

            self.validation_tab.hide()

    def closeEvent(self, event):

        self.settings.setValue(
            "mainSplitterState",
            self.main_splitter.saveState()
        )
        self.validation_tab.save_layout_state()
        super().closeEvent(event)

    def build_ui(self):

        layout = QtWidgets.QVBoxLayout(self)

        self.main_splitter = QtWidgets.QSplitter(
            QtCore.Qt.Horizontal
        )

        layout.addWidget(self.main_splitter)

        self.rename_tab = rename_tab.RenameTab()
        self.rename_tab.setMinimumWidth(320)
        self.rename_tab.setMaximumWidth(320)

        self.validation_tab = validation_tab.ValidationTab()
        self.validation_tab.setMinimumWidth(0)

        self.rename_tab.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Expanding
        )

        self.validation_tab.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        self.main_splitter.addWidget(self.rename_tab)

        self.main_splitter.addWidget(self.validation_tab)
        splitter_state = self.settings.value("mainSplitterState")

        if splitter_state:
            self.main_splitter.restoreState(
                splitter_state
            )

        self.main_splitter.setStretchFactor(0,1)

        self.main_splitter.setStretchFactor(1,2)

