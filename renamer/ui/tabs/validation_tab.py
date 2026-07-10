from importlib import reload
from utils.qt import QtWidgets

from operations import validation
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
            ["Validation Results", "Count"]
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

        issues_item = QtWidgets.QTreeWidgetItem(
            ["Issues"]
        )

        self.results_tree.addTopLevelItem(
            issues_item
        )
        
        for issue in report["issues"]:

            text = (
                f"[{issue['category']}] "
                f"{issue['message']} : "
                f"{issue['value']} -> "
                f"{issue['suggestion']}"
            )

            issues_item.addChild(
                QtWidgets.QTreeWidgetItem(
                    [
                        text,
                        issue["severity"]
                    ]
                )
            )

        self.results_tree.expandAll()