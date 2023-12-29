from PyQt6 import QtWidgets

from audiolibrary.api_service import ErrorType
from audiolibrary.utils.observer import DObserver
from audiolibrary.utils.ts_meta import TSMeta
from audiolibrary.views.auth.static_ui import UiAuthWindow


class AuthView(QtWidgets.QWidget, DObserver, metaclass=TSMeta):

    def __init__(self, controller, model, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.model = model

        self.ui = UiAuthWindow()
        self.ui.setup_ui(self)
        self.is_signin = True

        # Регистрация представлений
        self.model.add_observer(self)

        # События
        self.ui.switchAuthStateLabel.mousePressEvent = lambda event: self.switch_auth_state(not self.is_signin)
        self.ui.signin_button.clicked.connect(self.signin_clicked)
        self.ui.signup_button.clicked.connect(self.signup_clicked)

    def model_changed(self):
        self.ui.authResponseLabel.clear()
        self.ui.authResponseLabel.hide()

    def model_loaded(self):
        self.switch_auth_state(self.is_signin)

    def error_handler(self, error):
        self.ui.authResponseLabel.show()
        if error.type is ErrorType.MESSAGE:
            self.ui.authResponseLabel.setText(error.content)
        else:
            self.ui.authResponseLabel.setText('\n'.join(
                [
                    f"{el.field}: {el.message}" for el in error.content
                ]
            ))

    def signin_clicked(self):
        login = self.ui.login_line_edit.text()
        password = self.ui.password_line_edit.text()
        self.controller.signin(login, password)

    def signup_clicked(self):
        login = self.ui.login_line_edit.text()
        password = self.ui.password_line_edit.text()
        repeat_password = self.ui.repeat_password_line_edit.text()
        self.controller.signup(login, password, repeat_password)

    def signin_form(self):
        self.ui.authTitleLabel.setText("Авторизация")
        self.ui.switchAuthStateLabel.setText("Регистрация")

        self.ui.password_line_edit.clear()
        self.ui.repeat_password_line_edit.clear()
        self.ui.signup_button.hide()
        self.ui.repeat_password_line_edit.hide()

        self.ui.signin_button.show()

    def signup_form(self):
        self.ui.authTitleLabel.setText("Регистрация")
        self.ui.switchAuthStateLabel.setText("Авторизация")

        self.ui.password_line_edit.clear()
        self.ui.repeat_password_line_edit.clear()
        self.ui.signin_button.hide()

        self.ui.repeat_password_line_edit.show()
        self.ui.signup_button.show()

    def switch_auth_state(self, is_signin: bool):
        self.is_signin = is_signin
        if is_signin:
            self.signin_form()
        else:
            self.signup_form()
