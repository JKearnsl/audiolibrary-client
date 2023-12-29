from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QGraphicsDropShadowEffect


class UiAuthWindow(object):
    def setup_ui(self, window: QtWidgets.QWidget):
        window.setObjectName("window")
        window.resize(800, 600)
        window.setMinimumWidth(500)
        window.setMinimumHeight(400)
        window.setMaximumWidth(1920)
        window.setMaximumHeight(1080)
        window.setStyleSheet("""
            QLabel {
                color:  #1a3f13;
                font-weight: bold;
                font-size: 14px;
            }
            
            QWidget#window {
                background-color: rgb(220, 226, 218);
                border: none;
            }
        """)  # old background #dce29f
        self.horizontalLayout = QtWidgets.QHBoxLayout(window)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Основной макет
        self.leftVerticalLayout = QtWidgets.QVBoxLayout()
        self.leftVerticalLayout.setObjectName("leftVerticalLayout")
        self.leftVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.leftVerticalLayout.addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                  QtWidgets.QSizePolicy.Policy.Expanding)
        )
        self.horizontalLayout.addLayout(self.leftVerticalLayout)

        self.mainVerticalLayout = QtWidgets.QVBoxLayout()
        self.mainVerticalLayout.setObjectName("mainVerticalLayout")
        self.mainVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVerticalLayout.addItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        )
        self.horizontalLayout.addLayout(self.mainVerticalLayout)
        self.secondVerticalLayout = QtWidgets.QVBoxLayout()
        self.secondVerticalLayout.setObjectName("secondVerticalLayout")
        self.secondVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.addLayout(self.secondVerticalLayout)
        self.secondVerticalLayout.addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                  QtWidgets.QSizePolicy.Policy.Expanding)
        )
        window.setLayout(self.horizontalLayout)

        # Макет для формы авторизации
        self.authBox = QtWidgets.QGroupBox(window)
        self.authBox.setObjectName("authBox")
        self.authBox.setMaximumSize(QtCore.QSize(350, 350))
        self.authBox.setContentsMargins(5, 5, 5, 5)
        self.authBox.setStyleSheet("""
            QGroupBox {
                background-color: #eef2db;
                border: 1px solid #eef2db;
                border-radius: 10px;
            }
        """)
        self.authBox.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QtGui.QColor("#c0cfaf"),
            offset=QtCore.QPointF(0, 0)
        ))
        self.authBoxLayout = QtWidgets.QVBoxLayout()
        self.authBoxLayout.setObjectName("authBoxLayout")
        self.authBoxLayout.setContentsMargins(5, 5, 5, 5)
        self.authBox.setLayout(self.authBoxLayout)
        self.mainVerticalLayout.addWidget(self.authBox)

        # Заголовок формы авторизации
        self.authTitleLabel = QtWidgets.QLabel(window)
        self.authTitleLabel.setObjectName("authTitleLabel")
        self.authTitleLabel.setText("Авторизация")
        self.authTitleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.authTitleLabel.setStyleSheet("""
            QLabel {
                font-size: 24px;
            }
        """)
        self.authTitleLabel.setContentsMargins(5, 5, 5, 10)
        self.authBoxLayout.addItem(QtWidgets.QSpacerItem(
            10, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.MinimumExpanding
        ))
        self.authBoxLayout.addWidget(self.authTitleLabel)

        # Ответ сервера
        self.authResponseLabel = QtWidgets.QLabel(window)
        self.authResponseLabel.setObjectName("authResponseLabel")
        self.authResponseLabel.setWordWrap(True)
        self.authResponseLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.authResponseLabel.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: red;
            }
        """)
        self.authResponseLabel.hide()
        self.authBoxLayout.addWidget(self.authResponseLabel)

        # Форма авторизации
        self.authFormHorizontalLayout = QtWidgets.QHBoxLayout()
        self.authFormHorizontalLayout.setObjectName("authFormHorizontalLayout")
        self.authFormHorizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.authFormBox = QtWidgets.QGroupBox(self.authBox)
        self.authFormBox.setObjectName("authFormBox")
        self.authFormBox.setMaximumSize(QtCore.QSize(300, 400))
        self.authFormBoxLayout = QtWidgets.QVBoxLayout()
        self.authFormBoxLayout.setObjectName("authFormBoxLayout")
        self.authFormBoxLayout.setContentsMargins(10, 10, 10, 0)
        self.authFormBoxLayout.setProperty("spacing", 12)
        self.authFormBox.setLayout(self.authFormBoxLayout)

        self.authFormHorizontalLayout.addWidget(self.authFormBox)
        self.authBoxLayout.addLayout(self.authFormHorizontalLayout)

        # Поля
        self.login_line_edit = QtWidgets.QLineEdit()
        self.login_line_edit.setObjectName("loginLineEdit")
        self.login_line_edit.setPlaceholderText("Логин")
        self.login_line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #fff;
                border-radius: 5px;
                padding: 5px;
                color:  #1a3f13;
                font-weight: bold;
                font-size: 14px;
            }        
        """)
        self.login_line_edit.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=5,
            color=QtGui.QColor("#949a5e"),
            offset=QtCore.QPointF(0, 0)
        ))

        self.password_line_edit = QtWidgets.QLineEdit()
        self.password_line_edit.setObjectName("passwordLineEdit")
        self.password_line_edit.setPlaceholderText("Пароль")
        self.password_line_edit.setMaxLength(32)
        self.password_line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #fff;
                border-radius: 5px;
                padding: 5px;
                color:  #1a3f13;
                font-weight: bold;
                font-size: 14px;
            }        
        """)
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_line_edit.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=5,
            color=QtGui.QColor("#949a5e"),
            offset=QtCore.QPointF(0, 0)
        ))

        self.repeat_password_line_edit = QtWidgets.QLineEdit()
        self.repeat_password_line_edit.setObjectName("repeatPasswordLineEdit")
        self.repeat_password_line_edit.setPlaceholderText("Повторите пароль")
        self.repeat_password_line_edit.setMaxLength(32)
        self.repeat_password_line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #fff;
                border-radius: 5px;
                padding: 5px;
                color:  #1a3f13;
                font-weight: bold;
                font-size: 14px;
            }        
        """)
        self.repeat_password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.repeat_password_line_edit.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=5,
            color=QtGui.QColor("#949a5e"),
            offset=QtCore.QPointF(0, 0)
        ))

        self.signup_button = QtWidgets.QPushButton()
        self.signup_button.setObjectName("signupButton")
        self.signup_button.setText("Зарегистрироваться")
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: #729037;
                color: #dce29f;
                font-weight: bold;
                font-size: 16px;
       
                border-radius: 5px;
                padding: 5px;
                margin-top: 5px;
            }
            
            QPushButton:hover {
                background-color: #9ab740;
                color: #fff;
            }
            
            QPushButton:pressed {
                background-color: #729037;
                color: #dce29f;
            }
            
        """)
        self.signup_button.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QtGui.QColor("#93a63e"),
            offset=QtCore.QPointF(0, 0)
        ))

        self.signin_button = QtWidgets.QPushButton()
        self.signin_button.setObjectName("signinButton")
        self.signin_button.setText("Авторизоваться")
        self.signin_button.setStyleSheet("""
            QPushButton {
                background-color: #729037;
                color: #dce29f;
                font-weight: bold;
                font-size: 16px;
       
                border-radius: 5px;
                padding: 5px;
                margin-top: 5px;
            }
            
            QPushButton:hover {
                background-color: #9ab740;
                color: #fff;
            }
            
            QPushButton:pressed {
                background-color: #729037;
                color: #dce29f;
            }
            
        """)
        self.signin_button.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=10,
            color=QtGui.QColor("#93a63e"),
            offset=QtCore.QPointF(0, 0)
        ))
        self.authFormBoxLayout.addWidget(self.login_line_edit)
        self.authFormBoxLayout.addWidget(self.password_line_edit)
        self.authFormBoxLayout.addWidget(self.repeat_password_line_edit)
        self.authFormBoxLayout.addWidget(self.signup_button)
        self.authFormBoxLayout.addWidget(self.signin_button)

        # Ссылки
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.switchAuthStateLabel = QtWidgets.QLabel(self.authBox)
        self.switchAuthStateLabel.setObjectName("switchAuthStateLabel")
        self.switchAuthStateLabel.setText("Регистрация")
        self.switchAuthStateLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.switchAuthStateLabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.switchAuthStateLabel.setStyleSheet("""
            QLabel {
                color: #a4b096;
                text-decoration: underline;
                font-size: 15px;
            }
        """)
        self.horizontalLayout_2.addWidget(self.switchAuthStateLabel)
        self.authBoxLayout.addItem(self.horizontalLayout_2)

        self.authBoxLayout.addItem(
            QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        )

        self.mainVerticalLayout.addItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        )

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Login"))
