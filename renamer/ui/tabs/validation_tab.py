from importlib import reload
from utils.qt import (
    QtWidgets,
    QtGui
)
from collections import defaultdict

from operations import validation
from ui.style import coloring
from config import severityTypes
reload(validation)
reload(coloring)
reload(severityTypes)


class ValidationTab(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.build_ui()
        self.create_connections()

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

        self.results_tree.setAlternatingRowColors(
            True
        )

        self.results_tree.setUniformRowHeights(
            True
        )

        self.results_tree.setColumnWidth(
            0,
            300
        )

        layout.addWidget(
            self.results_tree
        )

    def create_connections(self):

        self.analyze_btn.clicked.connect(
            self.analyze_selection
        )

    def analyze_selection(self):

        self.results_tree.clear()

        report = validation.analyze_selection()

        nodes = defaultdict(list)

        for issue in report["issues"]:

            node = (
                issue.get("node")
                or issue["value"]
            )

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
                for severity, data in (
                    severityTypes.SEVERITY_TYPES.items()
                )
                if data["priority"]
                == highest_priority
            )

            node_color = (
                coloring.get_severity_color(
                    highest_severity
                )
            )

            node_item = (
                QtWidgets.QTreeWidgetItem(
                    [
                        node_name,
                        (
                            f"{len(issues)} "
                            f"issue(s)"
                        ),
                        ""
                    ]
                )
            )

            node_item.setForeground(
                0,
                QtGui.QBrush(
                    node_color
                )
            )

            node_item.setForeground(
                1,
                QtGui.QBrush(
                    node_color
                )
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
                    coloring.get_severity_color(
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

        self.results_tree.expandAll()