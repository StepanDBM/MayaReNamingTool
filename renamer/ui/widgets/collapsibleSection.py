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

        layout.setSpacing(0)

        # -------------------------
        # Header
        # -------------------------

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

        # -------------------------
        # Animated Wrapper
        # -------------------------

        self.content_area = QtWidgets.QWidget()

        area_layout = QtWidgets.QVBoxLayout(
            self.content_area
        )

        area_layout.setContentsMargins(
            0, 0, 0, 0
        )

        area_layout.setSpacing(0)

        self.content_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred
        )

        area_layout.addWidget(
            self.content_widget
        )

        layout.addWidget(
            self.content_area
        )

        self.expanded_height = (
            self.content_area.sizeHint().height()
        )

        # -------------------------
        # Animation
        # -------------------------

        self.animation = QtCore.QPropertyAnimation(
            self.content_area,
            b"maximumHeight"
        )

        self.animation.setDuration(
            150
        )

        self.animation.setEasingCurve(
            QtCore.QEasingCurve.OutCubic
        )

        self.animation.finished.connect(
            self._on_animation_finished
        )

        # -------------------------
        # Initial State
        # -------------------------

        if expanded:

            self.content_area.show()

            self.content_area.setMaximumHeight(
                self.expanded_height
            )

        else:

            self.content_area.setMaximumHeight(
                0
            )

            self.content_area.hide()

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

        return self.toggle_btn.isChecked()

    def _on_animation_finished(self):

        if not self.toggle_btn.isChecked():

            self.content_area.hide()

    def toggle(self):

        expanded = (
            self.toggle_btn.isChecked()
        )
        print(
            self.title,
            "cached:",
            self.expanded_height
        )

        print(
            self.title,
            "actual:",
            self.content_area.sizeHint().height()
        )

        self.update_header()

        self.animation.stop()

        if expanded:

            self.content_area.show()

            self.animation.setStartValue(
                self.content_area.maximumHeight()
            )

            target_height = (
                self.content_area.layout().sizeHint().height()
            )

            self.animation.setEndValue(
                target_height
            )

        else:

            self.animation.setStartValue(
                self.content_area.maximumHeight()
            )

            target_height = (
                self.content_area.layout().sizeHint().height()
            )

            self.animation.setEndValue(
                target_height
            )

        self.animation.start()