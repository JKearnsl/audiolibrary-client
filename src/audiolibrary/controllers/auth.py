from audiolibrary.models.auth import AuthModel
from audiolibrary.views.auth import AuthView
from audiolibrary.views.widgets import WidgetsFactory


class AuthController:

    def __init__(self, model: 'AuthModel', widgets_factory: 'WidgetsFactory', app_controller):
        self.model = model
        self.widgets_factory = widgets_factory
        self.app_controller = app_controller
        self.view = AuthView(self, self.model)
        self.view.model_loaded()
        self.view.show()

    def signin(self, login: str, password: str):
        if self.model.signin(login, password):
            self.view.close()
            self.app_controller.main()

    def signup(self, login: str, password: str, repeat_password: str):
        if self.model.signup(login, password, repeat_password):
            self.view.signin_form()
