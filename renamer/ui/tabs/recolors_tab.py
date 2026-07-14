# ui/tabs/recolors_tab.py

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

        color = QtWidgets.QColorDialog.getColor()

        if not color.isValid():
            return

        self.r_spin.setValue(color.red())

        self.g_spin.setValue(color.green())

        self.b_spin.setValue(color.blue())

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

    def build_ui(self):

        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.setSpacing(2)

        self.color_label = QtWidgets.QLabel("Color")

        main_layout.addWidget(self.color_label)

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

        self.rgb_label = QtWidgets.QLabel(
            "255, 255, 255"
        )

        self.rgb_label.setAlignment(
            QtCore.Qt.AlignCenter
        )

        self.rgb_label.setMinimumWidth(
            90
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
            "#59ffe7",
            "#4fa0ff",
            "#ff71b4",
            "#c956e5",
            "#7633e5",
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

            color_grid.addWidget(
                btn,
                0,
                len(self.color_buttons)
            )

            self.color_buttons.append(
                btn
            )

        main_layout.addLayout(
            color_grid
        )

        color_actions = QtWidgets.QHBoxLayout()

        self.apply_color_btn = (
            QtWidgets.QPushButton(
                "Apply Color"
            )
        )

        self.reset_color_btn = (
            QtWidgets.QPushButton(
                "Reset Color"
            )
        )

        self.dview_btn = (
            QtWidgets.QPushButton(
                "DView Color"
            )
        )

        self.doutliner_btn = (
            QtWidgets.QPushButton(
                "DOut Color"
            )
        )

        color_actions.addWidget(
            self.apply_color_btn
        )

        color_actions.addWidget(
            self.reset_color_btn
        )

        color_actions.addWidget(
            self.dview_btn
        )

        color_actions.addWidget(
            self.doutliner_btn
        )

        main_layout.addLayout(
            color_actions
        )

        #main_layout.addStretch()

    def create_connections(self):

        self.color_dialog_btn.clicked.connect(
            self.pick_color
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