from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

from audiolibrary.views.widgets import WidgetsFactory


class UiAuthWindow(object):
    def setup_ui(self, window: QtWidgets.QWidget, widgets_factory: WidgetsFactory):
        window.setObjectName("window")
        window.resize(800, 500)
        window.setMinimumWidth(500)
        window.setMinimumHeight(400)
        window.setMaximumWidth(1920)
        window.setMaximumHeight(1080)
        window.setStyleSheet("""
            QLabel {
                color: $TEXT_PRIMARY;
                font-weight: bold;
                font-size: 14px;
            }
            
            QWidget#window {
                background-color: $BG1;
                border: none;
            }
        """.replace(
            "$BG1", widgets_factory.theme.first_background
        ).replace(
            "$TEXT_PRIMARY", widgets_factory.theme.text_primary
        ))
        horizontal_layout = QtWidgets.QHBoxLayout(window)
        horizontal_layout.setObjectName("horizontal_layout")
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setSpacing(0)
        self.horizontal_layout = horizontal_layout

        # Макет колонки формы
        form_frame = QtWidgets.QFrame(window)
        form_frame.setObjectName("form_frame")
        form_frame.setMaximumWidth(350)

        self.form_column = QtWidgets.QVBoxLayout(form_frame)
        self.form_column.setObjectName("form_column")
        self.form_column.setContentsMargins(40, 40, 40, 40)
        self.form_column.addItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        )
        horizontal_layout.addWidget(form_frame)

        # Макет для формы авторизации
        form_box = QtWidgets.QGroupBox(window)
        form_box.setObjectName("form_box")
        form_box.setMaximumSize(QtCore.QSize(350, 350))
        form_box.setContentsMargins(5, 5, 5, 5)
        form_box.setStyleSheet("""
            QGroupBox {
                background-color: transparent;
                border: none;
                outline: none;
            }
        """)
        form_box_layout = QtWidgets.QVBoxLayout()
        form_box_layout.setObjectName("form_box_layout")
        form_box_layout.setContentsMargins(5, 5, 5, 5)
        form_box_layout.setSpacing(20)
        form_box_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        form_box.setLayout(form_box_layout)
        self.form_column.addWidget(form_box)
        self.form_column.addItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        )

        # Заголовок формы авторизации
        self.title_label = widgets_factory.heading1()
        self.title_label.setObjectName("title_label")
        self.title_label.setText("Аутентификация")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setContentsMargins(5, 5, 5, 10)
        form_box_layout.addWidget(self.title_label)


        # Ответ сервера
        self.response_label = QtWidgets.QLabel(window)
        self.response_label.setObjectName("response_label")
        self.response_label.setWordWrap(True)
        self.response_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.response_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: red;
            }
        """)
        self.response_label.hide()
        form_box_layout.addWidget(self.response_label)

        # Форма полей ввода
        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(0, 10, 0, 10)
        form_layout.setSpacing(15)
        form_box_layout.addLayout(form_layout)

        # Поля
        self.username_line_edit = widgets_factory.line_edit()
        self.username_line_edit.add_style("""
            QLineEdit {
                background-color: $BG2;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
        """.replace(
            "$BG2", widgets_factory.theme.second_background
        ))
        self.username_line_edit.setPlaceholderText("Имя пользователя")

        self.password_line_edit = widgets_factory.line_edit()
        self.password_line_edit.setStyleSheet(self.username_line_edit.styleSheet())
        self.password_line_edit.setPlaceholderText("Пароль")
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.repeat_password_line_edit = widgets_factory.line_edit()
        self.repeat_password_line_edit.setStyleSheet(self.username_line_edit.styleSheet())
        self.repeat_password_line_edit.setPlaceholderText("Повторите пароль")
        self.repeat_password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        # Кнопки
        sign_layout = QtWidgets.QHBoxLayout()
        column_btn = QtWidgets.QVBoxLayout()
        sign_layout.addLayout(column_btn)

        self.signup_button = widgets_factory.primary_button()
        self.signup_button.setText("Зарегистрироваться")
        self.signup_button.setFixedWidth(150)
        self.signup_button.add_style("""
            QPushButton {
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
        """)

        column_btn.addWidget(self.signup_button)

        self.signin_button = widgets_factory.primary_button()
        self.signin_button.setFixedWidth(100)
        self.signin_button.setText("Войти")
        self.signin_button.add_style("""
            QPushButton {
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
        """)
        column_btn.addWidget(self.signin_button)

        form_layout.addWidget(self.username_line_edit)
        form_layout.addWidget(self.password_line_edit)
        form_layout.addWidget(self.repeat_password_line_edit)

        form_box_layout.addLayout(sign_layout)

        # Poster panel
        self.poster_panel = QtWidgets.QFrame()
        self.poster_panel.setObjectName("poster_panel")
        self.poster_panel.setStyleSheet("""
            QFrame#poster_panel {
                background-color: $BG3;
                border: none;
            }
        """.replace(
            "$BG3", widgets_factory.theme.third_background
        ).replace(
            "$BG1", widgets_factory.theme.first_background
        ))
        horizontal_layout.addWidget(self.poster_panel)

        # Poster Content
        poster_layout = QtWidgets.QVBoxLayout(self.poster_panel)
        poster_layout.setObjectName("poster_layout")
        poster_layout.setContentsMargins(50, 0, 50, 0)
        poster_layout.setSpacing(30)
        poster_layout.addStretch(1)

        poster_header = widgets_factory.heading1(
            "...",
            widgets_factory.theme.text_tertiary
        )
        poster_header.setObjectName("poster_header")
        poster_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.poster_header = poster_header
        poster_layout.addWidget(poster_header)

        poster_text_layout = QtWidgets.QHBoxLayout()
        poster_text = widgets_factory.label("...", widgets_factory.theme.text_tertiary)
        poster_text.setObjectName("poster_text")
        poster_text.setWordWrap(True)
        poster_text.setMaximumWidth(350)
        poster_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.poster_text = poster_text
        poster_text_layout.addWidget(poster_text)
        poster_layout.addLayout(poster_text_layout)

        button_layout = QtWidgets.QHBoxLayout()
        poster_button = widgets_factory.outline_button()
        poster_button.setObjectName("poster_button")
        poster_button.setMaximumWidth(100)
        poster_button.setText("...")
        button_layout.addWidget(poster_button)
        self.poster_button = poster_button
        poster_layout.addLayout(button_layout)

        poster_layout.addStretch(1)



        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Auth"))
