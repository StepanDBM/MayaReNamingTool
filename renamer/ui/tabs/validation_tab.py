from importlib import reload
import copy
from utils.qt import (
    QtWidgets,
    QtCore,
    QtGui
)
from collections import defaultdict

from operations import validation, issue_solvers
from ui.style import QtColoring
from config import severityTypes
from utils import maya_utils as mayUtil
import maya.cmds as cmds
from utils.loaders import loadNamingRules as N_Rules
reload(validation)
reload(QtColoring)
reload(severityTypes)
reload(N_Rules)


class ValidationTab(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.rules = N_Rules.load_rules()

        self.known_prefixes = set(self.rules["prefixes"])
        self.side_tokens = set(self.rules["side_tokens"])
        self.known_suffixes = set(self.rules["suffixes"])
        self.known_types = (self.rules["types"])
        self.naming_categories = (self.rules["categories"])

        self.settings = QtCore.QSettings("StyopaDBM", "reNamePro")
        self.last_report = None
        
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

    def get_selected_validation_candidates(self):
        selection = cmds.ls(
            selection=True,
            long=True
        ) or []

        candidates = []
        for node in selection:
            short_name = mayUtil.get_short_name(node)
            candidates.append(short_name)
            if hasattr(mayUtil,
                "get_short_name_without_namespace"
            ):

                clean_name = (
                    mayUtil.get_short_name_without_namespace(
                        node
                    )
                )

                candidates.append(clean_name)

            if cmds.objectType(node, isAType="shape"):

                parents = cmds.listRelatives(
                    node,
                    parent=True,
                    fullPath=True
                ) or []

                for parent in parents:

                    parent_short = mayUtil.get_short_name(parent)

                    candidates.append(parent_short)

                    if hasattr(mayUtil, "get_short_name_without_namespace"):

                        parent_clean = (
                            mayUtil.get_short_name_without_namespace(
                                parent
                            )
                        )

                        candidates.append(parent_clean)

        return list(
            dict.fromkeys(candidates)
        )

    def find_tree_item_for_names(self, names):

        name_set = set(
            str(name)
            for name in names
            if name
        )

        for index in range(self.results_tree.topLevelItemCount()):
            top_item = self.results_tree.topLevelItem(index)
            top_node = top_item.data(0, QtCore.Qt.UserRole)

            if top_node in name_set:
                return top_item

            for child_index in range(top_item.childCount()):
                child_item = top_item.child(child_index)

                child_node = child_item.data(0, QtCore.Qt.UserRole)
                if child_node in name_set:
                    return child_item

        return None

    def focus_selected_node_issue(self):
        if self.last_report is None:
            cmds.warning(
                "No validation report available. "
                "Run Analyze Selection first."
            )
            return
        candidates = (self.get_selected_validation_candidates())

        if not candidates:
            cmds.warning("No Maya object selected.")
            return

        matched_item = self.find_tree_item_for_names(candidates)
        if not matched_item:
            cmds.warning("Selected object has no visible validation issue.")

            return
        parent = matched_item.parent()
        if parent:
            parent.setExpanded(True)
        matched_item.setExpanded(True)

        self.results_tree.clearSelection()
        matched_item.setSelected(True)

        self.results_tree.setCurrentItem(matched_item)

        self.results_tree.scrollToItem(matched_item,
            QtWidgets.QAbstractItemView.PositionAtCenter
        )

        self.results_tree.setFocus()
    def show_issue_context_menu(self, position):

        item = self.results_tree.itemAt(position)

        if not item:
            return

        node_name = item.data(0, QtCore.Qt.UserRole)
        issue = item.data(0, QtCore.Qt.UserRole + 1)
        menu = QtWidgets.QMenu(self)
        select_action = menu.addAction("Select / Frame Node")
        if issue and issue_solvers.can_solve(issue):
            solve_action = menu.addAction("Solve This Issue")
            solve_all_label = "Solve All Similar Visible Issues"

            if issue.get("message") == "Possible typo":

                solve_all_label = (
                    f"Solve All "
                    f"{issue.get('category')} typos "
                    f"to '{issue.get('suggestion')}'"
                )

            solve_all_action = menu.addAction(solve_all_label)

        else:
            disabled_action = menu.addAction("No Solver Available")
            disabled_action.setEnabled(False)

        if hasattr(menu, "exec_"):
            action = menu.exec_(
                self.results_tree.viewport().mapToGlobal(
                    position
                )
            )
        else:
            action = menu.exec(
                self.results_tree.viewport().mapToGlobal(
                    position
                )
            )

        if action == select_action:
            self.select_node_from_item(item)
            return

        if issue and action == solve_action:
            self.solve_issue(issue)
            return

        if issue and action == solve_all_action:
            self.solve_all_similar_visible_issues(issue)
    def solve_issue(self, issue):

        solved_nodes = issue_solvers.solve_issue(issue)

        if not solved_nodes:
            return

        self.analyze_selection()
    
    def get_visible_issues(self):
        issues = []
        for top_index in range(self.results_tree.topLevelItemCount()):
            top_item = self.results_tree.topLevelItem(top_index)

            for child_index in range(top_item.childCount()):
                child_item = top_item.child(child_index)
                issue = child_item.data(0, QtCore.Qt.UserRole + 1)

                if issue:
                    issues.append(issue)

        return issues

    def is_same_solve_family(self, issue, reference_issue):

        if not issue or not reference_issue:
            return False

        if issue.get("solver") != reference_issue.get("solver"):
            return False

        if issue.get("category") != reference_issue.get("category"):
            return False

        if issue.get("message") != reference_issue.get("message"):
            return False

        if issue.get("message") == "Possible typo":

            return (
                issue.get("suggestion")
                == reference_issue.get("suggestion")
            )

        return True
    def solve_all_similar_visible_issues(self, reference_issue):

        if self.last_report is None:
            return

        visible_issues = self.get_visible_issues()

        matching_issues = [
            issue
            for issue in visible_issues
            if self.is_same_solve_family(
                issue,
                reference_issue
            )
        ]

        solved_any = False

        for issue in matching_issues:

            result = issue_solvers.solve_issue(issue)

            if result:
                solved_any = True

        if solved_any:
            self.analyze_selection()

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
        
        self.rules["categories"] = {}
        for index in range(self.category_list.count()):
            item = self.category_list.item(index)
            category = item.data(QtCore.Qt.UserRole)
            label = item.text()
            enabled = (
                item.checkState()
                == QtCore.Qt.Checked
            )
            self.rules["categories"][category] = {
                "label": label,
                "enabled": enabled
            }

        N_Rules.save_rules(self.rules)

        self.known_prefixes = set(self.rules["prefixes"])
        self.known_suffixes = set(self.rules["suffixes"])
        self.side_tokens = set(self.rules["side_tokens"])

    def populate_category_list(self):
        self.category_list.blockSignals(True)
        self.category_list.clear()

        for category, data in sorted(self.naming_categories.items()):
            item = QtWidgets.QListWidgetItem(data["label"])
            item.setData(QtCore.Qt.UserRole, category)

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
            self.category_list.addItem(item)
        self.category_list.blockSignals(False)
    
    def on_category_changed(self):
        for index in range(
            self.category_list.count()
        ):
            item = self.category_list.item(index)
            category = item.data(QtCore.Qt.UserRole)

            if category not in self.rules["categories"]:
                continue
            self.rules["categories"][category]["enabled"] = (
                item.checkState()
                == QtCore.Qt.Checked
            )

        self.save_rules()
        if self.last_report is None:
            return
        self.analyze_selection()

    def restore_default_categories(self):

        self.rules["categories"] = copy.deepcopy(
            N_Rules.DEFAULT_RULES["categories"]
        )

        self.naming_categories = (
            self.rules["categories"]
        )

        self.populate_category_list()
        self.save_rules()
        if self.last_report is None:
            return
        self.analyze_selection()

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
            self.prefixes_list.addItem(prefix)

        for suffix in sorted(
            self.rules["suffixes"]
        ):
            self.suffixes_list.addItem(suffix)

        for token in sorted(
            self.rules["side_tokens"]
        ):
            self.sideTokens_list.addItem(token)

    def build_ui(self):

        layout = QtWidgets.QVBoxLayout(self)

        # -------------------------
        # TOP ACTIONS
        # -------------------------

        actions_layout = QtWidgets.QHBoxLayout()
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(4)

        self.analyze_btn = QtWidgets.QPushButton("Analyze Selection")
        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.clear_btn.setMaximumWidth(120)
        actions_layout.addWidget(self.analyze_btn)
        actions_layout.addWidget(self.clear_btn)

        layout.addLayout(actions_layout)

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

        filters_layout.addWidget(self.error_cb)

        filters_layout.addWidget(self.warning_cb)

        filters_layout.addWidget(self.mindme_cb)

        filters_layout.addSpacing(20)

        filters_layout.addWidget(
            QtWidgets.QLabel(
                "Categories"
            )
        )

        self.category_list = QtWidgets.QListWidget()
        self.populate_category_list()

        filters_layout.addWidget(
            self.category_list
        )
        self.restore_categories_btn = QtWidgets.QPushButton("Restore Categories")
        filters_layout.addWidget(self.restore_categories_btn)

        filters_layout.addStretch()

        # -------------------------
        # CENTER PANEL - OUTLINER
        # -------------------------

        center_widget = QtWidgets.QWidget()

        center_layout = QtWidgets.QVBoxLayout(center_widget)
        self.search_line = QtWidgets.QLineEdit()

        self.search_line.setPlaceholderText("Filter nodes...")

        center_layout.addWidget(self.search_line)

        self.results_tree = (QtWidgets.QTreeWidget())

        self.results_tree.setHeaderLabels(
            [
                "Node / Issue",
                "Severity",
                "Suggestion"
            ]
        )

        self.results_tree.setAlternatingRowColors(True)
        self.results_tree.setUniformRowHeights(True)
        self.results_tree.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        #To add any NEW functionality or override them. This si for the Right click.
        self.results_tree.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu
        )

        shortcut_class = (getattr(
                QtWidgets,
                "QShortcut",
                None
            )
            or QtGui.QShortcut
        )

        self.focus_selection_shortcut = shortcut_class(
            QtGui.QKeySequence("F"), self
        )
        
        center_layout.addWidget(self.results_tree)

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

        mayUtil.frame_object_on_name(node_name)


    def create_connections(self):
        #On F pressed focus for the validation list.
        self.focus_selection_shortcut.activated.connect(
            self.focus_selected_node_issue
        )
        #On RightClick will be using this context menu as it overrides the resutls from the operation.
        self.results_tree.customContextMenuRequested.connect(
            self.show_issue_context_menu
        )
        self.analyze_btn.clicked.connect(
            self.analyze_selection
        )
        self.clear_btn.clicked.connect(
            self.clear_results
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
            self.on_category_changed
        )
        self.restore_categories_btn.clicked.connect(
            self.restore_default_categories
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
    def clear_results(self):

        self.results_tree.clear()
        self.last_report = None
        self.update_summary(
            []
        )
    def analyze_selection(self):

        self.results_tree.clear()

        report = validation.analyze_selection()
        self.last_report = report
        #print(report)
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

            self.results_tree.addTopLevelItem(node_item)

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

                issue_item.setData(
                    0,
                    QtCore.Qt.UserRole + 1,
                    issue
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