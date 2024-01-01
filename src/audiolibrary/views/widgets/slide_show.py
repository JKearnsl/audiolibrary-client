from typing import Literal

from PyQt6.QtCore import QSize, QPropertyAnimation, QEasingCurve, QVariantAnimation, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSizePolicy,
    QStackedWidget,
    QToolButton,
    QLabel, QGraphicsDropShadowEffect
)

from audiolibrary.utils.icon import svg_ico

SlideType = Literal["left", "center", "right"]


class BiDirectionalCycle:
    def __init__(self, iterable):
        self.iterable = list(iterable)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index >= len(self.iterable):
            self.index = 0
        return self.iterable[self.index]

    def prev(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.iterable) - 1
        return self.iterable[self.index]


class ColorSwitcherAnimation(QVariantAnimation):
    def __init__(self, widget: QToolButton, start_color, end_color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget
        self.setStartValue(QColor(start_color))
        self.setEndValue(QColor(end_color))

    def updateCurrentValue(self, color):
        self.widget.setStyleSheet("""
            QToolButton {
                background-color: $COLOR;
                border-radius: 0px;
            }
        """.replace(
            "$COLOR", color.name()
        ))


class Slide(QWidget):
    def __init__(
            self,
            image_path: str,
            title: str,
            description: str,
            button,
            _type: SlideType,
            parent=None
    ):
        super().__init__(parent)
        self.image_path = image_path
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)
        layout = QHBoxLayout(self)

        slide_content = QWidget()
        layout.addWidget(slide_content)
        slide_content.setObjectName("slide_content")
        slide_content.setStyleSheet("""
            QWidget#slide_content {
                background-color: transparent;
            }
        """)
        slide_content_layout = QVBoxLayout(slide_content)
        slide_content_layout.setContentsMargins(0, 0, 0, 0)
        slide_content_layout.setSpacing(30)
        slide_content_layout.addStretch(1)

        slide_content_header = QLabel()
        slide_content_header.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
            }
        """)
        slide_content_header.setText(title)
        slide_content_layout.addWidget(slide_content_header)

        slide_content_description = QLabel()
        slide_content_description.setObjectName("slide_content_description")
        slide_content_description.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: normal;
                color: white;
            }
        """)
        slide_content_description.setWordWrap(True)
        slide_content_description.setText(description)
        slide_content_layout.addWidget(slide_content_description)
        slide_content_layout.addWidget(button)
        slide_content_layout.addStretch(1)

        if _type == "left":
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            slide_content_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
            slide_content_description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        elif _type == "center":
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            slide_content_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            slide_content_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        elif _type == "right":
            layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            slide_content_header.setAlignment(Qt.AlignmentFlag.AlignRight)
            slide_content_description.setAlignment(Qt.AlignmentFlag.AlignRight)


class SlideShow(QWidget):

    def __init__(
            self,
            background_color,
            parent=None
    ):
        super().__init__(parent)
        self._slides: list = []
        self._slide_inf_iterator = BiDirectionalCycle(self._slides)
        self.slide_type_generator = BiDirectionalCycle(["left", "center", "right"])

        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=10, xOffset=0, yOffset=0))

        self.setMinimumHeight(250)

        widget_layout = QHBoxLayout(self)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(0)

        canvas = QWidget()
        widget_layout.addWidget(canvas)
        canvas.setObjectName("canvas")
        canvas.setStyleSheet("""
            QWidget#canvas {
                background-color: $BG;
                border-radius: 10px;
            }
        """.replace(
            "$BG", background_color
        ))
        self._canvas = canvas

        canvas_layout = QHBoxLayout()
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.setSpacing(0)
        canvas.setLayout(canvas_layout)

        # Sheet
        sheet = QWidget()
        canvas_layout.addWidget(sheet)
        sheet.setObjectName("sheet")
        sheet.setStyleSheet("""
            QWidget#sheet {
                background-color: rgba(0, 0, 0, 0.5);
                border-radius: 10px;
            }
        """)

        slide_show_layout = QHBoxLayout()
        slide_show_layout.setContentsMargins(0, 0, 0, 0)
        slide_show_layout.setSpacing(0)
        sheet.setLayout(slide_show_layout)

        # Left switcher
        left_switcher = QToolButton()
        left_switcher.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        left_switcher.setStyleSheet("""
            QToolButton {
                border-radius: 5px;
                background-color: transparent;
            }
            QToolButton:pressed {
                background-color: transparent;
            }
        """)
        left_switcher.setFixedWidth(50)
        left_switcher.setIconSize(QSize(30, 30))
        left_switcher.setIcon(svg_ico("icons:left-arrow.svg", "white", "stroke"))
        left_switcher.clicked.connect(self.prev_slide)
        slide_show_layout.addWidget(left_switcher)

        # Central
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 10, 0, 10)
        central_layout.setSpacing(20)
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

        # SwitchButtons
        switch_buttons = QHBoxLayout()
        switch_buttons.setContentsMargins(0, 0, 0, 0)
        switch_buttons.setSpacing(10)
        switch_buttons.addStretch(1)
        central_layout.addLayout(switch_buttons)

        # SwitchButtons: left
        left_button = QToolButton()
        left_button.setStyleSheet("""
            QToolButton {
                background-color: white;
                border-radius: 0px;
            }
        """)
        left_button.setFixedSize(15, 5)
        left_button.clicked.connect(self.prev_slide)
        self._left_button = left_button
        switch_buttons.addWidget(left_button)

        # SwitchButtons: center
        center_button = QToolButton()
        center_button.setStyleSheet("""
            QToolButton {
                background-color: gray;
                border-radius: 0px;
            }
        """)
        center_button.setFixedSize(15, 5)
        self._center_button = center_button
        switch_buttons.addWidget(center_button)

        # SwitchButtons: right
        right_button = QToolButton()
        right_button.setStyleSheet("""
            QToolButton {
                background-color: white;
                border-radius: 0px;
            }
        """)
        right_button.setFixedSize(15, 5)
        right_button.clicked.connect(self.next_slide)
        self._right_button = right_button
        switch_buttons.addWidget(right_button)
        switch_buttons.addStretch(1)

        # Right switcher
        right_switcher = QToolButton()
        right_switcher.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        right_switcher.setStyleSheet("""
           QToolButton {
               border-radius: 5px;
               background-color: transparent;
           }
           QToolButton:pressed {
               background-color: transparent;
           }
       """)
        right_switcher.setFixedWidth(50)
        right_switcher.setIconSize(QSize(30, 30))
        right_switcher.setIcon(svg_ico("icons:right-arrow.svg", "white", "stroke"))
        right_switcher.clicked.connect(self.next_slide)
        slide_show_layout.addWidget(right_switcher)

        self._animations_buffer = []

    def add_slide(self, image_path: str, title: str, description: str, button, _type: SlideType = None) -> None:
        if _type is None:
            _type = next(self.slide_type_generator)

        self._slides.append(Slide(image_path, title, description, button, _type))
        self._content_widget.addWidget(self._slides[-1])
        self._slide_inf_iterator = BiDirectionalCycle(self._slides)
        self.next_slide()

    def _set_current_image(self, image_path: str) -> None:
        self._canvas.setStyleSheet("""
            QWidget#canvas {
                border-radius: 10px;
                background: url($IMAGE_PATH) center no-repeat;
            }
        """.replace(
            "$IMAGE_PATH", image_path
        ))

    def next_slide(self) -> None:
        if self._animations_buffer or not self._slides:
            return

        self.make_switch_animation("right")

        # Переключение слайдов
        widget = next(self._slide_inf_iterator)
        self._content_widget.setCurrentWidget(widget)
        self._set_current_image(widget.image_path)

    def prev_slide(self) -> None:
        if self._animations_buffer or not self._slides:
            return

        self.make_switch_animation("left")

        # Переключение слайдов
        widget = self._slide_inf_iterator.prev()
        self._content_widget.setCurrentWidget(widget)
        self._set_current_image(widget.image_path)

    def make_switch_animation(self, _type: Literal["left", "right"]):
        center_animation1 = ColorSwitcherAnimation(self._center_button, "gray", "white")
        center_animation2 = ColorSwitcherAnimation(self._center_button, "white", "gray")

        if _type == "left":
            arrow_animation1 = ColorSwitcherAnimation(self._left_button, "white", "gray")
            arrow_animation2 = ColorSwitcherAnimation(self._left_button, "gray", "white")
        elif _type == "right":
            arrow_animation1 = ColorSwitcherAnimation(self._right_button, "white", "gray")
            arrow_animation2 = ColorSwitcherAnimation(self._right_button, "gray", "white")
        else:
            raise ValueError("Invalid _type value")

        # Установка свойств анимаций
        center_animation1.setDuration(1000)
        center_animation1.setEasingCurve(QEasingCurve.Type.InOutQuad)

        center_animation2.setDuration(1000)
        center_animation2.setEasingCurve(QEasingCurve.Type.InOutQuad)

        arrow_animation1.setDuration(1000)
        arrow_animation1.setEasingCurve(QEasingCurve.Type.InOutQuad)

        arrow_animation2.setDuration(1000)
        arrow_animation2.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Добавление анимаций в буфер
        self._animations_buffer.append(center_animation1)
        self._animations_buffer.append(center_animation2)
        self._animations_buffer.append(arrow_animation1)
        self._animations_buffer.append(arrow_animation2)

        # Подключение сигнала `finished` анимаций к методу `start` для создания циклической анимации
        center_animation1.finished.connect(center_animation2.start)
        center_animation2.finished.connect(center_animation1.start)
        arrow_animation1.finished.connect(arrow_animation2.start)
        arrow_animation2.finished.connect(self._animations_buffer.clear)

        # Запуск анимаций
        center_animation1.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        arrow_animation1.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def heightForWidth(self, width):
        return width * 0.5
