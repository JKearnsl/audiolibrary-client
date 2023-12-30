from typing import Callable

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

from audiolibrary.api_service import ErrorType
from audiolibrary.utils.observer import DObserver
from audiolibrary.utils.ts_meta import TSMeta
from audiolibrary.views.auth.static_ui import UiAuthWindow
from audiolibrary.views.widgets import WidgetsFactory


class AuthView(QtWidgets.QWidget, DObserver, metaclass=TSMeta):

    def __init__(self, controller, model, widgets_factory: WidgetsFactory, parent=None):
        super().__init__(parent)
        self.animation_buffer = []
        self.controller = controller
        self.model = model
        self.widgets_factory = widgets_factory

        self.ui = UiAuthWindow()
        self.ui.setup_ui(self, widgets_factory)
        self.is_signin = True

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.poster_button.mousePressEvent = lambda event: self.switch_auth_state(not self.is_signin)
        self.ui.signin_button.clicked.connect(self.signin_clicked)
        self.ui.signup_button.clicked.connect(self.signup_clicked)

    def model_changed(self):
        self.ui.response_label.clear()
        self.ui.response_label.hide()

    def model_loaded(self):
        self.signin_form()

    def error_handler(self, error):
        self.ui.response_label.show()
        if error.type is ErrorType.MESSAGE:
            self.ui.response_label.setText(error.content)
        else:
            self.ui.response_label.setText('\n'.join(
                [
                    f"{el.field}: {el.message}" for el in error.content
                ]
            ))

    def signin_clicked(self):
        login = self.ui.username_line_edit.text()
        password = self.ui.password_line_edit.text()
        self.controller.signin(login, password)

    def signup_clicked(self):
        login = self.ui.username_line_edit.text()
        password = self.ui.password_line_edit.text()
        repeat_password = self.ui.repeat_password_line_edit.text()
        self.controller.signup(login, password, repeat_password)

    def signin_form(self):
        self.ui.title_label.setText("Вход")
        self.ui.poster_button.setText("Регистрация")
        self.ui.poster_header.setText("Привет, друг!")
        self.ui.poster_text.setText(
            "Зарегистрируйтесь, указав свои данные, чтобы использовать все возможности приложения"
        )

        self.ui.password_line_edit.clear()
        self.ui.repeat_password_line_edit.clear()
        self.ui.signup_button.hide()
        self.ui.repeat_password_line_edit.hide()
        self.ui.signin_button.show()

        self.ui.poster_panel.setStyleSheet(
            self.ui.poster_panel.styleSheet() + """
                QFrame {
                    border-top-right-radius: 0px;
                    border-bottom-right-radius: 0px;
                    border-top-left-radius: 50px;
                    border-bottom-left-radius: 50px;
                }
            """
        )
        self.ui.poster_panel.setGraphicsEffect(
            QGraphicsDropShadowEffect(
                blurRadius=10,
                color=QtGui.QColor(0, 0, 0, 60),
                offset=QtCore.QPointF(-1, 0)
            )
        )

    def signup_form(self):
        self.ui.title_label.setText("Регистрация")
        self.ui.poster_button.setText("Вход")
        self.ui.poster_header.setText("Добро пожаловать!")
        self.ui.poster_text.setText(
            "Введите свои данные, чтобы использовать все возможности приложения"
        )

        self.ui.password_line_edit.clear()
        self.ui.repeat_password_line_edit.clear()
        self.ui.signin_button.hide()

        self.ui.repeat_password_line_edit.show()
        self.ui.signup_button.show()

        self.ui.poster_panel.setStyleSheet(
            self.ui.poster_panel.styleSheet() + """
                QFrame {
                    border-top-right-radius: 50px;
                    border-bottom-right-radius: 50px;
                    border-top-left-radius: 0px;
                    border-bottom-left-radius: 0px;
                }
            """
        )
        self.ui.poster_panel.setGraphicsEffect(
            QGraphicsDropShadowEffect(
                blurRadius=10,
                color=QtGui.QColor(0, 0, 0, 60),
                offset=QtCore.QPointF(1, 0)
            )
        )

    def switch_auth_state(self, is_signin):
        for anim in self.animation_buffer:
            if anim.state() == QPropertyAnimation.State.Running:
                return

        self.is_signin = is_signin

        self.animate_widgets_switch(
            duration=1000,
            exec_finished=lambda: self.signin_form() if is_signin else self.signup_form()
        )

    def animate_widgets_switch(self, duration: int, exec_finished: Callable = None):
        cover_widget = self.ui.poster_panel

        # Анимация для cover_widget
        animation_cover = QPropertyAnimation(cover_widget, b"geometry")
        animation_cover.setDuration(duration)
        animation_cover.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation_cover.setStartValue(cover_widget.geometry())

        if self.ui.horizontal_layout.itemAt(0).widget() == cover_widget:
            animation_cover.setEndValue(
                QtCore.QRect(
                    cover_widget.x(), cover_widget.y(), cover_widget.width() + 100, cover_widget.height()
                )
            )
        else:
            animation_cover.setEndValue(
                QtCore.QRect(
                    cover_widget.x() - 100, cover_widget.y(), cover_widget.width() + 100, cover_widget.height()
                )
            )

        self.animation_buffer.append(animation_cover)
        animation_cover.start()

        # Обработчик события `finished` для анимации
        animation_cover.finished.connect(self.switch_widgets)
        animation_cover.finished.connect(lambda: exec_finished() if exec_finished else None)
        animation_cover.finished.connect(lambda: self.animation_buffer.remove(animation_cover))

    def switch_widgets(self):
        widgets = [self.ui.horizontal_layout.itemAt(i).widget() for i in range(self.ui.horizontal_layout.count())]

        for widget in reversed(widgets):
            self.ui.horizontal_layout.removeWidget(widget)
            self.ui.horizontal_layout.addWidget(widget)
