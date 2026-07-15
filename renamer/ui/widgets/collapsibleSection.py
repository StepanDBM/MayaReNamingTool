# ui/widgets/collapsible_section.py

from utils.qt import (
    QtWidgets
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
        self.settings_key = settings_key
        self.content_widget = content_widget

        expanded_color = lighter_color(
            "#083844",
            130
        )

        layout = QtWidgets.QVBoxLayout(self)

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        layout.setSpacing(
            0
        )

        # -------------------------
        # Header
        # -------------------------

        self.toggle_btn = QtWidgets.QPushButton()

        self.toggle_btn.setCheckable(
            True
        )

        self.toggle_btn.setChecked(
            expanded
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

        layout.addWidget(
            self.toggle_btn
        )

        # -------------------------
        # Content
        # -------------------------

        self.content_area = QtWidgets.QWidget()

        content_layout = QtWidgets.QVBoxLayout(
            self.content_area
        )

        content_layout.setContentsMargins(
            0, 0, 0, 0
        )

        content_layout.setSpacing(
            0
        )

        content_layout.addWidget(
            self.content_widget
        )

        layout.addWidget(
            self.content_area
        )

        self.update_header()

        self.content_area.setVisible(
            expanded
        )

    def update_header(self):

        if self.toggle_btn.isChecked():

            self.toggle_btn.setText(
                f"▼  {self.title}"
            )

        else:

            self.toggle_btn.setText(
                f"▶  {self.title}"
            )

    def is_expanded(self):

        return (
            self.toggle_btn.isChecked()
        )

    def toggle(self):

        expanded = (
            self.toggle_btn.isChecked()
        )

        self.content_area.setVisible(
            expanded
        )

        self.update_header()