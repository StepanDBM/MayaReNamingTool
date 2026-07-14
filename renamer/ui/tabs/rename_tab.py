# ui/tabs/rename_tab.py

from utils.qt import (
    QtWidgets,
    QtCore
)

from operations import rename
from operations import search_replace


class RenameTab(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.quick_suffix_uppercase = False

        self.build_ui()
        self.create_connections()

    def add_section(self, title):

        section_layout = QtWidgets.QHBoxLayout()

        left = QtWidgets.QFrame()
        left.setFrameShape(
            QtWidgets.QFrame.HLine
        )

        right = QtWidgets.QFrame()
        right.setFrameShape(
            QtWidgets.QFrame.HLine
        )

        label = QtWidgets.QLabel(title)

        label.setStyleSheet(
            "font-weight:bold;"
        )

        section_layout.addWidget(left)
        section_layout.addWidget(label)
        section_layout.addWidget(right)

        self.layout().addLayout(
            section_layout
        )

    def toggle_quick_suffix_case(self):

        self.quick_suffix_uppercase = (
            not self.quick_suffix_uppercase
        )

        for button in self.quick_suffix_buttons:

            text = button.text()

            if self.quick_suffix_uppercase:
                button.setText(text.upper())

            else:
                button.setText(text.lower())

    def get_search_mode(self):

        if self.hierarchy_radio.isChecked():
            return "hierarchy"

        if self.all_radio.isChecked():
            return "all"

        return "selected"

    def build_ui(self):

        main_layout = QtWidgets.QVBoxLayout(
            self
        )

        main_layout.setSpacing(3)

        # -------------------------
        # Strip Namespace
        # -------------------------

        self.add_section(
            "--------------- Strip Namespaces ---------------"
        )

        namespace_layout = QtWidgets.QHBoxLayout()

        self.stripDots = QtWidgets.QLabel(
            "Stripping..."
        )

        self.strip_namespace_btn = (
            QtWidgets.QPushButton(
                "Namespace"
            )
        )

        self.strip_namespace_hier_btn = (
            QtWidgets.QPushButton(
                "Hierarchy Namespace"
            )
        )

        namespace_layout.addWidget(
            self.stripDots
        )

        namespace_layout.addWidget(
            self.strip_namespace_btn
        )

        namespace_layout.addWidget(
            self.strip_namespace_hier_btn
        )

        main_layout.addLayout(
            namespace_layout
        )

        # -------------------------
        # Rename & Number
        # -------------------------

        self.add_section(
            "--------------- Rename and Number ---------------"
        )

        self.rename_line = (
            QtWidgets.QLineEdit()
        )

        self.start_spin = (
            QtWidgets.QSpinBox()
        )

        self.start_spin.setValue(1)

        self.padding_spin = (
            QtWidgets.QSpinBox()
        )

        self.padding_spin.setValue(2)

        rename_form = (
            QtWidgets.QFormLayout()
        )

        rename_form.addRow(
            "Rename:",
            self.rename_line
        )

        row = QtWidgets.QHBoxLayout()

        row.addWidget(
            QtWidgets.QLabel(
                "Start #:"
            )
        )

        row.addWidget(
            self.start_spin
        )

        row.addWidget(
            QtWidgets.QLabel(
                "Padding:"
            )
        )

        row.addWidget(
            self.padding_spin
        )

        self.rename_number_btn = (
            QtWidgets.QPushButton(
                "Rename and Number"
            )
        )

        row.addWidget(
            self.rename_number_btn
        )

        main_layout.addLayout(
            rename_form
        )

        main_layout.addLayout(
            row
        )

        # -------------------------
        # Remove Characters
        # -------------------------

        self.add_section(
            "--------------- Add/Remove Characters ---------------"
        )

        remove_layout = (
            QtWidgets.QHBoxLayout()
        )

        self.removeDotsLabel = (
            QtWidgets.QLabel(
                "Removing..."
            )
        )

        self.remove_first_btn = (
            QtWidgets.QPushButton(
                "First Character →"
            )
        )

        self.remove_last_btn = (
            QtWidgets.QPushButton(
                "← Last Character"
            )
        )

        remove_layout.addWidget(
            self.removeDotsLabel
        )

        remove_layout.addWidget(
            self.remove_first_btn
        )

        remove_layout.addWidget(
            self.remove_last_btn
        )

        main_layout.addLayout(
            remove_layout
        )

        # -------------------------
        # Hash Rename
        # -------------------------

        hash_layout = QtWidgets.QHBoxLayout()

        self.hash_line = QtWidgets.QLineEdit(
            "name_####_suffix"
        )

        self.hash_btn = (
            QtWidgets.QPushButton(
                "Rename"
            )
        )

        hash_layout.addWidget(
            QtWidgets.QLabel(
                "Hash Rename"
            )
        )

        hash_layout.addWidget(
            self.hash_line
        )

        hash_layout.addWidget(
            self.hash_btn
        )

        main_layout.addLayout(
            hash_layout
        )

        # -------------------------
        # Prefix
        # -------------------------

        prefix_layout = (
            QtWidgets.QHBoxLayout()
        )

        self.prefix_line = (
            QtWidgets.QLineEdit(
                "prefix_"
            )
        )

        self.prefix_add_btn = (
            QtWidgets.QPushButton(
                "Add"
            )
        )

        self.prefix_hier_btn = (
            QtWidgets.QPushButton(
                "Hier"
            )
        )

        prefix_layout.addWidget(
            QtWidgets.QLabel(
                "(Before)"
            )
        )

        prefix_layout.addWidget(
            self.prefix_line
        )

        prefix_layout.addWidget(
            self.prefix_add_btn
        )

        prefix_layout.addWidget(
            self.prefix_hier_btn
        )

        main_layout.addLayout(
            prefix_layout
        )

        # -------------------------
        # Suffix
        # -------------------------

        suffix_layout = (
            QtWidgets.QHBoxLayout()
        )

        self.suffix_line = (
            QtWidgets.QLineEdit(
                "_suffix"
            )
        )

        self.suffix_add_btn = (
            QtWidgets.QPushButton(
                "Add"
            )
        )

        self.suffix_hier_btn = (
            QtWidgets.QPushButton(
                "Hier"
            )
        )

        suffix_layout.addWidget(
            QtWidgets.QLabel(
                "(After)"
            )
        )

        suffix_layout.addWidget(
            self.suffix_line
        )

        suffix_layout.addWidget(
            self.suffix_add_btn
        )

        suffix_layout.addWidget(
            self.suffix_hier_btn
        )

        main_layout.addLayout(
            suffix_layout
        )

        # -------------------------
        # Quick Suffix
        # -------------------------

        quick_grid = QtWidgets.QGridLayout()

        self.quick_suffix_case_btn = (
            QtWidgets.QPushButton(
                "A2a"
            )
        )

        self.quick_suffix_case_btn.setMinimumWidth(
            40
        )

        self.quick_suffix_case_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Expanding
        )

        quick_grid.addWidget(
            self.quick_suffix_case_btn,
            0,
            0,
            2,
            1
        )

        quick_suffixes = [
            "grp",
            "geo",
            "jnt",
            "drv",
            "lgt",
            "BND",
            "low",
            "high",
            "offs",
            "auto",
            "anim",
            "ctrl",
        ]

        self.quick_suffix_buttons = []

        for index, suffix in enumerate(
            quick_suffixes
        ):

            button = QtWidgets.QPushButton(
                suffix
            )

            button.setProperty(
                "quickSuffix",
                True
            )

            row = index // 6
            col = (index % 6) + 1

            quick_grid.addWidget(
                button,
                row,
                col
            )

            self.quick_suffix_buttons.append(
                button
            )

        main_layout.addLayout(
            quick_grid
        )

        # -------------------------
        # Search Replace
        # -------------------------

        search_replace_layout = (
            QtWidgets.QFormLayout()
        )

        self.l_to_r_btn = (
            QtWidgets.QPushButton(
                "L -> R"
            )
        )

        self.r_to_l_btn = (
            QtWidgets.QPushButton(
                "R -> L"
            )
        )

        self.search_line = (
            QtWidgets.QLineEdit(
                "pasted_"
            )
        )

        self.replace_line = (
            QtWidgets.QLineEdit()
        )

        search_replace_layout.addRow(
            self.l_to_r_btn,
            self.search_line
        )

        search_replace_layout.addRow(
            self.r_to_l_btn,
            self.replace_line
        )

        main_layout.addLayout(
            search_replace_layout
        )

        self.hierarchy_radio = (
            QtWidgets.QRadioButton(
                "Hierarchy"
            )
        )

        self.selected_radio = (
            QtWidgets.QRadioButton(
                "Selected"
            )
        )

        self.all_radio = (
            QtWidgets.QRadioButton(
                "All"
            )
        )

        self.hierarchy_radio.setChecked(
            True
        )

        radio_layout = (
            QtWidgets.QHBoxLayout()
        )

        radio_layout.addWidget(
            self.hierarchy_radio
        )

        radio_layout.addWidget(
            self.selected_radio
        )

        radio_layout.addWidget(
            self.all_radio
        )

        main_layout.addLayout(
            radio_layout
        )

        self.apply_search_btn = (
            QtWidgets.QPushButton(
                "Apply"
            )
        )

        main_layout.addWidget(
            self.apply_search_btn
        )

        #main_layout.addStretch()

    def create_connections(self):

        self.strip_namespace_btn.clicked.connect(
            lambda:
            rename.strip_namespace()
        )

        self.strip_namespace_hier_btn.clicked.connect(
            lambda:
            rename.strip_namespace_hierarchy()
        )

        self.rename_number_btn.clicked.connect(
            lambda:
            rename.rename_and_number(
                self.rename_line.text(),
                self.start_spin.value(),
                self.padding_spin.value()
            )
        )

        self.remove_first_btn.clicked.connect(
            lambda:
            rename.remove_character(
                "first"
            )
        )

        self.remove_last_btn.clicked.connect(
            lambda:
            rename.remove_character(
                "last"
            )
        )

        self.hash_btn.clicked.connect(
            lambda:
            rename.hash_rename(
                self.hash_line.text()
            )
        )

        self.prefix_add_btn.clicked.connect(
            lambda:
            rename.add_prefix(
                self.prefix_line.text()
            )
        )

        self.prefix_hier_btn.clicked.connect(
            lambda:
            rename.add_prefix_hierarchy(
                self.prefix_line.text()
            )
        )

        self.suffix_add_btn.clicked.connect(
            lambda:
            rename.add_suffix(
                self.suffix_line.text()
            )
        )

        self.suffix_hier_btn.clicked.connect(
            lambda:
            rename.add_suffix_hierarchy(
                self.suffix_line.text()
            )
        )

        self.l_to_r_btn.clicked.connect(
            lambda:
            search_replace.set_l_to_r_values(
                self
            )
        )

        self.r_to_l_btn.clicked.connect(
            lambda:
            search_replace.set_r_to_l_values(
                self
            )
        )

        self.apply_search_btn.clicked.connect(
            lambda:
            search_replace.search_replace(
                self.search_line.text(),
                self.replace_line.text(),
                self.get_search_mode()
            )
        )

        self.quick_suffix_case_btn.clicked.connect(
            self.toggle_quick_suffix_case
        )

        for button in self.quick_suffix_buttons:

            button.clicked.connect(
                lambda checked=False,
                b=button:
                rename.quick_suffix(
                    b.text()
                )
            )