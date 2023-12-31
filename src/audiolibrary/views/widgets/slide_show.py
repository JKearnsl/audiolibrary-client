import itertools
from typing import Literal

from PyQt6.QtWidgets import QVBoxLayout, QLayout, QHBoxLayout, QWidget, QSizePolicy, QStackedWidget

SlideType = Literal["left", "center", "right"]


class Slide(QWidget):
    def __init__(
            self,
            image: str,
            title: str,
            description: str,
            button,
            _type: SlideType,
            parent=None
    ):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)
        self.layout = QHBoxLayout(self)


class SlideShow(QWidget):

    def __init__(
            self,
            background_color,
            parent=None
    ):
        super().__init__(parent)
        self.slide_type_generator = itertools.cycle(["left", "center", "right"])
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setMinimumHeight(250)
        self.setStyleSheet("""
            QWidget {
                background-color: $BG;
                border-radius: 10px;
            }
        """.replace(
            "$BG", background_color)
        )
        slide_show_layout = QHBoxLayout(self)
        slide_show_layout.setContentsMargins(0, 0, 0, 0)
        slide_show_layout.setSpacing(0)

        # Left switcher
        left_switcher = QWidget(self)
        left_switcher.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        left_switcher.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)
        left_switcher_layout = QVBoxLayout(left_switcher)
        left_switcher_layout.setContentsMargins(0, 0, 0, 0)
        left_switcher_layout.setSpacing(0)
        slide_show_layout.addWidget(left_switcher)

        # Central
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        slide_show_layout.addLayout(central_layout)

        # Content
        content_widget = QStackedWidget()
        content_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        content_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)
        self._content_widget = content_widget
        central_layout.addWidget(content_widget)
        central_layout.addStretch(1)

        # SwitchButtons
        switch_buttons = QHBoxLayout()
        switch_buttons.setContentsMargins(0, 0, 0, 0)
        switch_buttons.setSpacing(0)
        central_layout.addLayout(switch_buttons)

        # Right switcher
        right_switcher = QWidget(self)
        right_switcher.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        right_switcher.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)
        right_switcher_layout = QVBoxLayout(right_switcher)
        right_switcher_layout.setContentsMargins(0, 0, 0, 0)
        right_switcher_layout.setSpacing(0)
        slide_show_layout.addWidget(right_switcher)
        self._layout = slide_show_layout

    def add_slide(self, image: str, title: str, description: str, button):
        slide = Slide(image, title, description, button, next(self.slide_type_generator))
        self.layout().addWidget(slide)

    def next_slide(self) -> None:
        ...

    def prev_slide(self) -> None:
        ...

    def layout(self) -> QLayout | None:
        return self._layout

    def content_widget(self) -> QStackedWidget:
        return self._content_widget

    def heightForWidth(self, width):
        return width * 0.5
