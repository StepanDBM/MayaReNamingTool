from utils.qt import (
    QtWidgets,
    QtCore
)
from importlib import reload

from ui.style.styleSheets import MAYA_STYLE
from ui.tabs import (
    rename_tab,
    recolors_tab,
    validation_tab,
    selection_tab
)

from ui.widgets import collapsibleSection as collSect

reload(rename_tab)
reload(validation_tab)
reload(recolors_tab)
reload(selection_tab)
reload(collSect)

from utils.qt import get_environment_info

LEFT_SCROLL_WIDTH = 338
LEFT_CONTENT_WIDTH = 320
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

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(LEFT_SCROLL_WIDTH+22)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setStyleSheet(MAYA_STYLE)

        self.build_ui()

    def resizeEvent(self, event):

        super().resizeEvent(event)

        width = self.width()
        print(self.width())
        print(self.height())

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
            "windowGeometry",
            self.saveGeometry()
        )

        self.settings.setValue(
            "mainSplitterState",
            self.main_splitter.saveState()
        )

        self.settings.setValue(
            "renameSectionExpanded",
            self.rename_section.is_expanded()
        )

        self.settings.setValue(
            "recolorSectionExpanded",
            self.recolor_section.is_expanded()
        )

        self.settings.setValue(
            "SelectionSectionExpanded",
            self.selection_section.is_expanded()
        )


        self.validation_tab.save_layout_state()

        super().closeEvent(event)

    def build_ui(self):

        LEFT_CONTENT_WIDTH = 320
        LEFT_SCROLL_WIDTH = 338

        layout = QtWidgets.QVBoxLayout(self)

        self.main_splitter = QtWidgets.QSplitter(
            QtCore.Qt.Horizontal
        )

        layout.addWidget(
            self.main_splitter
        )

        # ---------------------------------
        # LEFT SCROLL AREA
        # ---------------------------------

        self.left_scroll = QtWidgets.QScrollArea()

        self.left_scroll.setWidgetResizable(
            True
        )

        self.left_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )

        self.left_scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded
        )

        self.left_scroll.setFrameShape(
            QtWidgets.QFrame.NoFrame
        )

        self.left_scroll.setMinimumWidth(
            LEFT_SCROLL_WIDTH
        )

        self.left_scroll.setMaximumWidth(
            LEFT_SCROLL_WIDTH
        )

        self.left_widget = QtWidgets.QWidget()

        self.left_widget.setMinimumWidth(
            LEFT_CONTENT_WIDTH
        )

        self.left_widget.setMaximumWidth(
            LEFT_CONTENT_WIDTH
        )

        self.left_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Minimum
        )

        left_layout = QtWidgets.QVBoxLayout(
            self.left_widget
        )

        left_layout.setContentsMargins(
            0, 0, 0, 0
        )

        left_layout.setSpacing(
            2
        )

        left_layout.setAlignment(
            QtCore.Qt.AlignTop
        )

        left_layout.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize
        )

        self.left_scroll.setWidget(
            self.left_widget
        )

        # -------------------------
        # RESTORE COLLAPSIBLE STATE
        # -------------------------

        rename_expanded = self.settings.value(
            "renameSectionExpanded",
            True,
            type=bool
        )

        recolor_expanded = self.settings.value(
            "recolorSectionExpanded",
            True,
            type=bool
        )

        selection_expanded = self.settings.value(
            "selectionSectionExpanded",
            False,
            type=bool
        )

        # -------------------------
        # TABS
        # -------------------------

        self.rename_tab = rename_tab.RenameTab()
        self.recolors_tab = recolors_tab.RecolorsTab()
        self.selection_tab = selection_tab.SelectionTab()

        # -------------------------
        # COLLAPSIBLE SECTIONS
        # -------------------------

        self.rename_section = collSect.CollapsibleSection(
            "reName",
            self.rename_tab,
            expanded=rename_expanded
        )

        self.recolor_section = collSect.CollapsibleSection(
            "reColors",
            self.recolors_tab,
            expanded=recolor_expanded
        )

        self.selection_section = collSect.CollapsibleSection(
            "reSelection",
            self.selection_tab,
            expanded=selection_expanded
        )

        left_layout.addWidget(
            self.rename_section
        )

        left_layout.addWidget(
            self.recolor_section
        )

        left_layout.addWidget(
            self.selection_section
        )

        left_layout.addStretch()

        # Important when setWidgetResizable(False)
        self.left_widget.adjustSize()

        self.left_widget.setMinimumHeight(
            self.left_widget.sizeHint().height()
        )

        self.left_scroll.setWidget(
            self.left_widget
        )

        # -------------------------
        # RIGHT SIDE
        # -------------------------

        self.validation_tab = validation_tab.ValidationTab()

        self.validation_tab.setMinimumWidth(
            0
        )

        self.validation_tab.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        # -------------------------
        # SPLITTER
        # -------------------------

        self.main_splitter.addWidget(
            self.left_scroll
        )

        self.main_splitter.addWidget(
            self.validation_tab
        )

        self.main_splitter.setStretchFactor(
            0,
            0
        )

        self.main_splitter.setStretchFactor(
            1,
            1
        )

        # -------------------------
        # RESTORE SETTINGS
        # -------------------------

        splitter_state = self.settings.value(
            "mainSplitterState"
        )

        geometry = self.settings.value(
            "windowGeometry"
        )

        if geometry:

            self.restoreGeometry(
                geometry
            )

        else:

            self.resize(
                1000,
                640
            )

            screen = QtWidgets.QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()

            self.move(
                screen_geometry.center()
                - self.rect().center()
            )

        if splitter_state:

            self.main_splitter.restoreState(
                splitter_state
            )