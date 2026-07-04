from PySide2 import QtWidgets, QtCore

from ui.styleSheets import MAYA_STYLE
from operations import rename

from utils.Qt_utils import lighter_color, darker_color

class RenamerMainWindow(QtWidgets.QWidget):

    WINDOW_TITLE = "reName_reColor"

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(320)
        self.setWindowFlags(
            QtCore.Qt.Window
        )
        """this allows MAYA to keep the window on top of other
        itself and other windows Otherwise if viewport is clicked
        or anything in outliner is clicked this just disappears
        in Window's window manager."""
        self.setStyleSheet(MAYA_STYLE)
        self.build_ui()
        self.create_connections()


    # UI
    def build_ui(self):

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(3)

        # Rename and Number
        self.rename_line = QtWidgets.QLineEdit()

        self.start_spin = QtWidgets.QSpinBox()
        self.start_spin.setValue(1)

        self.padding_spin = QtWidgets.QSpinBox()
        self.padding_spin.setValue(2)

        rename_form = QtWidgets.QFormLayout()
        rename_form.addRow("Rename:", self.rename_line)

        row = QtWidgets.QHBoxLayout()
        row.addWidget(QtWidgets.QLabel("Start #:"))
        row.addWidget(self.start_spin)
        row.addWidget(QtWidgets.QLabel("Padding:"))
        row.addWidget(self.padding_spin)
        self.rename_number_btn = QtWidgets.QPushButton("Rename and Number")
        row.addWidget(self.rename_number_btn)

        main_layout.addLayout(rename_form)
        main_layout.addLayout(row)


        # Remove
        remove_layout = QtWidgets.QHBoxLayout()

        self.remove_first_btn = QtWidgets.QPushButton("First Character →")

        self.remove_last_btn = QtWidgets.QPushButton("← Last Character")

        remove_layout.addWidget(self.remove_first_btn)
        remove_layout.addWidget(self.remove_last_btn)

        main_layout.addLayout(remove_layout)

        # Hash Rename
        hash_layout = QtWidgets.QHBoxLayout()

        self.hash_line = QtWidgets.QLineEdit("name_####_suffix")

        self.hash_btn = QtWidgets.QPushButton("Rename")

        hash_layout.addWidget(QtWidgets.QLabel("Hash Rename"))

        hash_layout.addWidget(self.hash_line)
        hash_layout.addWidget(self.hash_btn)

        main_layout.addLayout(hash_layout)

        # Prefix
        prefix_layout = QtWidgets.QHBoxLayout()

        self.prefix_line = QtWidgets.QLineEdit("prefix_")

        self.prefix_add_btn = QtWidgets.QPushButton("Add")

        self.prefix_hier_btn = QtWidgets.QPushButton("Hier")

        prefix_layout.addWidget(QtWidgets.QLabel("(Before)"))

        prefix_layout.addWidget(self.prefix_line)
        prefix_layout.addWidget(self.prefix_add_btn)
        prefix_layout.addWidget(self.prefix_hier_btn)

        main_layout.addLayout(prefix_layout)

        # Suffix
        suffix_layout = QtWidgets.QHBoxLayout()

        self.suffix_line = QtWidgets.QLineEdit("_suffix")

        self.suffix_add_btn = QtWidgets.QPushButton("Add")

        self.suffix_hier_btn = QtWidgets.QPushButton("Hier")

        suffix_layout.addWidget(QtWidgets.QLabel("(After)"))

        suffix_layout.addWidget(self.suffix_line)
        suffix_layout.addWidget(self.suffix_add_btn)
        suffix_layout.addWidget(self.suffix_hier_btn)

        main_layout.addLayout(suffix_layout)

        # Quick Suffix
        quick_grid = QtWidgets.QGridLayout()

        quick_suffixes = [
            "_grp",
            "_geo",
            "_jnt",
            "_drv",
            "_lgt",
            "_BND",
            "_low",
            "_high",
            "_offs",
            "_auto",
            "_anim",
            "_ctrl",
        ]

        self.quick_suffix_buttons = []

        for index, suffix in enumerate(quick_suffixes):

            button = QtWidgets.QPushButton(suffix)
            button.setProperty("quickSuffix", True)

            row = index // 6
            col = index % 6

            quick_grid.addWidget(button, row, col)

            self.quick_suffix_buttons.append(button)

        main_layout.addLayout(quick_grid)

        # Search Replace
        search_replace_layout = QtWidgets.QFormLayout()

        self.l_to_r_btn = QtWidgets.QPushButton("L -> R")

        self.r_to_l_btn = QtWidgets.QPushButton("R -> L")

        self.search_line = QtWidgets.QLineEdit("pasted_")

        self.replace_line = QtWidgets.QLineEdit()

        search_replace_layout.addRow(
            self.l_to_r_btn,
            self.search_line
        )

        search_replace_layout.addRow(
            self.r_to_l_btn,
            self.replace_line
        )

        main_layout.addLayout(search_replace_layout)

        self.hierarchy_radio = QtWidgets.QRadioButton("Hierarchy")

        self.selected_radio = QtWidgets.QRadioButton("Selected")

        self.all_radio = QtWidgets.QRadioButton("All")

        self.hierarchy_radio.setChecked(True)

        radio_layout = QtWidgets.QHBoxLayout()

        radio_layout.addWidget(self.hierarchy_radio)
        radio_layout.addWidget(self.selected_radio)
        radio_layout.addWidget(self.all_radio)

        main_layout.addLayout(radio_layout)

        self.apply_search_btn = QtWidgets.QPushButton("Apply")

        main_layout.addWidget(self.apply_search_btn)

        # Color
        self.color_label = QtWidgets.QLabel("Color")

        self.color_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        main_layout.addWidget(self.color_label)

        main_layout.addWidget(self.color_slider)

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

            hover_color = lighter_color(color)
            pressed_color = darker_color(color)

            btn = QtWidgets.QPushButton()

            btn.setProperty("colorButton", True)

            btn.setFixedHeight(22)

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

            self.color_buttons.append(btn)

        main_layout.addLayout(color_grid)

        color_actions = QtWidgets.QHBoxLayout()

        self.apply_color_btn = QtWidgets.QPushButton("Apply Color")

        self.reset_color_btn = QtWidgets.QPushButton("Reset Color")

        self.dview_btn = QtWidgets.QPushButton("DView Color")

        self.doutliner_btn = QtWidgets.QPushButton("DOut Color")

        color_actions.addWidget(self.apply_color_btn)

        color_actions.addWidget(self.reset_color_btn)

        color_actions.addWidget(self.dview_btn)

        color_actions.addWidget(self.doutliner_btn)

        main_layout.addLayout(color_actions)

    # Connections
    def create_connections(self):

        self.rename_number_btn.clicked.connect(
            lambda: rename.rename_and_number(
                self.rename_line.text(),
                self.start_spin.value(),
                self.padding_spin.value()
                )

        )
        self.remove_first_btn.clicked.connect(
            lambda: rename.remove_character("first")
        )
        self.remove_last_btn.clicked.connect(
            lambda: rename.remove_character("last")
        )
        self.hash_btn.clicked.connect(
            lambda: rename.hash_rename(self.hash_line.text())
        )
        self.prefix_add_btn.clicked.connect(
            lambda: rename.add_prefix(self.prefix_line.text())
        )
        self.prefix_hier_btn.clicked.connect(
            lambda: rename.add_prefix_hierarchy(self.prefix_line.text())
        )
        self.suffix_add_btn.clicked.connect(
            lambda: rename.add_suffix(self.suffix_line.text())

        )
        self.suffix_hier_btn.clicked.connect(
            lambda: rename.add_suffix_hierarchy(self.suffix_line.text())
        )
        self.l_to_r_btn.clicked.connect(
            lambda: print("L -> R")
        )
        self.r_to_l_btn.clicked.connect(
            lambda: print("R -> L")
        )

        self.apply_search_btn.clicked.connect(
            lambda: print("Search Replace")
        )
        self.apply_color_btn.clicked.connect(
            lambda: print("Apply Color")
        )
        self.reset_color_btn.clicked.connect(
            lambda: print("Reset Color")
        )
        self.dview_btn.clicked.connect(
            lambda: print("Display View Color")
        )
        self.doutliner_btn.clicked.connect(
            lambda: print("Display Outliner Color")
        )
        for button in self.quick_suffix_buttons:

            button.clicked.connect(
                lambda checked=False,
                s=button.text():
                rename.quick_suffix(
                    f"_{s}"
                )
            )
        for button in self.color_buttons:

            button.clicked.connect(
                lambda checked=False,
                b=button:
                print(
                    f"Preset Color: {b.styleSheet()}"
                )
            )