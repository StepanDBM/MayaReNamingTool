# ui/widgets/collapsible_section.py

from utils.qt import (
    QtWidgets,
    QtCore
)

from ui.style.QtColoring import (
    lighter_color
)


class CollapsibleSection(QtWidgets.QWidget):

    def __init__(
        self,
        title,
        content_widget,
        expanded=True,
        settings_key=None,
        parent=None
    ):
        super().__init__(parent)

        self.title = title
        self.content_widget = content_widget

        expanded_color = lighter_color(
            "#083844",
            130
        )

        layout = QtWidgets.QVBoxLayout(self)

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        layout.setSpacing(0)

        self.toggle_btn = QtWidgets.QPushButton()

        self.toggle_btn.setCheckable(True)

        self.toggle_btn.setChecked(
            expanded
        )

        self.toggle_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )

        self.toggle_btn.setFixedHeight(
            20
        )

        self.toggle_btn.setStyleSheet(
            f"""
            QPushButton
            {{
                background-color: #083844;
                border: 1px solid #144550;

                text-align: left;

                padding-left: 6px;

                font-weight: bold;
            }}

            QPushButton:hover
            {{
                background-color: #0c4b58;
            }}

            QPushButton:checked
            {{
                background-color: {expanded_color};
            }}
            """
        )

        self.toggle_btn.clicked.connect(
            self.toggle
        )

        self.update_header()

        layout.addWidget(
            self.toggle_btn
        )

        self.content_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred
        )

        layout.addWidget(
            self.content_widget
        )

        self.content_widget.setVisible(
            expanded
        )
        self.settings_key = settings_key

    def update_header(self):

        if self.toggle_btn.isChecked():

            self.toggle_btn.setText(
                f"{self.title}"
            )

        else:

            self.toggle_btn.setText(
                f"{self.title}"
            )

    def is_expanded(self):

        return self.toggle_btn.isChecked()
    
    def toggle(self):

        expanded = (
            self.toggle_btn.isChecked()
        )

        self.content_widget.setVisible(
            expanded
        )

        self.update_header()