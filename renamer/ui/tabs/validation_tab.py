from importlib import reload
from utils.qt import (
    QtWidgets,
    QtGui
)
from collections import defaultdict

from operations import validation
from ui.style import coloring
reload(validation)


class ValidationTab(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.build_ui()
        self.create_connections()

    def build_ui(self):

        layout = QtWidgets.QVBoxLayout(self)

        self.analyze_btn = QtWidgets.QPushButton(
            "Analyze Selection"
        )

        layout.addWidget(
            self.analyze_btn
        )

        self.results_tree = QtWidgets.QTreeWidget()

        self.results_tree.setHeaderLabels(
            ["Issue", "Value", "Suggestion"]
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

        categories = defaultdict(list)

        for issue in report["issues"]:

            categories[
                issue["category"]
            ].append(issue)

        for category, issues in sorted(
            categories.items()
        ):

            category_item = QtWidgets.QTreeWidgetItem(
                [
                    f"{category.title()} ({len(issues)})"
                ]
            )

            color = coloring.get_category_color(category)

            category_item.setForeground(
                0,
                QtGui.QBrush(color)
            )

            self.results_tree.addTopLevelItem(
                category_item
            )

            for issue in issues:

                issue_item = QtWidgets.QTreeWidgetItem(
                    [
                        issue["message"],
                        issue["value"],
                        issue["suggestion"]
                    ]
                )

                issue_item.setForeground(
                    0,
                    QtGui.QBrush(color)
                )

                category_item.addChild(
                    issue_item
                )

        self.results_tree.expandAll()