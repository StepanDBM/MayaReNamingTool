from utils.qt import QtWidgets

from operations import validation


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

        prefixes_item = QtWidgets.QTreeWidgetItem(
            ["Prefixes"]
        )

        self.results_tree.addTopLevelItem(
            prefixes_item
        )

        for name, count in sorted(
            report["prefixes"].items()
        ):

            prefixes_item.addChild(
                QtWidgets.QTreeWidgetItem(
                    [name, str(count)]
                )
            )

        suffixes_item = QtWidgets.QTreeWidgetItem(
            ["Suffixes"]
        )

        self.results_tree.addTopLevelItem(
            suffixes_item
        )

        for name, count in sorted(
            report["suffixes"].items()
        ):

            suffixes_item.addChild(
                QtWidgets.QTreeWidgetItem(
                    [name, str(count)]
                )
            )

        warnings_item = QtWidgets.QTreeWidgetItem(
            ["Warnings"]
        )

        self.results_tree.addTopLevelItem(
            warnings_item
        )

        for warning in report["warnings"]:

            warnings_item.addChild(
                QtWidgets.QTreeWidgetItem(
                    [warning]
                )
            )

        self.results_tree.expandAll()