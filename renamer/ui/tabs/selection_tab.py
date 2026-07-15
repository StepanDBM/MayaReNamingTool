# ui/tabs/selection_tab.py

from importlib import reload

from utils.qt import QtWidgets, QtCore

from operations import selection as selection_ops

reload(selection_ops)


class SelectionTab(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.build_ui()
        self.create_connections()
        self.refresh_preset_list()

    # --------------------------------------------------
    # UI helpers
    # --------------------------------------------------

    def make_button(
        self,
        text,
        wide=False
    ):
        button = QtWidgets.QPushButton(text)
        button.setProperty(
            "selectionWideButton"
            if wide
            else "selectionButton",
            True
        )
        button.setFixedHeight(22)

        return button

    def add_section(self, title):

        section_layout = QtWidgets.QHBoxLayout()
        section_layout.setContentsMargins(0, 4, 0, 0)
        section_layout.setSpacing(4)

        left = QtWidgets.QFrame()
        left.setFrameShape(QtWidgets.QFrame.HLine)

        right = QtWidgets.QFrame()
        right.setFrameShape(QtWidgets.QFrame.HLine)

        label = QtWidgets.QLabel(title)
        label.setProperty("sectionTitle", True)

        section_layout.addWidget(left)
        section_layout.addWidget(label)
        section_layout.addWidget(right)

        self.layout().addLayout(section_layout)

    def get_selection_mode(self):

        if self.add_radio.isChecked():
            return "add"

        if self.remove_radio.isChecked():
            return "remove"

        return "replace"

    def get_selected_preset_name(self):

        item = self.preset_list.currentItem()

        if not item:
            return None

        return item.text()

    def refresh_preset_list(self):

        current_name = self.get_selected_preset_name()
        self.preset_list.clear()

        names = selection_ops.get_selection_preset_names()
        for name in names:
            self.preset_list.addItem(name)

        if not current_name:
            return

        matching_items = self.preset_list.findItems(
            current_name,
            QtCore.Qt.MatchExactly
        )

        if matching_items:

            self.preset_list.setCurrentItem(matching_items[0])

    # --------------------------------------------------
    # Build UI
    # --------------------------------------------------

    def build_ui(self):

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(6, 4, 6, 6)
        main_layout.setSpacing(3)

        # --------------------------------------------------
        # Mode
        # --------------------------------------------------
        
        self.modeLabel = QtWidgets.QLabel("Mode:   ")
        mode_layout = QtWidgets.QHBoxLayout()
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.setSpacing(6)

        self.replace_radio = QtWidgets.QRadioButton("Replace")
        self.add_radio = QtWidgets.QRadioButton("Add")
        self.remove_radio = QtWidgets.QRadioButton("Remove")

        self.replace_radio.setChecked(True)

        mode_layout.addWidget(self.modeLabel)
        mode_layout.addWidget(self.replace_radio)
        mode_layout.addWidget(self.add_radio)
        mode_layout.addWidget(self.remove_radio)

        mode_layout.addStretch()

        main_layout.addLayout(mode_layout)

        # --------------------------------------------------
        # Pattern
        # --------------------------------------------------

        self.add_section("Pattern")

        pattern_layout = QtWidgets.QHBoxLayout()
        pattern_layout.setContentsMargins(0, 0, 0, 0)
        pattern_layout.setSpacing(3)

        self.pattern_line = QtWidgets.QLineEdit("*_ctrl")
        self.pattern_line.setFixedHeight(22)

        self.pattern_btn = self.make_button("Select")
        self.invert_btn = self.make_button("Invert")

        pattern_layout.addWidget(self.pattern_line)
        pattern_layout.addWidget(self.pattern_btn)
        pattern_layout.addWidget(self.invert_btn)

        main_layout.addLayout(pattern_layout)

        # --------------------------------------------------
        # Hierarchy
        # --------------------------------------------------

        self.add_section("Hierarchy")

        hierarchy_layout = QtWidgets.QHBoxLayout()
        hierarchy_layout.setContentsMargins(0, 0, 0, 0)
        hierarchy_layout.setSpacing(3)

        self.hierarchy_btn = self.make_button("Hierarchy")
        self.children_btn = self.make_button("Children")
        self.parents_btn = self.make_button("Parents")

        hierarchy_layout.addWidget(self.hierarchy_btn)
        hierarchy_layout.addWidget(self.children_btn)
        hierarchy_layout.addWidget(self.parents_btn)

        main_layout.addLayout(hierarchy_layout)

        # --------------------------------------------------
        # By Type
        # --------------------------------------------------

        self.add_section("By Type")

        type_grid = QtWidgets.QGridLayout()

        type_grid.setContentsMargins(0, 0, 0, 0)
        type_grid.setHorizontalSpacing(3)
        type_grid.setVerticalSpacing(3)

        self.joints_btn = self.make_button("Joints")
        self.meshes_btn = self.make_button("Meshes")
        self.curves_btn = self.make_button("Curves")
        self.locators_btn = self.make_button("Locators")
        self.cameras_btn = self.make_button("Cameras")
        self.transforms_btn = self.make_button("Transforms")
        self.same_type_btn = self.make_button("Same Type", wide=True)

        type_grid.addWidget(self.joints_btn, 0, 0)
        type_grid.addWidget(self.meshes_btn, 0, 1)
        type_grid.addWidget(self.curves_btn, 0, 2)
        type_grid.addWidget(self.locators_btn, 1, 0)
        type_grid.addWidget(self.cameras_btn, 1, 1)
        type_grid.addWidget(self.transforms_btn, 1, 2)
        type_grid.addWidget(self.same_type_btn, 2, 0, 1, 3)

        main_layout.addLayout(type_grid)

        # --------------------------------------------------
        # By Name
        # --------------------------------------------------

        self.add_section("By Name")

        name_layout = QtWidgets.QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(3)

        self.same_prefix_btn = self.make_button("Same Prefix")
        self.same_suffix_btn = self.make_button("Same Suffix")

        name_layout.addWidget(self.same_prefix_btn)
        name_layout.addWidget(self.same_suffix_btn)

        main_layout.addLayout(name_layout)

        # --------------------------------------------------
        # Stored Selection
        # --------------------------------------------------

        self.add_section("Stored Selection")

        preset_name_layout = QtWidgets.QHBoxLayout()
        preset_name_layout.setContentsMargins(0, 0, 0, 0)
        preset_name_layout.setSpacing(3)

        self.preset_name_line = QtWidgets.QLineEdit()
        self.preset_name_line.setPlaceholderText("Preset name...")
        self.preset_name_line.setFixedHeight(22)

        self.store_btn = self.make_button("Store")

        preset_name_layout.addWidget(self.preset_name_line)
        preset_name_layout.addWidget(self.store_btn)

        main_layout.addLayout(preset_name_layout)

        self.preset_list = QtWidgets.QListWidget()
        self.preset_list.setProperty("selectionPresetList", True)
        self.preset_list.setMaximumHeight(58)
        self.preset_list.setMinimumHeight(42)

        main_layout.addWidget(self.preset_list)

        preset_actions_layout = QtWidgets.QHBoxLayout()
        preset_actions_layout.setContentsMargins(0, 0, 0, 0)
        preset_actions_layout.setSpacing(3)

        self.restore_btn = self.make_button("Restore")

        self.delete_preset_btn = self.make_button("Delete")

        preset_actions_layout.addWidget(self.restore_btn)
        preset_actions_layout.addWidget(self.delete_preset_btn)

        main_layout.addLayout(preset_actions_layout)

        # --------------------------------------------------
        # Log
        # --------------------------------------------------
        self.log_label = QtWidgets.QLabel("Ready.")
        self.log_label.setStyleSheet("color:#9f9f9f;")
        self.log_label.setFixedHeight(18)

        main_layout.addWidget(self.log_label)

    # --------------------------------------------------
    # Connections
    # --------------------------------------------------

    def create_connections(self):

        self.pattern_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_by_pattern,
                "Selected pattern.",
                self.pattern_line.text(),
                self.get_selection_mode()
            )
        )

        self.pattern_line.returnPressed.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_by_pattern,
                "Selected pattern.",
                self.pattern_line.text(),
                self.get_selection_mode()
            )
        )

        self.invert_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.invert_selection,
                "Inverted selection.",
                self.get_selection_mode()
            )
        )

        self.hierarchy_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_hierarchy,
                "Selected hierarchy.",
                self.get_selection_mode()
            )
        )

        self.children_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_children,
                "Selected children.",
                self.get_selection_mode()
            )
        )

        self.parents_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_parents,
                "Selected parents.",
                self.get_selection_mode()
            )
        )

        self.joints_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_type_joints,
                "Selected joints.",
                self.get_selection_mode()
            )
        )

        self.meshes_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_type_meshes,
                "Selected meshes.",
                self.get_selection_mode()
            )
        )

        self.curves_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_type_curves,
                "Selected curves.",
                self.get_selection_mode()
            )
        )

        self.locators_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_type_locators,
                "Selected locators.",
                self.get_selection_mode()
            )
        )

        self.cameras_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_type_cameras,
                "Selected cameras.",
                self.get_selection_mode()
            )
        )

        self.transforms_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_type_transforms,
                "Selected transforms.",
                self.get_selection_mode()
            )
        )

        self.same_type_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_same_type,
                "Selected same type.",
                self.get_selection_mode()
            )
        )

        self.same_prefix_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_same_prefix,
                "Selected same prefix.",
                self.get_selection_mode()
            )
        )

        self.same_suffix_btn.clicked.connect(
            lambda:
            self.run_selection_action(
                selection_ops.select_same_suffix,
                "Selected same suffix.",
                self.get_selection_mode()
            )
        )

        self.store_btn.clicked.connect(self.store_preset)

        self.restore_btn.clicked.connect(self.restore_selected_preset)

        self.delete_preset_btn.clicked.connect(self.delete_selected_preset)

        self.preset_list.itemClicked.connect(self.restore_preset_from_item)

    # --------------------------------------------------
    # Presets
    # --------------------------------------------------

    def store_preset(self):

        name = (
            self.preset_name_line.text()
            .strip()
        )

        if not name:

            name = selection_ops.get_next_preset_name()

        result = selection_ops.store_selection_preset(name)

        self.refresh_preset_list()

        matching_items = self.preset_list.findItems(
            name,
            QtCore.Qt.MatchExactly
        )

        if matching_items:

            self.preset_list.setCurrentItem(
                matching_items[0]
            )

        count = len(result) if result else 0

        self.log_label.setText(
            f"Stored '{name}'. ({count})"
        )

    def restore_selected_preset(self):

        name = self.get_selected_preset_name()

        if not name:

            self.log_label.setText("No preset selected.")

            return

        self.run_selection_action(
            selection_ops.restore_selection_preset,
            f"Restored '{name}'.",
            name,
            self.get_selection_mode()
        )

    def restore_preset_from_item(self, item):

        if not item:
            return

        name = item.text()

        self.run_selection_action(
            selection_ops.restore_selection_preset,
            f"Restored '{name}'.",
            name,
            self.get_selection_mode()
        )

    def delete_selected_preset(self):

        name = self.get_selected_preset_name()

        if not name:

            self.log_label.setText("No preset selected.")

            return

        selection_ops.delete_selection_preset(name)

        self.refresh_preset_list()

        self.log_label.setText(
            f"Deleted '{name}'."
        )

    # --------------------------------------------------
    # Runner
    # --------------------------------------------------

    def run_selection_action(
        self,
        function,
        message,
        *args
    ):

        result = function(
            *args
        )

        count = len(result) if result else 0

        self.log_label.setText(
            f"{message} ({count})"
        )