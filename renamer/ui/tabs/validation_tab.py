from importlib import reload
from utils.qt import (
    QtWidgets,
    QtCore,
    QtGui
)
from collections import defaultdict

from operations import validation
from ui.style import QtColoring
from config import severityTypes
from utils import maya_utils as mayUtil
from utils.loaders import loadNamingRules as N_Rules
reload(validation)
reload(QtColoring)
reload(severityTypes)
reload(N_Rules)


class ValidationTab(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        
        self.rules = N_Rules.load_rules()

        self.known_prefixes = set(
            self.rules["prefixes"]
        )

        self.side_tokens = set(
            self.rules["side_tokens"]
        )

        self.known_suffixes = set(
            self.rules["suffixes"]
        )

        self.known_types = (
            self.rules["types"]
        )

        self.naming_categories = (
            self.rules["categories"]
        )

        self.settings = QtCore.QSettings(
            "StyopaDBM",
            "reNamePro"
        )
        
        self.build_ui()
        self.create_connections()

    def save_layout_state(self):

        self.settings.setValue(
            "validationSplitterState",
            self.splitter.saveState()
        )


    def update_summary(self, issues):

        error_count = sum(
            1
            for issue in issues
            if issue["severity"] == "error"
        )

        warning_count = sum(
            1
            for issue in issues
            if issue["severity"] == "warning"
        )

        mindme_count = sum(
            1
            for issue in issues
            if issue["severity"] == "mind_me"
        )

        self.error_count_lbl.setText(
            f"Errors: {error_count}"
        )

        self.warning_count_lbl.setText(
            f"Warnings: {warning_count}"
        )

        self.mindme_count_lbl.setText(
            f"MindMe: {mindme_count}"
        )

        self.total_count_lbl.setText(
            f"Total: {len(issues)}"
        )

    def get_allowed_severities(self):

        severities = set()

        if self.error_cb.isChecked():
            severities.add("error")

        if self.warning_cb.isChecked():
            severities.add("warning")

        if self.mindme_cb.isChecked():
            severities.add("mind_me")

        return severities


    def get_allowed_categories(self):

        categories = set()

        for index in range(
            self.category_list.count()
        ):

            item = self.category_list.item(
                index
            )

            if item.checkState() == (
                QtCore.Qt.Checked
            ):
                categories.add(
                    item.data(
                        QtCore.Qt.UserRole
                    )
                )

        return categories
    
    def add_list_item(self, list_widget):

        text, ok = (
            QtWidgets.QInputDialog.getText(
                self,
                "Add Item",
                "Value:"
            )
        )

        if not ok:
            return

        text = text.strip()

        if not text:
            return

        list_widget.addItem(text)

        self.save_rules()

    def remove_list_item(self, list_widget):

        item = list_widget.currentItem()

        if not item:
            return

        row = list_widget.row(item)

        list_widget.takeItem(row)

        self.save_rules()


    def save_rules(self):

        self.rules["prefixes"] = [

            self.prefixes_list.item(i).text()

            for i in range(
                self.prefixes_list.count()
            )
        ]

        self.rules["suffixes"] = [

            self.suffixes_list.item(i).text()

            for i in range(
                self.suffixes_list.count()
            )
        ]

        self.rules["side_tokens"] = [

            self.sideTokens_list.item(i).text()

            for i in range(
                self.sideTokens_list.count()
            )
        ]

        N_Rules.save_rules(
            self.rules
        )
        self.known_prefixes = set(self.rules["prefixes"])
        self.known_suffixes = set(self.rules["suffixes"])
        self.side_tokens = set(self.rules["side_tokens"])
    
    def restore_default_rules(self):
        self.rules = (
            N_Rules.restore_default_rules()
        )

        self.prefixes_list.clear()
        self.suffixes_list.clear()
        self.sideTokens_list.clear()

        for prefix in sorted(
            self.rules["prefixes"]
        ):
            self.prefixes_list.addItem(
                prefix
            )

        for suffix in sorted(
            self.rules["suffixes"]
        ):
            self.suffixes_list.addItem(
                suffix
            )

        for token in sorted(
            self.rules["side_tokens"]
        ):
            self.sideTokens_list.addItem(
                token
            )

    def build_ui(self):

        layout = QtWidgets.QVBoxLayout(
            self
        )

        self.analyze_btn = (
            QtWidgets.QPushButton(
                "Analyze Selection"
            )
        )

        layout.addWidget(
            self.analyze_btn
        )

        #TOP - SUMMARY
        self.summary_widget = QtWidgets.QWidget()

        summary_layout = QtWidgets.QHBoxLayout(self.summary_widget)

        summary_layout.setContentsMargins(0, 0, 0, 0)
        self.summary_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Fixed
        )

        self.error_count_lbl = QtWidgets.QLabel("Errors: 0")
        QtColoring.apply_severity_color(self.error_count_lbl,"error")

        self.warning_count_lbl = QtWidgets.QLabel("Warnings: 0")
        QtColoring.apply_severity_color(self.warning_count_lbl,"warning")

        self.mindme_count_lbl = QtWidgets.QLabel("MindMe: 0")
        QtColoring.apply_severity_color(self.mindme_count_lbl,"mind_me")

        self.total_count_lbl = QtWidgets.QLabel("Total: 0")
        QtColoring.apply_severity_color(self.total_count_lbl)

        summary_layout.addWidget(self.error_count_lbl)

        summary_layout.addWidget(self.warning_count_lbl)
        summary_layout.addWidget(self.mindme_count_lbl)
        summary_layout.addStretch()

        summary_layout.addWidget(self.total_count_lbl)

        layout.addWidget(self.summary_widget)

        self.splitter = QtWidgets.QSplitter()

        layout.addWidget(
            self.splitter
        )

        # -------------------------
        # LEFT PANEL - FILTERS
        # -------------------------

        self.filters_widget = QtWidgets.QWidget()

        filters_layout = QtWidgets.QVBoxLayout(self.filters_widget)

        filters_layout.addWidget(
            QtWidgets.QLabel(
                "Severity"
            )
        )

        self.error_cb = QtWidgets.QCheckBox("Error")

        self.warning_cb = QtWidgets.QCheckBox("Warning")

        self.mindme_cb = QtWidgets.QCheckBox("MindMe")

        self.error_cb.setChecked(True)
        self.warning_cb.setChecked(True)
        self.mindme_cb.setChecked(True)

        filters_layout.addWidget(
            self.error_cb
        )

        filters_layout.addWidget(
            self.warning_cb
        )

        filters_layout.addWidget(
            self.mindme_cb
        )

        filters_layout.addSpacing(20)

        filters_layout.addWidget(
            QtWidgets.QLabel(
                "Categories"
            )
        )

        self.category_list = QtWidgets.QListWidget()

        for category, data in sorted(
            self.naming_categories.items()
        ):

            item = QtWidgets.QListWidgetItem(
                data["label"]
            )

            item.setData(
                QtCore.Qt.UserRole,
                category
            )

            item.setFlags(
                item.flags()
                | QtCore.Qt.ItemIsUserCheckable
            )

            item.setCheckState(
                QtCore.Qt.Checked
                if data.get(
                    "enabled",
                    True
                )
                else QtCore.Qt.Unchecked
            )

            self.category_list.addItem(
                item
            )

        filters_layout.addWidget(
            self.category_list
        )

        filters_layout.addStretch()

        # -------------------------
        # CENTER PANEL - OUTLINER
        # -------------------------

        center_widget = QtWidgets.QWidget()

        center_layout = QtWidgets.QVBoxLayout(
            center_widget
        )
        self.search_line = QtWidgets.QLineEdit()

        self.search_line.setPlaceholderText(
            "Filter nodes..."
        )

        center_layout.addWidget(
            self.search_line
        )

        self.results_tree = (
            QtWidgets.QTreeWidget()
        )

        self.results_tree.setHeaderLabels(
            [
                "Node / Issue",
                "Severity",
                "Suggestion"
            ]
        )

        self.results_tree.setAlternatingRowColors(True)

        self.results_tree.setUniformRowHeights(True)

        
        center_layout.addWidget(
            self.results_tree
        )

        # -------------------------
        # RIGHT PANEL - RULES
        # -------------------------

        self.rules_widget = QtWidgets.QWidget()

        rules_layout = QtWidgets.QVBoxLayout(
            self.rules_widget
        )

        rules_layout.addWidget(
            QtWidgets.QLabel(
                "Valid Prefixes"
            )
        )
        self.restore_rules_btn = QtWidgets.QPushButton(
            "Restore Defaults"
        )
        rules_layout.addWidget(
            self.restore_rules_btn
        )
        self.prefixes_list = (
            QtWidgets.QListWidget()
        )

        rules_layout.addWidget(
            self.prefixes_list
        )

        #Prefix buttons Creation
        self.add_prefix_btn = QtWidgets.QPushButton(
            "+"
        )

        self.remove_prefix_btn = QtWidgets.QPushButton(
            "-"
        )
        #Prefix buttons Setting and placing.
        prefix_btn_layout = QtWidgets.QHBoxLayout()

        prefix_btn_layout.addWidget(
            self.add_prefix_btn
        )

        prefix_btn_layout.addWidget(
            self.remove_prefix_btn
        )

        rules_layout.addLayout(
            prefix_btn_layout
        )
        #Suffixes
        rules_layout.addWidget(
            QtWidgets.QLabel(
                "Valid Suffixes"
            )
        )

        self.suffixes_list = (
            QtWidgets.QListWidget()
        )

        rules_layout.addWidget(
            self.suffixes_list
        )
        #Suffix buttons Creation
        self.add_suffix_btn = QtWidgets.QPushButton(
            "+"
        )
        self.remove_suffix_btn = QtWidgets.QPushButton(
            "-"
        )
        #Suffix buttons Setting and placing.
        suffix_btn_layout = QtWidgets.QHBoxLayout()
        suffix_btn_layout.addWidget(
            self.add_suffix_btn
        )
        suffix_btn_layout.addWidget(
            self.remove_suffix_btn
        )

        rules_layout.addLayout(
            suffix_btn_layout
        )

        #Side Tokens
        rules_layout.addWidget(
            QtWidgets.QLabel(
                "Valid Side Tokens"
            )
        )

        self.sideTokens_list = (
            QtWidgets.QListWidget()
        )

        rules_layout.addWidget(
            self.sideTokens_list
        )
        #SideTokens buttons Creation
        self.add_sideToken_btn = QtWidgets.QPushButton(
            "+"
        )
        self.remove_sideToken_btn = QtWidgets.QPushButton(
            "-"
        )
        #SideToken buttons Setting and placing.
        sideToken_btn_layout = QtWidgets.QHBoxLayout()
        sideToken_btn_layout.addWidget(
            self.add_sideToken_btn
        )
        sideToken_btn_layout.addWidget(
            self.remove_sideToken_btn
        )

        rules_layout.addLayout(
            sideToken_btn_layout
        )

        # -------------------------
        # POPULATE RULES
        # -------------------------

        for prefix in sorted(
            self.known_prefixes
        ):
            self.prefixes_list.addItem(
                prefix
            )

        for suffix in sorted(
            self.known_suffixes
        ):
            self.suffixes_list.addItem(
                suffix
            )

        for sideToken in sorted(
            self.side_tokens
        ):
            self.sideTokens_list.addItem(
                sideToken
            )

        # -------------------------
        # splitter
        # -------------------------

        self.splitter.addWidget(
            self.filters_widget
        )

        self.splitter.addWidget(
            center_widget
        )

        self.splitter.addWidget(
            self.rules_widget
        )

        self.splitter.setSizes(
            [
                250,   # filters
                700,   # outliner
                200    # rules
            ]
        )
        self.splitter.setCollapsible(
            0,
            True
        )

        self.splitter.setCollapsible(
            2,
            True
        )

        self.splitter.setCollapsible(
            1,
            False
        )

        splitter_state = self.settings.value(
            "validationSplitterState"
        )

        if splitter_state:

            self.splitter.restoreState(
                splitter_state
            )

    def select_node_from_item(self, item):

        node_name = item.data(
            0,
            QtCore.Qt.UserRole
        )

        if not node_name:
            return

        if "*" in node_name:
            return

        mayUtil.frame_object_onName(node_name)


    def create_connections(self):

        self.analyze_btn.clicked.connect(
            self.analyze_selection
        )

        self.results_tree.itemDoubleClicked.connect(
            self.select_node_from_item
        )

        self.error_cb.stateChanged.connect(
            self.analyze_selection
        )

        self.warning_cb.stateChanged.connect(
            self.analyze_selection
        )

        self.mindme_cb.stateChanged.connect(
            self.analyze_selection
        )

        self.category_list.itemChanged.connect(
            self.analyze_selection
        )

        self.search_line.textChanged.connect(
            self.analyze_selection
        )
        self.restore_rules_btn.clicked.connect(
            self.restore_default_rules
        )
        self.add_prefix_btn.clicked.connect(
            lambda:
            self.add_list_item(
                self.prefixes_list
            )
        )

        self.remove_prefix_btn.clicked.connect(
            lambda:
            self.remove_list_item(
                self.prefixes_list
            )
        )

        self.add_suffix_btn.clicked.connect(
            lambda:
            self.add_list_item(
                self.suffixes_list
            )
        )

        self.remove_suffix_btn.clicked.connect(
            lambda:
            self.remove_list_item(
                self.suffixes_list
            )
        )

        self.add_sideToken_btn.clicked.connect(
            lambda:
            self.add_list_item(
                self.sideTokens_list
            )
        )

        self.remove_sideToken_btn.clicked.connect(
            lambda:
            self.remove_list_item(
                self.sideTokens_list
            )
        )

    def analyze_selection(self):

        self.results_tree.clear()

        report = validation.analyze_selection()
        self.update_summary(
            report["issues"]
        )

        allowed_severities = (
            self.get_allowed_severities()
        )

        allowed_categories = (
            self.get_allowed_categories()
        )

        search_text = (
            self.search_line.text()
            .strip()
            .lower()
        )

        nodes = defaultdict(list)

        for issue in report["issues"]:

            if (
                issue["severity"]
                not in allowed_severities
            ):
                continue

            if (
                issue["category"]
                not in allowed_categories
            ):
                continue

            node = (
                issue.get("node")
                or issue["value"]
            )

            if search_text:

                searchable = (
                    str(node).lower()
                )

                if search_text not in searchable:
                    continue

            nodes[node].append(
                issue
            )

        sorted_nodes = sorted(
            nodes.items(),
            key=lambda item: min(
                severityTypes.SEVERITY_TYPES[
                    issue["severity"]
                ]["priority"]
                for issue in item[1]
            )
        )

        for node_name, issues in sorted_nodes:

            highest_priority = min(
                severityTypes.SEVERITY_TYPES[
                    issue["severity"]
                ]["priority"]
                for issue in issues
            )

            highest_severity = next(
                severity
                for severity, data in
                severityTypes.SEVERITY_TYPES.items()
                if data["priority"]
                == highest_priority
            )

            node_color = (
                QtColoring.get_severity_color(
                    highest_severity
                )
            )

            node_item = (
                QtWidgets.QTreeWidgetItem(
                    [
                        node_name,
                        f"{len(issues)} issue(s)",
                        ""
                    ]
                )
            )

            node_item.setData(
                0,
                QtCore.Qt.UserRole,
                node_name
            )

            node_item.setForeground(
                0,
                QtGui.QBrush(node_color)
            )

            node_item.setForeground(
                1,
                QtGui.QBrush(node_color)
            )

            self.results_tree.addTopLevelItem(
                node_item
            )

            sorted_issues = sorted(
                issues,
                key=lambda issue:
                severityTypes.SEVERITY_TYPES[
                    issue["severity"]
                ]["priority"]
            )

            for issue in sorted_issues:

                issue_color = (
                    QtColoring.get_severity_color(
                        issue["severity"]
                    )
                )

                issue_item = (
                    QtWidgets.QTreeWidgetItem(
                        [
                            (
                                f"[{issue['category']}] "
                                f"{issue['message']}"
                            ),
                            issue["severity"],
                            issue["suggestion"]
                        ]
                    )
                )

                issue_item.setData(
                    0,
                    QtCore.Qt.UserRole,
                    node_name
                )

                issue_item.setForeground(
                    0,
                    QtGui.QBrush(
                        issue_color
                    )
                )

                issue_item.setForeground(
                    1,
                    QtGui.QBrush(
                        issue_color
                    )
                )

                node_item.addChild(
                    issue_item
                )

            if highest_severity in (
                "error",
                "fatal"
            ):
                node_item.setExpanded(
                    True
                )