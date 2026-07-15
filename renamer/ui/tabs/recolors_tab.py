# ui/tabs/recolors_tab.py
from ui.style.styleSheets import MAYA_STYLE
from utils.qt import (
    QtWidgets,
    QtCore,
    QtGui
)

from operations import colors

from ui.style.QtColoring import (
    lighter_color,
    darker_color
)


class RecolorsTab(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.build_ui()
        self.create_connections()

    def pick_color(self):

        initial_color = QtGui.QColor(
            self.r_spin.value(),
            self.g_spin.value(),
            self.b_spin.value()
        )

        dialog = QtWidgets.QColorDialog(
            initial_color,
            self
        )

        dialog.setWindowTitle(
            "Pick Color"
        )

        dialog.setOption(
            QtWidgets.QColorDialog.DontUseNativeDialog,
            True
        )

        dialog.setStyleSheet(
            MAYA_STYLE
            + """
            QColorDialog
            {
                background-color: #3a3a3a;
            }
            """
        )

        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        color = dialog.currentColor()

        if not color.isValid():
            return

        self.r_spin.setValue(
            color.red()
        )

        self.g_spin.setValue(
            color.green()
        )

        self.b_spin.setValue(
            color.blue()
        )

    def apply_color(self):

        r = self.r_spin.value() / 255.0
        g = self.g_spin.value() / 255.0
        b = self.b_spin.value() / 255.0

        colors.apply_viewport_color(r, g, b)
        colors.apply_outliner_color(r, g, b)

    def set_color_from_button(self, hex_color):

        color = QtGui.QColor(hex_color)

        self.r_spin.setValue(color.red())

        self.g_spin.setValue(color.green())

        self.b_spin.setValue(color.blue())

    def update_color_preview(self):

        color = QtGui.QColor(
            self.r_spin.value(),
            self.g_spin.value(),
            self.b_spin.value()
        )

        self.color_preview.setStyleSheet(
            f"""
            background-color: {color.name()};
            border: 1px solid #222;
            """
        )

        self.rgb_label.setText(
            f"[{color.red()}, "
            f"{color.green()}, "
            f"{color.blue()}]"
        )
    def set_color_from_text(self):

        text = self.rgb_label.text().strip()

        try:

            text = text.replace(
                "[",
                ""
            ).replace(
                "]",
                ""
            )

            r, g, b = [
                int(value.strip())
                for value in text.split(",")
            ]

            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            self.r_spin.setValue(r)
            self.g_spin.setValue(g)
            self.b_spin.setValue(b)

        except Exception:

            self.update_color_preview()
    def build_ui(self):

        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.setContentsMargins(6, 6, 6, 6)

        main_layout.setSpacing(2)

        self.color_dialog_btn = (
            QtWidgets.QPushButton(
                "Pick Color"
            )
        )

        self.r_spin = QtWidgets.QSpinBox()
        self.g_spin = QtWidgets.QSpinBox()
        self.b_spin = QtWidgets.QSpinBox()

        for spin in (
            self.r_spin,
            self.g_spin,
            self.b_spin
        ):
            spin.setRange(
                0,
                255
            )

            spin.hide()

        picker_layout = QtWidgets.QHBoxLayout()

        self.rgb_label = QtWidgets.QLineEdit()

        self.rgb_label.setText(
            "[255, 255, 255]"
        )

        self.rgb_label.setMaximumWidth(
            95
        )

        self.rgb_label.setAlignment(
            QtCore.Qt.AlignCenter
        )

        self.rgb_label.setMinimumWidth(
            80
        )

        self.color_preview = QtWidgets.QFrame()

        self.color_preview.setFixedSize(
            80,
            24
        )

        self.color_preview.setFrameShape(
            QtWidgets.QFrame.Box
        )

        picker_layout.addWidget(
            self.color_dialog_btn
        )

        picker_layout.addWidget(
            self.rgb_label
        )
        self.rgb_label.editingFinished.connect(
            self.set_color_from_text
        )
        picker_layout.addWidget(
            self.color_preview
        )

        main_layout.addLayout(
            picker_layout
        )

        color_grid = QtWidgets.QGridLayout()

        preset_colors = [
            "#ff3939",
            "#ff6652",
            "#ff7a2c",
            "#ffff64",
            "#87ff47",
            "#ffffff",
            "#59ffe7",
            "#4fa0ff",
            "#ff71b4",
            "#c956e5",
            "#7633e5",
            "#000000",
        ]

        self.color_buttons = []

        for color in preset_colors:

            hover_color = lighter_color(
                color
            )

            pressed_color = darker_color(
                color
            )

            btn = QtWidgets.QPushButton()

            btn.color = color

            btn.setProperty(
                "colorButton",
                True
            )

            btn.setFixedHeight(
                22
            )

            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {color};
                    border: 1px solid #222;
                }}

                QPushButton:hover {{
                    background-color: {hover_color};
                }}

                QPushButton:pressed {{
                    background-color: {pressed_color};
                }}
                """
            )

            btn.setMinimumWidth(
                0
            )

            btn.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Fixed
            )

            row = len(self.color_buttons) // 6
            column = len(self.color_buttons) % 6

            color_grid.addWidget(
                btn,
                row,
                column
            )

            self.color_buttons.append(
                btn
            )

        main_layout.addLayout(
            color_grid
        )

        spacer = QtWidgets.QWidget()
        spacer.setFixedHeight(8)
        
        main_layout.addWidget(
            spacer
        )

        color_actions = QtWidgets.QGridLayout()

        color_actions.setContentsMargins(
            0, 0, 0, 0
        )

        color_actions.setHorizontalSpacing(
            3
        )

        color_actions.setVerticalSpacing(
            3
        )

        self.apply_color_btn = QtWidgets.QPushButton(
            "Apply Color"
        )

        self.reset_color_btn = QtWidgets.QPushButton(
            "Reset Color"
        )

        self.dview_btn = QtWidgets.QPushButton(
            "DView Color"
        )

        self.doutliner_btn = QtWidgets.QPushButton(
            "DOut Color"
        )

        for button in (
            self.apply_color_btn,
            self.reset_color_btn,
            self.dview_btn,
            self.doutliner_btn
        ):

            button.setMinimumWidth(
                0
            )

            button.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Fixed
            )

        color_actions.addWidget(
            self.apply_color_btn,
            0,
            0
        )

        color_actions.addWidget(
            self.reset_color_btn,
            0,
            1
        )

        color_actions.addWidget(
            self.dview_btn,
            1,
            0
        )

        color_actions.addWidget(
            self.doutliner_btn,
            1,
            1
        )

        main_layout.addLayout(
            color_actions
        )

        #main_layout.addStretch()

    def create_connections(self):

        self.color_dialog_btn.clicked.connect(
            self.pick_color
        )
        self.color_dialog_btn.setMinimumWidth(
            0
        )

        self.color_dialog_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        self.dview_btn.clicked.connect(
            lambda:
            colors.apply_viewport_color(
                self.r_spin.value() / 255.0,
                self.g_spin.value() / 255.0,
                self.b_spin.value() / 255.0
            )
        )

        self.doutliner_btn.clicked.connect(
            lambda:
            colors.apply_outliner_color(
                self.r_spin.value() / 255.0,
                self.g_spin.value() / 255.0,
                self.b_spin.value() / 255.0
            )
        )

        self.reset_color_btn.clicked.connect(
            colors.reset_colors
        )

        self.apply_color_btn.clicked.connect(
            self.apply_color
        )

        self.r_spin.valueChanged.connect(
            self.update_color_preview
        )

        self.g_spin.valueChanged.connect(
            self.update_color_preview
        )

        self.b_spin.valueChanged.connect(
            self.update_color_preview
        )

        for button in self.color_buttons:

            button.clicked.connect(
                lambda checked=False,
                color=button.color:
                self.set_color_from_button(
                    color
                )
            )